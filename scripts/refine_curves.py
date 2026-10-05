"""Seven curved Regular Cyrillic forms; native o and l controls remain unmodified."""
import pathops

def curved_forms(native):
 def path(start,items):
  p=pathops.Path();p.moveTo(*start)
  for item in items:
   if len(item)==2:p.lineTo(*item)
   else:p.cubicTo(*item)
  p.close();return p
 def unite(a,b):return pathops.op(a,b,pathops.PathOp.UNION)
 def subtract(a,b):return pathops.op(a,b,pathops.PathOp.DIFFERENCE)
 # б: a native o bowl, with a flowing, tapered flag and no sharp inner shoulder.
 bowl=native['o'].transform(1,0,0,1,18,0)
 flag=path((41,245),[(41,473,70,610,151,677),(217,731,317,710,381,740),(384,744,390,741,388,734),(385,710),(351,693,239,704,174,662),(106,618,108,487,112,369),(116,292),(41,245)])
 be=unite(bowl,flag)
 # в and б share the actual native o bowl. Only the ascender construction differs.
 upper_outer=path((41,254),[(41,578,89,740,217,740),(287,740,350,713,350,655),(350,588,295,541,215,511),(177,497,142,482,113,479),(110,404,111,311,117,254),(41,254)])
 upper_inner=path((113,522),[(188,531,278,577,278,657),(278,703,253,717,217,714),(148,707,117,611,113,522)])
 ve=unite(bowl,subtract(upper_outer,upper_inner))
 # з: two rounded open bowls, a short curved waist and native-weight terminal.
 ze=path((170,-205),[(91,-205,20,-166,20,-118),(20,-96,35,-81,55,-81),(77,-81,89,-98,92,-123),(97,-153,125,-178,169,-178),(245,-178,302,-87,302,36),(302,157,251,226,162,226),(138,226,117,224,96,218),(81,214,76,232,92,238),(125,250,155,256,183,266),(245,289,279,335,279,397),(279,458,246,491,196,491),(146,491,106,452,89,399),(82,378,61,382,66,405),(83,475,137,517,205,517),(291,517,351,470,351,404),(351,328,297,281,231,255),(324,234,378,147,378,42),(378,-99,289,-205,170,-205)])
 # ж: native ascender, lighter curved upper arms and tapered lower joins.
 # Right half arm, reflected across the center. Curves ease into the central stem.
 arm=path((336,272),[(377,297,415,358,451,407),(486,455,489,479,455,486),(442,489,430,492,430,501),(430,510),(605,510),(617,510,619,491,607,488),(570,481,542,461,506,418),(472,379,431,327,413,302),(402,286,409,275,419,258),(490,121),(520,65,553,30,609,24),(623,23,623,0,609,0),(455,0),(441,0,440,20,454,23),(489,29,484,53,464,94),(396,231),(379,263,355,251,336,219),(336,272)])
 left=arm.transform(-1,0,0,1,668,0)
 stem=native['l'].transform(1,0,0,1,226,0) # native 74..142 -> 300..368
 zhe=unite(unite(arm,left),stem)
 # д: the real native q loop and joins, with a smooth Bulgarian descender.
 clipping=path((-100,-9),[(700,-9),(700,800),(-100,800),(-100,-9)])
 q_body=pathops.op(native['q'],clipping,pathops.PathOp.INTERSECTION).transform(1,0,0,1,9,0)
 de_tail=path((312,100),[(312,-78),(312,-145,274,-178,226,-178),(176,-178,148,-152,126,-113),(110,-85,107,-66,89,-66),(70,-66,64,-88,64,-110),(64,-161,128,-205,213,-205),(308,-205,380,-147,380,-57),(380,100),(312,100)])
 de=unite(q_body,de_tail)
 # ч: one native-style head serif, continuous right stem, no double ear.
 che=path((171,211),[(111,211,70,251,70,321),(70,449),(70,471,55,481,28,484),(11,486,11,510,30,510),(123,510),(138,510,138,502,138,495),(138,342),(138,283,160,257,204,257),(257,257,312,313,312,366),(312,449),(312,472,297,481,270,484),(253,486,253,510,272,510),(365,510),(380,510,380,502,380,495),(380,67),(380,43,396,29,414,26),(438,23,438,0,426,0),(268,0),(253,0,253,20,266,23),(297,28,312,43,312,67),(312,276),(277,239,223,211,171,211)])
 # я: preserve the original R bowl and curved leg; adapt to the Bulgarian x-height.
 ya=native['R'].transform(-0.96,0,0,510/720,522,0)
 return {'б':be,'в':ve,'з':ze,'ж':zhe,'д':de,'ч':che,'я':ya}
