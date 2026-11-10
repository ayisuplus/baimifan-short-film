"""Rebuild an edit plan from the actual author-modified Resolve baseline."""
from pathlib import Path
import json,copy,math
R=Path(__file__).resolve().parents[1];O=R/'后期/导演重构-v003';FPS=24
def read(p):return json.loads(p.read_text(encoding='utf8'))
old=read(R/'后期/声画重构-v002/后期执行计划.json');actual=read(O/'开始时达芬奇实际状态.json')['result'];props=read(O/'开始时画面属性.json')['result']['video'];dec=read(O/'剪辑决定.json')
lookup={s['name']:s for s in old['edl']};propmap={s['name']:s['props'] for s in props}
allowed=['Pan','Tilt','ZoomX','ZoomY','RotationAngle','AnchorPointX','AnchorPointY','Pitch','Yaw','FlipX','FlipY','CropLeft','CropRight','CropTop','CropBottom','CropSoftness','CropRetain']
base=[]
for a in actual['video']:
 s=copy.deepcopy(lookup[a['name']]);s.update(record=a['start'],frames=a['end']-a['start'],speed=a['speed']['Percentage']);s['in']=a['source_in'];s['out']=s['in']+round(s['frames']*s['speed']/100)
 s['props']={k:v for k,v in propmap[a['name']].items() if k in allowed};base.append(s)
edl=[];cursor=0;maps=[]
def put(s):
 global cursor
 s=copy.deepcopy(s);s['record']=cursor;s['speed']=(s['out']-s['in'])/s['frames']*100;s['source']=str((R/s['source']).resolve()) if not Path(s['source']).is_absolute() else s['source'];edl.append(s);cursor+=s['frames']
def original(lo,hi):
 for s in base:
  a=max(lo,s['record']);b=min(hi,s['record']+s['frames'])
  if b<=a:continue
  t=copy.deepcopy(s);t['in']=s['in']+round((a-s['record'])*s['speed']/100);t['out']=s['in']+round((b-s['record'])*s['speed']/100);t['frames']=b-a;put(t)
oldcursor=0
for e in sorted(dec['edits'],key=lambda e:(e['start'],e['end'])):
 assert e['start']>=oldcursor,(e,oldcursor)
 newstart=cursor;original(oldcursor,e['start']);maps.append([oldcursor,newstart,e['start'],cursor])
 a=cursor
 for j,s in enumerate(e['segments']):
  s={**s,'name':s.get('name',f'B{e["batch"]:02d}_v003_{e["id"]}_{j+1:02d}'),'batch':e['batch'],'props':s.get('props',{}),'note':e['reason']}
  put(s)
 maps.append([e['start'],a,e['end'],cursor]);oldcursor=e['end']
newstart=cursor;original(oldcursor,actual['frames']);maps.append([oldcursor,newstart,actual['frames'],cursor])
def mapped(frame):
 for a,c,b,d in reversed(maps):
  if a<=frame<=b:
   return d if b==a else c+(frame-a)*(d-c)/(b-a)
 raise ValueError(frame)
batches=[]
for ob in old['batches']:
 clips=[s for s in edl if s['batch']==ob['batch']];a=min(s['record'] for s in clips);end=max(s['record']+s['frames'] for s in clips)
 batches.append({**ob,'start':a,'frames':end-a})
voice_lookup={v['id']:v for v in old['voice']};voices=[];counts={}
tempo={v['id']:v for v in read(O/'咏唱速度候选.json')}
for a in actual['audio']:
 if a['track']!=1:continue
 v=copy.deepcopy(voice_lookup[a['name']]);counts[a['name']]=counts.get(a['name'],0)+1;v['part']=counts[a['name']];v['native_id']=a['name']+('-part2' if v['part']>1 else '')
 v.update(record=round(mapped(a['start'])),duration=(a['end']-a['start'])/FPS,source_start=a['source_start_time'],source_end=a['source_end_time'])
 if v['id'] in tempo and v['id'] in dec.get('tempo_voice_ids',[]):
  t=tempo[v['id']];v.update(path=t['path'],duration=t['duration'],source_start=0,source_end=t['duration'],rate=t['rate'])
 override=dec.get('voice_overrides',{}).get(v['id'])
 if override:
  if 'anchor' in override:
   anchor=next(s for s in edl if s.get('anchor')==override['anchor']);v['record']=anchor['record']+round(override['offset']*FPS)
   if override.get('retain_part_offsets'):v['record']+=round(a['start']-next(x['start'] for x in actual['audio'] if x['track']==1 and x['name']==a['name']))
  else:v['record']+=override.get('shift_frames',0)
 voices.append(v)
for a,b in zip(sorted(voices,key=lambda v:v['record']),sorted(voices,key=lambda v:v['record'])[1:]):
 assert a['record']/FPS+a['duration']<=b['record']/FPS+.005,(a['id'],b['id'])
result={'timeline':'v003_Dramatic_Reconstruction','fps':24,'width':1344,'height':768,'edl':edl,'frames':cursor,'seconds':cursor/FPS,'batches':batches,'voice':voices,'baseline_maps':maps,'baseline_actual_frames':actual['frames'],'author_edit_preserved':'B12原有20帧删改及音频切片以实际快照为准；未回滚v002。','export_policy':'仅工程内审阅；作者最终核验并明确要求后再导出'}
(O/'后期执行计划.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'clips':len(edl),'frames':cursor,'seconds':cursor/24,'voice_pieces':len(voices)},ensure_ascii=False))
