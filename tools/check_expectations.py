"""Independently check the pinned envelope and exact legacy row preservation."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rsi.codec import encode, load
from profiles.synthetic import make_profile
from runner.expectation_contract import admit, load_fixtures

def main():
    profile = make_profile(ROOT)
    profile.validate_scope(ROOT)
    documents = load_fixtures(ROOT, profile)
    admitted = admit(ROOT, profile, documents)
    rows = {}
    for document in documents:
        rows.update(admitted.for_fixture(document.fixture_id))
    legacy = load(ROOT / "oracle/expected.v0.json")
    if encode(rows) != encode(legacy["expectations"]):
        raise ValueError("legacy expectation rows changed")
    print("Expectation set admitted; legacy rows preserved:", len(rows))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
