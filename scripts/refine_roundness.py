"""Regular 0.551: redraw the hard-sign bowl and balance the phi footer."""
import pathops
from copy import deepcopy
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString

PAIR_CORRECTIONS = {'цА':26,'цД':19,'цЯ':6,'цз':4,'цх':14,'щА':24,'щД':19,'щЯ':6,'щз':4,'щх':14}
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen

def refine_roundness(f):
    assert abs(f['head'].fontRevision-.54)<.001
    name=f.getBestCmap()[ord('ъ')];gs=f.getGlyphSet();rec=DecomposingRecordingPen(gs);gs[name].draw(rec)
    p=pathops.Path();pen=p.getPen()
    # Complete outer bowl. Match Instrument Serif P's 75-unit side stroke and
    # 25-unit hairlines; use continuous elliptical quarters at the right turn.
    pen.moveTo((27,0));pen.lineTo((128,0));pen.curveTo((151,0),(178,-9),(211,-9))
    pen.curveTo((321.46,-9),(411,71.36),(411,170.5))
    pen.curveTo((411,269.64),(321.46,350),(211,350));pen.curveTo((185,350),(164,346),(142,339))
    # Preserve the exact native h head, left stem and left foot from 0.540.
    start=next(i for i,(op,args) in enumerate(rec.value) if op=='lineTo' and args==((142,494),))
    end=next(i for i,(op,args) in enumerate(rec.value[start:],start) if op=='closePath')
    for op,args in rec.value[start:end+1]:getattr(pen,op)(*args)
    # The full counter is rebuilt too: aligned center and horizontal/vertical
    # tangents, with gently rounded returns into the upright at top and bottom.
    pen.moveTo((142,285));pen.curveTo((142,306),(181,325),(211,325))
    pen.curveTo((280.04,325),(336,255.83),(336,170.5))
    pen.curveTo((336,85.17),(280.04,16),(211,16))
    pen.curveTo((172,16),(142,30),(142,56));pen.closePath()
    out=TTGlyphPen(None);p.draw(Cu2QuPen(out,.25,reverse_direction=False));g=out.glyph();g.recalcBounds(f['glyf']);f['glyf'][name]=g
    aw,_=f['hmtx'][name];f['hmtx'][name]=(aw,g.xMin)
    # Replace only phi's lower p footer with the original centered l footer.
    # The native l foot is translated +143 horizontally and -205 vertically.
    pname=f.getBestCmap()[ord('ф')];prec=DecomposingRecordingPen(f.getGlyphSet());f.getGlyphSet()[pname].draw(prec)
    phi=pathops.Path();pp=phi.getPen();pp.moveTo((163,-205));pp.lineTo((341,-205))
    pp.qCurveTo((353,-205),(353,-194));pp.qCurveTo((353,-184),(342,-182));pp.lineTo((319,-179));pp.qCurveTo((298,-176),(285,-159),(285,-138))
    lo=next(i for i,(op,args) in enumerate(prec.value) if op=='lineTo' and args==((285,-32),))
    hi=next(i for i,(op,args) in enumerate(prec.value[lo:],lo) if op=='lineTo' and args==((217,-138),))
    for op,args in prec.value[lo:hi+1]:getattr(pp,op)(*args)
    pp.qCurveTo((217,-159),(197,-177),(176,-180));pp.lineTo((162,-182));pp.qCurveTo((151,-184),(151,-194));pp.qCurveTo((151,-205),(163,-205));pp.closePath()
    end=next(i for i,(op,args) in enumerate(prec.value[hi:],hi) if op=='closePath')
    for op,args in prec.value[end+1:]:getattr(pp,op)(*args)
    out=TTGlyphPen(None);phi.draw(Cu2QuPen(out,.25,reverse_direction=False));g=out.glyph();g.recalcBounds(f['glyf']);f['glyf'][pname]=g;aw,_=f['hmtx'][pname];f['hmtx'][pname]=(aw,g.xMin)
    # The user proposes native u-like flared exits for lowercase ц/щ.
    # Keep the native triangular underside and blend a thin curved descender
    # into its outer flare. Both tail pieces have matching endpoint tangents.
    for ch,dx in [('ц',0),('щ',242)]:
        tname=f.getBestCmap()[ord(ch)];trec=DecomposingRecordingPen(f.getGlyphSet());f.getGlyphSet()[tname].draw(trec)
        start=next(i for i,(op,args) in enumerate(trec.value) if op=='qCurveTo' and args[-1]==(300+dx,58))
        end=next(i for i,(op,args) in enumerate(trec.value[start:],start) if op=='lineTo' and args==((380+dx,495),))
        tp=pathops.Path();q=tp.getPen()
        for op,args in trec.value[:start+1]:getattr(q,op)(*args)
        q.qCurveTo((306+dx,64),(317+dx,61),(317+dx,53));q.lineTo((317+dx,7));q.qCurveTo((317+dx,-5),(326+dx,-5));q.qCurveTo((332+dx,-5),(341+dx,4))
        # Original u underside, split halfway through its first quadratic.
        q.qCurveTo((355+dx,21),(373.5+dx,33));q.qCurveTo((382.75+dx,39),(395.125+dx,43))
        q.curveTo((407.5+dx,47),(411+dx,35),(423+dx,0));q.curveTo((435+dx,-35),(448+dx,-83),(445+dx,-126))
        q.qCurveTo((445+dx,-130),(449+dx,-130));q.lineTo((461+dx,-130));q.qCurveTo((465+dx,-130),(465+dx,-126))
        q.curveTo((468+dx,-85),(459+dx,5),(448+dx,38));q.curveTo((442+dx,56),(438+dx,69),(426+dx,71))
        q.lineTo((405+dx,74));q.qCurveTo((391+dx,76),(380+dx,89),(380+dx,107))
        for op,args in trec.value[end:]:getattr(q,op)(*args)
        out=TTGlyphPen(None);tp.draw(Cu2QuPen(out,.25,reverse_direction=False));g=out.glyph();g.recalcBounds(f['glyf']);f['glyf'][tname]=g;aw,_=f['hmtx'][tname];f['hmtx'][tname]=(aw,g.xMin)
    # Only ten collision-related Cyrillic pairs need extra clearance. Preserve
    # every existing lookup and the ordinary lowercase body spacing.
    cm=f.getBestCmap();temp=deepcopy(f)
    fea='languagesystem cyrl dflt; languagesystem cyrl BGR; feature kern {\n'+''.join(f'pos {cm[ord(pair[0])]} {cm[ord(pair[1])]} {delta};\n' for pair,delta in PAIR_CORRECTIONS.items())+'} kern;'
    addOpenTypeFeaturesFromString(temp,fea);table=f['GPOS'].table;indices=[]
    for lookup in temp['GPOS'].table.LookupList.Lookup:
        indices.append(len(table.LookupList.Lookup));table.LookupList.Lookup.append(deepcopy(lookup))
    table.LookupList.LookupCount=len(table.LookupList.Lookup);cyrl=set();other=set()
    for record in table.ScriptList.ScriptRecord:
        for lang in [record.Script.DefaultLangSys]+[x.LangSys for x in record.Script.LangSysRecord]:
            if lang:(cyrl if record.ScriptTag=='cyrl' else other).update(lang.FeatureIndex)
    for idx in cyrl:
        record=table.FeatureList.FeatureRecord[idx]
        if record.FeatureTag=='kern':
            assert idx not in other;record.Feature.LookupListIndex.extend(indices);record.Feature.LookupCount=len(record.Feature.LookupListIndex)
    for record in f['name'].names:
        if record.nameID in [3,5]:record.string=({3:'Lirena Regular 0.551',5:'Version 0.551'}[record.nameID]).encode(record.getEncoding())
    f['head'].fontRevision=.551
    return {'ц':'Native u flared exit and triangular underside, continuously extended into a 20-unit curved descender with a rounded tip. Original cups, upper stems and advance retained.','щ':'Same native-style flared exit and continuous descender as ц, translated 242 units. Three-stem body and advance retained.','ф':'Replace the asymmetric p descender footer with the exact native l footer, translated to the descender baseline. Keep a 68-unit stem and balance the 202-unit foot around its center; retain bowl, shoulder fillets, head and advance.','ъ':'Redraw the entire outer bowl and counter with aligned centers, continuous round quarters, curved upper shoulder and tangent-matched returns. Remove the baseline corner and skewed lower turn; retain native h head/left stem/foot, 68-unit upright, 75-unit side stroke, 25-unit hairlines and 451-unit advance.'}
