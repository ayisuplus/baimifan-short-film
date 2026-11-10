"""Preserve a verified native baseline and create the repair working timeline."""
import json
from pathlib import Path
import DaVinciResolveScript as dvr
R=Path('E:/projects/内容创作/故事短片/白米饭');O=R/'后期/教堂动画修订-v011';O.mkdir(exist_ok=True)
resolve=dvr.scriptapp('Resolve');pm=resolve.GetProjectManager();p=pm.GetCurrentProject()
assert p.GetName()=='《白米饭》' and not p.IsRenderingInProgress()
ts=[p.GetTimelineByIndex(i) for i in range(1,p.GetTimelineCount()+1)]
base=next(t for t in ts if t.GetName()=='v010_Dialogue_Subtitle_Sync')
def snapshot(t):
 tracks=[]
 for typ in ['video','audio','subtitle']:
  for k in range(1,t.GetTrackCount(typ)+1):
   items=[]
   for c in t.GetItemListInTrack(typ,k) or []:
    m=c.GetMediaPoolItem()
    x=dict(name=c.GetName(),start=c.GetStart(True),end=c.GetEnd(True),duration=c.GetDuration(True),path=m.GetClipProperty('File Path') if m else None,properties=c.GetProperties(),enabled=c.GetClipEnabled())
    if typ!='subtitle':x.update(source_start=c.GetSourceStartFrame(),source_end=c.GetSourceEndFrame(),speed=c.GetSpeed())
    items.append(x)
   tracks.append(dict(type=typ,index=k,name=t.GetTrackName(typ,k),enabled=t.GetIsTrackEnabled(typ,k),items=items))
 return dict(project=p.GetName(),timeline=t.GetName(),start=t.GetStartFrame(),end=t.GetEndFrame(),tracks=tracks)
before=snapshot(base);old=json.loads((R/'后期/对白字幕同步-v010/v010-工程读回.json').read_text(encoding='utf8'))
for a,b in zip(before['tracks'],old['tracks']):
 assert a['type']==b['type'] and len(a['items'])==len(b['items'])
 for x,y in zip(a['items'],b['items']):
  assert all(x[k]==y[k] for k in ['name','start','end','path']),('Baseline changed',x['name'])
assert pm.SaveProject()
target='v011_Church_Animation_Repair';existing=[t for t in ts if t.GetName()==target]
assert not existing,'Output exists; inspect before any repeat'
t=base.DuplicateTimeline(target);assert t and p.SetCurrentTimeline(t)
(O/'修前基线.json').write_text(json.dumps(before,ensure_ascii=False,indent=2),encoding='utf8')
assert pm.SaveProject()
print(json.dumps(dict(timeline=t.GetName(),frames=t.GetEndFrame(),baseline_preserved=base.GetName(),saved=True,exported=False),ensure_ascii=True))
