"""Post-freeze mechanical comparison; not a blind semantic deriver."""
import argparse, hashlib, json, pathlib, re, shutil, subprocess
def raw_hash(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def serial(v): return (json.dumps(v,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode()
def require(ok, message):
    if not ok: raise ValueError(message)
p=argparse.ArgumentParser()
for name in ['rsi_root','pack_root','submission_root','origin_record','h2_replay','output_dir']:
    p.add_argument('--'+name.replace('_','-'),type=pathlib.Path,required=True)
a=p.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
require(raw_hash(a.submission_root/'DERIVATION.json')=='c05b65cbca87433bceb1cd0d3a50600cbb71bbbbb673d576715700100d508ec1','Submission digest drift')
require(raw_hash(a.submission_root/'derive.mjs')=='6975ae8047202127b862cb08768dc6023a493b286b277d9eb3fe4bdbe73365b3','Harness digest drift')
require(raw_hash(a.pack_root/'HASHES.sha256')=='7043e00225a908cbccf8b5ea01f3b205a5983a1a562977d2118174c58b7533b3','Pack hash-list drift')
require(raw_hash(a.pack_root/'PACK_MANIFEST.json')=='fd1b54c809e87d19bde82d86bbc4e9aec56055021a95322898b5b81052cfb220','Pack manifest drift')
require(raw_hash(a.origin_record)=='b130cd433276cdcee8cce6ecf2820d85acad1943e05bf316a31751429531546e','Precommitted origin mapping drift')
for line in (a.pack_root/'HASHES.sha256').read_text().splitlines():
    digest,name=line.split(None,1);target=a.pack_root/name.strip()
    require(target.resolve().is_relative_to(a.pack_root.resolve()),'Pack path escape')
    require(raw_hash(target)==digest,'Pack payload drift: '+name)
frozen_path=a.rsi_root/'profiles/crystal_receipt/expectations.v0.json'
require(raw_hash(frozen_path)=='268b0e5dd6087cc60bf9c99ca5c20c0b135983d595ff632659c81b18634a4ba3','Frozen expectation drift')
definition=json.loads((a.submission_root/'DERIVATION.json').read_bytes())
origin=json.loads(a.origin_record.read_bytes())
mapping=origin['cases']
ids=[x['case_id'] for x in mapping]
require(len(ids)==len(set(ids))==4,'Origin inventory mismatch')
submitted={x['case_id']:x for x in definition['cases']}
require(len(definition['cases'])==len(submitted)==4 and set(submitted)==set(ids),'Submission missing/duplicate/extra cases')
require(set(x.stem for x in (a.pack_root/'inputs').glob('*.json'))==set(ids),'Pack inventory mismatch')
require(all(x['derived_state'] in ['PRESERVED','VIOLATED','UNVERIFIABLE'] for x in submitted.values()),'Invalid submission state')
source={}
for row in origin['source_files']:
    file=a.rsi_root/row['local_path'];require(raw_hash(file)==row['sha256'],'Origin source drift')
    source[pathlib.PurePosixPath(row['path']).name]=json.loads(file.read_bytes())
def select(spec):
    name,pointer=spec.split('#',1);v=source[name]
    for part in pointer.lstrip('/').split('/'):
        part=part.replace('~1','/').replace('~0','~')
        v=v[int(part)] if isinstance(v,list) else v[part]
    return v
inputs={}
for row in mapping:
    cid=row['case_id'];doc=json.loads((a.pack_root/'inputs'/f'{cid}.json').read_bytes())
    require(doc['case_id']==cid,'Case identity mismatch')
    require(set(doc)=={'case_id','left','right'},'Unexpected input shape')
    for side in ['left','right']:
        require(doc[side]=={'manifest':select(row[side+'_manifest']),'semantic_artifact':select(row[side+'_artifact'])},'Input-origin mismatch: '+cid)
    normalized={'baseline':doc['left'],'candidate':doc['right']}
    h2input=a.rsi_root/'reproducers/crystal-receipt-cleanroom/inputs'/f"{row['h2_vector']}.json"
    require(normalized==json.loads(h2input.read_bytes()),'Pack/H2 input mismatch')
    for ref in submitted[cid]['source_refs']:
        require(ref['commit']=='45b46bf7df3a60b32583291f577a36bf19d22f00','External source commit mismatch')
        file=a.pack_root/ref['source_path']
        require(file.resolve().is_relative_to(a.pack_root.resolve()),'Source ref path escape')
        require(raw_hash(file)==ref['included_sha256'],'External source ref digest mismatch')
    inputs[cid]=normalized
# Only the local input directory literal changes. The submitted file is retained.
code=(a.submission_root/'derive.mjs').read_text(encoding='utf-8')
needle='const uploads = "/mnt/user-data/uploads";'
require(code.count(needle)==1,'Unexpected external harness input path')
adapted=code.replace(needle,'const uploads = '+json.dumps(a.pack_root.resolve().as_posix())+';')
adapted_path=a.output_dir/'derive.local-path-only.mjs';adapted_path.write_bytes(adapted.encode())
run=subprocess.run([shutil.which('node'),str(adapted_path)],capture_output=True,text=True,timeout=40)
(a.output_dir/'external-harness.stdout.txt').write_bytes(run.stdout.encode())
(a.output_dir/'external-harness.stderr.txt').write_bytes(run.stderr.encode())
require(run.returncode==0,'External harness execution error (not semantic disagreement)')
matches=list(re.finditer(r'^(case-\d{3})  =>  ([^\r\n]+)$',run.stdout,re.M))
require(len(matches)==4 and {m[1] for m in matches}==set(ids),'External harness output inventory mismatch')
external={}
for i,m in enumerate(matches):
    block=run.stdout[m.end():matches[i+1].start() if i+1<len(matches) else len(run.stdout)]
    left=re.search(r'^  left \.semantic snapshot : (.*)$',block,re.M)
    right=re.search(r'^  right.semantic snapshot : (.*)$',block,re.M)
    require(left is not None and right is not None,'Missing external snapshot output')
    external[m[1]]={'state':m[2].strip(),'canonical_baseline':left[1].strip(),'canonical_candidate':right[1].strip()}
frozen={}
for f in json.loads(frozen_path.read_bytes())['expectations']: frozen.update(f['prediction'])
h2=json.loads(a.h2_replay.read_bytes())
h2rows={x['vector']:x for x in h2['matrix']}
require(len(h2rows)==len(h2['matrix'])==4,'H2 inventory mismatch')
def state(value):return 'PRESERVED' if value['semantic_identity_preserved'] else 'VIOLATED'
matrix=[]
for row in mapping:
    cid=row['case_id'];key=row['rsi_fixture']+'/'+row['rsi_case'];old=frozen[key]
    require(old['local_validity'] is True,'Unsupported frozen local validity')
    frozen_projection={k:old['observation']['outputs'][k] for k in ['canonical_baseline','canonical_candidate','semantic_identity_preserved']}
    h=h2rows[row['h2_vector']]
    require(h['admitted_row']==key,'H2/frozen row mapping mismatch')
    require(h['frozen_expectation']==frozen_projection,'Re-admitted versus frozen expectation mismatch')
    expected_state=state(frozen_projection)
    legs={k:state(h[k]) for k in ['actual','predictor','third_leg','frozen_expectation']}
    full_equal=h['actual']==h['predictor']==h['third_leg']==frozen_projection
    harness_projection={k:external[cid][k] for k in ['canonical_baseline','canonical_candidate']}
    snapshot_match=all(harness_projection[k]==frozen_projection[k] for k in harness_projection)
    agree=full_equal and snapshot_match and submitted[cid]['derived_state']==external[cid]['state']==expected_state
    matrix.append({'case_id':cid,'rsi_row':key,'h2_vector':row['h2_vector'],'external_derivation':submitted[cid]['derived_state'],'external_harness':external[cid]['state'],**legs,'input_origin_matches':True,'h2_input_matches':True,'all_local_canonical_outputs_equal':full_equal,'external_canonical_outputs_match':snapshot_match,'agreement':agree,'frozen_relation_state':old['observation']['relation_state'],'local_outputs':h['actual'],'input_sha256':raw_hash(a.pack_root/'inputs'/f'{cid}.json')})
result={'schema':'rsi-post-v0-external-mechanical-comparison.v1','round_id':'CR-EXT-DERIVATION-001-DA-001','rsi_v0_commit':'8d8e31291ecf96284212a353efb66f606cff2953','pack_commit':definition['pack_commit'],'derivation_sha256':raw_hash(a.submission_root/'DERIVATION.json'),'origin_record_sha256':raw_hash(a.origin_record),'frozen_expectations_sha256':raw_hash(frozen_path),'external_harness_original_sha256':raw_hash(a.submission_root/'derive.mjs'),'external_harness_local_sha256':raw_hash(adapted_path),'harness_adaptation':'Only /mnt/user-data/uploads input root literal replaced; original bytes retained.','node_version':subprocess.run([shutil.which('node'),'--version'],capture_output=True,text=True,check=True).stdout.strip(),'matrix':matrix,'agreement_count':sum(r['agreement'] for r in matrix),'disagreement_count':sum(not r['agreement'] for r in matrix),'missing_cases':[],'comparison_actor':'Exposed RSI coordinator/Codex; not an external POST_COMMIT_VERIFIER.','external_verifier_comparison':'NOT_PERFORMED','external_reveal':'NOT_SENT','status':'COORDINATOR_COMPARISON_COMPLETE' if all(r['agreement'] for r in matrix) else 'SEMANTIC_DISAGREEMENT_RECORDED','v0_author_independence':'UNKNOWN','strict_blind_derivation':'NOT_ESTABLISHED'}
(a.output_dir/'comparison.json').write_bytes(serial(result))
print(json.dumps({'agreement':result['agreement_count'],'disagreement':result['disagreement_count'],'matrix':[{k:r[k] for k in ['case_id','external_derivation','actual','predictor','third_leg','frozen_expectation','agreement']} for r in matrix]}))
