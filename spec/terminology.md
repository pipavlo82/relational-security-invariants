# Terminology

**RSI:** Relational Security Invariants, the candidate specification methodology.
**RBCF:** Relation-Binding Conformance Fixtures, its concrete test packaging.
The wire schema keeps the research source's `relation-binding-fixture.v0` name.

**Component validity:** here, successful Ed25519 verification of supplied
payload bytes under the supplied public key, independent of whether that key
is authorized. This is not source identity or authorization.

**Protected relation:** the profile's explicit subject/scope/policy/evidence or
state-transition predicate. Its validity is not inherited from component validity.

**Claim validity:** the stronger claim the consumer wants to make, justified
only within the modeled relation and trust assumptions.

**Oracle:** executable reference predicates in `rsi/oracle.py` plus detached,
byte-pinned expected results. It is trusted, reviewed finite code, not inferred
from target output and not an omniscient semantic truth source.

**ACCEPT / REJECT / CONFLICT / UNVERIFIABLE:** native operation outcomes.
UNVERIFIABLE means the required evidence is unavailable or ineligible here.

**PASS / FAIL / RUNNER_ERROR:** benchmark evaluation outcomes. Rejection of a
relation-broken input can earn PASS. Failure to execute a valid comparison cannot.

**Control / mutation / mirror_positive:** corpus roles never supplied to native
targets. Mirror-positive changes signed representation without changing the
protected outcome; a blanket rejection policy fails this control.

**Source mutant:** an isolated code edit that intentionally removes one guard.
It is different from the adversarial fixture's input mutation.
