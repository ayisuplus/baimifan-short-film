"""Targeted dramatic retakes with real selected audio references; never auto-retry."""
import argparse,json,time,mimetypes
from pathlib import Path
import metaso_h3_v002 as old
from metaso_h3_v001 import ROOT,BASE,read,save,sha,session,checked
OUT=ROOT/'视频制作/Metaso-H3-v006';QUEUE=OUT/'执行队列.json'
def submit(aid):
 q=read(QUEUE);b=next(x for x in q['items'] if x['attempt_id']==aid)
 assert b['status']=='prepared'
 assert sum(x['status']=='running' for x in q['items'])<4
 assert sum(x['estimated_credits'] for x in q['items'])<=q['spending_ceiling_credits']
 assert 4<=b['duration']<=15 and len(b['prompt'])<10000
 refs=b['references']; assert sum(x['role']=='reference_image' for x in refs)<=9
 assert sum(x.get('seconds',0) for x in refs if x['role']=='reference_audio')<=15
 s=session();cache=read(OUT/'上传索引.json') if (OUT/'上传索引.json').exists() else read(ROOT/'视频制作/Metaso-H3-v005/上传索引.json')
 content=[{'type':'text','text':b['prompt']}]
 for ref in refs:
  p=ROOT/ref['path'];assert sha(p)==ref['sha256']
  if ref['sha256'] not in cache:
   with p.open('rb') as f:r=checked(s.post(BASE+'/v1/files/upload',data={'purpose':'video_generation_input'},files={'file':(p.name,f,mimetypes.guess_type(p.name)[0] or 'application/octet-stream')},timeout=120))
   info=r.get('file') or {};uri='mm_file://'+str(info['file_id']) if info.get('file_id') else info.get('download_url');assert uri
   cache[ref['sha256']]={'path':ref['path'],'uri':uri,'receipt':r};save(OUT/'上传索引.json',cache)
  kind='audio_url' if ref['role']=='reference_audio' else 'image_url'
  content.append({'type':kind,kind:{'url':cache[ref['sha256']]['uri']},'role':ref['role']})
 payload={'model':'MiniMax-H3','content':content,'resolution':'768P','duration':b['duration'],'ratio':'16:9','fast_mode':False,'context_ir_enabled':False}
 if any(r['role']=='first_frame' for r in refs):
  assert len(refs)<=2 and all(r['role'] in ['first_frame','last_frame'] for r in refs)
  payload.pop('ratio')
 save(OUT/(aid+'-冻结执行.json'),{'batch':b,'payload':payload,'authorization':q['authorization']})
 b.update(status='submitting_outcome_unknown',submit_started=time.strftime('%Y-%m-%dT%H:%M:%S%z'));save(QUEUE,q)
 r=s.post(BASE+'/v2/video_generation',json=payload,timeout=120);receipt=r.json();save(OUT/(aid+'-受理回执.json'),{'http_status':r.status_code,'response':receipt});checked(r)
 assert receipt.get('task_id');b.update(status='running',task_id=str(receipt['task_id']));save(QUEUE,q)
 print(json.dumps({'attempt':aid,'task_id':b['task_id'],'estimate':b['estimated_credits']},ensure_ascii=False))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('action',choices=['submit','poll']);a.add_argument('--attempt');a=a.parse_args()
 old.OUT=OUT;old.QUEUE=QUEUE
 if a.action=='poll':old.poll()
 else:submit(a.attempt)
