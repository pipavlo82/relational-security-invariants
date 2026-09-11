// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

import {IBoundedAgentAction} from "@agent-ercs/metering/ERC8312/IBoundedAgentAction.sol";
import {IBudgetSubstrate} from "@agent-ercs/metering/ERC8312/IBudgetSubstrate.sol";

/// @title MockBudgetSubstrate
/// @notice Reference implementation of IBudgetSubstrate for local testing only.
///         Routes every envelope to the same cap=10000 USDC (mock address),
///         with cumulative spent tracked independently per envelope. A real
///         substrate would derive the bound from the capability structure.
///         This contract replicates IBoundedAgentAction state inline so it
///         can be deployed as a standalone mock without inheriting from a base.
contract MockBudgetSubstrate is IBudgetSubstrate {
    uint64 private _nextId;

    // Cap/asset are fixed for all envelopes in this mock.
    uint256 private constant DEFAULT_CAP = 10_000;
    address private constant USDC = address(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);

    struct InternalEnvelope {
        bytes32 id;
        address principal;
        bytes32 capabilityRoot;
        bytes32 cursorRoot;
        uint64 createdAt;
        uint64 expiresAt;
        Status status;
    }

    mapping(bytes32 id => InternalEnvelope) private _envelopes;
    mapping(bytes32 id => uint256) private _spent;

    /// @notice Deploy with id counter starting at 1.
    constructor() {
        _nextId = 1;
    }

    // ── IBoundedAgentAction (via IBudgetSubstrate inheritance) ──────────────

    function registerEnvelope(
        address principal,
        bytes32 capabilityRoot,
        uint64 expiresAt,
        bytes calldata /* initData */
    ) external override returns (bytes32 id) {
        id = keccak256(abi.encodePacked(address(this), _nextId++));
        require(_envelopes[id].createdAt == 0, "id collision");

        _envelopes[id] = InternalEnvelope({
            id: id,
            principal: principal,
            capabilityRoot: capabilityRoot,
            cursorRoot: bytes32(0),
            createdAt: uint64(block.timestamp),
            expiresAt: expiresAt,
            status: Status.Active
        });

        emit EnvelopeRegistered(id, principal, capabilityRoot);
    }

    function advanceCursor(
        bytes32 id,
        bytes calldata witness
    ) external override returns (bytes32 newCursor) {
        InternalEnvelope storage env = _requireActive(id);

        // Budget-substrate advance: decode witness as (uint256 delta),
        // increment spent, update cursorRoot = keccak256(abi.encode(spent)).
        uint256 delta = abi.decode(witness, (uint256));
        require(delta > 0, "delta must be positive");
        require(_spent[id] + delta <= DEFAULT_CAP, "exceeds cap");

        bytes32 prevCursor = env.cursorRoot;
        _spent[id] += delta;
        newCursor = keccak256(abi.encode(_spent[id]));
        env.cursorRoot = newCursor;

        emit EnvelopeAdvanced(id, prevCursor, newCursor);
    }

    function setStatus(bytes32 id, Status newStatus) external override {
        InternalEnvelope storage env = _envelopes[id];
        require(env.createdAt != 0, "unknown envelope");
        Status oldStatus = _effectiveStatus(env);
        env.status = newStatus;
        emit EnvelopeStatusChanged(id, oldStatus, newStatus);
    }

    function getEnvelope(bytes32 id) external view override returns (Envelope memory) {
        InternalEnvelope memory env = _envelopes[id];
        require(env.createdAt != 0, "unknown envelope");
        return Envelope({
            id: env.id,
            principal: env.principal,
            capabilityRoot: env.capabilityRoot,
            cursorRoot: env.cursorRoot,
            createdAt: env.createdAt,
            expiresAt: env.expiresAt,
            status: _effectiveStatus(env)
        });
    }

    function getCursor(bytes32 id) external view override returns (bytes32) {
        InternalEnvelope storage env = _envelopes[id];
        require(env.createdAt != 0, "unknown envelope");
        return env.cursorRoot;
    }

    function getStatus(bytes32 id) external view override returns (Status) {
        InternalEnvelope storage env = _envelopes[id];
        require(env.createdAt != 0, "unknown envelope");
        return _effectiveStatus(env);
    }

    function isActive(bytes32 id) external view override returns (bool) {
        InternalEnvelope storage env = _envelopes[id];
        if (env.createdAt == 0) return false;
        return _effectiveStatus(env) == Status.Active;
    }

    // ── IBudgetSubstrate ────────────────────────────────────────────────────

    function bound(bytes32 id) external view override returns (uint256 cap, address asset) {
        require(_envelopes[id].createdAt != 0, "unknown envelope");
        return (DEFAULT_CAP, USDC);
    }

    function spent(bytes32 id) external view override returns (uint256) {
        require(_envelopes[id].createdAt != 0, "unknown envelope");
        return _spent[id];
    }

    function remaining(bytes32 id) external view override returns (uint256) {
        InternalEnvelope storage env = _envelopes[id];
        require(env.createdAt != 0, "unknown envelope");
        if (_effectiveStatus(env) != Status.Active) return 0;
        return DEFAULT_CAP - _spent[id];
    }

    // ── Internals ────────────────────────────────────────────────────────────

    function _requireActive(bytes32 id) private view returns (InternalEnvelope storage) {
        InternalEnvelope storage env = _envelopes[id];
        require(env.createdAt != 0, "unknown envelope");
        require(_effectiveStatus(env) == Status.Active, "not active");
        return env;
    }

    function _effectiveStatus(InternalEnvelope memory env) private view returns (Status) {
        if (block.timestamp >= env.expiresAt && env.status == Status.Active) {
            return Status.Expired;
        }
        return env.status;
    }

    // ── ERC-165 ──────────────────────────────────────────────────────────────

    function supportsInterface(bytes4 interfaceId) external pure override returns (bool) {
        return interfaceId == type(IBudgetSubstrate).interfaceId
            || interfaceId == type(IBoundedAgentAction).interfaceId
            || interfaceId == 0x01ffc9a7;
    }
}
