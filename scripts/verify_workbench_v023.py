"""Verify identity, historical preservation and voice readiness across the joined view."""
from pathlib import Path
from urllib.parse import unquote
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'后期/制作工作台-v023'


def read(path):
    return json.loads(path.read_text('utf-8-sig'))


def main():
    d=read(OUT/'工作台数据.json')
    current=read(ROOT/'后期/配音挑选-v022/作者选择.json')
    original=read(OUT/'作者已完成选择-快照.json')
    indexed={c['id']:c for c in read(ROOT/'后期/配音挑选-v022/候选索引.json')['cues']}
    source=ROOT/'视频制作/生成板-v022/生成板.html'
    old=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',source.read_text('utf8'),re.S)[1])
    assert len(d['shots'])==133 and len(d['batches'])==43 and len(d['cues'])==63
    assert len({s['display_name'] for s in d['shots']})==133
    assert [s['id'] for s in d['shots']]==[sid for b in d['batches'] for sid in b['shot_ids']]
    for before,after in zip(old['batches'],d['batches']):
        for field in ('id','shot_ids','rows','references','prompts','dialogue','rhythm'):
            assert before[field]==after[field], (before['id'],field)
    for path,sha in d['sources'].items():
        # Choices may legitimately change after building; validate the frozen snapshot below.
        if path.endswith('作者选择.json'):continue
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
    assert hashlib.sha256((OUT/'作者已完成选择-快照.json').read_bytes()).hexdigest()==d['completed_pass_snapshot_sha256']
    for c in d['cues']:
        assert c['completed_pass_rejected']==(c['id'] not in original['cue_choices'])
    assert not original['group_choices']
    live_verified=0
    for c in d['cues']:
        assert any(c['id'] in s['cue_ids'] for s in d['shots'])
        for opt in c['options']:
            assert (ROOT/opt['path']).is_file(),opt['path']
            assert opt in indexed[c['id']]['options'], 'Visible candidate absent or stale in save index'
            if opt.get('delivery_version')=='v005':
                assert hashlib.sha256((ROOT/opt['path']).read_bytes()).hexdigest()==opt['sha256']
                assert opt['text_ja']==(c['revision'] or c)['ja']
        saved=current['cue_choices'].get(c['id'])
        if saved:
            opt=next(o for o in c['options'] if o['id']==saved['option_id'])
            assert opt['selectable'] and opt['path']==saved['path'] and opt['sha256']==saved['sha256']
            assert hashlib.sha256((ROOT/saved['path']).read_bytes()).hexdigest()==saved['sha256']
            live_verified+=1
        if c['revision']:assert '水之灵' not in c['revision']['zh']
    cross=next(c for c in d['cues'] if c['id']=='VO-CY024A9-01')
    assert set(cross['visual_shots'])=={'CY024A9','CY024A10','CY024A11','CY024A12','CY024A1'}
    for s in d['shots']:
        assert (ROOT/s['source_path']).is_file()
        for state in s['states']:assert (OUT/unquote(state['image'])).resolve().is_file()
    for b in d['batches']:
        for ref in b['references']:assert (ROOT/ref['path']).is_file()
    for m in d['music']:assert (ROOT/m['path']).is_file()
    for path in d['audio'].values():assert (OUT/unquote(path)).resolve().is_file()
    result=dict(shots=133,batches=43,cues=63,live_choices_verified=live_verified,
                frozen_choices_preserved=len(original['cue_choices']),
                prompt_reference_rhythm_unchanged=True,cross_shot_cue_shared=True,
                paths_valid=True,new_dialogue_status='v005_delivered_pending_listening',
                delivered_v005_cues=sum(any(o.get('delivery_version')=='v005' for o in c['options']) for c in d['cues']))
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
