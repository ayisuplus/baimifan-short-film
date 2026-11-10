"""Measure the actual PCM assembly and select conservative shared output headroom."""
from pathlib import Path
import json,subprocess,wave,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'后期/声画重构-v002';SR=48000
def read(p):return json.loads(p.read_text(encoding='utf8'))
P=read(O/'后期执行计划.json');M=read(O/'声音施工记录.json');S=read(O/'音效施工记录.json')
mix=np.zeros((round(P['seconds']*SR),2),np.float32);rows=[]
for group,arr in [('voice',P['voice']),('music',M['cues']),('sound',S['stems'])]:
    for v in arr:
        p=Path(v['path']);p=p if p.is_absolute() else R/p
        raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','2','-ar',str(SR),'-f','f32le','pipe:1'])
        x=np.frombuffer(raw,dtype='<f4').reshape(-1,2);offset=round(v['record']/24*SR);count=min(len(x),len(mix)-offset)
        assert count>=len(x)-2048,(v['id'],len(x)-count)
        mix[offset:offset+count]+=x[:count]
        rows.append({'id':v['id'],'group':group,'samples':len(x),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assert np.all(np.isfinite(mix));peak=float(np.abs(mix).max());gain=min(-3,20*np.log10(.84/max(peak,1e-9)))
mix*=10**(gain/20)
# The author requested review in Resolve before any further preview/master exports.
# Check samples in memory; the separate editable sound assets are the working media.
result={'samples':len(mix),'unattenuated_peak':peak,'shared_gain_db':round(float(gain),3),'peak_after_gain':float(np.abs(mix).max()),'finite':True,'voices':sum(x['group']=='voice' for x in rows),'music':sum(x['group']=='music' for x in rows),'sfx_events':len(S['events']),'rows':rows,'boundary':'PCM样本计算及不削波验证；未宣称连续听审/对白可懂度/音素匹配通过。'}
(O/'混音电平检查.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False))
