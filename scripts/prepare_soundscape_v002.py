"""Build sourced, editable sound events and aligned ambience/foley/action stems."""
from pathlib import Path
import json, subprocess, wave, hashlib
import numpy as np
R=Path(__file__).resolve().parents[1]; O=R/'后期/声画重构-v002'; D=O/'声音'; D.mkdir(exist_ok=True)
SR=48000
def read(p):return json.loads(p.read_text(encoding='utf8'))
P=read(O/'后期执行计划.json'); OLD=read(R/'后期/导演后期修正-v001/后期执行计划.json')
S={s['id']:s for s in read(R/'资产/声音/音效-v001/来源清单.json')}
obj=read(O/('音效设计-对位.json' if (O/'音效设计-对位.json').exists() else '音效设计.json')); events=obj if isinstance(obj,list) else obj['events']
delta_path=O/'音效对位增量.json'
if delta_path.exists():
    delta=read(delta_path)
    assert delta['operation']=='append_events_only'
    events=events+delta['events']
def wav(p,x):
    with wave.open(str(p),'wb') as f:
        f.setnchannels(2); f.setsampwidth(3); f.setframerate(SR)
        q=(np.clip(x,-1,1)*8388607).astype('<i4').view('uint8').reshape(-1,4)[:,:3]
        f.writeframes(q.tobytes())
def mapped_event(e):
    b=P['batches'][e['batch_number']-1]
    # Events with explicit shot anchors follow the new adopted shot, not stale elapsed time.
    if e.get('anchor'):
        matches=[s for s in P['edl'] if s.get('anchor')==e['anchor']]
        assert len(matches)==1,(e['anchor'],len(matches))
        return matches[0]['record']/24+e['relative_time']
    t=e['relative_time']; old=OLD['batches'][e['batch_number']-1]
    anchors=P.get('batch_time_maps',{}).get(str(e['batch_number']))
    if anchors:t=float(np.interp(t,[x[0] for x in anchors],[x[1] for x in anchors]))
    return b['start']/24+t
stems={k:np.zeros((round(P['seconds']*SR),2),np.float32) for k in ['Ambience','Foley','Action','Magic']}
out=[]
for i,e in enumerate(events,1):
    src=S[e['source_id']]; start=mapped_event(e); duration=e['duration']
    kind=e.get('track','Foley'); kind={'environment':'Ambience','ambience':'Ambience','foley':'Foley','action':'Action','magic':'Magic'}.get(kind.lower(),kind)
    if kind=='Ambience' and not e.get('anchor'):duration=max(.001,mapped_event({**e,'relative_time':e['relative_time']+duration})-start)
    n=round(duration*SR)
    assert duration>0 and start>=0
    filters=['highpass=f='+str(e.get('highpass',60)),'lowpass=f='+str(e.get('lowpass',14000))]
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(e.get('source_in',0)),'-i',str(R/src['path']),'-t',str(duration),'-af',','.join(filters),'-ac','2','-ar',str(SR),'-f','f32le','pipe:1'],capture_output=True,check=True).stdout
    x=np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy()
    assert kind in stems,kind
    if len(x)<n:
        if kind=='Ambience' and len(x)>SR:
            # Equal-power seam, only for nonverbal environmental beds.
            original=x.copy(); xf=min(SR,len(x)//4)
            while len(x)<n:
                f=np.linspace(0,1,xf)[:,None]; x[-xf:]=x[-xf:]*(1-f)+original[:xf]*f
                x=np.concatenate((x,original[xf:]))
        else:x=np.pad(x,((0,n-len(x)),(0,0)))
    x=x[:n]
    if e.get('reverb',False):
        for delay,gain in [(0.067,.15),(.113,.09),(.181,.045)]:
            d=round(delay*SR)
            if d<len(x):x[d:]+=x[:-d].copy()*gain
    fi=min(n//2,round(e.get('fade_in',.5 if kind=='Ambience' else .008)*SR))
    fo=min(n//2,round(e.get('fade_out',.7 if kind=='Ambience' else .045)*SR))
    if fi:x[:fi]*=np.linspace(0,1,fi)[:,None]
    if fo:x[-fo:]*=np.linspace(1,0,fo)[:,None]
    x*=10**(e['gain_db']/20)
    pan=e.get('pan',0); x[:,0]*=min(1,1-pan);x[:,1]*=min(1,1+pan)
    # Gentle additional dialogue clearance without changing chosen performances.
    if kind in ('Ambience','Magic'):
        t=start+np.arange(n)/SR
        for v in P['voice']:
            a=v['record']/24;b=a+v['duration']
            mask=(t>=a-.08)&(t<=b+.18)
            if mask.any():
                env=np.minimum(np.clip((t-a+.08)/.08,0,1),np.clip((b+.18-t)/.18,0,1))
                x*= (1-.30*env)[:,None]
    ident=e.get('id',f'SFX-{i:03d}');p=D/(ident+'.wav');wav(p,x)
    offset=round(start*SR);count=min(n,len(stems[kind])-offset)
    assert count>0
    stems[kind][offset:offset+count]+=x[:count]
    out.append({**e,'id':ident,'track':kind,'start':start,'record':round(start*24),'path':str(p),'source_path':src['path'],'source_url':src['url'],'license_url':src['license_url'],'source_sha256':src['sha256'],'peak':float(np.abs(x).max()),'status':'designed_and_rendered_not_continuously_auditioned'})
stemrows=[]
for name,x in stems.items():
    p=D/(name+('-aligned2-stem.wav' if delta_path.exists() else '-stem.wav'));wav(p,x);stemrows.append({'id':name,'path':str(p),'record':0,'peak':float(np.abs(x).max()),'samples':len(x)})
(O/'音效施工记录.json').write_text(json.dumps({'events':out,'stems':stemrows,'sample_rate':SR,'library_status':'Fairlight本地常见安装位置未找到音效；按作者说明暂视为未安装。实际使用効果音ラボ已下载源素材。','verification_boundary':'源出处、时长、混音样本检查；不是完整主观听审。'},ensure_ascii=False,indent=2),encoding='utf8')
(O/'音效来源清单.json').write_text(json.dumps(list(S.values()),ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'events':len(out),'stems':stemrows},ensure_ascii=False))
