# Design and verification detail

## Requirements before CAD
Extract supplied facts verbatim where useful. Ask only consequential unknowns, grouped in a few related questions per turn: purpose; input voltage range/source; output voltage/current/load including transients; interface levels/protocols; connector types/pinouts; batteries/charging; envelope/mounts/enclosure; environment/reliability/safety/isolation; mandatory parts; firmware/programming/debug expectations. If size is unconstrained choose a practical service-compatible size. Critical unknowns are not assumptions. Confirm unresolved consequential choices; do not ask for repeated approval on agreed implementation.

requirements.md records function, inputs/outputs, interfaces, connectors/pinouts, mechanics, environment, safety, programming, manufacturing, overrides, assumptions and open questions. status.json records current stage, completed/pending steps, blockers, last saved artifacts, exact validation results, next action and timestamp. Preserve known progress after timeout. Record effective defaults separately for auditability.

## Architecture/calculations
Before CAD plan applicable protection (reverse polarity, fuse/overcurrent, ESD/surge), regulation/filtering, processors/clocking, sensors, radio/antenna keepouts, drivers/switching, connectors, programming/debug, decoupling, test points and indicators. Calculate worst-case supply/current/power budget, losses/thermal rise, resistor power, component voltage/current stresses, signal-level margins, battery operating range, trace capacity and safety clearance. Use manufacturer application guidance, distinguish estimates from guaranteed bounds and identify prototype tests.

## Component verification table
One row per reference, with distinct-part evidence reusable across rows:
Reference, Function, Value, Manufacturer, MPN, LCSC, Package, KiCad symbol, KiCad footprint, Important ratings, Assembly classification, Availability, Pricing source, Datasheet source, Verification timestamp, Verification status.
Also retain stock quantities, tier prices/currency, MOQ, attrition assumptions, service eligibility and physical terminal mapping in supporting evidence.

Verify exact manufacturer MPN in authoritative datasheet. Record provenance if distributor hosts the manufacturer PDF. Check ratings/derating at actual operating conditions, body/lead dimensions, land pattern, pin count/function, temperature, soldering process and handling requirements. A matching 0603 label or plausible library name is not verification. Prefer standard KiCad libraries when correct. Local custom libraries/tables and required 3D/model dependencies must be portable; verify on a clean/copy path without unresolved libraries.

Check JLCPCB assembly catalog for the selected service (LCSC listing alone insufficient), current stock/sourcing, classification including time-limited fee waivers, price breaks, purchased quantity/extra components. Never invent numbers, specs, prices or stock. When inaccessible, preserve uncertainty. Do not silently use outside parts or Standard service to finish. Substitution changing requirements needs user decision and full revalidation.

## Pin/footprint/orientation
Prove electrical function → symbol pin → footprint pad → physical terminal including dimensions, pitch, drill/slots, land geometry, orientation mark, origin and rotation. Check connectors, MOSFET G/D/S, IC pin 1, polarized capacitors, LEDs/diodes. Numbering may differ without an error; do not renumber working connectivity just to match numbers.

For KT-0603R/C2286 only when actually selected: re-read its current manufacturer drawing. Known reference mapping is manufacturer 1=A/2=K versus KiCad Device:LED 1=K/2=A; physical cathode goes to KiCad cathode pad, not matching numeric terminal. Verify physical cathode mark, top/bottom drawing and expected board direction. This example is not a universal correction. No guessed blanket CPL offsets. Verify exporter conventions, origin, side, manufacturer tape orientation and exact supplier part model where accessible. Distinguish local geometric verification from actual JLCPCB preview; record unresolved offset as REVIEW REQUIRED.

## CAD
Use filesystem-safe short project names under ~/pcb-projects. Inspect existing files/editor state; checkpoint before consequential changes. Missing Git identity means timestamped verified backup, not blocked design. Never initialize an invented author or push.

Create complete schematic including supporting circuits, annotate, verify footprint assignment, populate Manufacturer/MPN/LCSC. Pin-critical custom work must be independently checked. Run ERC and fix legitimate errors/warnings.

For ordinary low-voltage two-layer starting targets: 0.25 trace, 0.20 clearance, 0.60/0.30 via, minimum 0.15 trace/clearance, 0.50 edge, all mm. These are preferences, not fabricator limits or voltage-safety/impedance/high-current calculations. Verify current service constraints.
Place mechanics/connectors, critical circuits/power, decoupling, flow, thermal, then remaining parts. Keep switching loops compact, bypass capacitors close, adequate return paths/ground continuity, suitable current widths, assembly spacing/access and antenna keepouts. Route all required nets, refill zones, save.

## Independent review and service
Use KiCad CLI help to select supported all-severity/failure/parity options, read actual ERC/DRC reports. Targets: no errors, unexplained warnings or unintended unconnected items. Justified exceptions must remain visible. Verify connectivity parity, power/polarity, ratings/calculations, actual pad geometry, orientation, size/outline/mounts, edge clearances, readable silk and mask/paste. Inspect saved rendered outputs when useful. A file timestamp, nonzero size or zero CLI exit does not prove correctness.

Verify current Economic PCBA rules before finalizing: layers, sides, packages, THT, size, heights, rails/panels, valid order quantities, finishes/options. Do not hardcode service limits from memory. Explain incompatibilities and practical alternatives; ask before consequential changes or service switch. Component catalog presence is not service eligibility. Distinguish verified design from functionality requiring a powered prototype.
