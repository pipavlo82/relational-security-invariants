# Post-v0 external blind semantic derivation protocol

Protocol version: `1.0`. Exercise: `CR-EXT-DERIVATION-001`.
`post_v0_protocol_base_commit`: `98e6f42b42b5d66ffb4fb99ea4c872c5bb2f5726`.
Immutable annotated `v0`: `8d8e31291ecf96284212a353efb66f606cff2953`,
tag object `c331f2f0beb0cee500629198926472fbeddc217e`.

This document prepares a post-v0 evidence exercise. It is not a completed
external reproduction, independent derivation, new relation admission, or a
revision of v0. No reviewer is appointed and no comparison is performed here.
All existing Crystal Receipt/H1/H2 results remain historical evidence.

## Evidence roles

| Role | Eligibility and responsibility | What it cannot establish |
|---|---|---|
| `STRICT_BLIND_DERIVER` | Fresh, unaffiliated external reviewer; receives only the source-only pack; derives the relation without the prior evaluator, frozen rows, research answers or comparison results; commits/hash-pins the derivation before reveal | Framework-wide independence, correctness solely from personal independence, or independence without an exposure record |
| `EXPOSED_REVIEWER` | Has had repository-level access to answer-bearing material, including a clone containing it; may reproduce results or review methodology | Strict blind derivation, even if they report not deliberately opening the files |
| `POST_COMMIT_VERIFIER` | Receives a derivation only after its immutable freeze; separately performs mechanical comparison against frozen observations/expectations and relevant third-leg evidence | Originating that blind derivation or becoming blind by waiting until comparison |

Baby Blue Viper is a **`POST_COMMIT_VERIFIER` candidate / NOT ELIGIBLE FOR
`STRICT_BLIND_DERIVER`** in this exercise. The owner reports that they cloned RSI
v0, so predictor and frozen-expectation files were present locally, although they
stated they did not deliberately inspect them. This is an owner-supplied exposure
record, not an independently observed inspection history or a claim of deliberate
answer use. Do not replace repository-level exposure with a zero-exposure claim.
Their comparison role has not yet been accepted or executed.

The pack preparer and coordinator have already inspected existing evidence and
are exposed. They cannot occupy the strict blind role for this round. A separate
implementation, language, account, repository or model session does not by itself
establish independent authorship. Unknown affiliations or exposure stay UNKNOWN.

## Claim discipline

**Mutation kills prove mapped decisions are load-bearing; they do NOT prove
independently derived semantic expectations.**

- v0 author independence remains **UNKNOWN**.
- Successful post-v0 work MUST NOT retroactively upgrade the v0 claim.
- One independently re-derived family does NOT imply framework-wide author independence.
- The current global wording remains **separately implemented expectation predictor**.
- An agreement can support a scoped external derivation claim only after role,
  exposure, chronology, source, submission and comparison evidence are complete.
- Disagreement is an evidence result, not grounds to coach the reviewer into the
  existing answer. Do not erase the first submission or selectively report cases.

## Exact source and question

Only the already admitted flat printable-ASCII string-object semantic-snapshot
subset is in scope. The source pin is `pipavlo82/crystal-receipt` at
`45b46bf7df3a60b32583291f577a36bf19d22f00`, verified against frozen RSI evidence
and exact external Git blobs. This is a historical pin, not a claim about the
current upstream main. No source checkout, branch or external artifact is changed.

Definition source: `conformance/counterfactual-audit-boundary-v0/SPEC.md`,
SHA-256 `9c17bd826c4a789464dab80c78a136153f3d9ce2f253198d0cf386bdef3a6d0b`.
Supply exact slices for Semantic input domain, Audit metadata domain and Reserved
field, without the source expected-outcome tables or result digest recipes.
Also supply byte-identical `src/receiptos/canon/canonicalize.ts`, SHA-256
`fca18d1642e6fe47d26ae2eb9f4bf15cf305653d6a7a08a5a0a09e2d6a716c81`.
These general source rules and operations are sufficient to derive the question
without an RSI-specific semantic definition. They are not a supplied case answer.

The input pairs contain only source JSON subtrees. Exact values are retained,
including source payload strings whose field name includes `expected`; those
strings are artifact data, not expectation rows. The coordinator-only registry
holds extraction selectors and the mapping to existing cases for later comparison.
No expected row, result, H2 deduction or solution code is copied into the pack.

Upstream input-container filenames themselves disclose classifications. They
must therefore not appear in pack paths, prose or source-pin metadata. Full input
extraction provenance is committed by SHA-256 and retained in the RSI registry
until reveal. The pack discloses this deliberate boundary: input-extraction
provenance is not independently checkable before reveal. This does not withhold
any semantic rule or input operand required for derivation. Original definition
and implementation paths/hashes, exact included bytes and input hashes are public
within the pack. Do not describe deferred provenance as already verified by the
reviewer. If a reviewer requires those selectors before derivation, stop this
round rather than reveal answer-bearing names and retain a blind classification.

Do not broaden into provenance authority, Lane K, wider ReceiptOS behavior,
Unicode/numeric/host-object semantics, or other families. The source canonicalizer
is supplied source evidence; its presence does not establish algorithm independence.

## Separate pack and distribution controls

The pack is its own Git repository, outside RSI, with neutral case identifiers,
one preparation commit and no inherited history. Intended remote:
`pipavlo82/crystal-receipt-semantic-snapshot-cleanroom`; it is not created or pushed
by this preparation. The actual local path and commit are in the registry.
The suggested `C:/Users/msi/dev/...` path was absent but outside this session's
writable roots; the separate repository is placed alongside RSI in `outputs/`.

Deliver only the exact pack commit or a verified archive of it. Do not distribute
this protocol, the registry, coordinator mapping, RSI checkout, sibling folders,
H1/H2 reports or this conversation to the strict reviewer before freeze. Do not
add a link from the pack to answer-bearing RSI material. A public source pin is
not a permission to browse excluded upstream vectors before submission.

Before recruitment, verify:

1. The candidate has no relevant prior clone, source/result review, correspondence
   or collaboration that compromises this exercise. Record affiliations, account
   ownership and an explicit exposure statement; identity/affiliation evidence
   is distinct from a self-attestation.
2. The working directory, environment and any assistant/model session are fresh:
   no loaded prior conversation, retrieval index, mounted RSI tree or reference
   outputs. Log tools, collaborators and model assistance. A model's pretraining
   history is not knowable from a fresh session; undisclosed or uncertain relevant
   exposure must not be certified as absent.
3. The candidate agrees not to search for RSI/current reports or excluded source
   vectors before freeze. Public availability prevents a technical proof of zero
   exposure; strict classification remains a documented protocol/attestation
   claim, not an omniscient guarantee about knowledge.
4. Identity, unaffiliated status and exposure are accepted before distribution.
   Until then status is `AWAITING_STRICT_BLIND_REVIEWER`; preparation alone cannot
   satisfy external author-independence evidence.

Any disqualifying exposure moves the candidate to `EXPOSED_REVIEWER` for this
round. Do not reset the same reviewer by creating another account/session. Obtain
a genuinely fresh reviewer. No reviewer outreach or message is sent by this task.

## Submission and reveal order

1. Freeze the prepared pack commit, `HASHES.sha256` digest, source closure and
   coordinator input-origin commitment. Preserve all versions; do not amend a
   distributed pack. A material correction requires a new version/round.
2. The fresh reviewer receives only that pack and creates `DERIVATION.json` with
   one `PRESERVED | VIOLATED | UNVERIFIABLE` state per case, source references,
   derivation, assumptions, identity, exposure statement and tool provenance.
3. Freeze its exact Git commit and SHA-256 over the submitted derivation bytes,
   plus any derivation code. A hash alone establishes content, not identity or
   time. Record an independently witnessed receipt/acknowledgment before reveal;
   self-authored Git timestamps alone are not ordering evidence. Verify any
   signatures actually supplied rather than inferring authenticity from presence.
4. Append the immutable submission event to the registry. Verify its pack binding
   and complete case inventory before any answer-bearing disclosure.
5. Only then reveal the exact pre-existing v0 expectation artifact, its digest,
   the committed input-origin record and mapping. Independently check the record's
   digest against the commitment already in the pack. Pin a reveal commit and
   timestamped disclosure record. No earlier side-channel hints or answer coaching.
6. A `POST_COMMIT_VERIFIER` separately compares the frozen derivation with v0's
   admitted expectations and actual adapter observation, and H2 where applicable.
   Use the pinned generations; independently inspect the case mapping and require
   a one-to-one inventory. No ID-based assumption of the expected outcome.
7. Freeze the comparison code/commands, environment, exact input/output hashes,
   comparison commit and all agreements/disagreements. Keep invalid submission,
   inability to derive, execution error and semantic disagreement distinct. Missing
   cases or malformed output are not agreement. These exercise states do not alter
   RSI PASS/FAIL or mutation taxonomy.
8. Add comparison evidence to post-v0 RSI only. Retain first submissions and later
   revisions as distinct events. Never rewrite v0 or generalize one-family success.

No steps involving a reviewer, submission, reveal or comparison have occurred in
this preparation. Reviewer identity, derivation, reveal and comparison pointers
must remain null until evidenced.

## Append-only registry

`external-derivation-registry.json` uses stable exercise IDs and immutable events.
The initial snapshot records preparation. Append subsequent events with increasing
sequence numbers and `previous_event_sha256` over the prior event's deterministic
JSON bytes; do not backfill nulls or rewrite the preparation record. Every event
names the exact pack/source version it concerns. Current state is a projection
of the latest validated event, not an edit to historical fields.

Event/record JSON serialization: UTF-8, `ensure_ascii=True`, sorted keys, two-space
indentation, one trailing LF. This is a specified serialization recipe, not a
claim of full JCS. Hash raw bytes with SHA-256. A Git commit anchors the registry;
no file includes a self-referential digest. Verify event ordering/content and
external submission evidence; a registry entry is not authority merely by presence.

## Leakage and non-interference gates

Audit the entire pack payload, filenames and first-commit history. Search for
`predictor`, `expectation`, `H2`, `COMMON_MODE`, `PASS`, `FAIL`, `preserved`,
`violated`, `expected`, `mutation`, `crystal_receipt.py`, old case IDs and current
verdict text. Review every hit; allow only neutral task vocabulary, exclusion
instructions, verbatim general source rules and exact opaque input data. Do not
allow case-assigned states or upstream answer-bearing filenames. Compare pack
administrative prose with prior reports; source excerpts are separately attributed.
Keep detailed audit findings and coordinator mappings in RSI, not the pack.

Pack hashing excludes `HASHES.sha256` from its own list and binds that file by
the pack commit plus a separately recorded SHA-256. `PACK_MANIFEST.json` lists
all payload files except itself and HASHES; HASHES includes PACK_MANIFEST. All
other payload files, including the neutral leakage audit, are covered. No build
script, hidden state, earlier Git history or solution is shipped.

For RSI, compare every pre-protocol tracked file hash to the verified base, run
the normal/optimized current baseline and complete conformance, and run mutation
gates where practical. Only this protocol and the registry are added. No existing
Crystal results, H1/H2 evidence, source maps, core semantics or tag are changed.
Separate local commits are required. No push occurs before both local audits and
the final report; later publication/reviewer distribution is a separate action.
