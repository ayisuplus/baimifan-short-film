import json,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
records=json.loads((root/'镜头设计/生成记录/天瀑空间-v014/结果映射.json').read_text(encoding='utf-8'))
for r in records:
 p=root/r['destination'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(r['original'],p)
print('Archived',len(records),'outputs')
