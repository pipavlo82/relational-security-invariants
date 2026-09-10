"""Actual TAS gate/service execution with controlled resolver and SDK ports."""
from copy import deepcopy
from pathlib import Path
import subprocess,shutil
from rsi.codec import encode,decode
from profiles.tas.source import read_sources,SourceUnavailable
ADAPTER_ID='tas.context-invocation.v0'
def evaluate(root,request):
    read_sources(root)
    value=deepcopy(request['inputs'])
    transported=value  # TAS-M1
    accepted=transported  # TAS-M4
    member_input=accepted  # TAS-M3
    node=shutil.which('node')
    if node is None:raise SourceUnavailable('NODE_UNAVAILABLE')
    p=subprocess.run([node,str(Path(root)/'adapters/tas/execute.mjs')],input=encode(member_input),capture_output=True,timeout=20)
    if p.returncode:raise SourceUnavailable('SOURCE_EXECUTION_FAILED')
    actual=decode(p.stdout)
    mirror=actual  # TAS-M6
    occurrence='UNSUPPORTED'  # TAS-M5
    return {'relation_id':'verified-workflow-dispatch','relation_state':'conditional_dispatch_observed','outputs':{'native':mirror,'invocation_admitted':mirror['dispatched'] is not None,'execution_occurrence':occurrence,'context_authenticity':'SUPPLIED_NOT_RECOMPUTED'}}
