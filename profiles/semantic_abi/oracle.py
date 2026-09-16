"""Separately implemented tuple-set derivation from manifest-v0 typed-unit rules.

No actual-side execution/import, source-parser or frozen expectation access.
Boundary annotation/positive-match precedence comes from the pinned linker;
this source-algorithm overlap is explicitly not independent-author evidence.
"""
def derive(v):
    def unit(c):
        temporal=tuple((k,c[k]) for k in ('issued_at','verification_time') if k in c)
        if len(temporal)!=1:raise ValueError('one temporal coordinate required')
        return (c['claim_type'],c['scope'],temporal[0],c['authority_class'])
    supplied={unit(c) for c in v['producer']['establishes']}
    # Directed, claim-local authority closure; no reverse or global coercion.
    permitted=supplied | {(*u[:3],'SEMANTIC_VERIFICATION') for u in supplied if u[3]=='INDEPENDENT_RECOMPUTATION'}
    wanted=unit(v['requirement'])
    accepted=wanted in permitted
    negative={(c['claim_type'],c['scope'],c['authority_class']) for c in v['producer']['does_not_establish']}
    hit=not accepted and (wanted[0],wanted[1],wanted[3]) in negative
    return {'relation_id':'claim-authority-scope-time-binding','relation_state':'edge_observed','outputs':{'edge_compatible':accepted,'explicit_boundary_hit':hit,'claim_truth':'UNSUPPORTED','execution_occurrence':'UNSUPPORTED'}}
