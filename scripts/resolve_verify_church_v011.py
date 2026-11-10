"""Read the native timeline back and check the complete repair against source records."""
from pathlib import Path
import json,hashlib,sys,os
import DaVinciResolveScript as dvr
R=Path('E:/projects/内容创作/故事短片/白米饭');O=R/'后期/教堂动画修订-v011'
def read(n):return json.loads((O/n).read_text(encoding='utf8'))
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
resolve=dvr.scriptapp('Resolve');pm=resolve.GetProjectManager();p=pm.GetCurrentProject();t=p.GetCurrentTimeline()
plan=read('修订计划.json');base=read('修前基线.json');sound=read('声音施工.json')
assert p.GetName()=='《白米饭》' and t.GetName()==plan['timeline']
def snapshot(t):
 assert p.SetCurrentTimeline(t)
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
b=next(p.GetTimelineByIndex(i) for i in range(1,p.GetTimelineCount()+1) if p.GetTimelineByIndex(i).GetName()==plan['baseline'])
current=snapshot(t);old=snapshot(b);assert p.SetCurrentTimeline(t);save('v011-完整工程读回.json',current);save('v010-保护线复核.json',old)
errors=[]
def check(ok,description):
 if not ok:errors.append(description)
def path(s):return str(s).replace('\\','/').lower()
check(old==base,'Protected baseline changed')
v=next(x['items'] for x in current['tracks'] if x['type']=='video' and x['index']==1)
check(len(v)==len(plan['edl']),'Picture count')
check(v[0]['start']==0 and v[-1]['end']==plan['frames'] and all(a['end']==b['start'] for a,b in zip(v,v[1:])),'Picture continuity')
for x,s in zip(v,plan['edl']):
 check(x['name']==s['name'] and x['start']==s['record'] and x['duration']==s['frames'] and path(x['path'])==path(s['source']),'Picture identity '+s['name'])
 check(abs(x['source_start']-s['in'])<=1 and abs(x['source_end']-s['out'])<=1,'Picture source window '+s['name'])
 check(abs(x['speed']['Percentage']-s['speed'])<.001,'Picture speed '+s['name'])
a=[dict(x,track=tr['index']) for tr in current['tracks'] if tr['type']=='audio' for x in tr['items']]
voices=[x for x in a if x['track']>=9];check(len(voices)==54,'54 voices')
for s in plan['lines']:
 xs=[x for x in voices if x['name'].startswith(s['id']+' | ')]
 check(len(xs)==1,'Unique voice '+s['id'])
 if not xs:continue
 x=xs[0];check(path(x['path'])==path(s['file']) and hashlib.sha256(Path(s['file']).read_bytes()).hexdigest()==s['sha256'],'Voice hash '+s['id'])
 check(x['start']==s['record'] and abs(x['duration']-s['duration_frames'])<.1 and x['speed']['Percentage']==100 and x['source_start']==0,'Voice frames '+s['id'])
 check(abs(x['properties'].get('AudioVolume',0)-s['gain_db'])<.001,'Voice gain '+s['id'])
for s in sound['rows']:
 xs=[x for x in a if x['track']==s['track'] and x['name']==s['name']]
 check(len(xs)==1,'Unique stem/music '+s['name'])
 if xs:
  x=xs[0];check(x['start']==s['record'] and path(x['path'])==path(s['file']) and x['speed']['Percentage']==100 and abs(x['properties'].get('AudioVolume',0)-s['volume'])<.001,'Stem/music install '+s['name'])
subs=[x for tr in current['tracks'] if tr['type']=='subtitle' for x in tr['items']];subs.sort(key=lambda x:x['start'])
check(len(subs)==56,'56 real subtitles')
for x,s in zip(subs,plan['subtitle_cues']):
 check(x['name']==s['zh'] and x['start']==s['start_frame'] and x['end']==s['end_frame_exclusive'],'Subtitle '+s['zh'])
check(current['end']==plan['frames'],'Timeline length')
result=dict(timeline=t.GetName(),frames=current['end'],fps=24,picture_clips=len(v),active_dialogue=len(voices),subtitle_cues=len(subs),music_stem_clips=len(a)-len(voices),baseline_all_tracks_exact=old==base,errors=errors,passed=not errors,voice_sources_hash_verified=True if not errors else None,plan_sha256=hashlib.sha256((O/'修订计划.json').read_bytes()).hexdigest(),saved=pm.SaveProject(),exported_film_or_project=False,continuous_viewing_accepted=False,exact_lipsync_accepted=False,author_final_accepted=False)
save('核验结果.json',result)
if not errors:
 save('工程读回.json',dict(result,video=[{k:x[k] for k in ['name','start','end','path']} for x in v],audio=a,subtitle_count=len(subs),subtitles_pending_ui=False,baseline_preserved=True))
 t.SetCurrentTimecode('00:03:00:17');resolve.OpenPage('edit')
print(json.dumps(result,ensure_ascii=True));sys.stdout.flush();os._exit(1 if errors else 0)
