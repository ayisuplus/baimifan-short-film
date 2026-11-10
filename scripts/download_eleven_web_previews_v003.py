"""Download already generated official previews; never synthesize or retry generation."""
from pathlib import Path
import json, hashlib, urllib.request, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ('声音/声线返修试听-v004' if '--v004' in sys.argv else '声音/ElevenLabs-正式台词试听-v003')
role = sys.argv[1]
web = json.loads((OUT / f'{role}-网页结果.json').read_text(encoding='utf8'))
assert len(web['previews']) == 3
keyfile = Path.home() / '.codex/local/content-tools/elevenlabs/.env.local'
key = next(x.split('=', 1)[1].strip().strip('"').strip("'") for x in keyfile.read_text(encoding='utf-8-sig').splitlines() if x.strip().startswith('ELEVENLABS_API_KEY='))
items = []
for i, preview in enumerate(web['previews'], 1):
    vid = preview['id']
    assert vid.isalnum()
    path = OUT / f'{role}-{i}.mp3'
    if not path.exists():
        request = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-voice/{vid}/stream', headers={'xi-api-key': key})
        with urllib.request.urlopen(request, timeout=40) as response:
            assert 'audio' in response.headers.get('Content-Type', '')
            data = response.read()
        assert len(data) > 1000
        path.write_bytes(data)
    data = path.read_bytes()
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_name,sample_rate,channels', '-of', 'json', str(path)], capture_output=True, check=True)
    decoded = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'null', '-'], capture_output=True)
    items.append({'candidate': i, 'generated_voice_id': vid, 'file': path.name, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data), 'media': json.loads(probe.stdout), 'decode_ok': decoded.returncode == 0, 'adopted': False})
receipt = {'role': role, 'status': 'saved_pending_author_selection', 'input': f'{role}-输入.json', 'generation_route': 'web_voice_design', 'download_route': 'official_existing_preview_GET', 'registered': False, 'listening_approved': False, 'previews': items}
(OUT / f'{role}-结果.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps({'role': role, 'saved': len(items), 'durations': [round(float(x['media']['format']['duration']), 2) for x in items], 'decode_ok': all(x['decode_ok'] for x in items)}, ensure_ascii=False))
