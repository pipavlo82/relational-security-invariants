"""Execute exact pinned Python reference bytes, never a recorded expected row."""
from copy import deepcopy
from profiles.rvr.source import read_sources
from profiles.rvr.relation import RELATION_ID, validate_inputs

ADAPTER_ID = "rvr.digest-binding.v0"


def reference_functions(root):
    _, blobs = read_sources(root)
    functions = []
    # Fixed trusted source/code association. Neither manifest nor input selects code.
    for filename, function in (("amendment_gate.py", "profile_transition"),
                               ("verdict_binding_gate.py", "verdict_binding")):
        namespace = {"__name__": "rsi_pinned_reference"}
        exec(compile(blobs["evidence/rvr/" + filename], filename, "exec"), namespace)
        functions.append(namespace[function])
    return tuple(functions)


def evaluate(root, request):
    inputs = deepcopy(request["inputs"])
    validate_inputs(inputs)
    transition_fn, verdict_fn = reference_functions(root)
    transition = transition_fn(inputs["transition"])  # RVR-M1
    verdict = None
    if inputs.get("verdict") is not None:
        value = {**inputs["verdict"], "task_effective_profile_commitment": transition["effective_profile_commitment"]}
        verdict = verdict_fn(value)  # RVR-M3
    # Keep raw source-native outputs separate. 'not_evaluated' is a wrapper
    # coverage annotation, NOT a source resolution outcome or a boolean false.
    substantive = "not_evaluated"  # RVR-M2
    layers = {"transition": transition, "verdict_binding": verdict}  # RVR-M4
    crypto = {"status": "UNSUPPORTED", "reason": "no_pinned_signature_verification_lane"}  # RVR-M5
    claim = inputs.get("claim", "digest_binding")
    digest_bound = transition["transition_status"] == "permitted" and (verdict is None or verdict["resolution_status"] == "bound")
    admissible = digest_bound if claim == "digest_binding" else False  # RVR-M6
    return {"relation_id": RELATION_ID, "relation_state": "digest_binding_observed", "outputs": {
        **layers, "substantive_resolution": substantive, "crypto_authentication": crypto,
        "requested_claim": claim, "claim_admissible": admissible,
    }}
