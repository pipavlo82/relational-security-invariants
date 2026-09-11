# Post-v0 README maintenance

Base and frozen `v0` tag: `8d8e31291ecf96284212a353efb66f606cff2953`.

The owner requested the root README reflect the closed ten-family v0 snapshot,
then explicitly requested commit/push. The former README still described a
private synthetic-only candidate with 36 checks. The updated document records
the bounded release, reproduction commands, source maps and unsupported claims.

The historical preservation gates hashed every pre-phase file, including that
README. Updating only the document therefore failed those gates despite leaving
all domain semantics unchanged. This maintenance does not rewrite any frozen
baseline, source map, validation report, expectation, fixture or mutation record.
It does not move the `v0` tag or change generic conformance code.

## Exact transition, not a documentation exclusion

[The versioned manifest](post-v0-readme-maintenance-v1.json) records before/after
SHA-256 for the README and twelve preservation-check call sites. The latter change
only how the approved maintenance transition is checked/reported. Their own byte
changes are explicit because later historical baselines also pinned these tools
and tests. No relation evaluator, adapter, predictor or semantic assertion changes.

`tools/protected_maintenance.py` accepts an unchanged historical digest, or the
exact recorded old-to-new transition for one of thirteen explicitly named paths.
Any third digest, different historical digest, missing file or unlisted change
fails. The manifest cannot expand into core paths. The helper and manifest are
reviewed test-infrastructure inputs, not an independent security oracle; a future
change to either requires review. There is no environment flag or wildcard bypass.

RVR, TSEI, PQ, TAS, ConsultEscrow and verify-layer maintenance reports now distinguish raw hash
equality (`protected_hashes_match`) from `approved_post_v0_maintenance`. A report
with an approved README change no longer claims all historical bytes are equal.
All frozen v0 reports retain their original historical statements. Outcome rows
and mutation records remain separate from these maintenance reports.

Seven tests exercise exact acceptance, third-digest rejection, wrong historical
pins, unrelated semantic drift, manifest-scope expansion, recorded current bytes
and unchanged/missing files. Full normal/optimized suites and exact conformance
comparison are delivery gates; this document alone is not evidence they ran.

The README's 539/539, 123 PASS and 84 KILLED figures remain explicitly the frozen
v0 results. The seven maintenance tests add to current-main unit totals without
adding a domain, conformance case, semantic exception or mutation classification.

## Local delivery verification

- Full suite: 546 PASS; `python -O`: 546 PASS (539 existing + 7 maintenance tests).
- All 123 conformance checks PASS; complete report byte-identical to the closed v0 report.
- All six updated domain preservation/report tools PASS.
- 635 base files compared: 622 byte-identical; 13 exact maintenance transitions recorded.
- Frozen baselines, domain semantics, source pins, mutation definitions/records and generic core unchanged.
- `v0` still resolves to the base commit. No new tag or release.
- The 84-mutation figure is the frozen v0 result; post-push CI runs the mutation gates again.
