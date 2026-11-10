"""Explicit one-shot Voice Design via the installed official CLI; never auto-retry."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '声音/ElevenLabs-声线试听-v001'
KEY_FILE = Path.home() / '.codex/local/content-tools/elevenlabs/.env.local'


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def run(candidate):
    request = OUT / f'{candidate}-输入.json'
    receipt = OUT / f'{candidate}-结果.json'
    assert request.exists() and not receipt.exists(), 'Missing input or existing/unknown attempt: do not repeat.'
    body = json.loads(request.read_text(encoding='utf8'))
    assert 100 <= len(body['text']) <= 1000
    env = os.environ.copy()
    for line in KEY_FILE.read_text(encoding='utf-8-sig').splitlines():
        if line.strip().startswith('ELEVENLABS_API_KEY='):
            env['ELEVENLABS_API_KEY'] = line.split('=', 1)[1].strip().strip('"').strip("'")
    assert env.get('ELEVENLABS_API_KEY')
    env['ELEVENLABS_TIMEOUT_SECS'] = '120'
    save(receipt, {'status': 'submission_outcome_unknown', 'request': request.name})
    args = ['npx.cmd', '--offline', '@elevenlabs/cli@1.7.1', 'text-to-voice', 'design',
            '--json', '-', '--output-format', 'mp3_44100_128', '--format', 'json', '--no-retry']
    try:
        result = subprocess.run(args, input=json.dumps(body, ensure_ascii=False).encode('utf8'),
                                cwd=ROOT, env=env, capture_output=True, timeout=150)
    except subprocess.TimeoutExpired:
        print(json.dumps({'candidate': candidate, 'status': 'unknown_timeout_do_not_retry'}))
        return
    if result.returncode:
        error = (result.stderr or result.stdout).decode('utf8', errors='replace')
        error = error.replace(env['ELEVENLABS_API_KEY'], '[REDACTED]')
        save(receipt, {'status': 'cli_error_do_not_retry_automatically', 'returncode': result.returncode, 'error': error})
        print(json.dumps({'candidate': candidate, 'status': 'cli_error', 'error': error[:1200]}, ensure_ascii=False))
        return
    response = json.loads(result.stdout)
    previews = response.get('previews', [])
    assert previews, 'No previews: inspect response before any repeat request.'
    items = []
    for i, item in enumerate(previews, 1):
        data = base64.b64decode(item['audio_base_64'])
        output = OUT / f'{candidate}-{i}.mp3'
        output.write_bytes(data)
        items.append({k: v for k, v in item.items() if k != 'audio_base_64'} |
                     {'path': output.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(data).hexdigest(),
                      'bytes': len(data), 'adopted': False})
    save(receipt, {'status': 'preview_candidates_saved_not_registered', 'text': response.get('text'), 'previews': items})
    print(json.dumps({'candidate': candidate, 'status': 'saved', 'previews': len(items)}, ensure_ascii=False))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('candidate')
    run(p.parse_args().candidate)
