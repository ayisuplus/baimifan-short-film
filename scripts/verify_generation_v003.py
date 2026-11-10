"""Verify compiled full-film prompts and their actual local reference files."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '视频制作/生成板-v003'
def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

board = load(OUT / '展开数据.json')
source = load(ROOT / board['source'])
assert sha(ROOT / board['source']) == board['source_sha256']
assert [r['id'] for b in board['batches'] for r in b['rows']] == [s['id'] for s in source['shots']]
music = load(ROOT / source['music_adoption'])
paths = set()
issues = {}
for batch in board['batches']:
    refs = batch['references']
    assert [r['slot'] for r in refs] == list(range(1, len(refs)+1))
    assert batch['used_seconds'] + batch['handle_seconds'] == 15
    for ref in refs:
        path = ROOT / ref['path']
        assert path.is_file() and sha(path) == ref['sha256'], path
        paths.add(ref['path'])
        if ref['kind'] == 'identity':
            assert '四方向' in ref['purpose']
    for row in batch['rows']:
        assert row['bgm'] == music['marks'][row['id']]
        assert row['camera'] and row['transition']
    for model, prompt in batch['prompts'].items():
        assert not re.search(r'CY\d|关键帧停在', prompt)
        assert (OUT/'提示词'/f"{batch['id']}-{model}.txt").read_text('utf-8').strip() == prompt.strip()
        pattern = r'图片(\d+)' if model == 'seedance25' else r'<Picture (\d+)>'
        assert set(map(int, re.findall(pattern, prompt))) == set(range(1, len(refs)+1))
    h3 = batch['prompts']['minimax-h3']
    assert len(h3) <= 7000
    spoken = re.findall(r'<d>\[Chinese\]\s*(.*?)</d>', h3, re.S)
    actual = ''.join(re.sub(r'<scenetrans>|\s+', '', s) for s in spoken)
    expected = ''.join(re.sub(r'\s+', '', c['text']) for c in batch['dialogue'])
    assert actual == expected, (batch['id'], actual, expected)
    assert not re.search(r'[\u4e00-\u9fff]', re.sub(r'<d>.*?</d>', '', h3, flags=re.S))
    if batch['models']['minimax-h3']['issues']:
        issues[batch['id']] = batch['models']['minimax-h3']['issues']

result = dict(status='passed', batches=len(board['batches']), shots=board['shot_count'],
              prompt_files=2*len(board['batches']), distinct_reference_files=len(paths),
              source_hash_unchanged=True, dialogue_exact_in_h3=True,
              reference_numbering_complete=True, music_marks_unchanged=True,
              max_h3_chars=max(len(b['prompts']['minimax-h3']) for b in board['batches']),
              scope='结构、文案和文件核验；不代表动态生成、声音听审或可提交性验收',
              unresolved_h3_input_issues=issues)
(OUT/'全片核验.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k != 'unresolved_h3_input_issues'}, ensure_ascii=False))
