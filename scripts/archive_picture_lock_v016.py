import json,hashlib,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=root/'镜头设计/shot-plan-v0.16.json'
d=json.loads(manifest.read_text(encoding='utf8'))
assert len(d['shots'])==91 and sum(s['seconds'] for s in d['shots'])==292
pairs=[('镜头设计/带图分镜.html','镜头设计/带图分镜-画面定稿-v0.16.html'),('镜头设计/shot-plan-v0.16.json','镜头设计/shot-plan-画面定稿-v0.16.json')]
for src,dst in pairs:
 target=root/dst
 if not target.exists():shutil.copy2(root/src,target)
 assert sha(root/src)==sha(target),dst
shots=[]
for s in d['shots']:
 p=root/s['presentation']['path']
 assert p.is_file(),p
 shots.append(dict(id=s['id'],path=s['presentation']['path'],seconds=s['seconds'],sha256=sha(p),generation_request=s.get('generation_request')))
docs=[dst for _,dst in pairs]+[d['story_script'],'资产/assets.json','资产/资产图册.html','镜头设计/生成记录/交付核验-v016.json','镜头设计/生成记录/生成索引-v016.json']
result=dict(project='穿云',version='v0.16',approved_on='2026-10-22',approval_quote='OK，画面收工。记录存档一下，然后呢，这个对话的使命已经结束了',status='author_approved_picture_lock',scope='静帧画面封版；动态与正式声音不在验收范围',source_commit='d048aea',shot_count=91,total_seconds=292,shots=shots,documents=[dict(path=p,sha256=sha(root/p)) for p in docs],media_backup='Existing local media preserved in place; no remote backup performed')
out=root/'归档/画面封版-v016-20261022.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Picture lock archived: 91 images verified; 292 seconds; snapshots match sources.')
