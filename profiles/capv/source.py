"""Byte-pinned public sources and local build artifacts; offline closure."""
from pathlib import Path
from rsi.codec import decode,raw_digest
from runner.expectation_contract import safe_path
from runner.relation_profile_registry import UnavailableRelation
SOURCE_PIN_SHA256='8fbaeb52d78ced267b9883942669d1da763b4b0ff51f0862fedb3616777cde83'
SDK='e41b117893fb56bc869922de378daf91aad63def'
OLD='948e090c09dd5ec1d4593013303bc5260ef7c466'
FIXED='d950ac1422cf79bafff11fcfb62c3e8b4ce3d782'
class SourceUnavailable(UnavailableRelation):pass
def verify_source(root):
    try:
        raw=safe_path(root,'evidence/capv/source-pin.v0.json').read_bytes()
        if raw_digest(raw)!=SOURCE_PIN_SHA256:raise SourceUnavailable('SOURCE_PIN_DIGEST')
        pin=decode(raw,canonical=True)
        if pin['generations']!={'sdk':OLD,'fixed':FIXED} or pin['sdk_commit']!=SDK:raise SourceUnavailable('GENERATION_PIN')
        for entry in pin['files']:
            if raw_digest(safe_path(root,entry['local_path']).read_bytes())!=entry['sha256']:raise SourceUnavailable('SOURCE_DIGEST: '+entry['local_path'])
        return pin
    except (OSError,ValueError) as e:raise SourceUnavailable('SOURCE_UNAVAILABLE') from e
