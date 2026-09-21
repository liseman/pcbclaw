# Installation and update validation

Use native Skill Workshop for authoring/publication. Read existing skill/support files first, preserve customizations and a retained revision/backup before updating. Existing pcb absent means create; do not silently shadow another name. Validate native structure with installed skill-creator/scripts/quick_validate.py, confirm live discovery using openclaw skills info/list/check (inspect --help), and apply/activate through native APIs appropriate to publication type. Plain "pcb" is model-discovered conversational routing, not a shell binary or guaranteed lexical interceptor. Do not claim an end-to-end chat test from static checks alone.

Run python3 scripts/test_helpers.py using the installed skill directory. It creates only temporary synthetic fixtures: no boards, exports, uploads or purchases. Run preflight for needed stage and inspect all required KiCad subcommands with --help. Verify defaults config is readable and preserves one-project precedence. Ensure each bundled reference resolves.

Conversation dry-run expectations:
- pcb → one short purpose/power/connection/size question, no long questionnaire or board creation.
- pcb ESP32 temperature logger powered by USB-C → preserve ESP32/logger/USB-C facts; ask consequential unknown sensor/logging/function/power details only, not already supplied facts; ask programming requirements.
- pcb 12V input with four independently controlled MOSFET outputs → preserve 12 V/count; ask load current/type/control levels and critical protection needs.
- pcb use four layers and ENIG for a small tracker → effective task override retains four layers/ENIG without changing user defaults; ask actual battery/radio/mechanical requirements.
- pcb modify <existing> <change> → inspect/save/backup, preserve correct work.
- pcb resume <existing> → status-guided continuation, no restart.
- pcb reprice <existing> → same BOM/design, refresh Economic eligibility/stock/costs only.
- pcb package <existing> → revalidate and automatically generate local manufacturing package; no separate local-export permission.
- Unknown LED rotation → local candidate REVIEW REQUIRED, not READY or universal rotation correction.
- Upload/quote requiring private BOM → separate authorization; public estimate remains possible.
- No Git author → backup and continue design/exports; commit pending.
- Economic ineligible → no silent service substitution.
- Unknown range → three categories with unknown quantities; no guessed range.
- Two valid quantities → unavailable distinct middle explicitly stated.
- Missing price element → unknown total with known subtotal, not zero.
- Stock shortage at service maximum → retain service maximum and flag fulfillment.

Routing helper fixtures test deterministic parsing/preserved text, not model interview intelligence. Inspect the skill's instruction contract against these expected responses; distinguish static/dry-run checks from a live next-turn invocation.

Coverage checklist: environment/setup; adaptive interview; editable defaults/precedence; architecture/calculations; JLCPCB parts/stock/classification; portable libraries; full pin/polarity mapping; preserved project/Git; supported efficient tooling/one computer owner; schematic/layout; actual ERC/DRC reports; Economic eligibility; automatic exports and cross-checks; final stock; Economic minimum/middle/maximum arithmetic; costs/unknowns; complete deliverables; resume/privacy boundaries. No inherited fixed schedule or unsolicited Standard comparison table should override the default Economic policy; explicit quantity/service requests must be honored.

Helpers use only Python standard library. Preflight is diagnostic, not a claim of environment completeness. Backup rejects unresolved symlinks, verifies contents and notices source changes. Packaging verifies a controlled staging tree; filename filters do not guarantee absence of secrets. BOM/CPL checker accepts normalized Designator/Quantity/LCSC BOM and Designator CPL, not a claimed live upload schema. Cost helper needs sourced verified inputs. Actual electrical/layout/export validation remains agent work.

## Revised workflow fixtures
- Request ten Standard assemblies after service approval → quote that quantity/service, do not re-ask or require Economic comparison.
- Requested WhatsApp updates → verify destination, preserve single writer, distinguish queued/running/saved/delivered.
- Repeated failed routing metric optimization → reassess reference design/topology/stackup, not another identical nudge.
- Supplier row matched but unchecked → select/verify exact authorized part before reporting full assembly price.
- Placeholder placement preview → retain manual review; never claim orientation signoff.
- Maximum soldering heat-resistance profile → do not reinterpret as mandatory minimum temperature.
- User requests only two revised cart items → verify new entries then remove only authorized obsolete/unrelated entries; no payment.
- First ordered request → tag exact designated source/assets and record user report versus verified order receipt.
- GitHub delivery → preserve visibility, verify assets, exclude account/project-private data from skill publication.
- Fully routed board with absent firmware → report hardware prototype and firmware absence, not working product.
These are static review fixtures, not executed live supplier transactions or physical tests.
