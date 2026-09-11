import { sha256, stringToBytes } from 'viem'

/**
 * Compute the raw proposal hash for a JudgmentExecutionAttestation (L4).
 *
 * ERC-8299 "L4 Judgment validator binding": rawProposalHash = sha256(artifact).
 *
 * Unlike the base WYRIWE triple-hash (L1-L3, keccak256-based — see recompute.ts),
 * the L4 layer is designed to anchor off-chain (Nostr-relay-published) verdicts as
 * well as on-chain ones, so it uses sha256 over the raw artifact string directly —
 * matching invinoveritas's reference implementation (services/proof_signing.py:
 * `artifact_hash = sha256(artifact)`), not the EVM-native keccak256 the L1-L3
 * layer uses for its on-chain contract calls.
 *
 * @param artifact - The exact proposed-action text as submitted for review (a
 *   diff, command, plan, etc. — whatever string the producer reviewed).
 * @returns The 32-byte sha256 hash of the UTF-8 artifact bytes, 0x-prefixed.
 */
export function computeRawProposalHash(artifact: string): `0x${string}` {
  return sha256(stringToBytes(artifact))
}

/**
 * Compute the verdict hash for a JudgmentExecutionAttestation (L4).
 *
 * ERC-8299 "L4 Judgment validator binding": verdictHash binds the verdict metadata
 * to rawProposalHash so a verdict cannot be replayed against a different proposal
 * than the one it judged ("verdict-shopping"). invinoveritas's reference
 * implementation computes this as `decision_ref = sha256(JCS({preimage fields}))`
 * over a fixed, sorted set of named fields — NOT `keccak256(verdict_event_id ||
 * rawProposalHash)` as a literal byte-concatenation. JCS (RFC 8785: sorted keys,
 * no extraneous whitespace, literal UTF-8 — NOT \\uXXXX-escaped) so the preimage
 * bytes recompute identically across implementations/languages.
 *
 * `fields` MUST include `raw_proposal_hash` (or whatever preimage field pins the
 * proposal) among `preimageFields` if the producer wants the anti-replay binding;
 * this function does not hardcode a specific field set — pass the producer's own
 * `decision_ref_preimage_fields` (published on each proof) so a recompute matches
 * the policy version that was actually in force when the verdict was issued.
 *
 * @param fields - The verdict's named metadata fields (string | null values).
 * @param preimageFields - Which keys of `fields` to include, in any order (they
 *   get sorted before hashing regardless).
 * @returns `sha256:<hex>` — matching invinoveritas's `decision_ref` format.
 */
export function computeVerdictHash(
  fields: Record<string, string | null>,
  preimageFields: readonly string[],
): string {
  // JCS/RFC-8785 requires CODE POINT order. Array.prototype.sort() compares UTF-16 code
  // units, which differs for any key above U+FFFF (a surrogate pair sorts below U+E000-
  // U+FFFF characters) — that divergence produced a different hash than the Python port
  // on the same input. Compare by code point explicitly. (cross-lane vector:
  // testkit/vectors/erc8299-l4.vectors.json, step 8299-l4/verdict-hash key-sort case)
  const cp = (s: string) => Array.from(s).map((c) => c.codePointAt(0)!)
  const sortedKeys = [...preimageFields].sort((a, b) => {
    const A = cp(a), B = cp(b)
    for (let i = 0; i < Math.min(A.length, B.length); i++) {
      if (A[i] !== B[i]) return A[i] - B[i]
    }
    return A.length - B.length
  })
  const parts = sortedKeys.map(
    (k) => JSON.stringify(k) + ':' + JSON.stringify(fields[k] ?? null),
  )
  const canon = '{' + parts.join(',') + '}'
  return 'sha256:' + sha256(stringToBytes(canon)).slice(2)
}
