# Relationship to PRF / ReceiptOS / Semantic ABI / TSEI

RSI is a separate security-oriented research lane. No compatibility or runtime
integration is claimed merely because the ideas compose conceptually.

The existing PRF README identifies weak observational equality vs protected
semantic equality, negative and mirror-positive cases, exact-byte validation
and a separately scoped corpus. Its outcome model separates PRESERVED,
VIOLATED, UNVERIFIABLE from benchmark PASS/FAIL. Those distinctions informed
this cut. Source read during implementation:

- https://github.com/pipavlo82/protected-relation-fixtures/blob/main/README.md
  Git blob: b4e3aa92601a8c68c72a634211b32839419be527
- https://github.com/pipavlo82/protected-relation-fixtures/blob/main/spec/outcome-model.md
  Git blob: ef8ac78d033ebe78170eb257e37c6cebc6bb486b

No source code is vendored and no existing corpus, schema identity, serializer
binding, ReceiptOS run history or TSEI frozen artifact is modified. These are
lineage pointers, not immutable commit URLs or claims about future main.

A future PRF adapter must map actual PRF contracts, distinguish protected-input
outcome from target behavior and provide exact source/fixture pins. A future
ReceiptOS or Semantic ABI adapter must call the real native checker rather than
return the synthetic model result under a renamed backend. Separate worktree
and separate PR required. Independent authorship must be evidenced, not inferred
from different filenames or programming languages.
