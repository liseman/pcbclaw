# Release generation and delivery

## Authorization and readiness
Normal pcb invocation authorizes safe setup, local CAD/research/verification, automatic local manufacturing exports after successful design validation, local packaging and public-data cost estimates. No second permission is needed to generate files. Uploading a private PCB/BOM, repository publication, purchases/payment/reservations or other chargeable action need separate explicit authorization. Do not overwrite credentials or include secrets in artifacts.

Three statuses:
- READY FOR JLCPCB UPLOAD: local source and all generated files are verified, selected service eligible and no unresolved critical design/manufacturing questions. This means ready for upload review, NOT production approval.
- REVIEW REQUIRED: useful local candidate bundle exists but a sourcing, eligibility, pricing or orientation issue still needs review; identify exact uncertainty. Unknown critical costs/stock cannot be presented as orderable.
- BLOCKED: a critical electrical, footprint or manufacturing issue prevents a trustworthy package; preserve artifacts and exact next action.

Supplier upload preview/feedback is checked only after authorized upload, and before ordering. A merely unvisited future preview is not a claim of failure in otherwise proven local geometry; an actually unknown part rotation is REVIEW REQUIRED. Never claim preview verification that did not occur. Preserve previous release review evidence; hash-bind final files, invalidate stale orientation review on source/exporter/BOM/CPL changes. Do not apply guessed universal rotations or bypass real unresolved mapping just because a script passes.

## Export
Inspect installed kicad-cli help for sch export pdf and pcb export gerbers, drill, pos and supported BOM export. Choose actual supported options; do not use imaginary flags. Native output schemas are not automatically JLCPCB schemas: verify current official BOM/CPL requirements and map fields explicitly. Select correct fitted references/quantities and units/side/origin. Preserve rich source metadata while producing accepted minimal upload schema.

Make manufacturing/<version-or-UTC-release>/ with:
- fabrication/ copper, mask, paste, silk and Edge.Cuts Gerbers as appropriate; plated/nonplated drills as applicable
- fabrication.zip containing only relevant fabrication inputs, suitable for the Gerber upload field
- BOM.csv and CPL.csv separately accessible
- schematic.pdf
- fabrication-notes.md and assembly-notes.md including orientation mapping
- top/bottom assembly previews where practical (mark absent/inapplicable honestly)
- ERC/DRC reports and components verification evidence
- costs.csv, costs.md
- release-checklist.md with status, unresolved items and source/export versions
- source.zip with editable KiCad project, local symbols/footprints, library tables, requirements/status and needed dependencies
- manifest with content hashes and complete-delivery.zip containing fabrication ZIP, BOM/CPL, documentation/reports and source archive

Never silently include personal/global credentials, logs with secrets, old backups, editor caches or unrelated files. Enumerate intended deliverables; validate archives by reading them, not just checking size. Source archive must not recursively contain manufacturing/ and complete delivery must not contain itself. Prefer controlled staging folders and checked file lists. Do not export Gerbers during skill installation tests.

## Cross-check generated outputs
Review actual Gerbers/drill data with a reliable viewer/validator: correct copper count, mask/paste/silk, closed correct-sized outline, drill types/positions, scaling/mirroring. Verify CPL origin/units/board side/rotations align with the design and assembly preview. Verify unique reference designators, fitted BOM/CPL sets, quantities per board, exclusions/DNP, mounting holes/fiducials and separately handled THT components. Missing THT in an SMT-only position export is not implicitly okay.
Run helpers on normalized CSV copies if current upload headers differ; retain the accepted upload files unchanged. A reference-set cross-check alone does not verify geometry or valid sourcing. Recheck current stock, allow quantities for spares/MOQ and mark limitations. Any substituted part must be verified and all affected reports/exports regenerated.

## Final response format
PROJECT
Name:
Purpose:
Project path:

DESIGN
Board dimensions:
Layers:
Input:
Outputs/interfaces:
Important assumptions:

VERIFICATION
ERC:
DRC:
Unconnected items:
Electrical review:
Footprint/polarity review:
JLCPCB eligibility:
Part availability:
Remaining prototype tests:

MANUFACTURING
Release status:
Fabrication options:
Assembly service:
Gerber ZIP:
BOM:
CPL:
Schematic PDF:
Reports:
Source archive:
Complete delivery bundle:

ECONOMIC PCBA COSTS
Use references/costs.md exact three category table.

ASSUMPTIONS AND LIMITATIONS
Pricing timestamp:
Shipping/tax treatment:
Stock not reserved:
Programming requirements:
Remaining concerns:

Provide actual tool-supported attachments or working download links. If unavailable give exact existing filesystem paths and the retrieval method actually supported (for example the shared filesystem); never fabricate an HTTP link. Explain fabrication.zip belongs in the Gerber upload field; complete-delivery.zip is an archival delivery bundle, not necessarily an accepted Gerber upload.

## Failure/resume
Record status on each saved milestone and error. After timeout inspect saved files, open editor state and exact error; never infer completed work from timestamps. Preserve good work, isolate repeated failure and use another documented deterministic method if practical. Avoid duplicate long runs. Ask only for the specific missing information/authorization that blocks remaining work.

## Delivery verification
A Markdown link to a local absolute path is not evidence of a remote download. Use only a supported attachment or download mechanism and verify the served bytes/hash when the tooling permits. Distinguish server-side verification from recipient confirmation; if downloads are unverified, say so and provide the existing path and a supported retrieval route. Never expose a public file server or publish private files merely to repair delivery.

## Ordering confidence and stage-specific summaries
Answer readiness directly using evidence: local checks completed; supplier acceptance pending/received; firmware readiness; physical validation pending/passed. Do not say simply "done" or "ready to order" when a known critical issue remains. User acceptance of prototype risk is not engineering sign-off. A local review bundle can be complete while production remains pending. Keep routine updates concise; use the full final report when delivering a design, not for every status question. Follow references/supplier.md for authorized cart/review work and references/github-delivery.md for publishing/delivery.
