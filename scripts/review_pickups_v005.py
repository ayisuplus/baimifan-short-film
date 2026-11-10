"""Sample new pickup clips for explicit visual review, without claiming continuous playback."""
from pathlib import Path
import json, cv2, argparse
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parents[1];O=R/'视频制作/Metaso-H3-v005'
ap=argparse.ArgumentParser();ap.add_argument('--fps',type=float,default=2);a=ap.parse_args()
q=json.loads((O/'执行队列.json').read_text(encoding='utf8'));out=O/'审查';out.mkdir(exist_ok=True)
for x in q['items']:
    if not x.get('local_path'):continue
    p=R/x['local_path']; target=out/(x['attempt_id']+f'-{a.fps:g}fps.jpg')
    if target.exists():continue
    cap=cv2.VideoCapture(str(p));dur=cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS)
    ts=[i/a.fps for i in range(int(dur*a.fps))];w,h=384,238
    for chunk in range(0,len(ts),24):
        times=ts[chunk:chunk+24];sheet=Image.new('RGB',(w*4,h*((len(times)+3)//4)),(16,20,25));d=ImageDraw.Draw(sheet)
        for j,t in enumerate(times):
            cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,frame=cap.read()
            if not ok:continue
            im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));im.thumbnail((w,h-22));ox=(j%4)*w;oy=(j//4)*h
            sheet.paste(im,(ox,oy+22));d.text((ox+4,oy+2),f'{x["attempt_id"]} {t:.3f}s',fill='white')
        dest=target if chunk==0 else target.with_stem(target.stem+f'-{chunk//24+1}')
        sheet.save(dest,quality=90);print(str(dest))
    cap.release()
