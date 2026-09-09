# Prior-art note — source-derived, preliminary

This is a scoped summary of the user's supplied novelty-research v0, not a new
exhaustive literature review. The full source and third-party audit are not
redistributed. Source SHA-256:
`80ed386c04072f94713a275191ae45f583a860f92da088854371c2105a2830cd`.

The source explicitly says identity misbinding, pre-key authentication,
nonce uniqueness, replay/rollback, trust-root continuity, fail-safe defaults,
complete mediation, transactional authentication and context binding have
substantial prior art. This prototype does not claim to invent any of them.

The candidate synthesis is an implementation-facing family of conformance
fixtures across subject, scope, evidence, policy and state relations. Its
novelty remains unverified. A useful experiment needs at least two or three
unrelated real systems using the same core semantics. Synthetic adapters alone
do not discharge that experiment.

## Primary and adjacent references identified in the supplied research

- Signal X3DH: https://signal.org/docs/specifications/x3dh/
- Signal Double Ratchet: https://signal.org/docs/specifications/doubleratchet/
- Signal Sesame: https://signal.org/docs/specifications/sesame/
- ProVerif / correspondence assertions:
  https://publications.bensmyth.com/files/ProVerif-manual-version-2.00.pdf
- Identity misbinding: https://doi.org/10.1145/3321705.3329813
- RFC 8844: https://www.rfc-editor.org/rfc/rfc8844.html
- RFC 5084: https://www.rfc-editor.org/rfc/rfc5084.html
- Saltzer and Schroeder: https://doi.org/10.1109/PROC.1975.9939
- TUF: https://theupdateframework.github.io/specification/draft/
- in-toto: https://github.com/in-toto/docs/blob/master/in-toto-spec.md

The source specifically calls for further work on formal protocol verification,
cryptographic composition, authorization, state continuity, attestations,
parser/ingestion differentials, recovery and agent-action receipts. Those gaps
remain open here. 'Not found in one review' is not 'does not exist'.

## Implementation documentation consulted separately

- Ed25519 API: https://cryptography.io/en/46.0.4/hazmat/primitives/asymmetric/ed25519/
- Draft 2020-12 validator: https://python-jsonschema.readthedocs.io/en/stable/validate/

These are implementation references, not prior-art evidence for novelty.
