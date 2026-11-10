"""Join reviewed voice choices, dialogue proposals and existing production inputs.

Never overwrite author choices or synthesize new timing from unrecorded dialogue.
"""
from pathlib import Path
from urllib.parse import quote
import hashlib
import json
import re
from voice_candidates_v005 import merge_v005

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '后期/制作工作台-v023'
SOURCES = {
    'preview': '后期/配音挑选-v022/全片声音预演.html',
    'board': '视频制作/生成板-v022/生成板.html',
    'voices': '后期/配音挑选-v022/候选索引.json',
    'choices': '后期/配音挑选-v022/作者选择.json',
    'revisions': '剧本/对白修订-v0.64-候选.json',
}


def read(path):
    return json.loads(path.read_text('utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def embedded(path):
    return json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', path.read_text('utf8'), re.S)[1])


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def url(path):
    return '../../' + quote(path, safe='/')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    preview, board = [embedded(ROOT/SOURCES[k]) for k in ('preview', 'board')]
    voices, choices, revisions = [read(ROOT/SOURCES[k]) for k in ('voices', 'choices', 'revisions')]
    voices = merge_v005(voices, ROOT)
    # The running save service reads this same index on every request.
    write(ROOT/SOURCES['voices'], voices)
    # Freeze the user's completed pass once. Rebuilds may not erase or relabel it.
    snapshot = OUT/'作者已完成选择-快照.json'
    if not snapshot.exists():
        write(snapshot, choices)
    snapshot_data = read(snapshot)
    changes = {c['id']: c for c in revisions['cues']}
    cue_baseline = {c['id']: c for c in preview['cues']}
    indexed = {c['id']: c for c in voices['cues']}
    assert set(cue_baseline) == set(indexed)
    assert set(changes) <= set(indexed)
    assert not choices['group_choices'], 'Review continuous intentions before rebasing choices'
    assert set(choices['cue_choices']) <= set(indexed)
    cues, missing, invalid, selected = [], [], [], 0
    for c in voices['cues']:
        cue = {**c, 'zh': cue_baseline[c['id']]['zh'], 'revision': changes.get(c['id'])}
        saved = choices['cue_choices'].get(c['id'])
        cue['completed_pass_rejected'] = c['id'] not in snapshot_data['cue_choices']
        if saved:
            opt = next((o for o in c['options'] if o['id'] == saved['option_id'] and o['path'] == saved['path'] and o['sha256'] == saved['sha256']), None)
            if opt and opt['selectable'] and (ROOT/opt['path']).is_file() and digest(ROOT/opt['path']) == opt['sha256']:
                selected += 1
                cue['selected_at_build'] = saved
                cue['selected_seconds'] = opt['seconds']
                cue['baseline_window_seconds'] = round(c['end'] - c['start'], 3)
                cue['duration_delta_seconds'] = round(opt['seconds'] - cue['baseline_window_seconds'], 3)
                cue['audio_state'] = ('selected_old_text_rerecord_if_revised' if cue['revision'] and opt.get('text_ja')!=cue['revision']['ja'] else 'author_selected_pending_timing')
            else:
                invalid.append(c['id'])
                cue['audio_state'] = 'invalid_choice_needs_review'
        else:
            missing.append(c['id'])
            cue['audio_state'] = 'all_existing_candidates_rejected'
        cues.append(cue)
    assert not invalid, f'Invalid chosen files: {invalid}'
    shots = preview['shots']
    by_shot = {s['id']: s for s in shots}
    coverage = []
    for n, batch in enumerate(board['batches'], 1):
        batch['number'] = n
        batch['submission_state'] = 'baseline_pending_voice_and_dialogue_revision'
        for j, sid in enumerate(batch['shot_ids'], 1):
            coverage.append(sid)
            shot = by_shot[sid]
            shot.update(batch_number=n, batch_id=batch['id'], batch_shot_number=j,
                        display_name=f'第{n}批 · 第{j}镜',
                        generation_row=next(row for row in batch['rows'] if row['id'] == sid))
            shot['cue_ids'] = [c['id'] for c in cues if sid in c['visual_shots'] or (c['start'] < shot['end'] and c['end'] > shot['start'])]
        batch['revision_ids'] = list(dict.fromkeys(cid for sid in batch['shot_ids'] for cid in by_shot[sid]['cue_ids'] if cid in changes))
    assert coverage == list(by_shot), 'Batch order or shot coverage drift'
    for c in cues:
        c['location'] = by_shot[c['shot']]['display_name']
    bgm_path = '后期/语音节奏定版-v021/BGM试听.mp3'
    mix_path = '后期/语音节奏定版-v021/全片声音预览.mp3'
    for p in [bgm_path, mix_path] + [s['source_path'] for s in shots]:
        assert (ROOT/p).is_file(), p
    affected = sorted({by_shot[c['shot']]['batch_number'] for c in cues if c['revision']})
    delivered = [c['id'] for c in cues if any(o.get('delivery_version')=='v005' and o.get('text_ja')==(c['revision'] or c)['ja'] for o in c['options'])]
    pending_recording = (set(missing)|set(changes))-set(delivered)
    dataset = dict(version='v023', title='白米饭 · 制作工作台',
                   duration=preview['duration'], timing_state='v021_navigation_baseline_not_final',
                   choice_api='/api/voice-choices-v022',
                   audio=dict(bgm=url(bgm_path), historical_mix=url(mix_path)),
                   shots=shots, cues=cues, groups=voices['groups'], batches=board['batches'],
                   music=preview['music'], silences=preview['silences'], music_titles=board['music_titles'],
                   sources={v:digest(ROOT/v) for v in SOURCES.values()},
                   completed_pass_snapshot_sha256=digest(snapshot),
                   summary=dict(shots=len(shots), batches=len(board['batches']), cues=len(cues),
                                selected=selected, rejected_ids=missing, revision_ids=list(changes),
                                revision_batches=affected, valid_audio_hashes=selected,
                                rerecord_scope_count=len(set(missing)|set(changes)),
                                delivered_v005_ids=delivered,
                                needs_rerecord_if_revisions_adopted=len(pending_recording)))
    write(OUT/'工作台数据.json', dataset)
    write(OUT/'选择与返工核验.json', dict(**dataset['summary'],
        selected_source_sha256=digest(ROOT/SOURCES['choices']),
        completed_pass_snapshot_sha256=digest(snapshot),
        invalid_choices=invalid, preserved_original_choices=True,
        candidate_text_not_adopted=True, no_generated_media=True))
    lines = ['# 台词修订与配音交接 v023', '',
             '作者已完成挑选：未选表示现有音色全部不采用。60句选择经路径、候选ID和实际文件SHA256核验；原选择文件不改写。', '',
             f'v005已交付{len(delivered)}句对应新录音；尚未逐字/表演听审或采用，原60句选择保留。', '',
             '## 上一轮旧音色全部不采用（新录已单列待试听）', '']
    for c in cues:
        if c['id'] in missing: lines.append(f"- {c['location']} / {c['role']}：{c['zh']}（{c['id']}）")
    lines += ['', '## 新台词候选（尚未采用）', '',
              '候选源为 `剧本/对白修订-v0.64-候选.json`；工作台从同一文件派生。保留v0.63正式剧情与全部历史音频。', '']
    for c in cues:
        p=c['revision']
        if not p: continue
        lines += [f"### {c['location']} / {c['role']}", '', f"原句：{c['zh']}", f"候选：{p['zh']}",
                  f"日语译配草案：{p['ja']}", f"表演与切点：{p['direction']}", f"时长：{p['timing']}", '']
    lines += ['## 执行状态', '',
              f"本轮重录范围{len(set(missing)|set(changes))}句，已交付{len(delivered)}句，文件缺口{len(pending_recording)}句。旧文录音选择保留；交付完成不等于新声已采用。月背分工长句尾部仍有信号，需重点听审原生末句，不能以补静音替代缺字检查。", '',
              '统一工作台以“第几批 · 第几镜”显示，底层保留CY镜号和GB批次ID；现有43批和483.22秒仅作为v021导航基线。新录音完成后重排声音窗口、镜长与批次。', '',
              '默认播放是v021画面+BGM，不播放旧对白；旧混音仅作对照。逐句可听作者已选版本和所有历史候选。BGM卡点显示原曲入出点和动作对应，不宣称已按本轮选择重混。', '',
              '完整批次提示词保留原始文本，明确为待重排基线；受改词影响处显示修订说明。提示词不提供提交按钮，未上传、未生成音视频。', '',
              '保留：Kimi4秒月光显形、Claude父亲插话真实词尾起6秒、GPT祈愿词尾至术名0.8秒、尾段4秒无BGM。新录音实测后重新验证，不能将旧时长当新词时长。']
    (OUT/'台词修订与配音交接.md').write_text('\n'.join(lines)+'\n', encoding='utf8')
    print(json.dumps(dataset['summary'], ensure_ascii=False))


if __name__ == '__main__':
    main()
