# Relational Security Invariants

Relational Security Invariants (RSI) tests whether locally valid components preserve the security-relevant relation required by a downstream claim. Relation-Binding Conformance Fixtures (RBCF) exercise substitutions, missing evidence, stale bindings and false claim promotion.

```text
local component validity != protected relation established
protected relation established != every stronger security claim proven
```

**Bounded v0 is closed and tagged.** The `v0` snapshot is commit
`8d8e31291ecf96284212a353efb66f606cff2953`; `main` is the maintained branch.
Start with the [v0 closure audit](research/rsi-v0-closure-audit.md),
[exact source pins](research/rsi-v0-source-pins.json),
[mutation matrix](research/rsi-v0-mutation-matrix.md) and
[unsupported surfaces](research/rsi-v0-unsupported-surfaces.md).
Earlier phase reports are historical evidence, not the current coverage summary.

RSI demonstrates implementation-facing reuse of the same generic conformance
architecture across **eleven bounded real relation families** (ten in frozen v0, plus the
post-v0 Semantic ABI declared-edge profile). It functions as a
cross-repository conformance plane for these validated surfaces. This is not
universal security, ecosystem-wide verification, a production security library,
a complete audit of the source repositories, or a proof of novelty.

## Verified v0 snapshot

These are results recorded at the tagged snapshot, not a claim that a future or
modified checkout has passed. Exact-HEAD CI completed on Python 3.12 and 3.13.

| Gate | Result |
|---|---|
| Full unit suite | 539 PASS |
| Full suite under `python -O` | 539 PASS |
| Conformance | 123 PASS; FAIL / INVALID_FIXTURE / UNSUPPORTED = 0 |
| Mapped mutations | 84 KILLED; SURVIVED / VACUOUS / NOT_APPLIED = 0 |
| Generic pipeline | 10 real families plus legacy; 11 admitted expectation profiles |
| Prior results preserved at 3G closure | 111 outcome rows and 76 mutation records; exact differences = 0 |
| Protected pre-3G files | 572 unchanged |
| Generic core / schemas / comparator / taxonomy | unchanged across domain admission; semantic exceptions = 0 |
| Static anti-coupling | no domain-specific branches in the 17 audited generic Python files |

**PASS means the actual observation matches admitted expected semantics.**
A negative case can PASS by correctly rejecting a substitution. A documented
source limitation can also be reproduced without approving it as secure.
Internal unsupported capabilities remain explicit even when conformance PASSes.
Mutation counts establish that selected decisions matter on this corpus; they
are not a measure of complete security coverage or oracle independence.

## Post-v0: Semantic ABI declared-edge validation

The [Semantic ABI admission report](research/semantic-abi-validation-v1.md)
adds one bounded family at upstream commit
`d15c666dfccff17f7350fe97d2fc7b71cb2cbaee`: exact claim, authority, scope and
temporal-key/value compatibility, including the directed local recomputation
rule. Actual observations execute the pinned upstream JavaScript linker.
Compatible declarations do not prove claim truth, freshness or action execution.

Local validation: **586 unit tests**, **586 under `python -O`**, **139 conformance
PASS** (123 previous + 16 new), and **10 new mapped mutations KILLED**.
The 84 prior mutation records and their implementation files are unchanged;
those gates were not rerun for this addition. The [machine-readable evidence](research/semantic-abi-validation-v1.json)
records that distinction. The table above remains the immutable v0 snapshot.
These are local gate results. CI runs separately for each published commit.

```sh
python -m unittest tests.test_semantic_abi -v
python tools/run_semantic_abi.py --include-previous --output artifacts/semantic-abi.json
python tools/prove_semantic_abi_can_fail.py --output artifacts/semantic-abi-mutations.json
```

## Validated relation families

Each link leads to the exact source-backed scope and its validation evidence.

| Family | Validated relation | Stronger claim not established |
|---|---|---|
| [Crystal Receipt](research/crystal-receipt-validation-v0.md) | Semantic-snapshot equivalence, substitution discrimination and a real mirror-positive | Provenance authority, Lane K, broad ReceiptOS semantics |
| [RVR](research/rvr-digest-binding-validation-v0.md) | Profile-transition / verdict digest binding, effective-profile continuity and unresolved separation | Cryptographic signatures or authenticated transition chain |
| [TSEI](research/tsei-serializer-adoption-validation-v0.md) | Serializer binding, mechanism / adoption / record-introduction boundaries and non-retroactivity | Provenance authority; public recomputation operands are unavailable |
| [PQ](research/pq-policy-asof-validation-v0.md) | Cutoff, governing as-of binding, historical/current separation and stale snapshots | Authenticated transition chain or independent anchor verification |
| [TAS](research/tas-context-invocation-validation-v0.md) | Accepted source context to `getTask` read dispatch | Arbitrary invocation authorization, context authenticity or execution occurrence |
| [ConsultEscrow](research/consult-escrow-validation-v0.md) | Contract-local `jobId` / `resultHash` to release | Cross-deployment replay security, chain finality or end-to-end payments |
| [verify-layer](research/verify-layer-validation-v0.md) | Account proof/root and supplied RPC-context binding | Consensus/header authority, finality, storage proofs or general downstream claim truth |
| [ERC-8354 CAPV](research/capv-expiry-generation-validation-v0.md) | Expiry proof binding versus freshness across exact old/fixed program generations | Full Guard acceptance, executor authorization or execution occurrence |
| [ERC-8312 Aggregate Budget](research/aggregate-budget-validation-v0.md) | Root/period admitted-budget conservation versus local edge validity | Non-bypassability, asset movement, cross-chain budgets or authoritative chain state |
| [ERC-8299 reference application](research/judgment-execution-validation-v0.md) | Signed verdict to supplied terminal-record binding | Action authorization/occurrence, anchor authority, judgment soundness or complete ERC-8299 semantics |
| [Semantic ABI (post-v0)](research/semantic-abi-validation-v1.md) | Supplied typed claim-edge compatibility; bounded directed authority conversion | Claim truth, cryptographic validity, freshness, action execution or backend-wide conformance |

CAPV preserves the distinction between the disclosed old consumer pin and the
later upstream expiry-binding fix. The newer program does not retroactively
upgrade historical artifacts. The ERC-8299 reference control contains a signed
**reject** verdict: successful record binding is not permission to execute.

**ERC-8380 Phase 3D remains BLOCKED** on the pinned draft/prover alignment
[evidence](research/erc8380-commitment-alignment-v0.md); it is not an admitted
RSI domain. Full RVR authentication and TSEI provenance-authority validation
also remain unsupported. PQ's SLH-DSA artifact / ML-DSA label mismatch remains
recorded rather than normalized away.

## How conformance runs

```text
fixture registration
  -> relation profile
  -> atomic expectation admission
  -> adapter execution
  -> generic comparator
  -> conformance report
```

Domain-specific slots and checks live in additive profiles and adapters.
Adapters receive detached requests, not expected rows or fixture roles.
Admission checks pinned expectations against a separately implemented expectation
predictor before execution. The comparator and top-level result taxonomy remain
generic. Unknown or unavailable profiles remain explicit rather than falling
back to guessed semantics.

Contracts: [Relation Profile](spec/relation-profile-contract-v0.md),
[Expectation](spec/expectation-contract-v0.md),
[Extension](spec/extension-contract-v0.md).

## Run the tagged validation

Use **Python 3.12 or 3.13** and **Node 22.15.0**, matching CI. Run from the
repository root. To reproduce the frozen snapshot, use a clean checkout of
`v0`; run these commands on `main` to evaluate the current checkout instead.

```sh
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt

# All admitted profiles, including the legacy corpus: 123 checks at v0.
python tools/run_judgment.py --include-previous --output artifacts/v0.json

# Full test suite, including optimized execution.
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v

# Crystal clean-room third-leg comparison and common-mode experiments.
python tools/check_crystal_cleanroom.py --output artifacts/h2.json
```

`run_judgment.py --include-previous` composes all existing registrations through
the generic runtime; its name reflects the last added family, not a different
comparator. Reports go to ignored `artifacts/`. Pinned source material is included
according to each domain's source map; evaluation does not silently fetch latest
upstream semantics.

Reproduce all 84 mapped mutations with the following tools. Each accepts
`--output artifacts/<report>.json`; counts below belong to `v0`.

| Tool under `tools/` | KILLED |
|---|---:|
| `run_registered_mutations.py` | 16 |
| `prove_relations_can_fail.py` | 7 |
| `prove_crystal_can_fail.py` | 3 |
| `prove_rvr_can_fail.py` | 6 |
| `prove_tsei_can_fail.py` | 6 |
| `prove_pq_can_fail.py` | 7 |
| `prove_tas_can_fail.py` | 5 |
| `prove_consult_escrow_can_fail.py` | 5 |
| `prove_verify_layer_can_fail.py` | 6 |
| `prove_capv_can_fail.py` | 6 |
| `prove_aggregate_can_fail.py` | 9 |
| `prove_judgment_can_fail.py` | 8 |

A kill requires execution of the mapped decision and failure of its intended
assertion. Setup/import/schema errors do not count as kills. H2's
`COMMON_MODE_CAUGHT` experiments are separate hardening evidence, not additional
entries in the mutation taxonomy.

## Independence and transport limits

Use **separately implemented expectation predictor** as the global wording.
Separate files or languages do not establish independent algorithms, authors or
semantic interpretation. The [H1 audit](research/predictor-adapter-independence-audit-v0.md)
records these dimensions; author independence remains UNKNOWN.

Crystal's [H2 clean-room reproducer](research/crystal-cleanroom-third-leg-v0.md)
adds a definition-derived third leg and catches two selected common-mode errors
shared by actual/predictor test doubles. Its score remains **10/15, MODERATE**.
This does not make all domains fully independent.

Frozen expectations detect divergence from previously admitted semantics; they
do not by themselves prove that the original expectation was independently derived.

The generic transport supports ASCII and safe integers. Domain-declared,
validated hex/decimal strings carry exact large values and proof bytes. The
shared codec is not full JCS, and Unicode, floats or raw binary must not be
silently coerced. Shared transport/admission helpers remain a common-mode risk.

## Legacy corpus and repository map

The original synthetic corpus remains **6 families x 3 cases x 2 adapters = 36
checks**, included in the 123 total. It covers subject binding, authentication
before state commit, unique consumption, context binding, evidence-dependent
status and ingestion policy. Both synthetic targets execute real Ed25519
verification; they share wire/crypto helpers and are not independently authored
production systems. See [design decisions](spec/design-decisions.md).

Run that corpus alone with `python -m rsi.run --output artifacts/legacy.json`.
The retired alternative prototype remains in Git history; the
[reconciliation record](spec/repository-reconciliation.md) explains why `main`
is the single maintained implementation.

| Path | Purpose |
|---|---|
| `spec/`, `schema/` | Core and extension contracts, closed schemas |
| `fixtures/`, `oracle/`, `manifest.json` | Original synthetic corpus and oracle |
| `corpora/`, `profiles/`, `extensions/` | Domain fixtures, expectation/relation profiles and registrations |
| `adapters/` | Actual execution paths for synthetic and source-backed domains |
| `rsi/`, `runner/` | Generic loading, admission, execution and comparison |
| `evidence/` | Pinned source material and historical preservation records |
| `reproducers/` | Standalone hardening/reproduction paths |
| `tools/`, `tests/`, `.github/workflows/` | Reproduction, mutations, tests and CI |
| `research/` | Source maps, phase reports, independence audits and v0 closure |

## Relationship to other work

RSI is informed by Protected Relation Fixtures; it does not alter that project's
frozen corpus. ReceiptOS owns an evidence/provenance artifact role.
The [ecosystem map](research/trustless-ai-cross-repo-map-v0.md) is a historical
architecture inventory; use the v0 audit above for current validated coverage.
External source repositories and their historical artifacts are not rewritten
by RSI validation.

The candidate contribution is adversarial cross-domain conformance packaging,
not the invention of replay protection, identity binding or relational security
reasoning. See [prior art](research/prior-art-v0.md), [LICENSE](LICENSE) and
[SECURITY.md](SECURITY.md). **No open-source license or patent grant has been
selected.** The bounded `v0` tag is an evidence snapshot, not an ERC standard,
production-safety certification or GitHub Release.
