"""Build an auditable four-window correction against the preserved screenshot timeline."""
from pathlib import Path
import json,copy
R=Path(__file__).resolve().parents[1];O=R/'后期/二维动漫纠偏-v005';P=R/'后期/截图定点修正-v004'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
p=read(P/'后期执行计划.json');edits=[]
for start,end,version,aid,lo,hi,batch in [(2126,2174,'v008','GB006-v008-early-inside-2d-r1',30,78,7),(4778,4838,'v009','GB014-v009-group-2d-r1',24,84,17),(6476,6650,'v009','GB018-v009-gpt-rise-2d-r1',0,174,25),(9699,9781,'v009','GB027-v009-stair-eyeline-2d-r1',0,82,37)]:
 s=dict(source=str(R/f'视频制作/Metaso-H3-{version}/产物/{aid}.mp4'),**{'in':lo,'out':hi},record=start,frames=end-start,speed=100,batch=batch,props={},name=f'B{batch:02d}_v005_2D_{start}',note='二维手绘动漫局部纠偏，实际角色表演；保留现有声音和全片时长')
 edits.append(dict(start=start,end=end,segments=[s]))
override=O/'剪辑修正增量.json'
if override.exists():
 for e in read(override)['replace_edits']:
  edits=[x for x in edits if x['start']!=e['start']]+[e]
affected=[];edl=[];replacement=[]
for s in p['edl']:
 overlaps=[e for e in edits if e['start']<s['record']+s['frames'] and e['end']>s['record']]
 if not overlaps:edl.append(copy.deepcopy(s));continue
 assert any(e['start']<=s['record'] and e['end']>=s['record']+s['frames'] for e in overlaps),'Unexpected partial replacement'
 affected.append(dict(name=s['name'],start=s['record'],end=s['record']+s['frames']))
for e in edits:
 assert sum(s['frames'] for s in e['segments'])==e['end']-e['start']
 for s in e['segments']:edl.append(s);replacement.append(s)
edl.sort(key=lambda s:s['record']);assert edl[0]['record']==0 and edl[-1]['record']+edl[-1]['frames']==11497
assert all(a['record']+a['frames']==b['record'] for a,b in zip(edl,edl[1:]))
p2=copy.deepcopy(p);p2.update(timeline='v005_2D_Anime_Fixes',edl=edl);save(O/'后期执行计划.json',p2)
data=dict(timeline=p2['timeline'],frames=p2['frames'],baseline=[dict(name=s['name'],start=s['record'],end=s['record']+s['frames'],path=s['source'].replace('\\','/')) for s in p['edl']],affected=affected,replacements=replacement)
save(O/'剪辑决定.json',dict(edits=edits,affected=affected,replacements=replacement,audio_change=False))
body=r'''
assert project.GetName()=='《白米饭》' and not project.IsRenderingInProgress()
mp=project.GetMediaPool();pm=resolve.GetProjectManager();base=project.GetCurrentTimeline()
assert base.GetName()=='v004_Screenshot_2D_Style_Rework'
assert not any(project.GetTimelineByIndex(i).GetName()==data['timeline'] for i in range(1,project.GetTimelineCount()+1)),'Existing v005: inspect before retry'
def av(t):
 return [dict(track=k,name=x.GetName(),start=x.GetStart(True),end=x.GetEnd(True),source=x.GetMediaPoolItem().GetClipProperty('File Path'),source_start=x.GetSourceStartTime(),source_end=x.GetSourceEndTime(),enabled=x.GetClipEnabled(),volume=x.GetProperties().get('AudioVolume')) for k in range(1,t.GetTrackCount('audio')+1) for x in t.GetItemListInTrack('audio',k) or []]
actual=[dict(name=x.GetName(),start=x.GetStart(),end=x.GetEnd(),path=x.GetMediaPoolItem().GetClipProperty('File Path').replace('\\','/')) for x in base.GetItemListInTrack('video',1)]
assert actual==data['baseline'],'Author changed picture timeline; reconcile first'
audio_before=av(base);assert len(audio_before)==85 and pm.SaveProject()
t=base.DuplicateTimeline(data['timeline']);assert t and project.SetCurrentTimeline(t)
f=mp.AddSubFolder(mp.GetRootFolder(),'10_2D_Anime_v005');mp.SetCurrentFolder(f)
paths=list(dict.fromkeys(s['source'] for s in data['replacements']));media=mp.ImportMedia(paths);assert len(media)==len(paths)
lookup={c.GetClipProperty('File Path').replace('\\','/'):c for c in media}
targets={(x['name'],x['start'],x['end']) for x in data['affected']}
old=[x for x in t.GetItemListInTrack('video',1) if (x.GetName(),x.GetStart(),x.GetEnd()) in targets]
assert len(old)==len(targets) and t.DeleteClips(old,False)
for s in data['replacements']:
 item=mp.AppendToTimeline([dict(mediaPoolItem=lookup[s['source'].replace('\\','/')],startFrame=s['in'],endFrame=s['in']+s['frames'],recordFrame=s['record'],trackIndex=1,mediaType=1)])[0]
 assert item.SetName(s['name'])
 if abs(s['speed']-100)>.0001:assert item.SetSpeed(dict(Percentage=s['speed'],RippleTimeline=False,PitchCorrection=False))
 if s['props']:assert item.SetProperties(dict(TransformEnabled=True,**s['props']))
 assert item.GetStart()==s['record'] and item.GetDuration()==s['frames']
 item.AddMarker(0,'Orange','二维动漫纠偏待作者核定',s['note'],s['frames'])
assert av(t)==audio_before,'Audio changed'
items=sorted(t.GetItemListInTrack('video',1),key=lambda x:x.GetStart())
assert items[0].GetStart()==0 and items[-1].GetEnd()==data['frames'] and all(a.GetEnd()==b.GetStart() for a,b in zip(items,items[1:]))
resolve.OpenPage('edit');t.SetCurrentTimecode('00:03:19:02')
result=dict(project=project.GetName(),timeline=t.GetName(),frames=t.GetEndFrame(),video_count=len(items),audio_count=len(audio_before),audio_unchanged=True,audio=av(t),audio_tracks=[dict(index=k,name=t.GetTrackName('audio',k),enabled=t.GetIsTrackEnabled('audio',k)) for k in range(1,t.GetTrackCount('audio')+1)],video=[dict(name=x.GetName(),start=x.GetStart(),end=x.GetEnd(),path=x.GetMediaPoolItem().GetClipProperty('File Path'),source_in=x.GetSourceStartFrame(),source_out=x.GetSourceEndFrame(),speed=x.GetSpeed(),enabled=x.GetClipEnabled()) for x in items],save=pm.SaveProject(),old_timeline=base.GetName(),exported=False)
'''
s='import json\ndata=json.loads('+repr(json.dumps(data,ensure_ascii=True))+')\n'+body
(O/'resolve_apply_v005.py').write_text(s.encode('ascii','backslashreplace').decode(),encoding='ascii')
print(dict(clips=len(edl),frames=11497,affected=len(affected)))
