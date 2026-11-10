"""Read-only capture before the author's shot-by-shot corrections."""
from pathlib import Path
import json,sys,os
import DaVinciResolveScript as dvr
R=Path('E:/projects/内容创作/故事短片/白米饭');O=R/'后期/逐镜修订-v012/第三批'
resolve=dvr.scriptapp('Resolve');p=resolve.GetProjectManager().GetCurrentProject();t=p.GetCurrentTimeline()
assert p.GetName()=='《白米饭》'
tracks=[]
for kind in ['video','audio','subtitle']:
 for k in range(1,t.GetTrackCount(kind)+1):
  items=[]
  for c in t.GetItemListInTrack(kind,k) or []:
   m=c.GetMediaPoolItem();x=dict(name=c.GetName(),start=c.GetStart(True),end=c.GetEnd(True),path=m.GetClipProperty('File Path') if m else None,properties=c.GetProperties(),enabled=c.GetClipEnabled())
   if kind!='subtitle':x.update(source_start=c.GetSourceStartFrame(),source_end=c.GetSourceEndFrame(),speed=c.GetSpeed())
   items.append(x)
  tracks.append(dict(type=kind,index=k,name=t.GetTrackName(kind,k),enabled=t.GetIsTrackEnabled(kind,k),items=items))
result=dict(project=p.GetName(),timeline=t.GetName(),start=t.GetStartFrame(),end=t.GetEndFrame(),tracks=tracks)
out=O/'修前实际工程.json';assert not out.exists(),'Capture exists; do not replace preservation evidence'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(timeline=t.GetName(),frames=t.GetEndFrame(),batch3=[{k:c[k] for k in ['name','start','end','path','source_start','source_end']} for tr in tracks if tr['type']=='video' for c in tr['items'] if c['name'].startswith('B03')]),ensure_ascii=True));sys.stdout.flush();os._exit(0)
