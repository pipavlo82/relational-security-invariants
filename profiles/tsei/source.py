"""Exact offline evidence closure. A source pin is not provenance authority."""
from rsi.codec import decode, raw_digest
from runner.expectation_contract import safe_path
from runner.relation_profile_registry import UnavailableRelation

SOURCE_PIN_PATH = "evidence/tsei/source-pin.v0.json"
SOURCE_PIN_SHA256 = "e35866da9b070603016233fda75d2a36efcf23f8782510b05ffb97d0a3cd345a"
MECHANISM = "d641510dff95541d8cd73d5bc2bf593fe024f79c"
ADOPTION = "45b46bf7df3a60b32583291f577a36bf19d22f00"
INTRODUCTION = "1dfc527d8f9b3561d32ca510f8fefd8d290391f6"
REGISTRY_MAIN = "15f7f59ac47b3358492bd5741143c418b5d657f5"
PRE_ADOPTION = "5c3f285495b41c357fab045b04b44d5714ced9a9"
PRE_RECORD = "79cb2da9c7943bd45fb64f099c3a18eab1922299"


class SourceUnavailable(UnavailableRelation):
    pass


def read_sources(root):
    try:
        raw = safe_path(root, SOURCE_PIN_PATH).read_bytes()
        if raw_digest(raw) != SOURCE_PIN_SHA256:
            raise SourceUnavailable("SOURCE_PIN_DIGEST")
        pin = decode(raw, canonical=True)
        if pin["repositories"] != {"pipavlo82/crystal-receipt": ADOPTION, "trustless-ai/recompute-kit": REGISTRY_MAIN}:
            raise SourceUnavailable("SOURCE_COMMIT")
        for key, wanted in (("mechanism", MECHANISM), ("producer_adoption", ADOPTION), ("record_introduction", INTRODUCTION)):
            if pin["chronology"][key]["commit"] != wanted:
                raise SourceUnavailable("SOURCE_CHRONOLOGY")
        blobs = {}
        for f in pin["files"]:
            data = safe_path(root, f["local_path"]).read_bytes()
            if raw_digest(data) != f["sha256"]:
                raise SourceUnavailable("SOURCE_ARTIFACT_DIGEST")
            blobs[f["local_path"].split("/")[-1]] = data
        return pin, blobs
    except (OSError, ValueError, KeyError) as exc:
        raise SourceUnavailable("SOURCE_UNAVAILABLE") from exc


def verify_source(root):
    return read_sources(root)[0]


def verify_snapshots(value):
    # Exact evidenced snapshots, not SHA ordering or an implicit latest revision.
    if value["registry_commit"] not in (MECHANISM, PRE_RECORD, INTRODUCTION, REGISTRY_MAIN):
        raise SourceUnavailable("REGISTRY_SNAPSHOT_UNSUPPORTED")
    if value["producer_commit"] not in (PRE_ADOPTION, ADOPTION):
        raise SourceUnavailable("PRODUCER_SNAPSHOT_UNSUPPORTED")
    if value["artifact_commit"] not in (PRE_ADOPTION, ADOPTION):
        raise SourceUnavailable("ARTIFACT_SNAPSHOT_UNSUPPORTED")
