# RSI core v0 — implementation/review candidate

The research source is authoritative for the proposal's terminology, not proof
that every candidate invariant has been implemented. Normative words below
apply to this finite prototype profile. No universal verification claim follows.

## Core relation

`LocalValid(c1) and LocalValid(c2)` does not imply that the relation needed by a
security claim holds. A profile declares its required relation and admissible
evidence. The runner evaluates a control, a discriminating negative and a
mirror-positive under that profile. For pure substitution fixtures, relevant
local validity MUST be recomputed rather than declared by a label.

## Candidate rules and v0 coverage

**RSI-CORE-1 — No relation inheritance.** An adapter MUST NOT substitute local
signature validity for the required subject, scope, policy or evidence relation.
This is exercised only by the named v0 predicates, not all possible relations.

**RSI-CORE-2 — Explicit protected relation.** Each fixture MUST name its relation,
mutation class, profile and full inputs. Unsupported classes MUST fail as a
contract error, not obtain an optimistic result. Completeness is relative to
the declared profile, not a claim to have discovered all system assumptions.

**RSI-CORE-3 — Relation substitution resistance.** In the subject/context
fixtures, a separately valid signature under an unauthorized subject or scope
MUST be rejected. The mirror-positive MUST still accept.

**RSI-CORE-4 — Authentication before authoritative commitment.** A failed
transition authenticator MUST leave the captured authoritative state unchanged
and emit no successful-transition effect. Tentative state is not authoritative.
The source's broader 'no durable state' wording is narrowed explicitly here:
quarantined bytes, audit logs and rejection counters are not automatically
forbidden; they must be outside this profile's protected projection. v0 captures
`revision` and `head`, not every byte on the machine.

**RSI-CORE-5 — Path invariance.** Equivalent object, policy and initial state
MUST receive equivalent admission across live/snapshot/import/restore. v0 fixes
one authority context across all four paths. Other profiles may define
different authority semantics, but must not silently inherit this result.

**RSI-CORE-6 — Evidence-bounded status.** A valid signed operation alone MUST
NOT promote confirmation. A qualifying receipt must have a valid signature
under the declared evidence key, matching operation and scope, and an allowed
kind. Missing qualifying evidence yields UNVERIFIABLE with no confirmation.
This does not assert the operation failed in the outside world.

**RSI-CORE-7 — Epoch continuity.** Retained as a research candidate only. This
cut does NOT implement replay across sessions, authenticated root rotation,
revocation epochs, or corresponding conformance fixtures.

**RSI-CORE-8 — Atomic consumption.** In the declared schedule, at most one
successful commit may consume each captured revision. A stale competitor yields
CONFLICT without effects. A fresh read may consume the next position. v0 models
an interleaving and CAS/conditional update; it does not test real scheduler,
multi-process, crash or retry semantics.

## Claim scope

No result here proves semantic truth, universal authentication, a production
security guarantee, global novelty, or exhaustive coverage of RSI-CORE-1..8.
The concrete coverage matrix is `conformance.md`.
