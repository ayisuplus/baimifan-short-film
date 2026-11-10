"""Run within Resolve scripting host. Duplicate v008; install complete selected dialogue."""
import json,hashlib
from pathlib import Path
ROOT=Path('E:/projects/内容创作/故事短片/白米饭')
OUT=ROOT/'后期/对白补齐-v009'
plan=json.loads((OUT/'对白装配计划.json').read_text(encoding='utf8'))
assert len(plan['lines'])==54 and not plan['missing']
assert project.GetName()=='《白米饭》'
all_timelines=[project.GetTimelineByIndex(i) for i in range(1,project.GetTimelineCount()+1)]
baseline=next(t for t in all_timelines if t.GetName()==plan['baseline'])
present=[t for t in all_timelines if t.GetName()==plan['timeline']]
assert project.GetCurrentTimeline().GetName() in [plan['baseline'],plan['timeline']]
assert baseline.GetEndFrame()==plan['frames']
for x in plan['lines']:
 p=Path(x['file']);assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
timeline=present[0] if present else baseline.DuplicateTimeline(plan['timeline'])
assert timeline and project.SetCurrentTimeline(timeline)
assert timeline.SetTrackEnable('audio',1,False)
assert timeline.SetTrackName('audio',1,'REF_v008_Dialogue_MUTED')
roles=['GPT','Claude','小鱼','Kimi','教主','千问','教徒','Gemini','Grok']
tracks={}
for role in roles:
 found=[i for i in range(9,timeline.GetTrackCount('audio')+1) if timeline.GetTrackName('audio',i)=='VO_v009_'+role]
 if found:i=found[0]
 else:
  assert timeline.AddTrack('audio','mono')
  i=timeline.GetTrackCount('audio')
  assert timeline.SetTrackName('audio',i,'VO_v009_'+role)
 tracks[role]=i
mp=project.GetMediaPool()
folders=[f for f in mp.GetRootFolder().GetSubFolderList() if f.GetName()=='v009_Selected_Dialogue_54']
folder=folders[0] if folders else mp.AddSubFolder(mp.GetRootFolder(),'v009_Selected_Dialogue_54')
assert folder and mp.SetCurrentFolder(folder)
pool=folder.GetClipList()
if not pool:pool=mp.ImportMedia([x['file'] for x in plan['lines']])
assert len(pool)==54
by_path={str(Path(m.GetClipProperty('File Path'))):m for m in pool}
installed=[]
for x in plan['lines']:
 m=by_path[str(Path(x['file']))]
 name=x['id']+' | '+x['role']
 if m.GetName()!=name:assert m.SetName(name)
 clips=[c for c in (timeline.GetItemListInTrack('audio',tracks[x['voice_role']]) or []) if str(Path(c.GetMediaPoolItem().GetClipProperty('File Path')))==str(Path(x['file']))]
 if not clips:clips=mp.AppendToTimeline([{'mediaPoolItem':m,'mediaType':2,'trackIndex':tracks[x['voice_role']],'recordFrame':x['record']}])
 assert len(clips)==1,x['id']
 c=clips[0]
 if c.GetName()!=name:c.SetName(name)
 assert c.GetName()==name
 assert c.SetProperties({'AudioVolumeEnabled':True,'AudioVolume':x['gain_db']})
 note=x['ja']+'\n'+x['zh']+'\n'+x['direction']+'\nSource: '+x['source_kind']+'; native speed 100%; performance/lip sync pending review.'
 if not c.GetMarkers():assert c.AddMarker(0,'Cyan',x['id'],note,1,x['id'])
 actual={'id':x['id'],'track':tracks[x['voice_role']],'start':c.GetStart(True),'end':c.GetEnd(True),'duration':c.GetDuration(True),'path':m.GetClipProperty('File Path'),'gain_db':c.GetProperties()['AudioVolume']}
 assert abs(actual['start']-x['record'])<.01
 assert abs(actual['duration']-x['duration_frames'])<.1,(x['id'],actual['duration'],x['duration_frames'])
 installed.append(actual)
assert sum(len(timeline.GetItemListInTrack('audio',i) or []) for i in tracks.values())==54
assert not timeline.GetIsTrackEnabled('audio',1)
assert timeline.GetEndFrame()==plan['frames']
assert resolve.GetProjectManager().SaveProject()
timeline.SetCurrentTimecode('00:00:39:00')
resolve.OpenPage('edit')
receipt={'project':project.GetName(),'timeline':timeline.GetName(),'baseline':baseline.GetName(),'tracks':tracks,'installed':installed,'saved':True,'exported':False,'author_performance_accepted':False,'picture_revision_complete':False}
(OUT/'达芬奇装配回执.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
result={'project':project.GetName(),'timeline':timeline.GetName(),'dialogue_count':len(installed),'tracks':tracks,'saved':True,'exported':False}
