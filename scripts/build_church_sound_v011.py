"""Rebuild working stems from edit mapping and explicit action anchors (no master export)."""
from pathlib import Path
import json,math,subprocess,hashlib
import numpy as np
import soundfile as sf
R=Path(__file__).resolve().parents[1];O=R/'后期/教堂动画修订-v011';A=O/'声音'/hashlib.sha256((O/'修订计划.json').read_bytes()).hexdigest()[:10];A.mkdir(exist_ok=True,parents=True)
def read(p):return json.loads(p.read_text(encoding='utf8'))
p=read(O/'修订计划.json');base=read(O/'修前基线.json');SR=48000;SPF=2000;N=p['frames']*SPF
def load(path):
 x,sr=sf.read(path,dtype='float32',always_2d=True)
 if sr!=SR:
  data=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ac','2','-ar',str(SR),'-f','f32le','pipe:1']);x=np.frombuffer(data,np.float32).reshape(-1,2).copy()
 if x.shape[1]==1:x=np.repeat(x,2,axis=1)
 return x[:,:2]
def ramp(x,fade=.015):
 x=x.copy();n=min(len(x)//2,round(fade*SR))
 if n:x[:n]*=np.linspace(0,1,n)[:,None];x[-n:]*=np.linspace(1,0,n)[:,None]
 return x
def put(dst,x,frame,gain=0):
 a=round(frame*SPF);lo=max(0,a);hi=min(len(dst),a+len(x))
 if hi>lo:dst[lo:hi]+=x[lo-a:hi-a]*(10**(gain/20))
def mapping(f):
 for m in p['maps']:
  if m['old_start']<=f<m['old_end']:
   ratio=1 if m['kind']=='unchanged' else (m['new_end']-m['new_start'])/(m['old_end']-m['old_start'])
   return m['new_start']+(f-m['old_start'])*ratio
 return p['frames'] if f>=11497 else f
events={x['id']:x for x in read(R/'后期/导演重构-v003/音效施工记录.json')['events']}
events.update({x['id']:x for x in read(R/'后期/局部收口-v008/声音施工增量.json')['events']})
w=p['water_start'];we=p['water_end']
spec=[('SFX-097',48,.6,0),('SFX-098',112,None,0),('V3-spear-whoosh',270,.6,0),('V3-fan-catch',354,None,0),('V3-fan-shield',354,.6,-5),('V3-water-collect',372,7,0),('SFX-110',540,4.5,0),('SFX-113',690,98/24,0),('SFX-116',724,None,0),('SFX-117',788,1.5,0),('SFX-120',790,.8,0),('SFX-125',884,1.4,0),('SFX-128',923,None,0),('SFX-126',923,105/24,0),('SFX-129',946,1.8,0),('SFX-130',1028,1.4,0),('V3-water-aftermath',1052,(1262-1052)/24,-3),('SFX-181',1188,None,0),('V3-church-fire-return',42,(989-42)/24,0)]
rows=[];checks=[];event_receipts=[]
for track in range(5,9):
 t=next(t for t in base['tracks'] if t['type']=='audio' and t['index']==track);old=load(t['items'][0]['path']);out=np.zeros((N,2),np.float32)
 for m in p['maps']:
  if m['kind']=='unchanged':
   a=round(m['old_start']*SPF);b=round(m['old_end']*SPF);put(out,old[a:b],m['new_start'])
  elif m['old_start']!=6303:
   ed=next(e for e in p['edits'] if e['start']==m['old_start']);offset=m['new_start']
   for s in ed['segments']:
    at=s.get('old_sound_start')
    if at is not None:put(out,ramp(old[round(at*SPF):round((at+s['frames'])*SPF)]),offset)
    offset+=s['frames']
 for eid,f,dur,gain in spec:
  e=events[eid]
  if e['track']!=t['name']:continue
  x=load(e['path']);x=x[:round(dur*SR)] if dur is not None else x;x=ramp(x,.03)
  if eid=='V3-church-fire-return':
   n=min(len(x),66*SPF);x[-n:]*=np.linspace(1,0,n)[:,None]
  if eid=='V3-water-collect':x[(444-372)*SPF:(480-372)*SPF]*=.35
  put(out,x,w+f,gain);event_receipts.append(dict(id=eid,track=track,record=w+f,relative=f,duration=len(x)/SR,incremental_gain_db=gain,source=e['path']))
 # Explicitly anchored local replacement sounds, never their rejected generated audio.
 for e in p['edits']:
  for fx in e.get('sound_events',[]):
   src=events[fx['id']]
   if src['track']!=t['name']:continue
   x=load(src['path']);x=x[:round(fx.get('duration',len(x)/SR)*SR)];put(out,ramp(x),e['new_start']+fx['offset'],fx.get('gain_db',0));event_receipts.append(dict(fx,record=e['new_start']+fx['offset'],track=track))
 peak=float(np.max(np.abs(out)));assert peak<.98,(t['name'],peak)
 path=A/(t['name']+'-v011-stem.wav');sf.write(path,out,SR,subtype='PCM_24')
 rows.append(dict(name=t['name']+'_v011',track=track,file=str(path),record=0,volume=t['items'][0]['properties'].get('AudioVolume',-3)))
 checks.append(dict(track=track,samples=N,peak=peak))
# Preserve existing music identities and source speed, trim to the new scene lengths.
for t in base['tracks']:
 if t['type']!='audio' or t['index'] not in [2,3]:continue
 for c in t['items']:
  x=load(c['path']);start=round(mapping(c['start']));end=round(mapping(c['end']))
  if c['name']=='M09':start=w-18;end=w+648
  elif c['name']=='M10':start=w+669;end=start+len(x)/SPF
  elif c['name']=='N02_aftermath':start=w+1038;end=start+len(x)/SPF
  length=max(0,round((end-start)*SPF))
  if not length:continue
  x=x[:length]
  if len(x)<length:x=np.pad(x,((0,length-len(x)),(0,0)))
  # Gentle fades on changed music boundaries and additional voice ducking.
  if abs(start-c['start'])>.01 or length<len(load(c['path'])):x=ramp(x,.35)
  env=np.ones(len(x),np.float32)
  for v in p['lines']:
   if not w<=v['record']<we:continue
   a=max(0,round((v['record']-start)*SPF)-4800);b=min(len(x),round((v['end']-start)*SPF)+7200)
   if b<=a:continue
   duck=np.full(b-a,.63,np.float32);n=min(4800,(b-a)//2);duck[:n]=np.linspace(1,.63,n);duck[-n:]=np.linspace(.63,1,n);env[a:b]=np.minimum(env[a:b],duck)
  x*=env[:,None];path=A/(c['name']+'-v011.wav');sf.write(path,x,SR,subtype='PCM_24')
  rows.append(dict(name=c['name'],track=t['index'],file=str(path),record=start,volume=c['properties'].get('AudioVolume',-3)))
result=dict(rows=rows,water_events=event_receipts,stems=checks,sample_rate=SR,old_generation_audio_used=False,dialogue_files_unchanged=True,continuous_listening_accepted=False)
(O/'声音施工.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Prepared',len(rows),'music/stem clips; water events',len(event_receipts),'samples',N)
