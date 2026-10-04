# Lirena Regular 0.400 — actual refinement

Only three outlines changed: Bulgarian lowercase в, ж and к. Originals remain
unchanged in /Users/s/Documents/Lirena and in the previous GitHub release.

## Changes and reasons

- в: redraw the upper loop at 740 units (formerly 958), matching the Latin b/k
  ascender height while retaining its Bulgarian two-loop form. Top hairline is
  approximately 25 units. Lower bowl remains the original design. Existing
  self-crossings were resolved by outline union in this edited glyph.
- ж: shorten the straight ascender extension by 218 units, preserving the original
  terminal shape; widen its 62-unit central stem to 68 to match Latin n/k. Open
  the upper boundary of the lower-branch joins by 4 units. Add 6 units of space
  on each side (advance 733 to 745).
- к: shorten the straight ascender extension by 218 units, widen its stem to 68,
  open the lower branch locally by 4 units and reduce the bulb terminal modestly.
  Add 8 units of space on each side (advance 505 to 521).

These are localized edits, not a global compression or a deslanting of Italic.
The reduced ascenders are a deliberate proportional decision; Bulgarian form
identity is retained. There is no claim that a 958-unit original was technically
invalid. The calmer Regular is now closer to the 740-unit Latin ascender rhythm.

## Preserved and inspected

All other outlines and metrics remain identical. Latin mappings, original glyph
instructions, GSUB, GPOS, GDEF, cmap, OS/2, hhea and post tables are preserved.
Italic TTF is byte-identical to the original. т retains the exact Latin m design.
The remaining Bulgarian alphabet was inspected in full-alphabet and word proofs;
д, з, м, я and the other letters were left unchanged. Existing pair kerning is
retained; the small ж/к sidebearing changes did not justify a broad new kern table.

## Validation

All TTF/WOFF2 tables reloaded and compiled. WOFF2 round trips preserve outlines
and spacing. Composite references, requested glyph coverage, Latin shaping and
Bulgarian decomposed accents pass. Edited contours have no adjacent duplicate
points. Approximate within-contour proper-crossing tests report no crossings in
the edited output; contour union resolves the original в crossings. Font style
linking, family name and vertical metrics remain intact. Regular version/unique
ID changes to 0.400; Italic remains 0.300.

See validation.json for exact results. The geometric crossing test uses flattened
curves and is not exhaustive mathematical certification. Intended overlap between
separate ж/к contours remains. Raster proofs are FreeType/HarfBuzz; the production
website is separately checked in Chrome. No exhaustive OS/application compatibility
survey was performed. Remaining manual review: longer Bulgarian text at intended
sizes, particularly д/з descender rhythm and м/я spacing. Small sizes remain those
of a high-contrast display/editorial family.

## Proofs

before_after_regular.png shows the actual original and exported refined TTFs at
shared size/baseline. Alphabet, paragraph, mixed-script, Latin/Cyrillic and native
pixel-size proofs are included separately. These review materials are not bundled
into the compact font download.
