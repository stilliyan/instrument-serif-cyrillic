"""Generate a vector social specimen from actual distributed font outlines.
Rasterize the output SVG at its native 3462×1818 size to update social-cover.png.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import re
r=Path(__file__).resolve().parent.parent; width,height=3462,1818
logo=(r/'website/assets/spasov-type-logo.svg').read_text();paths=re.search(r'<svg[^>]*>(.*)</svg>',logo,re.S).group(1);paths=re.sub(r'fill="[^"]*"','fill="#141413"',paths)
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="{width}" height="{height}" fill="#101010"/>',f'<g transform="translate(-180 640) rotate(-14) scale(5.6)">{paths}</g>',f'<g transform="translate(-100 1740) rotate(-14) scale(5.6)">{paths}</g>']
for style,cx in [('Regular',1140),('Italic',2280)]:
 f=TTFont(r/f'fonts/Lirena-{style}.ttf');gs=f.getGlyphSet();n=f.getBestCmap()[ord('ж')];p=SVGPathPen(gs);b=BoundsPen(gs);gs[n].draw(p);gs[n].draw(b);x1,y1,x2,y2=b.bounds;s=1.23;tx=cx-(x1+x2)*s/2;ty=height/2+(y1+y2)*s/2
 parts.append(f'<path d="{p.getCommands()}" fill="#F0EFEB" transform="translate({tx:.4f} {ty:.4f}) scale({s} {-s})"/>')
parts.append('</svg>');svg=''.join(parts);output=r/'build/social-cover.svg'; output.parent.mkdir(exist_ok=True); output.write_text(svg)
print('Actual Regular 0.500 and original Italic 0.300 outlines, shared 1230-unit em scale.')
