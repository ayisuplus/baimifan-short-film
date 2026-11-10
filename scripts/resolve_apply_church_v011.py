"""Install the reviewed EDL and complete native-speed dialogue in the working duplicate."""
from pathlib import Path
import json,hashlib,sys,os
import DaVinciResolveScript as dvr
R=Path('E:/projects/内容创作/故事短片/白米饭');O=R/'后期/教堂动画修订-v011'
def read(n):return json.loads((O/n).read_text(encoding='utf8'))
plan=read('修订计划.json');sound=read('声音施工.json');baseline=read('修前基线.json')
resolve=dvr.scriptapp('Resolve');pm=resolve.GetProjectManager();p=pm.GetCurrentProject();mp=p.GetMediaPool()
assert p.GetName()=='《白米饭》' and not p.IsRenderingInProgress()
t=p.GetCurrentTimeline();assert t.GetName()==plan['timeline']
base=next(p.GetTimelineByIndex(i) for i in range(1,p.GetTimelineCount()+1) if p.GetTimelineByIndex(i).GetName()==plan['baseline'])
def picture(t):return [dict(name=c.GetName(),start=c.GetStart(True),end=c.GetEnd(True),path=c.GetMediaPoolItem().GetClipProperty('File Path')) for c in t.GetItemListInTrack('video',1)]
oldpic=[{k:x[k] for k in ['name','start','end','path']} for x in next(x for x in baseline['tracks'] if x['type']=='video')['items']]
assert picture(base)==oldpic,'Protected v010 changed; reconcile first'
prior=O/'工程读回.json'
if prior.exists():
 expected=read('工程读回.json')['video'];assert picture(t)==[{k:x[k] for k in ['name','start','end','path']} for x in expected],'Working timeline changed outside this operation'
else:assert picture(t)==oldpic
assert pm.SaveProject()
def allclips(f):
 a=list(f.GetClipList() or [])
 for sub in f.GetSubFolderList() or []:a+=allclips(sub)
 return a
def key(s):return str(Path(s)).replace('\\','/').lower()
lookup={key(c.GetClipProperty('File Path')):c for c in allclips(mp.GetRootFolder()) if c.GetClipProperty('File Path')}
fs=[f for f in mp.GetRootFolder().GetSubFolderList() if f.GetName()=='v011_Church_Animation_Repair'];folder=fs[0] if fs else mp.AddSubFolder(mp.GetRootFolder(),'v011_Church_Animation_Repair');assert mp.SetCurrentFolder(folder)
paths=list(dict.fromkeys([x['source'] for x in plan['edl']]+[x['file'] for x in sound['rows']]+[x['file'] for x in plan['lines']]))
missing=[s for s in paths if key(s) not in lookup]
if missing:
 imported=mp.ImportMedia(missing);assert len(imported)==len(missing),(len(imported),len(missing));lookup.update({key(c.GetClipProperty('File Path')):c for c in imported})
# Keep the opening and all pre-church clips natively intact, including their effects.
remove=[c for c in t.GetItemListInTrack('video',1) if c.GetStart()>=3644];assert t.DeleteClips(remove,False)
for s in plan['edl']:
 if s['record']<3644:continue
 out=mp.AppendToTimeline([dict(mediaPoolItem=lookup[key(s['source'])],startFrame=s['in'],endFrame=s['in']+s['frames'],recordFrame=s['record'],trackIndex=1,mediaType=1)])
 assert len(out)==1;saved=out[0];assert saved.SetName(s['name'])
 if abs(s['speed']-100)>.0001:assert saved.SetSpeed(dict(Percentage=s['speed'],RippleTimeline=False,PitchCorrection=False))
 if s.get('props'):assert saved.SetProperties(dict(s['props'],TransformEnabled=True))
 assert saved.SetProperties(dict(RetimeAndScalingEnabled=True,RetimeProcess=resolve.RETIME_NEAREST))
 if s.get('fusion_comp'):
  f=R/'后期/导演后期修正-v001'/(s['fusion_comp']+'.comp');assert f.exists();assert saved.ImportFusionComp(str(f))
 assert saved.GetStart()==s['record'] and saved.GetDuration()==s['frames'],(s['name'],saved.GetStart(),saved.GetDuration(),s['frames'])
 if '_v011_' in s['name']:saved.AddMarker(0,'Orange','教堂修订候选',s.get('note',''),max(1,s['frames']))
for kind in ['audio','subtitle']:
 for k in range(1,t.GetTrackCount(kind)+1):
  items=t.GetItemListInTrack(kind,k) or []
  if items:assert t.DeleteClips(items,False)
assert t.SetTrackEnable('audio',1,False)
for row in sound['rows']:
 out=mp.AppendToTimeline([dict(mediaPoolItem=lookup[key(row['file'])],recordFrame=row['record'],trackIndex=row['track'],mediaType=2)]);assert len(out)==1;c=out[0];c.SetName(row['name']);assert c.SetProperties(dict(AudioVolumeEnabled=True,AudioVolume=row['volume']))
roles=['GPT','Claude','小鱼','Kimi','教主','千问','教徒','Gemini','Grok']
for x in plan['lines']:
 assert hashlib.sha256(Path(x['file']).read_bytes()).hexdigest()==x['sha256']
 track=9+roles.index(x['voice_role']);out=mp.AppendToTimeline([dict(mediaPoolItem=lookup[key(x['file'])],recordFrame=x['record'],trackIndex=track,mediaType=2)]);assert len(out)==1;c=out[0]
 c.SetName(x['id']+' | '+x['role']);assert c.SetProperties(dict(AudioVolumeEnabled=True,AudioVolume=x['gain_db']));assert abs(c.GetDuration(True)-x['duration_frames'])<.1
 c.AddMarker(0,'Cyan',x['id'],x['ja']+'\n'+x['zh'],1)
for f in list((t.GetMarkers() or {}).keys()):t.DeleteMarkerAtFrame(f)
for e in plan['edits']:
 if e['new_end']>e['new_start']:t.AddMarker(e['new_start'],'Orange',e['reason'],e['reason'],e['new_end']-e['new_start'])
# SRT is imported to the pool here; actual subtitle installation is a separate native UI operation.
subs=mp.ImportMedia([str(O/'白米饭-v011-中文字幕.srt')]);assert subs
v=picture(t);assert v[0]['start']==0 and v[-1]['end']==plan['frames'] and all(a['end']==b['start'] for a,b in zip(v,v[1:]))
assert picture(base)==oldpic
assert t.GetEndFrame()==plan['frames'],(t.GetEndFrame(),plan['frames'])
a=[dict(track=k,name=c.GetName(),start=c.GetStart(True),end=c.GetEnd(True),path=c.GetMediaPoolItem().GetClipProperty('File Path'),volume=c.GetProperties().get('AudioVolume')) for k in range(1,t.GetTrackCount('audio')+1) for c in t.GetItemListInTrack('audio',k) or []]
assert len([x for x in a if x['track']>=9])==54
result=dict(project=p.GetName(),timeline=t.GetName(),frames=t.GetEndFrame(),video=v,audio=a,subtitle_count=sum(len(t.GetItemListInTrack('subtitle',k) or []) for k in range(1,t.GetTrackCount('subtitle')+1)),subtitles_pending_ui=True,baseline_preserved=True,plan_sha256=hashlib.sha256((O/'修订计划.json').read_bytes()).hexdigest(),saved=pm.SaveProject(),exported=False)
(O/'工程读回.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');resolve.OpenPage('edit');t.SetCurrentTimecode('00:02:30:00')
print(json.dumps({k:result[k] for k in ['timeline','frames','subtitle_count','subtitles_pending_ui','baseline_preserved','saved','exported']},ensure_ascii=True))
sys.stdout.flush()
os._exit(0)
