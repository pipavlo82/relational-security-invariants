# Crystal Receipt H2 reproducer

Scope: the existing flat printable-ASCII string-map semantic-snapshot subset
of counterfactual-audit-boundary-v0. This is a third, definition-derived
implementation path, not an author-independent or procedurally blind result.
Read DERIVATION.md for the exact pinned definition and derivation protocol.

## Standalone, offline execution

Node 22.15.0 (the existing RSI CI runtime) or compatible Node is sufficient.
No npm packages, Python, RSI modules, frozen expectation rows, TypeScript
helpers, network calls, or home-directory files are used by this command.
From the checkout root on a POSIX shell:

```sh
node reproducers/crystal-receipt-cleanroom/reproduce.mjs < reproducers/crystal-receipt-cleanroom/inputs/CR-H2-G1.json
```

On PowerShell:

```powershell
Get-Content -Raw reproducers/crystal-receipt-cleanroom/inputs/CR-H2-G1.json | node reproducers/crystal-receipt-cleanroom/reproduce.mjs
```

Repeat for G2, G3, G4. The process reads only stdin and the definition file,
verifies the definition SHA-256, and returns two canonical strings and their
equality. An isolated reproduction needs only reproduce.mjs, input bytes,
and SPEC.md; pass `--definition /path/to/SPEC.md` when outside this checkout.
It rejects malformed/duplicate-key JSON and unsupported transport without
coercion. The output JSON serializer is not the semantic canonicalizer.

## Full comparison and selected common-mode experiments

With the existing RSI development dependencies installed:

```sh
python -m unittest tests.test_crystal_cleanroom -v
python tools/check_crystal_cleanroom.py --output artifacts/crystal-cleanroom.json
```

The comparison harness is outside this directory. It computes all C results
in isolated processes first, then executes the pinned A implementation,
separately implemented B predictor, and atomic admission of D. Golden input
bytes originate from the two pinned source vectors. Their manually derived
answers follow the SPEC rules and the derivation note; they are not copied
from the RSI expectation artifact. Each vector maps to an identical existing
admitted case. No new Crystal fixture/profile/expectation registration exists.

H2-M1 injects external manifest metadata into both A/B semantic projections;
H2-M2 replaces the candidate semantic map with the baseline in both doubles.
The original C input remains unchanged. These local projection doubles do
not modify production code or any external repository. COMMON_MODE_CAUGHT
is a research classification, not an RSI mutation result.

Frozen expectations detect divergence from previously admitted semantics; they do not by themselves prove that the original expectation was independently derived.

## Residual limitations

JavaScript and TypeScript share the Node/V8 runtime. The new parser and token
renderer share no semantic helpers or rsi.codec dependency with the other
paths, but the comparison harness and A/B admission still use RSI transport.
All legs share the same pinned definition, source input origin, and human
interpretation risk. The four vectors and selected projection experiments
are not exhaustive. Author independence is UNKNOWN. No provenance-authority,
Lane K, broad ReceiptOS, non-ASCII, nested-object, numeric, descriptor, or
full JavaScript input-domain claim is made.

This compact bundle is technically reproducible outside RSI's private
runtime environment once its files are available. H2 does not itself grant
repository access, publish the bundle, or constitute an external clean-room
reproduction by another author.
