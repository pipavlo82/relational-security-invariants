# Explicit implementation decisions / gaps relative to the source research

This file records choices introduced for the implementation. They are not
silently attributed to the source document and are not ratified group decisions.

1. **Private prototype, not a release.** Six requested families are implemented;
no audit details or identifying third-party payloads are copied into fixtures.
The full novelty research and original audit remain outside this repository.

2. **Keep the source terminology.** RSI/RBCF and the six RSI identifiers are
retained. `relation-binding-fixture.v0` remains the wire name. Research candidates
not implemented are explicitly marked pending rather than presented as coverage.

3. **Do not over-unify the mutation.** The source's central relation-substitution
thesis preserves local validity; its proposed auth-before-commit fixture uses
invalid ciphertext. This prototype uses an invalid Ed25519 signature as an
explicit `invalid_authentication` case, with local_validity=false. Atomic
consumption is labeled `concurrent_schedule`. Cross-ingress checks are labeled
`cross_path`. No claim that every test is a one-endpoint substitution remains.

4. **Bound state, not every disk byte.** CORE-4 protects authoritative state and
successful effects. Logging rejected input may be legitimate. The captured
projection is specified; no whole-machine rollback or crash test is claimed.

5. **Path equality needs equal prerequisites.** Each ingestion path is evaluated
from the same initial state and policy. This avoids interpreting legitimate
replay/dedup state changes as an ingestion-policy defect.

6. **Absent evidence is epistemic.** Lack of a receipt yields UNVERIFIABLE rather
than a factual assertion that an operation failed. A correctly fail-closed
UNVERIFIABLE can be a benchmark PASS.

7. **Two synthetic targets, not two external systems.** Real Ed25519 verification
and a SQLite state implementation make this more than a label checker, but do
not establish the source's proposed cross-domain experiment against unrelated
production systems. Both adapters are authored together and share infrastructure.

8. **Separate serializer identity.** Restrict to a documented ASCII/integer
subset and never alias existing JCS or LF serializers. This is a prototype
transport decision, not a migration of any old project bytes.

9. **No IP/novelty escalation.** No chosen open-source license, trademark claim,
ERC submission, public announcement, patentability or novelty proof. Those need
separate owner/reviewer decisions.
