"""Resume the approved H3 queue through Metaso's documented API. No automatic retries."""
from pathlib import Path
import argparse, hashlib, json, os, re, time
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '视频制作/Metaso-H3-v001'
SOURCE = ROOT / '视频制作/LibTV-H3-v001/H3节约余量执行队列.json'
BASE = 'https://metaso.cn/api/minimax'
KEY_FILE = Path.home() / '.codex/credentials/metaso-h3.key'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def session():
    key = os.environ.get('METASO_H3_API_KEY') or KEY_FILE.read_text().strip()
    s = requests.Session()
    s.headers['Authorization'] = 'Bearer ' + key
    return s

def checked(response):
    # Do not expose request headers, signed URLs, or credentials in console errors.
    result = response.json()
    if response.status_code >= 400 or (result.get('base_resp') or {}).get('status_code', 0):
        message = json.dumps(result, ensure_ascii=False)
        raise RuntimeError(f'HTTP {response.status_code}: ' + re.sub(r'mk-[A-Za-z0-9_-]+', '[REDACTED]', message))
    return result

def prepare():
    path = OUT / '执行队列.json'
    if path.exists():
        return read(path)
    items = []
    for b in read(SOURCE)['items']:
        if b['status'] != 'prepared_not_submitted':
            continue
        assert not b.get('task_id') and 1 <= len(b['references']) <= 9
        for ref in b['references']:
            assert sha(ROOT / ref['path']) == ref['sha256'], ref['path']
        prompt = re.sub(r'<Picture (\d+)>', r'Image \1', b['prompt'])
        assert len(prompt) <= 10000 and 4 <= b['duration'] <= 15
        estimate = round(b['duration'] * 10.2 + max(0, len(b['references']) - 5) * 5.7, 2)
        items.append(dict(batch_number=b['batch_number'], batch_id=b['batch_id'], title=b['title'],
                          shot_ids=b['shot_ids'], film_start=b['film_start'], duration=b['duration'],
                          prompt=prompt, references=b['references'], estimated_credits=estimate,
                          status='prepared', accepted=False))
    q = dict(provider='metaso', base_url=BASE, model='MiniMax-H3', resolution='768P', ratio='16:9',
             fast_mode=False, context_ir_enabled=False, observed_initial_balance=10270.7,
             estimated_total_credits=round(sum(b['estimated_credits'] for b in items), 2),
             authorization='2026-10-28 user requested switching remaining generation to https://metaso.cn/minimax-h3',
             source=str(SOURCE.relative_to(ROOT)), items=items)
    assert len(items) == 7 and q['estimated_total_credits'] == 755.1
    save(path, q)
    return q

def submit(number):
    q = prepare()
    b = next(x for x in q['items'] if x['batch_number'] == number)
    if b['status'] != 'prepared':
        raise RuntimeError('Already submitted or outcome unknown; query the existing task, do not retry.')
    prior = next(x for x in read(SOURCE)['items'] if x['batch_id'] == b['batch_id'])
    assert prior['status'] == 'prepared_not_submitted' and not prior.get('task_id')
    s = session()
    cache_path = OUT / '上传索引.json'
    cache = read(cache_path) if cache_path.exists() else {}
    content = [{'type': 'text', 'text': b['prompt']}]
    for ref in b['references']:
        path = ROOT / ref['path']
        assert sha(path) == ref['sha256']
        if ref['sha256'] not in cache:
            with path.open('rb') as f:
                receipt = checked(s.post(BASE + '/v1/files/upload', data={'purpose':'video_generation_input'},
                                      files={'file':(path.name, f, 'application/octet-stream')}, timeout=120))
            info = receipt.get('file') or {}
            uri = ('mm_file://' + str(info['file_id'])) if info.get('file_id') else info.get('download_url')
            if not uri:
                raise RuntimeError('Upload returned no file reference')
            cache[ref['sha256']] = dict(path=ref['path'], uri=uri, receipt=receipt)
            save(cache_path, cache)
        content.append({'type':'image_url', 'image_url':{'url':cache[ref['sha256']]['uri']}, 'role':'reference_image'})
    payload = dict(model=q['model'], content=content, resolution=q['resolution'], duration=b['duration'],
                   ratio=q['ratio'], fast_mode=False, context_ir_enabled=False)
    frozen = dict(batch=b, payload=payload, source_sha256=sha(SOURCE), approved_scope=q['authorization'])
    save(OUT / (b['batch_id'] + '-冻结执行.json'), frozen)
    b.update(status='submitting_outcome_unknown', submit_started=time.strftime('%Y-%m-%dT%H:%M:%S%z'))
    save(OUT / '执行队列.json', q)
    response = s.post(BASE + '/v2/video_generation', json=payload, timeout=120)
    receipt = response.json()
    save(OUT / (b['batch_id'] + '-受理回执.json'), dict(http_status=response.status_code, response=receipt))
    checked(response)
    if not receipt.get('task_id'):
        raise RuntimeError('No task ID; resolve outcome before retrying')
    b.update(status='running', task_id=str(receipt['task_id']))
    save(OUT / '执行队列.json', q)
    print(json.dumps({'batch':number, 'task_id':b['task_id'], 'status':'running', 'estimate':b['estimated_credits']}))

def poll():
    q = prepare()
    s = session()
    for b in q['items']:
        if b['status'] != 'running':
            continue
        result = checked(s.get(BASE + '/v2/query/video_generation/' + b['task_id'], timeout=60))
        save(OUT / (b['batch_id'] + '-状态回执.json'), result)
        task = result.get('task') or {}
        status = str(task.get('status', '')).lower()
        url = (task.get('content') or {}).get('url')
        if url:
            path = OUT / '产物' / (b['batch_id'] + '-Metaso-H3-v001.mp4')
            path.parent.mkdir(exist_ok=True)
            if not path.exists():
                # Never send the API Authorization header to a media CDN.
                r = requests.get(url, timeout=120)
                r.raise_for_status()
                tmp = path.with_suffix('.part')
                tmp.write_bytes(r.content)
                tmp.replace(path)
            b.update(status='downloaded_candidate', local_path=str(path.relative_to(ROOT)), sha256=sha(path), bytes=path.stat().st_size)
        elif status in {'failed','fail','error','cancelled','canceled','expired'}:
            b.update(status='failed_provider', error=task.get('error'))
        else:
            b['provider_status'] = status
        save(OUT / '执行队列.json', q)
        print(json.dumps({'batch':b['batch_number'],'status':b['status'],'provider_status':status},ensure_ascii=False))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare','submit','poll'])
    parser.add_argument('--batch', type=int)
    args = parser.parse_args()
    if args.action == 'prepare':
        q = prepare(); print(json.dumps({'batches':len(q['items']),'estimated_credits':q['estimated_total_credits']}))
    elif args.action == 'submit':
        submit(args.batch)
    else:
        poll()
