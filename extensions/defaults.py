"""Trusted application composition; no imports selected by metadata."""
from pathlib import Path
from rsi.codec import load
from rsi.corpus import validator
from profiles.defaults import registries
from runner.fixture_registry import Corpus, FixtureRegistry


def composition(root):
    root = Path(root)
    profiles, adapters = registries(root)
    pin = load(root / "extensions/corpora.v0.json")
    if set(pin) != {"schema", "corpora"} or pin["schema"] != "rsi-corpora.v0":
        raise ValueError("invalid corpus configuration")
    validate = validator(root / "schema/registered-fixture.v0.schema.json").validate
    corpora = FixtureRegistry(Corpus(validate_fixture=validate, **record) for record in pin["corpora"])
    return corpora, profiles, adapters
