# ERC-8299 record-binding ownership

| Role | Owner / evidence | Bound responsibility | Not established here |
|---|---|---|---|
| Declaration | ERC draft PR #1810, L4 + reference README | Judgment/proposal/execution-record joins and separate commitment/outcome | ERC-wide implementation conformance |
| Judgment producer | Invinoveritas published NIP01 event | Real signature over exact event content including artifact_hash | Judgment soundness or permission to act |
| Actor / terminal producer | Supplied chain records | actor key, action_ref, executed_envelope_hash | Real execution occurrence / truthful terminal reporting |
| Identity-policy owner | Supplied trust_policy | Listed signing keys distinct from actor | Organizational/author independence |
| Anchor source | Supplied accepted_anchor_point | Conditional ordering calculation | Bitcoin/OTS/consensus authority |
| Reference verifier | Pinned conformance/verifier.py + _bip340_nostr.py | Recompute signature and five source checks | Raw-to-canonical transform and conditional approval policy |
| Trustless consumer | agent-sdk L4 hash/client paths | Recompute named preimage and dispatch verifier call | Full execution or production signature verification from its mock |
| RSI | Additive profile, separate predictor, generic comparator | Finite record-substitution/promotion conformance tests | Universal correctness or every judgment/execution relation |

The strongest promotion risk is a consumer treating source overall_pass as approval/execution. The source control is signed `reject`; the RSI profile keeps approval and occurrence unsupported. Source anchor-existence checks likewise remain conditional on supplied trust, not a consensus verification claim.
