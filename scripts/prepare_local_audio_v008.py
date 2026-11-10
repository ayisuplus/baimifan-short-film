"""Reversible working sources for verified contact timing and a memory-return bridge."""
from pathlib import Path
import json,subprocess,wave,copy
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'后期/局部收口-v008';D=O/'声音';D.mkdir(exist_ok=True);SR=48000
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def decode(p,si=0,duration=None):
 c=['ffmpeg','-v','error','-ss',str(si),'-i',str(p)]
 if duration is not None:c+=['-t',str(duration)]
 return np.frombuffer(subprocess.check_output(c+['-ac','2','-ar',str(SR),'-f','f32le','pipe:1']),dtype='<f4').reshape(-1,2).copy()
def wav(p,x):
 assert np.isfinite(x).all() and np.abs(x).max()<1
 with wave.open(str(p),'wb') as w:
  w.setnchannels(2);w.setsampwidth(3);w.setframerate(SR);w.writeframes((x*8388607).astype('<i4').view('uint8').reshape(-1,4)[:,:3].tobytes())
P=read(R/'后期/二维动漫纠偏-v005/后期执行计划.json');B=read(O/'修前实际状态.json');N=P['frames']*2000
F=read(R/'后期/截图定点修正-v004/音效施工记录.json');events=copy.deepcopy(F['events']);changes=[]
targets={'V3-father-push':(3842,'推出瞬间，不在触肩时抢先重击'),'V3-father-slip':(3843,'推出后鞋底开始滑'),'V3-father-hand':(3857,'手掌首次落地'),'V3-father-ground':(3860,'随后身体/膝部受力'),'V3-turn-cloth':(3083,'切到下阶前衣料预入')}
for e in events:
 if e['id'] in ['SFX-031','SFX-032','SFX-033']:
  old=e['start'];e['start']=old-18/24;e['record']=round(e['start']*24)
  changes.append(dict(id=e['id'],old_start=old,new_start=e['start'],reason='B10下阶剪点提前18帧，源入点不变，三次落步等量提前'))
 if e['id'] in targets:
  f,reason=targets[e['id']];changes.append(dict(id=e['id'],old_start=e['start'],new_start=f/24,reason=reason));e.update(start=f/24,record=f,purpose=reason)
# Quiet first contact is distinct from the later push impulse.
contact=copy.deepcopy(next(e for e in events if e['id']=='V3-push-cloth'));contact.update(id='V8-father-contact',start=3824/24,record=3824,extra_gain_db=-4,purpose='手先接触肩臂，再发生推出，不做第二次重撞');events.append(contact)
replacements=[]
for kind,track in [('Foley',6),('Action',7)]:
 stem=np.zeros((N,2),np.float32)
 for e in events:
  if e['track']!=kind:continue
  x=decode(e['path'])*10**(e.get('extra_gain_db',0)/20);at=round(e['start']*SR);n=min(len(x),N-at);stem[at:at+n]+=x[:n]
 path=D/(kind+'-v008-stem.wav');wav(path,stem)
 replacements.append(dict(name=kind,path=str(path),track=track,record=0,frames=P['frames'],volume=-3))
M=read(R/'后期/导演重构-v003/声音施工记录.json');c=next(x for x in M['cues'] if x['id']=='M09');oldrecord=c['record'];newrecord=6285;delta=(oldrecord-newrecord)/24;end=8007
x=decode(c['source'],c['source_in']-delta,(end-newrecord)/24);n=(end-newrecord)*2000;x=np.pad(x,((0,max(0,n-len(x))),(0,0)))[:n]*10**(c['gain_db']/20)
# Fixed source gain, original source mapping and old tail. Never retime the music.
time=np.arange(n)/SR+c['start']-delta;g=np.ones(n,np.float32)
for v in P['voice']:
 a=v['record']/24;b=a+v['duration'];env=np.minimum(np.clip((time-a+.12)/.12,0,1),np.clip((b+.3-time)/.3,0,1));g=np.minimum(g,1-(1-10**(-6/20))*env)
x*=g[:,None];xf=36*2000;x[:xf]*=np.sin(np.linspace(0,np.pi/2,xf))[:,None]
# After original fade-in finishes use the exact old samples, preserving every later card point and deliberate silence.
old=decode(c['path']);splice=oldrecord-newrecord+20;sample=splice*2000;oi=20*2000;length=min(n-sample,len(old)-oi)
x[sample:sample+length]=old[oi:oi+length]
# Short crossfade around the sample splice avoids a phase discontinuity.
k=480;before=x[sample-k:sample+k].copy();oldpart=old[oi-k:oi+k];a=np.linspace(0,1,2*k)[:,None];x[sample-k:sample+k]=before*(1-a)+oldpart*a
path=D/'M09-return-bridge-v008.wav';wav(path,x);replacements.append(dict(name='M09',path=str(path),track=2,record=newrecord,frames=end-newrecord,volume=-3))
c2=next(x for x in M['cues'] if x['id']=='N01_flashback');x=decode(c2['path'])[:(6321-c2['record'])*2000];x[-xf:]*=np.cos(np.linspace(0,np.pi/2,xf))[:,None]
path=D/'N01-return-bridge-v008.wav';wav(path,x);replacements.append(dict(name='N01_flashback',path=str(path),track=3,record=c2['record'],frames=6321-c2['record'],volume=-3))
voice_stats=[]
for v in P['voice']:
 x=decode(v['path']);peak=float(np.abs(x).max());blocks=x[:len(x)//480*480].reshape(-1,480,2);energy=np.mean(blocks*blocks,axis=(1,2));gate=max(1e-7,float(energy.max())*.01);active=energy[energy>gate]
 rms=float(np.sqrt(active.mean())) if len(active) else 0
 voice_stats.append(dict(id=v['id'],role=v['role'],record=v['record'],active_rms_db=round(20*np.log10(max(rms,1e-10)),2),sample_peak_db=round(20*np.log10(max(peak,1e-10)),2),unchanged=True))
save(O/'对白电平复核.json',dict(method='10ms active RMS and sample peak, not LUFS or listening; no automatic normalization of acting dynamics',items=voice_stats,voices_changed=False,timbre_changed=False))
save(O/'声音施工增量.json',dict(replacements=replacements,events=events,changes=changes,music_bridge=dict(start=6285,cut=6303,end=6321,old_source_mapping_after=6409,old_tail=8007),voice_sources_and_timing_unchanged=True,dialogue_gain_changes_in='对白增益修正.json',existing_kimi_event_positions_unchanged=True,continuous_listening_verified=False,exported_master=False))
print('Prepared four reversible audio sources; original voices and all protected silence retained')
