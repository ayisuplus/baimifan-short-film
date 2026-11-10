"""Execute explicitly prepared reference reductions and repair attempts; preserve all prior attempts."""
import argparse, json, time
from pathlib import Path
import requests
from metaso_h3_v001 import ROOT, BASE, read, save, sha, session, checked

OUT=ROOT/'视频制作/Metaso-H3-v002'
QUEUE=OUT/'执行队列.json'

def upload(s, ref, cache):
    p=ROOT/ref['path']
    assert sha(p)==ref['sha256'], str(p)
    if ref['sha256'] not in cache:
        with p.open('rb') as f:
            receipt=checked(s.post(BASE+'/v1/files/upload',data={'purpose':'video_generation_input'},files={'file':(p.name,f,'application/octet-stream')},timeout=120))
        info=receipt.get('file') or {}
        uri='mm_file://'+str(info['file_id']) if info.get('file_id') else info.get('download_url')
        if not uri: raise RuntimeError('Upload returned no file reference')
        cache[ref['sha256']]={'path':ref['path'],'uri':uri,'receipt':receipt}
        save(OUT/'上传索引.json',cache)
    return cache[ref['sha256']]['uri']

def submit(attempt):
    q=read(QUEUE);b=next(x for x in q['items'] if x['attempt_id']==attempt)
    if b['status']!='prepared':raise RuntimeError('Attempt already submitted/unknown; query first, never duplicate.')
    if sum(x['status']=='running' for x in q['items'])>=4:
        raise RuntimeError('Four tracked tasks are active. Poll original tasks before submitting more.')
    assert b['change_reason'] and len(b['references'])<=9 and len(b['prompt'])<=10000 and 4<=b['duration']<=30
    assert sum(x['estimated_credits'] for x in q['items'])<=q['spending_ceiling_credits']
    # New attempts cannot silently reuse an existing batch without a documented repair reason.
    for prior in ['LibTV-H3-v001/H3节约余量执行队列.json','Metaso-H3-v001/执行队列.json']:
        for old in read(ROOT/'视频制作'/prior)['items']:
            if old['batch_id']==b['batch_id'] and old.get('task_id'):
                assert b.get('repair_of'), 'Existing task needs explicit repair provenance'
    s=session();cache_path=OUT/'上传索引.json'
    fallback=ROOT/'视频制作/Metaso-H3-v002/上传索引.json'
    if not fallback.exists():fallback=ROOT/'视频制作/Metaso-H3-v001/上传索引.json'
    cache=read(cache_path) if cache_path.exists() else read(fallback)
    content=[{'type':'text','text':b['prompt']}]
    for ref in b['references']:
        role=ref.get('role','reference_image')
        assert role in {'reference_image','first_frame','last_frame'}
        content.append({'type':'image_url','image_url':{'url':upload(s,ref,cache)},'role':role})
    payload=dict(model=q['model'],content=content,resolution=q['resolution'],duration=b['duration'],ratio=q['ratio'],fast_mode=False,context_ir_enabled=False)
    if any(r.get('role')=='first_frame' for r in b['references']):
        assert len(b['references'])<=2 and all(r.get('role') in {'first_frame','last_frame'} for r in b['references'])
        payload.pop('ratio')  # Official first-frame mode follows the image aspect ratio.
    save(OUT/(attempt+'-冻结执行.json'),{'batch':b,'payload':payload,'authorization':q['authorization']})
    b.update(status='submitting_outcome_unknown',submit_started=time.strftime('%Y-%m-%dT%H:%M:%S%z'));save(QUEUE,q)
    response=s.post(BASE+'/v2/video_generation',json=payload,timeout=120)
    receipt=response.json();save(OUT/(attempt+'-受理回执.json'),{'http_status':response.status_code,'response':receipt})
    checked(response)
    if not receipt.get('task_id'):raise RuntimeError('No task ID; resolve before any retry')
    b.update(status='running',task_id=str(receipt['task_id']));save(QUEUE,q)
    print(json.dumps({'attempt':attempt,'batch':b['batch_number'],'task_id':b['task_id']},ensure_ascii=False),flush=True)

def poll():
    q=read(QUEUE);s=session()
    for b in q['items']:
        if b['status']!='running':continue
        result=checked(s.get(BASE+'/v2/query/video_generation/'+b['task_id'],timeout=60))
        save(OUT/(b['attempt_id']+'-状态回执.json'),result)
        task=result.get('task') or {};status=str(task.get('status','')).lower();url=(task.get('content') or {}).get('url')
        if url:
            p=OUT/'产物'/(b['attempt_id']+'.mp4');p.parent.mkdir(exist_ok=True)
            if not p.exists():
                r=requests.get(url,timeout=120);r.raise_for_status();tmp=p.with_suffix('.part');tmp.write_bytes(r.content);tmp.replace(p)
            b.update(status='downloaded_candidate',local_path=p.relative_to(ROOT).as_posix(),sha256=sha(p),bytes=p.stat().st_size)
        elif status in {'failed','fail','error','cancelled','canceled','expired'}:b.update(status='failed_provider',error=task.get('error'))
        else:b['provider_status']=status
        save(QUEUE,q);print(json.dumps({'attempt':b['attempt_id'],'status':b['status'],'provider_status':status},ensure_ascii=False),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['submit','poll']);parser.add_argument('--attempt');parser.add_argument('--revision',choices=['v002','v003'],default='v002');a=parser.parse_args()
    OUT=ROOT/('视频制作/Metaso-H3-'+a.revision);QUEUE=OUT/'执行队列.json'
    if a.action=='submit':submit(a.attempt)
    else:poll()
