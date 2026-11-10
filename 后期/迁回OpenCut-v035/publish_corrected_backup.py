"""Publish a corrected independent backup; keep the first checked package archived."""
import build_migration as m
import shutil
from pathlib import Path
from datetime import datetime,timezone
newid=m.BACKUP+'-r2'
c=m.SOURCE/'creative'
for p in [*(c/'upscale').rglob('*.json'), c/'asset-library/import-report.json']:
 if p.exists():
  v=m.read(p);m.remap(v);m.write(p,v)
snapshot=m.read(m.OUT/'migration-browser.json')
proof=m.read(m.OUT/'source-media-evidence.json')
m.native(m.BACKUPS,'backup',{'action':'begin','id':newid,'snapshot':snapshot,'creative_root':str(c),'package_root':str(m.SOURCE/'package'),'created_at':datetime.now(timezone.utc).isoformat()})
# The checked manifest defines these paths, IDs are generated UUIDs, and no
# browser filesystem is touched. Upload host does the same binary file copy.
for meta,source in zip(snapshot['media'],proof):
 assert str(m.uuid.UUID(meta['id']))==meta['id']
 shutil.copy2(source['source'],m.BACKUPS/'pending'/newid/'browser-media'/meta['id'])
m.native(m.BACKUPS,'backup',{'action':'finish','id':newid})
manifest=m.native(m.BACKUPS,'backup',{'action':'verify','id':newid})
destination=m.OUT/'完整工程备份'/newid
shutil.copytree(m.BACKUPS/newid,destination)
m.native(destination.parent,'backup',{'action':'verify','id':newid})
e=m.read(m.OUT/'migration-package-evidence.json')
e.update(backup_id=newid,backup_directory=str(destination),native_result={'id':newid,'directory':str(m.BACKUPS/newid)},verified=manifest)
m.write(m.OUT/'migration-package-evidence.json',e)
# Verified absolute paths; archive only this task's first candidate directory.
src=(m.BACKUPS/m.BACKUP).resolve();dst=(m.OUT/'migration-source'/'first-backup-not-adopted').resolve()
assert src.parent==m.BACKUPS.resolve() and dst.parent==m.SOURCE.resolve() and not dst.exists()
shutil.move(str(src),str(dst))
print(newid,len(manifest['files']),manifest['bytes'],flush=True)
