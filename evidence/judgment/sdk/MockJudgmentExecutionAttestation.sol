// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

import {IJudgmentExecutionAttestation} from "@agent-ercs/verify/ERC8299/IJudgmentExecutionAttestation.sol";

/// @title MockJudgmentExecutionAttestation
/// @notice Reference implementation of IJudgmentExecutionAttestation for local
///         testing only. "Verification" checks that the signature's keccak256
///         matches a deterministic derivation of the struct — not
///         production-grade EIP-712 verification. See agent-ercs's README on
///         interface vs. base-implementation vs. example/reference contracts.
contract MockJudgmentExecutionAttestation is IJudgmentExecutionAttestation {
    function verify(JudgmentExecutionAttestation calldata attestation, bytes calldata signature)
        external
        pure
        override
        returns (bool valid)
    {
        bytes32 expectedDigest = keccak256(abi.encode(attestation));
        // signature is the raw 32-byte keccak256 digest, not wrapped in EIP-712
        valid = signature.length == 32 && bytes32(signature) == expectedDigest;
    }

    function proofSystem() external pure override returns (string memory) {
        return "attestation/judgment";
    }
}
