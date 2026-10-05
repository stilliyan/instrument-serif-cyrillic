# Lirena

Bulgarian Cyrillic adaptation of Instrument Serif.

**Cyrillic adaptation by Stiliyan Spasov / Spasov Type.**

[Try the typeface](https://spasovtype.com/) · [Portfolio](https://www.stiliyanspasov.com/) · [Download the release](https://github.com/stilliyan/lirena/releases/latest)

## Regular refinement — release 0.5.7

Regular 0.570 smooths the outer connection between lowercase в loops and removes
its accidental pinhole, retaining the preferred oval and main counters. Lowercase
м pointed tops are lowered slightly. All spacing, other letters, original Latin
and Italic remain unchanged. Source/adaptation cards now center visible outlines
and context words in both styles, on desktop and mobile.
[Actual before/after comparisons and validation](specimens/smoothness-refinement/notes.md).

## Previous Regular refinement — release 0.5.6

Regular 0.560 gives Cyrillic х a lower optical height and more consistent spacing.
The soft sign ь shares the approved hard-sign oval, counter and head, with its own
curled lower return. The ц/щ descenders gain fully rounded tips. Original Latin,
Italic and all other letters remain unchanged; only х/ь advances and 19 targeted
Cyrillic pairs change.
[Actual before/after comparisons and validation](specimens/rhythm-refinement/notes.md).

## Previous Regular refinement — release 0.5.5

Regular 0.551 redraws the entire rounded bowl and counter of ъ, with smooth
returns to the stem. The lower ф serif uses the centered native l foot. The ц/щ exits
follow the native u flare and flow into their curved descenders, based on the
user’s visual proposal. Ten targeted Cyrillic pair corrections provide tail
clearance. Advance widths, original Latin and Italic remain unchanged.
[Actual before/after comparisons and validation](specimens/roundness-refinement/notes.md).

Previous Regular 0.540 removes protruding pieces at the lower ф bowl/stem
junctions and makes the ц/щ exits flow continuously into their descenders.
[Analysis and measured checks](specimens/junction-refinement/notes.md).

Previous Regular 0.530 redraws the lower ш/щ joins as one continuous outline,
uses native h heads for н/ъ and retains the preferred earlier в shape with
corrected spacing. [Reviewed comparisons](specimens/soft-refinement/notes.md).

Previous Regular 0.520 refines **б, в, к, ц, ш, щ, н and ъ** with continuous contours,
clean native-style heads/cups, connected tails and 173 Cyrillic-only pair
corrections. Original Latin and Italic are preserved.
[Followup proofs and measured validation](specimens/followup-refinement/notes.md).

All 62 Bulgarian letter codepoints are reviewed in both styles. Regular 0.510
refines the distinct Cyrillic capitals, lowercase and accents: 41 changed outlines
since 0.300, including 20 capitals and 21 lowercase. Original Latin and shared
Latin-derived Cyrillic forms are preserved. Italic remains the original 0.300.
Version 0.510 additionally refines **Ц, Ш, Щ, б, ж, з, в, У, д, ч and я**, adds 69 targeted
Cyrillic pair adjustments and restores the website grid’s shared baselines.
[Actual priority comparisons, measurements and validation](specimens/priority-refinement/notes.md).
[Earlier full-alphabet refinement](specimens/full-refinement/notes.md).
The download contains eight files: two TTFs, two WOFF2s, web CSS, README/credits
and both original OFL licenses. Latin a and Cyrillic а are identical within each
style: double-storey in Regular, single-storey in Italic.

## Regular

![Regular Bulgarian alphabet, numerals and symbols](specimens/regular-alphabet.png)

## Italic

![Italic Bulgarian alphabet, numerals and symbols](specimens/italic-alphabet.png)

## Styles and formats

Regular 400 and true Italic 400, each available as TTF and WOFF2 in `fonts/`.
Includes the Bulgarian uppercase and lowercase alphabet, Й/й and Ѝ/ѝ, alongside the original Latin, numerals and punctuation. Bulgarian forms are the defaults in both styles. Other Cyrillic alphabets are outside this adaptation's scope.

## Desktop installation

Install `fonts/Lirena-Regular.ttf` and `fonts/Lirena-Italic.ttf` using your operating system's font installer. Select **Lirena**, then Regular or Italic. Restart applications that cache their font lists.

## Web use

Keep both WOFF2 files beside `fonts.css`, then load the stylesheet:

```html
<link rel="stylesheet" href="fonts/fonts.css">
<p class="specimen" lang="bg">Кирилица с характер.</p>
```

```css
.specimen {
  font-family: 'Lirena', serif;
  font-weight: 400;
  font-synthesis: none;
}
.specimen em { font-style: italic; }
```

## Sources and adaptation

Lirena is the new name of the project previously published as Instrument Serif Cyrillic. The new name identifies the independent adaptation; it does not change the original authorship of Instrument Serif or Cormorant Garamond.

This independent adaptation is based on **Instrument Serif** and **Cormorant Garamond**. It is not an official release of either original project.

- Instrument Serif's original Latin outlines and spacing are preserved. Shared Cyrillic forms reuse those outlines, including Latin **m** adapted as Bulgarian **т**.
- The initial distinct Bulgarian forms use Cormorant Garamond as their source. Regular 0.500 retains and refines their Bulgarian identity, rebuilding many forms with Instrument Serif’s native stems, bowls, diagonals and terminals.
- The Cyrillic work includes proportion matching, italic slant adjustment, Cyrillic spacing, accented-letter composition and shared vertical metrics for the two styles.

Intended for titles and short editorial passages. Test your intended text and rendering environment before use.

## Website

The interactive specimen is at [spasovtype.com](https://spasovtype.com/).
Its complete source is in [`website/`](website/), including the HTML, CSS,
JavaScript, fonts, glyph comparison assets and downloadable font package.

```sh
cd website
npm start
```

Open http://127.0.0.1:3040/. See [the website README](website/README.md) for
hosting settings.

## Rebuild the adaptation

The actual adaptation scripts and the four source TTFs are included. The original development scripts have been reduced to font generation and validation; local paths and unrelated specimen-generation dependencies have been removed.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build.py
```

Rebuilt fonts are written to `build/`; the published files in `fonts/` are left untouched. The scripts check original outlines, Bulgarian glyph coverage, decomposed accents and Latin shaping. Rebuilds can differ in timestamps, serialization and metadata from the distributed files.

## Credits and licenses

- Copyright 2022 The Instrument Serif Project Authors. [Instrument Serif](https://github.com/Instrument/instrument-serif). Original Instrument Serif design and Latin outlines. Designed by Rodrigo Fuenzalida, with direction from Jordan Egstad, JD Hooge and Jack De Caluwé on behalf of Instrument.
- Copyright 2015 the Cormorant Project Authors. [Cormorant](https://github.com/CatharsisFonts/Cormorant). Source Bulgarian forms from Cormorant Garamond, designed by Christian Thalmann / Catharsis Fonts.
- Cyrillic adaptation by **Stiliyan Spasov / Spasov Type**. Bulgarian Cyrillic proportions, italic slant, spacing and paired styles.

All included font software, including the source fonts, is distributed under the **SIL Open Font License 1.1**. Both original licenses and copyright notices are included unchanged in `licenses/`. See [AUTHORS.txt](AUTHORS.txt) for attribution. Original authors retain their copyright; credit does not imply their approval or endorsement. No paid or exclusive license is added.
