"""Explicit RSI ASCII/integer JSON subset. NOT JCS or encode-json-utf8-lf.v0."""
import hashlib
import json
from pathlib import Path

SERIALIZER = "rsi-json-ascii.v0"
LIMIT = 2**53 - 1

class ContractError(ValueError):
    """Invalid or unsupported benchmark input; never a security verdict."""

def domain(value):
    if value is None or type(value) is bool:
        return
    if type(value) is int and -LIMIT <= value <= LIMIT:
        return
    if type(value) is str and value.isascii():
        return
    if type(value) is list:
        for item in value:
            domain(item)
        return
    if type(value) is dict:
        for k, v in value.items():
            if type(k) is not str or not k.isascii():
                raise ContractError("object keys must be ASCII strings")
            domain(v)
        return
    raise ContractError("outside rsi-json-ascii.v0 domain")

def encode(value):
    domain(value)
    return (json.dumps(value, sort_keys=True, ensure_ascii=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")

def digest(value):
    return hashlib.sha256(encode(value)).hexdigest()

def raw_digest(raw):
    return hashlib.sha256(raw).hexdigest()

def _pairs(items):
    obj = {}
    for k, v in items:
        if k in obj:
            raise ContractError("duplicate JSON key: " + k)
        obj[k] = v
    return obj

def _bad_number(value):
    raise ContractError("floating/non-finite JSON number forbidden: " + value)

def decode(raw, canonical=False):
    try:
        text = raw.decode("utf-8")
        result = json.loads(text, object_pairs_hook=_pairs,
                            parse_float=_bad_number, parse_constant=_bad_number)
        domain(result)
    except (UnicodeError, ValueError) as exc:
        raise ContractError(str(exc)) from exc
    if canonical and encode(result) != raw:
        raise ContractError("non-canonical stored bytes")
    return result

def load(path, canonical=True):
    return decode(Path(path).read_bytes(), canonical=canonical)
