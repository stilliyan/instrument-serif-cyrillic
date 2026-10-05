"""Regular 0.530 — soften reviewed joins while retaining Instrument Serif contrast."""
from pathlib import Path
from copy import deepcopy
import json,pathops
from array import array
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.ttLib.removeOverlaps import skPathFromGlyph

PRESERVED_V_051 = [('moveTo', ((221, -9),)), ('qCurveTo', ((272, -9), (354, 60), (401, 180), (401, 328), (353, 446), (313, 481))), ('qCurveTo', ((275, 514), (227, 516))), ('qCurveTo', ((282, 538), (350, 607), (350, 655))), ('qCurveTo', ((350, 684), (313, 722), (252, 740), (217, 740))), ('qCurveTo', ((153, 740), (76, 632), (41, 416), (41, 254))), ('qCurveTo', ((41, 180), (89, 60), (170, -9), (221, -9))), ('closePath', ()), ('moveTo', ((221, 16),)), ('qCurveTo', ((117, 16), (117, 254))), ('qCurveTo', ((117, 491), (325, 491), (325, 254))), ('qCurveTo', ((325, 16), (221, 16))), ('closePath', ()), ('moveTo', ((113, 522),)), ('qCurveTo', ((115, 555), (128, 621), (153, 676), (191, 711), (217, 714))), ('qCurveTo', ((244, 716), (278, 692), (278, 657))), ('qCurveTo', ((278, 627), (248, 580), (199, 546), (141, 525), (113, 522))), ('closePath', ()), ('moveTo', ((112, 464),)), ('qCurveTo', ((113, 472), (113, 479))), ('qCurveTo', ((121, 480), (131, 482))), ('lineTo', ((130, 481),)), ('qCurveTo', ((121, 473), (112, 464))), ('closePath', ())]

def refine_soft(f):
    assert abs(f['head'].fontRevision-.52)<.001
    cm=f.getBestCmap();gs=f.getGlyphSet();changes={}
    def box(x1,y1,x2,y2):
     p=pathops.Path();p.moveTo(x1,y1);p.lineTo(x2,y1);p.lineTo(x2,y2);p.lineTo(x1,y2);p.close();return p
    def union(a,b):return pathops.op(a,b,pathops.PathOp.UNION)
    def cut(a,b):return pathops.op(a,b,pathops.PathOp.DIFFERENCE)
    def clip(a,b):return pathops.op(a,b,pathops.PathOp.INTERSECTION)
    def store(c,p,adv,reason):
     pen=TTGlyphPen(None);p.draw(Cu2QuPen(pen,.5,reverse_direction=False));g=pen.glyph();g.recalcBounds(f['glyf']);f['glyf'][cm[ord(c)]]=g;f['hmtx'][cm[ord(c)]]=(adv,g.xMin);changes[c]=reason
    # Re-use native u entry and lower bowls, replace the triangular terminal.
    rec=DecomposingRecordingPen(gs);gs[cm[ord('u')]].draw(rec);u=pathops.Path();pen=u.getPen()
    for op,args in rec.value:
     getattr(pen,op)(*args)
     if op=='lineTo' and args==((380,107),):break
    pen.qCurveTo((380,66),(385,32),(404,23));pen.qCurveTo((420,21),(420,11));pen.qCurveTo((420,0),(404,0));pen.lineTo((326,0));pen.qCurveTo((312,0),(312,14));pen.lineTo((312,50));pen.qCurveTo((312,65),(305,64),(300,58));pen.qCurveTo((263,21),(206,-9),(171,-9));pen.closePath()
    def tail(dx=0):
     p=pathops.Path();p.moveTo(370+dx,60);p.lineTo(390+dx,60);p.cubicTo(414+dx,30,438+dx,-63,435+dx,-130);p.lineTo(415+dx,-130);p.cubicTo(419+dx,-69,398+dx,-3,370+dx,40);p.close();return p
    store('ц',union(u,tail()),460,'Native u bowls with a gently bracketed exit and a continuously curved descender; remove the triangular terminal.')
    # One continuous three-stem outline, with no duplicated middle exit.
    sha=pathops.Path();pen=sha.getPen()
    for op,args in rec.value:
     if op=='lineTo' and args==((380,107),):break
     getattr(pen,op)(*args)
    pen.lineTo((380,122));pen.qCurveTo((380,76),(415,37),(446,37));pen.qCurveTo((477,37),(525,72),(554,131),(554,166));pen.lineTo((554,449));pen.qCurveTo((554,467),(543,481),(529,482));pen.lineTo((512,484));pen.qCurveTo((495,486),(495,497));pen.qCurveTo((495,510),(514,510));pen.lineTo((607,510));pen.qCurveTo((622,510),(622,495));pen.lineTo((622,107))
    pen.qCurveTo((622,66),(627,32),(646,23));pen.qCurveTo((662,21),(662,11));pen.qCurveTo((662,0),(646,0));pen.lineTo((568,0));pen.qCurveTo((554,0),(554,14));pen.lineTo((554,50));pen.qCurveTo((554,65),(547,64),(542,58));pen.qCurveTo((505,21),(448,-9),(413,-9));pen.qCurveTo((388,-9),(342,13),(312,61),(312,101));pen.curveTo((312,83),(310,70),(300,58));pen.qCurveTo((263,21),(206,-9),(171,-9));pen.closePath()
    store('ш',sha,677,'One continuous three-stem outline with matched native u cups and a smooth central lower connection; no duplicated u exit or pasted middle terminal.')
    store('щ',union(sha,tail(242)),702,'Same flowing cups as ш, with a curved descender joined through the final stem.')
    # Native h ascender entry and foot, moved intact to Cyrillic x-height.
    hp=skPathFromGlyph(cm[ord('h')],gs)
    hhead=clip(hp,box(-100,550,142,900)).transform(1,0,0,1,0,-230)
    hfoot=clip(hp,box(-100,-20,214,150));hstem=union(union(hhead,hfoot),box(74,100,142,350))
    nh=union(hstem,hstem.transform(1,0,0,1,242,0));bar=pathops.Path();bar.moveTo(142,232);bar.cubicTo(142,245,145,250,157,250);bar.lineTo(301,250);bar.cubicTo(313,250,316,245,316,232);bar.lineTo(316,289);bar.cubicTo(316,278,313,275,301,275);bar.lineTo(157,275);bar.cubicTo(145,275,142,278,142,289);bar.close();nh=union(nh,bar)
    store('н',nh,470,'Native h head and foot curves retained intact at Cyrillic x-height; 68-unit stems and a thin smoothly bracketed crossbar, replacing the flat square heads.')
    # Hard sign: lower bowl drawn as a continuous D, no inherited b baseline spur.
    stem=hstem;outer=pathops.Path();outer.moveTo(100,350);outer.cubicTo(262,382,411,338,411,190);outer.cubicTo(411,70,309,-9,209,-9);outer.cubicTo(139,-9,100,42,100,80);outer.close()
    hole=pathops.Path();hole.moveTo(142,285);hole.cubicTo(142,311,180,326,211,326);hole.cubicTo(287,326,337,270,337,181);hole.cubicTo(337,88,264,18,210,18);hole.cubicTo(170,18,142,56,142,80);hole.close()
    store('ъ',cut(union(stem,outer),hole),451,'Native-weight upright and bracketed serifs with a flowing lower bowl; remove the b-derived foot spur and clumsy union.')
    # The user prefers the 0.510 в at small sizes: retain its form and weight.
    vp=pathops.Path();pen=vp.getPen()
    for op,args in PRESERVED_V_051:getattr(pen,op)(*args)
    vp=vp.transform(1,0,0,1,-18,0)
    store('в',vp,408,'Restore the user-preferred 0.510 form and stroke weight; translate 18 units left and retain corrected 408-unit advance and 23/25 sidebearings.')
    for rec in f['name'].names:
     if rec.nameID in [3,5]:rec.string=({3:'Lirena Regular 0.530',5:'Version 0.530'}[rec.nameID]).encode(rec.getEncoding())
    f['head'].fontRevision=.53
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

    corrections={'Ан': -4, 'Кн': -4, 'Мн': 17, 'Нн': 12, 'Он': 11, 'Сн': 14, 'Тн': 40, 'Тц': 4, 'Тш': 4, 'Тщ': 4, 'Хн': 6, 'ен': 5, 'кн': -4, 'нА': -12, 'нВ': -8, 'нЕ': -8, 'нК': -8, 'нМ': -8, 'нН': -8, 'нО': -4, 'нР': -8, 'нС': -4, 'нТ': -8, 'на': -6, 'нб': -8, 'нв': -8, 'не': -8, 'ни': -8, 'нк': -14, 'нн': -14, 'но': -8, 'нп': -8, 'нр': -8, 'нс': -8, 'нт': -8, 'ну': -18, 'нх': -12, 'нц': -8, 'нш': -8, 'нщ': -8, 'пн': -6, 'тн': -6, 'ун': -9, 'хн': -6, 'цВ': 9, 'цЕ': 9, 'цК': 9, 'цМ': 9, 'цН': 9, 'цО': 9, 'цР': 9, 'цС': 9, 'цТ': 9, 'цХ': 9, 'ца': 9, 'цб': 9, 'цв': 9, 'це': 9, 'ци': 9, 'цк': 9, 'цн': 9, 'цо': 9, 'цп': 9, 'цр': 9, 'цс': 9, 'цт': 9, 'цу': 7, 'цх': 9, 'цц': 9, 'цш': 9, 'цщ': 9, 'шА': 19, 'шВ': 19, 'шЕ': 19, 'шК': 19, 'шМ': 19, 'шН': 19, 'шО': 19, 'шР': 19, 'шС': 19, 'шТ': 19, 'шХ': 19, 'ша': 19, 'шб': 19, 'шв': 19, 'ше': 19, 'ши': 19, 'шк': 19, 'шн': 19, 'шо': 19, 'шп': 19, 'шр': 19, 'шс': 19, 'шт': 19, 'шу': 19, 'шх': 19, 'шц': 19, 'шш': 19, 'шщ': 19, 'щА': 6, 'щВ': 13, 'щЕ': 13, 'щК': 13, 'щМ': 13, 'щН': 13, 'щО': 13, 'щР': 13, 'щС': 13, 'щТ': 13, 'щХ': 13, 'ща': 13, 'щб': 13, 'щв': 13, 'ще': 13, 'щи': 13, 'щк': 13, 'щн': 13, 'що': 13, 'щп': 13, 'щр': 13, 'щс': 13, 'щт': 13, 'щу': 13, 'щх': 13, 'щц': 13, 'щш': 13, 'щщ': 13}
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

