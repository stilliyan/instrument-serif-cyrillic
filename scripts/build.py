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
path = SCRIPTS.parent / 'build/Lirena-Regular.ttf'
font = TTFont(path, recalcTimestamp=False)
refine_regular(font)
refine_full(font)
refine_priority(font)
font.save(path)
font.flavor = 'woff2'
font.save(path.with_suffix('.woff2'))
print('Built refined Regular 0.510 and original Italic 0.300 in build/.')
