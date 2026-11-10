"""Build versioned, source-traceable church edits and voice/subtitle retiming."""
from pathlib import Path
import json,copy,math
R=Path(__file__).resolve().parents[1];O=R/'后期/教堂动画修订-v011';O.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
base=read(R/'后期/局部收口-v008/后期执行计划.json');voice=read(R/'后期/对白字幕同步-v010/同步计划.json');snap=read(O/'修前基线.json')
E=base['edl'];paths={Path(x['source']).name:x['source'] for x in E}
def seg(file,a,b,batch,note,old=None):
 path=paths.get(file,str(R/file));assert Path(path).exists(),path
 return dict(source=path,**{'in':a,'out':b},frames=b-a,speed=100,props={},batch=batch,note=note,old_sound_start=old)
edits=[]
def edit(a,b,rows,why):edits.append(dict(start=a,end=b,segments=rows,reason=why))
edit(3704,3758,[],'Claude说完后的持续无声喊嘴移除，直接接手部/父亲反应')
edit(4058,4130,[seg('视频制作/LibTV-H3-v001/产物/GB010-H3-v001.mp4',162,207,14,'同一年轻父亲听见恳求仍不回头',4058)],'替换换脸反打，保留闭口冷眼')
edit(5162,5211,[],'删除Kimi同一举刃动作的重复48源帧')
water=[
 ('GB018-v002.mp4',54,96,25,'回闪结束',6303),('GB018-v002.mp4',96,150,25,'千问抱稳',6399),
 ('GB018-v009-gpt-rise-2d-r1.mp4',0,102,25,'一次升空',6476),('GB019-v006-CY024A9-caster-r1.mp4',0,54,26,'抬掌起咏',6650),
 ('GB019-v002.mp4',0,120,26,'术矛发出、扇叶截击完整因果',6704),('GB019-v006-CY024A9-caster-r1.mp4',162,234,26,'聚水',6812),
 ('GB023-Metaso-H3-v001.mp4',138,174,30,'Kimi护持，手腕仍受束缚',8380),('CY024A3-水滴合并反放.mp4',0,60,27,'水珠上行',7010),
 ('GB020-1R2-v005-CY024A6-r1.mp4',0,108,28,'云海只一次',7287),('GB019-v006-CY024A9-caster-r1.mp4',108,150,26,'完整屋顶、无龙近景说术名',None),
 ('GB020-2-v002.mp4',36,134,29,'术名后俯冲破顶',7443),('GB021-v002.mp4',0,36,30,'内侧承接同一次破顶',7541),
 ('GB021-v002.mp4',153,189,30,'父亲察觉抬手',7709),('GB022-1-v002.mp4',276,324,31,'一次指令动作',8050),
 ('GB022-2-v002.mp4',0,120,32,'撞盾及散浪',8098),('GB023-Metaso-H3-v001.mp4',0,78,33,'教徒散开与退水',8218),
 ('GB023-Metaso-H3-v001.mp4',84,132,33,'浅水安全确认',8302),('GB023-Metaso-H3-v001.mp4',174,198,33,'扶护接续',8416),
 ('GB023-Metaso-H3-v001.mp4',204,288,33,'GPT落地',8446)]
water_segments=[seg(*x) for x in water]
caster=O/'施法补镜采用.json'
if caster.exists():
 for choice in read(caster)['windows']:
  s=water_segments[choice['water_index']]
  s.update(source=read(caster)['source'],**{'in':choice['in'],'out':choice['out']},speed=(choice['out']-choice['in'])/s['frames']*100,note=choice['note'])
edit(6303,8530,water_segments,'水术按起咏、敌袭、护持、云海、术名、破顶、撞盾、退水排列')
edit(10155,10293,[seg('GB029-v003.mp4',131,203,39,'掌心聚火恢复原速',10155)],'去除近一倍的慢放拖延')
edit(10368,10641,[seg('GB030-1-v003.mp4',78,108,40,'术名尾部接离指',10446),seg('GB030-1-v003.mp4',108,126,40,'空祭架确认',10476),seg('GB030-1-v003.mp4',153,228,40,'火沿木架燃起',10521),seg('GB030-1-v003.mp4',228,273,40,'Claude脱力，GPT靠近',10596)],'缩短术名后的等待，将离指和燃起紧接术名')
# Reviewed generation selections are added independently; this preparation never adopts unreviewed media.
extra=O/'补镜采用清单.json'
if extra.exists():
 for x in read(extra)['edits']:
  overlap=[e for e in edits if e['start']<x['end'] and x['start']<e['end']]
  if overlap:
   assert all(e['start']>=x['start'] and e['end']<=x['end'] for e in overlap)
   edits=[e for e in edits if e not in overlap]
  edits.append(x)
edits.sort(key=lambda e:e['start']);assert all(a['end']<=b['start'] for a,b in zip(edits,edits[1:]))
new=[];maps=[];cursor=0
def add_old(a,b):
 global cursor
 for s in E:
  lo=max(a,s['record']);hi=min(b,s['record']+s['frames'])
  if hi<=lo:continue
  z=copy.deepcopy(s);z['record']=cursor;z['frames']=hi-lo;z['in']=s['in']+round((lo-s['record'])*s['speed']/100);z['out']=z['in']+round((hi-lo)*s['speed']/100)
  z['baseline_record']=lo;new.append(z);maps.append(dict(old_start=lo,old_end=hi,new_start=cursor,new_end=cursor+hi-lo,kind='unchanged'));cursor+=hi-lo
prev=0
for e in edits:
 add_old(prev,e['start']);e['new_start']=cursor
 for i,s in enumerate(e['segments']):
  s=copy.deepcopy(s);s.update(record=cursor,name=f'B{s["batch"]:02d}_v011_{cursor}_{i}')
  new.append(s);cursor+=s['frames']
 e['new_end']=cursor;maps.append(dict(old_start=e['start'],old_end=e['end'],new_start=e['new_start'],new_end=cursor,kind='replacement'));prev=e['end']
add_old(prev,11497)
# The protected opening has native trims newer than the v008 planning file.
# Its actual snapshot, not the historical EDL, owns the untouched 0..3644 range.
native_opening={x['name']:x for tr in snap['tracks'] if tr['type']=='video' and tr['index']==1 for x in tr['items'] if x['start']<3644}
for s in new:
 if s['record']<3644:
  x=native_opening[s['name']]
  s.update(record=int(x['start']),frames=int(x['duration']),source=x['path'],**{'in':x['source_start'],'out':x['source_end']},speed=x['speed']['Percentage'],baseline_record=int(x['start']))
def remap(f):
 for m in maps:
  if m['old_start']<=f<m['old_end']:
   return m['new_start']+(f-m['old_start']) if m['kind']=='unchanged' else m['new_start']+(f-m['old_start'])*(m['new_end']-m['new_start'])/(m['old_end']-m['old_start'])
 if f==11497:return cursor
 raise ValueError(f)
w=next(e for e in edits if e['start']==6303);assert w['new_end']-w['new_start']==1262
override={'VO-CY026E-01':0,'VO-CY024A0-01':48,'VO-CY024A-01':202,'VO-CY024A2-01':376,'VO-CY024A3-01':480,'VO-CY024A4-01':540,'VO-CY024A5-01':580,'VO-CY024A5-02':650}
lines=copy.deepcopy(voice['lines'])
extra_vo=read(extra).get('voice_relative',{}) if extra.exists() else {}
for x in lines:
 old=x['record'];x['baseline_record']=old
 x['record']=w['new_start']+override[x['id']] if x['id'] in override else round(remap(old))
 if x['id'] in extra_vo:
  spec=extra_vo[x['id']];e=next(e for e in edits if e['start']==spec['edit_start']);x['record']=e['new_start']+spec['offset']
 x['end']=x['record']+x['duration_frames']
lines.sort(key=lambda x:x['record'])
assert len(lines)==54 and all(a['end']<=b['record'] for a,b in zip(lines,lines[1:])), 'Dialogue overlap'
cues=[]
for i,x in enumerate(lines):
 old=next(c for c in voice['subtitle_cues'] if c['id']==x['id']);duration=min(old['end_frame_exclusive']-old['start_frame'],max(math.ceil(x['duration_frames'])+6,24))
 end=x['record']+duration
 if i+1<len(lines):end=min(end,lines[i+1]['record'])
 if x['id']=='VO-CY003B-01':end=472
 if x['id']=='VO-CY024A5-02':end=w['new_start']+690
 cues.append(dict(index=i+1,id=x['id'],role=x['role'],start_frame=x['record'],end_frame_exclusive=end,zh=x['zh'],ja=x['ja']))
cards=[dict(start_frame=round(remap(5715)),end_frame_exclusive=round(remap(5715))+36,zh='稍早'),dict(start_frame=w['new_start']+42,end_frame_exclusive=w['new_start']+78,zh='此刻')]
allsubs=sorted(cues+cards,key=lambda x:x['start_frame'])
# Flashback labels occupy voice-free frames where possible; avoid overlapping the sole subtitle track.
cards[0].update(start_frame=round(remap(5690)),end_frame_exclusive=round(remap(5715)))
cards[1].update(start_frame=w['new_start']+80,end_frame_exclusive=w['new_start']+104)
allsubs=sorted(cues+cards,key=lambda x:x['start_frame'])
assert all(a['end_frame_exclusive']<=b['start_frame'] for a,b in zip(allsubs,allsubs[1:])), 'Subtitle overlap'
def stamp(f):
 ms=round(f*1000/24);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
(O/'白米饭-v011-中文字幕.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start_frame"])} --> {stamp(c["end_frame_exclusive"])}\n{c["zh"]}' for i,c in enumerate(allsubs))+'\n',encoding='utf-8-sig')
assert new[0]['record']==0 and new[-1]['record']+new[-1]['frames']==cursor and all(a['record']+a['frames']==b['record'] for a,b in zip(new,new[1:]))
plan=dict(timeline='v011_Church_Animation_Repair',baseline='v010_Dialogue_Subtitle_Sync',fps=24,frames=cursor,edl=new,edits=edits,maps=maps,lines=lines,subtitle_cues=allsubs,water_start=w['new_start'],water_end=w['new_end'],export_allowed=False,author_final_accepted=False)
save('修订计划.json',plan);print(json.dumps(dict(frames=cursor,seconds=cursor/24,video=len(new),voices=len(lines),subtitles=len(allsubs),water_frames=1262),ensure_ascii=True))
