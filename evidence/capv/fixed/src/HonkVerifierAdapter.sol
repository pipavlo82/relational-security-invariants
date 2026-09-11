// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.20;

import {IVerifier} from "./IVerifier.sol";
import {Verdict} from "./IConfidentialPolicyVerdict.sol";

/// @notice Minimal view of the bb-generated UltraHonk verifier.
interface IHonkVerifier {
    function verify(bytes calldata proof, bytes32[] calldata publicInputs) external view returns (bool);
}

/// @notice Adapts the Noir/UltraHonk allowlist verifier to the ERC's `IVerifier`. It serializes the
/// Verdict fields that are the circuit's public inputs and calls the generated Honk verifier.
///
/// The circuit's public inputs, in `main()` order, are 40 elements:
///   [0] agentId, [1] domainId, [2] policyRoot, [3..34] the 32 bytes of actionCommitment
///   (each byte as a field element), [35] nullifier, [36] decision, [37] policyKind, [38] executor,
///   [39] expiry.
/// `executor` is a committed circuit input (the proof binds to it, per the spec's Security
/// Considerations). `policyKind` is committed too, so the four-state taxonomy cannot be asserted
/// at the boundary without the proof having established it.
///
/// `expiry` was previously omitted here, with a comment claiming that was deliberate because the
/// Guard enforces the time check on chain. That was wrong. ERC-8354 requires every `Verdict` field
/// to be a public input and forbids any of them sitting in the private witness, and while the
/// Guard's check does establish that a supplied expiry is still live, it does not establish that
/// this was the expiry the circuit authorized. The same proof verified under any expiry the
/// submitter chose. It is now public input [39]: proving at one expiry and verifying at another
/// fails in the verifier's reduction step.
///
/// All three circuits (allowlist ALLOW, denylist, allowlist non-membership) share this layout;
/// only the constant each asserts for `policyKind` differs.
contract HonkVerifierAdapter is IVerifier {
    IHonkVerifier public immutable honk;
    /// @notice The program key this adapter accepts. Set at deployment to the wrapped verifier's
    /// own VK_HASH so a domain that rotates onto a different program (a different verifier
    /// contract, hence a different key) cannot have its old proofs accepted by this adapter
    /// instance -- the registry's declared `programKey` and this value must match, or verification
    /// fails closed.
    bytes32 public immutable expectedProgramKey;

    constructor(IHonkVerifier _honk, bytes32 _expectedProgramKey) {
        honk = _honk;
        expectedProgramKey = _expectedProgramKey;
    }

    /// @param programKey MUST equal `expectedProgramKey`, or verification fails closed (returns
    /// false, same convention as a malformed proof -- never reverts on a mismatch).
    /// @param publicInputs abi.encode(Verdict) as passed by the Guard.
    function verifyProof(
        bytes32 programKey,
        bytes calldata publicInputs,
        bytes calldata proof
    )
        external
        view
        returns (bool)
    {
        if (programKey != expectedProgramKey) return false;
        Verdict memory v = abi.decode(publicInputs, (Verdict));
        return honk.verify(proof, _toPublicInputs(v));
    }

    /// @notice The 40-element public-input vector the circuit expects, from a Verdict.
    function _toPublicInputs(Verdict memory v) internal pure returns (bytes32[] memory pi) {
        pi = new bytes32[](40);
        pi[0] = bytes32(v.agentId);
        pi[1] = v.domainId;
        pi[2] = v.policyRoot;
        for (uint256 i = 0; i < 32; i++) {
            pi[3 + i] = bytes32(uint256(uint8(v.actionCommitment[i])));
        }
        pi[35] = v.nullifier;
        pi[36] = bytes32(uint256(v.decision));
        pi[37] = bytes32(uint256(v.policyKind));
        pi[38] = bytes32(uint256(uint160(v.executor)));
        pi[39] = bytes32(uint256(v.expiry));
    }
}
