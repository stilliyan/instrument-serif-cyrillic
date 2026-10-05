# Regular 0.551 — round bowls and native-style exits

The user asked for the complete round turn of ъ, a balanced lower serif for ф,
and supplied a visual proposal for native u-like flared exits for lowercase
ц/щ. The before/after sheet compares actual published 0.540 and revised 0.551
exports, with native P, l and u controls at the same em and baseline.

- **ц**: Native u flared exit and triangular underside, continuously extended into a 20-unit curved descender with a rounded tip. Original cups, upper stems and advance retained.
- **щ**: Same native-style flared exit and continuous descender as ц, translated 242 units. Three-stem body and advance retained.
- **ф**: Replace the asymmetric p descender footer with the exact native l footer, translated to the descender baseline. Keep a 68-unit stem and balance the 202-unit foot around its center; retain bowl, shoulder fillets, head and advance.
- **ъ**: Redraw the entire outer bowl and counter with aligned centers, continuous round quarters, curved upper shoulder and tangent-matched returns. Remove the baseline corner and skewed lower turn; retain native h head/left stem/foot, 68-unit upright, 75-unit side stroke, 25-unit hairlines and 451-unit advance.

The entire ъ bowl and counter are redrawn with smooth elliptical quarters,
aligned centers at y=170.5 and rounded returns to the upright. The upper
outer shoulder is curved into the stem, and the inner shoulder follows a
matching smooth arch rather than a flat entry. The 75-unit side
stroke and 25-unit top/bottom hairlines follow native P's contrast. The native
h head, 68-unit upright and left foot are retained. A horizontal tangent blends
the outer left foot into the bowl, removing the abrupt baseline corner.

ф retains the ring, counter, shoulder fillets and head from 0.540. Its asymmetric
p footer is replaced by the exact original l footer, translated +143/-205.
Foot bounds x=151..353, width 202, center 252; the stem center is 251.

ц/щ retain their native cups and stems. The exit follows the original u's
flared terminal and triangular underside. A continuous curved descender joins
that flare; the nominal 20-unit tip has softly rounded corners. The tail
extends farther right below the baseline; it is measured against the following
letter rather than adding blanket spacing to every word. See final-metrics.json.

Exactly four outlines differ from 0.540. All advance widths, stored left
sidebearings and vertical metrics are preserved. Existing layout lookups remain
unchanged; one Cyrillic-only lookup adds ten measured pair corrections for ц/щ
before А, Д, Я, з and х. Other pair positioning and native Latin shaping remain
unchanged. See kern-corrections.json for the exact deltas.

480 pairs involving ъ/ф/ц/щ sampled every 4 units from -205 to 740 have minimum
scanline gaps >=4.12 units after corrections. This is a sampled diagnostic,
not an exhaustive mathematical collision proof. Actual word and
16/24/32/48/72 px proofs are included.

285 Latin mappings per style, all other glyphs, accents and original Italic
TTF/WOFF2 bytes are preserved. Compilation, WOFF2 roundtrip, flattened proper
crossing and adjacent duplicate checks pass. The full source pipeline reproduces
every final outline, metric and layout table. Supplied original files untouched.
Download contains eight files with both unchanged original OFL licenses.

The original static portfolio thumbnail stays fixed; font updates never
regenerate that artwork.
