"""Observed byte production plus explicit pinned registry/producer relations."""
from contextlib import ExitStack
from functools import lru_cache
from pathlib import Path
import json
import shutil
import subprocess
import tempfile
from rsi.codec import encode, raw_digest
from profiles.tsei.source import read_sources, verify_snapshots, SourceUnavailable
from profiles.tsei.relation import RELATION_ID, validate_inputs

ADAPTER_ID = "tsei.serializer-adoption.v0"
REASON = "required authority recomputation operands unavailable in canonical public receipt package"


@lru_cache(maxsize=32)
def produce(producer, vectors, harness, artifact):
    node = shutil.which("node")
    if node is None:
        raise SourceUnavailable("NODE_UNAVAILABLE")
    with tempfile.TemporaryDirectory(prefix="tsei-source-") as temp:
        directory = Path(temp)
        for name, payload in (("producer.ts", producer), ("vectors.json", vectors), ("run.mjs", harness)):
            (directory / name).write_bytes(payload)
        result = subprocess.run([node, "--experimental-strip-types", "run.mjs"], input=artifact, cwd=directory, capture_output=True, timeout=30)
        if result.returncode:
            raise RuntimeError("producer execution/qualification failed: " + result.stderr.decode("utf8", errors="replace")[-1500:])
        return json.loads(result.stdout)


def record_verdict(blobs, record):
    with tempfile.TemporaryDirectory(prefix="tsei-record-") as temp, ExitStack() as files:
        directory = Path(temp)
        (directory / "binding-record.schema.json").write_bytes(blobs["recompute-kit-binding-record.schema.json"])
        namespace = {"__name__": "rsi_pinned_record", "__file__": str(directory / "validator.py"),
                     "open": lambda *args, **kwargs: files.enter_context(open(*args, **kwargs))}
        exec(compile(blobs["recompute-kit-validate_binding_record.py"], str(directory / "validator.py"), "exec"), namespace)
        namespace["_preflight_schema"](namespace["SCHEMA"])
        return namespace["verdict"](record)


def evaluate(root, request):
    inputs = request["inputs"]
    validate_inputs(inputs); verify_snapshots(inputs)
    pin, blobs = read_sources(root)
    record = json.loads(blobs["recompute-kit-tsei.frozen-artifact.json"])
    verdict = record_verdict(blobs, inputs["binding_record"])
    produced = produce(blobs["crystal-receipt-encode-json-utf8-lf-v0.ts"], blobs["recompute-kit-encode-json-utf8-lf-v0.vectors.json"],
                       (Path(__file__).with_name("encoder.mjs")).read_bytes(), encode({"artifact": inputs["artifact"]}))
    if produced["qualified"] != record["producer_conformance"]["qualification"]["vector_count"]:
        raise RuntimeError("qualification count mismatch")
    chronology = pin["chronology"]
    exact_record = inputs["binding_record"] == record
    bound = exact_record and verdict == "valid" and inputs["binding_subject"] == record["binding_subject"] and inputs["serializer_id"] == record["serializer_contract"]["id"]  # TSEI-M1
    mechanism = inputs["registry_commit"] in (chronology["mechanism"]["commit"], chronology["record_introduction"]["parents"][0], chronology["record_introduction"]["commit"], pin["repositories"]["trustless-ai/recompute-kit"])
    adopted = inputs["producer_commit"] == record["effective_commit"]["commit"]  # TSEI-M2
    introduced = inputs["registry_commit"] in (chronology["record_introduction"]["commit"], pin["repositories"]["trustless-ai/recompute-kit"])  # TSEI-M3
    after_effective = inputs["artifact_commit"] == record["effective_commit"]["commit"]
    covered = bound and adopted and introduced and after_effective  # TSEI-M4
    historical = not after_effective
    state = "historically_unversioned" if historical else ("bound" if covered else "binding_not_established")
    authority = {"status": "UNSUPPORTED", "reason": REASON}  # TSEI-M5
    claim = inputs["claim"]
    admissible = covered if claim == "serializer_binding" else False  # TSEI-M6
    return {"relation_id": RELATION_ID, "relation_state": "serializer_adoption_observed", "outputs": {
        "local_structure_valid": verdict == "valid", "record_verdict": verdict,
        "artifact_serialized_sha256": produced["artifact_serialized_sha256"],
        "serializer_binding": bound, "mechanism_active": mechanism, "producer_adopted": adopted,
        "record_introduced": introduced, "artifact_covered": covered, "artifact_binding_state": state,
        "authority_validation": authority, "requested_claim": claim, "claim_admissible": admissible,
    }}
