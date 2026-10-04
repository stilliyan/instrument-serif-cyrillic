from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile, ZIP_DEFLATED
import json
import unicodedata
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'sources'
OUT = ROOT/'build'
OUT.mkdir(exist_ok=True)
FAMILY = 'Lirena'
LOW = 'абвгдежзийклмнопрстуфхцчшщъьюяѝ'
CYR = LOW + LOW.upper()
ALIASES = {'а':'a','е':'e','и':'u','о':'o','п':'n','р':'p','с':'c','т':'m','у':'y','х':'x',
           'А':'A','В':'B','Е':'E','К':'K','М':'M','Н':'H','О':'O','Р':'P','С':'C','Т':'T','Х':'X'}
SX = 1.095

def shape(path, text, features=None):
    hf = hb.Font(hb.Face(Path(path).read_bytes()))
    b = hb.Buffer(); b.add_str(text); b.guess_segment_properties(); b.language = 'bg'
    hb.shape(hf, b, features or {})
    return b

def advance(path, text):
    return sum(p.x_advance for p in shape(path,text,{'kern':True,'liga':False,'calt':False}).glyph_positions)

def merge_layout(original, extra):
    old, new = original.table, extra.table
    lookup_offset = len(old.LookupList.Lookup)
    feature_offset = len(old.FeatureList.FeatureRecord)
    old.LookupList.Lookup.extend(new.LookupList.Lookup)
    old.LookupList.LookupCount = len(old.LookupList.Lookup)
    for record in new.FeatureList.FeatureRecord:
        record.Feature.LookupListIndex = [i+lookup_offset for i in record.Feature.LookupListIndex]
        old.FeatureList.FeatureRecord.append(record)
    old.FeatureList.FeatureCount = len(old.FeatureList.FeatureRecord)
    for record in new.ScriptList.ScriptRecord:
        if record.ScriptTag != 'cyrl': continue
        for lang in [record.Script.DefaultLangSys]+[r.LangSys for r in record.Script.LangSysRecord]:
            if lang is not None:
                lang.FeatureIndex = [i+feature_offset for i in lang.FeatureIndex]
                if lang.ReqFeatureIndex != 0xFFFF: lang.ReqFeatureIndex += feature_offset
        assert not any(r.ScriptTag == 'cyrl' for r in old.ScriptList.ScriptRecord)
        old.ScriptList.ScriptRecord.append(record)
    old.ScriptList.ScriptRecord.sort(key=lambda r:r.ScriptTag)
    old.ScriptList.ScriptCount = len(old.ScriptList.ScriptRecord)
    indexed = sorted(enumerate(old.FeatureList.FeatureRecord),key=lambda x:x[1].FeatureTag)
    remap = {i:j for j,(i,_) in enumerate(indexed)}
    old.FeatureList.FeatureRecord = [r for _,r in indexed]
    for script in old.ScriptList.ScriptRecord:
        for lang in [script.Script.DefaultLangSys]+[r.LangSys for r in script.Script.LangSysRecord]:
            if lang is not None:
                lang.FeatureIndex = sorted(remap[i] for i in lang.FeatureIndex)
                if lang.ReqFeatureIndex != 0xFFFF: lang.ReqFeatureIndex = remap[lang.ReqFeatureIndex]
    return original

regular_source = SRC/'InstrumentSerif-Regular.ttf'
donor_path = SRC/'Cormorant-Regular400.ttf'
regular = TTFont(regular_source)
donor = TTFont(donor_path)
original_regular = TTFont(regular_source)
gs, dgs = regular.getGlyphSet(), donor.getGlyphSet()
cmap = regular.getBestCmap()
order = list(regular.getGlyphOrder())
created = {}
for char in CYR:
    name = f'uni{ord(char):04X}.lyric'
    if char in ALIASES:
        source = cmap[ord(ALIASES[char])]
        record = DecomposingRecordingPen(gs); gs[source].draw(record)
        pen = TTGlyphPen(None); record.replay(pen)
        glyph, metrics = pen.glyph(), regular['hmtx'][source]
    else:
        source = donor.getGlyphName(shape(donor_path,char,{'liga':False,'calt':False}).glyph_infos[0].codepoint)
        vertical = regular['OS/2'].sCapHeight/donor['OS/2'].sCapHeight if char.isupper() else regular['OS/2'].sxHeight/donor['OS/2'].sxHeight
        record = DecomposingRecordingPen(dgs); dgs[source].draw(record)
        pen = TTGlyphPen(None); record.replay(TransformPen(pen,(SX,0,0,vertical,0,0)))
        glyph = pen.glyph(); glyph.recalcBounds(regular['glyf'])
        metrics = (round(donor['hmtx'][source][0]*SX), glyph.xMin)
    regular['glyf'][name] = glyph
    regular['hmtx'][name] = metrics
    order.append(name); created[char] = name
    for table in regular['cmap'].tables:
        if table.isUnicode(): table.cmap[ord(char)] = name
regular.setGlyphOrder(order)

# Generate matching pair spacing; preserve all original Latin layout tables.
fea = 'languagesystem DFLT dflt; languagesystem cyrl dflt; languagesystem cyrl BGR;\nfeature kern {\n'
pairs = 0
for a in CYR:
    for b in CYR:
        if a in ALIASES and b in ALIASES:
            la,lb = ALIASES[a],ALIASES[b]
            value = advance(regular_source,la+lb)-advance(regular_source,la)-advance(regular_source,lb)
        else:
            value = round((advance(donor_path,a+b)-advance(donor_path,a)-advance(donor_path,b))*SX)
        value = max(-100,min(80,value))
        if abs(value) >= 5:
            fea += f'pos {created[a]} {created[b]} {value};\n'; pairs += 1
fea += '} kern;\n'
old_gpos,old_gsub,old_gdef = deepcopy(regular['GPOS']),deepcopy(regular['GSUB']),deepcopy(regular['GDEF'])
addOpenTypeFeaturesFromString(regular,fea)
regular['GPOS'] = merge_layout(old_gpos,regular['GPOS'])
regular['GSUB'],regular['GDEF'] = old_gsub,old_gdef

italic_path = ROOT/'build/Lirena-Italic.ttf'
italic = TTFont(italic_path)
if 'GDEF' not in italic:
    italic['GDEF'] = deepcopy(TTFont(SRC/'InstrumentSerif-Italic.ttf')['GDEF'])
fonts = {'Regular':regular,'Italic':italic}

# Explicit composition supports decomposed Bulgarian й/ѝ as well as precomposed text.
for font in fonts.values():
    cm = font.getBestCmap()
    fea = 'languagesystem DFLT dflt; languagesystem cyrl dflt; languagesystem cyrl BGR;\nfeature ccmp {\n'
    for base,mark,composed in [('и','\u0306','й'),('И','\u0306','Й'),('и','\u0300','ѝ'),('И','\u0300','Ѝ')]:
        fea += f'sub {cm[ord(base)]} {cm[ord(mark)]} by {cm[ord(composed)]};\n'
    fea += '} ccmp;'
    old_gpos,old_gsub,old_gdef = deepcopy(font['GPOS']),deepcopy(font['GSUB']),deepcopy(font['GDEF'])
    addOpenTypeFeaturesFromString(font,fea)
    font['GSUB'] = merge_layout(old_gsub,font['GSUB'])
    font['GPOS'],font['GDEF'] = old_gpos,old_gdef

# Both cuts share family and vertical metrics for reliable style switching.
ascent = max(f['hhea'].ascent for f in fonts.values())
descent = min(f['hhea'].descent for f in fonts.values())
win_ascent = max(f['OS/2'].usWinAscent for f in fonts.values())
win_descent = max(f['OS/2'].usWinDescent for f in fonts.values())
for font in fonts.values():
    for char in CYR:
        glyph = font['glyf'][font.getBestCmap()[ord(char)]]
        glyph.recalcBounds(font['glyf'])
        ascent,descent = max(ascent,glyph.yMax),min(descent,glyph.yMin)
        win_ascent,win_descent = max(win_ascent,glyph.yMax),max(win_descent,-glyph.yMin)

for style,font in fonts.items():
    names = {1:FAMILY,2:style,3:f'{FAMILY} {style} 0.300',4:f'{FAMILY} {style}',5:'Version 0.300',
             6:f'Lirena-{style}',16:FAMILY,17:style}
    for nid,value in names.items():
        font['name'].removeNames(nameID=nid)
        font['name'].setName(value,nid,3,1,0x409)
        font['name'].setName(value,nid,1,0,0)
    copyright_text = original_regular['name'].getDebugName(0)+'\n'+donor['name'].getDebugName(0)+'\nCyrillic adaptation by Stiliyan Spasov / Spasov Type, 2026.'
    font['name'].removeNames(nameID=0); font['name'].setName(copyright_text,0,3,1,0x409)
    font['name'].removeNames(nameID=10)
    font['name'].setName('Bulgarian Cyrillic adaptation of Instrument Serif. Cyrillic adaptation by Stiliyan Spasov / Spasov Type.',10,3,1,0x409)
    font['OS/2'].usWeightClass = 400
    font['OS/2'].fsSelection = (font['OS/2'].fsSelection & ~0x61) | (0x01 if style=='Italic' else 0x40)
    font['head'].macStyle = 2 if style=='Italic' else 0
    font['post'].italicAngle = -13 if style=='Italic' else 0
    font['OS/2'].ulUnicodeRange1 |= 1<<9
    font['hhea'].ascent,font['hhea'].descent = ascent,descent
    font['OS/2'].sTypoAscender,font['OS/2'].sTypoDescender = ascent,descent
    font['hhea'].lineGap = font['OS/2'].sTypoLineGap = 0
    font['OS/2'].usWinAscent,font['OS/2'].usWinDescent = win_ascent,win_descent
    if 'DSIG' in font: del font['DSIG']
    font.flavor = None
    path = OUT/f'Lirena-{style}.ttf'; font.save(path)
    check = TTFont(path)
    assert all(ord(c) in check.getBestCmap() for c in CYR)
    check.flavor = 'woff2'; check.save(path.with_suffix('.woff2'))
    check.flavor = None
    reference = original_regular if style=='Regular' else TTFont(italic_path)
    src_gs,new_gs = reference.getGlyphSet(),check.getGlyphSet()
    for name in reference.getGlyphOrder():
        a,b = DecomposingRecordingPen(src_gs),DecomposingRecordingPen(new_gs)
        src_gs[name].draw(a); new_gs[name].draw(b)
        assert a.value == b.value,(style,name,'outline changed')
        assert reference['hmtx'][name] == check['hmtx'][name],(style,name,'advance changed')
    for text in [CYR,'Думите имат характер.','Дизайн и типография','Щъркелът лети над жълтата къща.','Тя ѝ каза: „Здравей!“','АѝЙЍ — 0123456789']:
        buf = shape(path,text)
        assert all(g.codepoint for g in buf.glyph_infos),(style,text,'missing glyph')
    for text in ['й','Й','ѝ','Ѝ']:
        composed,decomposed = shape(path,text),shape(path,unicodedata.normalize('NFD',text))
        assert [g.codepoint for g in composed.glyph_infos] == [g.codepoint for g in decomposed.glyph_infos],(style,text,'NFD mismatch')
    for text in ['Instrument Serif','office affinity AVATAR','Àâëü']:
        source = regular_source if style=='Regular' else italic_path
        a,b = shape(source,text),shape(path,text)
        assert [(g.codepoint,p.x_advance,p.x_offset,p.y_offset) for g,p in zip(a.glyph_infos,a.glyph_positions)] == [(g.codepoint,p.x_advance,p.x_offset,p.y_offset) for g,p in zip(b.glyph_infos,b.glyph_positions)],(style,text,'Latin shaping changed')

