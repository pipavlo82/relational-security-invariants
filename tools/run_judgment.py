"""Judgment record profile composition through the unchanged generic pipeline."""
import argparse,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from extensions.judgment import composition,complete_composition
from runner.relation_runtime import execute
from rsi.codec import encode
def main():
    p=argparse.ArgumentParser();p.add_argument('--include-previous',action='store_true');p.add_argument('--output',type=Path,default=ROOT/'artifacts/judgment.json');a=p.parse_args()
    result=execute(ROOT,*(complete_composition(ROOT) if a.include_previous else composition(ROOT)))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(encode(result));print(result['totals'])
    return int(any(result['totals'][k] for k in ('FAIL','INVALID_FIXTURE','UNSUPPORTED')))
if __name__=='__main__':raise SystemExit(main())
