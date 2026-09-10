"""Isolated source mutants. Crashes/import errors never earn KILLED.
Only a completed conformance comparison at the mapped case can kill a mutant.
"""
import argparse
from pathlib import Path
import os
import py_compile
import shutil
import subprocess
import sys
import tempfile
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rsi.codec import encode, load, digest

STATUSES = ("KILLED", "SURVIVED", "VACUOUS", "NOT_APPLIED", "RUNNER_ERROR", "OFF_TARGET")

from extensions.legacy_mutations import definitions


def copy_repo(destination):
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", "artifacts", "*.pyc"))

def run_child(root):
    output = root / "artifacts" / "run.json"
    env = dict(os.environ, PYTHONPATH="", PYTHONDONTWRITEBYTECODE="1")
    process = subprocess.run([sys.executable, "-B", "-m", "rsi.run", "--output", str(output)],
        cwd=root, env=env, capture_output=True, text=True, timeout=30)
    report = load(output) if output.exists() else None
    if report is not None and digest(report["evidence"]) != report["evidence_digest"]:
        raise RuntimeError("child evidence digest mismatch")
    return process, report

def exercise(definition):
    with tempfile.TemporaryDirectory(prefix="rsi-mutant-") as tmp:
        root = Path(tmp) / "repo"
        copy_repo(root)
        source = root / definition["path"]
        text = source.read_text(encoding="utf-8")
        result = {"id": definition["id"], "status": "NOT_APPLIED", "killed_by": [],
                  "collateral": [], "exit_code": None, "errors": [], "mutant_evidence_digest": None}
        if text.count(definition["old"]) != 1:
            return result
        source.write_text(text.replace(definition["old"], definition["new"], 1), encoding="utf-8", newline="\n")
        try:
            py_compile.compile(str(source), doraise=True)
        except py_compile.PyCompileError:
            result["status"] = "VACUOUS"
            result["errors"] = ["COMPILE_ERROR"]
            return result
        try:
            process, report = run_child(root)
        except Exception as exc:
            result["status"] = "RUNNER_ERROR"
            result["errors"] = [type(exc).__name__]
            return result
        result["exit_code"] = process.returncode
        if report is None:
            result["status"] = "RUNNER_ERROR"
            result["errors"] = ["NO_STRUCTURED_REPORT"]
            return result
        result["mutant_evidence_digest"] = report["evidence_digest"]
        cases = report["evidence"]["cases"]
        result["check_events"] = [{"check_id":row["key"], "status":row["status"] if row["status"] in ("PASS","FAIL") else "ERROR", "phase":"decision" if row["status"] in ("PASS","FAIL") else "execution"} for row in cases]
        failed = {row["key"] for row in cases if row["status"] == "FAIL"}
        mapped = set(definition["mapped_cases"])
        result["killed_by"] = sorted(failed & mapped)
        result["collateral"] = sorted(failed - mapped)
        if process.returncode == 2 or any(row["status"] == "RUNNER_ERROR" for row in cases):
            result["status"] = "RUNNER_ERROR"
        elif process.returncode == 1 and mapped <= failed:
            result["status"] = "KILLED"
        elif failed:
            result["status"] = "OFF_TARGET"
        elif process.returncode == 0:
            result["status"] = "SURVIVED"
        else:
            result["status"] = "RUNNER_ERROR"
        return result

def self_controls():
    path = "adapters/messaging/model.py"
    original = 'subject_ok = proof["public_key_hex"] == policy["subject_key"]  # M001'
    examples = [("parse_failure", "subject_ok = (  # M001", "VACUOUS"),
                ("call_exception", 'raise RuntimeError("harness control")  # M001', "RUNNER_ERROR"),
                ("missing_patch", "unused", "NOT_APPLIED"),
                ("equivalent_patch", original.replace("# M001", "# equivalent"), "SURVIVED")]
    result = []
    for name, new, expect in examples:
        old = "not-present-in-source" if name == "missing_patch" else original
        observed = exercise({"id": name, "path": path, "old": old, "new": new,
                             "mapped_cases": ["RSI-001/mutation/messaging"]})
        result.append({"id": name, "expected": expect, "observed": observed["status"], "ok": observed["status"] == expect})
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT/"artifacts/prove-can-fail.json")
    args = parser.parse_args()
    baseline, report = run_child(ROOT)
    if baseline.returncode != 0 or report is None or report["evidence"]["counts"] != {"PASS":36,"FAIL":0,"RUNNER_ERROR":0}:
        print("BASELINE_NOT_GREEN", file=sys.stderr)
        return 2
    mutants = []
    for definition in definitions():
        result = exercise(definition)
        mutants.append(result)
        print(result["status"], result["id"], "mapped=" + ",".join(result["killed_by"]), "collateral="+str(len(result["collateral"])))
    controls = self_controls()
    counts = {status: sum(m["status"] == status for m in mutants) for status in STATUSES}
    evidence = {"schema": "rsi-mutation-gate.v0", "baseline_digest": report["evidence_digest"],
                "definitions": definitions(), "counts": counts, "mutants": mutants, "classifier_controls": controls}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encode({"evidence": evidence, "evidence_digest": digest(evidence)}))
    good = counts["KILLED"] == len(mutants) and all(c["ok"] for c in controls)
    print("MUTATION_GATE", "PASS" if good else "FAIL", counts, "classifier_controls="+str(sum(c["ok"] for c in controls))+"/"+str(len(controls)))
    return 0 if good else 1
if __name__ == "__main__":
    raise SystemExit(main())
