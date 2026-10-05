"""Regular 0.560: optical lowercase ha and a matching soft-sign bowl."""
from copy import deepcopy
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen

PAIR_CORRECTIONS = {'Аь': 11, 'Гь': 90, 'Дь': -25, 'Кь': 39, 'Ль': -13, 'Ть': 90, 'ль': -13, 'мь': -17, 'уь': 1, 'ъь': -31, 'Ах': 52, 'Кх': 58, 'Мх': 4, 'Хх': 37, 'хА': 16, 'хх': 16, 'ьь': -31, 'ъх': -5, 'ьх': -5}

def refine_rhythm(f):
    assert abs(f['head'].fontRevision-.551)<.0001
    cm=f.getBestCmap()
    # Keep native Latin x intact. Adapt only its Cyrillic copy: the central
    # diagonal span is shortened 30 units while complete terminal zones stay
    # 23 units high. A 3% horizontal reduction brings the middle stroke closer
    # to the native 68-unit stem. Modest sidebearing room prevents serif crowding.
    name=cm[ord('х')];g=deepcopy(f['glyf'][name])
    for i,(x,y) in enumerate(g.coordinates):
        ny=y if y<=91 else y-30 if y>=433 else 91+(y-91)*312/342
        g.coordinates[i]=(round(190+(x-190)*.97+4),round(ny))
    g.recalcBounds(f['glyf']);f['glyf'][name]=g;f['hmtx'][name]=(393,g.xMin)
    # Share the approved ъ upper shoulder, right bowl, counter and native head.
    # ь keeps its curled lower-left return without the hard sign's left footer.
    source=DecomposingRecordingPen(f.getGlyphSet());f.getGlyphSet()[cm[ord('ъ')]].draw(source)
    rec=source.value;out=TTGlyphPen(None);out.moveTo((142,339))
    for op,args in rec[6:13]:getattr(out,op)(*args)
    out.lineTo((74,87));out.qCurveTo((74,36),(98,3),(157,-9),(211,-9))
    for op,args in rec[3:6]:getattr(out,op)(*args)
    out.closePath()
    for op,args in rec[19:]:getattr(out,op)(*args)
    name=cm[ord('ь')];g=out.glyph();g.recalcBounds(f['glyf']);f['glyf'][name]=g;f['hmtx'][name]=(451,g.xMin)
    # A true 20-unit round cap replaces the short flat bottom of both tails.
    # Keep the body and upper descender exact; align the final curve tangents
    # vertically into two circular quarter arcs, retaining the -130 baseline.
    for ch,dx in [('ц',0),('щ',242)]:
        name=cm[ord(ch)];recorder=DecomposingRecordingPen(f.getGlyphSet());f.getGlyphSet()[name].draw(recorder)
        tail=recorder.value
        start=next(i for i,(op,args) in enumerate(tail) if op=='qCurveTo' and args[-1]==(445+dx,-126))
        end=next(i for i,(op,args) in enumerate(tail[start:],start) if op=='qCurveTo' and args[-1]==(448+dx,38))
        out=TTGlyphPen(None);p=Cu2QuPen(out,.25,reverse_direction=False)
        for op,args in tail[:start]:getattr(p,op)(*args)
        p.curveTo((435+dx,-35),(445+dx,-85),(445+dx,-120))
        p.curveTo((445+dx,-125.52285),(449.47715+dx,-130),(455+dx,-130))
        p.curveTo((460.52285+dx,-130),(465+dx,-125.52285),(465+dx,-120))
        p.curveTo((465+dx,-85),(459+dx,5),(448+dx,38))
        for op,args in tail[end+1:]:getattr(p,op)(*args)
        g=out.glyph();g.recalcBounds(f['glyf']);f['glyf'][name]=g
    if PAIR_CORRECTIONS:
        from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
        temp=deepcopy(f)
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
        if record.nameID in [3,5]:record.string=({3:'Lirena Regular 0.560',5:'Version 0.560'}[record.nameID]).encode(record.getEncoding())
    f['head'].fontRevision=.56
    return {'ц':'Continuous 20-unit round terminal cap, with vertical tangent joins and bottom retained at -130. Approved body and upper flare retained.','щ':'Same rounded terminal as ц, translated 242 units; approved three-stem body retained.','х':'Cyrillic-only optical adaptation of native x: top 510 to 480, original terminal thickness preserved, central diagonals shortened and width reduced 3%; sidebearings opened. Original Latin x untouched.','ь':'Share approved ъ head, upper shoulder, right oval and counter; align top at 510 and bowl at 350/-9. Keep a curled lower-left return and no left foot. Shared 68-unit stem, 75-unit right stroke, 25-unit hairlines and advance 451.'}
