# RVR evidence closure v0

Design/evidence only. RSI main: `05f3853756ad9deb0e5d08d54dfdfd462652a801`. No implementation, schema change, commit or push. Prior design documents are unchanged.

**Decision: YELLOW (clarification only, no model defect). The RVR architecture evidence gate is bounded and sufficient for generic Relation Profile implementation approval.** There is no source-backed universal assertion `A -> A = ACCEPT`. The safe statement is: without an authorized amendment, the effective commitment remains A; amendment status, verdict binding, and substantive resolution are separate outputs.

## Source identities and terminology

All source files, hashes, branch identities, source classes and reviewed identifiers are enumerated in [the closure source map](relation-profile-evidence-closure-v0.json). Every repository below was inspected at exact bytes on canonical `main`; no moving branch alone is the evidence identity.

| Alias | Repository | Exact main SHA | Relevant files |
|---|---|---|---|
| RK | trustless-ai/recompute-kit | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/profile-amendment-v0/{profile-amendment-v0.spec.md,profile-amendment-v0.vectors.json,amendment_gate.py,profile-amendment-v0.reference.mjs}`; corresponding spec/vectors/reference plus `verdict_binding_gate.py` under `conformance/verdict-profile-binding-v0/`; spec/vectors/reference under `conformance/companion-envelope-v0/`; README/grade under `conformance/erc-8309-envelope-v0/` |
| CS | damonzwicker/erc8309-companion-drafts | `02fef5fd1f54eff9221b863cc746cb74a97f3220` | `8309-vantage-authority-companion-v0.3.9.md`, historical `cuts/8309-vantage-authority-companion-v0.3.3.md` |
| VC | babyblueviper1/invinoveritas | `bdba0b674c2b2d301b75b4b23a33702b0bacfa64` | Under `integrations/conformance/erc-8309-vantage/`: README, `services/vantage_resolution.py`, `tests/test_vantage_resolution.py`, envelope/verdict schemas |
| RV | pipavlo82/recomputable-verification-receipts | `287c0ea1c2578c1833405bc2476975f95addbada` | `docs/spec/RECOMPUTABLE_VERIFICATION_RECEIPTS_V0.md` |

CS is a normative **companion draft**, not proof of an adopted ERC or deployment. VC is a reference consumer pinned to version 0.3.3; its opening docstring still mentions 0.2.2. Do not call it a fully verified 0.3.9 implementation. CS's historical and current cuts retain the relevant Profile A and output distinctions; references to newer deployment/conformance totals are documentation, not reruns here.

Critical naming separation:

- **A/B in amendment vectors** denote arbitrary prior/proposed verification-profile objects and their commitments.
- **Profile A / Profile B in CS** mean Divergence Surfacing / opt-in Quorum. They are not automatically those amendment objects.
- **companion-envelope.v0** binds a PQ companion to a verdict core. **erc-8309.envelope** declares vantage-resolution conditions. They are different objects despite sharing the word envelope.
- **RVR receipt outcome/recomputation** (RV) is another pair of axes. Its `REPRODUCED` is not `resolved` or `bound`.

## A -> A: exact answer

RK amendment spec, section Rule, lists A -> A as “no change; normal resolution.” Its construction authorizes a **change** by matching prior/new commitments, task `escrow_ref`, and both parties' `signed_digest` to the exact amendment commitment. Otherwise the effective profile stays prior and status is `unresolved`.

Both reference implementations implement that fallback without a no-change fast path. Their eight published vectors contain no no-change row. A read-only in-memory probe of the exact Python function, using equal prior/proposed objects and no amendment/authorizations, returned:

```json
{"amendment_cc":null,"transition_status":"unresolved","effective_profile_commitment":"cc458bd42359a4dcd873cd3bde38cc45e5562f51f674c214b4659030317c70ce"}
```

This is independently observed **reference behavior**, not a new normative vector or permission to relabel the transition `permitted`. “Normal resolution” does not specify that amendment validation succeeds, that a verdict exists, or that divergent observations are resolved. The prose/implementation granularity mismatch remains documented rather than repaired.

| Proposed reading | Supported? | Exact boundary |
|---|---|---|
| Effective profile remains A | Yes | RK fail-closed rule and both implementations |
| Transition is explicitly accepted | No, not without a qualifying amendment | No published A -> A `permitted` vector; no-amendment function returns unresolved |
| Resolution is complete | Not implied | Requires a separately defined resolution layer/result |
| Divergence is resolved | No | CS §7.0 Profile A resolves nothing |
| No amendment edge, current profile remains A | Yes | Identity/no-op in profile selection, not successful edge authentication |
| Reference returns unresolved while retaining A | Yes | Independently probed; result above |

## Case matrix

`not evaluated` below is a review annotation, **not** an invented source enum. `bound` means profile/preimage digest binding only, not signature cryptography or business acceptance. Resolution column explicitly distinguishes RK binding status from CS substantive state.

| Case | Source artifact / identifier | Effective profile | Transition status | Resolution status | Verdict admissibility | RSI candidate relation outcome | Confidence / notes |
|---|---|---|---|---|---|---|---|
| A, no amendment; proposed=A | RK spec Rule; `profile_transition` / `profileTransition`; derived probe | A | Reference: `unresolved` | Without verdict: not evaluated | A verdict may bind if its core names A and its signed digest names that core | Preserve effective=A and transition=unresolved; do not synthesize ACCEPT | High reference evidence; spec says no change/normal resolution, no exact normative no-op status |
| A, malformed amendment object (missing/wrong binding members) | RK Rule; reference `.get` guards; `wrong-prior`/`wrong-escrow` are well-shaped relation negatives | A for evaluable rejected binding | `unresolved` | Not evaluated without verdict | A can still be the binding target; malformed edge authorizes nothing | Keep unavailable transition and prior commitment | High for wrong-binding vectors; arbitrary malformed type is different: a truthy string raises AttributeError in the probe, not a semantic unresolved result |
| A -> B unauthorized, no amendment | RK `bare-swap-no-amendment` | A | `unresolved` | Verdict A can be bound; verdict B is unresolved under the supplied effective A | B does not become effective | Structured transition refusal/fallback; separately evaluate verdict | High spec/vector; composition derived from RK verdict Rule |
| A -> B valid bilateral amendment | RK `permitted`; prior/new/escrow and buyer/supplier signed_digest checks | B | `permitted` | Not evaluated until verdict supplied | B is eligible target for binding | Transition binding established at the suite's binding-only scope | High spec/vector; “authenticated” here is **not independently verified signatures** |
| Effective B + verdict B | RK verdict `bound`; Composition section | B | `permitted` from valid amendment when composed | RK `resolution_status=bound` | Bound commitment B; no substantive settlement claim | Preserve both outputs, including bound B | High spec/vector; crypto verification separate |
| Effective B + verdict A | RK verdict Rule and `wrong-profile` discriminator | B | Earlier valid transition remains `permitted` | RK `resolution_status=unresolved`; bound commitment null | Wrong-profile verdict not certified | Verdict relation not established; do not undo valid transition | High rule; exact A operand is a rule-derived instance, published wrong-profile vector uses another unequal commitment |
| Unresolved divergence, no amendment | CS §§6, 7.0; VC `test_profile_a_resolves_nothing`, `test_quorum_failure_falls_back_to_profile_a_never_to_agreement` | A if separately applying RK no-change rule | RK unresolved if amendment evaluator is called | CS `divergence`, preserved/unresolved; RK binding status independent | A verdict can attest the unresolved observation result without resolving it | Separate effective profile, binding and divergence state | High CS normative distinction; no published joined RK/VC end-to-end vector |
| A, no amendment + correctly bound verdict A | RK verdict Rule/Composition; derived in-memory probe | A | `unresolved` | RK `bound` | Binding admissible; completion/finality not implied | `{transition:unresolved, effective:A, verdict_binding:bound}` | Exact function composition reproduced; not an end-to-end protocol authority claim |

The independently run source-vector checks reproduced 8/8 amendment expectations and 6/6 verdict expectations. The derived no-change + verdict-A probe returned `bound`. These are in-memory calls of pinned reference functions, not RSI tests or new adapter code. A first attempt exceeded the Windows command-length limit before execution; the bounded retry fetched the same pinned sources in memory and completed. No false semantic result is inferred from that tooling failure.

## What unresolved means in each source

1. **RK amendment**: conditions for a permitted amendment were not established; effective commitment fails closed to prior. Reasons include absence and explicit mismatches. It does not mean “the prior profile is unknown,” or “the business dispute is unresolved.” The internal predicate can be false while the source API still uses its categorical unresolved state.
2. **RK verdict binding**: profile/preimage or resolver signed-digest binding was not established; bound commitment null. Does not invalidate a previously valid amendment.
3. **RK companion envelope**: absent companion or absent/wrong content_address is unresolved, never manufactured binding or boolean false. It is not a signature-validity result.
4. **CS divergence**: unresolved disagreement is preserved as the verified observation-level fact. Profile A emits agreement/divergence/insufficient-observation, never resolved. `resolved(policy,set,conditions)` belongs to opt-in resolution and is never folded into agreement (CS §§6-7; VC named tests).
5. **RV CANNOT_RECOMPUTE**: required normative dependency/evidence cannot legitimately support evaluation; separate from semantic UNVERIFIABLE and from a completed REPRODUCED result (RV §§2,6,9).

Thus neither “relation false” nor “relation unknown” is a safe universal translation of the string unresolved. Its source-scoped reason and associated commitments/results must travel with it.

## Decomposition and design assessment

Recommend **R2**, composition of independently scoped relations:

- transition-binding relation selects effective profile from prior/proposed/amendment/required parties;
- verdict-binding relation checks the verdict core against that effective commitment and its signed digest;
- when the task includes vantage resolution, retain its substantive observation/resolution state as a distinct component, with CS envelope/as-of/evidence obligations.

R1 alone cannot cover wrong-effective-profile verdicts. R3 may be a useful implementation representation of separate outputs, but these sources do not establish a universal mutable state machine, rollback protocol or amendment-status-to-business-status transition table. Do not invent one. A multi-valued **structured product of outcomes** is sufficient; no universal boolean truth is required.

| Current draft issue | Assessment | Reason |
|---|---|---|
| Boolean-only truth | GREEN | §5 explicitly rejects universal booleans and preserves categorical outcomes |
| Effective profile vs resolution state | GREEN | §§2,5 permit profile-specific inputs/outputs and scoped claims |
| Unresolved vs inability to execute | GREEN | §9 distinguishes completed source-native outcome from infrastructure unavailability |
| Temporal/as-of | GREEN | §7 requires source-specific point and evidence, no ambient time |
| Signed edge vs crypto proof | GREEN | §§5,7,8 preserve component validity and independent evidence |
| A -> A wording and Profile A homonym | YELLOW | Explicit clarification needed; no schema-level semantic change |
| Comparator/core domain branches | GREEN | Compare complete profile-specific observations; core need not interpret any status |

Proposed wording only, **not applied** to the prior design:

```diff
- RVR's A-to-A composed result needs a pinned rule/vector
+ RVR no-change is bounded as effective profile remaining A. The amendment
+ references report unresolved without an amendment; a correctly bound A
+ verdict may independently report bound. Neither status establishes completed
+ vantage resolution. Commitment placeholders A/B are not companion Profiles A/B.
+ Preserve these source-scoped outputs; no universal A-to-A ACCEPT is claimed.
```

A dedicated end-to-end no-change vector remains desirable for a future domain adapter, but it is not required to prove the generic design can represent these distinctions. Full bilateral signature authentication, deployment behavior, and business-resolution conformance remain outside this pass. No source inconsistency is silently normalized into a new oracle.
