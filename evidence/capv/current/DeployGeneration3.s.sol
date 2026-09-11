// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.20;

import {Script, console2} from "forge-std/Script.sol";
import {PolicyDomainRegistry} from "../src/PolicyDomainRegistry.sol";
import {ConfidentialPolicyVerdict} from "../src/ConfidentialPolicyVerdict.sol";
import {ProvableDenialAnchor} from "../src/ProvableDenialAnchor.sol";
import {IPolicyDomainRegistry} from "../src/IPolicyDomainRegistry.sol";
import {IVerifier} from "../src/IVerifier.sol";
import {HonkVerifierAdapter, IHonkVerifier} from "../src/HonkVerifierAdapter.sol";
import {HonkVerifier, VK_HASH as COMPOSED_VK_HASH} from "../src/verifier/HonkVerifier.sol";
import {DenyHonkVerifier, VK_HASH as DENY_VK_HASH} from "../src/verifier/DenyHonkVerifier.sol";
import {NotAllowedHonkVerifier, VK_HASH as NOT_ALLOWED_VK_HASH} from "../src/verifier/NotAllowedHonkVerifier.sol";
import {Verdict, PolicyKind} from "../src/IConfidentialPolicyVerdict.sol";

/// @notice Generation 3. Unlike generation 2, this moves every contract, because the circuits
/// themselves changed.
///
/// @dev PR #4 bound `expiry` as public input `[39]` on all three programs, which regenerated all
/// three verifying keys and every fixture. Three consequences chain from that:
///
///  1. The three deployed verifiers hold the pre-fix VK. Probing the live bytecode on 2026-09-02
///     found the old VK hash present in all three and the new one absent in all three, so the
///     addresses published as recompute-verifiable demonstrate the 39-input relation, which is the
///     relation where the same proof verifies under any expiry the submitter chooses. That is the
///     defect #4 exists to remove.
///  2. `HonkVerifierAdapter` now takes `expectedProgramKey` and fails closed on a mismatch (#5), so
///     every adapter has to be redeployed bound to its verifier's new VK.
///  3. `registerDomain` is once-only and carries `verifier` and `programKey`, so a domain cannot be
///     repointed at the new adapter in place. That forces a new registry, and `registry` is
///     `immutable` in both `ConfidentialPolicyVerdict` and `ProvableDenialAnchor`, so those move too.
///
/// Generation 2 is left live and unrevoked for the same reason generation 1 was: its addresses have
/// been independently recompute-verified by other people. What changes is which generation this
/// repository points at, and the README says plainly that generation 2 pins the pre-expiry relation.
///
/// `TransparentDenialAnchor` holds no registry reference and no verifier, so it is reused.
contract DeployGeneration3 is Script {
    address constant REGISTRAR = 0xb0175f56d4731C02aC9A30877fcD7c18C6af1858;

    bytes32 constant DENY_DOMAIN = bytes32(uint256(0x2a));
    bytes32 constant NOT_ALLOWED_DOMAIN = bytes32(uint256(0x2b));
    bytes32 constant COMPOSED_DOMAIN = 0x16079127bc55bd85d480837115b9bd82d26f03809c0bc4c6c80f7220836afad0;

    bytes32 constant DENY_ROOT = 0x053d4542d140ad2350a0ee79fae4a522821274e428bd881e7e803ecd816635ac;
    bytes32 constant NOT_ALLOWED_ROOT = 0x24e703f14986ec5abcb79d7292a4593b3370440fd4d1f2b6e51653e2e045707f;
    bytes32 constant COMPOSED_ROOT = 0x204a14dc3ab2fdead5450192caea7428c2751b53a95b57d22f93cccb61af19a8;

    uint64 constant MAX_ROOT_AGE = 1 hours;

    /// The expiry every regenerated fixture was proved at. Generation 2's script passed `0` on two
    /// legs and `1_700_003_600` on the third, which were free parameters then and are bound now, so
    /// carrying those constants across would fail verification at exactly the step this deploy
    /// exists to fix.
    uint64 constant FIXTURE_EXPIRY = 1900000000;

    bytes32 constant NOT_ALLOWED_COMMITMENT = 0xd1f89cac88ca71fea90df48ba29278d5782dc8eb76127bf7bfdafca71aaa8048;
    bytes32 constant NOT_ALLOWED_NULLIFIER = 0x1d38c31e6bb446623f552d36f1ce11aa86c06cefe2b5a26e53f4700792f32c84;

    bytes32 constant DENY_COMMITMENT = 0x7ccb7a4e9d51128b951cbeddefaec1140180a3d13f6eae6f06596dc432057cfa;
    bytes32 constant DENY_NULLIFIER = 0x041271fcaf479f6ab927df3a03f74d3809e9f49d880cd7a9595c8dc0a58a5e03;

    bytes32 constant COMPOSED_COMMITMENT = 0x5b5ec31c336cc8f95dc6d9025d1d008c6ed2cd5067b9c421b1d36927e230173a;
    bytes32 constant COMPOSED_NULLIFIER = 0x17f36ca085e9f988cc9e033ea510d5b6963265cb99e57e9677b0658531e0315f;
    address constant COMPOSED_EXECUTOR = 0x1C213D41668e5bDe79AaEE2240c6f6Ad7b4c9093;

    address constant DENIAL_EXECUTOR = address(0xe0);
    uint256 constant DENIAL_AGENT_ID = 7;
    /// The composed run is a different agent from the two denial legs, and its own fixture.
    uint256 constant COMPOSED_AGENT_ID = 54848;

    function run() external {
        vm.startBroadcast();

        // Verifiers first: each adapter binds its verifier's own VK_HASH, read off the freshly
        // deployed contract rather than from a constant, so a stale literal cannot be pasted in.
        HonkVerifier composedHonk = new HonkVerifier();
        DenyHonkVerifier denyHonk = new DenyHonkVerifier();
        NotAllowedHonkVerifier notAllowedHonk = new NotAllowedHonkVerifier();

        // Imported from each verifier file rather than pasted in, so regenerating a circuit
        // updates the key here automatically instead of leaving a literal to go stale.
        bytes32 composedKey = bytes32(COMPOSED_VK_HASH);
        bytes32 denyKey = bytes32(DENY_VK_HASH);
        bytes32 notAllowedKey = bytes32(NOT_ALLOWED_VK_HASH);

        HonkVerifierAdapter composedAdapter =
            new HonkVerifierAdapter(IHonkVerifier(address(composedHonk)), composedKey);
        HonkVerifierAdapter denyAdapter = new HonkVerifierAdapter(IHonkVerifier(address(denyHonk)), denyKey);
        HonkVerifierAdapter notAllowedAdapter =
            new HonkVerifierAdapter(IHonkVerifier(address(notAllowedHonk)), notAllowedKey);

        PolicyDomainRegistry registry = new PolicyDomainRegistry();
        ConfidentialPolicyVerdict guard = new ConfidentialPolicyVerdict(registry);
        ProvableDenialAnchor anchor = new ProvableDenialAnchor(registry);

        // The registry now declares the real programKey rather than bytes32(0). A later
        // `updateProgram` that rotates the key without rotating `verifier` stops verifying against
        // this adapter instead of silently accepting proofs for a program the domain no longer runs.
        registry.registerDomain(DENY_DOMAIN, REGISTRAR, address(denyAdapter), denyKey, MAX_ROOT_AGE);
        registry.updateRoot(DENY_DOMAIN, DENY_ROOT);

        registry.registerDomain(
            NOT_ALLOWED_DOMAIN, REGISTRAR, address(notAllowedAdapter), notAllowedKey, MAX_ROOT_AGE
        );
        registry.updateRoot(NOT_ALLOWED_DOMAIN, NOT_ALLOWED_ROOT);

        registry.registerDomain(
            COMPOSED_DOMAIN, REGISTRAR, address(composedAdapter), composedKey, MAX_ROOT_AGE
        );
        registry.updateRoot(COMPOSED_DOMAIN, COMPOSED_ROOT);

        vm.stopBroadcast();

        // Every leg is asserted, not logged. Generation 2's script printed `ok` and left reading it
        // to a human; a wrong constant would have deployed cleanly and only shown up later.
        _assertLeg(
            registry,
            "DENY (confidential)",
            DENY_DOMAIN,
            DENY_ROOT,
            _verdict(DENIAL_AGENT_ID, DENY_DOMAIN, DENY_ROOT, DENY_COMMITMENT, DENY_NULLIFIER, DENIAL_EXECUTOR, 0, PolicyKind.DENIED),
            "./test/fixtures/deny.proof"
        );

        _assertLeg(
            registry,
            "NOT_PERMITTED",
            NOT_ALLOWED_DOMAIN,
            NOT_ALLOWED_ROOT,
            _verdict(
                DENIAL_AGENT_ID,
                NOT_ALLOWED_DOMAIN,
                NOT_ALLOWED_ROOT,
                NOT_ALLOWED_COMMITMENT,
                NOT_ALLOWED_NULLIFIER,
                DENIAL_EXECUTOR,
                0,
                PolicyKind.NOT_PERMITTED
            ),
            "./test/fixtures/not_allowed.proof"
        );

        _assertLeg(
            registry,
            "composed run (ALLOW)",
            COMPOSED_DOMAIN,
            COMPOSED_ROOT,
            _verdict(
                COMPOSED_AGENT_ID,
                COMPOSED_DOMAIN,
                COMPOSED_ROOT,
                COMPOSED_COMMITMENT,
                COMPOSED_NULLIFIER,
                COMPOSED_EXECUTOR,
                1,
                PolicyKind.ALLOWED
            ),
            "./test/fixtures/composed_live.proof"
        );

        console2.log("");
        console2.log("=== generation 3 ===");
        console2.log("PolicyDomainRegistry        ", address(registry));
        console2.log("ConfidentialPolicyVerdict   ", address(guard));
        console2.log("ProvableDenialAnchor        ", address(anchor));
        console2.log("HonkVerifier                ", address(composedHonk));
        console2.log("HonkVerifierAdapter         ", address(composedAdapter));
        console2.log("DenyHonkVerifier            ", address(denyHonk));
        console2.log("DenyHonkVerifierAdapter     ", address(denyAdapter));
        console2.log("NotAllowedHonkVerifier      ", address(notAllowedHonk));
        console2.log("NotAllowedHonkVerifierAdapter", address(notAllowedAdapter));
    }

    function _verdict(
        uint256 agentId,
        bytes32 domainId,
        bytes32 root,
        bytes32 commitment,
        bytes32 nullifier,
        address executor,
        uint8 decision,
        uint8 kind
    ) internal pure returns (Verdict memory) {
        return Verdict({
            agentId: agentId,
            domainId: domainId,
            policyRoot: root,
            actionCommitment: commitment,
            executor: executor,
            nullifier: nullifier,
            expiry: FIXTURE_EXPIRY,
            decision: decision,
            policyKind: kind
        });
    }

    /// @dev Resolves the verifier and programKey out of the new registry, so a wrong adapter or a
    /// wrong root surfaces here rather than passing silently.
    function _assertLeg(
        PolicyDomainRegistry registry,
        string memory label,
        bytes32 domainId,
        bytes32 root,
        Verdict memory v,
        string memory proofPath
    ) internal view {
        IPolicyDomainRegistry.Domain memory d = registry.domain(domainId);
        bool rootOk = registry.isRootAcceptable(domainId, root);
        bytes memory proof = vm.readFileBinary(proofPath);
        bool ok = IVerifier(d.verifier).verifyProof(d.programKey, abi.encode(v), proof);

        console2.log(label);
        console2.log("  root acceptable ", rootOk);
        console2.log("  proof verifies  ", ok);

        require(rootOk, string.concat(label, ": root not acceptable on the new registry"));
        require(ok, string.concat(label, ": proof did not verify through the new registry"));
    }
}
