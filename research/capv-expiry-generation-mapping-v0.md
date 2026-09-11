# Phase 3E: CAPV expiry and program-generation binding

The relation is generation-specific: freshness of a supplied expiry is separate
from proof authorization of that expiry. The old public allowlist proof verifies
under the SDK-pinned verifier after expiry-only substitution. The fixed public
allowlist proof verifies at its original expiry and reverts after substitution.
These are real Solidity Honk verifier executions with BN254 pairing, not mocked
verifier responses or conclusions inferred only from a source diff.

## Source and feasibility gate

RSI started at `7b1eed97a54e6f16b9c57368e0de824756f9979f`, main equal to
origin/main, clean, with H2 closed. The pre-change suites passed 446 tests in
normal and optimized Python; the preserved baseline is 85 conformance PASS and
61 KILLED mutations. All 422 tracked files were hashed before implementation.

Current public refs were independently fetched, with no drift from the supplied
expectations. Historical commits were fetched explicitly, never replaced by main.

| Surface | Branch / role | Exact commit |
|---|---|---|
| trustless-ai/agent-sdk | main, pinned consumer | e41b117893fb56bc869922de378daf91aad63def |
| zexoverz/confidential-agent-policy-verdicts | historical allowlist generation | 948e090c09dd5ec1d4593013303bc5260ef7c466 |
| same upstream | programKey check fix | 6da56d5a1ee1b09e832f030442515ebd24db1ff5 |
| same upstream | expiry fix / evaluated fixed generation | d950ac1422cf79bafff11fcfb62c3e8b4ce3d782 |
| same upstream | current main | 7da0d69435190f1462e295c61fc0514a4754818d |
| ethereum/ERCs | master | 84b46e7d69d08dbd8876503e435fd299211c26b8 |
| trustless-ai/agent-ercs | main, interface/composition only | 01283ca57305f915afb560d23359a27fd748eb5a |

The source map records all 30 source files, SHA-256, Git blob OID, class, local
copy and reason. Git blob identity and raw SHA-256 were verified after download.
The SDK's verifier, proof and public-input fixture are byte-identical to 948e090.
The SDK adapter is a later hardened adapter, not a byte-identical historical
adapter: it constructs its verifier and checks programKey against VK_HASH.
Its PROVENANCE and `test_KNOWNGAP_SameProofVerifiesUnderDifferentExpiry` explicitly
disclose the separate expiry omission. This is not an undisclosed current-upstream bug.

Current upstream main and d950ac have identical Git blobs for the evaluated
allowlist circuit, adapter, verifier, proof and public inputs. The intervening
deployment script is deployment intent/reference evidence; no live deployment
or on-chain registry state was independently verified here.

The read-only feasibility probe compiled and ran both exact public verifier
generations before profile implementation. Old E1 and E1+1 returned true; fixed
E1 returned true and E1+1 reverted (`0x9fc3a218`). Both public fixture packages
were sufficient, so no synthetic proof or private proving material was needed.

## Exact relation

The old Solidity projection contains 39 field elements, in this order:

```text
agentId, domainId, policyRoot,
actionCommitment[0], ..., actionCommitment[31],
nullifier, decision, policyKind, executor
```

Each actionCommitment byte occupies a separate field element. The fixed
projection appends `expiry` as element 39, giving 40 elements. Observation
block timestamp is absent in both. Expiry is a uint64 carried as an exact
decimal string by the profile. The source freshness predicate is
`observation_time < supplied_expiry`; equality is expired.

Old VK_HASH:
`0x15dfad359ae3d919488f92128f12290d908220925f263eeec28e8a97f21a372a`.
Fixed VK_HASH:
`0x10d07da428220548a6d7c4f405b1c8ded613a92e0b797262985a9ccdb1e6288e`.

Program identity consists of the pinned generation and its compiled verifier/VK.
Consumer provenance is a separate relation. A fixed proof can verify while
failing the assertion that it represents the SDK's historical pinned generation.
The existence of d950ac does not change what the SDK at e41b117 pins.

The canonical ERC text requires every Verdict field to be public and includes
expiry. At the same canonical commit its Noir asset omits expiry and is
byte-identical to the old upstream circuit. This is an implementation/spec asset
mismatch, not an assertion that the normative requirement is wrong or an exploit.

## Cases and ownership

| Fixture | Protected experiment | Expected observation |
|---|---|---|
| CAPV-RSI-001 | normative obligation versus old projection | obligation true; projection omits expiry |
| CAPV-RSI-002 | pinned old control | real proof and adapter return true |
| CAPV-RSI-003 | only old expiry E1 -> E1+1 | same proof still true; expiry binding absent |
| CAPV-RSI-004 | both substituted expiries fresh | freshness does not establish expiry proof binding |
| CAPV-RSI-005 | fixed control at E1=1900000000 | real proof true; expiry public and bound |
| CAPV-RSI-006 | only fixed expiry E1 -> E1+1 | real verifier/adapter revert |
| CAPV-RSI-007 | two cross-generation proof substitutions | both rejected by real verifier |
| CAPV-RSI-008 | historical SDK plus attempted retroactive fixed assignment | old semantics retained; fixed assignment mismatches consumer pin |
| CAPV-RSI-009 | canonical text versus canonical circuit | explicit MISMATCH |
| CAPV-RSI-010 | observation time 1700000000 -> 1700000001 | same fixed proof relation; both fresh |
| CAPV-RSI-011 | wrong programKey, separately for each verifier | raw proof true; adapter returns false |

There are 11 fixtures and 14 cases. Inputs are locally well-formed even for
negative relations. No fixture ID conveys semantic authority. PASS means actual
structured observations equal the admitted expectations; it does not certify
that the old artifact satisfies the normative expiry requirement. Missing binding
is reported explicitly, never recast as security correctness.

The ERC declares Verdict/public-input requirements. Upstream produces circuits,
verifiers and fixture evidence. SDK pins a generation and consumes the adapter
result. The generated verifier establishes proof/public-input validity; the
adapter checks programKey; the Guard separately checks freshness and other
conditions. RSI observes this composition boundary without implementing the
whole Guard or claiming executor authorization, root authority or execution.

## Execution and expectation separation

`adapters/capv` invokes the exact compiled Solidity through committed EthereumJS
EVM code. A derived ProjectionProbe only exposes the source adapter's internal
projection; the source verifier and adapter are unmodified. The harness runs
both direct verifier and adapter calls, distinguishing TRUE, FALSE and REVERT.
Non-revert VM failures, deployment failures and schema/import errors are not
proof rejections or mutation kills.

The separately implemented expectation predictor reads the pinned Noir public
signature and binary public-input fixture and compares candidate field words.
It neither imports the adapter nor executes the Solidity verifier. It is a
bounded predictor for these known valid proof fixtures, not a second Honk
implementation or an oracle for arbitrary proofs. It relies on the source's
statement of proof/public-input binding and on the supplied fixture provenance.

Frozen expectations were derived as a manual obligation table, recorded in
capv-golden-derivation-v0.json, and admitted against that predictor. They were
not copied from the upstream test's reported result. Frozen expectations detect
divergence from previously admitted semantics; they do not by themselves prove
that the original expectation was independently derived.

No clean-room third leg or author independence is claimed. Shared immutable
source bytes, source-pin validation, RSI codec and generic admission remain
common dependencies. Distinct Solidity/EVM and Python implementations do not
eliminate common interpretation risk. The six one-sided mutations demonstrate
load-bearing separation, not general oracle independence.

## Mutation scope

| Mutation | Actual-side change | Mapped assertion |
|---|---|---|
| CAPV-M1 | fresh expiry promoted into proof binding | fresh_not_bound |
| CAPV-M2 | fixed projection drops expiry | fixed_control, real verifier no longer accepts |
| CAPV-M3 | verifier generation silently selected from proof generation | generation substitution |
| CAPV-M4 | fixed semantics applied to SDK's historical pin | nonretroactivity |
| CAPV-M5 | SDK adapter programKey gate removed | program_key, proof still valid but gate fails to reject |
| CAPV-M6 | observation time treated as proof-bound | timestamp mirror-positive |

Only mutation builds alter local in-memory source strings. External source
files remain exact. All six mutations execute the mapped check and are KILLED,
with no setup-only kills or taxonomy changes.

## Limits and reproduction

This is public allowlist-fixture verification, not witness/proof generation,
proof-system security, deny/non-membership coverage, arbitrary deployment
configuration, domain/root acceptability, executor authorization, overall Guard
acceptance or execution occurrence. Those stronger capabilities remain
UNSUPPORTED inside otherwise passing conformance rows.

The fixed constructor accepts a verifier and expected key from its deployer;
this harness supplies its actual compiled verifier and VK. It does not establish
that every external deployment does so. No ecosystem-wide ERC-8354 claim follows.

The unchanged ASCII/safe-integer transport carries large integers as validated
decimal strings and bytes/addresses as exact hex. Raw proof blobs are read from
hash-pinned binary artifacts, not coerced through JSON numbers. No generic
schema, comparator, taxonomy or prior-domain semantic change is needed.

See evidence/capv/REPRODUCING.md for offline execution and deterministic rebuild
commands. Reports include exact source and compiled artifact hashes.
