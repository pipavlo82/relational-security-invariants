# H2 definition-first derivation record

This note precedes the H2 executable implementation. It is not a claim of
procedural blindness: the implementer had already inspected the TypeScript
path and Python predictor during H1. Author independence is UNKNOWN.

## Definition authority

- Repository: pipavlo82/crystal-receipt
- Commit: 45b46bf7df3a60b32583291f577a36bf19d22f00
- Path: conformance/counterfactual-audit-boundary-v0/SPEC.md
- Local materialization: evidence/crystal-receipt/SPEC.md
- SHA-256: 9c17bd826c4a789464dab80c78a136153f3d9ce2f253198d0cf386bdef3a6d0b
- Evidence class: frozen semantic contract/specification.
- Sections: Domains / Semantic input domain; Audit metadata domain; Reserved
  field; Frozen expected-outcome vocabulary.

The contract is sufficient for the flat printable-ASCII string-map subset.
It explicitly orders own keys, preserves accepted values, rejects reserved
audit metadata inside the semantic artifact, and excludes external audit
metadata from semantic identity. Its reference to existing helpers does not
replace these explicit rules with implementation behavior.

## Definition-derived transformation

For each endpoint, require exactly a semantic_artifact and external manifest.
Require a nonempty semantic map with unique printable-ASCII string keys and
string values. Reject audit_timestamp inside that map. The external manifest
is empty or contains one printable-ASCII audit_timestamp string.

Represent each semantic map as the lexicographically ordered sequence of
(key, value) pairs. Escape only double quote and backslash when rendering
these printable strings in compact JSON. The ordered sequence is the
protected snapshot. Two endpoints preserve identity exactly when their
ordered rendered sequences are equal. Never project the external manifest
into that sequence. No hashing of source implementation output is needed.

The standalone transport will parse only objects and printable strings,
reject duplicate keys and unsupported values, and construct its own tokens.
It will not use rsi.codec or a production semantic parser/evaluator. Ordinary
JSON output serialization is transport, not the snapshot derivation.

## Four manual deductions, before computing A/B/D

The pinned source vectors supply input bytes, not the oracle. H2 uses their
same four already admitted cases so the frozen row comparison is exact.

1. G1: identical maps produce identical ordered pairs.
2. G2: replacing expected_conformance_observation changes one retained value;
   therefore the ordered snapshot differs.
3. G3: changing external audit_timestamp changes no semantic pair.
4. G4: removing external audit_timestamp changes no semantic pair.

Golden canonical strings are manually transcribed from the three input
pairs in alphabetical key order. Golden booleans follow the four deductions,
not frozen expected rows or executable source output.

## Limits and experiments

No nested values, Unicode, numbers, object descriptors, Lane K, provenance
authority, or broader ReceiptOS behavior is covered. A JavaScript/Node
implementation uses the already required CI runtime; adding Rust solely
for language optics would add an unconfigured CI toolchain. Language
independence from the TypeScript actual is therefore not established.

H2-M1 deliberately binds external metadata in two local test doubles;
H2-M2 deliberately discards a semantic value change in both. The third
derivation is held fixed. These demonstrate selected common-mode detection,
not unrestricted oracle independence or ordinary RSI mutation kills.

Frozen expectations detect divergence from previously admitted semantics;
they do not by themselves prove that the original expectation was
independently derived.
