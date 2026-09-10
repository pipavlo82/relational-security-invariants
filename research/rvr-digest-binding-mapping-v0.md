# RVR digest-binding mapping v0 — Phase 2B.1

This implements **digest binding only**. Bilateral digest binding != cryptographic
authentication. `signed_digest` equality, a public-key string, and the source
vector label `permitted` cannot establish a verified signature or control of a key.

RSI base: `5a3b90ccab1e6b9d463a80f419576820e0129608`, private `main`.
No external repository was modified. No generic runner, comparator, registry,
schema, taxonomy or RSI-CORE rule changed. Source-qualified use of “RVR” here
means the neighboring recompute-kit profile/verdict binding family; it does not
claim complete conformance to the RVR receipt protocol.

## Pinned evidence and authority

The exact repository, canonical branch, commit, path, SHA-256, evidence class,
fixture byte digests and prior compatibility records are in
`rvr-digest-binding-source-map-v0.json`. Runtime source bytes and their fixed
closure are in `evidence/rvr/source-pin.v0.json`.

| Repository | Verified canonical main | Use |
|---|---|---|
| trustless-ai/recompute-kit | `15f7f59ac47b3358492bd5741143c418b5d657f5` | Two Rule/Scope specs, two Python references, two JS references, 8 amendment + 6 verdict vectors |
| pipavlo82/recomputable-verification-receipts | `287c0ea1c2578c1833405bc2476975f95addbada` | `docs/spec/RECOMPUTABLE_VERIFICATION_RECEIPTS_V0.md`, §§1–2: profile authority and independent semantic/recomputation axes; context only |
| babyblueviper1/invinoveritas | `bdba0b674c2b2d301b75b4b23a33702b0bacfa64` | `integrations/conformance/erc-8309-vantage/services/vantage_resolution.py` and `tests/test_vantage_resolution.py`, `test_profile_a_resolves_nothing`; context only, not executed |
| damonzwicker/erc8309-companion-drafts | `f5f36778e7cbf6c26fd61a7d66b70b9108447746` | `8309-vantage-authority-companion-v0.3.9.md`, §§1,2,7.0; normative draft, not an adopted base standard |

The companion repository advanced from the earlier inspected
`02fef5fd1f54eff9221b863cc746cb74a97f3220`. The relevant v0.3.9 file is
**byte-identical**, SHA-256
`6401eba79926af05af740ccaa3efe4a94981a38b9b7527850104713130dea191` at both
commits. No relevant semantic delta was found in that file. The consumer's
opening docstring still names v0.2.2; it is not promoted to proof of full current
companion conformance.

Recompute-kit source roots:

- `conformance/profile-amendment-v0/`: `profile-amendment-v0.spec.md`,
  `amendment_gate.py`, `profile-amendment-v0.reference.mjs`,
  `profile-amendment-v0.vectors.json`.
- `conformance/verdict-profile-binding-v0/`: `verdict-profile-binding-v0.spec.md`,
  `verdict_binding_gate.py`, `verdict-profile-binding-v0.reference.mjs`,
  `verdict-profile-binding-v0.vectors.json`.

The specs' Scope sections explicitly exclude signature cryptography. Stronger
language in their narrative (“co-signed”, “cryptographic”) is qualified by those
Scope sections and the actual reference predicates. Neither the vectors nor the
reference functions contain signature bytes/verifiers sufficient to establish
cryptographic authentication. Public-key values are not part of the amendment
preimage and are not consulted by the binding predicate.

## Relation composition and responsibility

One registered profile, `rvr.digest-binding.v0`, exact version `0`, declares
`profile-and-verdict-digest-binding`. Its result is a product of the two source
relations, not a merger of their meanings. The smaller one-profile composition
shares exactly the effective-profile commitment named by the verdict spec's
Composition section. It needs no universal fields or new core branch.

Inputs: `transition` (required), `verdict` and dependent `claim` (optional).
Source-shaped objects stay inside these slots. No fake proof/policy/state fields
are required. This bounded profile covers the buyer/supplier default; other
party-set policies are not silently inferred or admitted.

- Actual path: verify exact captured source bytes, execute the fixed Python
  reference functions, compose their raw outputs. Source `run()`/`expect` vector
  helpers are never called by the adapter. Manifests cannot select Python paths.
- Interpretation: the Relation Profile validates slot shape and exposes observed
  composition; it never reads expected rows.
- Expected path: a separate predicate-obligation implementation derives the
  commitment/binding outcomes from the pinned rules. It does not call the source
  evaluator, adapter, or Relation Profile evaluator, and has no artifact argument.
- Admission: existing Expectation Contract binds exact fixture bytes, recomputes
  every row independently, compares every recorded row, and admits atomically.
- Comparison: the existing comparator checks the complete observation. PASS is
  conformance, including correctly refusing an unsupported stronger claim.

`transition` contains all five unrenamed source outputs. `verdict_binding` is
null when not evaluated; otherwise it contains all three unrenamed verdict
outputs, including source `resolution_status`. That name is qualified by its
verdict-binding container. `substantive_resolution: not_evaluated` is a wrapper
coverage annotation, **not** a source outcome and not “divergence resolved”. No
companion resolution algorithm is executed or fabricated.

`crypto_authentication` always reports status `UNSUPPORTED` and reason
`no_pinned_signature_verification_lane`. The requested `crypto_authentication`
claim is never admissible. A requested composite `digest_binding` claim requires
a permitted transition and, when a verdict is supplied, a bound verdict. This
claim is expressly limited to those digest predicates; a separately bound A
verdict can exist even when the composite transition claim is not established.

## Fixture mapping

All six registered IDs have namespace `rvr:`. The names select fixtures only;
no name, namespace, case ID, vector label or directory supplies expected truth.

| Fixture / cases | Exact source identifier or derivation | Preserved / changed | Expected bounded observation |
|---|---|---|---|
| RVR-RSI-001 / `no_amendment`, `retained_profile_bound_verdict` | Amendment Rule no-change wording + Python fallback; Verdict Rule/Composition | Prior and proposed profile A; amendment absent. Second case adds a core naming A with matching core digest | Effective A; amendment `unresolved`. Verdict null or independently `bound`. No ACCEPT or substantive resolution inference |
| RVR-RSI-002 / `unbound_substitution`, `wrong_party_digest` | Amendment vectors `bare-swap-no-amendment`, `auth-names-wrong-digest` | Both profile objects remain well-shaped; candidate B differs, but amendment/digest relation is absent or wrong | Effective A retained; transition `unresolved`; no silent substitution |
| RVR-RSI-003 / `bilateral_binding`, `pubkey_representation_change` | Amendment vectors `permitted`, `permitted-distinct-pubkey`; Scope | Exact source task/edge/party digest inputs; mirror changes only public-key value | Effective B, transition `permitted` at digest scope; crypto UNSUPPORTED in both |
| RVR-RSI-004 / `correct_verdict`, `different_verdict_same_binding` | Verdict vectors `bound`, `bound-distinct-verdict`, composed with amendment `permitted` | Verdict core is tied to effective B; alternative source payload gets its own matching digest | Verdict `bound`; no claim of substantive truth or execution |
| RVR-RSI-005 / `stale_profile_locally_digest_bound` | Verdict Rule and `wrong-profile` predicate, rule-derived A operand | B remains effective. Core's endpoint changes to A; resolver digest is recomputed for that altered core, preserving local core/digest validity | Transition stays `permitted`; verdict `unresolved`, bound commitment null; no stale-profile promotion |
| RVR-RSI-006 / `no_crypto_promotion` | Both Scope sections; source `permitted` + `bound` inputs | Digest relations succeed; fixture requests the stronger claim but supplies no new verification evidence | Digest results preserved; authentication UNSUPPORTED; requested crypto claim inadmissible |

No published no-amendment vector exists. RVR-RSI-001 is explicitly a
reference-behavior/rule-derived instance, not a newly discovered normative
`A -> A = ACCEPT` vector. RVR-RSI-005 likewise uses an independently derived A
endpoint rather than claiming its exact bytes were published upstream. The
mapping is lossless for the two returned digest results and partial for wider
protocol behavior.

All source vectors are also checked directly: each actual reference output and
each independent prediction must equal the frozen vector's own expectation.
Those vector rows are external cross-check evidence, not runtime oracle input.

## Unresolved and promotion boundaries

“Effective profile remains A” does not imply “transition accepted”.
“Transition digest binding established” does not imply “divergence resolved”.
“Verdict binds effective profile” does not imply “verdict substantively correct”.
“Public key present” does not imply “signature verified”.

Amendment unresolved and verdict unresolved are tested independently, including
amendment unresolved + verdict bound and amendment permitted + verdict
unresolved. Substantive divergence belongs to the companion's separate policy
layer and is not evaluated here. Base evidence preservation/divergence exposure,
companion resolution policy, and neighboring RVR receipt/binding are not merged.
The companion's named **Profile A** is not the arbitrary commitment operand A.

## Failure, transport and reproducibility

Wrong/missing source bytes or a changed source commit pin fail relation
availability before admission: top-level UNSUPPORTED, with no expectations
admitted for the profile. Malformed fixture inputs are INVALID_FIXTURE. A
completed observation that differs from admitted expectations is FAIL. A
digest-scoped fixture may PASS while crypto authentication remains internally
UNSUPPORTED. All four top-level counts remain separate.

Runtime is offline and pins captured bytes; it never accepts a moving branch.
Upstream changes require explicit repin/revalidation. The first source fetches
and current-main checks were read-only GitHub API operations; no external
checkout was edited. Source documentation may contain Unicode, but it is hashed
as raw evidence, never coerced into a fixture. Fixture transport remains the RSI
ASCII/integer subset. No universal JCS or arbitrary source-object coverage is
claimed. Python evaluator/predictor independence is a trusted-code review and
test property, not a process/filesystem sandbox guarantee.

## Mutation evidence

| Mutation | Mapped check | Incorrect promotion/substitution |
|---|---|---|
| RVR-M1 | `test_unbound_substitution` | Candidate becomes effective without required digest relation |
| RVR-M2 | `test_no_amendment` | Retained A implies substantive resolution |
| RVR-M3 | `test_wrong_verdict` | Ignore stale verdict profile |
| RVR-M4 | `test_layer_separation` | Propagate amendment unresolved into an independently bound verdict |
| RVR-M5 | `test_no_crypto_promotion` | Successful digest relation becomes crypto VERIFIED |
| RVR-M6 | `test_pubkeys_not_authentication` | Pubkey presence admits the crypto claim |

Each mutation runs the real pipeline and source evaluators before the mapped
assertion. Admission/source/execution failures raise errors and classify VACUOUS;
they cannot count as kills. Collateral assertion failures are recorded
separately. Optional RVR-M7 is not registered: vector labels and `expect` rows
are excluded from admitted input shape; hostile-label tests show they do not
alter reference/predictor behavior.

## Reproduction

Run the ordinary suite and `python -O` suite, then:

```text
python tools/run_rvr_digest_binding.py --include-previous
python tools/prove_rvr_can_fail.py --output artifacts/rvr-mutations.json
python tools/check_rvr_digest_binding.py
```

The final checker consumes fresh prior registry, Relation Profile and Crystal
mutation reports at their documented default artifact paths. It verifies exact
prior mutation records, outcomes, protected bytes, combined pipeline execution,
source closure and deterministic structured serialization. CI performs these
commands after the existing baseline gates.
