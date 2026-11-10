"""Verify compiled full-film prompts and their actual local reference files."""
import argparse
import hashlib
import json
import re
import sys,runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if len(sys.argv)==1 or ('--board' in sys.argv and sys.argv[sys.argv.index('--board')+1]=='视频制作/生成板-v012'):
    runpy.run_path(str(ROOT/'scripts/verify_repaired_board.py'),run_name='__main__')
    raise SystemExit(0)
parser=argparse.ArgumentParser()
parser.add_argument('--board',default='视频制作/生成板-v011')
OUT = ROOT / parser.parse_args().board
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
        if model == 'seedance25':
            assert not re.search(r'(?<!@)图片\s*\d|@@图片|@图片\d+(?:、|至)\d', prompt)
        pattern = r'@图片(\d+)' if model == 'seedance25' else r'<Picture (\d+)>'
        assert set(map(int, re.findall(pattern, prompt))) == set(range(1, len(refs)+1))
    h3 = batch['prompts']['minimax-h3']
    assert len(h3) <= 7000
    language=board.get('audio_execution',{}).get('dialogue_language','Chinese')
    spoken = re.findall(r'<d>\['+language+r'\]\s*(.*?)</d>', h3, re.S)
    actual = ''.join(re.sub(r'<scenetrans>|\s+', '', s) for s in spoken)
    expected = ''.join(re.sub(r'\s+', '', c['text']) for c in batch['dialogue'])
    assert actual == expected, (batch['id'], actual, expected)
    assert not re.search(r'[\u4e00-\u9fff]', re.sub(r'<d>.*?</d>', '', h3, flags=re.S))
    if board.get('audio_execution'):
        assert '[Chinese]' not in h3
        assert batch['rhythm']['status']=='action_targets_music_alignment_pending'
        for point in batch['rhythm']['points']:
            assert 0<=point['time']<batch['used_seconds']
            assert point['film_time']==batch['film_start']+point['time']
            assert point['source_seconds'] is None
        for c in batch['dialogue']:
            assert c['source_text'] and c['language']==language
    if batch['models']['minimax-h3']['issues']:
        issues[batch['id']] = batch['models']['minimax-h3']['issues']

result = dict(status='passed', batches=len(board['batches']), shots=board['shot_count'],
              prompt_files=2*len(board['batches']), distinct_reference_files=len(paths),
              source_hash_unchanged=True, dialogue_exact_in_h3=True,
              reference_numbering_complete=True, music_marks_unchanged=True,
              max_h3_chars=max(len(b['prompts']['minimax-h3']) for b in board['batches']),
              scope='结构、文案和文件核验；不代表动态生成、声音听审或可提交性验收',
              unresolved_h3_input_issues=issues)
if board.get('audio_execution'):
    execution=board['audio_execution']
    assert execution['dialogue_upload'] is False and execution['bgm_upload'] is False
    assert execution['generated_dialogue'] is True and execution['generated_bgm'] is False
    original=load(ROOT/'视频制作/生成板-v006/展开数据.json')
    for before,after in zip(original['batches'],board['batches']):
        assert before['references']==after['references'] and before['rows']==after['rows']
        assert [c['text'] for c in before['dialogue']]==[c['source_text'] for c in after['dialogue']]
    result.update(action_target_count=sum(len(b['rhythm']['points']) for b in board['batches']),music_beat_alignment='pending_not_measured',dialogue_language=language,localized_dialogue='draft_not_voice_tested',source_actions_and_references_preserved=True)
if board.get('dialogue_audit',{}).get('migration') in ('full_language_change','japanese_audio_return'):
    previous=load(ROOT/board['dialogue_audit']['board_source'])
    assert sha(ROOT/board['dialogue_audit']['board_source'])==board['dialogue_audit']['board_sha256']
    loc=load(ROOT/board['audio_execution']['localization'])
    assert sha(ROOT/board['audio_execution']['localization'])==board['dialogue_audit']['localization_sha256']
    japanese_return=board['dialogue_audit']['migration']=='japanese_audio_return'
    assert language==('Japanese' if japanese_return else 'English')
    if not japanese_return:assert board['audio_execution']['post_voice_engine']=='Breeze TTS 2'
    assert len(previous['batches'])==len(board['batches'])
    for a,b in zip(previous['batches'],board['batches']):
        assert a['id']==b['id'] and a['rhythm']==b['rhythm']
        assert len(a['dialogue'])==len(b['dialogue'])
        for c,d in zip(a['dialogue'],b['dialogue']):
            for key in ('shot_id','start','end','speaker','source_text','offscreen','mode'):assert c[key]==d[key]
            assert d['text']==loc['translations'][d['source_text']]==d['review']['current_text']
            assert all(d['review'].get(k) for k in ('listener','intention','delivery'))
        if japanese_return:
            for prompt in b['prompts'].values():assert not re.search(r'\[English\]|English speech|英语台词|Breeze',prompt)
            for d in b['dialogue']:
                audio=d['returned_audio']
                assert audio['text']==d['text'] and sha(ROOT/audio['path'])==audio['sha256']
                assert re.search(r'[\u3040-\u30ff]',d['text']),d['text']
        else:
            for prompt in b['prompts'].values():assert not re.search(r'[\u3040-\u30ff]|Japanese|日语',prompt)
    assert board['batches'][0]['dialogue'][0]['text']==next(b for b in board['batches'] if b['id']=='GB032')['dialogue'][0]['text']
    result.update(dialogue_review_count=sum(len(b['dialogue']) for b in board['batches']),comparison_baseline='v010' if japanese_return else 'v009',all_cues_translated=True,original_dialogue_windows_and_rhythm_preserved=True)
    if japanese_return:
        result.update(localized_dialogue='returned_japanese_text_audio_linked_not_word_audited',returned_audio_files=61,submission_ready=False)
elif board.get('dialogue_audit'):
    changes=board['dialogue_audit'].get('applied_changes',[])
    baseline='v008' if changes else 'v007'
    previous=load(ROOT/f'视频制作/生成板-{baseline}/展开数据.json')
    changed_prompts=0
    for a,b in zip(previous['batches'],board['batches']):
        edits=[c for c in changes if c['batch_id']==b['id']]
        for model,prompt in a['prompts'].items():
            expected=prompt
            for change in edits:
                assert change['old'] in expected
                expected=expected.replace(change['old'],change['new'])
            assert expected==b['prompts'][model]
            changed_prompts+=prompt!=b['prompts'][model]
        for ci,(c,d) in enumerate(zip(a['dialogue'],b['dialogue'])):
            expected={k:v for k,v in c.items() if k!='review'}
            for change in edits:
                if ci==change['cue_index']:
                    assert expected['text']==change['old']
                    expected['text']=change['new']
            assert expected=={k:v for k,v in d.items() if k!='review'}
            assert all(d['review'].get(k) for k in ('listener','intention','delivery'))
    result.update(dialogue_review_count=sum(len(b['dialogue']) for b in board['batches']),comparison_baseline=baseline,approved_dialogue_changes=len(changes),changed_prompt_files=changed_prompts,other_dialogue_and_prompts_unchanged=True)
(OUT/'全片核验.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k != 'unresolved_h3_input_issues'}, ensure_ascii=False))
