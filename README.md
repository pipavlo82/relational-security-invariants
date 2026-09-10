# Relational Security Invariants

Relational Security Invariants (RSI) is a conformance framework for failures where each local component can remain valid while the security-relevant relation between components is changed, missing, stale, or unauthorized.

**Start here: `main` is the single maintained implementation.** Use the commands below. The separate initial prototype has been retired from active development and preserved in Git history; [the reconciliation record](spec/repository-reconciliation.md) explains the choice and exact verification results.

```text
local validity preserved + protected relation broken
=> no acceptance / authority / state / policy / provenance / status promotion
```

This project does not claim to invent replay protection, identity binding, nonce uniqueness, complete mediation, trust-root continuity, or relational security reasoning. The research question is whether one implementation-facing adversarial fixture model can unify these relation failures across domains.

**Private v0 implementation/review candidate. Not a frozen standard, production
security library, completed audit, or proof of novelty.**

A locally valid component must not inherit identity, authority, scope, state,
policy, or completion semantics from a relation that has not been established.
RSI names the protected relation; Relation-Binding Conformance Fixtures (RBCF)
exercise it. This repository implements a small, executable proposal derived
from Pavlo Tvardovskyi's `relational-security-invariants-novelty-research-v0.md`.

## Run it

Python 3.12 or 3.13:

```sh
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python tools/generate_fixtures.py --check
python tools/validate-fixtures.py
python -m rsi.run --output artifacts/baseline.json
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
python tools/prove_can_fail.py --output artifacts/prove-can-fail.json
```

The corpus has **6 families x 3 cases x 2 target adapters = 36 evaluations**.
There are 12 isolated source mutants (one per family per adapter) and 4
classifier controls. Run the commands to establish the result at your checkout;
the existence of this README is not test evidence. Machine-readable outputs are
written to ignored `artifacts/`; their evidence blocks carry SHA-256 digests.

## Scope of this first implementation

| Family | Protected relation | Negative case |
|---|---|---|
| RSI-001 | signer to expected subject | authentic signature, different expected key |
| RSI-003 | authentication before state commit | invalid signature must not commit tentative state |
| RSI-004 | position to unique consumer | deterministic read/read/commit/commit interleaving |
| RSI-006 | authenticator to context | valid signed payload, substituted scope |
| RSI-008 | confirmation to required evidence | valid operation, no qualifying acknowledgement |
| RSI-009 | object to ingestion policy | signed but policy-ineligible object through four paths |

Every family includes an accepting control and a **mirror-positive**: the signed
payload bytes change (formatting and a new valid signature), while its protected
meaning and expected output remain unchanged. An always-reject checker does not
pass this corpus.

RSI-003 intentionally does **not** preserve cryptographic local validity.
RSI-004 is a trace/schedule test, not a single-tuple endpoint substitution.
RSI-008 removes evidence; missing evidence is **UNVERIFIABLE**, not evidence that
an operation never happened. See [design decisions](spec/design-decisions.md).

## What is actually executed

`adapters/messaging` is a synthetic signed-message/state model.
`adapters/generic` is a synthetic receipt journal using isolated in-memory SQLite.
Both execute real Ed25519 verification over exact payload bytes. They are
**different reference target domains, not two independently authored production
systems**. They share the wire parser, crypto library and serialization helper.
There is no Signal ratchet, deployed ReceiptOS integration, RPC, network attack,
OS-level race test, or crash-durability proof in this cut.

The trusted reference oracle is separate from the targets. The runner verifies
schema, exact fixture pins and regenerated oracle expectations before execution.
Adapters receive only a detached request: never fixture ids, roles, expected
answers or mutation labels. Observations include decisions, before/after state,
effects and allocated positions. PASS means these matched the declared oracle;
it does not mean the adversarial input was accepted.

## Prove that it can fail

The mutation gate copies the checkout to temporary directories, applies exactly
one source edit, compiles it, and re-executes the actual adapter. A mapped
comparison failure earns KILLED. Syntax errors are VACUOUS; exceptions, timeouts
and invalid output are RUNNER_ERROR; unrelated failures are OFF_TARGET.
Collateral cases are retained. No mutation is performed in the working tree.

## Repository map

- `spec/`: core, terminology, threat model, byte contract, conformance, decisions.
- `schema/`: closed Draft 2020-12 fixture/request and observation contracts.
- `fixtures/`, `oracle/`, `manifest.json`: six pinned fixture files and a detached oracle set.
- `rsi/`: strict loader, reference predicates and evaluation runner.
- `adapters/`: two synthetic native target implementations.
- `tools/`: definition-derived generation, validation and source mutation gate.
- `tests/`: contract, negative, mirror, evidence-binding and harness tests.
- `research/`: attributed prior-art note and provenance/scope record.

## Relationship to existing work

This is a security-oriented research/conformance lane **informed by**
[Protected Relation Fixtures](https://github.com/pipavlo82/protected-relation-fixtures),
not an update to its schema or frozen corpus. ReceiptOS, Semantic ABI and TSEI
are prospective integration targets, not claimed integrations. No code or
historical artifact in those repositories is modified. No formal PRF-compatible
adapter is claimed. [Integration boundary](spec/integration-boundary.md).

The underlying mechanisms have extensive prior art; the candidate contribution
is their cross-domain conformance packaging. Neither novelty nor general
cross-domain transfer is established by these synthetic models. A future
milestone needs pinned real target revisions and independent adapter authors.

No third-party vulnerability report or live exploit details are included. There
is no public release or selected open-source license yet; see `LICENSE` and
`SECURITY.md`. No version tag is a frozen conformance claim in this first commit.

Expectation extensibility: [Expectation Contract v0.1](spec/expectation-contract-v0.md), with the [extension architecture checkpoint](spec/extension-contract-v0.md).

Registered execution: `python -m runner.extension_runtime --output artifacts/extension.json`; see the [Extension Contract](spec/extension-contract-v0.md).
