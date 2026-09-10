"""Run every explicitly registered mutation through the common classifier."""
from pathlib import Path
import argparse
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from extensions.mutations import registry
from extensions.defaults import composition
from runner.extension_runtime import execute
from rsi.codec import encode, raw_digest


def code_hashes(root):
    return {path.relative_to(root).as_posix():raw_digest(path.read_bytes())
            for directory in ("runner","rsi","adapters","profiles","extensions","tools","tests")
            for path in sorted((root/directory).rglob("*.py"))}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=ROOT/"artifacts/registered-mutations.json")
    args=parser.parse_args()
    corpora,profiles,adapters=composition(ROOT)
    baseline=execute(ROOT,corpora,profiles,adapters)
    if any(baseline["totals"][s] for s in ("FAIL","INVALID_FIXTURE","UNSUPPORTED")):
        print("BASELINE_NOT_GREEN");return 2
    targets=set(adapters.identities()) | {"expectation-admission"}
    before=code_hashes(ROOT)
    report=registry().execute(targets)
    if before!=code_hashes(ROOT):raise RuntimeError("source changed during mutation execution")
    report["implementation_hashes"]=before
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(report))
    print(encode(report["totals"]).decode())
    return 0 if report["mutations"] and all(r["status"]=="KILLED" for r in report["mutations"]) else 1

if __name__=="__main__":raise SystemExit(main())
