import argparse,subprocess,json
from pathlib import Path
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent
NATIVE=Path('G:/comfyui/ComfyUI/ComfyUI/output/Baimifan/v032')
p=argparse.ArgumentParser();p.add_argument('ids',nargs='+');a=p.parse_args()
for id in a.ids:
    src=sorted(NATIVE.glob(f'{id}-video-*.mp4'))[-1]
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate,width,height','-of','json',str(src)]))['streams'][0]
    n=int(probe['nb_frames']);step=6
    d=OUT/'review'/id;d.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(src),'-vf',f"select='not(mod(n,{step}))+eq(n,{n-1})',scale=480:-1",'-fps_mode','vfr','-y',str(d/'%04d.png')],check=True)
    frames=sorted(set(range(0,n,step))|{n-1});files=sorted(d.glob('*.png'))
    for start in range(0,len(files),16):
        block=files[start:start+16];sheet=Image.new('RGB',(1920,((len(block)+3)//4)*294),(18,20,26));dr=ImageDraw.Draw(sheet)
        for i,path in enumerate(block):
            x=i%4*480;y=i//4*294
            sheet.paste(Image.open(path).convert('RGB').resize((480,270)),(x,y));dr.text((x+8,y+274),f'{id} | frame {frames[start+i]}',fill='white')
        sheet.save(OUT/'review'/f'{id}-{start//16+1}.jpg',quality=94)
    print(id,probe,flush=True)
