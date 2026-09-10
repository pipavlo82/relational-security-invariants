"""Pinned source functions on pinned JS dependencies, offline RPC replay."""
from pathlib import Path
import subprocess,shutil
from rsi.codec import encode,decode
from profiles.verify_layer.source import read_sources,SourceUnavailable
ADAPTER_ID='verify-layer.proof-context.v0'
def evaluate(root,request):
    read_sources(root)
    variant='canonical'  # VL-M5
    node=shutil.which('node')
    if node is None:raise SourceUnavailable('NODE_UNAVAILABLE')
    p=subprocess.run([node,str(Path(root)/'adapters/verify_layer/execute.mjs'),variant],input=encode(request['inputs']),capture_output=True,timeout=20)
    if p.returncode:raise SourceUnavailable('SOURCE_EXECUTION_FAILED')
    actual=decode(p.stdout)
    bound=actual['boundToHeader']  # VL-M1
    actual['boundToHeader']=bound
    header=actual['headerAuthority']  # VL-M2
    actual['headerAuthority']=header
    downstream=actual['downstreamAuthority']  # VL-M6
    actual['downstreamAuthority']=downstream
    claim=actual['claimMatchesProof']  # VL-M9
    actual['claimMatchesProof']=claim
    mirror=actual  # VL-M7
    return {'relation_id':'account-proof-root-balance','relation_state':'account_observed','outputs':mirror}
