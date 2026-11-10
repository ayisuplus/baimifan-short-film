from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'后期/截图定点修正-v004'
def read(p):return json.loads(p.read_text(encoding='utf8'))
p=read(O/'后期执行计划.json');d=read(O/'剪辑决定.json');base=read(R/'后期/导演重构-v003/后期执行计划.json')
data=dict(plan={k:p[k] for k in ['timeline','frames']},decisions={**d,'edits':[{k:e[k] for k in ['start','end','reason']} for e in d['edits']]},baseline=[dict(name=s['name'],start=s['record'],end=s['record']+s['frames'],path=s['source']) for s in base['edl']],fusion_base=str(R/'后期/导演后期修正-v001'),foley_path=str(O/'声音/Foley-v004-stem.wav'))
body=r'''
assert project.GetName()=='《白米饭》' and not project.IsRenderingInProgress()
mp=project.GetMediaPool();pm=resolve.GetProjectManager();base=project.GetCurrentTimeline()
assert base.GetName()=='v003_Dramatic_Reconstruction'
assert not any(project.GetTimelineByIndex(i).GetName().startswith('v004_Screenshot') for i in range(1,project.GetTimelineCount()+1)),'Read existing v004 before retry'
def av(t):
 return [dict(track=k,name=x.GetName(),start=x.GetStart(True),end=x.GetEnd(True),source=x.GetMediaPoolItem().GetClipProperty('File Path'),source_start=x.GetSourceStartTime(),source_end=x.GetSourceEndTime(),enabled=x.GetClipEnabled(),volume=x.GetProperties().get('AudioVolume')) for k in range(1,t.GetTrackCount('audio')+1) for x in t.GetItemListInTrack('audio',k) or []]
actual=[dict(name=x.GetName(),start=x.GetStart(),end=x.GetEnd(),path=x.GetMediaPoolItem().GetClipProperty('File Path')) for x in base.GetItemListInTrack('video',1)]
assert actual==data['baseline'],'Author changed baseline; reconcile before modifying'
audio_before=av(base);assert pm.SaveProject()
t=base.DuplicateTimeline('v004_Screenshot_Targeted_Fixes_Work');assert t;assert project.SetCurrentTimeline(t)
def allclips(f):
 a=list(f.GetClipList() or [])
 for s in f.GetSubFolderList() or []:a+=allclips(s)
 return a
lookup={c.GetClipProperty('File Path').replace('\\','/'):c for c in allclips(mp.GetRootFolder()) if c.GetClipProperty('File Path')}
f=mp.AddSubFolder(mp.GetRootFolder(),'09_Screenshot_Targeted_v004');mp.SetCurrentFolder(f)
paths=list(dict.fromkeys(x['source'].replace('\\','/') for x in data['decisions']['replacement_clips']));missing=[x for x in paths if x not in lookup]
if missing:
 imported=mp.ImportMedia(missing);assert len(imported)==len(missing)
 lookup.update({c.GetClipProperty('File Path').replace('\\','/'):c for c in imported})
targets={(s['name'],s['start'],s['end']) for s in data['decisions']['affected_originals']}
deleted=[x for x in t.GetItemListInTrack('video',1) if (x.GetName(),x.GetStart(),x.GetEnd()) in targets]
assert len(deleted)==len(targets);assert t.DeleteClips(deleted,False)
receipt=[]
for s in data['decisions']['replacement_clips']:
 item=mp.AppendToTimeline([dict(mediaPoolItem=lookup[s['source'].replace('\\','/')],startFrame=s['in'],endFrame=s['in']+s['frames'],recordFrame=s['record'],trackIndex=1,mediaType=1)])[0]
 item.SetName(s['name'])
 if abs(s['speed']-100)>.0001:assert item.SetSpeed(dict(Percentage=s['speed'],RippleTimeline=False,PitchCorrection=False))
 if s['props']:assert item.SetProperties(dict(TransformEnabled=True,**s['props']))
 item.SetProperties(dict(RetimeAndScalingEnabled=True,RetimeProcess=resolve.RETIME_OPTICAL_FLOW if s['speed']<95 else resolve.RETIME_NEAREST,MotionEstimation=resolve.MOTION_EST_ENHANCED_BETTER))
 assert item.GetStart()==s['record'] and item.GetDuration()==s['frames'],(s['name'],item.GetStart(),item.GetDuration(),s['frames'])
 if s.get('fusion_comp'):assert item.ImportFusionComp(data['fusion_base']+'/'+s['fusion_comp']+'.comp')
 receipt.append(dict(name=item.GetName(),start=item.GetStart(),end=item.GetEnd(),source_start=item.GetSourceStartFrame(),source_end=item.GetSourceEndFrame(),speed=item.GetSpeed()))
assert av(t)==audio_before,'Picture edits changed audio unexpectedly'
# Shift only the small child's decision line by seven frames, preserving the source and gain.
v=next(x for x in t.GetItemListInTrack('audio',1) if x.GetName()=='VO-CY009-01');c=v.GetMediaPoolItem();props=v.GetProperties();oldstart=v.GetStart();oldend=v.GetEnd();assert oldstart==1640
assert t.DeleteClips([v],False)
v=mp.AppendToTimeline([dict(mediaPoolItem=c,recordFrame=1647,trackIndex=1,mediaType=2)])[0];v.SetName('VO-CY009-01');assert v.SetProperties(dict(AudioVolumeEnabled=True,AudioVolume=props['AudioVolume']))
assert v.GetStart()==1647 and v.GetEnd()-v.GetStart()==oldend-oldstart
after=av(t)
expected=[dict(x,start=x['start']+7,end=x['end']+7) if x['track']==1 and x['name']=='VO-CY009-01' else x for x in audio_before]
key=lambda x:(x['track'],x['start'],x['name']);assert sorted(after,key=key)==sorted(expected,key=key)
oldfoley=t.GetItemListInTrack('audio',6);assert len(oldfoley)==1 and oldfoley[0].GetName()=='Foley'
c=mp.ImportMedia([data['foley_path']])[0];assert t.DeleteClips(oldfoley,False)
nf=mp.AppendToTimeline([dict(mediaPoolItem=c,recordFrame=0,trackIndex=6,mediaType=2)])[0];nf.SetName('Foley');assert nf.SetProperties(dict(AudioVolumeEnabled=True,AudioVolume=-3))
after=av(t);assert sorted([x for x in after if x['track']!=6],key=key)==sorted([x for x in expected if x['track']!=6],key=key)
items=sorted(t.GetItemListInTrack('video',1),key=lambda x:x.GetStart());assert items[0].GetStart()==0 and items[-1].GetEnd()==data['plan']['frames']
assert all(a.GetEnd()==b.GetStart() for a,b in zip(items,items[1:]))
assert t.GetEndFrame()==data['plan']['frames'];assert t.SetName(data['plan']['timeline'])
for e in data['decisions']['edits']:t.AddMarker(e['start'],'Orange','截图修正待作者核定',e['reason'],e['end']-e['start'])
resolve.OpenPage('edit');t.SetCurrentTimecode('00:00:53:10')
result=dict(timeline=t.GetName(),frames=t.GetEndFrame(),video_count=len(items),replacements=receipt,audio=after,tracks=[dict(index=k,name=t.GetTrackName('audio',k),enabled=t.GetIsTrackEnabled('audio',k)) for k in range(1,t.GetTrackCount('audio')+1)],save=pm.SaveProject(),exported=False)
'''
s='import json\ndata=json.loads('+repr(json.dumps(data,ensure_ascii=True))+')\n'+body
(O/'resolve_apply_v004.py').write_text(s.encode('ascii','backslashreplace').decode(),encoding='ascii')
print('Prepared native copy-and-replace script; no exports')
