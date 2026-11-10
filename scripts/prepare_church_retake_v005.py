"""Freeze only individually reviewed pickup shots; never overwrite submitted attempts."""
import json, hashlib, html
from pathlib import Path
R=Path(__file__).resolve().parents[1]
O=R/'视频制作/Metaso-H3-v005'; O.mkdir(exist_ok=True)
Q=O/'执行队列.json'
def read(p): return json.loads(p.read_text(encoding='utf8'))
q=read(Q) if Q.exists() else dict(model='MiniMax-H3',resolution='768P',ratio='16:9',spending_ceiling_credits=1500,authorization='作者已授权：后期优先，不能修复的只补对应镜头，Metaso H3延续；本轮教堂至Kimi段修复，非整批重做。',items=[])
existing={x['attempt_id'] for x in q['items']}
for p in sorted((R/'后期/声画重构-v002').glob('补拍输入*.json')):
    obj=read(p); rows=obj if isinstance(obj,list) else obj['items']
    for row in rows:
        aid=row.get('attempt_id') or f"{row['batch_id']}-v005-{row['shot_ids'][0]}-r1"
        if aid in existing: continue
        refs=[]
        for ref in row['references']:
            path=Path(ref['path']); path=path if path.is_absolute() else R/path
            assert path.exists(),str(path)
            refs.append({**ref,'purpose':ref.get('purpose',ref.get('role','reference_image')),'role':ref.get('role') if ref.get('role') in ('first_frame','last_frame') else 'reference_image','path':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        import re
        row['prompt']=re.sub('『([^』]+)』',r'<d>[Japanese] \1</d>',row['prompt'])
        q['items'].append({**row,'attempt_id':aid,'references':refs,'estimated_credits':round(row['duration']*10.2+max(0,len(refs)-5)*5.7,1),'repair_of':row.get('repair_of','导演后期修正-v001现行剪辑对应镜头'),'status':'prepared'})
        existing.add(aid)
assert sum(x['estimated_credits'] for x in q['items'])<=q['spending_ceiling_credits']
Q.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8')
parts=['<!doctype html><meta charset="utf-8"><title>教堂段单镜补拍输入</title><style>body{background:#141820;color:#eee;font:17px/1.65 system-ui;max-width:1100px;margin:auto;padding:30px}img{max-width:32%;max-height:280px}pre{white-space:pre-wrap}article{padding:24px;border-bottom:1px solid #666}</style><h1>教堂段单镜补拍输入 v005</h1><p>按作者授权执行。只替换列明镜头，原片保留。参考身份与构图职责分开；生成回片须审查后装配。</p>']
for x in q['items']:
    parts.append(f'<article><h2>第{x["batch_number"]}批 · {html.escape(" / ".join(x["shot_ids"]))}</h2><p>{html.escape(x["change_reason"])} · {x["duration"]}秒 · 预计{x["estimated_credits"]}积分</p>')
    for ref in x['references']:
        import os
        rel=os.path.relpath(R/ref['path'],O).replace('\\','/')
        parts.append(f'<img src="{html.escape(rel)}" title="{html.escape(ref.get("purpose",ref.get("role","参考")))}">')
    parts.append('<pre>'+html.escape(x['prompt'])+'</pre></article>')
(O/'补拍输入.html').write_text(''.join(parts),encoding='utf8')
print(json.dumps({'items':len(q['items']),'estimate':sum(x['estimated_credits'] for x in q['items']),'prepared':[x['attempt_id'] for x in q['items'] if x['status']=='prepared']},ensure_ascii=False))
