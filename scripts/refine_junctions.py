"""Regular 0.540: continuous descenders and clean phi bowl/stem junctions."""
from copy import deepcopy
import pathops
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.ttLib.removeOverlaps import skPathFromGlyph

def refine_junctions(f):
    assert abs(f['head'].fontRevision-.53)<.001
    cm=f.getBestCmap();gs=f.getGlyphSet();changes={}
    def box(x1,y1,x2,y2):
        p=pathops.Path();p.moveTo(x1,y1);p.lineTo(x2,y1);p.lineTo(x2,y2);p.lineTo(x1,y2);p.close();return p
    def union(a,b):return pathops.op(a,b,pathops.PathOp.UNION)
    def clip(a,b):return pathops.op(a,b,pathops.PathOp.INTERSECTION)
    def store(c,p,reason):
        pen=TTGlyphPen(None);p.draw(Cu2QuPen(pen,.35,reverse_direction=False));g=pen.glyph();g.recalcBounds(f['glyf']);f['glyf'][cm[ord(c)]]=g
        aw,_=f['hmtx'][cm[ord(c)]];f['hmtx'][cm[ord(c)]]=(aw,g.xMin);changes[c]=reason
    # One contour: final stem flows directly into the outer descender edge.
    # Both outer cubic pieces share tangent (15,-41) at y=0; no boolean splice.
    for c,dx in [('ц',0),('щ',242)]:
        rec=DecomposingRecordingPen(gs);gs[cm[ord(c)]].draw(rec)
        # Preserve every original native bowl/stem segment before the exit.
        p=pathops.Path();pen=p.getPen()
        # The old outline starts at the lower left cup and runs into its exit.
        # Rewrite the contiguous terminal/tail run, retaining the full remainder.
        values=rec.value;start=next(i for i,(op,args) in enumerate(values) if op=='qCurveTo' and args[-1]==(312+dx,50))
        end=next(i for i,(op,args) in enumerate(values) if op=='lineTo' and args==((380+dx,495),))
        # Existing outline runs from inner foot through tail to final stem.
        for op,args in values[:start+1]:getattr(pen,op)(*args)
        pen.lineTo((312+dx,14));pen.qCurveTo((312+dx,0),(326+dx,0));pen.lineTo((374+dx,0))
        pen.curveTo((388+dx,0),(393+dx,-21),(400+dx,-41))
        pen.curveTo((410+dx,-77),(417+dx,-101),(415+dx,-126))
        pen.qCurveTo((415+dx,-130),(419+dx,-130));pen.lineTo((431+dx,-130));pen.qCurveTo((435+dx,-130),(435+dx,-126))
        pen.curveTo((433+dx,-99),(419+dx,-41),(404+dx,0))
        pen.curveTo((389+dx,41),(380+dx,67),(380+dx,107))
        for op,args in values[end:]:getattr(pen,op)(*args)
        store(c,p,'Preserve native cups and three/two stems; draw one continuous curved exit into the descender, with matching tangents and a softly rounded tip. Remove the intersecting tail/terminal splice.')
    # Use original o bowls and genuine l/p extenders. Do not carry the l foot
    # or p bowl through the baseline junction; they caused the pointed tabs.
    og=deepcopy(f['glyf'][cm[ord('o')]])
    for i,(x,y) in enumerate(og.coordinates):og.coordinates[i]=(x+round(48*max(-1,min(1,(x-203)/65))),y)
    temp=deepcopy(f);temp['glyf']['__phi_bowl']=og;temp['hmtx']['__phi_bowl']=(532,23);temp.setGlyphOrder(f.getGlyphOrder()+['__phi_bowl'])
    bowl=skPathFromGlyph('__phi_bowl',temp.getGlyphSet()).transform(1,0,0,1,48,0)
    upper=clip(skPathFromGlyph(cm[ord('l')],gs),box(-100,100,500,900)).transform(1,0,0,1,143,0)
    lower=clip(skPathFromGlyph(cm[ord('p')],gs),box(-100,-240,500,-30)).transform(1,0,0,1,144,0)
    phi=union(union(union(bowl,upper),lower),box(217,-138,285,640))
    store('ф',phi,'Temporary native bowl/stem union.')
    # Small tangent fillets at the outer lower bowl/stem shoulders. The
    # untouched remainder is the exact native quadratic o curve, split at .2.
    rec=DecomposingRecordingPen(f.getGlyphSet());f.getGlyphSet()[cm[ord('ф')]].draw(rec)
    smooth=pathops.Path();pen=smooth.getPen();skip=False
    for op,args in rec.value:
        if skip:
            assert op=='qCurveTo' and args==((349,-2),(386,26));skip=False;continue
        if op=='lineTo' and args==((285,-8),):
            pen.lineTo((285,-32));pen.curveTo((285,-19),(295,-7.296),(309.52,-4.72));pen.qCurveTo((356.4,3.6),(386,26));skip=True
        elif op=='qCurveTo' and args==((153,-2),(217,-8)):
            pen.qCurveTo((145.8,3.6),(192.52,-4.72));pen.curveTo((207,-7.299),(217,-19),(217,-32))
        else:getattr(pen,op)(*args)
    store('ф',smooth,'Native o bowl and 68-unit l/p stem; remove inherited footer/bowl tabs and add tangent-matched rounded lower shoulder joins. Preserve the original rounded p descender foot.')
    for rec in f['name'].names:
        if rec.nameID in [3,5]:rec.string=({3:'Lirena Regular 0.540',5:'Version 0.540'}[rec.nameID]).encode(rec.getEncoding())
    f['head'].fontRevision=.54
    return changes
