# Offline proof lane reproduction

All conformance execution uses the checked-in `proof-runtime.mjs`; no runtime install, RPC, private key or credential lookup occurs.

To reproduce the bundle in an explicitly network-enabled build environment:

1. Create ignored `artifacts/vl-phase3c/runtime` and copy this directory's `package-lock.json` there.
2. Create its `package.json` with the `dependencies` object from `package-lock.json` at `packages[""].dependencies`. This includes the build-only esbuild package; upstream `package.json` is separately preserved unchanged.
3. Run `npm ci --prefix artifacts/vl-phase3c/runtime --ignore-scripts --no-audit --no-fund` with an ignored workspace npm cache.
4. From the RSI root, run `node evidence/verify-layer/build.cjs`.
5. Compare the resulting bundle SHA-256 with `source-pin.v0.json`. A mismatch must not be silently repinned.

The explicit filesystem resolver keeps build paths deterministic and uses ESM dependency sources. All upstream core function bodies between `// Core:` and `const fmt` are retained literally in build-entry.mjs; tests enforce this. RPC replay and output projection are RSI harness additions. The credential read, network transport, and live demo are excluded. Known MPT verification rejection is narrowly caught; infrastructure errors are not.

This file documents the build only; it does not authorize expectation rows or source drift.
