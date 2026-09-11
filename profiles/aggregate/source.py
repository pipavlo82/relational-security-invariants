"""Exact offline source closure; no semantic computation shared across the two legs."""
from rsi.codec import decode,raw_digest
from runner.expectation_contract import safe_path
from runner.relation_profile_registry import UnavailableRelation
SOURCE_PIN_SHA256='deb7bc66ffa1ae42eabd925d593965a21d479744139a4735c5368e0528edd835'
class SourceUnavailable(UnavailableRelation):pass
def verify_source(root):
    try:
        raw=safe_path(root,'evidence/aggregate/source-pin.v0.json').read_bytes()
        if raw_digest(raw)!=SOURCE_PIN_SHA256:raise SourceUnavailable('SOURCE_PIN_DIGEST')
        pin=decode(raw,canonical=True)
        for e in pin['files']:
            if raw_digest(safe_path(root,e['local_path']).read_bytes())!=e['sha256']:raise SourceUnavailable('SOURCE_DIGEST: '+e['local_path'])
        return pin
    except (OSError,ValueError) as e:raise SourceUnavailable('SOURCE_UNAVAILABLE') from e
