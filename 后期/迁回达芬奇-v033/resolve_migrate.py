"""Migrate the verified OpenCut picture edit using the installed Resolve API."""
from pathlib import Path
import json, sys, os
import DaVinciResolveScript as dvr

O = Path(__file__).resolve().parent
NAME = 'v033_OpenCut_Picture_Return'
r = dvr.scriptapp('Resolve')
assert r, 'Resolve not connected'
pm = r.GetProjectManager()
p = pm.GetCurrentProject()
assert p and p.GetName() == '《白米饭》' and not p.IsRenderingInProgress()
mp = p.GetMediaPool()

def save(name, value):
    (O/name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf8')

def snap(t):
    tracks=[]
    for kind in ['video', 'audio', 'subtitle']:
        for i in range(1, t.GetTrackCount(kind)+1):
            items=[]
            for c in t.GetItemListInTrack(kind,i) or []:
                m=c.GetMediaPoolItem()
                item=dict(name=c.GetName(),start=c.GetStart(),end=c.GetEnd(),enabled=c.GetClipEnabled(),source=m.GetClipProperty('File Path') if m else None)
                if kind != 'subtitle':
                    item.update(source_in=c.GetSourceStartFrame(),source_out=c.GetSourceEndFrame(),speed=c.GetSpeed(),properties=c.GetProperties())
                items.append(item)
            tracks.append(dict(kind=kind,index=i,name=t.GetTrackName(kind,i),enabled=t.GetIsTrackEnabled(kind,i),items=items))
    return dict(name=t.GetName(),id=t.GetUniqueId(),start=t.GetStartFrame(),end=t.GetEndFrame(),settings=t.GetSettings(),tracks=tracks)

def all_timelines():
    return [p.GetTimelineByIndex(i) for i in range(1,p.GetTimelineCount()+1)]

def verify_old(before):
    current=p.GetCurrentTimeline()
    baseline=next(t for t in all_timelines() if t.GetName()==before['current'])
    # Track enabled/audio property reporting depends on the active timeline.
    # Compare in the same active context as the original read-only snapshot.
    assert p.SetCurrentTimeline(baseline)
    expected={x['name']:x for x in before['timelines']}
    checks={t.GetName():snap(t)==expected[t.GetName()] for t in all_timelines() if t.GetName()!=NAME}
    assert p.SetCurrentTimeline(current)
    assert all(checks.values()),checks
    return checks

mode=sys.argv[1]
if mode=='inspect':
    assert not (O/'Resolve施工前.json').exists(), 'Do not overwrite checkpoint'
    save('Resolve施工前.json',dict(project=p.GetName(),current=p.GetCurrentTimeline().GetName(),settings=p.GetSettings(),timelines=[snap(t) for t in all_timelines()]))
    assert pm.SaveProject()
    assert pm.ExportProject(p.GetName(),str(O/'施工前工程备份.drp'),True)
    print(json.dumps(dict(project=p.GetName(),timeline=p.GetCurrentTimeline().GetName(),backup=True,settings=p.GetCurrentTimeline().GetSettings()),ensure_ascii=False),flush=True)
elif mode=='build':
    before=json.loads((O/'Resolve施工前.json').read_text(encoding='utf8'))
    assert [snap(t) for t in all_timelines()]==before['timelines'], 'Baseline changed since backup'
    assert all(t.GetName()!=NAME for t in all_timelines())
    plan=json.loads((O/'源片清单.json').read_text(encoding='utf8'))
    assert len(plan)==118 and sum(x['frames'] for x in plan)==9059
    for x in plan:
        assert Path(x['source']).is_file()
        x['source_in']=6 if x['name'].startswith('036_') else 0
        x['source_out_exclusive']=x['source_in']+x['frames']
        assert x['source_out_exclusive']<=int(x['media']['nb_frames'])
    save('迁移剪辑清单.json',plan)
    folder=mp.AddSubFolder(mp.GetRootFolder(),'33_OpenCut_Picture_Return')
    assert folder and mp.SetCurrentFolder(folder)
    imported=mp.ImportMedia([x['source'] for x in plan])
    assert imported and len(imported)==118
    lookup={Path(c.GetClipProperty('File Path')).resolve():c for c in imported}
    t=mp.CreateEmptyTimeline(NAME)
    assert t and p.SetCurrentTimeline(t)
    assert t.SetStartTimecode('00:00:00:00')
    assert float(t.GetSettings()['timelineFrameRate'])==24
    assert t.GetSettings()['timelineResolutionWidth']=='1344'
    assert t.GetSettings()['timelineResolutionHeight']=='768'
    assert t.SetTrackName('video',1,'OpenCut v032 画面迁回')
    for x in plan:
        c=lookup[Path(x['source']).resolve()]
        info=dict(mediaPoolItem=c,startFrame=x['source_in'],endFrame=x['source_out_exclusive'],recordFrame=x['start'],trackIndex=1,mediaType=1)
        made=mp.AppendToTimeline([info]);assert made and len(made)==1
        item=made[0]
        # API generations differ on out-point semantics. Only adjust a new
        # item when the returned duration proves an inclusive endpoint.
        if item.GetDuration()==x['frames']+1:
            assert t.DeleteClips([item],False)
            info['endFrame']-=1
            made=mp.AppendToTimeline([info]);assert made and len(made)==1
            item=made[0]
        assert item.GetStart()==x['start'] and item.GetDuration()==x['frames'],(x['name'],item.GetStart(),item.GetDuration())
        assert item.GetSourceStartFrame()==x['source_in'],x['name']
        assert item.SetName(x['name'])
    assert t.GetEndFrame()==9059 and len(t.GetItemListInTrack('video',1))==118
    assert all(not t.GetItemListInTrack(kind,i) for kind in ['audio','subtitle'] for i in range(1,t.GetTrackCount(kind)+1))
    verify_old(before)
    save('Resolve迁回读回.json',snap(t))
    assert pm.SaveProject()
    assert t.SetCurrentTimecode('00:02:18:13')
    assert r.OpenPage('edit')
    save('迁移核验.json',dict(project=p.GetName(),timeline=t.GetName(),timeline_id=t.GetUniqueId(),clips=118,frames=9059,fps=24,source_windows_verified=True,original_timelines_preserved=True,picture_only=True,saved=True,comfyui_used=False,final_render=False))
    print('Built and verified 118 editable picture clips / 9059 frames. Old timelines unchanged.',flush=True)
elif mode=='finalize':
    t=p.GetCurrentTimeline();assert t.GetName()==NAME
    plan=json.loads((O/'迁移剪辑清单.json').read_text(encoding='utf8'))
    items=t.GetItemListInTrack('video',1)
    assert len(items)==len(plan)==118 and t.GetEndFrame()==9059
    for c,x in zip(items,plan):
        assert c.GetName()==x['name'] and c.GetStart()==x['start'] and c.GetDuration()==x['frames']
        assert c.GetSourceStartFrame()==x['source_in']
        assert Path(c.GetMediaPoolItem().GetClipProperty('File Path')).resolve()==Path(x['source']).resolve()
    before=json.loads((O/'Resolve施工前.json').read_text(encoding='utf8'))
    checks=verify_old(before)
    save('Resolve迁回读回.json',snap(t))
    assert pm.SaveProject()
    assert t.SetCurrentTimecode('00:02:18:13')
    assert r.OpenPage('edit')
    save('迁移核验.json',dict(project=p.GetName(),timeline=t.GetName(),timeline_id=t.GetUniqueId(),clips=118,frames=9059,fps=24,source_windows_verified=True,original_timelines_preserved=checks,picture_only=True,saved=True,comfyui_used=False,final_render=False))
    print('Saved 118 clips / 9059 frames; all 16 original timelines unchanged.',flush=True)
elif mode=='verify':
    t=p.GetCurrentTimeline();assert t.GetName()==NAME
    expected=json.loads((O/'Resolve迁回读回.json').read_text(encoding='utf8'))
    assert snap(t)==expected
    before=json.loads((O/'Resolve施工前.json').read_text(encoding='utf8'))
    verify_old(before)
    assert pm.SaveProject()
    print('Separate API readback matches the saved edit and all prior timelines.',flush=True)
else:
    raise ValueError(mode)
sys.stdout.flush()
os._exit(0)
