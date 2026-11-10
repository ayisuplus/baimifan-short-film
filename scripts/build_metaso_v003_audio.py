"""Re-time one original-speed reply after the fan closes; preserve selected takes."""
import json,subprocess,hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'视频制作/Metaso-H3-v003';SR=48000
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decode(path,start=None,duration=None):
    cmd=['ffmpeg','-v','error']
    if start is not None:cmd+=['-ss',str(start)]
    cmd+=['-i',str(path)]
    if duration is not None:cmd+=['-t',str(duration)]
    return np.frombuffer(subprocess.check_output(cmd+['-ar',str(SR),'-ac','2','-f','f32le','-']),dtype='<f4').reshape(-1,2).copy()
w=read(ROOT/'后期/制作工作台-v025/工作台数据.json');b=next(b for b in w['batches'] if b['number']==21)
n=round(b['used_seconds']*SR);bgm_path=ROOT/'后期/生成收口-v025/BGM试听.wav'
assert bgm_path.exists()
bgm=decode(bgm_path,b['film_start'],b['used_seconds']);assert len(bgm)==n
duck=np.ones(n,dtype=np.float32);voice=np.zeros_like(bgm);events=[]
for c in w['cues']:
    if not b['film_start']<=c['start']<b['film_end']:continue
    delta=.45 if c['id']=='VO-CY026A1-01' else 0
    path=ROOT/c['aligned_option']['path']; samples=decode(path)
    start=round((c['start']-b['film_start']+delta)*SR);end=start+len(samples)
    assert 0<=start<end<=n
    voice[start:end]+=samples
    a=max(0,start-round(.1*SR));z=min(n,end+round(.45*SR));level=10**(-7/20)
    duck[a:start]=np.minimum(duck[a:start],np.linspace(1,level,start-a));duck[start:end]=np.minimum(duck[start:end],level);duck[end:z]=np.minimum(duck[end:z],np.linspace(level,1,z-end))
    events.append(dict(cue_id=c['id'],source=c['aligned_option']['path'],sha256=sha(path),source_samples=len(samples),sample_rate=SR,original_start=c['start'],new_start=c['start']+delta,delta_seconds=delta,playback_rate=1,source_trim=False))
mix=bgm*duck[:,None]+voice
assert float(np.max(np.abs(mix)))<1
dest=OUT/'声音/GB016-1-合扇后回应.wav';dest.parent.mkdir(parents=True,exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','pipe:0','-c:a','pcm_s24le',str(dest)],input=mix.astype('<f4').tobytes(),check=True)
report={'GB016-1':dict(path=dest.relative_to(ROOT).as_posix(),source_start=0,sha256=sha(dest),events=events,bgm_sha256=sha(bgm_path),duration=b['used_seconds'],note='沿用作者选声完整原速；千问短答仅后移0.45秒，在合扇后入声；BGM沿v025切片并重建-7dB对白避让，口型与完整听审待验。')}
(OUT/'声音修订.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'batch':21,'voice_events':len(events),'peak':float(np.abs(mix).max())},ensure_ascii=False))
