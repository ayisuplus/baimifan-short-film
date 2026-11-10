import json, os
from pathlib import Path
import DaVinciResolveScript as dvr
O=Path(__file__).resolve().parent
r=dvr.scriptapp('Resolve'); assert r
pm=r.GetProjectManager(); previous=pm.GetCurrentProject()
assert previous and previous.GetName()=='Untitled Project' and previous.GetTimelineCount()==0
p=pm.LoadProject('\u300a\u767d\u7c73\u996d\u300b'); assert p and not p.IsRenderingInProgress()
t=p.GetCurrentTimeline(); assert t
tracks=[]
for kind in ['video','audio','subtitle']:
 for i in range(1,t.GetTrackCount(kind)+1):
  items=[]
  for c in t.GetItemListInTrack(kind,i) or []:
   m=c.GetMediaPoolItem()
   x=dict(name=c.GetName(),start=c.GetStart(),end=c.GetEnd(),enabled=c.GetClipEnabled(),source=m.GetClipProperty('File Path') if m else None)
   if kind!='subtitle': x.update(source_in=c.GetSourceStartFrame(),source_out=c.GetSourceEndFrame(),speed=c.GetSpeed(),properties=c.GetProperties(),media=m.GetClipProperty() if m else None)
   items.append(x)
  tracks.append(dict(kind=kind,index=i,name=t.GetTrackName(kind,i),enabled=t.GetIsTrackEnabled(kind,i),items=items))
s=dict(project=p.GetName(),name=t.GetName(),id=t.GetUniqueId(),start=t.GetStartFrame(),end=t.GetEndFrame(),settings=t.GetSettings(),tracks=tracks,project_settings=p.GetSettings(),timelines=[p.GetTimelineByIndex(i).GetName() for i in range(1,p.GetTimelineCount()+1)])
assert not (O/'Resolve-current.json').exists()
(O/'Resolve-current.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf8')
assert pm.ExportProject(p.GetName(),str(O/'migration-source.drp'),True)
print(json.dumps({'project':s['project'],'timeline':s['name'],'start':s['start'],'end':s['end'],'tracks':[{'kind':x['kind'],'count':len(x['items'])} for x in tracks],'backup':True},ensure_ascii=False),flush=True)
os._exit(0)
