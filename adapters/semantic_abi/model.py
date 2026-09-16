"""Offline execution of the byte-pinned upstream JavaScript linker."""
from pathlib import Path
import subprocess, shutil
from rsi.codec import encode, decode
from profiles.semantic_abi.source import verify_source, SourceUnavailable
ADAPTER_ID='semantic-abi.claim-edge.v0'

def evaluate(root,request):
    verify_source(root)
    node=shutil.which('node')
    if node is None:raise SourceUnavailable('NODE_UNAVAILABLE')
    p=subprocess.run([node,str(Path(root)/'adapters/semantic_abi/execute.mjs')],input=encode(request['inputs']),capture_output=True,timeout=20)
    if p.returncode:raise SourceUnavailable('SOURCE_EXECUTION_FAILED')
    o=decode(p.stdout)
    o['claim_truth']='UNSUPPORTED'  # SABI-M9
    o['execution_occurrence']='UNSUPPORTED'  # SABI-M10
    return {'relation_id':'claim-authority-scope-time-binding','relation_state':'edge_observed','outputs':o}
