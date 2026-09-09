# Terminology - v0

| Term | Meaning |
|---|---|
| Component | Artifact or input whose local validity is explicitly scoped. |
| Local validity | Named checks that remain true in both members of the pair; never an assertion of overall security. |
| Protected relation | One declared relationship required for a positive claim. |
| Relation oracle | Independent precondition computation from concrete inputs, not an adapter's acceptance result. |
| Claim validity | Whether the positive protected claim is warranted; this profile computes the conjunction of local validity and its relation. |
| Conformance | Whether observed decisions and effects satisfy fixture requirements. A rejected negative case earns PASS. |
| Control | Valid positive case that must execute successfully. |
| Mutation | Concrete replacement inputs with the same declared local validity and one broken protected relation. |
| Changed fields | Exact recursive leaf differences in component objects; arrays are atomic fields. This is not a count of relations. |
| Promotion | Admission or increase in authority, durable state, policy, provenance or evidence-implying status. |
| Policy version | `rsi-reference-policy.v0`, the explicit six-profile policy used by both pair members. |
| Evaluator | Name/version of the system adapter. Only `reference` / `0` is supported here. |
| Durable-model state | An in-memory representation of what a real system would persist. No physical persistence is tested. |
| Evidence | In the status model, a successful recipient acknowledgment or durable-publication observation bound to exact subject, scope and operation. |
| Atomic consumption | At most one successful consumer of the same logical revision. The first legitimate consumption is permitted. |
| Unsupported | Structurally valid case naming an evaluator the runner cannot execute. It is not a pass. |

A parseable ciphertext is locally structurally valid even when AEAD authentication fails. RSI-003 explicitly preserves structure, not authentication. An ingestion object can be structurally and cryptographically valid while its signed guest role fails the member-only admission relation.
