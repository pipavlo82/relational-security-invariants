"""Separately implemented predictor: derive balances from admitted-history sums.
No EVM, source gate, source storage evaluator, or frozen row is an oracle here.
"""
from pathlib import Path
from rsi.codec import load
from runner.expectation_registry import ExpectationProfile,FixtureSource
from runner.relation_runtime import validate_envelope,plan
from profiles.aggregate.source import verify_source
EXPECTATION_ID='erc8312.aggregate-budget.v0'
def derive(v):
    edge=v['engine']=='edge';nodes=[[dict(parent=0,agent=r['agent'],cap=int(r['cap']) if edge else 0,revoked=False,depth=0)] for r in v['roots']];ledger=[];rows=[]
    def amount(root,period,node=None):return sum(e[3] for e in ledger if e[0]==root and e[1]==period and (node is None or e[2]==node))
    def active(root,node):
        while True:
            n=nodes[root][node]
            if n['revoked']:return False
            if node==0:return True
            node=n['parent']
    for s in v['steps']:
        ri=s['root'];root=v['roots'][ri];nn=nodes[ri];error=None;period=0;value=int(s['amount']);i=s['node'];op=s['op']
        if i>=len(nn):error='UnknownGrant' if edge else 'UnknownNode'
        else:
            n=nn[i]
            if op=='delegate':
                if s['caller']!=n['agent']:error='Unauthorized'
                elif edge and value>n['cap']:error='AttenuationViolated'
                elif not edge and n['cap']!=0:error='CappedNodeCannotDelegate'
                elif not active(ri,i):error='PathRevoked'
                elif not edge and n['depth']+1>=16:error='DepthExceeded'
                if error is None:nn.append(dict(parent=i,agent=s['agent'],cap=value,revoked=False,depth=n['depth']+1))
            elif op=='revoke':
                if s['caller']!=root['issuer'] and not (i!=0 and s['caller']==nn[n['parent']]['agent']):error='Unauthorized'
                else:n['revoked']=True
            else:
                t=int(s['time']);start=int(root['period_anchor']);length=int(root['period_length'])
                if value==0 and not edge:error='ZeroAmount'
                elif s['caller']!=n['agent']:error='Unauthorized'
                elif not active(ri,i):error='PathRevoked'
                elif length and t<start:error='PeriodNotStarted'
                else:
                    period=(t-start)//length if length else 0
                    own=amount(ri,period,i)
                    if (edge or n['cap']!=0) and own+value>n['cap']:error='EdgeBoundExceeded' if edge else 'NodeBoundExceeded'
                    elif not edge and amount(ri,period)+value>int(root['cap']):error='RootBoundExceeded'
                    if error is None:ledger.append((ri,period,i,value))
        rows.append(dict(op=op,status='RETURN' if error is None else 'REVERT',error=error,local_draw_valid=error in (None,'RootBoundExceeded') if op=='draw' else None,drawn_events=int(not edge and op=='draw' and error is None),meters=['UNSUPPORTED' if edge else str(amount(r,p)) for r in range(len(v['roots'])) for p in v['periods']]))
    meters=[dict(root=r,period=p,cap=root['cap'],spent_root='UNSUPPORTED' if edge else str(amount(r,p)),admitted_sum=str(amount(r,p)),conserves=amount(r,p)<=int(root['cap']),meter_matches='UNSUPPORTED' if edge else True) for r,root in enumerate(v['roots']) for p in v['periods']]
    out=dict(steps=rows,meters=meters,log_origin='SUCCESSFUL_SOURCE_CALLS' if edge else 'SOURCE_DRAWN_EVENTS',realized=str(sum(e[3] for e in ledger)),conserved=all(m['conserves'] for m in meters))
    for k in ('non_bypassability','asset_movement','cross_chain_conservation','subtree_budgets','authoritative_chain_state'):out[k]='UNSUPPORTED'
    return dict(relation_id='root-budget-conservation',relation_state='meter_observed',outputs=out)
def predict(f):return {f['id']+'/'+c['case_id']:{'local_validity':True,'observation':derive(c['inputs'])} for c in f['cases']}
def validate_prediction(v):
    if type(v) is not dict or not v:raise ValueError('prediction')
    for r in v.values():
        if set(r)!={'local_validity','observation'} or r['local_validity'] is not True:raise ValueError('prediction row')
def make_profile(root):
    m=load(Path(root)/'profiles/aggregate/expectation-profile.v0.json')
    if m['profile_id']!=EXPECTATION_ID or m['version']!='0':raise ValueError('profile pin')
    return ExpectationProfile(EXPECTATION_ID,'0',tuple(FixtureSource(**r) for r in m['fixture_scope']),predict,m['expectations_path'],m['expectations_digest'],validate_envelope,validate_prediction,lambda f:plan(f,'binding'),lambda r:verify_source(r))
