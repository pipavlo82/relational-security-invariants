"""Offline, exact-byte source closure; no fixture-selected code or network."""
from pathlib import Path
from rsi.codec import decode, raw_digest
from runner.expectation_contract import safe_path
from runner.relation_profile_registry import UnavailableRelation

SOURCE_COMMIT = "a344ef80f7c52c03b9183814d1874b8054639c3e"
SOURCE_PIN_SHA256 = "02df3014d53b012a3358c5d22285382df66cb1fd3a9576d106e5297bd7812dfd"
SOURCE_PIN_PATH = "evidence/tas/source-pin.v0.json"


class SourceUnavailable(UnavailableRelation):
    pass


def read_sources(root):
    try:
        raw = safe_path(root, SOURCE_PIN_PATH).read_bytes()
        if raw_digest(raw) != SOURCE_PIN_SHA256:
            raise SourceUnavailable("SOURCE_PIN_DIGEST")
        pin = decode(raw, canonical=True)
        if pin["commit"] != SOURCE_COMMIT:
            raise SourceUnavailable("SOURCE_COMMIT")
        blobs = {}
        for entry in pin["files"]:
            payload = safe_path(root, entry["local_path"]).read_bytes()
            if raw_digest(payload) != entry["sha256"]:
                raise SourceUnavailable("SOURCE_ARTIFACT_DIGEST: " + entry["path"])
            blobs[entry["local_path"]] = payload
        return pin, blobs
    except (OSError, ValueError) as exc:
        raise SourceUnavailable("SOURCE_UNAVAILABLE") from exc


def verify_source(root):
    return read_sources(root)[0]
