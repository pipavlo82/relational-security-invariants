# Crystal Receipt / ReceiptOS mapping v0 — STOP assessment

Status: no adapter, fixture corpus, expectation profile or domain mutation was
implemented. Candidate identifiers below are proposed assessment labels, not
registered fixtures. None was executed or admitted.

## Exact source authority

Read-only source repository: `C:/Users/msi/dev/crystal-receipt`, remote
`https://github.com/pipavlo82/crystal-receipt.git`.
The local checkout is on `feature/tsei-spec-artifact-v0` at
`46bed9ba8662ede63f0682ac6d2c93e52b6536cd`; it has no tracked changes and
14 untracked entries. Those worktree files are not source evidence.

GitHub default branch and main ref were independently checked. Canonical main:
`45b46bf7df3a60b32583291f577a36bf19d22f00`, also present as local origin/main.
All evidence was read using exact-commit Git blobs, without checkout, fetch,
source tests, index refresh or source writes. Lane K feature worktrees were not
silently selected. Its frozen v1 SPEC is present in canonical main itself.

The admission package README at canonical main explicitly freezes member-byte
integrity to `7d9b67c96f2b472f5b4acfef3f95b669eb24de7b`. That pin is not an
ancestor of current main; it is selected because the canonical README explicitly
names it as frozen byte authority, not because of an inferred landed status.
The machine report records raw SHA-256, Git blob OID, current-main byte comparison,
file path, source kind and interpretation boundary for each used artifact.

## Source-to-RSI assessment

| Candidate | Exact source concept | Faithful interpretation | Mapping status |
|---|---|---|---|
| CR-RSI-001 | `V-SEM-MUTATION-DIFFERS`: `accepted_snapshot`, `canonical_snapshots_must_differ` | Both source snapshots are accepted, while changing one semantic value changes their canonical identity. Discrimination is distinct from rejecting the artifact. | UNSUPPORTED: no declared snapshot-equivalence relation/request in frozen RBCF. |
| CR-RSI-002 | `V-SEM-MANIFEST-INVARIANT`: external `manifest_variants`, invariant semantic snapshot | Audit timestamps are outside the semantic artifact; three manifest variants preserve the same accepted canonical snapshot. This is real mirror-positive evidence. | UNSUPPORTED by current RBCF representation, not missing source evidence. |
| CR-RSI-003 | frozen `clean_admitted` / `proof_root_mismatch` | Independently verified evidence root must agree with the portable proof-object root before Chronicle admission. | Candidate cross-object relation exists, but no native unsigned receipt/root-binding request is declared by frozen RBCF. |
| CR-RSI-004 | `counterfactual-traversal-stability-v1` | Twelve authenticated schedules, fresh process per schedule/shared process within schedule, 120 member evaluations, separate semantic/stability axes. | Frozen in canonical main, but not executed or mapped. This is not the remembered graph-degree/local-neighborhood fixture shape. |

Source paths at canonical main:

- `conformance/counterfactual-audit-boundary-v0/SPEC.md`
- `conformance/counterfactual-audit-boundary-v0/vectors/V-SEM-MANIFEST-INVARIANT.json`
- `conformance/counterfactual-audit-boundary-v0/vectors/V-SEM-MUTATION-DIFFERS.json`
- `conformance/counterfactual-conformance-v0/SPEC.md`
- `conformance/counterfactual-traversal-stability-v1/SPEC.md`
- `tests/fixtures/receiptos-chronicle-admission-v0/README.md`

Frozen admission vector paths at the explicitly documented pin:

- `tests/fixtures/receiptos-chronicle-admission-v0/vectors/01-clean-admitted.json`
- `tests/fixtures/receiptos-chronicle-admission-v0/vectors/04-proof-root-mismatch.json`

The actual admission pair differs at `/input/proof_object/receipt_root` **and**
`/input/options` (the negative omits options). It is not claimed to already be an
exact one-field substitution fixture. A minimal reduction would require its own
source-backed verification, which was not attempted after the STOP condition.
No producer-signature or real-world authorization claim follows from these roots.

## Exact model blocker

`schema/registered-fixture.v0.schema.json` preserves these closed relations:

`signer_to_subject`, `authentication_before_commit`, `atomic_consumption`,
`context_binding`, `evidence_bounded_status`, `ingestion_equivalence`.

Its request operations are only `admit`, `transition`, `consume`, `confirm`,
`ingest`. Every alternative requires `proof`, `policy` and `state`; the proof
shape has `payload_hex`, `public_key_hex` and `signature_hex`. The profile field
is fixed to `rsi-reference-profile.v0`. Request objects reject extra properties.
There is no source artifact/snapshot/root-comparison request alternative.

The source mirror operation is `semantic_snapshot`, with a semantic artifact
and separately varied manifest metadata. Its independent derivation rule exists
in the frozen SPEC. What is missing is an approved representation and explicit
protected-relation declaration for that rule in the preserved RBCF profile.

Relevant schema locations:
`/properties/protected_relation/enum`, `/$defs/request/oneOf`, `/$defs/proof`,
`/$defs/policy`, `/properties/profile_version`.
RSI-CORE-2 requires the fixture to name its relation and full inputs; unsupported
classes must fail rather than receive optimistic reinterpretation.

No workaround was implemented: no dummy Ed25519 proof, synthetic state/policy,
identifier-based artifact lookup as hidden semantic input, new relation enum,
replacement validator that silently accepts a different fixture model, or
renaming snapshot equality to the existing signed `context_binding` predicate.
No new field is proposed or added automatically. A separate semantic-profile
model decision is required before resuming this candidate mapping.

## Preserved and not claimed

Preserved: source acceptance versus identity discrimination, external audit
metadata versus semantic input, root consistency versus authorization, and
Lane K semantic versus schedule-stability axes.

No lossy translation was admitted. The registration architecture remains usable,
but architecture readiness did not prove that all real domains fit the frozen
reference profile. Neither first-domain success nor cross-domain validation is
claimed. Full source auditors and Lane K workers were not run.
