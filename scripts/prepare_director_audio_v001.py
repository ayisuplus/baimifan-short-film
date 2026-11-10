"""Render editable music cues against the repaired picture, keeping selected voices intact."""
from pathlib import Path
import json, subprocess, wave
import numpy as np

R=Path(__file__).resolve().parents[1];O=R/'后期/导演后期修正-v001';D=O/'声音';D.mkdir(exist_ok=True)
P=json.loads((O/'后期执行计划.json').read_text(encoding='utf8'))
B=json.loads((R/'后期/生成收口-v025/实际BGM剪辑.json').read_text(encoding='utf8'))
SR=48000
def mapped(t):
    b=next((b for b in reversed(P['batches']) if t>=b['old_start']-0.00001),P['batches'][0])
    local=max(0,t-b['old_start'])*24
    ss=[s for s in P['edl'] if s['batch']==b['batch'] and s['source_batch']==b['batch']]
    for s in ss:
        if s['in']<=local<=s['out']:
            return (s['record']+(local-s['in'])*s['frames']/(s['out']-s['in']))/24
    edges=[(abs(local-s[e]),(s['record']+(s['frames'] if e=='out' else 0))/24) for s in ss for e in ['in','out']]
    return min(edges)[1]
def wav(path,x):
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes())
silences=[dict(id=s['id'],start=mapped(s['timeline_start']),end=mapped(s['timeline_end']),reason=s['reason']) for s in B['silences']]
silences[3].update(start=P['batches'][30]['start']/24+6.816687,end=P['batches'][30]['start']/24+7.616687)
silences[-1].update(start=P['seconds']-4,end=P['seconds'])
voices=[(v['record']/24,v['record']/24+v['duration']) for v in P['voice']]
mix=np.zeros((round(P['seconds']*SR),2),np.float32);cues=[]
for c in B['cues']:
    start=round(mapped(c['timeline_start'])*24)/24;end=round(mapped(c['timeline_end'])*24)/24
    if c['id']=='M13':end=P['seconds']-4
    action=mapped(c['aligned_action_timeline']) if c.get('aligned_action_timeline') is not None else None
    if action is not None and start-1/24<action<start:action=start # Snap a boundary transient to the first displayed frame.
    si=c['source_in'] if action is None else c['measured_source_transient']-(action-start)
    assert si>=0 and end>start,(c['id'],si,start,end)
    dur=end-start;n=round(dur*SR)
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(si),'-i',str(R/c['path']),'-t',str(dur),'-ac','2','-ar',str(SR),'-f','f32le','pipe:1'],capture_output=True,check=True).stdout
    x=np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy();assert len(x)>=n-2048,(c['id'],len(x),n,si,dur)
    x=np.pad(x,((0,max(0,n-len(x))),(0,0)))[:n]
    t=np.arange(n)/SR;g=np.ones(n,np.float32)*10**(c['nominal_gain_db']/20)
    fi=c['fade_in_seconds'];fo=c['fade_out_seconds']
    if fi:g*=np.sin(np.minimum(1,t/fi)*np.pi/2)
    if fo:g*=np.sin(np.minimum(1,(dur-t)/fo)*np.pi/2)
    duck=np.ones(n,np.float32);low=10**(c['dialogue_duck_additional_db']/20)
    for a,b in voices:
        a-=start;b-=start;attack=c['duck_attack_seconds'];release=c['duck_release_seconds']
        if b+release<0 or a-attack>dur:continue
        env=np.ones(n,np.float32);q=(t>=a)&(t<=b);env[q]=low
        q=(t>=a-attack)&(t<a);env[q]=1-(1-low)*(t[q]-a+attack)/attack
        q=(t>b)&(t<=b+release);env[q]=low+(1-low)*(t[q]-b)/release
        duck=np.minimum(duck,env)
    g*=duck
    for s in silences:
        lo=max(0,int(np.floor((s['start']-start)*SR)));hi=min(n,int(np.ceil((s['end']-start)*SR)))
        if hi>lo:g[lo:hi]=0
    x*=g[:,None];path=D/(c['id']+'-原速卡点-r2.wav');wav(path,x)
    off=round(start*SR);mix[off:off+n]+=x[:len(mix)-off]
    cues.append(dict(id=c['id'],path=str(path),record=round(start*24),start=start,end=end,source=str(R/c['path']),source_in=si,source_out=si+dur,action=action,transient=c.get('measured_source_transient'),rate=1,nominal_gain_db=c['nominal_gain_db'],duck_db=c['dialogue_duck_additional_db']))
wav(D/'BGM校验混音.wav',mix)
assert not np.any(mix[-4*SR:])
result=dict(cues=cues,silences=silences,voices=P['voice'],peak=float(np.max(np.abs(mix))),status='measured_alignment_candidate_not_audition_approved',sfx_status='independent_foley_and_ambience_not_yet_finished')
(O/'声音施工记录.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'music_cues':len(cues),'voices':len(voices),'peak':result['peak'],'final_four_music_zero':True}))
