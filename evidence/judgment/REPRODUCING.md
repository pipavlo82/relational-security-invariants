# Reproduce the judgment record-binding lane

Python 3.12/3.13 stdlib suffices for this lane. From repository root:

```sh
python -m unittest tests.test_judgment -v
python tools/run_judgment.py --output artifacts/judgment.json
python tools/prove_judgment_can_fail.py --output artifacts/judgment-mutations.json
```

The architecture test also executes prior domains and requires their existing Node runtime. Install requirements-dev.txt for the full suite. No network is used during evaluation. All source bytes and SHA-256 pins are tracked; verify_source checks each before admission and execution. Changing a source or manifest requires an explicit new pin; latest is never substituted.

`reference/verifier.py` and `_bip340_nostr.py` are byte-identical upstream artifacts. The subprocess calls verify_fixture, discards human-readable detail only, and preserves each source pass/code, overall status, failure and envelope hash. Source signature validity is reported separately. The wrapper adds explicit unsupported capabilities, never production authority.

The SDK/interface/older draft files are evidence, not executed crypto. Source test annotations are not passed to either evaluator. See research/judgment-execution-mapping-v0.md for input projection, missing source checks and independence limitations. A reported executed label or declared anchor is not execution/consensus evidence.
