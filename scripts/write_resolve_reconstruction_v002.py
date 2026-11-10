"""Generate reviewable ASCII-only Resolve scripts with frozen local input data."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'后期/声画重构-v002'
def read(p):return json.loads(p.read_text(encoding='utf8'))
P=read(O/'后期执行计划.json');M=read(O/'声音施工记录.json');F=read(O/'音效施工记录.json')
if '--dialogue-music-only' in sys.argv:F={'stems':[]}
def emit(name,data,body):
    code='import json\ndata=json.loads('+repr(json.dumps(data,ensure_ascii=True))+')\n'+body
    (O/name).write_text(code.encode('ascii','backslashreplace').decode(),encoding='ascii')
emit('resolve_build_v002.py',{'plan':P,'base':str(O),'fusion_base':str(R/'后期/导演后期修正-v001')},'''
assert not project.IsRenderingInProgress()
assert project.GetName()=='《白米饭》'
mp=project.GetMediaPool(); p=data['plan']; pm=resolve.GetProjectManager()
assert not any(project.GetTimelineByIndex(i).GetName()==p['timeline'] for i in range(1,project.GetTimelineCount()+1)), 'Timeline already exists; inspect instead of rebuilding'
assert pm.ExportProject(project.GetName(),data['base']+'/施工前工程备份.drp',True)
def clips(f):
 a=list(f.GetClipList() or [])
 for sub in f.GetSubFolderList() or []:a+=clips(sub)
 return a
lookup={c.GetClipProperty('File Path').replace('\\\\','/'):c for c in clips(mp.GetRootFolder()) if c.GetClipProperty('File Path')}
folder=next((f for f in mp.GetRootFolder().GetSubFolderList() if f.GetName()=='04_Church_Reconstruction_v002'),None)
if folder is None:folder=mp.AddSubFolder(mp.GetRootFolder(),'04_Church_Reconstruction_v002')
mp.SetCurrentFolder(folder)
paths=list(dict.fromkeys(s['source'].replace('\\\\','/') for s in p['edl']))
missing=[x for x in paths if x not in lookup]
if missing:
 imported=mp.ImportMedia(missing); assert len(imported)==len(missing)
 lookup.update({c.GetClipProperty('File Path').replace('\\\\','/'):c for c in imported})
t=mp.CreateEmptyTimeline(p['timeline']);assert t
t.SetStartTimecode('00:00:00:00');project.SetCurrentTimeline(t)
receipt=[]
for s in p['edl']:
 c=lookup[s['source'].replace('\\\\','/')]
 item=mp.AppendToTimeline([{'mediaPoolItem':c,'startFrame':s['in'],'endFrame':s['out'],'recordFrame':s['record'],'trackIndex':1,'mediaType':1}])[0]
 item.SetName(s['name'])
 if abs(s['speed']-100)>.0001:assert item.SetSpeed({'Percentage':s['speed'],'RippleTimeline':True,'PitchCorrection':False})
 if s['props']:assert item.SetProperties({'TransformEnabled':True,**s['props']})
 item.SetProperties({'RetimeAndScalingEnabled':True,'RetimeProcess':resolve.RETIME_OPTICAL_FLOW if s['speed']<95 else resolve.RETIME_NEAREST,'MotionEstimation':resolve.MOTION_EST_ENHANCED_BETTER})
 for attempt in range(4):
  actual=item.GetDuration()
  if actual==s['frames']:break
  item.SetSpeed({'Percentage':round(item.GetSpeed()['Percentage']*actual/s['frames'],2),'RippleTimeline':True})
 assert item.GetStart()==s['record'] and item.GetDuration()==s['frames'],s['name']
 receipt.append({'name':s['name'],'start':item.GetStart(),'end':item.GetEnd(),'source':c.GetClipProperty('File Path'),'speed':item.GetSpeed()})
 # The pre-existing corrections remain in their original local shot coordinate systems.
 oldcomp=s.get('fusion_comp')
 if oldcomp:assert item.ImportFusionComp(data['fusion_base']+'/'+oldcomp+'.comp')
 if s.get('fx_flash'):
  comp=item.AddFusionComp(); mi=comp.FindTool('MediaIn1');mo=comp.FindTool('MediaOut1');cc=comp.AddTool('ColorCorrector')
  cc.ConnectInput('Input',mi);mo.ConnectInput('Input',cc)
  cc.MasterRGBGain.SetExpression('iif(time<2,2.7,1)')
for b in p['batches']:t.AddMarker(b['start'],'Blue','第%d批'%b['batch'],b['id']+' — voice and sound reconformed',b['frames'])
assert t.GetEndFrame()==p['frames']
result={'timeline':t.GetName(),'video':receipt,'frames':t.GetEndFrame(),'save':pm.SaveProject()}
''')
gain=read(O/'混音电平检查.json')['shared_gain_db'] if (O/'混音电平检查.json').exists() else -3
emit('resolve_audio_v002.py',{'plan':P,'music':M['cues'],'stems':F['stems'],'gain_db':gain},'''
mp=project.GetMediaPool();t=project.GetCurrentTimeline();p=data['plan']
assert t.GetName()==p['timeline']
def clips(f):
 a=list(f.GetClipList() or [])
 for sub in f.GetSubFolderList() or []:a+=clips(sub)
 return a
lookup={c.GetClipProperty('File Path').replace('\\\\','/'):c for c in clips(mp.GetRootFolder()) if c.GetClipProperty('File Path')}
rows=[(1,v) for v in p['voice']]+[(2,m) for m in data['music']]+[(i+3,s) for i,s in enumerate(data['stems'])]
paths=list(dict.fromkeys(v['path'].replace('\\\\','/') for _,v in rows));missing=[x for x in paths if x not in lookup]
if missing:
 folder=mp.AddSubFolder(mp.GetRootFolder(),'05_Soundscape_v002');mp.SetCurrentFolder(folder)
 imported=mp.ImportMedia(missing);assert len(imported)==len(missing)
 lookup.update({c.GetClipProperty('File Path').replace('\\\\','/'):c for c in imported})
while t.GetTrackCount('audio')<6:assert t.AddTrack('audio','stereo')
for i,name in enumerate(['Dialogue_Selected_63','Music_Reconformed_13','Ambience','Foley','Action','Magic'],1):t.SetTrackName('audio',i,name)
receipt=[]
for track,v in rows:
 c=lookup[v['path'].replace('\\\\','/')]
 existing=[a for a in (t.GetItemListInTrack('audio',track) or []) if a.GetName()==v['id']]
 assert len(existing)<=1, v['id']
 if existing:
  item=existing[0]
  assert item.GetMediaPoolItem().GetClipProperty('File Path').replace('\\\\','/')==v['path'].replace('\\\\','/'),v['id']
 else:
  item=mp.AppendToTimeline([{'mediaPoolItem':c,'recordFrame':v['record'],'mediaType':2,'trackIndex':track}])[0];item.SetName(v['id'])
 assert item.SetProperties({'AudioVolumeEnabled':True,'AudioVolume':data['gain_db']})
 assert item.GetStart(True)==v['record']
 receipt.append({'id':v['id'],'track':track,'start':item.GetStart(True),'duration':item.GetDuration(True),'source':c.GetClipProperty('File Path'),'volume':item.GetProperties().get('AudioVolume'),'speed':item.GetSpeed()})
assert t.GetEndFrame()<=p['frames']+1
result={'audio':receipt,'save':resolve.GetProjectManager().SaveProject()}
''')
print('Resolve scripts prepared')
