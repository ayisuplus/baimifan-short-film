"""Inspect/apply palace shot matching in Resolve; no media or edit replacement."""
from pathlib import Path
import json, sys, os, time
import DaVinciResolveScript as dvr
R=Path('E:/projects/内容创作/故事短片/白米饭')
O=R/'后期/宫殿调色-v014';O.mkdir(parents=True,exist_ok=True)
resolve=dvr.scriptapp('Resolve');pm=resolve.GetProjectManager();p=pm.GetCurrentProject()
assert p and p.GetName()=='《白米饭》' and not p.IsRenderingInProgress()
def save(n,d): (O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
def snap(t):
 assert p.SetCurrentTimeline(t)
 tracks=[]
 for kind in ['video','audio','subtitle']:
  for k in range(1,t.GetTrackCount(kind)+1):
   items=[]
   for c in t.GetItemListInTrack(kind,k) or []:
    m=c.GetMediaPoolItem();x=dict(name=c.GetName(),start=c.GetStart(True),end=c.GetEnd(True),path=m.GetClipProperty('File Path') if m else None,properties=c.GetProperties(),enabled=c.GetClipEnabled())
    if kind!='subtitle':x.update(source_start=c.GetSourceStartFrame(),source_end=c.GetSourceEndFrame(),speed=c.GetSpeed())
    items.append(x)
   tracks.append(dict(type=kind,index=k,name=t.GetTrackName(kind,k),enabled=t.GetIsTrackEnabled(kind,k),items=items))
 return dict(project=p.GetName(),timeline=t.GetName(),start=t.GetStartFrame(),end=t.GetEndFrame(),tracks=tracks)
def grades(t):
 assert p.SetCurrentTimeline(t)
 out=[]
 for c in t.GetItemListInTrack('video',1):
  g=c.GetNodeGraph();n=g.GetNumNodes()
  out.append(dict(name=c.GetName(),start=c.GetStart(),end=c.GetEnd(),versions=c.GetVersionNameList(0),current=c.GetCurrentVersion(),nodes=[dict(lut=g.GetLUT(i),label=g.GetNodeLabel(i),tools=g.GetToolsInNode(i)) for i in range(1,n+1)]))
 return out
def tc(f):return '%02d:%02d:%02d:%02d'%(f//86400,f//1440%60,f//24%60,f%24)
FRAMES=[700,760,920,970,1130,1220,1300]
def stills(t,tag):
 assert p.SetCurrentTimeline(t)
 for f in FRAMES:
  assert t.SetCurrentTimecode(tc(f));time.sleep(.3)
  assert p.ExportCurrentFrameAsStill(str(O/f'{tag}-{f}.png'))
mode=sys.argv[1] if len(sys.argv)>1 else 'inspect'
t=p.GetCurrentTimeline()
if mode=='inspect':
 assert t.GetName()=='v013_Stair_Restore'
 save('before.json',snap(t));g=grades(t);save('before-grades.json',g)
 save('color-settings.json',{k:v for k,v in p.GetSetting().items() if any(s in k.lower() for s in ['color','gamma','lut'])})
 stills(t,'before')
 print(json.dumps({'timeline':t.GetName(),'targets':[x for x in g if 682<=x['start']<1400]},ensure_ascii=True))
elif mode=='apply':
 assert t.GetName()=='v013_Stair_Restore'
 base=json.loads((O/'before.json').read_text(encoding='utf8'))
 before_grades=json.loads((O/'before-grades.json').read_text(encoding='utf8'))
 assert snap(t)==base and grades(t)==before_grades
 target='v014_Palace_Color_Match'
 assert all(p.GetTimelineByIndex(i).GetName()!=target for i in range(1,p.GetTimelineCount()+1))
 assert pm.SaveProject()
 new=t.DuplicateTimeline(target);assert new and p.SetCurrentTimeline(new)
 assert p.RefreshLUTList()
 lut=json.loads((O/'lut-manifest.json').read_text(encoding='utf8'))
 applied=[]
 for c in new.GetItemListInTrack('video',1):
  f=c.GetStart()
  if not 682<=f<1282:continue
  key='stair' if f==682 else 'gate' if f<916 else 'inner' if f<946 else 'dialogue'
  g=c.GetNodeGraph();assert g.GetNumNodes()==1 and not g.GetLUT(1) and not g.GetToolsInNode(1)
  version='v014_Palace_'+key
  assert c.AddVersion(version,0) and c.LoadVersionByName(version,0)
  assert c.GetNodeGraph().SetLUT(1,lut[key]['relative_lut'])
  applied.append(dict(name=c.GetName(),start=f,end=c.GetEnd(),grade=key,lut=c.GetNodeGraph().GetLUT(1)))
 assert len(applied)==9
 actual=snap(new);comparison=dict(actual,timeline=base['timeline']);assert comparison==base,'Edit, sound or subtitle changed'
 assert snap(t)==base and grades(t)==before_grades,'Baseline changed'
 assert p.SetCurrentTimeline(new)
 save('applied.json',applied);save('after.json',actual);save('after-grades.json',grades(new))
 assert pm.SaveProject()
 stills(new,'after')
 save('verification.json',dict(timeline=target,frames=new.GetEndFrame(),graded_items=len(applied),picture_range=[682,1282],all_edits_audio_subtitles_exact=True,baseline_edits_and_grades_preserved=True,saved=True,final_export=False,visual_review_pending=True))
 new.SetCurrentTimecode(tc(730));resolve.OpenPage('color')
 print(json.dumps({'timeline':target,'graded_items':len(applied),'saved':True,'all_edits_audio_subtitles_exact':True},ensure_ascii=True))
elif mode=='verify':
 assert t.GetName()=='v014_Palace_Color_Match'
 base=json.loads((O/'before.json').read_text(encoding='utf8'))
 before_grades=json.loads((O/'before-grades.json').read_text(encoding='utf8'))
 actual=snap(t);assert dict(actual,timeline=base['timeline'])==base
 old=next(p.GetTimelineByIndex(i) for i in range(1,p.GetTimelineCount()+1) if p.GetTimelineByIndex(i).GetName()==base['timeline'])
 assert snap(old)==base and grades(old)==before_grades
 FRAMES=[760,920,970]
 stills(old,'baseline-check')
 g=grades(t)
 assert [x for x in g if x['start']<682 or x['start']>=1282]==[x for x in before_grades if x['start']<682 or x['start']>=1282]
 FRAMES=[729,730,915,916,945,946,1281,1282]
 stills(t,'join')
 assert pm.SaveProject()
 t.SetCurrentTimecode(tc(970));resolve.OpenPage('color')
 print('Verified all edits/audio/subtitles and all out-of-range grades; baseline unchanged; joins captured.')
else:raise ValueError(mode)
sys.stdout.flush();os._exit(0)
