"""Check the saved edit/media plan without rendering a video."""
from pathlib import Path
import json, hashlib, subprocess
R=Path(__file__).resolve().parents[1]; O=R/'后期/声画重构-v002'
def read(p): return json.loads(p.read_text(encoding='utf8'))
def absolute(s):
    p=Path(s); return p if p.is_absolute() else R/p
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
P=read(O/'后期执行计划.json'); old=read(R/'后期/导演后期修正-v001/后期执行计划.json')
cursor=0
for s in P['edl']:
    assert s['record']==cursor,(s['name'],cursor)
    assert s['frames']>0 and s['out']>s['in']
    assert absolute(s['source']).is_file(),s['source']
    cursor+=s['frames']
assert cursor==P['frames']
assert len(P['batches'])==44
assert len(P['voice'])==len(old['voice'])==63
oldvoices={v['id']:v for v in old['voice']}
voices=[]
for v in P['voice']:
    prior=oldvoices[v['id']];path=absolute(v['path'])
    assert path.resolve()==absolute(prior['path']).resolve(),v['id']
    assert abs(v['duration']-prior['duration'])<.001
    assert v['record']>=0 and v['record']/24+v['duration']<=P['seconds']+1/24
    voices.append({'id':v['id'],'sha256':digest(path),'source_unchanged':True})
originals=[]
for b in read(R/'后期/导演全片审查-v001/当前44批审查清单.json'):
    actual=digest(absolute(b['path']))
    assert actual==b['sha256'],b['id']
    originals.append({'batch':b['batch_number'],'sha256':actual})
native=read(O/'达芬奇时间线核对.json')['result']
assert native['frames']==P['frames'] and len(native['video'])==len(P['edl'])
assert all(i['start']==s['record'] and i['end']-i['start']==s['frames'] for i,s in zip(native['video'],P['edl']))
nv={i['name']:i for i in native['audio'] if i['track']==1}
assert len(nv)==63
assert all(abs(nv[s['id']]['duration']/24-s['duration'])<.002 and nv[s['id']]['start']==s['record'] and nv[s['id']]['speed']['Percentage']==100 for s in P['voice'])
result={'timeline':P['timeline'],'video_segments':len(P['edl']),'frames':cursor,'seconds':P['seconds'],'continuous_video_plan':True,'native_video_matches_plan':True,'native_voices_full_length_original_speed':True,'selected_voice_files':voices,'original_44_batches':originals,'export_policy':'用户要求最终核验通过并明确要求后再导出；本检查不渲染、不导出。','boundary':'文件、剪辑计划、来源完整性及实际时间线读回核验，不代替连续听审或主观视觉验收。'}
(O/'文件与剪辑计划检查.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if not isinstance(v,list)},ensure_ascii=False))
