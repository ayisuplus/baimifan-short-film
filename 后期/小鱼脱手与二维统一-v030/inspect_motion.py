"""Extract ordered frames for shot-specific animation inspection; never edits sources."""
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw

p=argparse.ArgumentParser()
p.add_argument('video',type=Path)
p.add_argument('--step',type=int,default=6)
p.add_argument('--name',default=None)
a=p.parse_args()
out=Path(__file__).parent
name=a.name or a.video.stem
data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(a.video)]))
stream=next(x for x in data['streams'] if x['codec_type']=='video')
n=int(stream['nb_frames'])
indices=sorted(set(range(0,n,a.step))|{n-1})
frames_dir=out/'检查抽帧'/name
frames_dir.mkdir(parents=True,exist_ok=True)
for f in indices:
    dest=frames_dir/f'{f:04}.jpg'
    if not dest.exists():
        subprocess.run(['ffmpeg','-v','error','-i',str(a.video),'-vf',f'select=eq(n\\,{f})','-frames:v','1','-q:v','2','-y',str(dest)],check=True)
cols=4
w,h=400,229
for start in range(0,len(indices),20):
    block=indices[start:start+20]
    sheet=Image.new('RGB',(cols*w,((len(block)+cols-1)//cols)*(h+25)),(18,20,26))
    d=ImageDraw.Draw(sheet)
    for i,f in enumerate(block):
        with Image.open(frames_dir/f'{f:04}.jpg') as im:
            im=im.convert('RGB').resize((w,h),Image.Resampling.LANCZOS)
            x=(i%cols)*w; y=(i//cols)*(h+25)
            sheet.paste(im,(x,y));d.text((x+5,y+h+5),f'{name} | frame {f} | {f/24:.3f}s',fill='white')
    dest=out/f'{name}-动作-{start//20+1}.jpg'
    sheet.save(dest,quality=93)
    print(dest)
(out/f'{name}-probe.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'frames={n}, duration={data["format"]["duration"]}, audio={any(s["codec_type"]=="audio" for s in data["streams"])}')
