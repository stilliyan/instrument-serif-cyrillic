"""Rebuild Regular and Italic from the included OFL source fonts."""
from pathlib import Path
import runpy
SCRIPTS = Path(__file__).resolve().parent
runpy.run_path(str(SCRIPTS / 'build_italic.py'), run_name='__main__')
runpy.run_path(str(SCRIPTS / 'build_family.py'), run_name='__main__')
from fontTools.ttLib import TTFont
from refine_regular import refine_regular
from refine_full import refine_full
from refine_priority import refine_priority
from refine_followup import refine_followup
from refine_soft import refine_soft
from refine_junctions import refine_junctions
from refine_roundness import refine_roundness
from refine_rhythm import refine_rhythm
from refine_smoothness import refine_smoothness
from refine_terminals import refine_terminals
path = SCRIPTS.parent / 'build/Lirena-Regular.ttf'
font = TTFont(path, recalcTimestamp=False)
refine_regular(font)
refine_full(font)
refine_priority(font)
refine_followup(font)
refine_soft(font)
refine_junctions(font)
refine_roundness(font)
refine_rhythm(font)
refine_smoothness(font)
refine_terminals(font)
from finalize_release import finalize_release
finalize_release(font, 'Regular')
font.save(path)
font.flavor = 'woff2'
font.save(path.with_suffix('.woff2'))
italic_path = SCRIPTS.parent / 'build/Lirena-Italic.ttf'
italic = TTFont(italic_path, recalcTimestamp=False)
finalize_release(italic, 'Italic')
italic.save(italic_path)
italic.flavor = 'woff2'
italic.save(italic_path.with_suffix('.woff2'))
print('Built Lirena 1.000 Regular and Italic in build/.')
