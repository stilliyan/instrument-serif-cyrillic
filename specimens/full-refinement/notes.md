# Lirena Regular 0.500 — full Cyrillic refinement

The original four supplied fonts were compared before editing. See
[pre-edit analysis](full_analysis_before.png), [actual before/after](before_after_full.png),
[Latin control comparison](capital_comparison.png) and [a / а](a_a_comparison.png).
Proofs render actual font files through HarfBuzz and FreeType, with common em sizes
and baselines for comparisons. No substitute typeface or simulated after is shown.

## Scope

All 62 Bulgarian letter codepoints were reviewed in each style, including Й/й and
Ѝ/ѝ. Regular has 38 newly changed outlines since 0.400, and 41 since the original
0.300: 20 capitals and 21 lowercase, including accents. The earlier в/ж/к work is
retained. Shared Latin-derived Cyrillic forms are deliberately kept intact.
Latin outlines, advances, sidebearings and shaping remain unchanged. Italic TTF is
byte-identical to the supplied 0.300 file; it remains the successful style reference.
Original source files are untouched. This refinement targets Regular.

## Capitals

The former donor capitals had oversized counters and advances beside native
Instrument Serif Latin. Rebuild distinct capitals from the family's own I stems,
A/K diagonals, O/P/R bowls and native terminal geometry. Retain Cyrillic identity:
И has a rising diagonal, Л has no crossbar, Д/Ц/Щ have tapered descenders and
Ж/Ф/Ю/Я remain their distinct Cyrillic constructions. У is adjusted by moving
its branches independently, rather than compressing every stroke horizontally.

Advance widths, in the shared 1000-unit em:

| Letter | Regular 0.400 | Regular 0.500 |
| --- | ---: | ---: |
| П | 811 | 546 |
| И | 842 | 546 |
| Г | 562 | 408 |
| Б | 611 | 478 |
| Ъ | 718 | 574 |
| Л | 769 | 505 |
| Д | 777 | 535 |
| Ж | 1085 | 822 |
| З | 550 | 371 |
| У | 669 | 535 |
| Ф | 915 | 600 |
| Ц | 797 | 564 |
| Ш | 1127 | 713 |
| Щ | 1137 | 732 |
| Ч | 687 | 587 |
| Ю | 1134 | 770 |
| Я | 650 | 513 |

## Lowercase and accents

Retain Bulgarian handwritten constructions; bring inconsistent ascenders to the
native 740-unit rhythm and large д/з loops to -205 units. Use native u-based cup
construction for ц/ш/щ and native stem/curve components for н/ч/ф/ю. Correct local
stems, terminal thickness and spacing in м/ь/ъ/я. Original Latin т/m is unchanged.
Й/Ѝ/й/ѝ now use matching native accent geometry on the appropriate Cyrillic body.

Latin a and Cyrillic а have exactly equal outlines and horizontal metrics within
both styles. Regular is double-storey; Italic is single-storey, as in the original
Instrument Serif. The a/а proof uses identical size and baseline for each pair.

## Per-character changes since 0.400

- **П**: Latin I stems and native 25-unit top bar; width 811 to 546.
- **И**: Native 71-unit stems with 33-unit rising diagonal; width 842 to 546.
- **Й**: New И body with the corresponding original Latin accent.
- **Ѝ**: New И body with the corresponding original Latin accent.
- **Г**: Latin F top arm, stem and serif system, with the middle arm removed.
- **Ь**: Native P bowl rotated vertically into a lower bowl, joined to Latin I.
- **Б**: Native lower bowl plus Latin E top-arm terminal; width 611 to 478.
- **Ъ**: Same bowl/stem as Ь with a native T entry terminal; width 718 to 574.
- **Л**: Native A diagonals and feet, with its crossbar removed; width 769 to 505.
- **Д**: Л triangle with 25-unit footer and short tapered descenders; width 777 to 535.
- **Ж**: Two native K branch systems around Latin I; width 1085 to 822.
- **З**: Native numeral 3 curve and terminal logic, rather than the wide donor construction.
- **У**: Move diagonal branches inward independently; preserve stroke runs and bring terminal thickness to 23 units.
- **Ф**: O curve/counter logic with native I ascender/descender stem; width 915 to 600.
- **Ц**: Two native I stems, 25-unit base and short tapered descender.
- **Ш**: Three Latin I stems and a native 25-unit base; width 1127 to 713.
- **Щ**: Same body as Ш with the shared short descender.
- **Ч**: Native U bowl with shortened left arm, and Latin I right stem; replaces the heavy donor join.
- **Ю**: Latin I and O linked by the H crossbar thickness; width 1134 to 770.
- **Я**: Reflected native R construction; native bowl, leg and serif proportions.
- **й**: Exactly the corresponding native Latin u accent; same base as Cyrillic и.
- **ѝ**: Exactly the corresponding native Latin u accent; same base as Cyrillic и.
- **б**: Refit the curved Bulgarian ascender to the native 740-unit Latin height; preserve lower bowl.
- **д**: Shorter -205-unit descender loop, 68-unit right stem and less excess right-side spacing.
- **з**: Shorter -205-unit lower loop with a slightly stronger bottom hairline.
- **г**: Calmer upper overshoot and a stronger entry hairline; cursive Bulgarian construction retained.
- **л**: Native v stroke and terminal system rotated into the Bulgarian lambda form; width 495 to 433.
- **н**: Latin n stem/serif system and 25-unit crossbar; width 558 to 454.
- **ц**: Latin u body (same as и) with a 130-unit descender.
- **ш**: Two overlapping native u constructions give three 68-unit stems and consistent cups.
- **щ**: Same body as ш with the shared short descender.
- **ч**: Native u mid-bowl and n right stem; removes the weaker donor stem system.
- **ф**: Native o counter/curve system and l/p 68-unit stem; 740/-205 extenders replace 958/-363.
- **ю**: Native l/o construction and 25-unit link; ascender 740 instead of 958.
- **м**: Increase only the baseline serif surfaces from 16 to 23 units, matching native terminal logic.
- **ь**: Right edge of the straight stem moved by 6 units to a 68-unit stem; bowl identity retained.
- **ъ**: Local upright-stem widening to 68 units; Bulgarian entry hook and lower bowl retained.
- **я**: 68-unit right stem, stronger upper-counter hairline and 23-unit baseline terminals.

## Spacing and validation

Add 28 pair-specific Cyrillic kerning corrections where edited shapes otherwise
collide. Latin kerning is unchanged; the existing Cyrillic lookup is retained.
Pair scanning is a sampled geometric diagnostic, not a full manual kerning audit.
Inherited serif interlocks between unchanged Latin-derived forms are retained.

TTF tables compile and reload; composite references, Bulgarian coverage,
precomposed/decomposed accents, Latin shaping and WOFF2 round trips pass.
All 38 newly edited outlines have zero adjacent duplicate points and zero proper
self-crossings in the flattened-curve diagnostic. This is not exhaustive
mathematical certification. Edited paths were united before export.

UPM 1000, x-height 510, cap height 720, ascent 990, descent -371 and line gap 0
remain unchanged. Horizontal maxima in hhea are recalculated for the actual new
widths. Regular metadata is 0.500; Italic metadata remains 0.300.

See [validation.json](validation.json) for measured results. Native 16–72px,
paragraph, alphabet and mixed-script proofs are reviewed separately. This remains
a high-contrast display/editorial family. No exhaustive OS/app survey is claimed.

The compact download contains eight files only: two TTFs, two WOFF2s, fonts.css,
README with credits and the two original OFL licenses. Proof materials remain
outside that package. Source fonts and reproducible scripts are in the repository.
