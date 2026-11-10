from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'视频制作/LibTV-H3-v001'
p=OUT/'H3节约余量执行队列.json'
q=json.loads(p.read_text(encoding='utf-8'))
nodes={n['id']:n for n in json.loads((OUT/'最终画布回读.json').read_text(encoding='utf-8'))}
for b in q['items']:
 n=nodes.get(b.get('node_id'));t=n['data'].get('taskInfo',{}) if n else {}
 if t.get('status')==3:
  b.update(status='failed_provider_review' if '审核' in t.get('failedReason','') else 'failed_provider',failure=t.get('failedReason','平台任务失败'),task_id=t['taskId'],retry='保留原失败回执，不自动重试')
  (OUT/(b['batch_id']+'-失败回执.json')).write_text(json.dumps(n,ensure_ascii=False,indent=2),encoding='utf-8')
p.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
print('failed',[(b['batch_number'],b.get('failure')) for b in q['items'] if b['status'].startswith('failed')])
