"""Freeze reviewed batch-3 windows and rebuild only its local foley interval."""
from pathlib import Path
import json,hashlib
import numpy as np,soundfile as sf
R=Path(__file__).resolve().parents[1];O=R/'后期/逐镜修订-v012/第三批'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
b=read(O/'修前实际工程.json');tr=next(x for x in b['tracks'] if x['type']=='audio' and x['index']==6);assert len(tr['items'])==1
old,sr=sf.read(tr['items'][0]['path'],dtype='float32',always_2d=True);assert sr==48000
new=old.copy();lo=682*2000;hi=946*2000;new[lo:hi]=0
events={x['id']:x for x in read(R/'后期/导演重构-v003/音效施工记录.json')['events']}
anchors=[('SFX-176',.25,.26,-4),('SFX-177',.65,.26,-4),('SFX-176',1.05,.26,-4),('SFX-177',1.5,.26,-4),('SFX-009',2.1,1.4,-2),('SFX-009',7.25,.9,-4),('SFX-176',8.5,.26,-3),('SFX-177',8.9,.26,-3),('SFX-176',9.35,.26,-4),('SFX-177',9.85,.26,-4),('SFX-176',10.25,.26,-4),('SFX-177',10.65,.26,-5)]
receipts=[]
for id,t,dur,gain in anchors:
 src=events[id];x,rate=sf.read(src['path'],dtype='float32',always_2d=True);assert rate==sr
 if x.shape[1]==1:x=np.repeat(x,2,axis=1)
 x=x[:round(dur*sr)].copy();n=min(round(.015*sr),len(x)//2);x[:n]*=np.linspace(0,1,n)[:,None];x[-n:]*=np.linspace(1,0,n)[:,None]
 at=lo+round(t*sr);end=min(at+len(x),hi);new[at:end]+=x[:end-at]*10**(gain/20)
 receipts.append(dict(id=id,source=src['path'],relative_seconds=t,duration=(end-at)/sr,incremental_gain_db=gain))
assert np.max(np.abs(new))<1
a=O/'声音';a.mkdir(exist_ok=True);dest=a/'Foley-v012-B03.wav';assert not dest.exists()
sf.write(dest,new,sr,subtype='PCM_24');back,_=sf.read(dest,dtype='float32',always_2d=True)
assert np.array_equal(old[:lo],back[:lo]) and np.array_equal(old[hi:],back[hi:])
path='视频制作/Metaso-H3-v015/产物/GB003-v015-guards-night-r2.mp4';source=R/path
video=[dict(path=path,sha256=sha(source),**{'in':0,'out':234},frames=234,speed=100),dict(path=path,sha256=sha(source),**{'in':247,'out':277},frames=30,speed=100)]
result=dict(review_passed=True,review_scope='Independent dense-frame check plus lead review; low spear barrier and fixed guards verified. Remove [234,247) spatial morph, use hard cut. Not full-film artistic acceptance.',video=video,foley=dict(path=dest.relative_to(R).as_posix(),sha256=sha(dest),changed_frames=[682,946],outside_interval_pcm_exact=True,events=receipts),voice_subtitles_unchanged=True,author_final_accepted=False)
(O/'采用施工.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print('Prepared 264 frames at native speed, foley changes bounded to B03')
