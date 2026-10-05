"""Regular 0.580: restrained hard-sign flag and smooth be/tail terminals."""
from copy import deepcopy
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen

PAIR_CORRECTIONS = {'аб': 4, 'ав': 3, 'аг': -9, 'ад': 3, 'аж': -24, 'аз': -24, 'ал': -17, 'ам': -3, 'ач': -24, 'аь': -3, 'аю': -5, 'ая': -13, 'ба': 4, 'бб': 7, 'бв': 9, 'бг': -6, 'бд': 16, 'бе': 4, 'бж': -24, 'бз': -24, 'би': 4, 'бй': -9, 'бк': 10, 'бл': -4, 'бм': 5, 'бн': 16, 'бо': 4, 'бп': 4, 'бр': 4, 'бс': 4, 'бт': 4, 'бу': 4, 'бф': -24, 'бх': 3, 'бц': 4, 'бч': -24, 'бш': 4, 'бщ': 4, 'бъ': 16, 'бь': 16, 'бю': -16, 'бя': -9, 'бѝ': -12, 'ва': 4, 'вб': 16, 'вв': 16, 'вг': -6, 'вд': 16, 'ве': 4, 'вж': -24, 'вз': -24, 'ви': 4, 'вк': 16, 'вл': -4, 'вм': 5, 'вн': 16, 'во': 4, 'вп': 4, 'вр': 4, 'вс': 4, 'вт': 4, 'ву': 4, 'вф': -14, 'вх': 3, 'вц': 4, 'вч': -24, 'вш': 4, 'вщ': 4, 'въ': 16, 'вь': 16, 'вю': -4, 'вя': -9, 'вѝ': -5, 'га': 3, 'гб': 13, 'гв': 13, 'гд': 10, 'ге': 8, 'гж': -12, 'гз': -24, 'ги': 9, 'гй': 9, 'гк': 9, 'гм': 11, 'гн': 10, 'го': 8, 'гп': 9, 'гр': 9, 'гс': 8, 'гт': 9, 'гу': 9, 'гф': 7, 'гх': 8, 'гц': 9, 'гч': -20, 'гш': 9, 'гщ': 9, 'гъ': 8, 'гь': 6, 'гю': 3, 'гя': -10, 'гѝ': 9, 'да': 16, 'дб': 16, 'дв': 16, 'дг': 13, 'дд': 14, 'де': 16, 'дз': -18, 'ди': 16, 'дй': 16, 'дк': 16, 'дл': 10, 'дм': 16, 'дн': 16, 'до': 16, 'дп': 16, 'др': 14, 'дс': 16, 'дт': 16, 'ду': 11, 'дф': 7, 'дх': 16, 'дц': -3, 'дч': -11, 'дш': 16, 'дщ': -16, 'дъ': 16, 'дь': 14, 'дю': 16, 'дя': 4, 'дѝ': 16, 'ег': -7, 'ед': 8, 'еж': -21, 'ез': -24, 'ел': -7, 'еч': -24, 'еь': -3, 'ею': -5, 'ея': -13, 'жа': -21, 'жб': -24, 'жв': -24, 'жг': -24, 'жд': -12, 'же': -20, 'жж': -24, 'жз': -24, 'жи': -20, 'жй': -24, 'жк': -24, 'жл': -24, 'жм': -21, 'жн': -21, 'жо': -23, 'жп': -21, 'жр': -21, 'жс': -20, 'жт': -21, 'жу': -9, 'жф': -24, 'жх': -20, 'жц': -20, 'жч': -24, 'жш': -20, 'жщ': -20, 'жъ': -20, 'жь': -23, 'жю': -24, 'жя': -24, 'жѝ': -24, 'за': -3, 'зг': -13, 'зд': -5, 'зе': -3, 'зж': -24, 'зз': -24, 'зи': -3, 'зй': -3, 'зк': -4, 'зл': -13, 'зм': -3, 'зн': -3, 'зо': -3, 'зп': -4, 'зр': -4, 'зс': -3, 'зт': -4, 'зу': -5, 'зф': -17, 'зх': -8, 'зц': -23, 'зч': -24, 'зш': -3, 'зщ': -24, 'зъ': -4, 'зь': -6, 'зю': -8, 'зя': -17, 'зѝ': -3, 'иг': -10, 'ид': 5, 'иж': -20, 'из': -24, 'ил': -10, 'им': 3, 'ич': -24, 'ию': -5, 'ия': -14, 'йб': -3, 'йг': -10, 'йд': 5, 'йж': -24, 'йз': -24, 'йй': -6, 'йк': -3, 'йл': -6, 'йм': 3, 'йф': -14, 'йч': -24, 'йю': -8, 'йя': -14, 'йѝ': -9, 'кб': 7, 'кв': 7, 'кг': -13, 'кд': 16, 'кж': -18, 'кз': -24, 'ки': 9, 'кй': -6, 'кк': 9, 'км': 4, 'кн': 16, 'кп': 9, 'кт': 9, 'ку': 9, 'кф': -24, 'кц': 9, 'кч': -11, 'кш': 9, 'кщ': 9, 'къ': 16, 'кь': 14, 'кю': 6, 'кя': -9, 'кѝ': -6, 'ла': -9, 'лб': -3, 'лг': -18, 'лж': -24, 'лз': -24, 'ли': -6, 'лй': -6, 'лк': -7, 'лл': -24, 'лн': -7, 'лп': -7, 'лр': -9, 'лт': -7, 'лу': 5, 'лх': 6, 'лц': -6, 'лч': -20, 'лш': -6, 'лщ': -6, 'лъ': 6, 'ль': -7, 'ля': -24, 'лѝ': -6, 'мб': 3, 'мв': 3, 'мг': -12, 'мж': -24, 'мз': -24, 'мл': -9, 'мр': -3, 'му': 3, 'мф': -3, 'мч': -24, 'мъ': 5, 'мю': -5, 'мя': -16, 'нб': 16, 'нв': 16, 'нг': -9, 'нд': 16, 'нж': -24, 'нз': -24, 'нк': 16, 'нл': -11, 'нн': 16, 'нч': -24, 'нъ': 16, 'нь': 16, 'ню': -4, 'ня': -15, 'ов': 3, 'ог': -9, 'од': 6, 'ож': -20, 'оз': -24, 'оч': -24, 'ою': -5, 'оя': -9, 'пб': 3, 'пв': 3, 'пг': -8, 'пд': 7, 'пж': -24, 'пз': -24, 'пл': -9, 'пх': 9, 'пч': -24, 'пь': -3, 'пю': -3, 'пя': -14, 'рв': 3, 'рг': -9, 'рд': -4, 'рж': -20, 'рз': -24, 'рф': -24, 'рц': -24, 'рч': -24, 'рщ': -24, 'рю': -5, 'ря': -9, 'сб': -7, 'св': -7, 'сг': -7, 'сд': 8, 'сж': -21, 'сз': -24, 'сл': -7, 'сч': -24, 'сь': -3, 'сю': -5, 'ся': -14, 'тб': 3, 'тв': 3, 'тг': -8, 'тд': 7, 'тж': -24, 'тз': -24, 'тл': -9, 'тх': 9, 'тч': -24, 'ть': -3, 'тю': -3, 'тя': -14, 'уб': 5, 'ув': 5, 'уг': -10, 'уд': -13, 'уж': -15, 'уз': -24, 'уи': 11, 'уй': 11, 'ул': 5, 'ум': 3, 'уу': 54, 'уф': -24, 'ух': 36, 'уц': 10, 'уч': 6, 'уш': 10, 'ущ': 10, 'уъ': 10, 'уь': -5, 'ую': -10, 'уя': -18, 'уѝ': 11, 'фа': -9, 'фб': -22, 'фв': -21, 'фг': -19, 'фд': -21, 'фе': -9, 'фж': -24, 'фз': -24, 'фи': -9, 'фй': -22, 'фк': -23, 'фл': -11, 'фм': -9, 'фн': -8, 'фо': -9, 'фп': -9, 'фр': -20, 'фс': -9, 'фт': -9, 'фу': -22, 'фф': -24, 'фх': -14, 'фц': -24, 'фч': -24, 'фш': -9, 'фщ': -24, 'фъ': -9, 'фь': -11, 'фю': -24, 'фя': -18, 'фѝ': -24, 'хб': 8, 'хв': 8, 'хг': -11, 'хж': -24, 'хз': -24, 'хл': -4, 'ху': 35, 'хф': -10, 'хх': 10, 'хч': -12, 'хъ': -3, 'хь': -5, 'хя': -18, 'ца': 4, 'цб': 6, 'цв': 5, 'цг': -8, 'цд': 4, 'це': 4, 'цж': -20, 'ци': 4, 'цл': -9, 'цм': 4, 'цн': 3, 'цо': 4, 'цр': 7, 'цс': 4, 'цу': 6, 'цф': -4, 'цх': -4, 'цц': -13, 'цч': -24, 'цш': 4, 'цщ': -24, 'ця': -13, 'чб': 7, 'чв': 7, 'чг': -8, 'чд': 6, 'чж': -20, 'чз': -24, 'чл': -5, 'чм': 4, 'чч': -24, 'чя': -13, 'шг': -5, 'шд': 10, 'шж': -15, 'шз': -24, 'шй': 5, 'шл': -4, 'шм': 8, 'шф': 5, 'шч': -22, 'шъ': 5, 'шь': 3, 'шя': -8, 'шѝ': 5, 'ща': 4, 'щб': 6, 'щв': 5, 'щг': -8, 'щд': 4, 'ще': 4, 'щж': -20, 'щи': 4, 'щл': -9, 'щм': 4, 'щн': 3, 'що': 4, 'щр': 7, 'щс': 4, 'щу': 6, 'щф': -4, 'щх': -4, 'щц': -13, 'щч': -24, 'щш': 4, 'щщ': -24, 'щя': -13, 'ъа': -12, 'ъб': 13, 'ъв': 14, 'ъг': -22, 'ъд': 12, 'ъе': -12, 'ъж': -24, 'ъз': -24, 'ъи': -13, 'ъй': -13, 'ък': 9, 'ъл': -21, 'ъм': -12, 'ън': 9, 'ъо': -12, 'ъп': -12, 'ър': -12, 'ъс': -12, 'ът': -12, 'ъу': -8, 'ъф': -12, 'ъх': -17, 'ъц': -13, 'ъч': -24, 'ъш': -13, 'ъщ': -13, 'ъъ': 16, 'ъь': 15, 'ъю': -17, 'ъя': -24, 'ъѝ': -13, 'ьа': -12, 'ьб': 14, 'ьв': 14, 'ьг': -22, 'ьд': 12, 'ье': -11, 'ьж': -24, 'ьз': -24, 'ьи': -12, 'ьй': -12, 'ьк': 9, 'ьл': -21, 'ьм': -12, 'ьн': 10, 'ьо': -11, 'ьп': -12, 'ьр': -12, 'ьс': -11, 'ьт': -12, 'ьу': -7, 'ьф': -12, 'ьх': -17, 'ьц': -12, 'ьч': -24, 'ьш': -12, 'ьщ': -12, 'ьъ': 16, 'ьь': 15, 'ью': -16, 'ья': -24, 'ьѝ': -12, 'юб': -24, 'юв': -24, 'юг': -10, 'юд': 6, 'юж': -24, 'юз': -24, 'юй': -24, 'юк': -24, 'юф': -24, 'юх': -6, 'юч': -24, 'юю': -24, 'юя': -9, 'юѝ': -24, 'яа': -4, 'яг': -13, 'яе': -3, 'яж': -24, 'яз': -24, 'яи': -4, 'яй': -4, 'як': -3, 'ял': -15, 'ям': -8, 'яо': -3, 'яр': -4, 'яс': -3, 'яу': 7, 'яф': -4, 'ях': -8, 'яц': -4, 'яч': -24, 'яш': -4, 'ящ': -4, 'яъ': -5, 'яь': -7, 'яю': -8, 'яя': -18, 'яѝ': -4, 'ѝб': -7, 'ѝв': -7, 'ѝг': -10, 'ѝд': 5, 'ѝж': -24, 'ѝз': -24, 'ѝй': -10, 'ѝк': -9, 'ѝл': -6, 'ѝм': 3, 'ѝф': -20, 'ѝч': -24, 'ѝю': -13, 'ѝя': -14, 'ѝѝ': -15, 'Ал': 4, 'Ам': 3, 'Ап': 8, 'Ат': 8, 'Ах': 1, 'Аю': 4, 'Кл': 4, 'Км': 3, 'Кп': 34, 'Кт': 34, 'Кх': 1, 'Кю': 4, 'Мх': 1, 'Хп': 7, 'Хт': 7, 'Хх': 1, 'кД': 1, 'кЯ': 1, 'лА': 4, 'лЯ': 1, 'мА': 3, 'пА': 12, 'тА': 12, 'хА': 1, 'яА': 1}

def refine_terminals(f):
    assert abs(f['head'].fontRevision-.57)<.0001
    cm=f.getBestCmap()
    def read(ch):
        p=DecomposingRecordingPen(f.getGlyphSet());f.getGlyphSet()[cm[ord(ch)]].draw(p);return p.value
    def store(ch,draw):
        out=TTGlyphPen(None);pen=Cu2QuPen(out,.25,reverse_direction=False);draw(pen)
        g=out.glyph();g.recalcBounds(f['glyf']);name=cm[ord(ch)];f['glyf'][name]=g
        advance,_=f['hmtx'][name];f['hmtx'][name]=(advance,g.xMin)
    def replay(p,rec):
        for op,args in rec:getattr(p,op)(*args)
    rec=read('Ъ');assert rec[14]==('lineTo',((16,580),))
    def hard_sign(p):
        replay(p,rec[:11]);p.lineTo((129,720))
        p.curveTo((104,720),(91,726),(77,728))
        p.curveTo((68,729),(57,726),(56,710))
        p.lineTo((50,620));p.lineTo((77,620))
        p.curveTo((88,659),(133,697),(155,694));replay(p,rec[17:])
    store('Ъ',hard_sign)
    rec=read('б');assert rec[6]==('lineTo',((368,730),))
    def be(p):
        replay(p,rec[:6])
        # A smooth rounded end replaces the slanted cut and raised cusp.
        p.curveTo((369,707),(370,711),(370,718))
        p.curveTo((370,726),(366,730),(359,730))
        p.curveTo((337,730),(292,728),(269,728));replay(p,rec[9:])
    store('б',be)
    for ch,dx,start,end in [('ц',0,9,13),('щ',242,12,16)]:
        rec=read(ch);assert rec[start-1][1][-1]==(423+dx,0)
        def tail(p,rec=rec,dx=dx,start=start,end=end):
            replay(p,rec[:start])
            # Keep the approved upper flare. A less bowed thin tail reaches
            # a centered round cap ten units to the left of the previous tip.
            p.curveTo((435+dx,-36),(435+dx,-85),(435+dx,-120))
            p.curveTo((435+dx,-125.52285),(439.47715+dx,-130),(445+dx,-130))
            p.curveTo((450.52285+dx,-130),(455+dx,-125.52285),(455+dx,-120))
            p.curveTo((455+dx,-85),(454+dx,17),(448+dx,38))
            replay(p,rec[end:])
        store(ch,tail)
    # Keep a common native bowl and head, with distinct hard/soft lower returns.
    native=read('b')
    def adapt_xy(pt):
        x,y=pt
        return (x+12,y-230 if y>=640 else y*402/516)
    shared=[(op,tuple(adapt_xy(pt) if pt is not None else None for pt in args)) for op,args in native]
    def soft(p):replay(p,shared)
    store('ь',soft)
    def hard(p):
        p.moveTo((218,-9*402/516))
        p.qCurveTo((180,-9*402/516),(160,0),(128,0));p.lineTo((27,0))
        p.qCurveTo((15,0),(15,11));p.qCurveTo((15,21),(26,23))
        p.lineTo((40,25));p.qCurveTo((61,28),(74,46),(74,67));p.lineTo((74,410))
        # A restrained hard-sign flag distinguishes the head from soft sign.
        p.lineTo((74,463));p.curveTo((74,482),(62,491),(47,491))
        p.curveTo((36,491),(25,470),(21,447));p.lineTo((7,447))
        p.lineTo((11,499));p.curveTo((12,510),(17,513),(27,510))
        p.curveTo((43,505),(58,505),(77,505));p.lineTo((131,505))
        p.qCurveTo((142,505),(142,494));replay(p,shared[14:19]);p.closePath();replay(p,shared[20:])
    store('ъ',hard)
    for ch in 'ъь':f['hmtx'][cm[ord(ch)]]=(451,f['glyf'][cm[ord(ch)]].xMin)
    # Restore twenty units of ha height while keeping terminal thickness intact.
    name=cm[ord('х')];g=deepcopy(f['glyf'][name])
    for i,(x,y) in enumerate(g.coordinates):
        ny=y if y<=91 else y+20 if y>=403 else 91+(y-91)*332/312
        g.coordinates[i]=(x,round(ny))
    g.recalcBounds(f['glyf']);f['glyf'][name]=g
    # Correct de's excessive basic bearings, preserving its exact contour shape.
    name=cm[ord('д')];g=deepcopy(f['glyf'][name]);g.coordinates.translate((-16,0))
    g.recalcBounds(f['glyf']);f['glyf'][name]=g;f['hmtx'][name]=(406,g.xMin)
    # Tighten zhe's basic sidebearings equally, keeping its outline shape exact.
    name=cm[ord('ж')];g=deepcopy(f['glyf'][name]);g.coordinates.translate((-16,0))
    g.recalcBounds(f['glyf']);f['glyf'][name]=g;f['hmtx'][name]=(636,g.xMin)
    # Ya is already at x-height; a modest width reduction quiets its mass.
    name=cm[ord('я')];g=deepcopy(f['glyf'][name])
    for i,(x,y) in enumerate(g.coordinates):g.coordinates[i]=(round(20+(x-20)*.94),y)
    g.recalcBounds(f['glyf']);f['glyf'][name]=g;f['hmtx'][name]=(496,g.xMin)
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
        if record.nameID in [3,5]:record.string=({3:'Lirena Regular 0.580',5:'Version 0.580'}[record.nameID]).encode(record.getEncoding())
    f['head'].fontRevision=.58
    return {'д':'Reduce left bearing 39 to 23 and right bearing 70 to 32; preserve contour shape and height; advance 460 to 406.','х':'Restore optical top from 480 to 500 while retaining terminal thickness and width.','ъ':'Shared 402-unit Instrument-derived bowl; distinct restrained upper-left flag and lower serif.','ь':'Shared ъ bowl, counter and head; distinct curled lower return without a left serif.','я':'Reduce width six percent, preserving height and right-side room.','Ъ':'Reduce flag overhang and depth; soften crest.','б':'Round and level the flag terminal.','ц':'Smooth and straighten the thin descender; round its terminal.','щ':'Identical ц descender, translated 242 units.','ж':'Reduce both basic sidebearings 47 to 31; preserve the exact contour shape; advance 668 to 636.'}
