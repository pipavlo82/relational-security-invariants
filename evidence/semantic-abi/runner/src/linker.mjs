const TEMPORAL_FIELDS = ["issued_at", "verification_time"];

const temporalEntry = (claim) => {
  const present = TEMPORAL_FIELDS.filter((field) =>
    Object.prototype.hasOwnProperty.call(claim || {}, field));
  if (present.length !== 1) return null;
  return [present[0], claim[present[0]]];
};

const sameTemporalBoundary = (left, right) => {
  const a = temporalEntry(left);
  const b = temporalEntry(right);
  return a != null && b != null && a[0] === b[0] && a[1] === b[1];
};

const sameClaim = (left, right) => left?.claim_type === right?.claim_type;
const sameScope = (left, right) => left?.scope === right?.scope;

function authorityCompatible(established, required) {
  if (established?.authority_class === required?.authority_class) return true;
  return established?.authority_class === "INDEPENDENT_RECOMPUTATION"
    && required?.authority_class === "SEMANTIC_VERIFICATION"
    && sameClaim(established, required)
    && sameScope(established, required)
    && sameTemporalBoundary(established, required);
}

const claimCompatible = (established, required) =>
  sameClaim(established, required)
  && sameScope(established, required)
  && sameTemporalBoundary(established, required)
  && authorityCompatible(established, required);

const boundaryMatches = (boundary, required) =>
  boundary?.claim_type === required?.claim_type
  && boundary?.authority_class === required?.authority_class
  && boundary?.scope === required?.scope;

function mismatchDimensions(established, required) {
  if (established == null) return ["claim_type", "authority_class", "scope", "temporal_boundary"];
  const mismatches = [];
  if (!sameClaim(established, required)) mismatches.push("claim_type");
  if (!authorityCompatible(established, required)) mismatches.push("authority_class");
  if (!sameScope(established, required)) mismatches.push("scope");
  if (!sameTemporalBoundary(established, required)) mismatches.push("temporal_boundary");
  return mismatches;
}

function closestClaim(establishedClaims, required) {
  if (establishedClaims.length === 0) return null;
  return establishedClaims
    .map((claim, index) => ({
      claim,
      index,
      score: Number(sameClaim(claim, required))
        + Number(claim?.authority_class === required?.authority_class)
        + Number(sameScope(claim, required))
        + Number(sameTemporalBoundary(claim, required)),
    }))
    .sort((a, b) => b.score - a.score || a.index - b.index)[0].claim;
}

// Semantic linker: can the producer satisfy this exact claim-level consumer
// requirement? Authority is necessary but never sufficient by itself.
//
// producer: { component, establishes: EvidenceClaim[], does_not_establish?: NegativeClaimBoundary[] }
// requirement: { claim_type, authority_class, scope, issued_at | verification_time }
export function linkEdge(producer, requirement) {
  const establishedClaims = Array.isArray(producer?.establishes) ? producer.establishes : [];
  const match = establishedClaims.find((claim) => claimCompatible(claim, requirement));
  if (match) {
    return {
      valid: true,
      edge: { producer_claim: match, consumer_requirement: requirement },
    };
  }

  const explicitBoundary = (producer?.does_not_establish || [])
    .find((boundary) => boundaryMatches(boundary, requirement));
  const closest = closestClaim(establishedClaims, requirement);
  const mismatches = mismatchDimensions(closest, requirement);
  return {
    valid: false,
    error: "TYPE_ERROR",
    counterexample: {
      producer: producer?.component ?? "UNKNOWN_COMPONENT",
      producer_claim: closest,
      consumer_requirement: requirement,
      explicit_boundary_hit: explicitBoundary != null,
      explicit_boundary: explicitBoundary ?? null,
      reason: explicitBoundary
        ? "explicitly disclaimed by producer.does_not_establish"
        : "no compatible claim-level semantic edge exists",
      minimal_unsupported_semantic_upgrade: {
        from: closest,
        to: requirement,
        mismatched_dimensions: mismatches,
      },
    },
  };
}
