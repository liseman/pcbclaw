# Economic PCBA cost policy

Provide exactly three comparison categories: MINIMUM, MIDDLE, MAXIMUM. No fixed-quantity schedule and no separate Standard PCBA table. An explicit user change can override pricing service; never silently switch it. If Economic is ineligible, show its pricing unavailable rather than substituting another service.

Determine actual currently valid Economic assembled finished-board quantities for the selected design/options from official JLCPCB information and the quotation interface when accessible and authorized. Record source/time and verified versus unknown. Do not assume every integer or infer valid endpoints from memory. Select smallest and largest permitted quantities; select the permitted quantity nearest (minimum+maximum)/2, ties lower. If fewer than three distinct values exist, retain three category rows but mark the unavailable distinct MIDDLE not applicable and explain. If range is unknown, keep category quantities unverified/unknown, not guesses. Stock shortage does not redefine the service maximum; flag fulfillment/cost limitations separately.

Distinguish requested finished boards, PCBs fabricated, boards assembled, panels and boards/panel. Include required fabrication MOQ and panelization to obtain the assembled quantity. Use identical electrical design/BOM and declared manufacturing options for all rows; document any quantity-specific requirement.

Calculate required purchased component quantities from fitted pieces per board, verified spare/attrition allowance, package/order multiples and MOQ. Apply the corresponding actual purchase-price tier, not merely the assembled quantity. Recheck stock for all tiers before final delivery; timestamp exact MPN/LCSC/service. Stock is not reserved. Do not imply a maximum row is orderable if stock or eligibility is incomplete.

For each row account for fabrication, components, labor, setup, stencil, Extended/feeder charges, spares/attrition, MOQ, rails/panels and predictable other fees. Avoid double counting bundled quote charges. No linear extrapolation of prototype unit prices. Mark unavailable elements unknown (or a supported sourced range); never zero by default. Separate known subtotal from complete total. Cost per assembled board = all required expenditure / assembled finished-board quantity, not fabricated quantity.

Prefer actual quote only with explicit authorization for necessary private design/BOM upload, accessible authenticated interface, and no order/payment/reservation. If unauthorized, use verified public pricing or supported estimate ranges and state omissions; do not ask to upload just to hide an estimation limitation. Never use invented precision, stale availability or unverified currencies/exchange rates.

## Required report
Economic PCBA quantity range:
Quantity-selection basis (valid quantities, source and verification status):
Currency:
Pricing timestamp:
Quote or estimate (also label each row):

Level | Assembled Qty | PCB Fab | Components | Assembly/Setup/Other | Estimated Total | Cost per Assembled Board
MINIMUM
MIDDLE
MAXIMUM

Then state fabricated quantities if different, panel counts/boards-per-panel, stock limitations, shipping/tax/duties excluded unless actually determined, other exclusions, sources/assumptions, major cost drivers and safe reduction opportunities. Show known subtotal separately when total cannot be determined. Keep blocked/unknown rows visibly non-orderable.

Save costs.csv and costs.md. The helper accepts an explicit verified valid-quantity list and source/time/currency plus keyed row costs; it only computes categories/arithmetic. It cannot discover eligibility, fetch prices or convert raw KiCad BOM/CPL schemas. Null costs remain unknown; a missing tier must never become a zero quote.
