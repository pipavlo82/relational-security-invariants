import test from "node:test";
import assert from "node:assert/strict";

import { linkEdge } from "../src/linker.mjs";

const established = {
  claim_type: "DETERMINISTIC_ACTION_RESULT",
  authority_class: "INDEPENDENT_RECOMPUTATION",
  scope: "action:demo-001/output",
  verification_time: "receipt.verified_at",
};

const producer = {
  component: "demo./verify",
  establishes: [established],
  does_not_establish: [{
    claim_type: "NONDETERMINISTIC_JUDGMENT_CORRECT",
    authority_class: "SEMANTIC_VERIFICATION",
    scope: established.scope,
    reason: "the judgment is not recomputable",
  }],
};

test("same authority but wrong claim is TYPE_ERROR", () => {
  const requirement = { ...established, claim_type: "DIFFERENT_ACTION_RESULT" };
  const result = linkEdge(producer, requirement);
  assert.equal(result.valid, false);
  assert.equal(result.error, "TYPE_ERROR");
  assert.deepEqual(result.counterexample.minimal_unsupported_semantic_upgrade.mismatched_dimensions, ["claim_type"]);
});

test("same claim and authority but incompatible scope is TYPE_ERROR", () => {
  const requirement = { ...established, scope: "action:demo-002/output" };
  const result = linkEdge(producer, requirement);
  assert.equal(result.valid, false);
  assert.equal(result.error, "TYPE_ERROR");
  assert.deepEqual(result.counterexample.minimal_unsupported_semantic_upgrade.mismatched_dimensions, ["scope"]);
});

test("valid claim plus authority plus scope edge passes", () => {
  const result = linkEdge(producer, { ...established });
  assert.equal(result.valid, true);
  assert.deepEqual(result.edge.producer_claim, established);
});

test("recomputation satisfies semantic verification only for its exact claim boundary", () => {
  const compatible = linkEdge(producer, { ...established, authority_class: "SEMANTIC_VERIFICATION" });
  assert.equal(compatible.valid, true);

  const wrongClaim = linkEdge(producer, {
    ...established,
    claim_type: "NONDETERMINISTIC_JUDGMENT_CORRECT",
    authority_class: "SEMANTIC_VERIFICATION",
  });
  assert.equal(wrongClaim.valid, false);
  assert.equal(wrongClaim.counterexample.explicit_boundary_hit, true);
  assert.deepEqual(wrongClaim.counterexample.minimal_unsupported_semantic_upgrade.mismatched_dimensions,
    ["claim_type", "authority_class"]);
});

test("temporal boundary mismatch is TYPE_ERROR", () => {
  const result = linkEdge(producer, { ...established, verification_time: "another.check_time" });
  assert.equal(result.valid, false);
  assert.deepEqual(result.counterexample.minimal_unsupported_semantic_upgrade.mismatched_dimensions,
    ["temporal_boundary"]);
});
