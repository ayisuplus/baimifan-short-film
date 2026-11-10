"""Read-only production status; does not submit, cancel, or approve anything."""
import json,urllib.request
from pathlib import Path
P=Path(__file__).resolve().parent
OUT=Path('G:/comfyui/ComfyUI/ComfyUI/output/Baimifan/v034')
def get(route):
 with urllib.request.urlopen('http://127.0.0.1:8188/'+route,timeout=20) as r:return json.load(r)
q=get('queue');running={x[1] for x in q['queue_running']};pending={x[1] for x in q['queue_pending']}
pause=P/'暂停与取消记录.json'
cancelled={x['prompt_id'] for x in json.loads(pause.read_text('utf8'))['cancelled']} if pause.exists() else set()
rows=[]
for f in sorted((P/'receipts').glob('*-submit.json')):
 name=f.name.removesuffix('-submit.json');r=json.loads(f.read_text('utf8'));pid=r['data']['prompt_id']
 job=json.loads((P/'jobs'/f'{name}.json').read_text('utf8'))
 ext='.png' if job['type']=='key' else '.mp4';files=list(OUT.glob(name+'_*'+ext))
 state='running' if pid in running else 'queued' if pid in pending else 'output_ready' if files else 'cancelled' if pid in cancelled else 'inspect'
 row=dict(name=name,type=job['type'],prompt_id=pid,state=state,outputs=[str(x) for x in files])
 if state=='inspect':
  h=get('history/'+pid).get(pid,{});row['status']=h.get('status',{});row['state']='failed' if row['status'].get('status_str')=='error' else 'unknown'
 rows.append(row)
(P/'生产状态.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),'utf8')
counts={s:sum(x['state']==s for x in rows) for s in sorted(set(x['state'] for x in rows))}
print(json.dumps(dict(counts=counts,running=[x['name'] for x in rows if x['state']=='running'],errors=[x for x in rows if x['state'] in ['failed','unknown']]),ensure_ascii=False))
