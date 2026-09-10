import { readFileSync } from "node:fs";
import { snapshotCounterfactualSemanticJson } from "../../evidence/crystal-receipt/counterfactual-audit-boundary.ts";
import { canonicalize } from "../../evidence/crystal-receipt/canonicalize.ts";
const inputs = JSON.parse(readFileSync(0, "utf8"));
const baseline = canonicalize(snapshotCounterfactualSemanticJson(inputs.baseline.semantic_artifact));
const candidate = canonicalize(snapshotCounterfactualSemanticJson(inputs.candidate.semantic_artifact));
process.stdout.write(JSON.stringify({baseline, candidate, baseline_outcome:"accepted_snapshot", candidate_outcome:"accepted_snapshot"}));
