"""Trusted, immutable relation contracts; no expected-outcome authority."""
from copy import deepcopy
from dataclasses import dataclass
import re
from rsi.codec import encode


def identifier(value):
    return type(value) is str and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", value) is not None


@dataclass(frozen=True)
class Relation:
    relation_id: str
    required_slots: tuple
    optional_slots: tuple
    validate_inputs: object
    evaluate: object
    validate_outputs: object


@dataclass(frozen=True)
class RelationProfile:
    profile_id: str
    version: str
    relations: tuple
    descriptor_sha256: str | None = None

    def relation(self, relation_id):
        return next((r for r in self.relations if r.relation_id == relation_id), None)

    def validate(self, relation_id, inputs):
        relation = self.relation(relation_id)
        if relation is None:
            raise ValueError("unsupported relation")
        if type(inputs) is not dict:
            raise ValueError("inputs must be an object")
        keys = set(inputs)
        if not set(relation.required_slots) <= keys or keys - set(relation.required_slots + relation.optional_slots):
            raise ValueError("missing required or undeclared input slot")
        before = encode(inputs)
        candidate = deepcopy(inputs)
        relation.validate_inputs(candidate)
        if encode(candidate) != before:
            raise ValueError("input validator changed its input")

    def validate_result(self, relation_id, value):
        if type(value) is not dict or set(value) != {"relation_id", "relation_state", "outputs"}:
            raise ValueError("invalid relation result")
        if value["relation_id"] != relation_id or not identifier(value["relation_state"]) or type(value["outputs"]) is not dict:
            raise ValueError("invalid result binding or state")
        if len(encode(value)) > 1048576:
            raise ValueError("relation result exceeds byte limit")
        before = encode(value)
        candidate = deepcopy(value)
        self.relation(relation_id).validate_outputs(candidate)
        if encode(candidate) != before:
            raise ValueError("output validator changed its input")

    def evaluate_relation(self, relation_id, inputs, context=None):
        self.validate(relation_id, inputs)
        candidate = deepcopy(inputs)
        before = encode(candidate)
        result = self.relation(relation_id).evaluate(candidate, deepcopy(context or {}))
        if encode(candidate) != before:
            raise ValueError("evaluator changed its input")
        self.validate_result(relation_id, result)
        return deepcopy(result)
