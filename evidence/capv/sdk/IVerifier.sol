// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.20;

/// @notice ZK verifier for a domain's interpreter program.
interface IVerifier {
    function verifyProof(bytes32 programKey, bytes calldata publicInputs, bytes calldata proof)
        external
        view
        returns (bool);
}
