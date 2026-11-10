"""Read-only check that migration left the source Resolve timeline unchanged."""
from pathlib import Path
import json,os
import DaVinciResolveScript as dvr
O=Path(__file__).resolve().parent
s=json.loads((O/'Resolve-current.json').read_text(encoding='utf8'))
r=dvr.scriptapp('Resolve');assert r
p=r.GetProjectManager().GetCurrentProject();assert p.GetName()==s['project']
t=p.GetCurrentTimeline();assert t.GetUniqueId()==s['id'] and t.GetSettings()==s['settings']
assert t.GetStartFrame()==s['start'] and t.GetEndFrame()==s['end']
for track in s['tracks']:
 items=t.GetItemListInTrack(track['kind'],track['index']) or []
 assert len(items)==len(track['items'])
 for c,x in zip(items,track['items']):
  assert c.GetName()==x['name'] and c.GetStart()==x['start'] and c.GetEnd()==x['end']
  assert c.GetSourceStartFrame()==x['source_in'] and c.GetSpeed()==x['speed'] and c.GetProperties()==x['properties']
  assert c.GetMediaPoolItem().GetClipProperty('File Path')==x['source']
assert [p.GetTimelineByIndex(i).GetName() for i in range(1,p.GetTimelineCount()+1)]==s['timelines']
e={'project':p.GetName(),'timeline':t.GetName(),'frames':t.GetEndFrame()-t.GetStartFrame(),'source_unchanged':True,'render_started':False}
(O/'resolve-preservation.json').write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(e,ensure_ascii=False),flush=True)
os._exit(0)
