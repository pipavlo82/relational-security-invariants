"""Fail-closed corpus runner. PASS/FAIL concern the benchmark, not the input's safety."""
import argparse
from copy import deepcopy
import importlib
from pathlib import Path
import sys
from rsi.codec import encode, digest, raw_digest
from rsi.corpus import verify, validator

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = ("messaging", "generic")

def source_identity(root):
    files = []
    for directory in ["rsi", "adapters", "schema", "fixtures", "oracle", "spec", "tools", "tests", "research"]:
        files.extend(p for p in (root/directory).rglob("*") if p.is_file() and p.suffix in (".py", ".json", ".md"))
    files += [root/"manifest.json", root/"requirements-dev.txt"]
    return {p.relative_to(root).as_posix(): raw_digest(p.read_bytes()) for p in sorted(files)}

def evaluate(root=ROOT):
    root = Path(root)
    fixtures, expectations = verify(root)
    output_validator = validator(root/"schema/observation.v0.schema.json")
    modules = {name: importlib.import_module("adapters." + name + ".model") for name in ADAPTERS}
    rows = []
    for fixture in fixtures:
        for case in fixture["cases"]:
            for name in ADAPTERS:
                key = fixture["id"] + "/" + case["name"] + "/" + name
                # Detached challenge: no id, name, role, expected value or oracle given to target.
                request = deepcopy(case["requests"][name])
                input_digest = digest(request)
                errors = []
                try:
                    actual = modules[name].run(request)
                    output_validator.validate(actual)
                    if digest(request) != input_digest:
                        raise RuntimeError("adapter mutated its supplied challenge")
                    expected = expectations[key]["observation"]
                    success = encode(actual) == encode(expected)
                    status = "PASS" if success else "FAIL"
                except Exception as exc:
                    actual = None
                    status = "RUNNER_ERROR"
                    errors = [type(exc).__name__]
                rows.append({"key": key, "status": status, "input_digest": input_digest,
                    "local_validity": expectations[key]["local_validity"],
                    "expected": expectations[key]["observation"], "observed": actual, "errors": errors})
    counts = {state: sum(r["status"] == state for r in rows) for state in ("PASS", "FAIL", "RUNNER_ERROR")}
    evidence = {"schema": "rsi-run.v0", "scope": "synthetic-reference-models-only", "source_hashes": source_identity(root),
                "corpus_digest": raw_digest((root/"manifest.json").read_bytes()), "counts": counts, "cases": rows}
    return {"evidence": evidence, "evidence_digest": digest(evidence)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = evaluate()
    except Exception as exc:
        print("RUNNER_ERROR: " + type(exc).__name__ + ": " + str(exc), file=sys.stderr)
        return 2
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(encode(report))
    counts = report["evidence"]["counts"]
    print("RSI", " ".join(k+"="+str(v) for k,v in counts.items()), "digest="+report["evidence_digest"])
    for row in report["evidence"]["cases"]:
        if row["status"] != "PASS":
            print(row["status"], row["key"], ",".join(row["errors"]))
    if counts["RUNNER_ERROR"]:
        return 2
    return 1 if counts["FAIL"] else 0
if __name__ == "__main__":
    raise SystemExit(main())
