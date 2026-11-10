"""Verify the bounded image revision without regenerating or changing selections."""
import hashlib
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))
def sha(path):
    return hashlib.sha256((root / path).read_bytes()).hexdigest()

old = read('镜头设计/shot-plan-v0.48r1.json')
new = read('镜头设计/shot-plan-v0.49.json')
changes = read('镜头设计/生成记录/连续性修复-v049/变更清单.json')['changes']
expected = {r['shot'] for r in changes}
assert len(old['shots']) == len(new['shots']) == 131
assert old['total_seconds'] == new['total_seconds'] == 431.5
assert new['music_adoption'] == old['music_adoption']
allowed = {'presentation', 'invariants', 'visual_prompt', 'generation_request', 'refs',
           'final_static_review', 'page_size', 'panel_rect_pixels', 'panel_region'}
changed = set()
for a, b in zip(old['shots'], new['shots']):
    for key in a:
        if key not in allowed:
            assert a[key] == b[key], (a['id'], key)
    if a['presentation']['path'] != b['presentation']['path']:
        changed.add(a['id'])
    else:
        assert a == b, a['id']
assert changed == expected and len(changed) == 10
for row in changes:
    assert sha(row['after']) == row['sha256']
    req = read(row['request'])
    assert req['output'] == row['after'] and req['sha256'] == row['sha256']
    with Image.open(root / row['after']) as im:
        im.verify()
a = read(old['audio_arrangement'])
b = read(new['audio_arrangement'])
for key in a:
    if key not in {'version', 'shot_plan', 'shot_plan_sha256'}:
        assert a[key] == b[key], key
assert b['shot_plan_sha256'] == sha(b['shot_plan'])
ui = read('镜头设计/审查/连续性修复-v049-浏览器读回.json')
marks = read(new['music_adoption'])['marks']
names = {'BGM-CY-MT-03':'存在魔法的世界', 'BGM-CY-KH-05':'To Jerusalem',
         'BGM-CY-HP7-02':'Snape to Malfoy Manor', 'BGM-CY-RZ-01':'沉默的镇魂曲',
         'BGM-CY-FEAR-001':'Fear Brought Me This Far',
         'BGM-CY-FZ-02':'let the stars fall down', 'BGM-CY-TIME-001':'Time Flows Ever Onward'}
assert len(ui['options']) == 131
assert {x['id'] for x in ui['options']} == set(marks)
for option in ui['options']:
    assert option['label'].startswith('✓') and names[marks[option['id']]] in option['label']
result = {'status':'passed', 'shots':131, 'seconds':431.5,
          'changed_images':sorted(changed), 'unchanged_images':121,
          'unchanged_audio_arrangement':True, 'browser_marks_verified':131,
          'new_images_integrity_verified':10,
          'scope':'Data, file integrity and rendered selection labels; visual review is separate.'}
(root / '镜头设计/审查/连续性修复-v049-数据核验.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
