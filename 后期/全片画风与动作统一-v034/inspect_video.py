"""CPU dense frame review; exact job name, no automatic acceptance."""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
N=Path('G:/comfyui/ComfyUI/ComfyUI/output/Baimifan/v034')
a=argparse.ArgumentParser();a.add_argument('names',nargs='+');a.add_argument('--step',type=int,default=6);args=a.parse_args()
for name in args.names:
 files=list(N.glob(name+'_*.mp4'));assert len(files)==1,(name,files)
 src=files[0];d=P/'review'/name;d.mkdir(parents=True,exist_ok=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(src)]))
 v=next(x for x in probe['streams'] if x['codec_type']=='video');n=int(v['nb_frames'])
 assert v['r_frame_rate']=='24/1'
 frames=sorted(set(range(0,n,args.step))|{n-1})
 subprocess.run(['ffmpeg','-v','error','-i',str(src),'-vf',f"select='not(mod(n,{args.step}))+eq(n,{n-1})',scale=480:-2",'-fps_mode','vfr','-y',str(d/'%04d.png')],check=True)
 paths=sorted(d.glob('*.png'));assert len(paths)==len(frames)
 h=Image.open(paths[0]).height;rowh=h+26
 sheets=[]
 for start in range(0,len(paths),16):
  block=paths[start:start+16];im=Image.new('RGB',(1920,((len(block)+3)//4)*rowh),(16,18,24));draw=ImageDraw.Draw(im)
  for i,path in enumerate(block):
   x=i%4*480;y=i//4*rowh;im.paste(Image.open(path).convert('RGB'),(x,y));draw.text((x+6,y+h+4),f'{name} | frame {frames[start+i]}',fill='white')
  out=d/f'sheet-{start//16+1}.jpg';im.save(out,quality=92);sheets.append(str(out))
 (d/'probe.json').write_text(json.dumps(dict(source=str(src),probe=probe,frames=frames,sheets=sheets,review='pending'),ensure_ascii=False,indent=2),'utf8')
 print(name,n,sheets,flush=True)
