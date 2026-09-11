// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.20;

import {IERC165} from "@openzeppelin/contracts/utils/introspection/IERC165.sol";

/// @notice The verdict envelope. EVERY field is a public input of the proving program.
struct Verdict {
    uint256 agentId;          // ERC-8004 Identity Registry token id
    bytes32 domainId;         // policy domain
    bytes32 policyRoot;       // ERC-7812 EvidenceDB root the decision was made against
    bytes32 actionCommitment; // commitment to the action being authorized (see PolicyAction)
    address executor;         // the address permitted to consume this verdict
    uint64  expiry;           // unix seconds, exclusive
    bytes32 nullifier;        // single-use, domain-scoped
    uint8   decision;         // 0 = DENY, 1 = ALLOW
    uint8   policyKind;       // which of the four states this verdict carries
}

/// @notice The four states a verdict can carry.
library PolicyKind {
    uint8 internal constant ALLOWED = 0;
    uint8 internal constant DENIED = 1;
    uint8 internal constant NOT_PERMITTED = 2;
    uint8 internal constant COULD_NOT_EVALUATE = 3;

    function agreesWithDecision(uint8 kind, uint8 decision) internal pure returns (bool) {
        return decision == 1
            ? kind == ALLOWED
            : (kind == DENIED || kind == NOT_PERMITTED || kind == COULD_NOT_EVALUATE);
    }
}

/// @notice Consume a confidential policy verdict: a ZK proof that an action was
/// evaluated against a committed secret policy and permitted.
interface IConfidentialPolicyVerdict is IERC165 {
    event VerdictConsumed(
        bytes32 indexed nullifier,
        uint256 indexed agentId,
        bytes32 indexed domainId,
        bytes32 policyRoot,
        bytes32 actionCommitment
    );

    /// @dev The domain declares an ERC-8004 Identity Registry and `agentId` does not exist in it.
    error AgentUnknown(uint256 agentId);
    error VerdictExpired(uint64 expiry);
    error VerdictReplayed(bytes32 nullifier);
    error ExecutorMismatch(address expected, address actual);
    error ExecutorAuthInvalid();
    error PolicyRootRejected(bytes32 root);
    error DomainInactive(bytes32 domainId);
    error VerdictDenied();
    error VerdictKindMismatch(uint8 decision, uint8 policyKind);
    error InvalidProof();

    function verify(Verdict calldata v, bytes calldata proof) external view returns (bool);
    function verdictDigest(Verdict calldata v) external view returns (bytes32);
    function consume(Verdict calldata v, bytes calldata proof) external;
    function consume(Verdict calldata v, bytes calldata proof, bytes calldata executorAuth) external;
    function isConsumed(bytes32 domainId, bytes32 nullifier) external view returns (bool);
}

/// @notice A contract gated by a policy verdict.
interface IPolicyGuarded {
    function policyDomain() external view returns (bytes32);
}
