# Regular 0.520 — curves, joins and spacing

The user's screenshots showed 0.510. `analysis-before-after.png` and
`word-comparison.png` compare its actual exports with 0.520, at identical em
and shared baselines; `small-size-final.png` covers 16/24/32/48/72 px.
Source reference: original Instrument Serif in this repository's sources/.

## Eight scoped outline changes

- **б**: Single flowing outer contour with the native o bowl/counter; rounded shoulder connection, modestly strengthened curved ascender and flag and native o sidebearings.
- **в**: Single flowing outer contour, smooth waist and native o lower bowl/counter; 68-unit upper right stroke and native o spacing.
- **к**: Exact original Instrument Serif k outline, hints and metrics, mapped to Bulgarian к.
- **ц**: Connect the curved descender to the actual raised native u exit, replacing the detached angular stub.
- **ш**: Three native 68-unit u stems; remove the first u exit foot from the second cup to keep both lower curves clean.
- **щ**: Same cleaned cups as ш with a continuously attached curved descender.
- **н**: Native flat u head serifs, k baseline serifs and 68-unit stems; controlled 25-unit crossbar without two pointed entry wedges.
- **ъ**: Native b lower bowl at 0.68 height and 68-unit upright stem with the flat native u entry; remove the oversized pointed flag and retain the distinct lower-bowl hard-sign structure.

б and в now have native o's exact lower bowl and counter. Advance 459 → 408,
sidebearings 41/58 → 23/25. At y=250 both native o and б/в have ~76-unit curved
strokes; straight native stems are 68 units. б's curved ascending return and
flag were modestly strengthened after comparing native f/b controls. These are
optical controls, not a requirement that every horizontal section match a
straight stem. Original Latin outlines and metrics stay unchanged.

## Spacing and validation

Append 173 Cyrillic-only corrections, preserving all 0.510 lookups. Use real
native Latin spacing as controls for the changed forms' body contours, then
check 1,819 pairs involving all priority glyphs at 4-unit y steps, -205..740.
All sampled minimum gaps are >=3.5 units. This sampled clearance diagnostic and
word review are not an exhaustive manual kerning audit. Detailed decisions:
kern-references.json, kern-corrections.json, kern-after.json.

Exactly eight outlines differ from 0.510; other outlines and metrics retained.
285 Latin mappings per style, original Latin shaping, vertical metrics, GSUB,
GDEF and accent decomposition preserved. Italic TTF/WOFF2 bytes unchanged.
TTF table compilation, WOFF2 roundtrip and flattened proper-crossing diagnostic
pass. See validation.json and final-metrics.json. Desktop source files untouched.

Download has exactly eight files: two TTFs, two WOFF2s, CSS, README and both
unchanged original OFL licenses. Website and repository use the same final fonts.
