# Reproducing the pinned local execution lane

Run from the RSI root. Node 22.15.0, solc 0.8.25 and exact lockfile dependencies
were used. Runtime evaluation is offline; it never installs packages or imports
fixture-selected code. Build dependencies are an explicit review/build step only.

1. Copy this directory's package.json/package-lock.json into
   artifacts/ce-phase3b/runtime/.
2. npm ci --prefix artifacts/ce-phase3b/runtime --cache artifacts/ce-phase3b/npm-cache --ignore-scripts --no-audit --no-fund
3. node evidence/consult-escrow/compile.cjs
4. node evidence/consult-escrow/build.cjs
5. Compare output SHA-256 with source-pin.v0.json. Do not silently repin.

The source files are exact upstream bytes. Compile settings and compiler version
are recorded in each bytecode artifact. canonical.json is unchanged source;
job/signature/replay.json are explicit negative mutation implementations.
The bundle includes the selected dependency closure and license notices. Optional
supports-color is replaced with false for deterministic diagnostics only. No EVM
opcode, signature check or contract condition is replaced in the canonical lane.
The Node runtime is exercised without node_modules in temporary test copies.

Python predictor implements the mathematical recovery independently. Frozen
fixture signatures use the public upstream 0xA11CE test key, ethers personal_sign
over keccak256(bytes32 jobA || bytes32 sameResult), and source Keccak identifiers.
No secret key, production wallet or on-chain transaction is used.
