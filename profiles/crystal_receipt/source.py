"""Offline source closure. Fixture data cannot select executable paths."""
from pathlib import Path
from rsi.codec import decode,raw_digest
from runner.expectation_contract import safe_path
from runner.relation_profile_registry import UnavailableRelation
SOURCE_COMMIT = "45b46bf7df3a60b32583291f577a36bf19d22f00"
SOURCE_PIN_SHA256 = "17f072840b3dd50f23fafaadafe6ee8321b771f6c211e8af5bc95b17ee0229fb"
SOURCE_PIN_PATH = "evidence/crystal-receipt/source-pin.v0.json"
class SourceUnavailable(UnavailableRelation):
    pass

def read_sources(root):
    try:
        raw=(Path(root)/SOURCE_PIN_PATH).read_bytes()
        if raw_digest(raw)!=SOURCE_PIN_SHA256:raise SourceUnavailable("SOURCE_PIN_DIGEST")
        pin=decode(raw,canonical=True)
        if pin["commit"]!=SOURCE_COMMIT:raise SourceUnavailable("SOURCE_COMMIT")
        blobs={}
        for entry in pin["files"]:
            payload=safe_path(root,entry["local_path"]).read_bytes()
            if raw_digest(payload)!=entry["sha256"]:
                raise SourceUnavailable("SOURCE_ARTIFACT_DIGEST: "+entry["path"])
            blobs[entry["local_path"]]=payload
        return pin,blobs
    except (OSError,ValueError) as exc:
        raise SourceUnavailable("SOURCE_UNAVAILABLE") from exc

def verify_source(root):
    return read_sources(root)[0]
