"""Read back actual Resolve subtitles and audio; preserve the v009 baseline."""
import json, hashlib
from pathlib import Path
ROOT=Path('E:/projects/内容创作/故事短片/白米饭')
OUT=ROOT/'后期/对白字幕同步-v010'
plan=json.loads((OUT/'同步计划.json').read_text(encoding='utf8'))
old=json.loads((ROOT/'后期/对白补齐-v009/v009-装配后快照.json').read_text(encoding='utf8'))
def snapshot(t):
    assert project.SetCurrentTimeline(t)
    d={'project':project.GetName(),'timeline':t.GetName(),'start':t.GetStartFrame(),'end':t.GetEndFrame(),'fps':t.GetSetting('timelineFrameRate'),'tracks':[]}
    for typ in ['video','audio']:
        for i in range(1,t.GetTrackCount(typ)+1):
            items=[]
            for c in t.GetItemListInTrack(typ,i) or []:
                m=c.GetMediaPoolItem()
                items.append({'name':c.GetName(),'start':c.GetStart(True),'end':c.GetEnd(True),'duration':c.GetDuration(True),'left':c.GetLeftOffset(True),'right':c.GetRightOffset(True),'path':m.GetClipProperty('File Path') if m else None,'properties':c.GetProperties()})
            d['tracks'].append({'type':typ,'index':i,'name':t.GetTrackName(typ,i),'enabled':t.GetIsTrackEnabled(typ,i),'items':items})
    return d
ts=[project.GetTimelineByIndex(i) for i in range(1,project.GetTimelineCount()+1)]
b=next(t for t in ts if t.GetName()==plan['baseline'])
t=next(t for t in ts if t.GetName()==plan['timeline'])
bn=snapshot(b)
assert bn==old,'v009 baseline changed'
n=snapshot(t)
assert n['tracks'][:9]==old['tracks'][:9],'Picture, original dialogue or music/SFX changed'
assert n['end']==old['end']==11497
audio=[c for tr in n['tracks'][9:] for c in tr['items']]
assert len(audio)==54 and all(tr['enabled'] for tr in n['tracks'][9:])
actual={Path(c['path']).name.split('__')[0]:c for c in audio}
previous={Path(c['path']).name.split('__')[0]:c for tr in old['tracks'][9:] for c in tr['items']}
assert set(actual)=={x['id'] for x in plan['lines']}
for x in plan['lines']:
    a=actual[x['id']]
    assert Path(a['path'])==Path(x['file'])
    assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==x['sha256']
    assert abs(a['start']-x['record'])<.01 and abs(a['end']-x['end'])<.1
    assert a['properties']==previous[x['id']]['properties']
    if x['id']!='VO-CY003B-01': assert a==previous[x['id']],x['id']
assert t.GetTrackCount('subtitle')==1 and t.GetIsTrackEnabled('subtitle',1)
subs=[{'text':c.GetName(),'start':c.GetStart(),'end':c.GetEnd()} for c in t.GetItemListInTrack('subtitle',1)]
assert len(subs)==54
for s,c in zip(subs,plan['subtitle_cues']):
    assert s=={'text':c['zh'],'start':c['start_frame'],'end':c['end_frame_exclusive']},(s,c)
assert all(a['end']<=b['start'] for a,b in zip(subs,subs[1:]))
n['subtitles']=subs
report={'timeline':t.GetName(),'active_dialogue':54,'subtitle_tracks':1,'subtitle_cues':54,'subtitle_text_and_frames_exact':True,'v009_unchanged':True,'picture_music_sfx_unchanged':True,'other_53_dialogue_unchanged':True,'voice_sources_hash_verified':True,'opening_sync':plan['opening_sync'],'saved':resolve.GetProjectManager().SaveProject(),'exported_film_or_project':False,'performance_lipsync_accepted':False}
(OUT/'v010-工程读回.json').write_text(json.dumps(n,ensure_ascii=True,indent=2),encoding='utf8')
(OUT/'核验结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
result=report
