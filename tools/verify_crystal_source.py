"""Explicit read-only live-source preflight; never fetches/checks out or repins."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from profiles.crystal_receipt.source import SOURCE_COMMIT,verify_source,SourceUnavailable
from rsi.codec import encode,raw_digest

def inspect(path):
    path=Path(path).resolve()
    if not (path/".git").exists():raise SourceUnavailable("SOURCE_REPOSITORY_UNAVAILABLE")
    command=["git","-c","safe.directory="+path.as_posix(),"-C",str(path)]
    def git(*args):return subprocess.check_output(command+list(args))
    metadata=json.loads(subprocess.check_output(["gh","api","repos/pipavlo82/crystal-receipt"]))
    canonical=json.loads(subprocess.check_output(["gh","api","repos/pipavlo82/crystal-receipt/commits/main"]))["sha"]
    if metadata["default_branch"]!="main" or canonical!=SOURCE_COMMIT:raise SourceUnavailable("SOURCE_DRIFT_REPIN_REVALIDATION_REQUIRED")
    source=verify_source(ROOT)
    for entry in source["files"]:
        if raw_digest(git("show",canonical+":"+entry["path"]))!=entry["sha256"]:raise SourceUnavailable("SOURCE_BLOB_MISMATCH")
    return {"repo":source["repo"],"canonical_branch":"main","canonical_commit":canonical,
        "local_path":path.as_posix(),"remote":git("remote","get-url","origin").decode().strip(),
        "worktree_branch":git("branch","--show-current").decode().strip(),"worktree_head":git("rev-parse","HEAD").decode().strip(),
        "worktree_status":git("status","--porcelain=v1").decode().splitlines(),"source_files_match":True}

def main():
    p=argparse.ArgumentParser();p.add_argument("--source-repo",type=Path,required=True);p.add_argument("--output",type=Path,default=ROOT/"artifacts/crystal-source-preflight.json");args=p.parse_args()
    result=inspect(args.source_repo);args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(result));print("Exact canonical source and vendored Git blob payloads match:",result["canonical_commit"])
if __name__=="__main__":main()
