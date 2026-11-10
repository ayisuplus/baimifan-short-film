"""Append reviewed, targeted repairs; never mutate an existing frozen attempt."""
from pathlib import Path
import json,hashlib,copy,shutil,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'视频制作/Metaso-H3-v002'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
q=read(OUT/'执行队列.json');existing={b['attempt_id'] for b in q['items']}
def add(b):
 if b['attempt_id'] in existing:return
 for r in b['references']:
  p=ROOT/r['path'];assert p.exists();r['sha256']=sha(p)
 assert len(b['references'])<=9 and len(b['prompt'])<=10000
 b.update(status='prepared',accepted=False,estimated_credits=round(b['duration']*10.2+max(0,len(b['references'])-5)*5.7,2))
 q['items'].append(b);existing.add(b['attempt_id'])
for b in read(OUT/'合扇单镜返修-r003-准备.json'):add(b)
d=read(OUT/'新增问题返修-准备.json')
for j in d['jobs']:
 old=next(x for x in q['items'] if x['attempt_id']==j['source_attempt_id'])
 shot=j['prepared_id'].split('-')[1]
 add(dict(batch_number=old['batch_number'],batch_id=old['batch_id'],attempt_id=old['batch_id']+'-r002-'+shot,title=old['title'],shot_ids=[shot],
  film_start=j['target_film_in'],part_offset=j['target_batch_in'],used_seconds=round(j['target_batch_out']-j['target_batch_in'],6),duration=j['request_seconds'],
  prompt=j['prompt'],references=j['references'],change_reason='独立回片复核明确缺陷：'+j['prepared_id'],repair_of={'attempt_id':old['attempt_id'],'task_id':old['task_id'],'local_path':old['local_path']},source='新增问题返修-准备.json'))
# Keep all three image edits, but only regenerate failed shots (31 part1 already passed).
folder=OUT/'修订参考';folder.mkdir(exist_ok=True)
base=Path.home()/'.codex/generated_images/01a17883-69dd-74f1-8f13-bbde7422c943'
files={'CY024A7':'exec-5668ec3d-8ddf-47cb-b239-c47e761a1387.png','CY024A5':'exec-4e6f67a9-b337-469b-a085-c549fff312ca.png','CY024A5B':'exec-e9b62285-f535-4e8f-aff5-da16e1244498.png'}
for name,file in files.items():
 p=folder/(name+'-纯流体-r003.png')
 if not p.exists():shutil.copy2(base/file,p)
for oldid,name,newid in [('GB020-2-r002','CY024A7','GB020-2-r003'),('GB022-1-r002-part2','CY024A5B','GB022-1-r003-part2')]:
 old=next(x for x in q['items'] if x['attempt_id']==oldid);b=copy.deepcopy(old)
 for k in ['task_id','local_path','sha256','bytes','submit_started','provider_status']:b.pop(k,None)
 b['attempt_id']=newid;b['repair_of']={k:old[k] for k in ['attempt_id','task_id','local_path']}
 ref=b['references'][-1];ref['path']=(folder/(name+'-纯流体-r003.png')).relative_to(ROOT).as_posix()
 b['change_reason']='r002实体鳞片/固定亮眼未修正，已局部修改源参考为无眼球、无鳞片的连续流体。'
 b['prompt']='本轮最高优先：严格保持最后一张参考中新修的水体材质。它是龙形巨浪而不是蓝色动物；只有连续透明水流、折射、泡沫，无鳞片格纹、皮肤、冰、眼球或眼部亮点。流向改变时仍无固定的脸部眼点。\n'+b['prompt']
 if name=='CY024A5B':
  # Give the editor a full gesture with handles; no later shot timing changes.
  b['prompt']='单镜4秒，前1.5秒完整完成发令：0秒GPT双手已经开始解开手印；0–0.3秒右手前伸，0.3–0.8秒食指明确向前指，0.8–1.5秒水流随之向前响应。1.5–4秒仅保持指向与水流，不再重复发令，无对白。\n'+b['prompt']
 add(b)
q['estimated_total_credits']=round(sum(x['estimated_credits'] for x in q['items']),2)
assert q['estimated_total_credits']<=q['spending_ceiling_credits']
save(OUT/'执行队列.json',q)
print(json.dumps({'planned_tasks':len(q['items']),'estimated_total':q['estimated_total_credits'],'prepared':[x['attempt_id'] for x in q['items'] if x['status']=='prepared']}))
