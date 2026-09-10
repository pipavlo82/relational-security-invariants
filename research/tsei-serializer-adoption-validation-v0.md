# Phase 2C.1: TSEI serializer/adoption validation

RSI base: `366974070b0684af8b5c07dcf4cba0cde90eb8e5`, private `main`.
The resulting SHA is the commit containing this report; exact-HEAD CI is verified separately after publication, avoiding a self-referential commit hash. Local validation is complete. Phase 2C.1 closure requires green checks on that exact revision.

## Verified local result

| Gate | Before | After |
|---|---:|---:|
| Full unittest suite | 264 PASS | 303 PASS |
| Full suite under `python -O` | 264 PASS | 303 PASS |
| Legacy fixture checks | 36 PASS | 36 PASS |
| Crystal Receipt checks | 4 PASS | 4 PASS |
| RVR digest-binding checks | 10 PASS | 10 PASS |
| TSEI serializer/adoption checks | 0 | 7 PASS |
| Total conformance checks | 50 PASS | 57 PASS |
| FAIL / INVALID_FIXTURE / UNSUPPORTED | 0 / 0 / 0 | 0 / 0 / 0 |
| Existing mutation records | 32 KILLED | 32 identical KILLED records |
| New TSEI mutations | 0 | 6 KILLED |
| Total KILLED | 32 | 38 |
| SURVIVED / VACUOUS / NOT_APPLIED | 0 / 0 / 0 | 0 / 0 / 0 |

All 158 previous tracked-file SHA-256 values match. Generic runner, comparator, expectation/extension core, relation registry, result taxonomy, schemas, RSI-CORE, legacy expectations/predictor/fixtures and existing Crystal/RVR implementations are byte-identical. No old file was edited. Generic static anti-coupling checks pass. Semantic exceptions added: **0**.

All 50 prior structured rows compare exactly, including observed/expected data. All 32 prior mutation records compare exactly, including mapped checks, phases, errors and collateral lists. The structured domain report was regenerated twice and compared byte-for-byte; canonical serialization round-trip also matches.

## Source identity

Canonical heads reverified before implementation:

- Producer TSEI paths: `pipavlo82/crystal-receipt@45b46bf7df3a60b32583291f577a36bf19d22f00`, branch `main`.
- Registry: `trustless-ai/recompute-kit@15f7f59ac47b3358492bd5741143c418b5d657f5`, branch `main`.
- Canonical serializer pre-images: `trustless-ai/recompute-kit@f1d75a530761c983e8b6900f036935ac7758538c`, pinned ancestor of `main`.

Chronology: mechanism `d641510dff95541d8cd73d5bc2bf593fe024f79c`; producer adoption `45b46bf7df3a60b32583291f577a36bf19d22f00`; authoritative record introduction `1dfc527d8f9b3561d32ca510f8fefd8d290391f6`. Producer pre-adoption snapshot is `5c3f285495b41c357fab045b04b44d5714ced9a9`; registry pre-record snapshot is `79cb2da9c7943bd45fb64f099c3a18eab1922299`.

Source map and mapping document record all 12 file paths, full SHA-256 values, source classes, Git parent/ancestry evidence, fixture derivations and interpretation limits. No external repository was modified.

## Fixture results

- `tsei:TSEI-RSI-001`: correct serializer identity and adopted/current binding recognized; PASS.
- `tsei:TSEI-RSI-002`: unversioned serializer identity substituted while record and serialized bytes remain valid; binding discriminated; conformance PASS.
- `tsei:TSEI-RSI-003`: registry mechanism exists without producer adoption; no adoption promotion; PASS.
- `tsei:TSEI-RSI-004`: producer adopted, authoritative registry record not introduced at queried snapshot; states stay separate; PASS.
- `tsei:TSEI-RSI-005`: exact record introduction recognized independently of adoption; PASS.
- `tsei:TSEI-RSI-006`: historical pre-adoption bytes reproduce identically without automatic rebinding; PASS.
- `tsei:TSEI-RSI-007`: serializer/adoption succeeds but reported PROVEN / VALID_PROVENANCE cannot establish provenance authority; PASS with authority capability UNSUPPORTED.

No generic rule rejects every artifact before record introduction. Registry availability and producer effective coverage are separate coordinates. The historical prohibition tested here is the source's pre-adoption/non-rebinding rule.

The pinned producer passes all **48** serializer qualification vectors; the pinned record checker reproduces all **15** shape vectors. These are source qualifications within the tests, not additional RSI fixture-count inflation. Actual probe bytes are produced by captured pinned TypeScript. Expectations are independently derived in Python and atomically admitted; tampered expectation rows block all seven fixtures before adapter execution.

## Mutation decision evidence

All six TSEI mutations are KILLED at their mapped test-phase assertion after normal source loading, expectation admission and adapter execution. No errors or setup crashes were used as kill evidence. The JSON report retains each mapped check and collateral list.

| Mutation | Broken relation | Mapped test | Collateral failures |
|---|---|---|---:|
| TSEI-M1 | local validity promoted over wrong serializer binding | test_wrong_serializer | 3 |
| TSEI-M2 | mechanism promoted to producer adoption | test_mechanism_not_adoption | 2 |
| TSEI-M3 | adoption promoted to record introduction | test_adoption_not_record | 2 |
| TSEI-M4 | current binding applied before artifact effective boundary | test_nonretroactivity | 2 |
| TSEI-M5 | serializer success promoted to provenance authority | test_no_authority_promotion | 5 |
| TSEI-M6 | reported labels trusted without required operands | test_reported_labels_not_authority | 4 |

## Scope and limitations

TSEI serializer/adoption scope is locally validated. TSEI authority/provenance remains **UNSUPPORTED**; full Phase 2C remains **BLOCKED**. The public receipt withholds Object A/B, oracle, nonce and attribution operands required for independent recomputation. Reported labels do not supply those operands.

The narrow three-domain claim is supported by a common-pipeline test and exact prior regressions: semantic-snapshot equivalence, profile/verdict digest binding, and serializer/adoption boundary binding. This does not validate full TSEI provenance, RVR cryptographic authentication, all ReceiptOS semantics, or a universal security model.

Remaining limits: exact finite snapshots; no arbitrary artifact-origin attestation; ASCII/integer RSI fixture transport; independent trusted Python code still requires review. Full tagged serializer qualification is an external-byte lane, not a relaxation or normalization of fixture transport. The historical example is explicitly a public synthetic preflight object, not a real authority oracle.

The source checker emitted an unclosed-file warning during the first domain test run. The RSI wrapper now owns and closes that handle with ExitStack; source bytes remain unchanged. Final suite runs pass without that warning. No conformance failures were hidden or reclassified.

## Reproduction and CI

```text
python -m unittest discover -s tests -q
python -O -m unittest discover -s tests -q
python tools/run_tsei_serializer_adoption.py --include-previous
python tools/prove_tsei_can_fail.py --output artifacts/tsei-mutations.json
python tools/check_tsei_serializer_adoption.py --mutations artifacts/tsei-mutations.json
```

The unchanged primary workflow runs the full suite and prior mutation gates on Python 3.12/3.13. A new TSEI workflow runs domain tests in both modes, the six mutations and deterministic closure checks with Node 22.15.0. Publication uses only private origin/main, without tag, release or PR. CI results and resulting HEAD are reported after the containing commit is published.

The four older Phase 2C STOP research files are included unchanged as historical evidence; this narrowed validation does not overwrite their authority blocker.

## Files added

- `.github/workflows/tsei.yml`
- `adapters/tsei/__init__.py`
- `adapters/tsei/encoder.mjs`
- `adapters/tsei/model.py`
- `corpora/tsei/fixtures/TSEI-RSI-001.json`
- `corpora/tsei/fixtures/TSEI-RSI-002.json`
- `corpora/tsei/fixtures/TSEI-RSI-003.json`
- `corpora/tsei/fixtures/TSEI-RSI-004.json`
- `corpora/tsei/fixtures/TSEI-RSI-005.json`
- `corpora/tsei/fixtures/TSEI-RSI-006.json`
- `corpora/tsei/fixtures/TSEI-RSI-007.json`
- `evidence/tsei/crystal-receipt-README.md`
- `evidence/tsei/crystal-receipt-authority-object-b-valid-v1.json`
- `evidence/tsei/crystal-receipt-encode-json-utf8-lf-v0.ts`
- `evidence/tsei/recompute-kit-README.md`
- `evidence/tsei/recompute-kit-binding-record.schema.json`
- `evidence/tsei/recompute-kit-binding-record.vectors.json`
- `evidence/tsei/recompute-kit-encode-json-utf8-lf-v0.spec.md`
- `evidence/tsei/recompute-kit-encode-json-utf8-lf-v0.vectors.json`
- `evidence/tsei/recompute-kit-tsei.frozen-artifact.json`
- `evidence/tsei/recompute-kit-validate_binding_record.py`
- `evidence/tsei/source-pin.v0.json`
- `evidence/tsei/tsei-encode-json-utf8-lf-v0.test.ts`
- `evidence/tsei/tsei-ia-real-v2-20260824-02.production-grounding.json`
- `extensions/tsei.corpus.v0.json`
- `extensions/tsei.py`
- `profiles/tsei/__init__.py`
- `profiles/tsei/expectation-profile.v0.json`
- `profiles/tsei/expectation.py`
- `profiles/tsei/expectations.v0.json`
- `profiles/tsei/relation.py`
- `profiles/tsei/source.py`
- `research/tsei-mapping-v0.md`
- `research/tsei-serializer-adoption-mapping-v0.md`
- `research/tsei-serializer-adoption-source-map-v0.json`
- `research/tsei-serializer-adoption-validation-v0.json`
- `research/tsei-serializer-adoption-validation-v0.md`
- `research/tsei-source-map-v0.json`
- `research/tsei-validation-v0.json`
- `research/tsei-validation-v0.md`
- `tests/test_tsei.py`
- `tools/check_tsei_serializer_adoption.py`
- `tools/prove_tsei_can_fail.py`
- `tools/run_tsei_serializer_adoption.py`
