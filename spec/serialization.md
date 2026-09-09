# Serialization and identity — rsi-json-ascii.v0

This prototype defines a deliberately restricted, separately named transport.
It is NOT RFC 8785 JCS and MUST NOT alias `encode-json-utf8-lf.v0`, an unversioned
family serializer, or an existing PRF binding.

Accepted values: null, booleans, integers in [-9007199254740991,
9007199254740991], ASCII strings, arrays and objects with unique ASCII keys.
Floats, non-finite tokens, non-ASCII, surrogate strings, duplicate keys and
non-string keys are outside the domain. Keys sort lexicographically; ASCII
code-point and UTF-16 order coincide. Strings use Python JSON ensure_ascii
escaping; separators are comma and colon with no spaces. Emit UTF-8 followed
by exactly one LF. Stored artifacts MUST equal the re-encoding byte-for-byte.
No BOM, CRLF, extra LF or whitespace normalization is accepted.

Digests: lowercase hexadecimal SHA-256 of exact file bytes for raw pins;
SHA-256 of this encoding for structured objects. Manifest/schema/oracle pins
are checked before adapter execution. Runtime source hashes identify actual
read source bytes; they do not attest author identity or remote deployment.

Signed payloads are different: the proof carries `payload_hex`, Ed25519
`public_key_hex` and `signature_hex`. The signature covers the exact decoded
payload bytes. Non-canonical JSON formatting is permitted inside a signed
payload for mirror-positive testing; duplicate keys, floats and out-of-domain
values remain forbidden. Parsing cannot stand in for signature verification.

`rsi-run.v0` and `rsi-mutation-gate.v0` have an `evidence` block plus
`evidence_digest = SHA256(encode(evidence))`. Output path, temporary directory,
wall-clock, console text and runtime duration are not part of that block. Each
state/effect/decision is retained directly, never derived from a missing count.
