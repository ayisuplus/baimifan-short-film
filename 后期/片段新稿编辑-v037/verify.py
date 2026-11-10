"""Read-only native draft and full-backup preservation checks. No browser access."""
import json
import hashlib
import subprocess
import sys
from pathlib import Path

REPO = Path('E:/projects/媒体后期/OpenCut-classic')
PROJECT = 'restored-ad3867fc-177c-4371-bb51-7ed75d686e30'
ROOT = REPO / '.local/project-backups'
LIVE = ROOT / 'restored' / PROJECT
BEFORE = ROOT / '54727fa5-e3b9-40f2-9d39-9dd6526145f5'
OUT = Path(__file__).parent

def read(path):
    return json.loads(path.read_text('utf-8'))

def native(root, command, payload):
    p = subprocess.run([str(REPO / 'target/debug/opencut-creative.exe'), str(root), command],
                       input=json.dumps(payload, ensure_ascii=False), capture_output=True, encoding='utf-8', check=True)
    r = json.loads(p.stdout)
    assert r['ok'], r
    return r['value']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

package = read(LIVE / 'package/manifest.json')
contexts = package['clipContexts']['contexts']
assert len(contexts) == 118
rows = []
for key, context in contexts.items():
    result = native(LIVE / 'creative', 'clip-context', {
        'action': 'draft_read', 'project_id': PROJECT, 'context_id': key,
        'package_root': str(LIVE / 'package')})
    v = result['current']
    assert len(v['texts']['script']) == len(context['script'])
    assert len(v['texts']['prompts']) == len(context['prompts'])
    assert v['project_id'] == PROJECT and v['context_id'] == key
    assert all(v['texts']['script'])
    assert '临时验收' not in json.dumps(v, ensure_ascii=False)
    rows.append({'context_id': key, 'title': context['title'], 'revision': v['revision'],
                 'script_count': len(v['texts']['script']), 'prompt_count': len(v['texts']['prompts']),
                 'nonempty_prompts': sum(bool(s) for s in v['texts']['prompts'])})
assert sum(r['revision'] == 1 for r in rows) == 1
assert sum(r['revision'] == 0 for r in rows) == 117
(OUT / '118段新稿读取核验.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', 'utf-8')
print('All 118 native draft reads passed.')

if len(sys.argv) > 1:
    after = ROOT / sys.argv[1]
    old, new = read(BEFORE / 'browser.json'), read(after / 'browser.json')
    assert [s['tracks'] for s in old['project']['scenes']] == [s['tracks'] for s in new['project']['scenes']]
    assert old['media'] == new['media']
    assert old['project']['settings'] == new['project']['settings']
    checked = []
    for sub in ['package', 'creative']:
        for p in (BEFORE / sub).rglob('*'):
            if not p.is_file():
                continue
            rel = p.relative_to(BEFORE)
            assert sha(p) == sha(after / rel), str(rel)
            checked.append(str(rel))
    new_files = sorted(str(p.relative_to(after)) for p in (after / 'creative').rglob('*')
                       if p.is_file() and not (BEFORE / p.relative_to(after)).exists())
    assert new_files == ['creative\\clip-drafts\\CUT003\\000001.json'], new_files
    draft = read(after / new_files[0])
    base = native(LIVE / 'creative', 'clip-context', {
        'action': 'draft_version', 'project_id': PROJECT, 'context_id': 'CUT003',
        'package_root': str(LIVE / 'package'), 'revision': 0})['version']
    assert draft['texts'] == base['texts'], 'UI acceptance copy must retain source text exactly'
    scratch = new['drafts'].get('opencut-creative:' + package['id'] + ':clip-drafts')
    assert scratch is None or json.loads(scratch) == {}, scratch
    report = {'before_backup': BEFORE.name, 'after_backup': after.name,
              'all_118_drafts_readable': True, 'timeline_tracks_exactly_equal': True,
              'media_inventory_equal': True, 'settings_equal': True,
              'preserved_native_and_package_files': len(checked), 'new_files': new_files,
              'ui_saved_copy_equals_source': True, 'no_temporary_input_remains': True}
    (OUT / '保存前后核验.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    print(json.dumps(report, ensure_ascii=False))
