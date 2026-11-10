"""Read current-timeline state for each timeline: inactive API reads omit live properties."""
import json,hashlib
from pathlib import Path
out=Path('E:/projects/内容创作/故事短片/白米饭/后期/对白补齐-v009')
old=json.loads((out/'v008-装配前快照.json').read_text(encoding='utf8'))
plan=json.loads((out/'对白装配计划.json').read_text(encoding='utf8'))
timelines=[project.GetTimelineByIndex(i) for i in range(1,project.GetTimelineCount()+1)]
b=next(t for t in timelines if t.GetName()==plan['baseline'])
t=next(t for t in timelines if t.GetName()==plan['timeline'])
def snap(t):
 assert project.SetCurrentTimeline(t)
 d={'project':project.GetName(),'timeline':t.GetName(),'start':t.GetStartFrame(),'end':t.GetEndFrame(),'fps':t.GetSetting('timelineFrameRate'),'tracks':[]}
 for typ in ['video','audio']:
  for i in range(1,t.GetTrackCount(typ)+1):
   items=[]
   for c in (t.GetItemListInTrack(typ,i) or []):
    m=c.GetMediaPoolItem()
    items.append({'name':c.GetName(),'start':c.GetStart(True),'end':c.GetEnd(True),'duration':c.GetDuration(True),'left':c.GetLeftOffset(True),'right':c.GetRightOffset(True),'path':m.GetClipProperty('File Path') if m else None,'properties':c.GetProperties()})
   d['tracks'].append({'type':typ,'index':i,'name':t.GetTrackName(typ,i),'enabled':t.GetIsTrackEnabled(typ,i),'items':items})
 return d
bnow=snap(b);new=snap(t)
assert bnow==old,'Original timeline changed'
assert new['tracks'][0]==old['tracks'][0],'Picture changed'
assert new['tracks'][2:9]==old['tracks'][2:9],'Music/effects changed'
assert new['tracks'][1]['items']==old['tracks'][1]['items'] and not new['tracks'][1]['enabled']
lines=[c for tr in new['tracks'][9:] for c in tr['items']]
assert len(lines)==54 and all(tr['enabled'] for tr in new['tracks'][9:])
actual={Path(c['path']).name.split('__')[0]:c for c in lines}
assert set(actual)=={x['id'] for x in plan['lines']}
for x in plan['lines']:
 c=actual[x['id']]
 assert Path(c['path'])==Path(x['file']),x['id']+' wrong source version'
 assert hashlib.sha256(Path(c['path']).read_bytes()).hexdigest()==x['sha256'],x['id']+' wrong media hash'
 assert abs(c['start']-x['record'])<.01 and abs(c['duration']-x['duration_frames'])<.1
 assert abs(c['properties']['AudioVolume']-x['gain_db'])<.02
 assert c['properties']['AudioPitchSemiTones']==0 and c['properties']['AudioPitchCents']==0
ordered=sorted(lines,key=lambda x:x['start'])
assert all(b['start']>=a['end'] for a,b in zip(ordered,ordered[1:]))
report={'timeline':t.GetName(),'project':project.GetName(),'active_dialogue':54,'active_roles':9,'old_dialogue_muted':True,'removed_merged_old_ids_absent':plan['removed_or_merged_old_ids'],'baseline_unchanged':True,'picture_unchanged':True,'music_sfx_unchanged':True,'exact_start_duration_gain':True,'dialogue_overlaps':0,'frames':t.GetEndFrame(),'timeline_saved':resolve.GetProjectManager().SaveProject(),'exported':False,'listening_or_lipsync_acceptance':False,'api_note':'Each timeline made current before reading track enable and Fairlight properties.'}
(out/'v009-装配后快照.json').write_text(json.dumps(new,ensure_ascii=False,indent=2),encoding='utf8')
(out/'核验结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
result=report
