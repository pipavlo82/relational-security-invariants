# Generic reference adapters

`artifacts.py` uses Ed25519 for signer and context fixtures and AES-GCM for the messaging fixture, through the pinned cryptography package. Public deterministic test seeds and fixed cipher bytes are intentionally reproducible and have no production authority.

`models.py` provides signer/subject, artifact/context, status/evidence and ingestion-policy reference systems. Inputs are concrete fixture components; outputs are decisions/effects. These functions never receive expectations. No real transports, identity directory, provenance service or ingestion system is integrated.
