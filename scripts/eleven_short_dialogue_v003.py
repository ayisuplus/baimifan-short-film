"""One-shot short lines with official existing voices; immutable attempt receipts."""
from pathlib import Path
import json, hashlib, urllib.request, urllib.error, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '声音/ElevenLabs-正式台词试听-v003'
CAST = {
    '千问': ('4lOQ7A2l7HPuG7UIHiKA', 'Kyoko - Warm, Clear and Natural'),
    'Gemini': ('fUjY9K2nAIwlALOwSiwc', 'Yui - Warm, Clear and Natural'),
    'Grok': ('8EkOjt4xTPGMclNlh1pk', 'Morioki - Calm, Measured and Muffled'),
    '天使GPT': ('WQz3clzUdMqvBf0jswZQ', 'Shizuka - Natural and Soft'),
    '恶魔GPT': ('T7yYq3WpB94yAuOXraRi', 'Konoha - Professional JP Explainer'),
}
keyfile = Path.home() / '.codex/local/content-tools/elevenlabs/.env.local'
key = next(x.split('=', 1)[1].strip().strip('"').strip("'") for x in keyfile.read_text(encoding='utf-8-sig').splitlines() if x.strip().startswith('ELEVENLABS_API_KEY='))
source = json.loads((ROOT / '剧本/白米饭-日语对白-v0.69.json').read_text(encoding='utf8'))
for role in sys.argv[1:]:
    voice, name = CAST[role]
    lines = [x for x in source['lines'] if x['role'] == role and x.get('ja') and x['status'] not in ['merged_not_spoken', 'removed_not_spoken', 'removed_from_draft']]
    for line in lines:
        prefix = f'{role}-{line["id"]}'
        receipt = OUT / f'{prefix}-结果.json'
        assert not receipt.exists(), 'Existing attempt: inspect, never auto repeat.'
        body = {'text': line['ja'], 'model_id': 'eleven_multilingual_v2', 'language_code': 'ja'}
        meta = {'role': role, 'line': line, 'voice_id': voice, 'voice_name': name, 'body': body, 'status': 'outcome_unknown_do_not_repeat', 'adopted': False}
        receipt.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf8')
        request = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{voice}', data=json.dumps(body, ensure_ascii=False).encode(), headers={'xi-api-key': key, 'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = response.read()
                assert 'audio' in response.headers.get('Content-Type', '')
                meta['request_id'] = response.headers.get('request-id')
                meta['character_cost_header'] = response.headers.get('character-cost')
        except urllib.error.HTTPError as error:
            meta['status'] = 'api_rejected'; meta['http_status'] = error.code; meta['error'] = error.read().decode('utf8', errors='replace')
            receipt.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf8')
            print(json.dumps(meta, ensure_ascii=False)); sys.exit(2)
        path = OUT / f'{prefix}.mp3'; path.write_bytes(data)
        meta.update(status='saved_pending_review', file=path.name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(path)], capture_output=True, check=True)
        meta['media'] = json.loads(probe.stdout)
        meta['decode_ok'] = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'null', '-'], capture_output=True).returncode == 0
        receipt.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf8')
        print(json.dumps({'role': role, 'line_id': line['id'], 'status': meta['status'], 'seconds': meta['media']['format']['duration']}, ensure_ascii=False))
