"""Full Regular Cyrillic refinement; run after the 0.400 refinement stage.
Latin outlines and metrics are preserved. The CLI always writes a separate file.
"""
from pathlib import Path
from copy import deepcopy
from array import array
from fontTools.ttLib import TTFont
from fontTools.ttLib.removeOverlaps import skPathFromGlyph,ttfGlyphFromSkPath
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
import pathops,json,math

def refine_full(font):
    assert abs(font["head"].fontRevision - .4) < .001, "Expected Regular 0.400 input"
    original_order=font.getGlyphOrder()[:]
    cm=font.getBestCmap();gs=font.getGlyphSet();paths={ch:skPathFromGlyph(cm[ord(ch)],gs) for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'}
    changes={}
    def polygon(pts):
     p=pathops.Path();p.moveTo(*pts[0])
     for pt in pts[1:]:p.lineTo(*pt)
     p.close();return p
    def box(x1,y1,x2,y2):return polygon([(x1,y1),(x2,y1),(x2,y2),(x1,y2)])
    def union(*ps):
     result=ps[0]
     for p in ps[1:]:result=pathops.op(result,p,pathops.PathOp.UNION)
     return result
    def intersect(a,b):return pathops.op(a,b,pathops.PathOp.INTERSECTION)
    def subtract(a,b):return pathops.op(a,b,pathops.PathOp.DIFFERENCE)
    def move(p,x=0,y=0):return p.transform(1,0,0,1,x,y)
    def temporary(name,g):
     g.recalcBounds(font['glyf']);font['glyf'][name]=g;font['hmtx'][name]=(1000,g.xMin)
    def save(ch,p,advance,why):
     g=ttfGlyphFromSkPath(p);font['glyf'][cm[ord(ch)]]=g;font['hmtx'][cm[ord(ch)]]=(advance,g.xMin);changes[ch]=why
     return p
    I=paths['I']
    # All component stems/serifs are original Latin outlines, not donor-font scaling.
    pi=save('П',union(I,move(I,297),box(89,695,457,720)),546,'Latin I stems and native 25-unit top bar; width 811 to 546.')
    reverse_n=save('И',union(I,move(I,297),polygon([(144,0),(177,0),(402,720),(369,720)])),546,'Native 71-unit stems with 33-unit rising diagonal; width 842 to 546.')
    # Native breve/grave marks, positioned over the new body.
    for ch,latin,offset in [('Й','Ŭ',0),('Ѝ','Ì',148)]:
     original=font['glyf'][cm[ord(latin)]];component=original.components[-1];mark=skPathFromGlyph(component.glyphName,gs);mark=move(mark,component.x+offset,component.y)
     save(ch,union(reverse_n,mark),546,'New И body with the corresponding original Latin accent.')
    # Г: the native F without its middle arm; all original terminal geometry retained.
    save('Г',subtract(paths['F'],box(160,230,330,500)),408,'Latin F top arm, stem and serif system, with the middle arm removed.')
    # Ь/Б: lower bowl from the native P, plus native I stem and E upper terminal.
    bowl=intersect(paths['P'],box(145,270,600,760)).transform(1,0,0,-1,0,720)
    soft=save('Ь',union(I,bowl),466,'Native P bowl rotated vertically into a lower bowl, joined to Latin I.')
    save('Б',union(soft,intersect(paths['E'],box(145,535,600,760))),478,'Native lower bowl plus Latin E top-arm terminal; width 611 to 478.')
    # Ъ adds the native T entry terminal to the same lower-bowl system.
    save('Ъ',union(move(soft,108),move(intersect(paths['T'],box(-100,580,266,760)),2)),574,'Same bowl/stem as Ь with a native T entry terminal; width 718 to 574.')
    # Л: remove the A crossbar by joining its original inner diagonal edges.
    a=deepcopy(font['glyf'][cm[ord('A')]])
    coords=list(a.coordinates[:35])+[(276,295),(212,563),(207,563),(140,295)]+list(a.coordinates[39:48])
    flags=list(a.flags[:35])+[1,1,1,1]+list(a.flags[39:48]);a.coordinates=GlyphCoordinates(coords);a.flags=type(a.flags)(flags);a.endPtsOfContours=[len(coords)-1];a.numberOfContours=1;a.program.fromBytecode(b'');a.recalcBounds(font['glyf'])
    temporary('__temporary_lambda',a)
    lp=move(skPathFromGlyph('__temporary_lambda',font.getGlyphSet()),24)
    save('Л',lp,505,'Native A diagonals and feet, with its crossbar removed; width 769 to 505.')
    # Д: same triangle; the footer has short tapered terminals rather than deep spikes.
    footer=polygon([(6,25),(499,25),(513,-90),(492,-90),(479,0),(26,0),(13,-90),(-8,-90)])
    save('Д',union(lp,footer),535,'Л triangle with 25-unit footer and short tapered descenders; width 777 to 535.')
    # Ж reuses the K branching arms around an original I stem.
    arm=intersect(paths['K'],box(145,-50,600,760));right=move(arm,286.5);left=arm.transform(-1,0,0,1,535.5,0)
    save('Ж',union(right,left,move(I,286.5)),822,'Two native K branch systems around Latin I; width 1085 to 822.')
    save('З',paths['3'],371,'Native numeral 3 curve and terminal logic, rather than the wide donor construction.')
    # У: optically move the two diagonal branches inward, preserving the serif spans.
    g=deepcopy(font['glyf'][cm[ord('У')]])
    for i,(x,y) in enumerate(g.coordinates):
     if i<=33:
      dx=round(-50-100*min(max(y,0),620)/620)
     else:dx=round(-50*max(0,1-y/720))
     g.coordinates[i]=(x+dx,y)
     # The source 14-unit serif is brought to the Latin 23-unit terminal thickness.
     if y==706:g.coordinates[i]=(x+dx,697)
    font['glyf'][cm[ord('У')]]=g;g.recalcBounds(font['glyf']);font['hmtx'][cm[ord('У')]]=(535,g.xMin);changes['У']='Move diagonal branches inward independently; preserve stroke runs and bring terminal thickness to 23 units.'
    # Ф: horizontally open the O counters without scaling the side-stroke widths.
    og=deepcopy(font['glyf'][cm[ord('O')]])
    for i,(x,y) in enumerate(og.coordinates):og.coordinates[i]=(x+round(30*max(-1,min(1,(x-270)/90))),y)
    temporary('__temporary_phi_bowl',og);phi_bowl=move(skPathFromGlyph('__temporary_phi_bowl',font.getGlyphSet()),30)
    ig=deepcopy(font['glyf'][cm[ord('I')]])
    for i,(x,y) in enumerate(ig.coordinates):
     if y>=654:ig.coordinates[i]=(x,y+105)
     elif y<=66:ig.coordinates[i]=(x,y-100)
    temporary('__temporary_phi_stem',ig)
    save('Ф',union(phi_bowl,move(skPathFromGlyph('__temporary_phi_stem',font.getGlyphSet()),175.5)),600,'O curve/counter logic with native I ascender/descender stem; width 915 to 600.')
    # Ц/Ш/Щ: repeated native stems with a single consistent bottom-bar/descender system.
    def tail(x,depth=110):return polygon([(x-21,25),(x+4,25),(x+12,-depth),(x-9,-depth)])
    cu=union(I,move(I,297),box(89,0,457,25));save('Ц',union(cu,tail(523)),564,'Two native I stems, 25-unit base and short tapered descender.')
    sha=union(I,move(I,232),move(I,464),box(89,0,624,25));save('Ш',sha,713,'Three Latin I stems and a native 25-unit base; width 1127 to 713.')
    save('Щ',union(sha,tail(690)),732,'Same body as Ш with the shared short descender.')
    # Ч: lift the native U bowl, shorten its straight stems, add an I stem on the right.
    ug=deepcopy(font['glyf'][cm[ord('U')]])
    for i,(x,y) in enumerate(ug.coordinates):
     if y<=192:ug.coordinates[i]=(x,y+300)
    temporary('__temporary_che_bowl',ug)
    che=skPathFromGlyph('__temporary_che_bowl',font.getGlyphSet());che=intersect(che,box(-100,-50,422,760));save('Ч',union(che,move(I,333)),587,'Native U bowl with shortened left arm, and Latin I right stem; replaces the heavy donor join.')
    # Ю/Я: actual O and R curve systems.
    save('Ю',union(I,move(paths['O'],230),box(145,358,290,388)),770,'Latin I and O linked by the H crossbar thickness; width 1134 to 770.')
    save('Я',paths['R'].transform(-1,0,0,1,513,0),513,'Reflected native R construction; native bowl, leg and serif proportions.')
    # Lowercase: keep all shared Latin outlines and rebuild only inconsistent donor forms.
    for ch,latin in [('й','ŭ'),('ѝ','ù')]:
     font['glyf'][cm[ord(ch)]]=deepcopy(font['glyf'][cm[ord(latin)]]);font['hmtx'][cm[ord(ch)]]=font['hmtx'][cm[ord(latin)]];changes[ch]='Exactly the corresponding native Latin u accent; same base as Cyrillic и.'
    # б: shorten the curved ascender; retain the original lower bowl and Bulgarian flag.
    g=font['glyf'][cm[ord('б')]]
    ys={6:560,7:650,8:705,9:720,10:731,11:733,12:737,13:740,14:740,15:740,16:737,17:720,18:694,19:682,20:641,21:598,22:581,23:576,24:572,25:565,26:560,27:551,28:530,29:495,30:480,31:455}
    for i,y in ys.items():x,_=g.coordinates[i];g.coordinates[i]=(x,y)
    changes['б']='Refit the curved Bulgarian ascender to the native 740-unit Latin height; preserve lower bowl.'
    # д/з: shorten the large lower loops, retaining their bottom hairline dimensions.
    g=font['glyf'][cm[ord('д')]]
    for i in range(15):x,y=g.coordinates[i];g.coordinates[i]=(x,y+166)
    for i,y in {15:-120,16:-55,24:-55,25:-95,26:-135,27:-205}.items():x,_=g.coordinates[i];g.coordinates[i]=(x,y)
    for i in [19,20,21,22,23,24,25]:x,y=g.coordinates[i];g.coordinates[i]=(x+8,y)
    font['hmtx'][cm[ord('д')]]=(483,39);changes['д']='Shorter -205-unit descender loop, 68-unit right stem and less excess right-side spacing.'
    g=font['glyf'][cm[ord('з')]]
    for i in range(15):x,y=g.coordinates[i];g.coordinates[i]=(x,y+166)
    for i,y in {12:-180,15:-110,16:-55,59:-22,60:-55,61:-105,62:-155,63:-205}.items():x,_=g.coordinates[i];g.coordinates[i]=(x,y)
    changes['з']='Shorter -205-unit lower loop with a slightly stronger bottom hairline.'
    # г: controlled upper overshoot and less fragile entry hairline.
    g=font['glyf'][cm[ord('г')]]
    for i in [8,9,10,11]:x,y=g.coordinates[i];g.coordinates[i]=(x,y-18)
    for i in [16,17,18]:x,y=g.coordinates[i];g.coordinates[i]=(x,y-11)
    for i in [0,1]:x,y=g.coordinates[i];g.coordinates[i]=(x,y-6)
    for i,x in {4:65,5:64,6:46,7:47}.items():_,y=g.coordinates[i];g.coordinates[i]=(x,y)
    changes['г']='Calmer upper overshoot and a stronger entry hairline; cursive Bulgarian construction retained.'
    # л: retain the thin-left/thick-right lambda construction using native v strokes.
    save('л',paths['v'].transform(-1,0,0,-1,413,510),433,'Native v stroke and terminal system rotated into the Bulgarian lambda form; width 495 to 433.')
    # н: native short stems from n, with a controlled crossbar.
    nstem=union(intersect(paths['n'],box(-100,-20,200,100)),intersect(paths['n'],box(-100,100,150,550)))
    save('н',union(nstem,move(nstem,238),box(130,250,325,275)),454,'Latin n stem/serif system and 25-unit crossbar; width 558 to 454.')
    # ц/ш/щ: native Bulgarian u system, with coherent stem widths and small descenders.
    u=paths['u'];low_sha=union(u,move(u,242))
    def low_tail(x):return polygon([(x-18,22),(x+7,22),(x+13,-130),(x-8,-130)])
    save('ц',union(u,low_tail(430)),469,'Latin u body (same as и) with a 130-unit descender.')
    save('ш',low_sha,696,'Two overlapping native u constructions give three 68-unit stems and consistent cups.')
    save('щ',union(low_sha,low_tail(672)),715,'Same body as ш with the shared short descender.')
    # ч: lift the u bowl and retain a native n right stem down to baseline.
    ug=deepcopy(font['glyf'][cm[ord('u')]])
    for i,(x,y) in enumerate(ug.coordinates):
     if y<=200:ug.coordinates[i]=(x,y+220)
    temporary('__temporary_low_che',ug)
    lowche=intersect(skPathFromGlyph('__temporary_low_che',font.getGlyphSet()),box(-100,0,380,560));save('ч',union(lowche,move(nstem,238)),454,'Native u mid-bowl and n right stem; removes the weaker donor stem system.')
    # ф: native o bowl with opened counters and native l/p stem/descender.
    og=deepcopy(font['glyf'][cm[ord('o')]])
    for i,(x,y) in enumerate(og.coordinates):og.coordinates[i]=(x+round(48*max(-1,min(1,(x-203)/65))),y)
    temporary('__temporary_low_phi',og)
    small_phi_bowl=move(skPathFromGlyph('__temporary_low_phi',font.getGlyphSet()),48)
    ls=move(paths['l'],143);ps=move(intersect(paths['p'],box(-100,-240,200,10)),144)
    save('ф',union(small_phi_bowl,ls,ps),532,'Native o counter/curve system and l/p 68-unit stem; 740/-205 extenders replace 958/-363.')
    save('ю',union(paths['l'],move(paths['o'],220),box(130,245,250,270)),628,'Native l/o construction and 25-unit link; ascender 740 instead of 958.')
    # м/ь/ъ/я: retain identity, align terminal/hairline and stem dimensions locally.
    g=font['glyf'][cm[ord('м')]]
    for i,(x,y) in enumerate(g.coordinates):
     if y==16:g.coordinates[i]=(x,23)
    changes['м']='Increase only the baseline serif surfaces from 16 to 23 units, matching native terminal logic.'
    g=font['glyf'][cm[ord('ь')]]
    for i in [17,18,19,20,21]:x,y=g.coordinates[i];g.coordinates[i]=(x+6,y)
    changes['ь']='Right edge of the straight stem moved by 6 units to a 68-unit stem; bowl identity retained.'
    g=font['glyf'][cm[ord('ъ')]]
    for i in [32,33,34,35]:x,y=g.coordinates[i];g.coordinates[i]=(x+8,y)
    changes['ъ']='Local upright-stem widening to 68 units; Bulgarian entry hook and lower bowl retained.'
    g=font['glyf'][cm[ord('я')]]
    for i in [48,49,50,51,52,53,54,55,56,57,58,59]:x,y=g.coordinates[i];g.coordinates[i]=(x+7,y)
    for i in [70,71,72]:x,y=g.coordinates[i];g.coordinates[i]=(x,y-5)
    for i,(x,y) in enumerate(g.coordinates):
     if y==16:g.coordinates[i]=(x,23)
    font['hmtx'][cm[ord('я')]]=(468,-2);changes['я']='68-unit right stem, stronger upper-counter hairline and 23-unit baseline terminals.'
    # Resolve contour overlaps only in edited glyphs; leave every Latin glyph untouched.
    from fontTools.ttLib.removeOverlaps import removeOverlaps
    removeOverlaps(font,[cm[ord(c)] for c in changes],removeHinting=True)
    # Remove zero-length segments introduced by integer rounding of the boolean paths.
    for ch in changes:
     g = font['glyf'][cm[ord(ch)]]
     if not g.isComposite():
      pts=[];flags=[];ends=[];start=0
      for end in g.endPtsOfContours:
       local=[];local_flags=[]
       for i in range(start,end+1):
        xy=g.coordinates[i];flag=g.flags[i]
        if local and xy==local[-1] and local_flags[-1]&1:continue
        local.append(xy);local_flags.append(flag)
       if len(local)>1 and local[0]==local[-1] and local_flags[0]&1 and local_flags[-1]&1:
        local.pop();local_flags.pop()
       pts.extend(local);flags.extend(local_flags);ends.append(len(pts)-1);start=end+1
      g.coordinates=GlyphCoordinates(pts);g.flags=array('B',flags);g.endPtsOfContours=ends
    for ch in changes:
     g=font['glyf'][cm[ord(ch)]];g.recalcBounds(font['glyf']);aw,_=font['hmtx'][cm[ord(ch)]];font['hmtx'][cm[ord(ch)]]=(aw,g.xMin)
    for name in list(font['glyf'].glyphs):
     if name.startswith('__temporary_'):
      del font['glyf'].glyphs[name];del font['hmtx'].metrics[name]
    font.setGlyphOrder(original_order)
    for nid,value in {3:'Lirena Regular 0.500',5:'Version 0.500'}.items():
     for rec in font['name'].names:
      if rec.nameID==nid:rec.string=value.encode(rec.getEncoding())
    # Pair-specific compensation for edited shapes; the original Latin lookup is untouched.
    from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
    pair_corrections = {'АД': 16, 'АЛ': 13, 'АУ': 33, 'АЯ': 22, 'Ал': 7, 'Ам': 10, 'Ан': 4, 'Аю': 11, 'Ая': 22, 'Гз': 10, 'Жх': 15, 'КД': 18, 'КЛ': 15, 'КЯ': 25, 'Кл': 9, 'Км': 12, 'Кн': 31, 'Кю': 13, 'Кя': 24, 'ЛА': 13, 'ЛУ': 9, 'Тз': 17, 'лА': 13, 'мА': 9, 'нА': 4, 'хЯ': 9, 'хя': 8, 'чА': 4}
    if pair_corrections:
     temp = deepcopy(font)
     fea = 'languagesystem cyrl dflt; languagesystem cyrl BGR; feature kern {\n'
     for pair,delta in pair_corrections.items():fea += f'pos {cm[ord(pair[0])]} {cm[ord(pair[1])]} {delta};\n'
     fea += '} kern;'
     addOpenTypeFeaturesFromString(temp, fea)
     table = font['GPOS'].table
     indices = []
     for lookup in temp['GPOS'].table.LookupList.Lookup:
      indices.append(len(table.LookupList.Lookup));table.LookupList.Lookup.append(deepcopy(lookup))
     table.LookupList.LookupCount = len(table.LookupList.Lookup)
     cyrl_features = set()
     latin_features = set()
     for script in table.ScriptList.ScriptRecord:
      langs = [script.Script.DefaultLangSys]+[r.LangSys for r in script.Script.LangSysRecord]
      for lang in langs:
       if lang is not None:
        (cyrl_features if script.ScriptTag=='cyrl' else latin_features).update(lang.FeatureIndex)
     for idx in cyrl_features:
      rec = table.FeatureList.FeatureRecord[idx]
      if rec.FeatureTag=='kern':
       assert idx not in latin_features
       rec.Feature.LookupListIndex.extend(indices)
       rec.Feature.LookupCount=len(rec.Feature.LookupListIndex)
    font['head'].fontRevision=.5
    return changes

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Choose a separate output path; the input is never overwritten.')
    font = TTFont(args.input, recalcTimestamp=False)
    changes = refine_full(font)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    font.save(args.output)
    font.flavor = 'woff2'
    font.save(args.output.with_suffix('.woff2'))
    print(f'Refined {len(changes)} Cyrillic glyphs; Latin preserved.')
