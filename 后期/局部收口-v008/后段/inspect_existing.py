from pathlib import Path
import subprocess,json,io
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[3]
O=Path(__file__).resolve().parent
def frame(p,t):
    return Image.open(io.BytesIO(subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=480:-1','-f','image2pipe','-vcodec','png','pipe:1']))).convert('RGB')
clips=[]
for p in (R/'视频制作').rglob('*.mp4'):
    if (p.name.startswith('GB027') and ('CY028A' in p.name or p.name=='GB027-r001.mp4')) or p.name in ['GB030-1-r001.mp4','GB030-1-r002-part45.mp4','GB031-r001.mp4','GB028-r002-part1.mp4','GB028-r001.mp4','GB029-v003-CY029E4.mp4','GB029-v003-CY029E4-r002.mp4']:
        clips.append(p)
index=[]
for k,p in enumerate(clips):
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)]))
    times=[d*x for x in [.04,.25,.5,.75,.96]]
    sheet=Image.new('RGB',(2400,320),'#18202b');draw=ImageDraw.Draw(sheet)
    for i,t in enumerate(times):
        im=frame(p,t);sheet.paste(im,(480*i,40));draw.text((480*i+4,5),p.name,fill='white');draw.text((480*i+4,22),f'{t:.3f}s',fill='white')
    out=O/f'old-{k:02d}.jpg';sheet.save(out,quality=90)
    index.append(dict(path=str(p.relative_to(R)),duration=d,contact=out.name))
(O/'old-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf8')
for group,names in {
    'down':['独立镜头-v009/CY028A-v009.png','动作收尾-v015/CY028A-v015-r1.png','天瀑空间-v014/CY028A-v014-r1.png','火焰伤后与星火-v036/CY028A-v036-r1.png','暗月瞬临-v045/CY028A-v045-r1.png','月刃救援-v041/CY028A-v041-r1.png','关键动作-v062/CY028A-v062-r1.png'],
    'carry':['独立镜头-v009/CY028-v009.png','动作收尾-v015/CY028-v015-r1.png','天瀑空间-v014/CY028-v014-r1.png','展翼与扇叶-v033/CY028-v033-r1.png','火焰伤后与星火-v036/CY028-v036-r1.png','关键动作-v062/CY029D-v062-r2.png','火焰伤后与星火-v036/CY029A-v036-r1.png']}.items():
    sheet=Image.new('RGB',(1440,310*((len(names)+2)//3)),'#18202b');draw=ImageDraw.Draw(sheet)
    for i,n in enumerate(names):
        p=R/'镜头设计/图像'/n; im=Image.open(p).convert('RGB');im.thumbnail((480,270));x=(i%3)*480;y=(i//3)*310;sheet.paste(im,(x,y+35));draw.text((x+5,y+5),n.encode('ascii','replace').decode(),fill='white')
    sheet.save(O/f'original-{group}.jpg',quality=90)
print(json.dumps(index,ensure_ascii=False))
