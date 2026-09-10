"""Pinned Crystal Receipt corpus through the existing relation-aware pipeline."""
import argparse
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from extensions.crystal_receipt import composition,complete_composition
from runner.relation_runtime import execute
from rsi.codec import encode

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path,default=ROOT/"artifacts/crystal-receipt.json");parser.add_argument("--include-legacy",action="store_true");args=parser.parse_args()
    report=execute(ROOT,*(complete_composition(ROOT) if args.include_legacy else composition(ROOT)))
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(report));print(report["totals"])
    return int(any(report["totals"][s] for s in ("FAIL","INVALID_FIXTURE","UNSUPPORTED")))
if __name__=="__main__":raise SystemExit(main())
