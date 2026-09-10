"""Actual-only execution of exact pinned production TypeScript helpers."""
from pathlib import Path
import shutil
import subprocess
import tempfile
from rsi.codec import encode,decode
from profiles.crystal_receipt.source import read_sources,SourceUnavailable
from profiles.crystal_receipt.relation import observed,validate_inputs
ADAPTER_ID="crystal-receipt.v0"

def capture(root,inputs):
    root=Path(root).resolve()
    pin,blobs=read_sources(root)
    validate_inputs(inputs)
    node=shutil.which("node")
    if node is None:raise SourceUnavailable("NODE_RUNTIME_UNAVAILABLE")
    staging=root/"artifacts";staging.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="crystal-source-",dir=staging) as directory:
        sandbox=Path(directory).resolve()
        if not sandbox.is_relative_to(root):raise SourceUnavailable("SOURCE_STAGE_PATH")
        for name in ("counterfactual-audit-boundary.ts","canonicalize.ts"):
            relative="evidence/crystal-receipt/"+name
            target=sandbox/relative;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(blobs[relative])
        relative="adapters/crystal_receipt/execute.mjs"
        target=sandbox/relative;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((root/relative).read_bytes())
        process=subprocess.run([node,"--experimental-strip-types",str(target)],
            input=encode(inputs),capture_output=True,timeout=15,cwd=sandbox)
    if process.returncode:raise SourceUnavailable("SOURCE_EXECUTION_FAILED")
    value=decode(process.stdout)
    if type(value) is not dict or set(value)!={"baseline","candidate","baseline_outcome","candidate_outcome"}:raise SourceUnavailable("SOURCE_PROTOCOL")
    return value

def evaluate(root,request):
    value=capture(root,request["inputs"])
    return observed(value)  # mapped relation decision
