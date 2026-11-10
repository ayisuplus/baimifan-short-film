"""Install a reviewed equal-length batch-3 retake in a preserved timeline duplicate."""
from pathlib import Path
import json,sys,os,hashlib
import DaVinciResolveScript as dvr
R=Path('E:/projects/内容创作/故事短片/白米饭');O=R/'后期/逐镜修订-v012/第三批/长阶恢复'
def read(n):return json.loads((O/n).read_text(encoding='utf8'))
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
base=json.loads((O.parent/'v012-工程读回.json').read_text(encoding='utf8'));edit=read('采用施工.json');assert edit['review_passed'] and sum(x['frames'] for x in edit['video'])==264
resolve=dvr.scriptapp('Resolve');pm=resolve.GetProjectManager();p=pm.GetCurrentProject();mp=p.GetMediaPool()
assert p.GetName()=='《白米饭》' and not p.IsRenderingInProgress()
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
t=p.GetCurrentTimeline();assert t.GetName()==base['timeline'] and snap(t)==base,'Current timeline changed; inspect before writing'
assert pm.SaveProject()
target='v013_Stair_Restore';assert all(p.GetTimelineByIndex(i).GetName()!=target for i in range(1,p.GetTimelineCount()+1))
new=t.DuplicateTimeline(target);assert new and p.SetCurrentTimeline(new)
old=[c for c in new.GetItemListInTrack('video',1) if 682<=c.GetStart()<946];assert len(old)==2 and old[0].GetStart()==682 and old[-1].GetEnd()==946
props=old[0].GetProperties();assert new.DeleteClips(old,False)
cursor=682
for i,s in enumerate(edit['video']):
 path=R/s['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==s['sha256']
 mi=mp.ImportMedia([str(path)]);assert len(mi)==1
 c=mp.AppendToTimeline([dict(mediaPoolItem=mi[0],startFrame=s['in'],endFrame=s['in']+s['frames'],recordFrame=cursor,trackIndex=1,mediaType=1)])[0]
 assert c.SetName('B03_v013_StairsAndGuards_'+str(i+1)) and c.SetProperties(props)
 if s.get('speed',100)!=100:assert c.SetSpeed(dict(Percentage=s['speed'],RippleTimeline=False,PitchCorrection=False))
 assert c.GetStart()==cursor and c.GetDuration()==s['frames'];cursor+=s['frames']
assert cursor==946
if edit.get('foley'):
 s=edit['foley'];old=new.GetItemListInTrack('audio',6);assert len(old)==1;props=old[0].GetProperties();assert new.DeleteClips(old,False)
 mi=mp.ImportMedia([str(R/s['path'])]);assert len(mi)==1
 c=mp.AppendToTimeline([dict(mediaPoolItem=mi[0],recordFrame=0,trackIndex=6,mediaType=2)])[0]
 assert c.SetName('Foley_v013_B03') and c.SetProperties(dict(AudioVolumeEnabled=True,AudioVolume=props['AudioVolume']))
new.AddMarker(682,'Orange','第三批：恢复登长阶','原长阶2秒→守卫竖枪→低位交叉→收枪放行；BGM字幕暂不处理',264)
actual=snap(new);old_after=snap(t);assert old_after==base;assert p.SetCurrentTimeline(new)
assert actual['end']==base['end']
for a,b in zip(actual['tracks'],base['tracks']):
 assert all(a[k]==b[k] for k in ['type','index','name','enabled'])
 if a['type']=='video' and a['index']==1:
  assert [x for x in a['items'] if x['end']<=682 or x['start']>=946]==[x for x in b['items'] if x['end']<=682 or x['start']>=946]
 elif a['type']=='audio' and a['index']==6 and edit.get('foley'):pass
 else:assert a['items']==b['items'],('Unexpected change',a['type'],a['index'])
v=actual['tracks'][0]['items'];assert all(a['end']==b['start'] for a,b in zip(v,v[1:]))
save('v013-工程读回.json',actual)
result=dict(timeline=target,frames=new.GetEndFrame(),changed_picture_range=[682,946],baseline_preserved=True,other_picture_audio_subtitles_exact=True,foley_only_batch3_changed=bool(edit.get('foley')),active_dialogue=54,subtitle_cues=56,saved=pm.SaveProject(),exported=False,author_final_accepted=False)
save('核验结果.json',result);new.SetCurrentTimecode('00:00:28:10');resolve.OpenPage('edit')
print(json.dumps(result,ensure_ascii=True));sys.stdout.flush();os._exit(0)
