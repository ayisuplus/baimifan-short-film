"""Readback and PCM checks only; does not render/export a movie or a mix."""
from pathlib import Path
import json,subprocess,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'后期/局部收口-v008';SR=48000
def read(p):return json.loads(p.read_text(encoding='utf8'))
A=read(O/'修后实际状态.json');B=read(O/'修前实际状态.json');D=read(O/'剪辑施工增量.json')
changed={c['name'] for c in D['affected']};before={c['name']:c for c in B['video']};after={c['name']:c for c in A['video']}
untouched=[]
for name,b in before.items():
 if name in changed:continue
 a=after[name]
 for k in ['start','end','path','source_in','source_out','speed','props']:assert a[k]==b[k],(name,k,a[k],b[k])
 untouched.append(name)
v=A['video'];assert all(a['end']==b['start'] for a,b in zip(v,v[1:])) and v[-1]['end']==11497
mix=np.zeros((round(A['frames']*SR/24),2),np.float32);rows=[]
for c in A['audio']:
 assert Path(c['path']).exists()
 if not c['enabled']:continue
 dur=(c['end']-c['start'])/24
 data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(c['source_in']),'-i',c['path'],'-t',str(dur),'-ar',str(SR),'-ac','2','-f','f32le','pipe:1'])
 x=np.frombuffer(data,dtype='<f4').reshape(-1,2).copy();x*=10**(c['volume']/20)
 at=round(c['start']*SR/24);n=min(len(x),len(mix)-at);mix[at:at+n]+=x[:n]
 rows.append(dict(name=c['name'],track=c['track'],source=c['path'],samples=n,sample_peak_db=round(float(20*np.log10(max(np.abs(x).max(),1e-12))),3)))
peak=float(np.abs(mix).max());clipped=int(np.sum(np.abs(mix)>=1));assert np.isfinite(mix).all() and clipped==0,(peak,clipped)
maxidx=np.unravel_index(np.argmax(np.abs(mix)),mix.shape)[0]
result=dict(timeline=A['timeline'],frames=A['frames'],video_count=len(v),audio_count=len(A['audio']),untouched_video_count=len(untouched),untouched_video_names=untouched,voice_count=sum(c['track']==1 for c in A['audio']),no_picture_gaps=True,all_audio_files_exist=True,pcm_sample_peak_db=round(20*np.log10(peak),3),peak_frame=round(maxidx/SR*24,3),clipped_samples=clipped,method='48k stereo decoded sources, actual readback in/out and clip gain; mathematical sum before Fairlight bus/effects, not a native final mix or listening pass',continuous_listening_verified=False,final_lip_sync_verified=False,exported_master=False,audio=rows)
(O/'结构与PCM核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print({k:v for k,v in result.items() if k not in ['untouched_video_names','audio']})
