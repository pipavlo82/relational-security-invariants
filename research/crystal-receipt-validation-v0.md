# Phase 2A — Crystal Receipt validation stopped at semantic-fit gate

**STOPPED BEFORE IMPLEMENTATION.**

RSI main remains `05f3853756ad9deb0e5d08d54dfdfd462652a801` before and after.
No commit or push was made because the requested success criteria were not met.
Only this report, the machine report and the mapping assessment were added as
untracked review files. No source or generic RSI component was changed.

## Finding

A real source-backed mirror-positive exists:
`V-SEM-MANIFEST-INVARIANT` at Crystal Receipt canonical main
`45b46bf7df3a60b32583291f577a36bf19d22f00`. Its frozen contract requires accepted
semantic snapshots to remain identical while external audit metadata varies.

The blocker is the preserved RBCF semantic vocabulary and input shape, not
fixture IDs or plugin registration. The source `semantic_snapshot` operation
and unsigned snapshot/root relations have no authorized representation among
the current six relations and five signed-operation request variants. Admitting
a different source schema or manufacturing signed-operation fields would bypass
or reinterpret the model this task explicitly freezes. The STOP condition was
therefore applied before adapter/predictor/mutation implementation.

## Verified baseline

- 150 tests pass; 150 tests pass under python -O.
- Legacy and extension baseline: 36 PASS; FAIL, INVALID_FIXTURE, UNSUPPORTED = 0.
- Shared mutation registry: 16 KILLED; SURVIVED, VACUOUS, NOT_APPLIED = 0.
- All 26 snapshotted core/schema/registry/expectation/legacy artifact hashes remain
  identical. No semantic exception was added.
- Existing exact-main CI is green on Python 3.12 and 3.13:
  https://github.com/pipavlo82/relational-security-invariants/actions/runs/34424963934 .
  No new CI run is claimed.

## Domain results

Zero Crystal Receipt fixtures registered or executed; zero expectations admitted;
zero Crystal Receipt mutations implemented or run. Four proposed candidates are
recorded separately as UNSUPPORTED assessments, not as fabricated runner results.
No first-external-domain success or cross-domain validation claim is made.

The mirror-positive is evidenced, semantic-snapshot discrimination is evidenced,
a frozen root-mismatch admission pair is evidenced, and Lane K v1 is frozen in
canonical main. Their exact distinctions and remaining interpretation limits
are described in [the mapping assessment](crystal-receipt-mapping-v0.md).

## Source and preservation evidence

The local source checkout is a feature branch with untracked files; none of its
mutable worktree contents was used. Canonical exact-commit blobs were read only.
The admission README's separate frozen byte pin was honored explicitly, without
asserting ancestry or silently choosing a feature branch. No Crystal Receipt
repository files, Git refs, index or configuration were modified.

[Machine-readable report](crystal-receipt-validation-v0.json) contains exact
source commits/paths/raw SHA-256 values/blob OIDs, source state, before/after RSI
hashes, baseline structured report hashes, the actual admission input diff and
candidate status/limitations. Source expected labels are evidence, not admitted
RSI oracle rows. Full Crystal Receipt package auditors and execution were not run.

Resumption requires a separate, explicit decision about a semantic profile/input
representation for these source-defined relations. This task did not make that
decision, weaken the contract, or start another domain.
