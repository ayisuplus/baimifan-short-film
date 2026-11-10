import json, os, sys
from pathlib import Path
import DaVinciResolveScript as dvr
r=dvr.scriptapp('Resolve'); assert r
pm=r.GetProjectManager()
p=pm.GetCurrentProject()
print(json.dumps({'current':p.GetName() if p else None,'projects':pm.GetProjectListInCurrentFolder(),'folders':pm.GetFolderListInCurrentFolder()},ensure_ascii=False),flush=True)
os._exit(0)
