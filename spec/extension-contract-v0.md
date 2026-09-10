# Extension Contract v0.1 — architecture checkpoint

Status: expectation gate resolved by [Expectation Contract v0.1](expectation-contract-v0.md).
This document supersedes the earlier uncommitted gate-stop design. It is not a
claim that all extension work or cross-domain validation has been implemented.

```text
RBCF fixture
  -> Expectation Profile <-> pinned expectation set
  -> independent predictor
  -> atomic admitted expectation
  -> Adapter Registry
  -> implementation-under-test
  -> actual result
  -> generic comparator / four-state result taxonomy
```

An external expectation file cannot bypass independent prediction and atomic
admission. Profiles and adapters are registered explicitly in trusted source;
no reflection, executable manifest contents or runtime package discovery.
Unknown profile/adapter is UNSUPPORTED. Malformed fixture is INVALID_FIXTURE.
Profile admission failure is an internal PROFILE_ERROR mapped to UNSUPPORTED,
not a claim that a structurally valid fixture is malformed.

Fixture IDs remain opaque exact lookup identities. The current synthetic profile
preserves its existing IDs, fixed corpus and explicit historical execution order.
A future namespaced identity contract must not infer relations, expected results,
adapters or policies from prefixes. Duplicate registered fixture identities fail
closed. A future directory-discovery extension must explicitly sort all files,
reject duplicates and report unexpected JSON instead of silently skipping it.
This task uses explicit fixture scopes with exact byte-level set binding.

The generic runner and expectation registry have no domain-specific decision
branches. The synthetic compatibility profile retains the frozen schema and
predictor. A later fixture/adapter identity and deterministic discovery extension
can now proceed against the expectation contract. Original corpus-specific
schema restrictions and legacy mutation mappings still need that work; Phase 2
external validation remains blocked until it is complete and source evidence is
independently pinned. No external-domain success is claimed here.

Mutation registration must retain stable identity and mapped checks; unknown
unapplied targets are NOT_APPLIED and setup failures VACUOUS. Expectation
architecture mutations implement these distinctions separately from the unchanged
12 legacy mutations. General mutation-registry migration remains pending.

Non-goals: arbitrary runtime plugins, network loading, dynamic package
installation, domain-specific semantics in core, and changes to RSI
protected-relation rules. RBCF semantic fields and normative RSI-CORE stay frozen.
