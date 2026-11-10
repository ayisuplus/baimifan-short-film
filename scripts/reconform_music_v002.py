"""Re-cut the approved original music at original speed after the picture pickups."""
from pathlib import Path
import json,subprocess,wave
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'后期/声画重构-v002';D=O/'声音';D.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf8'))
P=read(O/'后期执行计划.json');OLD=read(R/'后期/导演后期修正-v001/后期执行计划.json');M=read(R/'后期/导演后期修正-v001/声音施工记录.json');B=read(R/'后期/生成收口-v025/实际BGM剪辑.json');A=read(O/'采用剪辑.json')
SR=48000
def mapped(t):
    b=next((b for b in reversed(OLD['batches']) if t>=b['start']/24-.00001),OLD['batches'][0]);n=b['batch'];local=t-b['start']/24;k=P['batch_time_maps'][str(n)]
    return P['batches'][n-1]['start']/24+float(np.interp(local,[x[0] for x in k],[x[1] for x in k]))
def wav(p,x):
    with wave.open(str(p),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes())
silences=[{**s,'start':mapped(s['start']),'end':mapped(s['end'])} for s in M['silences']]
silences[3].update(start=P['batches'][30]['start']/24+6.816687,end=P['batches'][30]['start']/24+7.616687)
silences[-1].update(start=P['seconds']-4,end=P['seconds'])
voices=[(v['record']/24,v['record']/24+v['duration']) for v in P['voice']];mix=np.zeros((round(P['seconds']*SR),2),np.float32);cues=[]
for old in M['cues']:
    c=next(x for x in B['cues'] if x['id']==old['id']);start=round(mapped(old['start'])*24)/24;end=round(mapped(old['end'])*24)/24
    if c['id']=='M13':end=P['seconds']-4
    action=mapped(old['action']) if old.get('action') is not None else None
    override=A.get('music_action_overrides',{}).get(c['id'])
    if override:
        s=next(s for s in P['edl'] if s.get('anchor')==override['anchor']);action=s['record']/24+override['offset']
        if override.get('start_at_action'):start=round(action*24)/24
    if action is not None and start-1/24<action<start:action=start
    si=old['source_in'] if action is None else c['measured_source_transient']-(action-start)
    assert si>=0 and end>start,(c['id'],si,start,end)
    dur=end-start;n=round(dur*SR)
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(si),'-i',str(R/c['path']),'-t',str(dur),'-ac','2','-ar',str(SR),'-f','f32le','pipe:1'],capture_output=True,check=True).stdout
    x=np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy();assert len(x)>=n-2048,(c['id'],len(x),n)
    x=np.pad(x,((0,max(0,n-len(x))),(0,0)))[:n];t=np.arange(n)/SR;g=np.full(n,10**(c['nominal_gain_db']/20),np.float32)
    if c['fade_in_seconds']:g*=np.sin(np.minimum(1,t/c['fade_in_seconds'])*np.pi/2)
    if c['fade_out_seconds']:g*=np.sin(np.minimum(1,(dur-t)/c['fade_out_seconds'])*np.pi/2)
    duck=np.ones(n,np.float32);low=10**(c['dialogue_duck_additional_db']/20)
    for a,b in voices:
        a-=start;b-=start;attack=c['duck_attack_seconds'];release=c['duck_release_seconds']
        if b+release<0 or a-attack>dur:continue
        envelope=np.minimum(np.clip((t-a+attack)/attack,0,1),np.clip((b+release-t)/release,0,1));duck=np.minimum(duck,1-(1-low)*envelope)
    g*=duck
    for s in silences:
        lo=max(0,int(np.floor((s['start']-start)*SR)));hi=min(n,int(np.ceil((s['end']-start)*SR)))
        if hi>lo:g[lo:hi]=0
    x*=g[:,None];path=D/(c['id']+'-原速卡点-v002.wav');wav(path,x);off=round(start*SR);mix[off:off+n]+=x[:len(mix)-off]
    cues.append(dict(id=c['id'],path=str(path),record=round(start*24),start=start,end=end,source=str(R/c['path']),source_in=si,source_out=si+dur,action=action,transient=c.get('measured_source_transient'),rate=1,nominal_gain_db=c['nominal_gain_db'],duck_db=c['dialogue_duck_additional_db']))
assert not np.any(mix[-4*SR:]);wav(D/'BGM校验混音.wav',mix)
(O/'声音施工记录.json').write_text(json.dumps(dict(cues=cues,silences=silences,voices=P['voice'],peak=float(np.max(np.abs(mix))),status='reconformed_original_rate_not_continuously_auditioned'),ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'cues':len(cues),'voices':len(voices),'last_four_music_zero':True}))
