# Regular 0.540 — smooth ф and ц/щ junctions

Before and after compare published 0.530 and 0.540 exports at the same em and
baseline, with the supplied original Instrument Serif as the actual control.
The baseline analysis sheet and measurements were produced before changes.

- **ц**: Preserve native cups and three/two stems; draw one continuous curved exit into the descender, with matching tangents and a softly rounded tip. Remove the intersecting tail/terminal splice.
- **щ**: Preserve native cups and three/two stems; draw one continuous curved exit into the descender, with matching tangents and a softly rounded tip. Remove the intersecting tail/terminal splice.
- **ф**: Native o bowl and 68-unit l/p stem; remove inherited footer/bowl tabs and add tangent-matched rounded lower shoulder joins. Preserve the original rounded p descender foot.

The lower ф ring previously contained parts of the native l foot and clipped p
bowl. Remove those protruding pieces, keep the widened native o bowl and 68-unit
stem, fillet the two outer lower shoulders, and retain the original rounded p
foot. The lower counters now follow the native o curves without inserted serifs.

ц and щ previously joined a separate tail to a rounded exit with boolean
intersection. Draw the exit and tail as one continuous section, removing the
successive changes of direction. The two outer cubic sections have matching
tangents; the tips have small round corners. Native cups and upper stems retained.

Exactly three outlines changed. All advance widths, sidebearings, vertical
metrics and layout tables, including GPOS kerning, are unchanged from 0.530.
363 pairs involving ф/ц/щ sampled every 4 units from -205 to 740 have minimum
scanline gaps >=4.12 units. This is a sampled diagnostic, not an exhaustive
mathematical collision proof. Actual word and 16/24/32/48/72 px proofs included.

285 Latin mappings per style, Latin shaping, all other outlines, accents and
original Italic TTF/WOFF2 bytes are preserved. Compilation, WOFF2 roundtrip,
flattened proper-crossing and adjacent-duplicate checks pass. The full source
pipeline reproduces every final outline, metric and layout table. Supplied
original files were not overwritten. Release contains eight files, including
both unchanged original OFL licenses.

The original static portfolio thumbnail is fixed artwork and is preserved;
it is not regenerated from new font outlines.
