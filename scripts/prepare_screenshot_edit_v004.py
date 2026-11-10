"""Same-duration picture replacements; original timeline and all media are retained."""
from pathlib import Path
import json,copy
R=Path(__file__).resolve().parents[1];O=R/'后期/截图定点修正-v004';G=R/'视频制作/Metaso-H3-v007'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
p=read(R/'后期/导演重构-v003/后期执行计划.json');q=read(G/'执行队列.json');lookup={x['attempt_id']:x for x in q['items']};edits=[]
def seg(aid,lo,hi,batch,frames=None):
 return dict(source=str(G/'产物'/(aid+'.mp4')),**{'in':lo,'out':hi},frames=frames or hi-lo,batch=batch,props={},new_pickup=True)
def edit(a,b,segments,reason):
 assert sum(s['frames'] for s in segments)==b-a
 edits.append(dict(start=a,end=b,segments=segments,reason=reason))
edit(3478,3622,[seg('GB010-v007-father-style-audio-r1',0,144,12)],'教主原片质感三分之二侧脸；撤掉上一版极端放大追脸')
edit(3644,3758,[seg('GB011-v007-Claude-style-audio-r2',0,114,13)],'Claude怒斥使用实际选声口型参考，剔除误生鱼形物体')
edit(3914,4058,[seg('GB011-v007-Claude-style-audio-r2',114,258,14)],'整段恳求保持Claude；撤掉过早小鱼抓袍插入')
edit(9699,9781,[seg('GB027-v007-stair-eyeline-r1',0,82,37)],'阶上Claude与GPT肩后看阶下千问抱小鱼；撤掉重复反应和回切')
for name in ['前段补拍草案.json','后段补拍草案.json']:
 for x in read(O/name)['items']:
  if 'edit_mapping' in x:
   m=x['edit_mapping'];a,b=m['timeline_frames'];lo,hi=m['candidate_source_frames']
   ss=[seg(x['attempt_id'],lo,hi,x['batch_number'],b-a)]
   if 'remaining_original' in m:
    z=m['remaining_original'];b=z['timeline_frames'][1];ss.append(dict(source=str(R/m['original_source']),**{'in':z['source_frames'][0],'out':z['source_frames'][1]},frames=z['timeline_frames'][1]-z['timeline_frames'][0],batch=x['batch_number'],props={}))
  else:a,b=x['timeline_replace_frames'];lo,hi=x['use_candidate_frames'];ss=[seg(x['attempt_id'],lo,hi,x['batch_number'],b-a)]
  edit(a,b,ss,x['change_reason'])
# Optional reviewed source/interval overrides are explicit, not generated implicitly.
override=O/'剪辑修正增量.json'
if override.exists():
 for x in read(override)['replace_edits']:
  edits=[e for e in edits if e['start']!=x['start']];edits.append(x)
edits.sort(key=lambda e:e['start']);assert all(a['end']<=b['start'] for a,b in zip(edits,edits[1:]))
new=[];affected=[];replacement=[]
def original_piece(s,a,b,suffix):
 t=copy.deepcopy(s);t['record']=a;t['frames']=b-a;t['in']=s['in']+round((a-s['record'])*s['speed']/100);t['out']=s['in']+round((b-s['record'])*s['speed']/100);t['name']=s['name']+suffix;return t
for s in p['edl']:
 overlaps=[e for e in edits if e['start']<s['record']+s['frames'] and e['end']>s['record']]
 if not overlaps:new.append(copy.deepcopy(s));continue
 affected.append(dict(name=s['name'],start=s['record'],end=s['record']+s['frames']))
 cursor=s['record'];end=cursor+s['frames']
 for e in overlaps:
  if cursor<e['start']:
   z=original_piece(s,cursor,e['start'],'_v004_keep');new.append(z);replacement.append(z)
  cursor=max(cursor,e['end'])
 if cursor<end:
  z=original_piece(s,cursor,end,'_v004_keep');new.append(z);replacement.append(z)
for e in edits:
 cursor=e['start']
 for j,s in enumerate(e['segments'],1):
  s=copy.deepcopy(s);s.update(record=cursor,speed=(s['out']-s['in'])/s['frames']*100,name=f"B{s['batch']:02d}_v004_{e['start']}_{j:02d}",note=e['reason'])
  cursor+=s['frames'];new.append(s);replacement.append(s)
 assert cursor==e['end']
new.sort(key=lambda s:s['record']);replacement.sort(key=lambda s:s['record']);assert new[0]['record']==0
assert all(a['record']+a['frames']==b['record'] for a,b in zip(new,new[1:]));assert new[-1]['record']+new[-1]['frames']==p['frames']
for s in new:
 assert Path(s['source']).exists(),s['source']
newp=copy.deepcopy(p);newp.update(timeline='v004_Screenshot_Targeted_Fixes',edl=new)
next(v for v in newp['voice'] if v['id']=='VO-CY009-01')['record']+=7
save(O/'后期执行计划.json',newp);save(O/'剪辑决定.json',dict(edits=edits,affected_originals=affected,replacement_clips=replacement,voice_shift=dict(id='VO-CY009-01',frames=7),total_frame_delta=0))
print(dict(edited_windows=len(edits),replaced_original_clips=len(affected),replacement_clips=len(replacement),total_clips=len(new),frames=p['frames']))
