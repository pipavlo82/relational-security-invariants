# Crystal H2 three-leg comparison

All C computations complete before A/B execution and D admission. D is the existing atomically admitted frozen row for exactly the same input. Equality compares both complete canonical strings and the semantic-identity Boolean, plus the manually derived H2 golden.

| Vector | Actual A | Predictor B | Third leg C | Admitted D | All equal | Semantic note |
|---|---|---|---|---|---|---|
| CR-H2-G1 | preserved | preserved | preserved | preserved | true | Identical retained pairs. |
| CR-H2-G2 | changed | changed | changed | changed | true | One retained semantic value changes. |
| CR-H2-G3 | preserved | preserved | preserved | preserved | true | Only external audit metadata changes. |
| CR-H2-G4 | preserved | preserved | preserved | preserved | true | Only external audit metadata is removed. |

These are semantic relation results; a source-backed substitution case still has conformance PASS. H2 statuses do not change RSI taxonomy. Full comparison values are in the H2 JSON report.

| Vector | Exact admitted row | Input SHA-256 |
|---|---|---|
| CR-H2-G1 | `CR-RSI-001/control` | `0f88c70b0c915c7e056d2421c04b3011be15de31a6a35d5d6669ec9dae7abb00` |
| CR-H2-G2 | `CR-RSI-001/relation_substitution` | `3efc9a11e5402d29765773c7c0d171807bbd564705a6276215bf3ecead1252f4` |
| CR-H2-G3 | `CR-RSI-002/audit_timestamp_changed` | `722f0d82d914e731d5b4132ff68105f1c01155d1f2fbafa7dab4477818863fe4` |
| CR-H2-G4 | `CR-RSI-002/audit_timestamp_removed` | `785ec77ed32aae1add1264f2e850ca794f2b35c0379b82015b1b4cec4ba09cef` |

Frozen expectations detect divergence from previously admitted semantics; they do not by themselves prove that the original expectation was independently derived.
