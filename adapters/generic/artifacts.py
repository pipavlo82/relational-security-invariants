"""Real Ed25519/AES-GCM with PUBLIC TEST KEYS, never production secrets."""
import hashlib
import json

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def key(owner):
    # Public deterministic test seeds. These confer no real-world authority.
    return Ed25519PrivateKey.from_private_bytes(hashlib.sha256(("RSI TEST " + owner).encode()).digest())


def signed(owner, body):
    return {"signer": owner, "body": body, "signature": key(owner).sign(canonical(body)).hex()}


def signature_valid(artifact):
    try:
        key(artifact["signer"]).public_key().verify(bytes.fromhex(artifact["signature"]), canonical(artifact["body"]))
        return True
    except (InvalidSignature, ValueError):
        return False


TEST_AES_KEY = bytes(range(32))
TEST_NONCE = bytes(range(12))
TEST_AAD = b"rsi/bootstrap/v0"


def ciphertext():
    # A single fixed test vector; never allocate production nonces this way.
    return AESGCM(TEST_AES_KEY).encrypt(TEST_NONCE, b"bootstrap", TEST_AAD).hex()


def authenticates(encoded):
    try:
        AESGCM(TEST_AES_KEY).decrypt(TEST_NONCE, bytes.fromhex(encoded), TEST_AAD)
        return True
    except (InvalidTag, ValueError):
        return False
