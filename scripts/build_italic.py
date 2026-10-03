from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile,ZIP_DEFLATED
from math import tan,radians
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString

ROOT=Path(__file__).resolve().parents[1];SOURCES=ROOT/'sources'
OUT=ROOT/'build';OUT.mkdir(exist_ok=True)
font=TTFont(SOURCES/'InstrumentSerif-Italic.ttf')
donor=TTFont(SOURCES/'Cormorant-Italic400.ttf')
gs=font.getGlyphSet();dgs=donor.getGlyphSet();cmap=font.getBestCmap();dmap=donor.getBestCmap()
original=TTFont(SOURCES/'InstrumentSerif-Italic.ttf')
donor_hb=hb.Font(hb.Face((SOURCES/'Cormorant-Italic400.ttf').read_bytes()))
original_hb=hb.Font(hb.Face((SOURCES/'InstrumentSerif-Italic.ttf').read_bytes()))
LOW='абвгдежзийклмнопрстуфхцчшщъьюяѝ';CYR=LOW+LOW.upper()
# Shared shapes are taken directly from Instrument's true italic outlines.
ALIASES={'а':'a','е':'e','и':'u','о':'o','п':'n','р':'p','с':'c','т':'m','у':'y','х':'x',
         'А':'A','В':'B','Е':'E','К':'K','М':'M','Н':'H','О':'O','Р':'P','С':'C','Т':'T','Х':'X'}
order=list(font.getGlyphOrder());created={};donor_shapes={}
for char in CYR:
    buf=hb.Buffer();buf.add_str(char);buf.guess_segment_properties();buf.language='bg';hb.shape(donor_hb,buf,{'liga':False,'calt':False})
    donor_shapes[char]=donor.getGlyphName(buf.glyph_infos[0].codepoint)

sx=1.095;sy=font['OS/2'].sxHeight/donor['OS/2'].sxHeight
# Correct slant after changing horizontal/vertical proportions.
shear=tan(radians(13))*sy-tan(radians(10))*sx
for char in CYR:
    name=f'uni{ord(char):04X}.lyric'
    if char in ALIASES:
        source=cmap[ord(ALIASES[char])];record=DecomposingRecordingPen(gs);gs[source].draw(record)
        pen=TTGlyphPen(None);record.replay(pen);glyph=pen.glyph()
        metrics=font['hmtx'][source]
    else:
        source=donor_shapes[char]
        # Capitals align to the Instrument cap height; lowercase to its x-height.
        vertical=font['OS/2'].sCapHeight/donor['OS/2'].sCapHeight if char.isupper() else sy
        slant=tan(radians(13))*vertical-tan(radians(10))*sx
        record=DecomposingRecordingPen(dgs);dgs[source].draw(record)
        pen=TTGlyphPen(None);record.replay(TransformPen(pen,(sx,0,slant,vertical,0,0)));glyph=pen.glyph()
        advance=round(donor['hmtx'][source][0]*sx)
        glyph.recalcBounds(font['glyf']);metrics=(advance,glyph.xMin)
    font['glyf'][name]=glyph;font['hmtx'][name]=metrics;order.append(name);created[char]=name
    for table in font['cmap'].tables:
        if table.isUnicode():table.cmap[ord(char)]=name
font.setGlyphOrder(order)

def total_advance(hfont,text):
    buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties();buf.language='bg'
    hb.shape(hfont,buf,{'kern':True,'liga':False,'calt':False})
    return sum(p.x_advance for p in buf.glyph_positions)

# Keep source layout tables; append a kern feature for the new Cyrillic glyphs.
old_gpos=deepcopy(font['GPOS']);old_gsub=deepcopy(font['GSUB'])
fea='languagesystem DFLT dflt; languagesystem cyrl dflt; languagesystem cyrl BGR;\nfeature kern {\n'
pairs=0
for a in CYR:
    for b in CYR:
        if a in ALIASES and b in ALIASES:
            la,lb=ALIASES[a],ALIASES[b]
            value=total_advance(original_hb,la+lb)-total_advance(original_hb,la)-total_advance(original_hb,lb)
        else:
            value=round((total_advance(donor_hb,a+b)-total_advance(donor_hb,a)-total_advance(donor_hb,b))*sx)
        value=max(-100,min(80,value))
        if abs(value)>=5:
            fea+=f'pos {created[a]} {created[b]} {value};\n';pairs+=1
fea+='} kern;'
addOpenTypeFeaturesFromString(font,fea)
new=font['GPOS'].table;old=old_gpos.table
offset=len(old.LookupList.Lookup);feature_offset=len(old.FeatureList.FeatureRecord)
old.LookupList.Lookup.extend(new.LookupList.Lookup);old.LookupList.LookupCount=len(old.LookupList.Lookup)
for record in new.FeatureList.FeatureRecord:
    record.Feature.LookupListIndex=[v+offset for v in record.Feature.LookupListIndex]
    old.FeatureList.FeatureRecord.append(record)
old.FeatureList.FeatureCount=len(old.FeatureList.FeatureRecord)
for record in new.ScriptList.ScriptRecord:
    if record.ScriptTag!='cyrl':continue
    for lang in [record.Script.DefaultLangSys]+[r.LangSys for r in record.Script.LangSysRecord]:
        if lang is not None:lang.FeatureIndex=[v+feature_offset for v in lang.FeatureIndex]
    old.ScriptList.ScriptRecord.append(record)
old.ScriptList.ScriptRecord.sort(key=lambda r:r.ScriptTag);old.ScriptList.ScriptCount=len(old.ScriptList.ScriptRecord)
# Sort feature tags and reindex both original Latin and added Cyrillic languages.
indexed=sorted(enumerate(old.FeatureList.FeatureRecord),key=lambda x:x[1].FeatureTag)
remap={i:j for j,(i,_) in enumerate(indexed)};old.FeatureList.FeatureRecord=[r for _,r in indexed]
for script in old.ScriptList.ScriptRecord:
    for lang in [script.Script.DefaultLangSys]+[r.LangSys for r in script.Script.LangSysRecord]:
        if lang is not None:
            lang.FeatureIndex=sorted(remap[i] for i in lang.FeatureIndex)
            if lang.ReqFeatureIndex!=0xFFFF:lang.ReqFeatureIndex=remap[lang.ReqFeatureIndex]
font['GPOS']=old_gpos;font['GSUB']=old_gsub

FAMILY='Instrument Serif Cyrillic'
names={1:FAMILY,2:'Italic',3:FAMILY+' Italic 0.100',4:FAMILY+' Italic',5:'Version 0.100',6:'InstrumentSerifCyrillic-Italic',16:FAMILY,17:'Italic'}
for id,value in names.items():
    font['name'].removeNames(nameID=id)
    font['name'].setName(value,id,3,1,0x409);font['name'].setName(value,id,1,0,0)
copyright_text=original['name'].getDebugName(0)+'\n'+donor['name'].getDebugName(0)+'\nCustom Cyrillic adaptation, 2026.'
font['name'].removeNames(nameID=0);font['name'].setName(copyright_text,0,3,1,0x409)
font['OS/2'].usWeightClass=400;font['OS/2'].fsSelection=(font['OS/2'].fsSelection & ~((1<<5)|(1<<6))) | 1
font['head'].macStyle=2;font['post'].italicAngle=-13
font['OS/2'].ulUnicodeRange1 |= 1<<9
# Original hinted glyphs keep their matching hint tables; new glyphs are unhinted.
for tag in ['DSIG']:
    if tag in font:del font[tag]
for name in created.values():font['glyf'][name].recalcBounds(font['glyf'])
font['OS/2'].usWinAscent=max(font['OS/2'].usWinAscent,max(font['glyf'][n].yMax for n in created.values()))
font['OS/2'].usWinDescent=max(font['OS/2'].usWinDescent,-min(font['glyf'][n].yMin for n in created.values()))
outfile=OUT/'InstrumentSerifCyrillic-Italic.ttf';font.save(outfile)
check=TTFont(outfile);c=check.getBestCmap();assert all(ord(x) in c for x in CYR)
check_gs=check.getGlyphSet();orig_gs=original.getGlyphSet()
for name in original.getGlyphOrder():
    a=DecomposingRecordingPen(orig_gs);b=DecomposingRecordingPen(check_gs)
    orig_gs[name].draw(a);check_gs[name].draw(b);assert a.value==b.value,name
for text in ['Валентин','Дизайн и типография','Създавам красиви истории','Щъркел, жълт, ѝ','АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯ']:
    hfont=hb.Font(hb.Face(outfile.read_bytes()));buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties();buf.language='bg';hb.shape(hfont,buf)
    assert all(g.codepoint!=0 for g in buf.glyph_infos),text
check.flavor='woff2';check.save(outfile.with_suffix('.woff2'))
