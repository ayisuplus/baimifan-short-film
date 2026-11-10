"""Import the author's adopted high-angle lamps shot; leave all timelines unchanged."""
from pathlib import Path
import json,os,sys,hashlib
import DaVinciResolveScript as dvr
R=Path('E:/projects/内容创作/故事短片/白米饭');O=R/'视频制作/Metaso-H3-v016'
q=json.loads((O/'执行队列.json').read_text(encoding='utf8'))
b=next(x for x in q['items'] if x['attempt_id']=='CY005L-v016-high-angle-r2')
path=R/b['local_path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==b['sha256']
r=dvr.scriptapp('Resolve');pm=r.GetProjectManager();p=pm.GetCurrentProject()
assert p and p.GetName()=='《白米饭》' and not p.IsRenderingInProgress()
t=p.GetCurrentTimeline();original_timeline=t.GetName();mp=p.GetMediaPool();old_folder=mp.GetCurrentFolder();root=mp.GetRootFolder()
name='v016_宫殿俯拍亮灯_作者采用'
folder=next((x for x in root.GetSubFolderList() if x.GetName()==name),None)
if folder is None:folder=mp.AddSubFolder(root,name)
assert folder and mp.SetCurrentFolder(folder)
existing=[x for x in folder.GetClipList() if x.GetClipProperty('File Path')==str(path)]
clips=existing or mp.ImportMedia([str(path)]);assert len(clips)==1
assert p.GetCurrentTimeline().GetName()==original_timeline
assert mp.SetCurrentFolder(old_folder) and pm.SaveProject()
receipt=dict(project=p.GetName(),timeline_unchanged=original_timeline,bin=name,media_path=str(path),clip_name=clips[0].GetName(),sha256=b['sha256'],imported=True,timeline_installed=False,bgm_subtitle_untouched=True,saved=True)
(O/'达芬奇素材导入.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=True));sys.stdout.flush();os._exit(0)
