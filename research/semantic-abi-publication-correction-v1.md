# Semantic ABI publication correction

The initial publication `48c08160214b8caa26cb9c1928166db2064b7f01` failed CI protected-file checks because the final README update occurred after the recorded local full-suite runs. The recorded 586 normal/optimized passes apply to the implementation before that final documentation update, not to the failed published tree. This ordering omission is retained in history.

The existing post-v0 maintenance mechanism already permits an exact README byte transition. This correction updates only its README after-digest, preserving the frozen v0 before-digest and all 12 other entries. No checker code, semantic allowlist, core, domain implementation, test, frozen baseline or v0 tag changes. An arbitrary third README digest still fails.

- Previous allowed README SHA-256: `01f6c35273af73040d0c7b137f2d6eb3b8711d6cce539e2f3512245bb7c2d807`
- New allowed README SHA-256: `eedc3c53717164f369f1b57d99509f4f4f829344de7acaa8c6943a059ea749b4`
- Frozen before SHA-256: `8ef0d5dcdad74c37251b9425e7285c4accbc804bb4cded4a844eca556b93ab64`

Relative to the pre-admission base ff7e308, README and the existing documentation-maintenance manifest are the only prior files changed; the other 721 prior tracked files remain unchanged. The earlier local validation receipt is historical and is supplemented by this correction. Fresh CI must be checked on the correction commit; success on another SHA is insufficient.

Local correction checks: all 12 mapped protected-file tests passed; the 7 maintenance tests also passed normally and with `python -O`. The guard still rejects unapproved README digests and unrelated semantic drift. [Mapped check log](semantic-abi-validation-v1/publication-protection-checks.log), SHA-256 `48291bf4207dbc9bb5e7820fde50fdcd8dba6e5f3d4809e2e97ee6f2796b6af9`.
