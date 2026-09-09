"""Compatibility entry point: validates bytes/schema/oracle only, not adapter conformance."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rsi.corpus import verify
try:
    fixtures, oracle = verify(ROOT)
except Exception as exc:
    print("INVALID", type(exc).__name__, str(exc), file=sys.stderr)
    raise SystemExit(2)
print("VALID fixtures=" + str(len(fixtures)) + " cases=" + str(len(oracle)))
