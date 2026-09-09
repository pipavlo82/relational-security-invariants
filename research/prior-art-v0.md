# Prior art and research boundaries - v0

Derived from [the supplied research](source-research-v0.md), sections 3-4, 9, 13-14; see [source digests](source-provenance.json). The underlying audit and literature review are upstream reported, not independently reverified by this implementation. No new novelty search was performed.

The candidate contribution is the cross-domain relation-substitution conformance methodology. The individual mechanisms are established prior art. Promising is not novel; absence of an identified equivalent is not evidence of absence.

Legend:

- **Established** — substantial direct prior art.
- **Adjacent** — known ideas exist, but the exact fixture/generalization is less obvious.
- **Promising** — this research pass did not find an obvious standardized equivalent.
- **Unverified** — requires deeper dedicated literature/patent/standards search.

| Candidate | Prior art | Novelty assessment |
|---|---|---|
| Signer-to-subject binding | UKS/misbinding, formal authentication | Established |
| Signed pre-key / identity continuity | X3DH, Signal safety numbers | Established |
| Authentication-before-commit | Sesame transactional receive semantics | Established in messaging |
| Nonce uniqueness | AEAD standards | Established |
| Atomic ratchet consumption under concurrency | nonce rules + concurrent state management | Adjacent |
| Replay across epochs | protocol replay / anti-rollback | Established |
| Trust-root non-substitution | TUF continuity | Established |
| Policy-preserving fallback | fail-safe defaults | Established principle; fixture is adjacent |
| Context-complete authentication | AEAD AAD, transcript binding | Established |
| Evidence-based confirmation | attestations, event correspondence, receipts | **Promising as a generic status/evidence invariant** |
| Ingestion equivalence | complete mediation, parser/validation consistency | **Promising as an explicit cross-path fixture** |
| Recovery completeness under declared relation | backup/restore semantics | Adjacent / promising |
| Relation-substitution fixture family | misbinding + formal correspondence + conformance testing | **Promising synthesis** |
| Single protected-relation taxonomy spanning crypto/auth/provenance/policy/state | many adjacent literatures | **Promising synthesis; novelty unverified** |

Formal event correspondence, misbinding/unknown-key-share research, complete mediation, fail-safe defaults, capability security/confused deputy, TUF continuity and in-toto provenance are the closest conceptual ancestors. Source references and their original assessments are preserved in the supplied research copy.

Unverified: novelty of the synthesis, standardized equivalents for status/evidence and cross-ingestion fixtures, patent landscape, and utility across unrelated real implementations. Publication-grade work still requires the dedicated searches listed in source section 14. These six reference models do not complete that work.
