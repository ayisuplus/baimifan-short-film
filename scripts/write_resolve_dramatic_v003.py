"""Prepare native timeline scripts, explicitly without project/video exports."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'后期/导演重构-v003'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def emit(name,data,body):
 s='import json\ndata=json.loads('+repr(json.dumps(data,ensure_ascii=True))+')\n'+body
 (O/name).write_text(s.encode('ascii','backslashreplace').decode(),encoding='ascii')
P=read(O/'后期执行计划.json');M=read(O/'声音施工记录.json');F=read(O/'音效施工记录.json');G=read(O/'混音电平检查.json')
emit('resolve_build_v003.py',dict(plan={k:P[k] for k in ['timeline','edl','batches','frames']},fusion_base=str(R/'后期/导演后期修正-v001')),'''
assert project.GetName()=='《白米饭》' and not project.IsRenderingInProgress()
mp=project.GetMediaPool();p=data['plan'];pm=resolve.GetProjectManager()
assert not any(project.GetTimelineByIndex(i).GetName()==p['timeline'] for i in range(1,project.GetTimelineCount()+1)),'Already exists; read back, do not duplicate'
assert pm.SaveProject()
def clips(f):
 a=list(f.GetClipList() or [])
 for s in f.GetSubFolderList() or []:a+=clips(s)
 return a
lookup={c.GetClipProperty('File Path').replace('\\\\','/'):c for c in clips(mp.GetRootFolder()) if c.GetClipProperty('File Path')}
folder=mp.AddSubFolder(mp.GetRootFolder(),'06_Dramatic_Reconstruction_v003');mp.SetCurrentFolder(folder)
paths=list(dict.fromkeys(s['source'].replace('\\\\','/') for s in p['edl']));missing=[x for x in paths if x not in lookup]
if missing:
 imported=mp.ImportMedia(missing);assert len(imported)==len(missing)
 lookup.update({c.GetClipProperty('File Path').replace('\\\\','/'):c for c in imported})
t=mp.CreateEmptyTimeline(p['timeline']);assert t;t.SetStartTimecode('00:00:00:00');project.SetCurrentTimeline(t)
receipt=[]
for s in p['edl']:
 c=lookup[s['source'].replace('\\\\','/')]
 item=mp.AppendToTimeline([dict(mediaPoolItem=c,startFrame=s['in'],endFrame=s['out'],recordFrame=s['record'],trackIndex=1,mediaType=1)])[0]
 item.SetName(s['name'])
 if abs(s['speed']-100)>.0001:assert item.SetSpeed(dict(Percentage=s['speed'],RippleTimeline=True,PitchCorrection=False))
 if s['props']:assert item.SetProperties(dict(TransformEnabled=True,**s['props']))
 item.SetProperties(dict(RetimeAndScalingEnabled=True,RetimeProcess=resolve.RETIME_OPTICAL_FLOW if s['speed']<95 else resolve.RETIME_NEAREST,MotionEstimation=resolve.MOTION_EST_ENHANCED_BETTER))
 for attempt in range(4):
  actual=item.GetDuration()
  if actual==s['frames']:break
  item.SetSpeed(dict(Percentage=round(item.GetSpeed()['Percentage']*actual/s['frames'],2),RippleTimeline=True))
 assert item.GetStart()==s['record'] and item.GetDuration()==s['frames'],s['name']
 if s.get('fusion_comp'):assert item.ImportFusionComp(data['fusion_base']+'/'+s['fusion_comp']+'.comp')
 if s.get('follow_face'):
  comp=item.AddFusionComp();mi=comp.FindTool('MediaIn1');mo=comp.FindTool('MediaOut1');tr=comp.AddTool('Transform');tr.SetAttrs({'TOOLS_Name':'FollowFace_v003'});tr.ConnectInput('Input',mi);mo.ConnectInput('Input',tr);tr.Size=2.7;tr.Center.SetExpression('Point(0.5, 0.4515625 + 0.1125 * min(max((time-84)/54,0),1))')
 if s.get('fx_flash'):
  comp=item.AddFusionComp();mi=comp.FindTool('MediaIn1');mo=comp.FindTool('MediaOut1');cc=comp.AddTool('ColorCorrector');cc.ConnectInput('Input',mi);mo.ConnectInput('Input',cc);cc.MasterRGBGain.SetExpression('iif(time<2,2.7,1)')
 receipt.append(dict(name=s['name'],start=item.GetStart(),end=item.GetEnd(),source=c.GetClipProperty('File Path'),speed=item.GetSpeed()))
for b in p['batches']:t.AddMarker(b['start'],'Blue','第%d批'%b['batch'],b['id'],b['frames'])
assert t.GetEndFrame()==p['frames']
result=dict(timeline=t.GetName(),frames=t.GetEndFrame(),video=receipt,save=pm.SaveProject())
''')
rows=[dict(v,track=1,id=v['native_id']) for v in P['voice']]+M['cues']+F['stems']
extras=read(O/'新增BGM来源.json')
emit('resolve_audio_v003.py',dict(plan={k:P[k] for k in ['timeline','frames']},rows=rows,gain=G['shared_gain_db'],extra=extras,root=str(R)),'''
mp=project.GetMediaPool();t=project.GetCurrentTimeline();p=data['plan'];assert t.GetName()==p['timeline']
def clips(f):
 a=list(f.GetClipList() or [])
 for s in f.GetSubFolderList() or []:a+=clips(s)
 return a
lookup={c.GetClipProperty('File Path').replace('\\\\','/'):c for c in clips(mp.GetRootFolder()) if c.GetClipProperty('File Path')}
folder=mp.AddSubFolder(mp.GetRootFolder(),'07_Sound_v003');mp.SetCurrentFolder(folder)
paths=list(dict.fromkeys(v['path'].replace('\\\\','/') for v in data['rows']));missing=[x for x in paths if x not in lookup]
if missing:
 imported=mp.ImportMedia(missing);assert len(imported)==len(missing)
 lookup.update({c.GetClipProperty('File Path').replace('\\\\','/'):c for c in imported})
while t.GetTrackCount('audio')<8:assert t.AddTrack('audio','stereo')
for i,name in enumerate(['Dialogue_Selected','Music_A','Music_B','Music_C','Ambience','Foley','Action','Magic'],1):t.SetTrackName('audio',i,name);t.SetTrackEnable('audio',i,True)
receipt=[]
for v in data['rows']:
 track=v['track'];c=lookup[v['path'].replace('\\\\','/')]
 existing=[x for x in t.GetItemListInTrack('audio',track) or [] if x.GetName()==v['id']]
 assert len(existing)<=1
 if existing:item=existing[0]
 else:item=mp.AppendToTimeline([dict(mediaPoolItem=c,recordFrame=v['record'],mediaType=2,trackIndex=track)])[0];item.SetName(v['id'])
 assert item.SetProperties(dict(AudioVolumeEnabled=True,AudioVolume=data['gain']))
 assert item.GetStart(True)==v['record']
 receipt.append(dict(id=v['id'],track=track,start=item.GetStart(True),duration=item.GetDuration(True),volume=item.GetProperties().get('AudioVolume'),source=c.GetClipProperty('File Path')))
folder=mp.AddSubFolder(mp.GetRootFolder(),'08_BGM_New_Audition_Candidates');mp.SetCurrentFolder(folder)
additional=mp.ImportMedia([data['root']+'/'+x['path'] for x in data['extra']]);assert len(additional)==len(data['extra'])
assert t.GetEndFrame()<=p['frames']+1
resolve.OpenPage('edit');t.SetCurrentTimecode('00:01:19:14')
result=dict(timeline=t.GetName(),frames=t.GetEndFrame(),audio=receipt,additional_music=len(additional),tracks=[dict(index=i,enabled=t.GetIsTrackEnabled('audio',i)) for i in range(1,9)],save=resolve.GetProjectManager().SaveProject())
''')
print('Prepared native scripts without export operations')
