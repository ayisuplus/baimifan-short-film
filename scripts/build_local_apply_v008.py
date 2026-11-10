"""Build an idempotence-guarded native duplicate-and-replace operation."""
from pathlib import Path
import json,copy
R=Path(__file__).resolve().parents[1];O=R/'后期/局部收口-v008'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
B=read(O/'修前实际状态.json');P=read(R/'后期/二维动漫纠偏-v005/后期执行计划.json');p=copy.deepcopy(P);p['timeline']='v008_Local_Continuity_Fixes'
changes=[]
for e in read(O/'前段/最小剪辑清单.json')['edits']:
 changes.append(dict(start=e['current_timeline_start'],end=e['current_timeline_end'],source=e['new_source'],sin=e['source_in'],speed=e['speed_percent'],props=e['props'],reason=e['reason']))
changes.append(dict(start=4778,end=4838,source=str(R/'视频制作/Metaso-H3-v010/产物/GB014-v010-original-shot-only-r1.mp4'),sin=24,speed=100,props={},reason='只取九人/月夜/原武器正确窗口，保留教主反应'))
bridge=read(O/'后段/最小剪辑建议.json')['posterior_edit']
changes.append(dict(start=9699,end=9781,source=str(R/bridge['path']),sin=0,speed=48/82*100,props=bridge['props'],reason='冷蓝湿地听者反应承接Claude画外半句，避免干石阶空间跳变'))
for start,end,sin,props in [(9632,9666,12,{}),(9666,9699,46,dict(ZoomX=1344/760,ZoomY=1344/760,Pan=292*1344/760,Tilt=-157*1344/760))]:
 changes.append(dict(start=start,end=end,source=str(R/'视频制作/Metaso-H3-v012/产物/GB027-v012-support-close-r1.mp4'),sin=sin,speed=100,props=props,reason='原造型扶稳；对白结束转Claude听者反应特写，连续源动作，不保留GPT无声张嘴'))
for start,end,sin in [(10641,10689,12),(10689,10708,60),(10708,10732,79),(10732,10761,103),(10761,10833,132)]:
 props=dict(ZoomX=2.1,ZoomY=2.1,Pan=-604.8,Tilt=81.9) if start==10708 else {}
 reason='同一连续动作：托背托膝、抱起站稳；原声与离场远景不动'
 if props:reason='行こう保留画外原声，剪托膝/手部细节覆盖闭嘴说话，接回连续承重动作'
 changes.append(dict(start=start,end=end,source=str(R/'视频制作/Metaso-H3-v012/产物/GB030-v012-carry-design-r1.mp4'),sin=sin,speed=100,props=props,reason=reason))
changes.sort(key=lambda e:e['start']);assert all(a['end']<=b['start'] for a,b in zip(changes,changes[1:]))
affected=[c for c in B['video'] if any(c['start']<e['end'] and c['end']>e['start'] for e in changes)]
affected_names={c['name'] for c in affected}
# Split affected originals once at all new boundaries; preserve uncovered tails.
repl=[]
for s in P['edl']:
 if s['name'] not in affected_names:continue
 a=s['record'];b=a+s['frames'];cuts=sorted({a,b}|{v for e in changes for v in [e['start'],e['end']] if a<v<b})
 for lo,hi in zip(cuts,cuts[1:]):
  if any(e['start']<=lo and hi<=e['end'] for e in changes):continue
  q=copy.deepcopy(s);q.update(record=lo,frames=hi-lo,name=s['name']+'_v008_keep',note='原镜头未受影响部分保持')
  q['props']=copy.deepcopy(next(c['props'] for c in B['video'] if c['name']==s['name']))
  q['in']=s['in']+round((lo-a)*s['speed']/100);q['out']=q['in']+round((hi-lo)*s['speed']/100);repl.append(q)
for e in changes:
 b=next(b['batch'] for b in P['batches'] if b['start']<=e['start']<b['start']+b['frames'])
 repl.append(dict(source=e['source'],record=e['start'],frames=e['end']-e['start'],in_=e['sin'],out=e['sin']+round((e['end']-e['start'])*e['speed']/100),speed=e['speed'],props=e['props'],name=f'B{b:02d}_v008_{e["start"]}',batch=b,note=e['reason']))
for s in repl:
 if 'in_' in s:s['in']=s.pop('in_')
 assert Path(s['source']).exists()
p['edl']=sorted([s for s in P['edl'] if s['name'] not in affected_names]+repl,key=lambda s:s['record'])
assert p['edl'][0]['record']==0 and p['edl'][-1]['record']+p['edl'][-1]['frames']==11497
assert all(a['record']+a['frames']==b['record'] for a,b in zip(p['edl'],p['edl'][1:]))
p['local_repair_notes']='仅通过审核的局部候选；画面629帧涉及剪辑/替换，未整批重做；口型/连续听审仍待作者核验'
save(O/'后期执行计划.json',p)
data=dict(timeline=p['timeline'],baseline=B,affected=affected,replacements=sorted(repl,key=lambda s:s['record']),audio=read(O/'声音施工增量.json')['replacements'],gains=read(O/'对白增益修正.json')['adjustments'],changes=changes)
save(O/'剪辑施工增量.json',{k:v for k,v in data.items() if k!='baseline'})
body=r'''
assert project.GetName()=='《白米饭》' and not project.IsRenderingInProgress()
base=project.GetCurrentTimeline();assert base.GetName()==data['baseline']['timeline']
assert not any(project.GetTimelineByIndex(i).GetName()==data['timeline'] for i in range(1,project.GetTimelineCount()+1)),'Existing output timeline: inspect, do not repeat'
def picture(t):
 return [dict(name=x.GetName(),start=x.GetStart(),end=x.GetEnd(),path=x.GetMediaPoolItem().GetClipProperty('File Path')) for x in (t.GetItemListInTrack('video',1) or [])]
def audio(t):
 return [dict(track=k,name=x.GetName(),start=x.GetStart(True),end=x.GetEnd(True),path=x.GetMediaPoolItem().GetClipProperty('File Path'),source_in=x.GetSourceStartTime(),source_out=x.GetSourceEndTime(),volume=x.GetProperties().get('AudioVolume'),enabled=x.GetClipEnabled()) for k in range(1,t.GetTrackCount('audio')+1) for x in (t.GetItemListInTrack('audio',k) or [])]
assert picture(base)==[{k:c[k] for k in ['name','start','end','path']} for c in data['baseline']['video']],'Baseline changed: reconcile author edits first'
pm=resolve.GetProjectManager();mp=project.GetMediaPool();ab=audio(base);assert pm.SaveProject()
t=base.DuplicateTimeline(data['timeline']);assert t and project.SetCurrentTimeline(t)
def clips(f):
 out=list(f.GetClipList() or [])
 for sub in f.GetSubFolderList() or []:out+=clips(sub)
 return out
lookup={c.GetClipProperty('File Path').replace('\\','/'):c for c in clips(mp.GetRootFolder()) if c.GetClipProperty('File Path')}
folder=mp.AddSubFolder(mp.GetRootFolder(),'11_Local_Continuity_v008');assert folder;mp.SetCurrentFolder(folder)
paths=list(dict.fromkeys([s['source'] for s in data['replacements']]+[s['path'] for s in data['audio']]))
missing=[p for p in paths if p.replace('\\','/') not in lookup]
if missing:
 imported=mp.ImportMedia(missing);assert len(imported)==len(missing)
 lookup.update({c.GetClipProperty('File Path').replace('\\','/'):c for c in imported})
targets={(x['name'],x['start'],x['end']) for x in data['affected']}
old=[x for x in t.GetItemListInTrack('video',1) if (x.GetName(),x.GetStart(),x.GetEnd()) in targets]
assert len(old)==len(targets) and t.DeleteClips(old,False)
for s in data['replacements']:
 c=lookup[s['source'].replace('\\','/')]
 it=mp.AppendToTimeline([dict(mediaPoolItem=c,startFrame=s['in'],endFrame=s['in']+s['frames'],recordFrame=s['record'],trackIndex=1,mediaType=1)])[0]
 assert it.SetName(s['name'])
 if abs(s['speed']-100)>.0001:assert it.SetSpeed(dict(Percentage=s['speed'],RippleTimeline=False,PitchCorrection=False))
 if s['props']:assert it.SetProperties(dict(s['props'],TransformEnabled=True))
 assert it.SetProperties(dict(RetimeAndScalingEnabled=True,RetimeProcess=resolve.RETIME_NEAREST))
 assert it.GetStart()==s['record'] and it.GetDuration()==s['frames'],(s['name'],it.GetStart(),it.GetDuration())
 it.AddMarker(0,'Orange','局部修复待作者核定',s['note'],s['frames'])
assert audio(t)==ab,'Picture operation changed sound'
for s in data['audio']:
 old=[x for x in t.GetItemListInTrack('audio',s['track']) if x.GetName()==s['name']];assert len(old)==1
 assert t.DeleteClips(old,False)
 it=mp.AppendToTimeline([dict(mediaPoolItem=lookup[s['path'].replace('\\','/')],startFrame=0,endFrame=s['frames'],recordFrame=s['record'],trackIndex=s['track'],mediaType=2)])[0]
 assert it.SetName(s['name']);assert it.SetProperties(dict(AudioVolumeEnabled=True,AudioVolume=s['volume']))
 assert it.GetStart()==s['record'] and it.GetDuration()==s['frames']
for g in data['gains']:
 it=next(x for x in t.GetItemListInTrack('audio',1) if x.GetName()==g['name'])
 assert it.GetStart()==g['start'] and it.GetEnd()==g['end'] and it.GetMediaPoolItem().GetClipProperty('File Path')==g['path']
 assert it.SetProperties(dict(AudioVolumeEnabled=True,AudioVolume=g['new_volume']))
after=audio(t)
# Every voice source/time survives, only explicitly listed gain values differ.
key=lambda x:(x['track'],x['start'],x['name'])
gains={g['name']:g['new_volume'] for g in data['gains']}
expected=[dict(x,volume=gains.get(x['name'],x['volume'])) for x in ab if x['track']==1]
assert sorted([x for x in after if x['track']==1],key=key)==sorted(expected,key=key)
allowed={(s['track'],s['name']) for s in data['audio']}|{(1,g['name']) for g in data['gains']}
assert sorted([x for x in after if (x['track'],x['name']) not in allowed],key=key)==sorted([x for x in ab if (x['track'],x['name']) not in allowed],key=key)
v=sorted(t.GetItemListInTrack('video',1),key=lambda x:x.GetStart())
assert v[0].GetStart()==0 and v[-1].GetEnd()==11497 and all(a.GetEnd()==b.GetStart() for a,b in zip(v,v[1:]))
assert t.GetEndFrame()==11497 and len(after)==85
resolve.OpenPage('edit');t.SetCurrentTimecode('00:02:39:02')
result=dict(project=project.GetName(),timeline=t.GetName(),frames=t.GetEndFrame(),video_count=len(v),audio_count=len(after),video=[dict(name=x.GetName(),start=x.GetStart(),end=x.GetEnd(),path=x.GetMediaPoolItem().GetClipProperty('File Path'),source_in=x.GetSourceStartFrame(),source_out=x.GetSourceEndFrame(),speed=x.GetSpeed(),props=x.GetProperties()) for x in v],audio=after,save=pm.SaveProject(),exported=False,old_timeline_preserved=base.GetName())
'''
script='import json\ndata=json.loads('+repr(json.dumps(data,ensure_ascii=True))+')\n'+body
(O/'resolve_apply_v008.py').write_text(script.encode('ascii','backslashreplace').decode(),encoding='ascii')
print('Prepared',len(p['edl']),'video segments; only',len(changes),'local changes; no Resolve mutation yet')
