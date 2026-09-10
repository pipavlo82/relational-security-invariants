"""Offline, exact-byte source closure; no fixture-selected code or network."""
from pathlib import Path
from rsi.codec import decode, raw_digest
from runner.expectation_contract import safe_path
from runner.relation_profile_registry import UnavailableRelation

SOURCE_COMMIT = "01283ca57305f915afb560d23359a27fd748eb5a"
SOURCE_PIN_SHA256 = "83a5414eeff501015a682967f4e6ec9704cf1c609d74426eef3777f38a319e5b"
SOURCE_PIN_PATH = "evidence/consult-escrow/source-pin.v0.json"


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
