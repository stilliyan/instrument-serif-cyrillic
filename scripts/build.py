"""Rebuild Regular and Italic from the included OFL source fonts."""
from pathlib import Path
import runpy
SCRIPTS = Path(__file__).resolve().parent
runpy.run_path(str(SCRIPTS / 'build_italic.py'), run_name='__main__')
runpy.run_path(str(SCRIPTS / 'build_family.py'), run_name='__main__')
print('Built Regular and Italic (TTF and WOFF2) in build/.')
