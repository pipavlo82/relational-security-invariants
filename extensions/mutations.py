"""Trusted bridges preserve the existing mutation implementations and mappings."""
from runner.mutation_registry import Mutation, MutationTrace, CheckEvent, MutationRegistry
from extensions.legacy_mutations import definitions


def legacy_trace(definition):
    from tools.prove_can_fail import exercise
    result = exercise(definition)
    events = tuple(CheckEvent(**row) for row in result.get("check_events", []))
    errors = tuple(result.get("errors", []))
    if result["status"] in ("RUNNER_ERROR", "VACUOUS") and not errors:
        errors = ("HARNESS_ERROR",)
    return MutationTrace(result["status"] != "NOT_APPLIED", events, errors)


def expectation_source_trace(definition):
    from tools.prove_expectations_can_fail import source_mutation
    result = source_mutation(definition)
    events = tuple(CheckEvent(row["id"],row["status"],row.get("phase","test")) for row in result.get("checks",[]))
    errors = (result.get("error","HARNESS_ERROR"),) if result["status"] == "VACUOUS" else ()
    return MutationTrace(result["status"] != "NOT_APPLIED", events, errors)


def expectation_tamper_trace(ident, check):
    from tools.prove_expectations_can_fail import tamper
    result = tamper(ident)
    if result["status"] == "VACUOUS":
        return MutationTrace(True, errors=(result.get("error","WRONG_ADMISSION_GUARD"),))
    # A named admission guard rejected the well-formed mutated evidence.
    # Reaching that failure point is the mapped event, not a setup exception.
    event = CheckEvent(check,"FAIL" if result.get("executed_check") == check else "PASS","admission")
    return MutationTrace(True,(event,))


def registry():
    from tools.prove_expectations_can_fail import DEFINITIONS
    records = []
    for definition in definitions():
        # Target identity is explicit metadata, never parsed from mutation ID.
        target = definition["target_adapter_id"]
        records.append(Mutation(definition["id"],target,definition["mapped_cases"][0],
                                lambda context,d=definition:legacy_trace(d),"decision"))
    for ident,check in (("EXP-M1","PREDICTION_MISMATCH"),("EXP-M2","FIXTURE_SET_DIGEST")):
        records.append(Mutation(ident,"expectation-admission",check,
                                lambda context,i=ident,c=check:expectation_tamper_trace(i,c),"admission"))
    for definition in DEFINITIONS:
        records.append(Mutation(definition["id"],"expectation-admission",definition["mapped"],
                                lambda context,d=definition:expectation_source_trace(d),"test"))
    return MutationRegistry(records)
