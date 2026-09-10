"""Explicit mutation registration and phase-aware, project-neutral classification."""
from dataclasses import dataclass
from rsi.codec import encode

STATES = ("KILLED", "SURVIVED", "VACUOUS", "NOT_APPLIED")

@dataclass(frozen=True)
class CheckEvent:
    check_id: str
    status: str
    phase: str

@dataclass(frozen=True)
class MutationTrace:
    applied: bool
    events: tuple = ()
    errors: tuple = ()

@dataclass(frozen=True)
class Mutation:
    mutation_id: str
    target_id: str
    mapped_check: str
    implementation: object
    expected_failure_phase: str
    applicable: object = lambda context: True


class MutationRegistry:
    def __init__(self, mutations=()):
        self._mutations = {}
        for mutation in mutations:
            self.register(mutation)
    def register(self, mutation):
        if not isinstance(mutation, Mutation):
            raise ValueError("trusted mutation registration required")
        if any(type(x) is not str or not x or not x.isascii() for x in (mutation.mutation_id,mutation.target_id,mutation.mapped_check,mutation.expected_failure_phase)):
            raise ValueError("invalid mutation identity or mapping")
        if mutation.expected_failure_phase not in ("decision", "test", "admission"):
            raise ValueError("only mapped execution/admission/assertion phases can kill")
        if mutation.mutation_id in self._mutations:
            raise ValueError("duplicate mutation identity")
        if not callable(mutation.implementation) or not callable(mutation.applicable):
            raise ValueError("trusted mutation implementation required")
        self._mutations[mutation.mutation_id] = mutation
    def identities(self):
        return tuple(sorted(self._mutations))
    def execute(self, targets, context=None):
        rows = []
        for ident in self.identities():
            mutation = self._mutations[ident]
            try:
                if mutation.target_id not in targets or not mutation.applicable(context):
                    trace = MutationTrace(False)
                else:
                    trace = mutation.implementation(context)
                row = classify(mutation, trace)
            except Exception as exc:
                row = {"mutation_id":ident,"status":"VACUOUS","mapped_check":mutation.mapped_check,
                       "collateral":[],"errors":[type(exc).__name__]}
            rows.append(row)
        return {"schema":"rsi-registered-mutations.v0","mutations":rows,
                "totals":{state:sum(row["status"]==state for row in rows) for state in STATES}}


def classify(mutation, trace):
    if not isinstance(trace, MutationTrace) or type(trace.applied) is not bool or type(trace.events) is not tuple or type(trace.errors) is not tuple:
        raise ValueError("invalid mutation trace")
    for event in trace.events:
        if not isinstance(event, CheckEvent) or event.status not in ("PASS","FAIL","ERROR"):
            raise ValueError("invalid check event")
    mapped = [event for event in trace.events if event.check_id == mutation.mapped_check]
    collateral = sorted(event.check_id for event in trace.events if event.status=="FAIL" and event.check_id != mutation.mapped_check)
    if trace.errors or any(event.status=="ERROR" or (event.status=="FAIL" and event.phase not in ("decision", "test", "admission")) for event in trace.events):
        status = "VACUOUS"
    elif not trace.applied or not mapped:
        status = "NOT_APPLIED"
    elif len(mapped) != 1 or mapped[0].phase != mutation.expected_failure_phase:
        status = "VACUOUS"
    else:
        status = "KILLED" if mapped[0].status == "FAIL" else "SURVIVED"
    return {"mutation_id":mutation.mutation_id,"target_id":mutation.target_id,
            "mapped_check":mutation.mapped_check,"expected_failure_phase":mutation.expected_failure_phase,
            "status":status,"collateral":collateral,"errors":list(trace.errors)}
