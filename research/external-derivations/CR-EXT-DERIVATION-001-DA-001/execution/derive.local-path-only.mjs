// Clean-room derivation harness for the Crystal Receipt semantic-snapshot pack.
// Uses ONLY the supplied source-material/canonicalize.ts (serialization) and the
// prose rules in source-material/semantic-domain.md. No external repo or prior
// solution is consulted.
//
// canonicalize() below is a byte-faithful port of source-material/canonicalize.ts
// (sha256 fca18d1642e6fe47d26ae2eb9f4bf15cf305653d6a7a08a5a0a09e2d6a716c81):
// the ONLY edits are removal of TypeScript type-only syntax
//   ": unknown"  and  "as Record<string, unknown>"  and  "export "
// which have no runtime effect. Logic (Object.keys -> filter undefined -> sort
// -> "key":canonicalize(value), joined by ",") is identical.

import { readFileSync } from "node:fs";

function canonicalize(value) {
  if (value === null || typeof value !== "object") {
    return JSON.stringify(value);
  }

  if (Array.isArray(value)) {
    return `[${value.map(canonicalize).join(",")}]`;
  }

  const record = value;
  const entries = Object.keys(record)
    .filter((key) => record[key] !== undefined)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${canonicalize(record[key])}`);

  return `{${entries.join(",")}}`;
}

// Reserved-field rule (semantic-domain.md): "audit_timestamp" is forbidden at
// EVERY object depth INSIDE semantic artifact input; presence => malformed =>
// MUST be rejected (naming the inspection path). It MAY exist OUTSIDE the
// semantic artifact (e.g. in the enclosing manifest) and MUST NOT affect
// semantic identity. This walks the semantic_artifact subtree only.
function findReservedInside(value, path) {
  const hits = [];
  if (value === null || typeof value !== "object") return hits;
  if (Array.isArray(value)) {
    value.forEach((v, i) => hits.push(...findReservedInside(v, `${path}[${i}]`)));
    return hits;
  }
  for (const key of Object.keys(value)) {
    const child = `${path}.${key}`;
    if (key === "audit_timestamp") hits.push(child);
    hits.push(...findReservedInside(value[key], child));
  }
  return hits;
}

const uploads = "C:/Users/msi/Documents/Codex/2026-09-09/files-pasted-by-the-user-create/outputs/crystal-external-comparison-2026-09-13/pack";
const files = ["case-001", "case-002", "case-003", "case-004"];

const ACCEPTED_SCALARS = new Set(["boolean", "number", "string"]); // + null
function scalarsOk(value, path, bad) {
  if (value === null) return;
  const t = typeof value;
  if (t === "object") {
    if (Array.isArray(value)) value.forEach((v, i) => scalarsOk(v, `${path}[${i}]`, bad));
    else for (const k of Object.keys(value)) scalarsOk(value[k], `${path}.${k}`, bad);
    return;
  }
  if (!ACCEPTED_SCALARS.has(t)) bad.push(`${path} (${t})`);
  if (t === "number" && !Number.isFinite(value)) bad.push(`${path} (non-finite number)`);
}

const results = [];
for (const id of files) {
  const raw = readFileSync(`${uploads}/inputs/${id}.json`, "utf8");
  const doc = JSON.parse(raw);
  const rec = {};
  for (const side of ["left", "right"]) {
    const sa = doc[side].semantic_artifact;
    const mf = doc[side].manifest;
    const reserved = findReservedInside(sa, "$semantic_artifact");
    const badScalars = [];
    scalarsOk(sa, "$semantic_artifact", badScalars);
    rec[side] = {
      accepted: reserved.length === 0 && badScalars.length === 0,
      reserved_hits: reserved,
      bad_scalars: badScalars,
      snapshot: reserved.length === 0 ? canonicalize(sa) : null,
      manifest_canon: canonicalize(mf),
      manifest_has_audit: Object.prototype.hasOwnProperty.call(mf, "audit_timestamp"),
      manifest_audit_value: mf.audit_timestamp ?? null,
    };
  }
  const bothAccepted = rec.left.accepted && rec.right.accepted;
  const snapshotsEqual = rec.left.snapshot !== null && rec.left.snapshot === rec.right.snapshot;
  let state;
  if (!bothAccepted) state = "UNVERIFIABLE(rejection-asymmetry-or-malformed)";
  else if (snapshotsEqual) state = "PRESERVED";
  else state = "VIOLATED";
  results.push({ id, state, snapshotsEqual, bothAccepted, rec });
}

for (const r of results) {
  console.log("=".repeat(72));
  console.log(`${r.id}  =>  ${r.state}`);
  console.log(`  semantic snapshots equal? ${r.snapshotsEqual}   both accepted? ${r.bothAccepted}`);
  console.log(`  left .semantic snapshot : ${r.rec.left.snapshot}`);
  console.log(`  right.semantic snapshot : ${r.rec.right.snapshot}`);
  console.log(`  left  manifest canon    : ${r.rec.left.manifest_canon}  (audit=${r.rec.left.manifest_has_audit}:${r.rec.left.manifest_audit_value})`);
  console.log(`  right manifest canon    : ${r.rec.right.manifest_canon}  (audit=${r.rec.right.manifest_has_audit}:${r.rec.right.manifest_audit_value})`);
  console.log(`  reserved-inside-sa hits : left=${JSON.stringify(r.rec.left.reserved_hits)} right=${JSON.stringify(r.rec.right.reserved_hits)}`);
}
console.log("=".repeat(72));
