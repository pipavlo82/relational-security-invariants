# H1 wording review: proposals only

No existing reports/docstrings were changed. Prefer "separately implemented expectation predictor" and "atomic expectation admission". Separate source-code paths do not prove independent authorship, semantic origin or authority. Keep all existing unsupported-signature/anchor/header/provenance statements.

- Crystal Receipt: "separately implemented expectation predictor for the pinned Crystal Receipt scope"; Python / source TypeScript.
- RVR digest-binding: "separately implemented expectation predictor for the pinned RVR digest-binding scope"; Python / source Python.
- TSEI serializer/adoption: "separately implemented expectation predictor for the pinned TSEI serializer/adoption scope"; Python / TypeScript producer + Python checker/wrapper.
- PQ policy/as-of: "separately implemented expectation predictor for the pinned PQ policy/as-of scope"; Python / source Python.
- TAS context/dispatch: "separately implemented expectation predictor for the pinned TAS context/dispatch scope"; Python / source TypeScript + controlled JS ports.
- ConsultEscrow: "separately implemented expectation predictor for the pinned ConsultEscrow scope"; Python integer crypto / Solidity on JS EVM.
- verify-layer: "separately implemented expectation predictor for the pinned verify-layer scope"; Python MPT/RLP/Keccak / source JS EthereumJS trie.
- Legacy/synthetic: "separately implemented expectation predictor for the pinned Legacy/synthetic scope"; Python / Python messaging and SQLite models.

## Exact existing report locations

- `research/consult-escrow-validation-v0.md:24`: pipeline uses existing registries, independent admission and comparator unchanged.
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.
- `research/consult-escrow-validation-v0.md:74`: including ecrecover and local transfers. Expected uses independent Python integer
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.
- `research/crystal-receipt-validation-v0.md:28`: Every case traverses fixture registration, envelope validation, exact relation-profile resolution, profile input validation, independent expectation admission, adapter lookup, real source execution, unchanged generic comparison and unchanged top-level result taxonomy. Combined legacy + Crystal registration uses the same coordinator and gives 40 PASS.
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.
- `research/crystal-receipt-validation-v0.md:30`: The independent Python predictor derives canonical strings and equality from the frozen SPEC, separately from the actual TypeScript helpers and relation observation function. Artifact deletion tests show actual-side/profile interpretation does not require the expectation file. Patching actual-side behavior leaves expected results unchanged. A repinned tampered expectation row prevents admission of the entire two-fixture expectation set.
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.
- `research/extension-contract-v0.1-validation.md:10`: independent expectation profile/predictor and mapped mutations without editing
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.
- `research/pq-policy-asof-validation-v0.md:31`: All 21 supplied cutoff/rotation/revocation policy vectors also match both the pinned native reference and the independent predictor. Expectations admit atomically; tampering blocks admission. The adapter executes pinned source policy logic and cannot read expected rows. The predictor does not call the adapter or source implementation.
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.
- `research/pq-policy-asof-validation-v0.md:47`: RVR crypto authentication, TSEI provenance authority and full PQ authenticated transition-chain validation remain UNSUPPORTED. A top-level conformance PASS means actual matches independently admitted expectation; it does not promote any unsupported capability. ASCII/integer transport limits and trusted Python predictor independence caveats remain.
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.
- `research/rvr-digest-binding-validation-v0.md:82`: PASS means actual behavior matched independently admitted expected behavior. It
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.
- `research/tas-context-invocation-validation-v0.md:39`: Actual uses pinned production TypeScript compiled with pinned dependencies; expected uses separately implemented Python tuple/membership obligations. No adapter/predictor calls or expected-row access are shared. Different languages/code paths do not prove author independence or rule out common interpretation errors.
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.
- `research/trustless-ai-validation-gaps-v0.md:61`: | RVR digest | source-derived separately implemented | pinned Python reference | separate Python predicates and JSON/digest computation | no | upstream reference versus RSI predictor; shared encoding assumptions | not established | No-call separation prevents direct self-validation, not correlated semantic mistakes. |
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.
- `research/trustless-ai-validation-gaps-v0.md:63`: | PQ policy/as-of | source-derived separately implemented | pinned Python cutoff policy plus RSI scope guard | separate Python interval/policy derivation | no | upstream function versus RSI predictor; same trusted runtime | not established | Both depend on supplied history/anchor/signature-validity flags. Neither authenticates them. |
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.
- `research/verify-layer-validation-v0.md:9`: Six conformance cases: VL-RSI-001, 002, 005, 006, 007, 008. Control and source-backed hex-case mirror preserve the relation. Substituted root, account address and claimed balance are discriminated. All six cases PASS through fixture registration, exact Relation Profile resolution, independent expectation admission, adapter and generic comparator. Combined corpus: 85 PASS, other top-level statuses zero.
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.
- `research/verify-layer-validation-v0.md:34`: * Original source functions execute on pinned JavaScript dependencies; expectation uses separate Python Keccak/RLP/MPT obligations. No shared semantic helper or adapter/predictor call dependency. Author independence and exhaustive cryptographic assurance are not established.
  Proposed qualification: separately implemented expectation predictor / atomic expectation admission, qualified by language, source and scope; retain authorship/authority caveats.


Docstrings in profiles/*/expectation.py and consult_escrow/crypto.py, verify_layer/oracle.py also require dimension qualifiers. Their no-adapter-call statements are supported for inspected paths. "Independent" should mean code-separated there, not independent authorship or full oracle correctness. TAS and verify-layer already disclose authorship and scope caveats; retain them. Legacy rsi/oracle.py already discloses finite trusted predicates and shared crypto/codec.


Additional exact proposals:

- `research/tsei-serializer-adoption-validation-v0.md:51`: replace "Expectations are independently derived in Python" with "Expectations are separately derived in Python over the pinned serializer/chronology scope".
- `research/rvr-digest-binding-validation-v0.md:51`: replace the two-line "independently implemented predictor" phrase with "separately implemented predicate predictor".
- `research/pq-policy-asof-validation-v0.md:31`: qualify the 21-vector comparison: "Both paths agree with source policy vectors after shared source revocation preprocessing; this does not independently validate that preprocessing."

Existing reports remain unedited.
