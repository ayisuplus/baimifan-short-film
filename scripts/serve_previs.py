"""Local storyboard server with byte ranges for audio scrubbing."""
import argparse
import functools
import json
import os
import re
import threading
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

CHOICE_LOCK = threading.Lock()


class PrevisHandler(SimpleHTTPRequestHandler):
    server_version = 'PrevisHTTP/1.0'

    def __init__(self, *args, choices_file=None, **kwargs):
        self.choices_file = Path(choices_file)
        super().__init__(*args, **kwargs)

    def _json(self, status, value):
        body = json.dumps(value, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_choices(self):
        if not self.choices_file.exists():
            return {'schema': 1, 'cue_choices': {}, 'group_choices': {}}
        data = json.loads(self.choices_file.read_text(encoding='utf-8-sig'))
        if data.get('schema') != 1 or not isinstance(data.get('cue_choices'), dict) or not isinstance(data.get('group_choices'), dict):
            raise ValueError('选择记录格式不正确；原文件未修改')
        return data

    def do_GET(self):
        if urlsplit(self.path).path == '/api/voice-choices-v022':
            try:
                with CHOICE_LOCK:
                    data = self._read_choices()
                self._json(200, data)
            except (OSError, ValueError, json.JSONDecodeError) as e:
                self._json(500, {'error': str(e)})
            return
        return super().do_GET()

    def do_POST(self):
        if urlsplit(self.path).path != '/api/voice-choices-v022':
            self.send_error(404)
            return
        host = self.headers.get('Host', '')
        origin = self.headers.get('Origin', '')
        if host != f'127.0.0.1:{self.server.server_port}' or origin != f'http://{host}':
            self._json(403, {'error': '只接受本机预演页的同源请求'})
            return
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if size <= 0 or size > 4096 or self.headers.get_content_type() != 'application/json':
                raise ValueError('请求格式无效')
            req = json.loads(self.rfile.read(size).decode('utf-8'))
            kind, key, option_id = req.get('kind'), req.get('key'), req.get('option_id')
            if kind not in ('cue', 'group') or not isinstance(key, str) or (option_id is not None and not isinstance(option_id, str)):
                raise ValueError('选择格式无效')
            manifest = json.loads((Path(self.directory) / '后期/配音挑选-v022/候选索引.json').read_text('utf-8'))
            items = manifest['cues'] if kind == 'cue' else manifest['groups']
            item = next((v for v in items if v['id'] == key), None)
            if item is None:
                raise ValueError('未知对白或连续段落')
            option = next((v for v in item['options'] if v['id'] == option_id), None) if option_id else None
            if option_id and (option is None or not option.get('selectable', False)):
                raise ValueError('候选不可选或已经变化')
            with CHOICE_LOCK:
                data = self._read_choices()
                bucket = data['cue_choices' if kind == 'cue' else 'group_choices']
                if option is None:
                    bucket.pop(key, None)
                else:
                    bucket[key] = {'option_id': option['id'], 'path': option['path'], 'sha256': option['sha256'],
                                   'label': option['label'], 'chosen_at': datetime.now(timezone.utc).isoformat()}
                self.choices_file.parent.mkdir(parents=True, exist_ok=True)
                tmp = self.choices_file.with_name(self.choices_file.name + '.tmp')
                tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                os.replace(tmp, self.choices_file)
            self._json(200, data)
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as e:
            self._json(400, {'error': str(e)})

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def send_head(self):
        self.range_remaining = None
        path = Path(self.translate_path(self.path))
        requested = self.headers.get('Range')
        if not requested or not path.is_file() or self.headers.get('If-Range'):
            return super().send_head()
        f = path.open('rb')
        size = path.stat().st_size
        match = re.fullmatch(r'bytes=(\d*)-(\d*)', requested.strip())
        start, end = 0, size - 1
        valid = bool(match and size)
        if valid:
            left, right = match.groups()
            if not left:
                suffix = int(right or 0)
                valid = suffix > 0
                start = max(0, size - suffix)
            else:
                start = int(left)
                end = min(size - 1, int(right)) if right else size - 1
                valid = start <= end and start < size
        if not valid:
            f.close()
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return None
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(str(path)))
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.send_header('Last-Modified', self.date_time_string(path.stat().st_mtime))
        self.end_headers()
        f.seek(start)
        self.range_remaining = end - start + 1
        return f

    def copyfile(self, source, outputfile):
        try:
            if self.range_remaining is None:
                return super().copyfile(source, outputfile)
            remaining = self.range_remaining
            while remaining:
                block = source.read(min(65536, remaining))
                if not block:
                    break
                outputfile.write(block)
                remaining -= len(block)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass  # Normal when the listener seeks or switches tracks.


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--port', type=int, default=8965)
    parser.add_argument('--voice-choices', type=Path, help='Optional isolated choice file, useful for testing')
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root/'镜头设计/带图分镜.html').is_file():
        parser.error('Expected the storyboard project root')
    choices = args.voice_choices or (root/'后期/配音挑选-v022/作者选择.json')
    handler = functools.partial(PrevisHandler, directory=str(root), choices_file=choices)
    with ThreadingHTTPServer(('127.0.0.1', args.port), handler) as server:
        server.serve_forever()


if __name__ == '__main__':
    main()
