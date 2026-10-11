# Licensing scope

The Apache License, Version 2.0, reproduced in [LICENSE](LICENSE), applies to
Pavlo-authored repository material within the scope below, to the extent Pavlo
owns or is authorized to license the relevant rights.

Copyright 2026 Pavlo Tvardovskyi

Existing third-party copyright, license, patent, attribution and trademark
notices remain applicable. For mixed or adapted material, the new grant covers
only Pavlo's original additions. Imported source, external contributions,
quoted specifications, captures and other third-party material are not
relicensed by this grant. Inclusion in this repository or a missing license
does not itself supply permission. Existing grants are not withdrawn or narrowed.

## Repository-authored material

The grant covers Pavlo-authored RSI code in `rsi/`, `runner/`, `adapters/`,
`profiles/`, `extensions/`, `tools/`, `tests/` and `reproducers/`; original
contracts and schemas in `spec/` and `schema/`; original synthetic fixtures,
corpora, oracle records and `manifest.json`; repository configuration, and
Pavlo-authored documentation and analysis in the root and `research/`.
Any embedded quotations, imported source or separately attributed portions
within those paths retain their original rights.

## Preserved material

| Path or scope | Preserved licensing and provenance boundary |
| --- | --- |
| `evidence/**` | Pinned upstream source, dependency notices, supplied artifacts and captures are excluded from the new blanket grant. Each `source-pin.v0.json` and corresponding `research/*source-map*.json` records the copied paths and exact source identities. Pavlo's original local glue remains distinguishable from those copies. |
| `evidence/semantic-abi/` | Keep the included root license and `schema/LICENSE-CC0.txt`; do not replace either with this root grant. |
| `evidence/verify-layer/`, `evidence/tas/`, `evidence/aggregate/`, `evidence/capv/`, `evidence/consult-escrow/` | Preserve included LICENSE files, `dependency-licenses/`, `THIRD_PARTY_LICENSES.txt`, SPDX headers, package metadata and source pins. |
| Other evidence families (`crystal-receipt`, `judgment`, `pq`, `rvr`, `tsei`) | Original upstream rights and per-file grants apply; a missing bundled grant is not resolved by this LICENSE. |
| `research/external-derivations/**`, `research/external-verifications/**` | Third-party submissions, correspondence, captures and their embedded content are excluded; existing permission and attribution requirements remain applicable. |
| Quoted specifications, source excerpts, addresses, signatures and supplied proof/data records elsewhere | No ownership or new rights are inferred from storage or reproduction. Existing source records and notices remain authoritative. |

External repositories are references only; this change licenses no external
repository. Dependency installation remains subject to each dependency's terms.

## Historical records and locks

This is the owner's current licensing decision for eligible first-party
material on the maintained branch. Earlier pending-license statements in
historical design/reconciliation reports describe the earlier state and are
superseded by this document for the maintained tree. The `v0` tag, frozen
reports, third-party bytes, evidence/source maps and their technical pins are
unchanged; no historical artifact is rewritten or assigned new semantics.
The root LICENSE and README changes, and the checker/test transitions needed
to admit them, are recorded as exact before/after digests in the existing
post-v0 maintenance mechanism. Unknown byte changes remain rejected. Frozen
baseline manifests and technical source identities are not repinned.
