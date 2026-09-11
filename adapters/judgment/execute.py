"""Execute the unchanged pinned reference in an isolated process, offline."""
import importlib.util,json,sys
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'evidence/judgment/reference/verifier.py'
spec=importlib.util.spec_from_file_location('pinned_governance',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
v=json.load(sys.stdin);raw=m.verify_fixture(v)
out={'source_overall':raw['overall_pass'],'source_failure':raw['failure_reason'],'source_checks':{k:{'pass':s['pass'],'code':s['code']} for k,s in raw['suites'].items()},'envelope_hash':raw['envelope_hash'],'signature_valid':m._event_signature_valid(v['admission']['verdict_event'])}
print(json.dumps(out,sort_keys=True,separators=(',',':')))
