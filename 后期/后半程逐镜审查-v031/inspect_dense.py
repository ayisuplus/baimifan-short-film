"""Read-only ordered action evidence; all times are local frames at 24 fps."""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw

OUT=Path(__file__).resolve().parent
rows=json.loads((OUT/'镜头索引.json').read_text('utf8'))
selected={43,44,45,46,47,49,56,59,61,62,66,71,80,82,86,91,92,93,99,100,104,105,106,108,110,116}
for r in rows:
    if int(r['shot']) not in selected:continue
    n=r['frames'];step=1 if int(r['shot']) in {104,105} else (6 if n<=96 else 12)
    indices=sorted(set(range(0,n,step))|{n-1})
    d=OUT/'动作抽帧'/r['shot'];d.mkdir(parents=True,exist_ok=True)
    if len(list(d.glob('*.png')))!=len(indices):
        filt=f"select='not(mod(n,{step}))+eq(n,{n-1})',scale=400:-1"
        subprocess.run(['ffmpeg','-v','error','-i',r['source'],'-vf',filt,'-fps_mode','vfr','-pix_fmt','rgb24','-y',str(d/'%04d.png')],check=True)
    files=sorted(d.glob('*.png'));assert len(files)==len(indices),(r['shot'],len(files),len(indices))
    for start in range(0,len(indices),20):
        block=files[start:start+20];sheet=Image.new('RGB',(1600,((len(block)+3)//4)*254),(18,20,26));draw=ImageDraw.Draw(sheet)
        for i,p in enumerate(block):
            x=i%4*400;y=i//4*254
            with Image.open(p) as im:sheet.paste(im.convert('RGB').resize((400,225)),(x,y))
            f=indices[start+i];draw.text((x+4,y+229),f"{r['shot']} | f{f} | {f/24:.3f}s",fill='white')
        target=OUT/'动作检查'/f"{r['shot']}-{start//20+1}.jpg";target.parent.mkdir(exist_ok=True)
        sheet.save(target,quality=93)
    print(r['shot'],flush=True)
