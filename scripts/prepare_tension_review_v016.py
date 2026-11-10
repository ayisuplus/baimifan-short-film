"""Read-only review contact sheets from current main images; never edits source art."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageOps,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'后期/全片张力审查-v016'
SOURCE=ROOT/'镜头设计/shot-plan-v0.61.json'
def main():
    data=json.loads(SOURCE.read_text('utf-8-sig'));OUT.mkdir(exist_ok=True,parents=True)
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15)
    records=[];shots=data['shots']
    for start in range(0,len(shots),12):
        canvas=Image.new('RGB',(1620,1408),'#101620');draw=ImageDraw.Draw(canvas)
        for i,s in enumerate(shots[start:start+12]):
            x=(i%3)*540;y=(i//3)*352
            path=ROOT/s['presentation']['path']
            with Image.open(path) as im:
                thumb=ImageOps.contain(im.convert('RGB'),(534,300))
                canvas.paste(thumb,(x+(540-thumb.width)//2,y+(300-thumb.height)//2))
            draw.text((x+8,y+302),f"{start+i+1:03} {s['id']}  {s['start_second']:.2f}s  {s['seconds']:g}s",font=font,fill='white')
            draw.text((x+8,y+327),s['title'],font=small,fill='#bccbdc')
            records.append(dict(index=start+i+1,id=s['id'],title=s['title'],start=s['start_second'],seconds=s['seconds'],path=s['presentation']['path'],sha256=hashlib.sha256(path.read_bytes()).hexdigest(),sheet=f'contact-{start//12+1:02}.jpg',action=s['action'],purpose=s.get('purpose'),framing=s['framing']))
        canvas.save(OUT/f'contact-{start//12+1:02}.jpg',quality=91)
    manifest=dict(source=str(SOURCE.relative_to(ROOT)).replace('\\','/'),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),shots=records,scope='Contact sheets for inspection only; original art and generation inputs unchanged.')
    (OUT/'审查索引.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(f'{len(records)} main images; 12 contact sheets; source hash {manifest["source_sha256"]}')
if __name__=='__main__':main()

