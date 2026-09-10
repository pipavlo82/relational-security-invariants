import { keccak_256 } from '@noble/hashes/sha3.js';
import { RLP } from '@ethereumjs/rlp';
import { hexToBytes, bytesToHex, bytesToBigInt, equalsBytes, setLengthLeft, bigIntToBytes } from '@ethereumjs/util';
import { verifyMerkleProof } from '@ethereumjs/mpt';
import fs from 'node:fs';

const keccak = (b) => keccak_256(b);
let supplied;
async function rpc(method,params) {
 if(method==='eth_getBlockByNumber') return supplied.header;
 if(method==='eth_getProof') return supplied.response;
 throw new Error('unimplemented transport');
}
// Core: verify an account against a KNOWN stateRoot. Returns the proven account,
// or throws (invalid MPT proof), or {boundToHeader:false} (proof roots elsewhere).
async function checkAccountProof(expectedStateRoot, address, accountProofBytes) {
  // (A) BINDING — the proof's top node must hash to the header's stateRoot.
  const boundToHeader = equalsBytes(keccak(accountProofBytes[0]), expectedStateRoot);

  // (B) MPT PROOF — verify the Merkle-Patricia path for keccak(address).
  const key = keccak(hexToBytes(address));
  const value = await verifyMerkleProof(key, accountProofBytes); // throws if tampered; null = non-existence

  let proven = null;
  if (value !== null) {
    const [nonce, balance, storageRoot, codeHash] = RLP.decode(value);
    proven = {
      nonce: bytesToBigInt(nonce),
      balance: bytesToBigInt(balance),
      storageRoot: bytesToHex(storageRoot),
      codeHash: bytesToHex(codeHash),
    };
  }
  return { boundToHeader, proven };
}

// ── L1 header sources (pluggable) ────────────────────────────────────────────
// The state proof (L2) verifies against whatever stateRoot a header source returns; what changes between
// sources is HOW MUCH you trust that stateRoot. This is the L1/L2 seam made concrete: swap the source, the
// state proof is untouched. The proof itself can come from any RPC — we verify it against the trusted root.
class RpcHeaderSource {
  async getStateRoot(blockTag = 'finalized') {
    const block = await rpc('eth_getBlockByNumber', [blockTag, false]);
    return {
      stateRoot: hexToBytes(block.stateRoot), blockNumber: block.number,
      trust: { tier: 'RPC-TRUSTED', note: 'stateRoot taken from the RPC on faith — the one open seam' },
    };
  }
}
// The drop-in that closes the seam: a consensus light client. Bootstrap from a weak-subjectivity checkpoint,
// verify sync-committee signatures, return the execution stateRoot from a light-client-verified header
// (post-Capella LightClientHeader.execution.stateRoot). Trust then reduces to the checkpoint root — far
// weaker than trusting an RPC, and RE-DERIVED (you check the signatures), not circuit-attested.
class LightClientHeaderSource {
  async getStateRoot() {
    throw new Error('LightClientHeaderSource not wired yet (L1) — @lodestar/light-client: bootstrap from a ' +
      'checkpoint root, verify the sync committee, take the verified execution stateRoot. Needs a beacon ' +
      'node exposing /eth/v1/beacon/light_client/*. This class is the exact drop-in point.');
  }
}

async function verifyAccount(address, blockTag = 'finalized', headerSource = new RpcHeaderSource()) {
  const { stateRoot, blockNumber, trust: headerTrust } = await headerSource.getStateRoot(blockTag);
  const res = await rpc('eth_getProof', [address, [], blockNumber]); // proof may come from ANY RPC — verified below
  const accountProof = res.accountProof.map(hexToBytes);
  const { boundToHeader, proven } = await checkAccountProof(stateRoot, address, accountProof);

  // Cross-check: does the RPC's own claimed balance match what the PROOF proves?
  const claimedBalance = BigInt(res.balance);
  const provenBalance = proven ? proven.balance : 0n;
  const claimMatchesProof = claimedBalance === provenBalance;

  const ok = boundToHeader && claimMatchesProof;
  return {
    verified: ok,
    address, block: BigInt(blockNumber), stateRoot: bytesToHex(stateRoot),
    boundToHeader, claimMatchesProof,
    provenBalanceWei: provenBalance, provenBalanceEth: Number(provenBalance) / 1e18,
    // TRUST-TIER DISCLOSURE — the marker travels with the value (never collapse these into one ✓).
    // Verification has a KIND: RE-DERIVED (you checked the rule yourself, no circuit) vs PROOF-ATTESTED
    // (you verified a ZK proof, trusting the circuit is faithful) vs RPC-TRUSTED (took the RPC's word).
    // `header` now reflects the chosen L1 source — swap the header source and this label changes.
    trust: {
      state: ok ? 'RE-DERIVED' : 'UNVERIFIED', // MPT proof, no circuit trusted
      header: headerTrust.tier,                // from the L1 header source (RPC-TRUSTED today)
      overall: ok ? `state-proven / header ${headerTrust.tier}` : 'rejected',
    },
    proven, raw: { block: { number: blockNumber, stateRoot: bytesToHex(stateRoot) }, res, accountProof, stateRoot },
  };
}

// Verify a STORAGE slot — chains proof-of-custody: state root → account.storageRoot → slot value.
// (Token balances are just a storage slot: keccak(pad32(holder) ++ pad32(mappingSlot)).)
async function verifyStorage(address, slot, blockTag = 'finalized') {
  const block = await rpc('eth_getBlockByNumber', [blockTag, false]);
  const slotHex = bytesToHex(setLengthLeft(bigIntToBytes(BigInt(slot)), 32));
  const res = await rpc('eth_getProof', [address, [slotHex], block.number]);
  const stateRoot = hexToBytes(block.stateRoot);
  const accountProof = res.accountProof.map(hexToBytes);
  const { boundToHeader, proven } = await checkAccountProof(stateRoot, address, accountProof); // → storageRoot
  const storageRoot = hexToBytes(proven.storageRoot);

  const sp = res.storageProof[0];
  const sProof = sp.proof.map(hexToBytes);
  const storageKey = keccak(setLengthLeft(bigIntToBytes(BigInt(slot)), 32));
  const boundToAccount = equalsBytes(keccak(sProof[0]), storageRoot); // storage proof roots at account.storageRoot
  const leaf = await verifyMerkleProof(storageKey, sProof);           // throws if tampered
  const provenValue = leaf === null ? 0n : bytesToBigInt(RLP.decode(leaf));

  return {
    verified: boundToHeader && boundToAccount && provenValue === BigInt(sp.value),
    slot: BigInt(slot), provenValue, claimed: BigInt(sp.value),
    boundToHeader, boundToAccount, block: BigInt(block.number),
  };
}

export async function observe(input,variant='canonical') {
 supplied=input;
 const address=variant==='address' ? input.response.address : input.address;
 let r;
 try {r=await verifyAccount(address);} catch(e) {
  if(e.constructor.name!=='EthereumJSError' || e.message!=='Invalid proof provided') throw e;
  return {verified:false,boundToHeader:null,claimMatchesProof:null,provenBalanceWei:null,accountExists:null,stateTrust:'MPT-REJECTED',headerTrust:'RPC-TRUSTED',overall:'rejected',headerAuthority:'UNSUPPORTED',downstreamAuthority:'UNSUPPORTED'};
 }
 return {
  verified:r.verified,boundToHeader:r.boundToHeader,claimMatchesProof:r.claimMatchesProof,
  provenBalanceWei:r.provenBalanceWei.toString(),accountExists:r.proven!==null,
  stateTrust:r.trust.state,headerTrust:r.trust.header,overall:r.trust.overall,
  headerAuthority:'UNSUPPORTED',downstreamAuthority:'UNSUPPORTED'
 };
}
export {LightClientHeaderSource};
