# PQ policy/cutoff/as-of mapping v0

Phase 2D scope is conditional policy conformance over pinned supplied binding history. It is not independent verification of deployed anchors, companion signatures or transition authentication. This scope is source-defined and executable; the stronger capabilities remain explicitly UNSUPPORTED.

RSI base: `b899b485f02dbe9de4d20b10cfcfb1e2e74578a2`, private main. The canonical source main was rechecked at `trustless-ai/recompute-kit@15f7f59ac47b3358492bd5741143c418b5d657f5`. Every inspected source hash matches the earlier evidence closure. No external repository was modified.

## Source identities

| Repository | Exact commit | Path | SHA-256 | Evidence class |
|---|---|---|---|---|
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/pq-key-binding-v0/pq-key-binding-v0.spec.md` | `877499e8dae1d20e6e3f056cc48337f08755af63fef0c66d58ca44e628928af0` | normative spec |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/pq-key-binding-v0/pq-key-binding-v0.rotation.json` | `150817aef5862ef601f487ef2f038917bfe78fa302bdf546607a40a7215adee6` | signed-object artifact |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/pq-key-binding-v0/pq-key-binding-v0.rotation-vectors.json` | `2c046fdaaebe1a8e71b99b191cbd8efa48abe7b6449e5f4b32cc30f1750d6b1a` | vector |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/pq-key-binding-v0/pq-key-binding-v0.revocation.json` | `b97752168fd1071a7a00c72cd584f2e14f24a7314719bdbabc0b089e630151bc` | signed-object artifact |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/pq-key-binding-v0/pq-key-binding-v0.revocation-vectors.json` | `3481360d3ffa5e785ca640a06994a9724ab6e7cee1a2e033102e70b91f31cac0` | vector |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/pq-key-binding-v0/pq-key-binding-v0.cutoff-vectors.json` | `7cfd7e8906b0afbfa1d000e99177ab797b2f757dc2d71364ff79cc48fbc506f7` | vector |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/pq-key-binding-v0/pq-key-binding-v0.vectors.json` | `9ee62960f0fade98ee107ee600feac3bca9b6b1157c273568ee060efec235823` | vector |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/pq-key-binding-v0/deep_recompute.py` | `8b43d22524a2f9c18ee90e302afd84a604b5b5cb949d4325203a86479187ba46` | reference implementation |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/pq-key-binding-v0/cutoff_enforce.py` | `a11d528b97bd88b7850a679122e1bbaec162bf98f6164587c23e47f9174df528` | reference implementation |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/pq-key-binding-v0/gate.py` | `36347585715c22d8862aae34e6d5ab84b5e9283e08fa8366382fba9935e66d43` | reference implementation |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/pq-key-binding-v0/suite.json` | `bcd7a1eeeb9e9b392cb917d900313636051c5b4eac18bf12a0d8ded02a9df6dc` | manifest |

The spec's normative verifier rule is cutoff by anchor time, never created_at, with consumer-selected cutoff. Its rotation and revocation sections define governing binding at the artifact's anchor, preserving earlier governing eras. The executable source is `cutoff_enforce.py`: `resolve_in_force`, `admit`, and `apply_revocations`. The generic comparator and all prior domains are unchanged.

## Evidence qualifications that remain load-bearing

- `pq_companion.valid` and `artifact.anchored` are supplied evidence flags in the source policy vectors. This implementation evaluates the predicate conditional on them; it does not independently establish their authenticity.
- The rotation vectors explicitly call `1788000000` an **intended on-chain anchor**. No claim is made that rotation-1 is independently proven deployed/anchored. Merely pinning this vector does not create that proof.
- The source spec says rotation signatures verify in a separate deep lane. The inspected offline `deep_recompute.py` verifies hash/canonical-content consistency and explicitly defers signature verification. These are different evidence scopes, not silently reconciled claims.
- The rotation statement identifies `SLH-DSA-SHA2-192s`. The offline deferred labels say `continuity_signature (ML-DSA)` and `pq_companion_signature (ML-DSA)`. The artifact's hash-bound algorithm field is preserved; neither label constitutes algorithm-specific signature verification.
- The actual rotation object contains predecessor and signature fields. Their presence does not establish authenticated continuity. The adapter runs only the source hash checks; it does not call signature-verification code.

No proof bytes, key signatures or chain history were invented. The two public source keys are used as exact identities. Policy-vector case names/descriptions contain non-ASCII explanatory text; they stay in the raw source evidence. Only source semantic operands, which are ASCII/integer/boolean, enter the RSI fixtures. No semantic operand is coerced or relabeled.

## Relation and pipeline

`pq.policy-asof.v0`, exact version `0`, interprets relation `policy-cutoff-asof`. Inputs are source binding history, consumer cutoff, artifact anchor/evidence/companion fields, a separate current-as-of query, requested snapshot key, requested claim and reported algorithm label. No universal schema fields were added.

The adapter executes captured pinned `cutoff_enforce.py` functions. Its native policy output is preserved. A second resolver invocation answers current authority under the same supplied history, independently of the artifact's governing era. The requested snapshot key must equal the source-computed governing key. Exact pinned-history identity is separately checked; this does not authenticate that history.

The independent predictor derives temporal eligibility by ordering eligible binding intervals and applying the spec's two admission alternatives. It never imports/calls the source enforcer, adapter or relation evaluator, and cannot read expectation rows. One tampered expected row blocks the entire six-fixture profile before execution. Source digest/commit drift yields UNSUPPORTED before admission, not a malformed-fixture verdict.

`claim_admissible` for `policy_eligibility` means only that the conditional policy decision, requested governing snapshot and pinned history agree. It is not an authenticated authority claim. Every observation carries both `anchor_validation.status = UNSUPPORTED` and `authenticated_transition_validation.status = UNSUPPORTED`.

## Fixture matrix

| Fixture / case | Exact source basis | Preserved local validity | Protected relation and expected conformance |
|---|---|---|---|
| PQ-RSI-001 / before_cutoff | rotation vectors case 3, BETWEEN rotations | Source history and artifact shape valid | A governs at `1786500000`; anchored-before-cutoff alternative applies; PASS |
| PQ-RSI-002 / retired_key | rotation vectors case 7 | Companion present/valid flag remains true under old key | At `1789000000`, B governs; old-key companion cannot satisfy resolution binding; native REJECT, conformance PASS |
| PQ-RSI-003 / new_key | rotation vectors case 6 | Same post-cutoff source policy shape; companion uses B | Native ADMIT under supplied valid-companion evidence; authentication still unsupported; PASS |
| PQ-RSI-004 / historical_anchor | case 3 anchor plus case 6 cutoff/current query | Historical anchor flag true; no companion required by pre-cutoff alternative | Artifact governed by A while current query resolves B; conditional historical eligibility preserved; PASS |
| PQ-RSI-004 / created_at_is_not_anchor | Same historical case with anchored=false and earlier created_at, derived from normative never-created_at rule | JSON, history, times remain valid | Earlier signing/creation time supplies no anchor proof; no companion alternative; native REJECT, conformance PASS |
| PQ-RSI-005 / stale_snapshot | case 6 with requested snapshot endpoint replaced by A | Native policy under B can ADMIT; stale key remains well formed | Requested snapshot differs from recomputed governing key; dependent claim inadmissible; PASS |
| PQ-RSI-007 / metadata_not_authentication | case 6 plus exact rotation artifact and offline deferred labels | Policy succeeds; predecessor/signature fields present | Stronger transition claim inadmissible and UNSUPPORTED; SLH-DSA statement cannot be relabeled ML-DSA; PASS |

PQ-RSI-006 is omitted: the inspected resolver does not establish a general subject/signature authentication relation. A separate test ensures changing pinned history (including its subject field) cannot inherit this profile's history qualification; that is not presented as a general subject-authentication fixture.

A = `kya-l4-genesis`, B = `kya-l4-rotation-1`. The complete key identities remain in source/fixtures. Cutoff and rotation time are **not the same boundary**: cutoff requires the companion alternative; rotation determines which key governs. A is not universally revoked merely by passing a cutoff. The registered negative uses an as-of point after B's supplied rotation boundary.

Historical eligibility is a conditional result under the governing proven-anchor evidence premise. This phase does not establish an actual artifact anchor merely because a vector sets anchored=true. Unverified historical reality remains outside the claim. The source policy also permits the valid-companion alternative; this profile does not invent a universal anchored=false rejection when that alternative holds.

## Mutation mapping

| ID | Defect | Mapped test |
|---|---|---|
| PQ-M1 | valid flag under retired key bypasses in-force key check | test_old_key_after_cutoff |
| PQ-M2 | current query time replaces historical artifact anchor | test_historical_anchor |
| PQ-M3 | created_at before cutoff manufactures anchored evidence | test_signing_not_anchor |
| PQ-M4 | requested stale snapshot accepted without equality | test_stale_snapshot |
| PQ-M5 | policy ADMIT promoted to VERIFIED transition | test_no_crypto_promotion |
| PQ-M6 | predecessor/signature-field presence authorizes transition | test_metadata_not_authentication |
| PQ-M7 | ML-DSA label replaces SLH-DSA artifact algorithm | test_algorithm_label |

Each mapped assertion runs only after normal fixture loading, source verification, atomic expectation admission and actual evaluation. Setup/import/schema errors are VACUOUS. Collateral failures remain separately recorded.

## Boundaries and non-goals

Six fixture files contain seven conformance checks. Top-level PASS means actual conditional behavior matches an independently admitted expected result; it does not prove every stronger security claim. Unknown profile versions/source drift remain UNSUPPORTED; malformed input is INVALID_FIXTURE; executed mismatches are FAIL.

The generic core has no new domain branches or identifier-based semantic inference. All 202 prior tracked files are protected, including TSEI implementation and its workflow. New registration and workflow files compose the fourth domain without editing the preceding compositions. No generic code/schema/taxonomy changes, tag, release, PR or external-repository modification.

RVR cryptographic authentication, TSEI provenance authority, and full PQ authenticated transition-chain validation remain UNSUPPORTED. The four-domain claim is limited to shared conformance architecture and the stated evidence-qualified relation scopes; it is not universal Trustless AI validation. ASCII/integer fixture transport and trusted Python independence remain limitations.
