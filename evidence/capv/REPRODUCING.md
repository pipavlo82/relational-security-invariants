# CAPV pinned proof reproduction

Scope: the SDK-pinned allowlist generation and the expiry-bound allowlist
generation. No proof is synthesized. The source Solidity verifier and adapter
are compiled unchanged; ProjectionProbe inherits the adapter and exposes only
its internal public-input projection. It introduces no verification predicate.

Evaluation from a clean RSI checkout uses Node 22.15.0, Python development
requirements and committed EVM/runtime/bytecode/proof files. No npm install,
RPC, proving service, home-directory artifact or network is needed:

```sh
python tools/run_capv.py --include-previous --output artifacts/capv.json
python -m unittest tests.test_capv -v
python tools/prove_capv_can_fail.py --output artifacts/capv-mutations.json
```

Rebuild the committed bytecode and runtime (network needed only to materialize
the exact package-lock dependencies), from the repository root:

```sh
mkdir -p artifacts/capv-phase3e/runtime
cp evidence/capv/package*.json artifacts/capv-phase3e/runtime/
npm ci --prefix artifacts/capv-phase3e/runtime
node evidence/capv/compile.cjs
node evidence/capv/build.cjs
git diff --exit-code -- evidence/capv
```

Compiler: solc 0.8.27, Cancun, optimizer enabled/200 runs. EVM: EthereumJS
3.1.1, Cancun. Default contract-size limits apply. Actual controls reach BN254
pairing precompiles; failures in deployment, compilation or non-revert EVM
execution are errors, never claimed proof rejection or mutation kills.

`fixed-drop.json` and `sdk-key.json` are explicitly generated mutation-only
artifacts, not upstream generations. Canonical execution selects sdk/fixed;
mutation tests select the named altered artifacts. The exact transformations
are in compile.cjs. All files remain pinned during mutation execution.

The upstream fixed constructor accepts verifier and expectedProgramKey from
the deployer. This harness supplies its actual compiled verifier and VK_HASH.
This does not prove arbitrary third-party deployments are configured correctly.
The SDK adapter constructs its own verifier and derives its key internally.

Only the public allowlist fixtures are covered. Proving from private witnesses,
deny/non-membership circuits, Guard acceptance, domain/root authority, executor
authorization, on-chain deployment state and execution occurrence are excluded.
ASCII decimal/hex strings preserve uint256/uint64/bytes values; raw proof bytes
are read from exact pinned binary files. No large-integer JSON coercion occurs.

Generated runtime strings/comments and collected third-party license notices
retain upstream trailing whitespace. Git's whitespace check is clean for the
authored files; these two generated/vendor files are preserved byte-for-byte.
