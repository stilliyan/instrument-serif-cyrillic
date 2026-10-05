# Regular 0.530 — reviewed lower joins and native heads

The before/after sheets compare actual published 0.520 and 0.530 exports at the
same em and baseline, with original Instrument Serif controls. The user asked
specifically to remove the faulty lower connection into the second cup of ш/щ,
restore native-style head shapes, and preferred the earlier в at small sizes.

- **ц**: Native u bowls with a gently bracketed exit and a continuously curved descender; remove the triangular terminal.
- **ш**: One continuous three-stem outline with matched native u cups and a smooth central lower connection; no duplicated u exit or pasted middle terminal.
- **щ**: Same flowing cups as ш, with a curved descender joined through the final stem.
- **н**: Native h head and foot curves retained intact at Cyrillic x-height; 68-unit stems and a thin smoothly bracketed crossbar, replacing the flat square heads.
- **ъ**: Native-weight upright and bracketed serifs with a flowing lower bowl; remove the b-derived foot spur and clumsy union.
- **в**: Restore the user-preferred 0.510 form and stroke weight; translate 18 units left and retain corrected 408-unit advance and 23/25 sidebearings.

The preferred 0.510 в contour is retained exactly, translated 18 units left:
its shape and weight stay intact, with advance 408 and sidebearings 23/25.
ш/щ are a single continuous three-stem contour, not a union of two u glyphs.
The central lower transition contains no duplicated native u exit. Native u
inner/outer bowl curves remain the controls; final terminals are bracketed.
н uses native h's actual head and foot curves without vertically scaling them,
with 68-unit stems and a 25-unit crossbar with curved joins. The pointed head is
the actual native Instrument Serif contour. ъ has a continuous lower bowl and
uses the same native stem/head, with the old b foot spur removed.

## Spacing and validation

Preserve original lookups and add 127 Cyrillic-only followup corrections. Check
1,819 pairs involving priority glyphs at 4-unit vertical sampling, -205..740;
minimum sampled gaps are >=3.5 units. This diagnostic is not exhaustive manual
kerning or a mathematical collision proof. Real word proofs and 16/24/32/48/72
px sheets support visual review. See kern-references.json and kern-after.json.

Exactly six outlines differ from 0.520; all other outlines/metrics preserved.
285 Latin mappings per style, native Latin shaping, vertical metrics, GSUB/GDEF,
and accent decomposition unchanged. Italic TTF/WOFF2 bytes unchanged. Compilation,
WOFF2 roundtrip and flattened proper-crossing checks pass. Rebuild matches all
final outlines, metrics and layout tables. Original supplied fonts untouched.

The compact release has eight files: two TTFs, two WOFF2s, CSS, README and both
unchanged original OFL licenses. Source and measurements live in the repository.
