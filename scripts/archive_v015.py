import json,shutil,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
r=json.loads((root/'镜头设计/生成记录/动作收尾-v015/结果映射.json').read_text(encoding='utf8'))
a=[]
for j in r:
 p=root/j['destination'];p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():shutil.copy2(j['original'],p)
 h=hashlib.sha256(p.read_bytes()).hexdigest()
 assert h==hashlib.sha256(Path(j['original']).read_bytes()).hexdigest()
 a.append(dict(id=j['id'],take=j['take'],path=j['destination'],sha256=h,original=j['original']))
(root/'镜头设计/生成记录/动作收尾-v015/归档校验.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Archived and verified',len(a))
