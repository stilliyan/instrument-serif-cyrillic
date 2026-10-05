"""Regular 0.570: calmer em peaks and a clean small-ve bowl connection."""
from copy import deepcopy
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen

PAIR_CORRECTIONS = {}

def refine_smoothness(f):
    assert abs(f['head'].fontRevision-.56)<.0001
    cm=f.getBestCmap();name=cm[ord('м')];g=deepcopy(f['glyf'][name])
    # Translate the upper construction twelve units: neither width nor the
    # lower serif/stem return is scaled. Leave all coordinates below y=300 exact.
    for i,(x,y) in enumerate(g.coordinates):
        if y>=300:g.coordinates[i]=(x,y-12)
    g.recalcBounds(f['glyf']);f['glyf'][name]=g
    name=cm[ord('в')];record=DecomposingRecordingPen(f.getGlyphSet());f.getGlyphSet()[name].draw(record);rec=record.value
    assert rec[2]==('qCurveTo',((257,514),(209,516)))
    out=TTGlyphPen(None);pen=Cu2QuPen(out,.25,reverse_direction=False)
    for op,args in rec[:2]:getattr(pen,op)(*args)
    # Trim each original quadratic at ten percent and bridge their sharp
    # waist with a small tangent-matched cubic fillet. Keep the rest of the
    # preferred upper loop and every lower-bowl/counter point exact.
    pen.qCurveTo((260.8,510.7),(218.52,515.29))
    pen.curveTo((214.881,515.685),(215.89,518.87),(219.795,520.745))
    pen.qCurveTo((267.4,541.45),(298,572.5));pen.qCurveTo((332,607),(332,655))
    for op,args in rec[4:18]:getattr(pen,op)(*args)
    # Omit the tiny fourth contour: it is an accidental pinhole in the join.
    g=out.glyph();g.recalcBounds(f['glyf']);f['glyf'][name]=g
    if PAIR_CORRECTIONS:
        from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
        temp=deepcopy(f);fea='languagesystem cyrl dflt; languagesystem cyrl BGR; feature kern {\n'+''.join(f'pos {cm[ord(p[0])]} {cm[ord(p[1])]} {v};\n' for p,v in PAIR_CORRECTIONS.items())+'} kern;'
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
        if record.nameID in [3,5]:record.string=({3:'Lirena Regular 0.570',5:'Version 0.570'}[record.nameID]).encode(record.getEncoding())
    f['head'].fontRevision=.57
    return {'м':'Translate the upper construction down 12 units; retain all lower coordinates, original width, advance and serif thickness. Control bound top 527 to 515; pointed ink peaks optically align with adjacent lowercase.','в':'Round the sharp outer waist with a small tangent-matched fillet and remove the triangular pinhole contour. Retain the preferred 0.510 lower oval, both counters, upper loop, width and advance.'}
