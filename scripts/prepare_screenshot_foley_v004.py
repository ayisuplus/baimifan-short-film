"""Rebuild only the changed foley stem from existing licensed working sounds."""
from pathlib import Path
import json,subprocess,wave,copy
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'后期/截图定点修正-v004';D=O/'声音';D.mkdir(exist_ok=True);SR=48000
def read(p):return json.loads(p.read_text(encoding='utf8'))
def decode(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','2','-ar',str(SR),'-f','f32le','pipe:1']),dtype='<f4').reshape(-1,2).copy()
def wav(p,x):
 assert np.isfinite(x).all() and np.abs(x).max()<1
 with wave.open(str(p),'wb') as w:
  w.setnchannels(2);w.setsampwidth(3);w.setframerate(SR);w.writeframes((x*8388607).astype('<i4').view('uint8').reshape(-1,4)[:,:3].tobytes())
p=read(R/'后期/导演重构-v003/后期执行计划.json');f=read(R/'后期/导演重构-v003/音效施工记录.json');events=copy.deepcopy([e for e in f['events'] if e['track']=='Foley']);lookup={e['id']:e for e in events}
lookup['SFX-014'].update(start=1694/24,purpose='说完切回离开动作，衣擦随转身接点后移')
events=[e for e in events if e['id'] not in ['SFX-178','SFX-179','SFX-180']]
for ident,src,t,gain,purpose in [('V4-entry-step1','SFX-178',200.333333,-3,'群像侧向警戒步，轻于原三连脚步'),('V4-entry-step2','SFX-178',201.083333,-5,'队伍散开第二落步'),('V4-hole-palm','SFX-020',89.125,-8,'洞内双手膝盖接地，轻触低音'),('V4-hole-cloth','SFX-014',88.75,-6,'帽鳍离洞与衣服摩擦')]:
 e=copy.deepcopy(lookup[src]);e.update(id=ident,start=t,extra_gain_db=gain,purpose=purpose,reused_working_source=src);events.append(e)
n=round(p['seconds']*SR);stem=np.zeros((n,2),np.float32)
for e in events:
 x=decode(e['path'])*10**(e.get('extra_gain_db',0)/20);i=round(e['start']*SR);m=min(len(x),n-i);stem[i:i+m]+=x[:m];e['record']=round(e['start']*24)
path=D/'Foley-v004-stem.wav';wav(path,stem)
newstem=dict(id='Foley',path=str(path),record=0,track=6,duration=p['seconds'],peak=float(np.abs(stem).max()))
other=[e for e in f['events'] if e['track']!='Foley'];stems=[newstem if s['id']=='Foley' else s for s in f['stems']]
(O/'音效施工记录.json').write_text(json.dumps(dict(events=other+events,stems=stems,sample_rate=SR,changes='仅重排转身、群像落步、补洞口内落地衣擦。其他音效、音乐、环境声原位保留。',verification_boundary='事件与候选画面对位，未宣称完整连续听审'),ensure_ascii=False,indent=2),encoding='utf8')
# PCM check in memory; no master or preview export.
mix=stem
for s in stems:
 if s['id']!='Foley':mix+=decode(s['path'])[:n]
for c in read(R/'后期/导演重构-v003/声音施工记录.json')['cues']:
 x=decode(c['path']);i=round(c['start']*SR);m=min(len(x),n-i);mix[i:i+m]+=x[:m]
for v in p['voice']:
 x=decode(v['path']);i=round((v['record']+(7 if v['id']=='VO-CY009-01' else 0))/24*SR);m=min(len(x),n-i);mix[i:i+m]+=x[:m]
peak=float(np.abs(mix).max());assert peak*10**(-3/20)<1
(O/'混音电平检查.json').write_text(json.dumps(dict(unattenuated_peak=peak,shared_gain_db=-3,peak_after_gain=peak*10**(-3/20),finite=bool(np.isfinite(mix).all()),exported_video_or_master=False,verification_boundary='PCM样本电平检查不等于听感、响度和音色最终验收'),ensure_ascii=False,indent=2),encoding='utf8')
print(dict(foley_events=len(events),peak=peak,stem=str(path)))
