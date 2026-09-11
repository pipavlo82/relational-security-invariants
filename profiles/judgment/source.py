"""Exact offline source closure; no semantic computation shared across the two legs."""
from rsi.codec import decode,raw_digest
from runner.expectation_contract import safe_path
from runner.relation_profile_registry import UnavailableRelation
SOURCE_PIN_SHA256='015c1bd9f03e5b41d8611fcb849cfd41f0600e282a4bcee6871ed3fb7eb1e207'
class SourceUnavailable(UnavailableRelation):pass
def verify_source(root):
    try:
        raw=safe_path(root,'evidence/judgment/source-pin.v0.json').read_bytes()
        if raw_digest(raw)!=SOURCE_PIN_SHA256:raise SourceUnavailable('SOURCE_PIN_DIGEST')
        pin=decode(raw,canonical=True)
        for e in pin['files']:
            if raw_digest(safe_path(root,e['local_path']).read_bytes())!=e['sha256']:raise SourceUnavailable('SOURCE_DIGEST: '+e['local_path'])
        return pin
    except (OSError,ValueError) as e:raise SourceUnavailable('SOURCE_UNAVAILABLE') from e
