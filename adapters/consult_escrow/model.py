"""Actual pinned Solidity bytecode on isolated EVM; no RPC or wallets."""
from pathlib import Path
import subprocess,shutil
from rsi.codec import encode,decode
from profiles.consult_escrow.source import read_sources,SourceUnavailable
ADAPTER_ID='consult-escrow.release-binding.v0'
def evaluate(root,request):
    read_sources(root)
    variant='canonical'  # CE-M1 CE-M5 CE-M8
    node=shutil.which('node')
    if node is None:raise SourceUnavailable('NODE_UNAVAILABLE')
    p=subprocess.run([node,str(Path(root)/'adapters/consult_escrow/execute.mjs'),variant],input=encode(request['inputs']),capture_output=True,timeout=20)
    if p.returncode:raise SourceUnavailable('SOURCE_EXECUTION_FAILED')
    actual=decode(p.stdout)
    occurrence=actual['execution_occurrence']  # CE-M6
    actual['execution_occurrence']=occurrence
    mirror=actual  # CE-M7
    return {'relation_id':'job-bound-release','relation_state':'release_observed','outputs':mirror}
