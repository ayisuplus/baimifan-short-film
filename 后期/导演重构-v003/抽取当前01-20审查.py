import json,cv2,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]
O=Path(__file__).resolve().parent/'证据'/'争执复核'
O.mkdir(parents=True,exist_ok=True)
plan=json.loads((R/'后期/声画重构-v002/后期执行计划.json').read_text(encoding='utf-8'))
actual=json.loads((R/'后期/导演重构-v003/开始时达芬奇实际状态.json').read_text(encoding='utf-8'))['result']
lookup={x['name']:x for x in plan['edl']}
segments=[]
for x in actual['video']:
    p=lookup.get(x['name'])
    if not p or p['batch']>20:continue
    segments.append(dict(x,batch=p['batch'],props=p.get('props',{}),planned_record=p['record']))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
caps={}
summary=[]
for b in range(1,21):
    ss=[x for x in segments if x['batch']==b]; lo=min(x['start'] for x in ss); hi=max(x['end'] for x in ss)
    times=list(range(lo,hi,12)); rows=math.ceil(len(times)/5)
    sheet=Image.new('RGB',(5*384,rows*238),(15,15,15)); draw=ImageDraw.Draw(sheet)
    for k,f in enumerate(times):
        s=next(x for x in ss if x['start']<=f<x['end'])
        sf=s['source_in']+(f-s['start'])*s['speed']['Percentage']/100
        if s['path'] not in caps:caps[s['path']]=cv2.VideoCapture(s['path'])
        cap=caps[s['path']]; cap.set(cv2.CAP_PROP_POS_FRAMES,int(sf)); ok,frame=cap.read()
        if not ok:raise RuntimeError((b,f,s['path']))
        im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        props=s['props']; z=props.get('ZoomX',1); pan=props.get('Pan',0); tilt=props.get('Tilt',0)
        if z!=1:
            w,h=im.size; cw,ch=w/z,h/z; cx=w/2-pan/z; cy=h/2+tilt/z
            im=im.crop((cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2))
        im=im.resize((384,216)); x=(k%5)*384;y=(k//5)*238
        sheet.paste(im,(x,y+22));draw.text((x+3,y+2),f'B{b:02} actual {f/24:.3f} src {sf/24:.3f}',font=font,fill='white')
    out=O/f'B{b:02}-current-2fps.jpg';sheet.save(out,quality=88)
    summary.append(dict(batch=b,actual_start=lo/24,actual_end=hi/24,planned_start=min(x['planned_record'] for x in ss)/24,sheet=str(out.relative_to(R)),segments=[dict(name=x['name'],source=str(Path(x['path']).relative_to(R)),source_in=x['source_in']/24,source_out=x['source_out']/24,actual_start=x['start']/24,actual_end=x['end']/24,speed=x['speed'],props=x['props']) for x in ss]))
for cap in caps.values():cap.release()
(O/'当前01-20采用摘要.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print('20 current source-range sheets written; props reproduced approximately, not Resolve render')
