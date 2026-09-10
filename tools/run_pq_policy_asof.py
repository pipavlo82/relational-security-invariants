"""Explicit PQ conditional policy/as-of corpus composition through the existing generic runtime."""
import argparse
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from extensions.pq import composition, complete_composition
from runner.relation_runtime import execute
from rsi.codec import encode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/pq-policy-asof.json")
    parser.add_argument("--include-previous", action="store_true")
    args = parser.parse_args()
    result = execute(ROOT, *(complete_composition(ROOT) if args.include_previous else composition(ROOT)))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encode(result)); print(result["totals"])
    return int(any(result["totals"][s] for s in ("FAIL", "INVALID_FIXTURE", "UNSUPPORTED")))


if __name__ == "__main__":
    raise SystemExit(main())
