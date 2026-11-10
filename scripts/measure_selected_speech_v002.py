"""Measure non-silent intervals; these are timing evidence, not transcription or listening."""
from pathlib import Path
import json,subprocess,re,concurrent.futures
R=Path(__file__).resolve().parents[1];O=R/'后期/声画重构-v002'
P=json.loads((R/'后期/导演后期修正-v001/后期执行计划.json').read_text(encoding='utf8'))
def one(v):
    p=Path(v['path']);p=p if p.is_absolute() else R/p
    z=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-af','silencedetect=n=-35dB:d=0.12','-f','null','-'],capture_output=True,text=True,check=True)
    silence=[];start=None
    for line in z.stderr.splitlines():
        m=re.search(r'silence_start: ([\d.]+)',line)
        if m:start=float(m[1])
        m=re.search(r'silence_end: ([\d.]+)',line)
        if m and start is not None:silence.append([start,float(m[1])]);start=None
    if start is not None:silence.append([start,v['duration']])
    active=[];cursor=0
    for a,b in silence:
        if a>cursor:active.append([cursor,a])
        cursor=b
    if cursor<v['duration']-.001:active.append([cursor,v['duration']])
    return {'id':v['id'],'batch':v['batch'],'path':str(p),'file_duration':v['duration'],'silences':silence,'signal_intervals':active,'boundary':'amplitude threshold only; breaths may count; no phoneme or subjective listening claim'}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:rows=list(e.map(one,P['voice']))
(O/'选定配音实测停顿.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps([x for x in rows if 7<=x['batch']<=20],ensure_ascii=False,indent=2))
