"""Replace only three equal-duration picture windows; audio and subtitles stay intact."""
from pathlib import Path
import json,sys,os
import DaVinciResolveScript as dvr
R=Path('E:/projects/内容创作/故事短片/白米饭');O=R/'后期/教堂动画修订-v011'
plan=json.loads((O/'修订计划.json').read_text(encoding='utf8'))
resolve=dvr.scriptapp('Resolve');pm=resolve.GetProjectManager();p=pm.GetCurrentProject();t=p.GetCurrentTimeline();mp=p.GetMediaPool()
assert p.GetName()=='《白米饭》' and t.GetName()==plan['timeline'] and not p.IsRenderingInProgress()
def preserved():
 return [(kind,k,c.GetName(),c.GetStart(True),c.GetEnd(True),c.GetProperties()) for kind in ['audio','subtitle'] for k in range(1,t.GetTrackCount(kind)+1) for c in t.GetItemListInTrack(kind,k) or []]
before=preserved();assert sum(x[0]=='subtitle' for x in before)==56
assert pm.SaveProject()
rows=[x for x in plan['edl'] if 'CY024A-v014-caster-2d-sync-r1.mp4' in x['source']];assert len(rows)==3
source=mp.ImportMedia([rows[0]['source']]);assert len(source)==1
changes=[]
for s in rows:
 c=next(c for c in t.GetItemListInTrack('video',1) if c.GetStart()==s['record'])
 assert c.GetDuration()==s['frames']
 old=dict(name=c.GetName(),source=c.GetMediaPoolItem().GetClipProperty('File Path'))
 assert 'GB019-v006-CY024A9-caster-r1' in old['source'],'Already replaced or external change'
 assert t.DeleteClips([c],False)
 clips=mp.AppendToTimeline([dict(mediaPoolItem=source[0],startFrame=s['in'],endFrame=s['in']+s['frames'],recordFrame=s['record'],trackIndex=1,mediaType=1)]);assert len(clips)==1;c=clips[0]
 assert c.SetName(s['name'])
 if s['speed']!=100:assert c.SetSpeed(dict(Percentage=s['speed'],RippleTimeline=False,PitchCorrection=False))
 assert c.SetProperties(dict(RetimeAndScalingEnabled=True,RetimeProcess=resolve.RETIME_NEAREST))
 assert c.GetStart()==s['record'] and c.GetDuration()==s['frames']
 c.AddMarker(0,'Orange','二维施法补镜',s['note'],s['frames'])
 changes.append(dict(record=s['record'],frames=s['frames'],old=old,new_source=s['source'],source_start=c.GetSourceStartFrame(),source_end=c.GetSourceEndFrame(),speed=c.GetSpeed()))
assert preserved()==before and t.GetEndFrame()==plan['frames']
result=dict(changes=changes,audio_and_subtitles_unchanged=True,saved=pm.SaveProject(),exported=False)
(O/'施法补镜写入.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=True));sys.stdout.flush();os._exit(0)
