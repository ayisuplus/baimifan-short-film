"""Create a new picture-only timeline from reviewed, CPU-conformed media.

Run with the installed ResolvePython runtime. Never modifies an old timeline.
All manifest records require review=pass, source window and exact frame count.
"""
import argparse,json,os,sys
from pathlib import Path
import DaVinciResolveScript as dvr

P=Path(__file__).resolve().parent
def save(path,value):
 path.write_text(json.dumps(value,ensure_ascii=False,indent=2),'utf8')
def snapshot(t):
 tracks=[]
 for kind in ['video','audio','subtitle']:
  for n in range(1,t.GetTrackCount(kind)+1):
   items=[]
   for c in t.GetItemListInTrack(kind,n) or []:
    m=c.GetMediaPoolItem()
    item=dict(name=c.GetName(),start=c.GetStart(),end=c.GetEnd(),enabled=c.GetClipEnabled(),source=m.GetClipProperty('File Path') if m else None)
    if kind!='subtitle':item.update(source_in=c.GetSourceStartFrame(),source_out=c.GetSourceEndFrame(),speed=c.GetSpeed())
    items.append(item)
   tracks.append(dict(kind=kind,index=n,name=t.GetTrackName(kind,n),items=items))
 return dict(name=t.GetName(),id=t.GetUniqueId(),start=t.GetStartFrame(),end=t.GetEndFrame(),tracks=tracks)

a=argparse.ArgumentParser();a.add_argument('mode',choices=['build','verify']);a.add_argument('manifest');a.add_argument('--name',default='v034_2D_Continuity_Edit');args=a.parse_args()
plan=json.loads(Path(args.manifest).read_text('utf8'))
assert plan and all(x.get('review')=='pass' for x in plan), 'Manifest contains unreviewed material'
position=0
for x in plan:
 assert Path(x['source']).is_file(),x['source']
 assert x['start']==position and x['frames']>0 and x['source_in']>=0,x
 assert x['source_out_exclusive']-x['source_in']==x['frames'],x
 position+=x['frames']
r=dvr.scriptapp('Resolve');assert r
pm=r.GetProjectManager();p=pm.GetCurrentProject();assert p and p.GetName()=='《白米饭》' and not p.IsRenderingInProgress()
mp=p.GetMediaPool()
def timelines():return [p.GetTimelineByIndex(i) for i in range(1,p.GetTimelineCount()+1)]
out=P/'resolve';out.mkdir(exist_ok=True)
checkpoint=out/(args.name+'-before.json')
if args.mode=='build':
 assert not checkpoint.exists(),'Checkpoint already exists; inspect instead of overwriting'
 assert all(t.GetName()!=args.name for t in timelines())
 before={t.GetUniqueId():snapshot(t) for t in timelines()}
 save(checkpoint,before)
 assert pm.SaveProject()
 assert pm.ExportProject(p.GetName(),str(out/(args.name+'-before.drp')),True)
 folder=mp.AddSubFolder(mp.GetRootFolder(),args.name);assert folder and mp.SetCurrentFolder(folder)
 paths=list(dict.fromkeys(x['source'] for x in plan))
 clips=mp.ImportMedia(paths);assert clips and len(clips)==len(paths)
 lookup={Path(c.GetClipProperty('File Path')).resolve():c for c in clips}
 t=mp.CreateEmptyTimeline(args.name);assert t and p.SetCurrentTimeline(t)
 assert t.SetStartTimecode('00:00:00:00')
 settings=t.GetSettings();assert float(settings['timelineFrameRate'])==24 and settings['timelineResolutionWidth']=='1344' and settings['timelineResolutionHeight']=='768'
 assert t.SetTrackName('video',1,'二维画风与动作修订 v034')
 for x in plan:
  info=dict(mediaPoolItem=lookup[Path(x['source']).resolve()],startFrame=x['source_in'],endFrame=x['source_out_exclusive'],recordFrame=x['start'],trackIndex=1,mediaType=1)
  made=mp.AppendToTimeline([info]);assert made and len(made)==1
  c=made[0]
  if c.GetDuration()==x['frames']+1:
   assert t.DeleteClips([c],False);info['endFrame']-=1
   made=mp.AppendToTimeline([info]);assert made and len(made)==1;c=made[0]
  assert c.GetDuration()==x['frames'] and c.GetStart()==x['start'],x['name']
  assert c.SetName(x['name'])
  if x.get('chapter_start'):
   assert t.AddMarker(x['start'],'Blue',x['chapter_start'],x.get('note',''),1)
else:
 before=json.loads(checkpoint.read_text('utf8'))
 t=next(t for t in timelines() if t.GetName()==args.name)
 assert p.SetCurrentTimeline(t)

items=t.GetItemListInTrack('video',1);assert len(items)==len(plan) and t.GetEndFrame()==position
for c,x in zip(items,plan):
 assert c.GetName()==x['name'] and c.GetStart()==x['start'] and c.GetDuration()==x['frames'],x['name']
 assert c.GetSourceStartFrame()==x['source_in'],x['name']
 assert Path(c.GetMediaPoolItem().GetClipProperty('File Path')).resolve()==Path(x['source']).resolve(),x['name']
 assert c.GetClipEnabled(),x['name']
assert all(not t.GetItemListInTrack(k,n) for k in ['audio','subtitle'] for n in range(1,t.GetTrackCount(k)+1))
old_checks={v.GetName():snapshot(v)==before[v.GetUniqueId()] for v in timelines() if v.GetUniqueId() in before}
assert all(old_checks.values()),old_checks
assert pm.SaveProject()
save(out/(args.name+'-readback.json'),snapshot(t))
save(out/(args.name+'-verification.json'),dict(project=p.GetName(),timeline=t.GetName(),id=t.GetUniqueId(),clips=len(items),frames=position,fps=24,picture_only=True,old_timelines=old_checks,saved=True,mode=args.mode))
print(json.dumps(dict(timeline=t.GetName(),clips=len(items),frames=position,saved=True,old_preserved=len(old_checks)),ensure_ascii=False),flush=True)
sys.stdout.flush();os._exit(0)
