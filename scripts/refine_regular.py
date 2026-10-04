"""Targeted Regular refinement; input is the unedited Lirena Regular 0.300."""
from pathlib import Path
from fontTools.ttLib import TTFont

def refine_regular(font):
    f = font
    cm=f.getBestCmap()
    assert f['name'].getDebugName(5) == 'Version 0.300', 'Input must be the original 0.300 Regular'
    assert f['glyf'][cm[ord('к')]].coordinates[16] == (143,957), 'Unexpected outline point order'
    changes={}
    # Shorten only the straight ascender extension; keep the original cap/terminal contour.
    for ch in 'жк':
     g=f['glyf'][cm[ord(ch)]]
     coords=g.coordinates
     end=19 if ch=='ж' else 21
     for i in range(7,end+1):
      x,y=coords[i]; coords[i]=(x,y-218)
     # Align the straight stem with the 68-unit Latin n/k control.
     for i in [6,7,8]:
      x,y=coords[i];coords[i]=(x-3,y)
     indices=[18,19,20,21] if ch=='ж' else [20,21,22,23]
     for i in indices:
      x,y=coords[i];coords[i]=(x+3,y)
     changes[ch]='Ascender terminal translated down 218 units; straight stem widened from 62 to 68 units; local branch and spacing refinement.'
    # Open the upper edge of the lower branches modestly; keep the 16-unit serif terminals.
    g=f['glyf'][cm[ord('ж')]]
    for i in [42,43,44,45,92,93,94,95]:
     x,y=g.coordinates[i];g.coordinates[i]=(x,y-4)
    g=f['glyf'][cm[ord('к')]]
    for i in [45,46,47,48,49]:
     x,y=g.coordinates[i];g.coordinates[i]=(x,y-4)
    # Reduce the bulb terminal's overshoot and mass without replacing its construction.
    for i,xy in {69:(382,516),70:(411,516),71:(432,516),72:(454,491),73:(454,476),74:(454,459),75:(435,434),76:(417,434),77:(407,434),78:(393,441),79:(379,448)}.items():g.coordinates[i]=xy
    # Redraw the upper loop to the Latin ascender height; retain the Bulgarian two-loop identity.
    g=f['glyf'][cm[ord('в')]]
    for i,y in {15:548,16:620,17:688,18:727,19:740,20:740,21:740,22:682,23:620,24:575,25:530,42:544,43:590,44:605,45:650,46:715,47:715,48:715,49:684,50:615,51:535}.items():
     x,_=g.coordinates[i];g.coordinates[i]=(x,y)
    changes['в']='Upper loop redrawn to 740-unit ascender height, with 25-unit top hairline; lower bowl and terminal retained.'
    # Keep advances elsewhere. Add only a small amount of air at the two tight branching glyphs.
    for ch,delta in [('ж',6),('к',8)]:
     name=cm[ord(ch)];g=f['glyf'][name]
     g.coordinates.translate((delta,0));aw,lsb=f['hmtx'][name];f['hmtx'][name]=(aw+2*delta,lsb+delta)
    for ch in changes:f['glyf'][cm[ord(ch)]].recalcBounds(f['glyf'])
    from fontTools.ttLib.removeOverlaps import removeOverlaps
    removeOverlaps(f, [cm[ord('в')]], removeHinting=False)
    changes['в'] += ' Existing self-crossings removed with outline union.'
    # Standard family/style linking remains Lirena Regular; bump version/unique ID only.
    for nid,value in {3:'Lirena Regular 0.400',5:'Version 0.400'}.items():
     for rec in f['name'].names:
      if rec.nameID==nid:rec.string=value.encode(rec.getEncoding())
    f['head'].fontRevision=.4
    return changes

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Use a separate output path; the original must remain intact.')
    font = TTFont(args.input, recalcTimestamp=False)
    print(refine_regular(font))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    font.save(args.output)
    font.flavor = 'woff2'
    font.save(args.output.with_suffix('.woff2'))
