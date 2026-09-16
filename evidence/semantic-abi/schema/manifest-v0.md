# Semantic manifest — v0 (draft, not yet frozen)

A manifest declares, per endpoint/component, what each evidence claim is allowed to mean. The claim,
authority, scope, and temporal boundary form one typed unit:

```text
EvidenceClaim<claim_type, authority_class, scope, issued_at | verification_time>
```

`claim_type` names the proposition. `authority_class` names how that proposition was established. They are
different namespaces: `SIGNED_VERDICT_AUTHENTIC` is a claim, while `CRYPTOGRAPHIC_VERIFICATION` is an
authority class. Neither may be substituted for the other.

## Declaration fields

| field | meaning |
|---|---|
| `consumes` | an array of typed claim-level evidence requirements |
| `establishes` | a non-empty array of typed claim-level evidence created by this component |
| `does_not_establish` | explicit negative claim boundaries, each naming claim, authority, and scope |
| `claim_type` | the proposition established or required |
| `authority_class` | how that specific claim is established |
| `scope` | the exact boundary over which that claim holds |
| `issued_at` | when the underlying claim was made or originated |
| `verification_time` | when a separate check/recomputation of a claim occurred |

Every consumed or established claim contains exactly one temporal field. A component never uses both for
the same claim. An issuing component uses `issued_at`; a component whose claim is the result of checking
something else uses `verification_time`. There is no generic temporal alias.

Negative boundaries are also claim-level. For example, "this authentic signed verdict does not establish
that the judgment is correct" names both the unsupported correctness claim and the authority that would be
needed. A bare claim name or authority-class string is not a valid negative boundary.

The minimal v0 authority-class enum is:

```text
INDEPENDENT_JUDGMENT
CRYPTOGRAPHIC_VERIFICATION
EX_POST_VALIDATION
INFRASTRUCTURE_ATTESTATION
ONCHAIN_COMMITMENT
INDEPENDENT_RECOMPUTATION
KEY_BINDING_AUTHORITY
SEMANTIC_VERIFICATION
```

Claim names such as `STATE_INCLUSION`, `NOT_BACKDATED`, or `ACTION_SETTLED` do not become authority
classes merely because an earlier draft used them in a negative boundary.

The runner keeps three values explicit:

- `expected_pair`: `PRESERVED | VIOLATED | UNVERIFIABLE`, pinned by the vector oracle;
- `observed_pair`: `PRESERVED | VIOLATED | UNVERIFIABLE`, returned by the adapter;
- `backend_conformance`: `PASS | FAIL | CANNOT_CHECK`, derived from the first two.

## Worked manifest — InvinoVeritas

```json
{
  "component": "invinoveritas",
  "author": "@babyblueviper1",
  "declarations": [
    {
      "endpoint": "/review?sign=true",
      "consumes": [],
      "establishes": [
        {
          "claim_type": "SIGNED_VERDICT",
          "authority_class": "INDEPENDENT_JUDGMENT",
          "scope": "verdict:event-id",
          "issued_at": "proof.created_at"
        }
      ],
      "does_not_establish": [
        {
          "claim_type": "JUDGMENT_CORRECT",
          "authority_class": "SEMANTIC_VERIFICATION",
          "scope": "verdict:event-id"
        }
      ]
    },
    {
      "endpoint": "/verify-proof",
      "consumes": [
        {
          "claim_type": "SIGNED_VERDICT",
          "authority_class": "INDEPENDENT_JUDGMENT",
          "scope": "verdict:event-id",
          "issued_at": "proof.created_at"
        }
      ],
      "establishes": [
        {
          "claim_type": "SIGNED_VERDICT_AUTHENTIC",
          "authority_class": "CRYPTOGRAPHIC_VERIFICATION",
          "scope": "verdict:event-id",
          "verification_time": "verification.completed_at"
        }
      ],
      "does_not_establish": [
        {
          "claim_type": "JUDGMENT_CORRECT",
          "authority_class": "SEMANTIC_VERIFICATION",
          "scope": "verdict:event-id",
          "reason": "valid means authentic, not correct"
        }
      ]
    }
  ]
}
```

For the adversarial epistemic-basis pair, both historical and repaired vectors have
`expected_pair = VIOLATED`. The historical pre-v18 commitment observed `PRESERVED`, so its backend
conformance is `FAIL`. The v18 commitment observes `VIOLATED`, so its backend conformance is `PASS`.
The repair changed whether the backend detects the distinction; it did not turn the adversarial pair into a
preserved pair.

## Worked manifest — Vértice gateway

```json
{
  "component": "vertice-gateway",
  "author": "@TMerlini",
  "declarations": [
    {
      "endpoint": "/verify",
      "consumes": [
        {
          "claim_type": "ACTION_RECEIPT",
          "authority_class": "INFRASTRUCTURE_ATTESTATION",
          "scope": "action:receipt-id",
          "issued_at": "receipt.issued_at"
        }
      ],
      "establishes": [
        {
          "claim_type": "DETERMINISTIC_ACTION_RESULT",
          "authority_class": "INDEPENDENT_RECOMPUTATION",
          "scope": "action:receipt-id/output",
          "verification_time": "verification.completed_at"
        }
      ],
      "does_not_establish": [
        {
          "claim_type": "NONDETERMINISTIC_JUDGMENT_CORRECT",
          "authority_class": "SEMANTIC_VERIFICATION",
          "scope": "action:receipt-id/output",
          "reason": "the judgment is outside the recomputable claim"
        },
        {
          "claim_type": "ACTION_SETTLED",
          "authority_class": "EX_POST_VALIDATION",
          "scope": "action:receipt-id"
        }
      ]
    }
  ]
}
```

Independent recomputation does not globally satisfy semantic verification. It can support that authority
only for the exact recomputable claim, compatible scope, and matching temporal boundary that it actually
re-derived. A different claim, wider scope, or different time remains a `TYPE_ERROR`.

## Open items before freezing v0

- [x] Split temporal identity into `issued_at` and `verification_time`, never both on one claim.
- [x] Make `consumes`, `establishes`, and `does_not_establish` claim-level structures.
- [x] Remove the global `INDEPENDENT_RECOMPUTATION -> SEMANTIC_VERIFICATION` coercion.
- [x] Close the minimal authority-class enum without retaining claim names as aliases.
