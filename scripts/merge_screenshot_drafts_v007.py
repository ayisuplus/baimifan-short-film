from pathlib import Path
import json,hashlib,html
R=Path(__file__).resolve().parents[1];G=R/'视频制作/Metaso-H3-v007';O=R/'后期/截图定点修正-v004'
q=json.loads((G/'执行队列.json').read_text(encoding='utf8'));ids={x['attempt_id'] for x in q['items']};added=[]
for name in ['前段补拍草案.json','后段补拍草案.json']:
 d=json.loads((O/name).read_text(encoding='utf8'))
 for x in d['items']:
  assert x['attempt_id'] not in ids
  for r in x['references']:
   assert hashlib.sha256((R/r['path']).read_bytes()).hexdigest()==r['sha256']
  x['status']='prepared';q['items'].append(x);added.append(x)
assert sum(x['estimated_credits'] for x in q['items'])<=q['spending_ceiling_credits']
(G/'执行队列.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8')
with (G/'补拍输入.html').open('a',encoding='utf8') as f:
 for x in added:f.write('<article><h2>'+x['attempt_id']+'</h2><p>'+str(x['duration'])+'秒，预计'+str(x['estimated_credits'])+'积分</p><ul>'+''.join('<li>'+html.escape(r['role']+': '+r['path'])+'</li>' for r in x['references'])+'</ul><pre>'+html.escape(x['prompt'])+'</pre></article>')
print(json.dumps(dict(added=[x['attempt_id'] for x in added],estimate=sum(x['estimated_credits'] for x in q['items'])),ensure_ascii=False))
