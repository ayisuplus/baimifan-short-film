from pathlib import Path
import json,hashlib,sys,os
import DaVinciResolveScript as dvr
R=Path('E:/projects/内容创作/故事短片/白米饭');O=R/'后期/教堂动画修订-v011'
resolve=dvr.scriptapp('Resolve');p=resolve.GetProjectManager().GetCurrentProject();t=p.GetCurrentTimeline();assert t.GetName()=='v011_Church_Animation_Repair';mp=p.GetMediaPool()
raw=(O/'白米饭-v011-中文字幕.srt').read_bytes();tag=hashlib.sha256(raw).hexdigest()[:8];source=O/f'白米饭-v011-中文字幕-{tag}.srt';source.write_bytes(raw)
name='v011_Subtitles_'+tag;folders=[f for f in mp.GetRootFolder().GetSubFolderList() if f.GetName()==name];folder=folders[0] if folders else mp.AddSubFolder(mp.GetRootFolder(),name);mp.SetCurrentFolder(folder)
clips=folder.GetClipList() or mp.ImportMedia([str(source)]);assert len(clips)==1;assert mp.SetSelectedClip(clips[0]);resolve.OpenPage('edit');resolve.GetProjectManager().SaveProject()
print(json.dumps(dict(selected=clips[0].GetName(),folder=name,source=str(source)),ensure_ascii=True));sys.stdout.flush();os._exit(0)
