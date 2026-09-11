# ERC-8312 aggregate-budget reproduction

Scope: the pinned Aggregate Budget draft, exact reference cursor, its deliberate
per-edge counterexample, and the recompute-kit admitted-log predicate. This is
single-chain metered conservation, not proof that all consuming paths use the
meter. No external repository is modified.

From a clean RSI checkout with Python 3.12/3.13 and Node 22.15.0:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest tests.test_aggregate -v
python -O -m unittest tests.test_aggregate -v
python tools/run_aggregate.py --include-previous --output artifacts/aggregate.json
python tools/prove_aggregate_can_fail.py --output artifacts/aggregate-mutations.json
```

Evaluation is offline after checkout/dependency installation. It uses the frozen
EVM runtime, ABI/bytecode and gate; no user-home paths, RPC, wallet, Forge, Bun,
private source checkout or network request is used during evaluation.

Rebuild the frozen artifacts with the lockfile (network needed only for npm ci):

```sh
mkdir -p artifacts/aggregate-phase3f/runtime
cp evidence/aggregate/package*.json artifacts/aggregate-phase3f/runtime/
(cd artifacts/aggregate-phase3f/runtime && npm ci)
node evidence/aggregate/compile.cjs
node evidence/aggregate/build.cjs
git diff --exit-code -- evidence/aggregate
```

Solc 0.8.24, Cancun and optimizer 200 match the reference foundry.toml. The EVM
is EthereumJS; supplied timestamps are local simulation inputs. It does not
establish chain history, consensus, finality, signatures or economic effects.
The source counterexample contract is extracted intact from its test file;
only Forge test imports and the surrounding test class are omitted. Six explicit
mutant builds accompany the canonical cursor. They are selected only by the
mutation runner, never by a fixture-supplied artifact path.

The exact recompute-kit TypeScript gate is transpiled with an export bridge for
`valueFor`. Its Bun CLI, expected-vector grading and self-test branches do not
run under Node. Actual observations come from EVM returns/reverts, Drawn events
and storage views, then this source gate sums admitted events by root/period.
The counterexample emits no Drawn event: its separate log origin is successful
source calls, reconciled with its native `totalRealized` view. These origins are
never described as interchangeable on-chain evidence.

Transport uses canonical ASCII JSON, decimal strings for uint256/uint64, lower
case hex addresses/salts, and bounded integer fixture aliases. Scope is at most
4 roots, 64 calls, node aliases 0..255 and period keys 0..1024. Every attempted
draw's nonnegative period must be in the query set. The total of attempted draw
amounts must fit uint256; overflow/panic traces are outside this profile. Values
above JavaScript's safe integer range remain decimal strings and are passed to
BigInt/ABI encoding exactly. A 2^100-scaled trace is tested. Source prose Unicode
is retained byte-for-byte as provenance; it is not transported as semantic input.

Fixture root aliases are resolved to native deployment-derived root IDs. Source
events must name the invoked root; queried storage and admitted-log sums are
compared. The report retains period/root aliases rather than claiming independent
deployment or historical-root authentication. No amount rounding occurs.

Frozen expectations detect divergence from previously admitted semantics; they
do not by themselves prove that the original expectation was independently
derived. Here the admitted decisions were declared from draft section 5 and
reference tests before running the predictor/adapter comparison. The separately
implemented Python predictor folds an admitted ledger instead of executing the
source storage update algorithm. Shared semantics, codec, immutable inputs and
pin verification remain common dependencies; author independence is UNKNOWN.

Generated runtime/license text is preserved, including dependency whitespace.
Source-file hashes and the 498-file prior baseline are checked in tests. The
new workflow rebuilds and checks frozen artifacts on Linux as well.
