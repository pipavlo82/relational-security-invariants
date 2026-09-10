"""Composition of two source-scoped digest relations, without crypto promotion."""
from rsi.codec import domain
from runner.relation_profile import Relation, RelationProfile
from profiles.rvr.source import SOURCE_PIN_SHA256, verify_source

PROFILE_ID = "rvr.digest-binding.v0"
RELATION_ID = "profile-and-verdict-digest-binding"
VERSION = "0"


def obj(value, required, optional=()):
    if type(value) is not dict or not set(required) <= set(value) or set(value) - set(required) - set(optional):
        raise ValueError("missing or undeclared source input member")


def authorization(value):
    obj(value, (), ("party", "signed_digest", "pubkey"))
    if any(v is not None and type(v) is not str for v in value.values()):
        raise ValueError("authorization members must be strings or null")


def validate_inputs(value):
    domain(value)  # No float/Unicode normalization into the supported transport.
    task = value["transition"]
    obj(task, ("in_force_profile", "proposed_profile", "escrow_ref"),
        ("amendment", "authorizations", "required_parties"))
    for field in ("in_force_profile", "proposed_profile"):
        if type(task[field]) is not dict or not task[field]:
            raise ValueError("nonempty profile object required")
    if type(task["escrow_ref"]) is not str or not task["escrow_ref"]:
        raise ValueError("escrow reference required")
    if task.get("required_parties", ["buyer", "supplier"]) != ["buyer", "supplier"]:
        raise ValueError("this profile covers the source bilateral default only")
    amendment = task.get("amendment")
    if amendment is not None:
        obj(amendment, ("schema", "prior_profile_commitment", "new_profile_commitment", "escrow_ref"))
        if amendment["schema"] != "profile-amendment.v0" or any(type(v) is not str for v in amendment.values()):
            raise ValueError("well-shaped amendment required; binding checked separately")
    auth = task.get("authorizations", {})
    obj(auth, (), ("buyer", "supplier"))
    for entry in auth.values():
        authorization(entry)
    verdict = value.get("verdict")
    if verdict is not None:
        obj(verdict, ("verdict_core",), ("resolver_sig",))
        if type(verdict["verdict_core"]) is not dict:
            raise ValueError("verdict core object required")
        if verdict.get("resolver_sig") is not None:
            authorization(verdict["resolver_sig"])
    if value.get("claim", "digest_binding") not in ("digest_binding", "crypto_authentication"):
        raise ValueError("unsupported dependent claim")


def validate_outputs(value):
    out = value["outputs"]
    obj(out, ("transition", "verdict_binding", "substantive_resolution", "crypto_authentication", "requested_claim", "claim_admissible"))
    obj(out["transition"], ("prior_profile_commitment", "new_profile_commitment", "amendment_cc", "transition_status", "effective_profile_commitment"))
    if any(v is not None and type(v) is not str for v in out["transition"].values()):
        raise ValueError("transition output transport")
    if out["verdict_binding"] is not None:
        obj(out["verdict_binding"], ("verdict_core_cc", "resolution_status", "bound_profile_commitment"))
        if any(v is not None and type(v) is not str for v in out["verdict_binding"].values()):
            raise ValueError("verdict output transport")
    obj(out["crypto_authentication"], ("status", "reason"))
    if any(type(v) is not str for v in out["crypto_authentication"].values()):
        raise ValueError("capability output transport")
    if type(out["claim_admissible"]) is not bool or type(out["requested_claim"]) is not str or type(out["substantive_resolution"]) is not str:
        raise ValueError("claim output transport")
    # Shape only. Truth is independently compared with admitted expectations.


def make_profile(root):
    def validate(value):
        verify_source(root)
        validate_inputs(value)

    def interpret(value, context):
        from adapters.rvr.model import evaluate
        return evaluate(root, {"inputs": value})

    return RelationProfile(PROFILE_ID, VERSION, (
        Relation(RELATION_ID, ("transition",), ("verdict", "claim"), validate, interpret, validate_outputs),
    ), SOURCE_PIN_SHA256)
