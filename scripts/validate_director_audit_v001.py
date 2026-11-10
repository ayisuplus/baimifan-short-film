"""Validate audit coverage and local links, without implying audiovisual acceptance."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import hashlib, json, py_compile, re, shutil, subprocess, tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '后期/导演全片审查-v001'

def read(name):
    return json.loads((OUT / name).read_text(encoding='utf8'))

sources = read('当前44批审查清单.json')
report = read('导演审查结论.json')
assert len(report['batches']) == 44
assert sorted(r['batch_number'] for r in report['batches']) == list(range(1, 45))
assert sum(len(b['shots']) for b in sources) == 133
source_by = {b['batch_number']: b for b in sources}
evidence_count = 0
for row in report['batches']:
    source = source_by[row['batch_number']]
    assert row['id'] == source['id']
    assert row['verdict'] in ('regenerate', 'post', 'keep')
    for issue in row.get('issues', []):
        assert set(issue.get('shot_ids', [])) <= {s['id'] for s in source['shots']}, row['batch_number']
        assert issue['category'] in ('regenerate', 'post', 'optional')
        start = issue.get('local_start', 0) or 0
        end = issue.get('local_end', start)
        assert end is not None and 0 <= start <= end <= source['video_duration'] + .1, (row['batch_number'], start, end)
        for name in issue.get('evidence', []):
            assert (ROOT / name).exists() or (OUT / name).exists(), name
            evidence_count += 1
    assert hashlib.file_digest((ROOT / source['path']).open('rb'), 'sha256').hexdigest() == source['sha256'], source['path']

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src', 'poster') and value and not value.startswith('#'):
                if not urlsplit(value).scheme:
                    self.links.append(value)

page = (OUT / '导演审查.html').read_text(encoding='utf8')
parser = Links()
parser.feed(page)
for link in parser.links:
    assert (OUT / unquote(urlsplit(link).path)).exists(), link
for name in ('prepare_director_audit_v001.py', 'build_director_audit_v001.py', 'validate_director_audit_v001.py'):
    py_compile.compile(str(ROOT / 'scripts' / name), doraise=True)
js_result = 'not_checked_node_unavailable'
if node := shutil.which('node'):
    script = re.findall(r'<script>(.*?)</script>', page, re.S)[0]
    with tempfile.TemporaryDirectory(prefix='director-audit-') as folder:
        path = Path(folder) / 'check.js'
        path.write_text(script, encoding='utf8')
        subprocess.run([node, '--check', str(path)], check=True, capture_output=True)
    js_result = 'passed'

result = {
    'batches': 44, 'planned_shots': 133,
    'current_source_hashes_unchanged': True,
    'local_links_checked': len(parser.links), 'issue_evidence_links_checked': evidence_count,
    'issue_times_within_actual_videos': True, 'python_syntax': 'passed', 'javascript_syntax': js_result,
    'visual_review': '全时长2fps抽帧与疑点加密，三名独立分段复核，主代理归并',
    'continuous_audio_listening': False, 'lip_sync_accepted': False,
    'browser_visual_verification': False,
    'preview_service': '8968连接拒绝；启动操作被自动审批策略阻止，未绕过',
    'media_modified': False, 'paid_generation_submitted': False,
    'repair_methods_trial_edited': False,
}
(OUT / '交付核验.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps(result, ensure_ascii=False))
