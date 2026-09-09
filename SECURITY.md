# Security and disclosure scope

This repository contains synthetic public test data and deterministic test
signing keys. These keys are deliberately reproducible from public labels and
MUST NOT be used for real accounts, messages, assets, or credentials.

Do not publish source-project vulnerabilities or customer artifacts here.
The source audit is intentionally excluded. Findings concerning third-party
systems must follow an agreed responsible-disclosure process; neither the end
of a contest nor a private benchmark experiment establishes permission to
publish an unfixed vulnerability.

The adapters execute locally and are trusted code. The runner is not a sandbox
for arbitrary hostile adapters. It does not attest real network delivery,
production identities, disk persistence or remote execution. Synthetic
acknowledgements establish only the exact local relation checked by this model.
