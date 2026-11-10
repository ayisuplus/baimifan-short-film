"""Editable working audio only; never renders a preview or delivery master."""
from pathlib import Path
import json,subprocess,wave,math
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'后期/导演重构-v003';D=O/'声音';D.mkdir(exist_ok=True);SR=48000
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
P=read(O/'后期执行计划.json');N=round(P['seconds']*SR)
def current(t):return t if t<3494/24 else max(3494/24,t-20/24)
def mapped(t):
 f=t*24
 for a,c,b,d in reversed(P['baseline_maps']):
  if a-.00001<=f<=b+.00001:return (d if b==a else c+(f-a)*(d-c)/(b-a))/24
 raise ValueError(t)
def oldmap(t):return mapped(current(t))
def anchor(name):return next(s['record']/24 for s in P['edl'] if s.get('anchor')==name)
def decode(path,si=0,dur=None,filters=None):
 cmd=['ffmpeg','-v','error','-ss',str(si),'-i',str(R/path)]
 if dur is not None:cmd+=['-t',str(dur)]
 if filters:cmd+=['-af',filters]
 raw=subprocess.check_output(cmd+['-ac','2','-ar',str(SR),'-f','f32le','pipe:1'])
 return np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy()
def wav(path,x):
 assert np.max(np.abs(x))<1,('working-file clipping',path,float(np.abs(x).max()))
 with wave.open(str(path),'wb') as f:
  f.setnchannels(2);f.setsampwidth(3);f.setframerate(SR)
  f.writeframes((x*8388607).astype('<i4').view('uint8').reshape(-1,4)[:,:3].tobytes())
def fit(x,n,loop=False):
 if len(x)<n and loop:
  orig=x.copy();xf=min(SR//2,len(x)//4)
  while len(x)<n:
   k=np.linspace(0,1,xf)[:,None];x[-xf:]=x[-xf:]*(1-k)+orig[:xf]*k;x=np.concatenate([x,orig[xf:]])
 return np.pad(x,((0,max(0,n-len(x))),(0,0)))[:n]
def fades(x,fi,fo):
 for reverse,s in [(False,fi),(True,fo)]:
  n=min(len(x)//2,round(s*SR))
  if n:
   g=np.sin(np.linspace(0,np.pi/2,n))[:,None]
   if reverse:x[-n:]*=g[::-1]
   else:x[:n]*=g
 return x
def level(x,target_rms=None,target_peak=None,max_gain=18):
 rms=float(np.sqrt(np.mean(x*x)));peak=float(np.abs(x).max());db=0
 if target_rms is not None:db=target_rms-20*np.log10(max(rms,1e-9))
 if target_peak is not None:
  p=target_peak-20*np.log10(max(peak,1e-9));db=min(db,p) if target_rms is not None else p
 db=min(max_gain,db);return x*10**(db/20),float(db)
def duck(x,start,db):
 t=np.arange(len(x))/SR+start;g=np.ones(len(x),np.float32);low=10**(db/20)
 for v in P['voice']:
  a=v['record']/24;b=a+v['duration'];env=np.minimum(np.clip((t-a+.12)/.12,0,1),np.clip((b+.3-t)/.3,0,1));g=np.minimum(g,1-(1-low)*env)
 return x*g[:,None]
# Keep the author's existing audio trim exactly, including the two pieces at B12.
for v in P['voice']:
 if v.get('original_path'):continue # Existing trimmed work sources preserve provenance on retry.
 x=decode(v['path'],v.get('source_start',0),v['duration']);n=round(v['duration']*SR);x=fit(x,n)
 path=D/(v['native_id']+'-工作源.wav');wav(path,x)
 v['original_path']=v['path'];v['path']=str(path);v['source_start']=0;v['source_end']=v['duration'];v['id_display']=v['native_id']
save(O/'后期执行计划.json',P)
coverage=read(O/'声音覆盖审查.json');silences=[dict(start=mapped(s['start']),end=mapped(s['end']),reason=s['reason']) for s in coverage['protected_silences']]
silences[-1].update(start=P['seconds']-4,end=P['seconds'])
music=[]
for c in read(R/'后期/声画重构-v002/声音施工记录.json')['cues']:
 a=round(oldmap(c['start'])*24)/24;b=round(oldmap(c['end'])*24)/24
 # Continuous original-source recut repairs the B12 user cut without cutting a beat out of the music.
 a=max(0,a-.4);b=min(P['seconds']-4,b+.4)
 action=oldmap(c['action']) if c.get('action') is not None else None
 si=max(0,c['source_in']-.4 if action is None else c['transient']-(action-a))
 music.append(dict(id=c['id'],source=c['source'],source_in=si,start=a,end=b,action=action,fade_in=.8,fade_out=.8,target_rms=-27 if c['id'] not in ['M07','M08','M10'] else -24))
for c in coverage['proposed_music_segments'][:4]:
 music.append(dict(id=c['id'],source=str(R/c['source_path']),source_in=c['source_in'],start=round(mapped(c['current_start'])*24)/24,end=round(mapped(c['current_end'])*24)/24,fade_in=c['fade_in_seconds'],fade_out=c['fade_out_seconds'],target_rms=-29,reason=c['role']))
musicmix=np.zeros((N,2),np.float32);trackends=[-1,-1,-1]
for c in sorted(music,key=lambda x:x['start']):
 n=round((c['end']-c['start'])*SR);x=decode(c['source'],c['source_in'],n/SR)
 assert len(x)>=n-2048,(c['id'],len(x),n)
 x=fit(x,n);x,g=level(x,c['target_rms'],-17,max_gain=8);x=fades(x,c['fade_in'],c['fade_out']);x=duck(x,c['start'],-6)
 t=np.arange(n)/SR+c['start']
 for silence_index,s in enumerate(silences):
  # 80 ms ramps into deliberate silence; no discontinuous digital mute.
  mute=np.minimum(np.clip((t-s['start']+.08)/.08,0,1),np.clip((s['end']+.08-t)/.08,0,1))
  if silence_index==1:mute[t>=s['end']]=0 # Door impact music onset must not be muted.
  x*=1-mute[:,None]
 c['path']=str(D/(c['id']+'-音乐工作段.wav'));c['record']=round(c['start']*24);c['gain_db']=g;c['duration']=n/SR
 j=next(j for j,e in enumerate(trackends) if e<=c['start']+.001);trackends[j]=c['end'];c['track']=j+2
 wav(Path(c['path']),x);i=round(c['start']*SR);musicmix[i:i+n]+=x[:N-i]
save(O/'声音施工记录.json',dict(cues=music,silences=silences,notes='原速源重切、跨淡及对白压低；4处长空缺试排；尚待连续听审'))
# Rebuild old events against source-aware edit mapping; remove replaced action foley.
sources={s['id']:s for s in read(R/'资产/声音/音效-v001/来源清单.json')+read(O/'新增音效来源.json')}
events=[]
for e in read(R/'后期/声画重构-v002/音效施工记录.json')['events']:
 if e['track']=='Ambience' and e['batch_number'] not in [22,23,24]:continue
 if (e['batch_number'] in [11,13,14,20,26]):continue
 t=oldmap(e['start']);dur=e['duration']
 e={**e,'start':t,'duration':dur}
 e['target_peak']=-26 if e['track']=='Foley' else -20
 if e['source_id'].startswith('rustling'):e['target_peak']=-29
 if e['batch_number'] in [7,8,9,12,15] and e['track']=='Foley':e['target_peak']=-25
 if e['track']=='Ambience':e.update(target_peak=-28,target_rms=-40,loop=True)
 events.append(e)
def ev(ident,src,kind,start,dur,peak=-24,**kw):
 events.append(dict(id=ident,source_id=src,track=kind,start=start,duration=dur,target_peak=peak,**kw))
def bed(ident,src,a,b,rms=-40,peak=-28,**kw):ev(ident,src,'Ambience',a,b-a,peak,target_rms=rms,fade_in=1,fade_out=1,loop=True,**kw)
# Location beds are continuous across cuts; the moon flashback has no outdoor wind.
bed('V3-air-opening','plants-swaying1',0,mapped(28.416667),-40)
bed('V3-palace','wind1',mapped(28.416667),mapped(79.583333),-44,-33,lowpass=1000)
bed('V3-night-exterior','wind3',mapped(79.583333),mapped(88.983333),-39,-27)
bed('V3-church-quiet','wind1',mapped(88.183333),mapped(168.916667),-42,-31,lowpass=850,reverb=True)
bed('V3-church-fire','fire1',mapped(168.916667),mapped(228.5),-36,-24)
bed('V3-church-fire-return','fire1',mapped(257),mapped(327.666667),-38,-26)
bed('V3-water-collect','water-flow1',mapped(282.333333),mapped(327.666667),-33,-22)
bed('V3-water-impact','waterfall-small1',mapped(327.666667),mapped(336.8),-27,-15)
bed('V3-water-aftermath','water-flow1',mapped(336.8),mapped(379.083333),-36,-25)
bed('V3-church-rescue','wind1',mapped(379.083333),mapped(442.125),-40,-29,lowpass=1200,reverb=True)
bed('V3-market-end','plants-swaying1',mapped(442.125),P['seconds'],-39,-27)
for t in [448,453,459]:ev('V3-bird-'+str(t),'sparrow-morning1','Ambience',mapped(t),3,-31)
# New action events are tied to visible contacts, never stale batch-relative times.
dec=read(O/'剪辑决定.json')
for e in dec.get('sound_events',[]):
 e=dict(e);name=e.pop('anchor',None);offset=e.pop('offset',0);t=anchor(name)+offset if name else mapped(e.pop('baseline_time'));ev(start=t,**e)
stems={k:np.zeros((N,2),np.float32) for k in ['Ambience','Foley','Action','Magic']};out=[]
for e in events:
 src=sources[e['source_id']];n=round(e['duration']*SR)
 x=decode(src['path'],e.get('source_in',0),e['duration'],f"highpass=f={e.get('highpass',55)},lowpass=f={e.get('lowpass',14000)}")
 x=fit(x,n,e.get('loop',False))
 if e.get('reverb'):
  for dt,g in [(.067,.12),(.113,.07),(.181,.04)]:
   d=round(dt*SR)
   if d<n:x[d:]+=x[:-d].copy()*g
 x,g=level(x,e.get('target_rms'),e.get('target_peak',-24),max_gain=24)
 x=fades(x,e.get('fade_in',.008),e.get('fade_out',.08))
 pan=e.get('pan',0);x[:,0]*=min(1,1-pan);x[:,1]*=min(1,1+pan)
 if e['track'] in ['Ambience','Magic']:x=duck(x,e['start'],-2.5)
 path=D/(e['id']+'-音效工作段.wav');wav(path,x);i=round(e['start']*SR);m=min(n,N-i);assert m>0
 stems[e['track']][i:i+m]+=x[:m]
 out.append({**e,'path':str(path),'gain_db':g,'peak':float(np.abs(x).max()),'source_path':src['path'],'source_url':src.get('url'),'license_url':src.get('license_url'),'source_sha256':src['sha256']})
rows=[]
for i,(name,x) in enumerate(stems.items(),5):
 path=D/(name+'-v003-stem.wav');wav(path,x);rows.append(dict(id=name,path=str(path),record=0,track=i,duration=P['seconds'],peak=float(np.abs(x).max())))
save(O/'音效施工记录.json',dict(events=out,stems=rows,sample_rate=SR,verification_boundary='逐事件源锚点、电平与样本检查；未冒称连续听审'))
mix=musicmix
for x in stems.values():mix+=x
for v in P['voice']:
 x=decode(v['path']);i=round(v['record']/24*SR);m=min(len(x),N-i);assert m>=len(x)-2048;mix[i:i+m]+=x[:m]
peak=float(np.abs(mix).max());gain=min(-3.,20*np.log10(.84/max(peak,1e-9)))
save(O/'混音电平检查.json',dict(shared_gain_db=round(gain,3),unattenuated_peak=peak,peak_after_gain=peak*10**(gain/20),finite=bool(np.isfinite(mix).all()),voice_pieces=len(P['voice']),music_cues=len(music),sfx_events=len(events),samples=N,export='未导出成片；检查在内存中进行',boundary='PCM无削波不等于响度、音色及听感验收'))
print(json.dumps(dict(voice=len(P['voice']),music=len(music),events=len(events),shared_gain_db=gain),ensure_ascii=False))
