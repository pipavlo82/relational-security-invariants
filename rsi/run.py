"""Fail-closed corpus runner. PASS/FAIL concern the benchmark, not the input's safety."""
import argparse
from pathlib import Path
import sys
from rsi.codec import encode, digest, raw_digest
from runner.execution import run_profile, summary, unavailable
from profiles.defaults import registries, DEFAULT_PROFILE

ROOT = Path(__file__).resolve().parents[1]

def source_identity(root):
    files = []
    for directory in ["rsi", "runner", "profiles", "adapters", "schema", "fixtures", "oracle", "spec", "tools", "tests", "research"]:
        files.extend(p for p in (root/directory).rglob("*") if p.is_file() and p.suffix in (".py", ".json", ".md"))
    files += [root/"manifest.json", root/"requirements-dev.txt"]
    return {p.relative_to(root).as_posix(): raw_digest(p.read_bytes()) for p in sorted(files) if p.is_file()}

def evaluate(root=ROOT, *, profile_id=DEFAULT_PROFILE, profiles=None, adapters=None):
    root = Path(root)
    result = None
    if profiles is None or adapters is None:
        try:
            defaults = registries(root)
            profiles = defaults[0] if profiles is None else profiles
            adapters = defaults[1] if adapters is None else adapters
        except Exception as exc:
            result = unavailable(profile_id, "PROFILE_ERROR:REGISTRATION", str(exc))
    if result is None:
        result = run_profile(root, profile_id, profiles, adapters)
    rows = result["cases"]
    counts = {state: sum(r["status"] == state for r in rows) for state in ("PASS", "FAIL", "RUNNER_ERROR")}
    evidence = {"schema":"rsi-run.v0", "scope":"registered-expectation-profiles", "source_hashes":source_identity(root),
                "corpus_digest":raw_digest((root/"manifest.json").read_bytes()) if (root/"manifest.json").is_file() else None,
                "counts":counts, "cases":rows}
    return {"evidence":evidence, "evidence_digest":digest(evidence), "totals":summary(rows), "profile_error":result["profile_error"], "profile_id":profile_id, "expectation_admission":result.get("expectation_admission")}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    args = parser.parse_args()
    try:
        report = evaluate(profile_id=args.profile)
    except Exception as exc:
        print("RUNNER_ERROR: " + type(exc).__name__ + ": " + str(exc), file=sys.stderr)
        return 2
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(encode(report))
    counts = report["evidence"]["counts"]
    print("RSI", " ".join(k+"="+str(v) for k,v in report["totals"].items()), "digest="+report["evidence_digest"])
    for row in report["evidence"]["cases"]:
        if row["status"] != "PASS":
            print(row["status"], row["key"], ",".join(row["errors"]))
    if report["totals"]["UNSUPPORTED"] or report["totals"]["INVALID_FIXTURE"] or counts["RUNNER_ERROR"]:
        return 2
    return 1 if counts["FAIL"] else 0
if __name__ == "__main__":
    raise SystemExit(main())
