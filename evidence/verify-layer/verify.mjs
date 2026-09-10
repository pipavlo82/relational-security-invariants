// ─────────────────────────────────────────────────────────────────────────────
// trustless-ai wallet · verify-don't-trust layer (sketch, v0)
//
// A normal wallet TRUSTS the RPC's answer for a balance. This PROVES it: we take
// the RPC's eth_getProof (an EIP-1186 Merkle-Patricia proof of the account) and
// verify it against the block's stateRoot — so a lying RPC cannot forge a balance
// without breaking keccak.
//
// The trust boundary, stated honestly:
//   • The block HEADER (hence stateRoot) here still comes from the RPC. A full
//     trustless client gets the header from a consensus light client (sync
//     committee), removing that last trust. Swapping the header source is the
//     ONLY remaining step to full trustlessness — the state proof below is done.
//   • Given a stateRoot, the ACCOUNT STATE is proven, not trusted.
//
// Two independent defenses, both demonstrated below with prove-it-can-fail:
//   (A) BINDING   — keccak(proof[0]) must equal the block's stateRoot. Stops an
//                   RPC handing a self-consistent proof rooted at a fake state.
//   (B) MPT PROOF — the Merkle-Patricia path for keccak(address) must verify.
//                   Stops any tampered node / forged balance.
// ─────────────────────────────────────────────────────────────────────────────
import { keccak_256 } from '@noble/hashes/sha3.js';
import { RLP } from '@ethereumjs/rlp';
import { hexToBytes, bytesToHex, bytesToBigInt, equalsBytes, setLengthLeft, bigIntToBytes } from '@ethereumjs/util';
import { verifyMerkleProof } from '@ethereumjs/mpt';
import fs from 'node:fs';

const keccak = (b) => keccak_256(b);
const KEY = fs.readFileSync(process.env.HOME + '/.claude/alchemy_key', 'utf8').trim();
const RPC = `https://eth-mainnet.g.alchemy.com/v2/${KEY}`;

async function rpc(method, params) {
  const r = await fetch(RPC, {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }),
  });
  const j = await r.json();
  if (j.error) throw new Error(`${method}: ${JSON.stringify(j.error)}`);
  return j.result;
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

const fmt = (b) => `${b} wei  (${(Number(b) / 1e18).toFixed(4)} ETH)`;

async function main() {
  const WETH = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'; // holds all wrapped ETH — visible balance
  console.log('trustless-ai · verify-don\'t-trust layer (v0)\n');

  // ── 1) HONEST PATH — prove the balance ───────────────────────────────────────
  const r = await verifyAccount(WETH);
  console.log(`account   ${r.address}`);
  console.log(`block     #${r.block}   stateRoot ${r.stateRoot}`);
  console.log(`PROVEN    balance = ${fmt(r.provenBalanceWei)}   nonce=${r.proven.nonce}`);
  console.log(`bound to header stateRoot?  ${r.boundToHeader ? 'YES' : 'NO'}`);
  console.log(`RPC-claimed balance matches PROVEN?  ${r.claimMatchesProof ? 'YES' : 'NO'}`);
  console.log(`==> ${r.verified ? '✅ VERIFIED (proven, not trusted)' : '❌ REJECTED'}\n`);

  // ── 2) prove-it-can-fail A: forged state root (RPC roots the proof elsewhere) ─
  const wrongRoot = hexToBytes(r.stateRoot); wrongRoot[0] ^= 0x01; // flip one bit of the expected root
  const a = await checkAccountProof(wrongRoot, r.address, r.raw.accountProof);
  console.log(`[tamper A] verify against a WRONG stateRoot (1 bit flipped):`);
  console.log(`  bound to header?  ${a.boundToHeader ? 'YES' : 'NO'}  ==> ${a.boundToHeader ? '❌ (should reject!)' : '✅ REJECTED (binding caught it)'}\n`);

  // ── 3) prove-it-can-fail B: tampered proof node (forge the balance) ───────────
  const tampered = r.raw.accountProof.map((n) => Uint8Array.from(n));
  tampered[tampered.length - 1][5] ^= 0x01; // corrupt a byte inside the account LEAF node
  let rejectedB = false, note = '';
  try {
    const b = await checkAccountProof(r.raw.stateRoot, r.address, tampered);
    // if it didn't throw, the tampered leaf no longer hashes into its parent → verify returns null/other
    rejectedB = !(b.boundToHeader && b.proven && b.proven.balance === r.provenBalanceWei);
    note = b.proven ? `proven balance now ${fmt(b.proven.balance)}` : 'proof no longer resolves the account';
  } catch (e) {
    rejectedB = true; note = 'MPT verification threw: ' + e.message.split('\n')[0].slice(0, 80);
  }
  console.log(`[tamper B] corrupt one byte inside the account leaf node:`);
  console.log(`  ${note}`);
  console.log(`  ==> ${rejectedB ? '✅ REJECTED (MPT proof caught it)' : '❌ (should reject!)'}\n`);

  // ── 4) STORAGE proof — verify a contract variable, chained state→account→slot ──
  const s = await verifyStorage(WETH, 2); // WETH9 slot 2 = decimals (18)
  console.log(`[storage] WETH slot 2 (decimals):  proven=${s.provenValue}  RPC-claimed=${s.claimed}`);
  console.log(`  chain of custody: header→account.storageRoot→slot  = ${s.boundToHeader && s.boundToAccount ? 'intact' : 'BROKEN'}`);
  console.log(`  ==> ${s.verified ? '✅ VERIFIED (storage proven, not trusted)' : '❌ REJECTED'}\n`);

  // ── TRUST-TIER DISCLOSURE — what each answer is actually worth (marker travels with the value) ──
  console.log('trust tier (what each answer is actually worth — never collapse to one ✓):');
  console.log(`  state   : ${r.trust.state}   — MPT proof verified against stateRoot; no circuit trusted`);
  console.log(`  header  : ${r.trust.header}  — stateRoot taken from the RPC in v0 (the one open seam)`);
  console.log(`  overall : ${r.trust.overall}`);
  console.log(`            upgrade the header via L1 — a light client RE-DERIVES, a ZK light client ATTESTS — for fully trustless.`);

  // ── the L1 seam is pluggable: swapping the header source IS the whole L1 upgrade (L2 untouched) ──
  try { await new LightClientHeaderSource().getStateRoot(); }
  catch (e) {
    console.log(`\nL1 header source is pluggable:  now = RpcHeaderSource (RPC-TRUSTED)`);
    console.log(`  drop-in LightClientHeaderSource → header flips to RE-DERIVED, L2 unchanged. Status: ${e.message.split('—')[0].trim()}`);
  }
}
main().catch((e) => { console.error('ERROR', e); process.exit(1); });
