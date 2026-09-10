# Phase 2C preflight — BLOCKED, not CLOSED

RSI HEAD before/after:
`366974070b0684af8b5c07dcf4cba0cde90eb8e5`, private `main`.

**STOP before implementation:** the inspected canonical package does not expose
the operands needed to independently reproduce the real positive authority
result required for TSEI-RSI-001 and its substitution negative. The real v2
public receipt reports PROVEN but explicitly withholds Object A/B, oracle,
nonce and case-level attribution data. Its reported outcome cannot become an
RSI oracle by declaration or digest pin alone.

This is not a claim that TSEI never achieved production grounding. Older
UNPROVEN entry points and the reported v2 PROVEN instance must remain distinct.
Newer production evaluators exist and require the actual evidence bundle bytes.

The serializer registry chronology is independently pinned:

- mechanism: recompute-kit `d641510dff95541d8cd73d5bc2bf593fe024f79c`;
- producer adoption: crystal-receipt `45b46bf7df3a60b32583291f577a36bf19d22f00`;
- record introduction: recompute-kit `1dfc527d8f9b3561d32ca510f8fefd8d290391f6`.

Those three boundaries were not collapsed. Current recompute-kit main is
`15f7f59ac47b3358492bd5741143c418b5d657f5`; TSEI-host main is the adoption
commit above. The real record's exact bytes were checked at introduction and
current main. The selected historical test artifact predates adoption and has
the same bytes afterward; no historical authority was inferred from that match.

Detailed paths, digests, evidence classes and boundary analysis are in
`tsei-source-map-v0.json` and `tsei-mapping-v0.md`.

## Reverified baseline

| Check | Result |
|---|---|
| Full suite | 264 PASS |
| Full suite under `python -O` | 264 PASS |
| Legacy checks | 36 PASS; outcome diff 0 |
| Crystal Receipt checks | 4 PASS; outcome diff 0 |
| RVR checks | 10 PASS; outcome diff 0 |
| Combined report | 50 PASS; exact pre/post byte diff 0 |
| Existing mutations | 32 KILLED; exact record diff 0 |
| SURVIVED / VACUOUS / NOT_APPLIED | 0 / 0 / 0 |
| Existing tracked file hashes | All 158 unchanged, including the protected historical sets |
| RSI-CORE / schemas / generic runner / comparator / taxonomy | Unchanged |
| New domain branches / semantic exceptions | None |

No TSEI fixture, profile, adapter, expectation set or mutation was implemented.
TSEI executed fixture/mutation totals are zero, not failed or unsupported runner
results. No TSEI transport adaptation was attempted. No external repository was
modified; no private operands were searched or copied. The producer's 48-vector
test was inspected as source evidence, not rerun as TSEI validation.

Existing exact-HEAD CI remains green on Python 3.12 and 3.13:
https://github.com/pipavlo82/relational-security-invariants/actions/runs/34475431751

No new CI run, commit, push, PR, tag or release was created. The only deliverables
are four uncommitted research files. The tracked working tree remains unchanged.

**Phase 2C is not CLOSED. A three-domain validation claim is not supported.**
An explicitly narrower serializer-binding/adoption task can use the established
pins; it must not silently replace independent authority/oracle provenance.
