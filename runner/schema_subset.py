"""Fail-closed evaluator for the explicitly documented v0 JSON Schema subset.

This is NOT a general JSON Schema implementation. The shipped schema is standard
Draft 2020-12 JSON Schema; unsupported schema keywords/shapes are rejected.
"""
import json
import re


class Invalid(ValueError):
    pass


KEYWORDS = {"$schema", "title", "description", "type", "properties", "required", "additionalProperties", "items", "minItems", "uniqueItems", "enum", "const", "oneOf", "pattern", "minimum", "minLength"}
TYPES = {"object": dict, "array": list, "string": str, "integer": int, "boolean": bool}


def load(path):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                raise Invalid("duplicate JSON key: " + k)
            result[k] = v
        return result
    def bad_constant(value):
        raise Invalid("non-JSON number: " + value)
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs, parse_constant=bad_constant)


def check_schema(s):
    if type(s) is not dict or not s or set(s) - KEYWORDS:
        raise Invalid("unsupported schema shape/keyword")
    for name in ("$schema", "title", "description", "pattern"):
        if name in s and type(s[name]) is not str:
            raise Invalid("invalid schema " + name)
    if "$schema" in s and s["$schema"] != "https://json-schema.org/draft/2020-12/schema":
        raise Invalid("unsupported schema dialect")
    if "type" in s and (type(s["type"]) is not str or s["type"] not in TYPES):
        raise Invalid("unsupported schema type")
    allowed_for = {
        "object": {"properties", "required", "additionalProperties"},
        "array": {"items", "minItems", "uniqueItems"},
        "string": {"pattern", "minLength"},
        "integer": {"minimum"},
    }
    structural = set().union(*allowed_for.values())
    if (set(s) & structural) - allowed_for.get(s.get("type"), set()):
        raise Invalid("schema keywords applied to unsupported type")
    if s.get("type") == "object" and not {"properties", "required", "additionalProperties"} <= set(s):
        raise Invalid("v0 object schema must explicitly close its shape")
    if s.get("type") == "array" and "items" not in s:
        raise Invalid("v0 array schema requires items")
    if not {"type", "oneOf", "enum", "const"} & set(s):
        raise Invalid("schema must constrain its value")
    if "oneOf" in s:
        if type(s["oneOf"]) is not list or not s["oneOf"]:
            raise Invalid("invalid oneOf")
        for branch in s["oneOf"]:
            check_schema(branch)
    if "properties" in s:
        if type(s["properties"]) is not dict or s.get("type") != "object" or s.get("additionalProperties") is not False:
            raise Invalid("v0 objects must be closed")
        for value in s["properties"].values():
            check_schema(value)
    if "required" in s:
        r = s["required"]
        if type(r) is not list or any(type(k) is not str for k in r) or len(r) != len(set(r)) or not set(r) <= set(s.get("properties", {})):
            raise Invalid("invalid required")
    if "additionalProperties" in s and s["additionalProperties"] is not False:
        raise Invalid("unsupported additionalProperties")
    if "items" in s:
        check_schema(s["items"])
    for name in ("minItems", "minimum", "minLength"):
        if name in s and (type(s[name]) is not int or s[name] < 0):
            raise Invalid("invalid " + name)
    if "uniqueItems" in s and type(s["uniqueItems"]) is not bool:
        raise Invalid("invalid uniqueItems")
    if "enum" in s and (type(s["enum"]) is not list or not s["enum"]):
        raise Invalid("invalid enum")
    if "pattern" in s:
        try:
            re.compile(s["pattern"])
        except re.error as exc:
            raise Invalid("invalid pattern") from exc


def equal(a, b):
    # JSON equality distinguishes booleans from numbers.
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def validate(value, s, path="$"):
    def require(condition, why):
        if not condition:
            raise Invalid(path + ": " + why)
    if "oneOf" in s:
        matches = 0
        for branch in s["oneOf"]:
            try:
                validate(value, branch, path)
                matches += 1
            except Invalid:
                pass
        require(matches == 1, "must match exactly one supported structural shape")
    if "type" in s:
        require(type(value) is TYPES[s["type"]], "expected " + s["type"])
    if "const" in s:
        require(equal(value, s["const"]), "wrong constant")
    if "enum" in s:
        require(any(equal(value, item) for item in s["enum"]), "unknown value")
    if type(value) is dict:
        require(set(s.get("required", [])) <= set(value), "missing required field")
        if s.get("additionalProperties") is False:
            require(set(value) <= set(s["properties"]), "unknown field")
        for k, v in value.items():
            if k in s.get("properties", {}):
                validate(v, s["properties"][k], path + "." + k)
    if type(value) is list:
        require(len(value) >= s.get("minItems", 0), "too few items")
        if s.get("uniqueItems"):
            require(len({json.dumps(x, sort_keys=True) for x in value}) == len(value), "duplicate items")
        for i, item in enumerate(value):
            if "items" in s:
                validate(item, s["items"], path + "[" + str(i) + "]")
    if type(value) is str:
        require(len(value) >= s.get("minLength", 0), "too short")
        if "pattern" in s:
            require(re.search(s["pattern"], value) is not None, "pattern mismatch")
    if type(value) is int and "minimum" in s:
        require(value >= s["minimum"], "below minimum")
