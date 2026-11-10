from pathlib import Path
import json,subprocess,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[3]
D=Path(__file__).resolve().parent
E=D/'证据';E.mkdir(exist_ok=True)
sources={
 'B17-v010':R/'视频制作/Metaso-H3-v010/产物/GB014-v010-original-shot-only-r1.mp4',
 'B17-v011':R/'视频制作/Metaso-H3-v011/产物/GB014-v011-original-2d-group-r1.mp4',
 'B26':R/'视频制作/Metaso-H3-v002/剪辑候选/GB019-v002.mp4'}
manifest=[]
for key,path in sources.items():
 out=E/key;out.mkdir(exist_ok=True)
 duration=5 if key.startswith('B17') else 4.5
 subprocess.run(['ffmpeg','-v','error','-i',str(path),'-t',str(duration),'-vf','fps=24','-start_number','0','-y',str(out/'%03d.png')],check=True)
 files=sorted(out.glob('*.png'))
 for page in range((len(files)+11)//12):
  part=files[page*12:(page+1)*12]
  sheet=Image.new('RGB',(1920,870),'#111722');dr=ImageDraw.Draw(sheet)
  for j,p in enumerate(part):
   im=Image.open(p);im.thumbnail((480,270));x=(j%4)*480;y=(j//4)*290;sheet.paste(im,(x,y));f=int(p.stem);dr.text((x+4,y+271),f'{key} f{f} {f/24:.3f}s',fill='white')
  sheet.save(E/f'{key}-full-{page:02d}.jpg',quality=92)
 if key.startswith('B17'):
  for page in range(3):
   part=files[page*40:(page+1)*40]
   sheet=Image.new('RGB',(1600,1200),'#111722');dr=ImageDraw.Draw(sheet)
   for j,p in enumerate(part):
    im=Image.open(p);w,h=im.size;im=im.crop((int(w*.43),int(h*.12),int(w*.61),int(h*.40)));im.thumbnail((200,215));x=(j%8)*200;y=(j//8)*240;sheet.paste(im,(x,y));f=int(p.stem);dr.text((x+4,y+218),f'f{f} {f/24:.3f}s',fill='white')
   sheet.save(E/f'{key}-face-{page:02d}.jpg',quality=94)
 manifest.append({'id':key,'source':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sampled_frames':len(files),'fps':24})
(D/'证据索引.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('done',manifest)
