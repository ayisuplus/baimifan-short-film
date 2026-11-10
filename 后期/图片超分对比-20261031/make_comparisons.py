import json,pathlib
from PIL import Image,ImageDraw,ImageFont
p=pathlib.Path(__file__).parent
samples=json.loads((p/'samples.json').read_text(encoding='utf-8-sig'))
methods=['original','realesrgan','seedvr2','rtx']; labels=['原图 · Lanczos','Real-ESRGAN','SeedVR2 · 7B Q8','RTX · ULTRA']
crops={'closeup':[('face',1210,800,360,540),('hands',1450,1370,400,460),('hair',400,1340,400,460)],'fullbody':[('face',660,480,400,400),('clothes',370,1000,400,400),('text',1220,850,400,400)],'palace':[('throne',1180,900,400,440),('ornament',1220,40,400,440),('floor',1750,1450,400,440)]}
f=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
for s in samples:
 sid=s['id'];ims=[Image.open(s['baseline']).convert('RGB')]+[Image.open(p/'outputs'/f'{sid}_{m}.png').convert('RGB') for m in methods[1:]]
 assert all(im.size==tuple(s['target_size']) for im in ims)
 for name,x,y,w,h in crops[sid]:
  board=Image.new('RGB',(w*4,h+60),'#18212c');d=ImageDraw.Draw(board)
  for i,(im,label) in enumerate(zip(ims,labels)):
   board.paste(im.crop((x,y,x+w,y+h)),(i*w,60));d.text((i*w+8,16),label,font=f,fill='white')
  board.save(p/'comparisons'/f'{sid}_{name}.png')
 ow=640;oh=round(ow*ims[0].height/ims[0].width);board=Image.new('RGB',(ow*2,(oh+55)*2),'#18212c');d=ImageDraw.Draw(board)
 for i,(im,label) in enumerate(zip(ims,labels)):
  x=(i%2)*ow;y=(i//2)*(oh+55);board.paste(im.resize((ow,oh),Image.Resampling.LANCZOS),(x,y+55));d.text((x+14,y+14),label,font=f,fill='white')
 board.save(p/'comparisons'/f'{sid}_overview.jpg',quality=94)
(p/'crop-regions.json').write_text(json.dumps(crops,indent=2),encoding='utf-8')
print('9 native-pixel crops and 3 overview boards created.')
