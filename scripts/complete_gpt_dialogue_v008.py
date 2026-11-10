"""Fill nine missing lines using the author's saved v004 voice. No automatic retry."""
from pathlib import Path
import json, hashlib, urllib.request, urllib.error, subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '声音/缺口补齐-v008'
voice = json.loads((OUT / 'GPT-声线注册.json').read_text(encoding='utf8'))
assert voice['status'] == 'registered'
manifest = json.loads((ROOT / '声音/逐句切分审阅-v007/切分清单.json').read_text(encoding='utf8'))
lines = [x for x in manifest['missing_lines'] if x['role'] == 'GPT']
assert len(lines) == 9
keyfile = Path.home() / '.codex/local/content-tools/elevenlabs/.env.local'
key = next(x.split('=',1)[1].strip().strip('"').strip("'") for x in keyfile.read_text(encoding='utf-8-sig').splitlines() if x.strip().startswith('ELEVENLABS_API_KEY='))
for line in lines:
    receipt = OUT / (line['id'] + '-结果.json')
    if receipt.exists():
        saved = json.loads(receipt.read_text(encoding='utf8'))
        assert saved['status'] == 'saved_pending_review', 'Uncertain/rejected attempt: inspect before proceeding'
        continue
    body = {'text':line['tts_reading_text'], 'model_id':'eleven_multilingual_v2', 'language_code':'ja'}
    meta = {'line_id':line['id'], 'role':line['role'], 'line':line, 'voice_id':voice['voice_id'], 'voice_source':'selected v004 candidate 1', 'body':body, 'status':'outcome_unknown_do_not_repeat', 'author_performance_accepted':False}
    receipt.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/'+voice['voice_id'],data=json.dumps(body,ensure_ascii=False).encode(),headers={'xi-api-key':key,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=60) as response:
            data=response.read()
            assert 'audio' in response.headers.get('Content-Type','')
            meta.update(request_id=response.headers.get('request-id'),character_cost_header=response.headers.get('character-cost'))
    except urllib.error.HTTPError as e:
        meta.update(status='api_rejected',http_status=e.code,error=e.read().decode('utf8',errors='replace'))
        receipt.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
        raise
    path=OUT/(line['id']+'__GPT.mp3');path.write_bytes(data)
    probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(path)],capture_output=True,check=True)
    meta.update(status='saved_pending_review',file=path.relative_to(ROOT).as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),media=json.loads(probe.stdout))
    meta['decode_ok']=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],capture_output=True).returncode==0
    receipt.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'id':line['id'],'status':meta['status'],'seconds':meta['media']['format']['duration']},ensure_ascii=False),flush=True)
