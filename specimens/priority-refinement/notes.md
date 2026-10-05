# Regular 0.510 — Instrument Serif Cyrillic refinement

Use the supplied Instrument Serif Regular as the family reference. The original
Latin outlines and shaping are preserved. Work from native o, I, l, q and R
components, rather than stretching another typeface into an approximation.
Official source: https://github.com/Instrument/instrument-serif

The supplied Regular 0.500 was measured before edits. Original Desktop files are
unchanged. See analysis-before.png, glyph-metrics.json, kern-before.json and
baseline-before.png for the first analysis; seven-form-analysis.png compares the
final seven lowercase constructions against supplied 0.500 and real native Latin
controls at the same em. seven-form-words.png and before-after.png show actual
exports, not mockups. small-size-final.png covers 16/24/32/48/72 px.

## Eleven refined forms

- **Ц**: Counter +13 units, 23-unit base, curved 140-unit tail instead of the angular 110-unit stub.
- **Ш**: Two counters opened by 20 units each; native 71-unit stems and 23-unit baseline bar retained.
- **Щ**: Same opened body as Ш, with the matching curved 140-unit tail and adequate right spacing.
- **У**: Remove the protruding junction spur, reduce the thick diagonal toward native 71-unit weight, and strengthen the thin continuation by 5 units.
- **б**: Native o bowl with a smooth tapered flag and continuous upper return.
- **в**: Same native o bowl and width as б; flowing closed ascender loop with an open upper counter.
- **з**: Two flowing bowls with a curved waist instead of a numeral-derived diagonal spur.
- **ж**: Curved upper arms and lighter lower diagonals, joined to the native ascender.
- **д**: Preserve the native Instrument Serif q loop and joins; attach a smooth Bulgarian descender return.
- **ч**: Single native-style head serif and continuous right stem, removing the double ear.
- **я**: Mirror native Instrument Serif R and adapt cap height to x-height; preserve its bowl and flowing leg construction at a 68-unit stem weight.

| Letter | Final advance | Final stored outline bounds |
| --- | ---: | --- |
| Ц | 592 | [19, -140, 561, 720] |
| Ш | 753 | [19, 0, 734, 720] |
| Щ | 786 | [19, -140, 755, 720] |
| б | 459 | [41, -9, 401, 743] |
| ж | 668 | [47, 0, 621, 740] |
| з | 416 | [20, -205, 378, 517] |
| в | 459 | [41, -9, 401, 740] |
| У | 535 | [8, 0, 527, 720] |
| д | 460 | [39, -205, 390, 516] |
| ч | 454 | [14, 0, 435, 510] |
| я | 525 | [20, -6, 504, 510] |

б and в share the native o bowl, 360-unit stored width, 459-unit advance and
baseline overshoot. Their different upper constructions retain Bulgarian forms.
д uses the actual native q body and its original joins with a curved descender.
я mirrors native R at 0.96 horizontal scale (68-unit stem) and 510/720 vertical
scale; its curved leg and bowl construction come directly from Instrument Serif.
Other curves are constructed for Cyrillic and use the native family as controls;
not every Cyrillic form is obtainable by copying a Latin glyph. Export all new
curves as quadratic TrueType contours with sub-unit conversion tolerance.

## Spacing and validation

A 4-unit-step scan from -205 to 740 checks all 1,243 Bulgarian pairs involving
one of the eleven edited letters. Append 69 pair corrections in a Cyrillic-only
GPOS lookup, with native H/V spacing as controls for Ц/Щ/У. All sampled minimum
gaps are >=3.5 units. This is a sampled diagnostic, not a mathematical collision
proof or exhaustive manual kerning. kern-corrections.json, kern-references.json
and kern-after.json contain the evidence; actual word proofs support review.

Exactly eleven glyph outlines changed relative to supplied 0.500. All other
outlines and metrics remain unchanged. Preserve 285 Latin mappings per style,
Latin shaping, coverage, GSUB/GDEF and vertical metrics. Existing GPOS lookups are
retained. Original Italic TTF/WOFF2 bytes are unchanged. TTF compilation, WOFF2
outline/metric round trips and decomposed accents pass. Edited contours have no
adjacent duplicate points or proper crossings in the flattened-curve diagnostic.
Standalone refinement reproduces exact font bytes; the full build matches all
outlines, metrics and layout tables. See validation.json.

## Website baseline and package

The grid previously centered each glyph vertically by its individual ink bounds.
That caused the apparent misalignment in the screenshot. Keep horizontal optical
centering and remove individual vertical translations so rows share one baseline
in both styles. Normal round overshoot and descenders remain part of the font.

The compact v0.5.1 download has eight files: two TTFs, two WOFF2s, CSS, README,
and both original OFL licenses. Font diagrams and portfolio thumbnail use actual
current outlines. Original inputs and previous releases remain intact.
