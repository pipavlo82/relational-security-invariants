"""Offline, exact-byte source closure; no fixture-selected code or network."""
from pathlib import Path
from rsi.codec import decode, raw_digest
from runner.expectation_contract import safe_path
from runner.relation_profile_registry import UnavailableRelation

SOURCE_COMMIT = "15f7f59ac47b3358492bd5741143c418b5d657f5"
SOURCE_PIN_SHA256 = "2f752225295dc88805b6b618d84c3c511f4f447e6e4648037277523ae8fe17df"
SOURCE_PIN_PATH = "evidence/rvr/source-pin.v0.json"


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
