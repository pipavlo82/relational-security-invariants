"""Wire parser and real signature primitive, shared infrastructure, not independent code."""
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from rsi.codec import ContractError, decode

def unpack(envelope):
    raw = bytes.fromhex(envelope["payload_hex"])
    body = decode(raw)
    if type(body) is not dict:
        raise ContractError("payload must be an object")
    return raw, body

def valid_signature(envelope):
    raw, _ = unpack(envelope)
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(envelope["public_key_hex"])).verify(
            bytes.fromhex(envelope["signature_hex"]), raw)
        return True
    except InvalidSignature:
        return False
