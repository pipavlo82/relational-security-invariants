# v0 threat model

## Trust boundary

The corpus, reference oracle, fixture loader and implementation harness are
trusted code inputs, reviewed and pinned to exact bytes by the run report.
The synthetic native target is the implementation under test; mutations make
specific target code wrong. The target does not receive expected answers.
The profile/policy is trusted input. Its origin is not discovered or attested
by this prototype. Signature verification alone does not authenticate a
policy's choice of signer. Both targets and the oracle share libraries, so
agreement is not a claim of independently implemented cryptography.

## Captured state and effects

The projection is `{revision, head}` plus normalized effect names and allocated
positions. The messaging target uses memory; the receipt target uses in-memory
SQLite. There is no claim that all external side effects are observed. Paths
in the ingestion fixture start from the same state independently; the fixture
is not asking a replayed object to be admitted four times to one live store.

The schedule explicitly creates reads before commits. It demonstrates a stale
revision race deterministically but is not an OS-level concurrency stress test.
Receipt signatures are real test cryptography; claims about actual delivery or
settlement remain outside the model.

## Unsupported / incomplete

No production integrations, deployed source audit, adversarial adapter sandbox,
cryptographic security proof, revocation, replay-across-epochs, recovery
completeness, multi-device protocol, AES-GCM nonce allocation or crash recovery.
Malformed benchmark input is RUNNER_ERROR, not REJECT from a target that never
executed. Missing evidence in a valid supported request is UNVERIFIABLE.
