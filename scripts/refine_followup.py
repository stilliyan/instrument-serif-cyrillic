"""Regular 0.520: native k, single-contour б/в, consistent spacing and connected tails."""
from pathlib import Path
from copy import deepcopy
import pathops
from array import array
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.ttLib.removeOverlaps import skPathFromGlyph

def refine_followup(f):
    assert abs(f['head'].fontRevision-.51)<.001
    cm=f.getBestCmap();gs=f.getGlyphSet();native={c:skPathFromGlyph(cm[ord(c)],gs) for c in 'oubk'};changes={}
    def box(x1,y1,x2,y2):
     p=pathops.Path();p.moveTo(x1,y1);p.lineTo(x2,y1);p.lineTo(x2,y2);p.lineTo(x1,y2);p.close();return p
    def union(a,b):return pathops.op(a,b,pathops.PathOp.UNION)
    def cut(a,b):return pathops.op(a,b,pathops.PathOp.DIFFERENCE)
    def clip(a,b):return pathops.op(a,b,pathops.PathOp.INTERSECTION)
    def store(c,p,advance,reason):
     pen=TTGlyphPen(None);p.draw(Cu2QuPen(pen,.5,reverse_direction=False));g=pen.glyph();g.recalcBounds(f['glyf']);f['glyf'][cm[ord(c)]]=g;f['hmtx'][cm[ord(c)]]=(advance,g.xMin);changes[c]=reason
    # Preserve native o's exact lower-left/right quadratics and inner counter.
    def bowl_start(p):
     pen=p.getPen();pen.moveTo((203,-9));pen.qCurveTo((152,-9),(71,60),(23,180),(23,254));return pen
    def bowl_finish(pen):
     pen.qCurveTo((254,516),(335,446),(383,328),(383,254));pen.qCurveTo((383,180),(336,60),(254,-9),(203,-9));pen.closePath()
    hole=pathops.Path();pen=hole.getPen();pen.moveTo((203,16));pen.qCurveTo((307,16),(307,254));pen.qCurveTo((307,491),(203,491));pen.qCurveTo((99,491),(99,254));pen.qCurveTo((99,16),(203,16));pen.closePath()
    p=pathops.Path();pen=bowl_start(p)
    pen.curveTo((23,519),(55,651),(170,712));pen.curveTo((226,742),(297,716),(365,740));pen.curveTo((370,742),(371,738),(368,730));pen.lineTo((361,706));pen.curveTo((294,696),(228,699),(178,673));pen.curveTo((113,642),(91,596),(91,477));pen.curveTo((91,450),(107,450),(114,465));pen.curveTo((130,500),(170,516),(203,516));bowl_finish(pen)
    store('б',cut(p,hole),408,'Single flowing outer contour with the native o bowl/counter; rounded shoulder connection, modestly strengthened curved ascender and flag and native o sidebearings.')
    p=pathops.Path();pen=bowl_start(p)
    pen.curveTo((23,588),(71,740),(195,740));pen.curveTo((266,740),(332,710),(332,655));pen.curveTo((332,590),(273,550),(201,526));pen.curveTo((180,519),(179,516),(203,516));bowl_finish(pen)
    upper_hole=pathops.Path();pen=upper_hole.getPen();pen.moveTo((99,535));pen.curveTo((130,540),(264,594),(264,657));pen.curveTo((264,698),(246,714),(195,714));pen.curveTo((132,714),(99,629),(99,535));pen.closePath()
    store('в',cut(cut(p,hole),upper_hole),408,'Single flowing outer contour, smooth waist and native o lower bowl/counter; 68-unit upper right stroke and native o spacing.')
    f['glyf'][cm[ord('к')]]=deepcopy(f['glyf'][cm[ord('k')]]);f['hmtx'][cm[ord('к')]]=f['hmtx'][cm[ord('k')]];changes['к']='Exact original Instrument Serif k outline, hints and metrics, mapped to Bulgarian к.'
    u=native['u']
    def tail(dx=0):
     p=pathops.Path();p.moveTo(410+dx,65);p.lineTo(436+dx,65);p.cubicTo(436+dx,30,446+dx,-68,445+dx,-130);p.lineTo(425+dx,-130);p.cubicTo(425+dx,-74,421+dx,15,410+dx,45);p.close();return p
    # The previous tail started below the raised u exit and was disconnected.
    store('ц',union(u,tail()),469,'Connect the curved descender to the actual raised native u exit, replacing the detached angular stub.')
    first=cut(u,box(380,-20,500,120));sha=union(first,u.transform(1,0,0,1,242,0))
    store('ш',sha,696,'Three native 68-unit u stems; remove the first u exit foot from the second cup to keep both lower curves clean.')
    store('щ',union(sha,tail(242)),715,'Same cleaned cups as ш with a continuously attached curved descender.')
    # Native u heads, k baseline serifs and 68-unit stems; avoid duplicated n entry wedges.
    head=clip(u,box(-100,120,150,550));foot=clip(native['k'],box(-100,-20,216,100)).transform(1,0,0,1,-4,0)
    stem=union(union(head,foot),box(70,50,138,140));right=stem.transform(1,0,0,1,242,0);n=union(union(stem,right),box(130,250,320,275))
    store('н',n,454,'Native flat u head serifs, k baseline serifs and 68-unit stems; controlled 25-unit crossbar without two pointed entry wedges.')
    # Native b bowl with the native u flat entry; remove the oversized wedge flag.
    hard_body=clip(native['b'].transform(1,0,0,.68,8,0),box(-100,-20,550,370))
    store('ъ',union(hard_body,stem),451,'Native b lower bowl at 0.68 height and 68-unit upright stem with the flat native u entry; remove the oversized pointed flag and retain the distinct lower-bowl hard-sign structure.')
    for rec in f['name'].names:
     if rec.nameID in [3,5]:rec.string=({3:'Lirena Regular 0.520',5:'Version 0.520'}[rec.nameID]).encode(rec.getEncoding())
    f['head'].fontRevision=.52
    for ch in changes:
     if ch=='к':continue
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

    corrections={'Аб': -11, 'Ав': -11, 'Ак': 8, 'Ан': 8, 'Ац': -8, 'Аш': -8, 'Ащ': -8, 'Вб': 11, 'Вв': 11, 'Еб': 4, 'Ев': 4, 'Кв': -17, 'Кк': 10, 'Кн': 8, 'Мн': -16, 'Мц': -16, 'Мш': -16, 'Мщ': -16, 'Нб': -9, 'Нв': -8, 'Нн': -12, 'Нц': -12, 'Нш': -12, 'Нщ': -12, 'Об': 17, 'Ов': 17, 'Он': -8, 'Оц': -8, 'Ош': -8, 'Ощ': -8, 'Рб': -18, 'Рв': -18, 'Сн': -12, 'Сц': -12, 'Сш': -12, 'Сщ': -12, 'Тв': -46, 'Тн': 50, 'Тц': 50, 'Тш': 50, 'Тщ': 50, 'Хб': -50, 'Хв': -50, 'Хк': -28, 'Хн': -25, 'Хц': -48, 'Хш': -48, 'Хщ': -48, 'аб': 4, 'ав': 5, 'бб': 8, 'бв': 8, 'бу': -8, 'бх': -14, 'вб': 8, 'вв': 8, 'ву': -8, 'вх': -14, 'еб': 26, 'ев': 20, 'иб': 9, 'ив': 10, 'кА': 23, 'ка': -22, 'кб': -17, 'кв': -17, 'ке': -12, 'ки': -15, 'кк': -10, 'кн': -6, 'ко': -12, 'кп': -10, 'кр': -16, 'кс': -12, 'кт': -10, 'ку': 10, 'кх': 13, 'кц': -15, 'кш': -15, 'кщ': -15, 'нА': 17, 'нб': 9, 'нв': 10, 'нх': 11, 'об': 8, 'ов': 8, 'пб': 9, 'пв': 10, 'пк': -6, 'рб': 8, 'рв': 8, 'сб': 47, 'св': 41, 'тб': 9, 'тв': 10, 'тк': -6, 'уб': -9, 'ув': -9, 'ук': -8, 'хб': -15, 'хв': -15, 'хк': -6, 'цА': -8, 'цВ': -15, 'цЕ': -15, 'цК': -15, 'цМ': -15, 'цН': -15, 'цО': -15, 'цР': -15, 'цС': -15, 'цТ': -15, 'цХ': -15, 'ца': -15, 'цб': -6, 'цв': -5, 'це': -15, 'ци': -15, 'цк': -15, 'цн': -15, 'цо': -15, 'цп': -15, 'цр': -15, 'цс': -15, 'цт': -15, 'цх': -15, 'цц': -15, 'цш': -15, 'цщ': -15, 'шб': 9, 'шв': 10, 'шу': 13, 'щА': -12, 'щВ': -19, 'щЕ': -19, 'щК': -19, 'щМ': -19, 'щН': -19, 'щО': -19, 'щР': -19, 'щС': -19, 'щТ': -19, 'щХ': -19, 'ща': -19, 'щб': -10, 'щв': -9, 'ще': -19, 'щи': -19, 'щк': -19, 'щн': -19, 'що': -19, 'щп': -19, 'щр': -19, 'щс': -19, 'щт': -19, 'щу': -6, 'щх': -19, 'щц': -19, 'щш': -19, 'щщ': -19, 'Аъ': 36, 'Жъ': 21, 'Къ': 60, 'Лъ': 12, 'кЯ': 7, 'лъ': 38, 'мъ': 2, 'нЯ': 6, 'ун': 1, 'уц': 1, 'уш': 1, 'ущ': 1, 'уъ': 1}
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

