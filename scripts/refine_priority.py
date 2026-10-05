"""Refine eleven Regular Cyrillic glyphs after the 0.500 stage.
Original Latin and all other outlines are preserved.
"""
from pathlib import Path
from copy import deepcopy
from array import array
import json
import pathops
from fontTools.ttLib import TTFont
from fontTools.ttLib.removeOverlaps import skPathFromGlyph,ttfGlyphFromSkPath,removeOverlaps
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from refine_curves import curved_forms
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

def refine_priority(f):
    assert abs(f["head"].fontRevision-.5)<.001, "Expected Regular 0.500 input"
    cm=f.getBestCmap();gs=f.getGlyphSet();paths={c:skPathFromGlyph(cm[ord(c)],gs) for c in 'Ikl3oRq'};changes={}
    def poly(points):
     p=pathops.Path();p.moveTo(*points[0])
     for pt in points[1:]:p.lineTo(*pt)
     p.close();return p
    def box(x1,y1,x2,y2):return poly([(x1,y1),(x2,y1),(x2,y2),(x1,y2)])
    def move(p,x=0,y=0):return p.transform(1,0,0,1,x,y)
    def union(*items):
     p=items[0]
     for q in items[1:]:p=pathops.op(p,q,pathops.PathOp.UNION)
     return p
    def save(c,p,adv,reason):
     pen=TTGlyphPen(None);p.draw(Cu2QuPen(pen,0.5,reverse_direction=False));g=pen.glyph();g.recalcBounds(f['glyf']);f['glyf'][cm[ord(c)]]=g;f['hmtx'][cm[ord(c)]]=(adv,g.xMin);changes[c]=reason
    # Wider counters and native terminal thickness; contours retain their common baseline.
    I=paths['I']
    def tail(x):
     p=pathops.Path();p.moveTo(x-26,23);p.lineTo(x+6,23);p.cubicTo(x+9,-26,x+13,-99,x+13,-140);p.lineTo(x-8,-140);p.cubicTo(x-9,-79,x-13,-23,x-26,0);p.close();return p
    cu=union(I,move(I,310),box(89,0,470,23));save('Ц',union(cu,tail(548)),592,'Counter +13 units, 23-unit base, curved 140-unit tail instead of the angular 110-unit stub.')
    sha=union(I,move(I,252),move(I,504),box(89,0,664,23));save('Ш',sha,753,'Two counters opened by 20 units each; native 71-unit stems and 23-unit baseline bar retained.')
    save('Щ',union(sha,tail(742)),786,'Same opened body as Ш, with the matching curved 140-unit tail and adequate right spacing.')
    # У: remove the surplus junction spur; align thick/thin diagonal contrast locally.
    g=f['glyf'][cm[ord('У')]]
    for i in [21,22,23]:g.coordinates[i]=(332-round((290-g.coordinates[i][1])*.284),g.coordinates[i][1])
    for i in [64,65]:x,y=g.coordinates[i];g.coordinates[i]=(x-13,y)
    for i in [19,20,21,22,23,24,25,26,27,28,29]:x,y=g.coordinates[i];g.coordinates[i]=(x+5,y)
    changes['У']='Remove the protruding junction spur, reduce the thick diagonal toward native 71-unit weight, and strengthen the thin continuation by 5 units.'
    reasons = {
        'б': 'Native o bowl with a smooth tapered flag and continuous upper return.',
        'в': 'Same native o bowl and width as б; flowing closed ascender loop with an open upper counter.',
        'ж': 'Curved upper arms and lighter lower diagonals, joined to the native ascender.',
        'з': 'Two flowing bowls with a curved waist instead of a numeral-derived diagonal spur.',
        'д': 'Preserve the native Instrument Serif q loop and joins; attach a smooth Bulgarian descender return.',
        'ч': 'Single native-style head serif and continuous right stem, removing the double ear.',
        'я': 'Mirror native Instrument Serif R and adapt cap height to x-height; preserve its bowl and flowing leg construction at a 68-unit stem weight.'
    }
    for c, outline in curved_forms(paths).items():
        save(c, outline, {'б':459,'в':459,'з':416,'ж':668,'я':525,'д':460}.get(c, f['hmtx'][cm[ord(c)]][0]), reasons[c])
    removeOverlaps(f,[cm[ord(c)] for c in changes],removeHinting=True)
    for c in changes:
     g=f['glyf'][cm[ord(c)]];g.recalcBounds(f['glyf']);adv,_=f['hmtx'][cm[ord(c)]];f['hmtx'][cm[ord(c)]]=(adv,g.xMin)
    for nid,value in {3:'Lirena Regular 0.510',5:'Version 0.510'}.items():
     for rec in f['name'].names:
      if rec.nameID==nid:rec.string=value.encode(rec.getEncoding())
    f['head'].fontRevision=.51
    for ch in changes:
     g=f['glyf'][cm[ord(ch)]];pts=[];flags=[];ends=[];start=0
     for end in g.endPtsOfContours:
      local=[];lf=[]
      for i in range(start,end+1):
       xy=g.coordinates[i];flag=g.flags[i]
       if local and xy==local[-1] and lf[-1]&1:continue
       local.append(xy);lf.append(flag)
      if len(local)>1 and local[0]==local[-1] and lf[0]&1 and lf[-1]&1:local.pop();lf.pop()
      pts.extend(local);flags.extend(lf);ends.append(len(pts)-1);start=end+1
     g.coordinates=GlyphCoordinates(pts);g.flags=array('B',flags);g.endPtsOfContours=ends;g.recalcBounds(f['glyf'])
    
    corrections={'ЦА': -14, 'ЦО': -33, 'ЦС': -33, 'ЦЕ': -33, 'ЦН': -33, 'ЦК': -33, 'ЦТ': -33, 'Ца': -45, 'Цо': -51, 'Це': -51, 'Ци': -45, 'Цп': -33, 'Цр': -33, 'Цс': -51, 'Цт': -33, 'Цу': -50, 'Цх': -24, 'Цб': -33, 'Цв': -33, 'Цж': -33, 'ЩА': -14, 'ЩО': -33, 'ЩС': -33, 'ЩЕ': -33, 'ЩН': -33, 'ЩК': -33, 'ЩТ': -33, 'Ща': -45, 'Що': -51, 'Ще': -51, 'Щи': -45, 'Щп': -33, 'Щр': -33, 'Щс': -51, 'Щт': -33, 'Щу': -50, 'Щх': -24, 'Щб': -33, 'Щв': -33, 'Щж': -33, 'УА': -61, 'УО': -41, 'УС': -41, 'УЕ': -22, 'УН': -22, 'УК': -22, 'УТ': -24, 'Уа': -15, 'Уо': -17, 'Уе': -17, 'Уп': -11, 'Ур': -11, 'Ус': -16, 'Ут': -11, 'Уу': -27, 'Ух': -17, 'Уб': 22, 'Ув': -55, 'Уж': -27, 'АУ': 3, 'АЦ': 3, 'АШ': 3, 'АЩ': 3, 'КЦ': 6, 'КШ': 6, 'КЩ': 6, 'ЛУ': 3, 'ША': 3, 'яА': 1}
    temp=deepcopy(f);fea='languagesystem cyrl dflt; languagesystem cyrl BGR; feature kern {\n'+''.join(f'pos {cm[ord(pair[0])]} {cm[ord(pair[1])]} {value};\n' for pair,value in corrections.items())+'} kern;';addOpenTypeFeaturesFromString(temp,fea);table=f['GPOS'].table;indices=[]
    for lookup in temp['GPOS'].table.LookupList.Lookup:indices.append(len(table.LookupList.Lookup));table.LookupList.Lookup.append(deepcopy(lookup))
    table.LookupList.LookupCount=len(table.LookupList.Lookup);cyrl=set();other=set()
    for record in table.ScriptList.ScriptRecord:
     for lang in [record.Script.DefaultLangSys]+[x.LangSys for x in record.Script.LangSysRecord]:
      if lang:(cyrl if record.ScriptTag=='cyrl' else other).update(lang.FeatureIndex)
    for idx in cyrl:
     rec=table.FeatureList.FeatureRecord[idx]
     if rec.FeatureTag=='kern':assert idx not in other;rec.Feature.LookupListIndex.extend(indices);rec.Feature.LookupCount=len(rec.Feature.LookupListIndex)
    return changes

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Choose a separate output path.')
    f = TTFont(args.input, recalcTimestamp=False)
    refine_priority(f)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    f.save(args.output)
    f.flavor = 'woff2'
    f.save(args.output.with_suffix('.woff2'))
