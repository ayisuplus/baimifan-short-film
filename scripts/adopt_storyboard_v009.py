"""Attach completed independent renders to the v0.9 candidate without touching originals."""
import json,hashlib,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
rec=R/'镜头设计/生成记录/逐镜独立-v009'
jobs=json.loads((rec/'计划.json').read_text(encoding='utf-8'))
outputs=json.loads((rec/'输出归档.json').read_text(encoding='utf-8'))
d=json.loads((R/'镜头设计/shot-plan-v0.9.json').read_text(encoding='utf-8'))
byid={s['id']:s for s in d['shots']}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for j in jobs:
 id=j['id'];o=outputs.get(id)
 if not o or o.get('status')=='rejected':continue
 src=Path(o['original']);dst=R/j['destination']
 if not dst.exists() or sha(dst)!=sha(src):shutil.copy2(src,dst)
 with Image.open(dst) as im:w,h=im.size;im.verify()
 assert 1.7<w/h<1.85,(id,w,h)
 o.update(path=j['destination'],size=[w,h],sha256=sha(dst))
 s=byid[id]
 s.update(panel_index=0,generation_request='镜头设计/生成记录/逐镜独立-v009/'+o['request'])
 for k in ['page_size','panel_region','panel_rect_pixels','display_crop_normalized']:s.pop(k,None)
 s['presentation']=dict(path=j['destination'],role='action',visible=s['action'],status='v0.9独立单镜候选，待作者审阅',missing='连续动作、运镜和声音待视频阶段实现。',show_as_main=True)
 s['refs']=[dict(path=j['destination'],role='本镜独立原画候选'),dict(path=j['source'],role=f"旧分格参考，原第{j['source_panel']+1}格")]+[r for r in s['refs'] if not r['path'].startswith('镜头设计/图像/')]
layout={p['path']:p for p in d['page_layouts']}
for o in outputs.values():
 if o.get('path'):layout[o['path']]=dict(path=o['path'],cols=1,rows=1)
used={s['presentation']['path'] for s in d['shots']}
d['page_layouts']=[layout[p] for p in dict.fromkeys(s['presentation']['path'] for s in d['shots'])]
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']]
 sc.update(path=ss[0]['presentation']['path'],pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)))
(rec/'输出归档.json').write_text(json.dumps(outputs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(R/'镜头设计/shot-plan-v0.9.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(completed=len(outputs),planned=len(jobs),pending=[j['id'] for j in jobs if j['id'] not in outputs]),ensure_ascii=False))
