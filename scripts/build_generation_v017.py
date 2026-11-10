"""Integrate reviewed v062 shot revisions without rewriting the source or audio.

The authoring agent owns shot-plan-v0.62.json. This adapter only builds the
versioned generation board, static preview, and comparison handoff.
"""
import copy
import hashlib
import html
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OLD = '视频制作/生成板-v016'
OUT = '视频制作/生成板-v017'
OLDFIX = '后期/扇子法术-v016'
FIX = '后期/关键动作重拍-v017'
BASE = '镜头设计/shot-plan-v0.61.json'
SOURCE = '镜头设计/shot-plan-v0.62.json'
TARGETS = ['CY021A', 'CY022A', 'CY023', 'CY027B1', 'CY028A', 'CY029C', 'CY029D']
EN = {
    'CY021A': 'Close over the delivering cultist shoulder: the priest takes the single ritual torch in his RIGHT hand, then looks toward his bound daughter high in depth. Keep his calm resolve, dark flame with a thin violet edge, and ordinary warm fixed flames. A short focus shift links hand, father and daughter without adding hesitation.',
    'CY022A': 'Ground-level oblique close-up of the child hand, robe hem and part of her face. Continue the same grip: taut fabric slips across fingertips, fingers try to close once but miss, then the hand sinks. Child screen-left, departing priest screen-right; next shot establishes the stairs. Torch stays in his right hand offscreen.',
    'CY023': 'Oblique low camera immediately inside the doorway. A single effortless kick drives the door inward; sole, splintering wood and the cold light opening dominate, with the face partly occluded. Complete impact and foot landing within two seconds, then reveal the whole group in the next shot.',
    'CY027B1': 'One continuous subject transforms: GPT rises inside white-violet waterlight as her body silhouette becomes the long dragon body, with white horns and violet mane continuing the same motion. No complete humanoid beside an independently summoned complete dragon. Finish the transformation and preserve the subsequent upward exit direction.',
    'CY028A': 'Begin wide enough to show the supported step down from the footrest. After Claude is stable, move in on the same side to a chest-up two-shot: GPT supporting her upper arm and Claude looking down the stairs for the child. Kimi withdraws into soft depth. Preserve 6.2 seconds and all original Japanese speech.',
    'CY029C': 'Same-side waist-height oblique medium shot. Claude lowers her spell hand, loses support through shoulder and hip, and leans toward GPT without falling to the floor. GPT steps into the weight-transfer space and starts taking her weight. Keep the burned cloth edges, pallor and bare feet; the burning empty frame stays peripheral and soft.',
    'CY029D': 'Continue the SAME catch, without a second stumble. GPT supports Claude back, slides her other arm under the knees, and lifts; keep both supporting arms readable. Do not begin already settled in a bridal pose. The following shot holds the stable carry; the next voluntary shoulder touch remains later.',
}


def load(p):
    return json.loads((ROOT / p).read_text('utf-8-sig'))


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def write(p, data):
    path = ROOT / p
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', 'utf-8')


def remap(data, oldhash, newhash):
    if isinstance(data, dict):
        return {k: remap(v, oldhash, newhash) for k, v in data.items()}
    if isinstance(data, list):
        return [remap(v, oldhash, newhash) for v in data]
    if isinstance(data, str):
        return data.replace(OLD, OUT).replace(OLDFIX, FIX).replace(BASE, SOURCE).replace(oldhash, newhash)
    return data


def run_renderer(name, entry='main'):
    path = ROOT / 'scripts' / name
    code = path.read_text('utf-8').replace('视频制作/生成板-v014', OUT).replace('后期/生成前修正-v014', FIX).replace('镜头设计/shot-plan-v0.59.json', SOURCE)
    ns = {'__file__': str(path), '__name__': 'v017_adapter'}
    exec(compile(code, str(path), 'exec'), ns)
    return ns[entry](ROOT) if entry == 'build' else ns[entry]()


def review_page(old, new, changed):
    om = {s['id']: s for s in old['shots']}
    sm = {s['id']: s for s in new['shots']}

    def url(p):
        return quote(os.path.relpath(ROOT / p, ROOT / FIX).replace('\\', '/'), safe='/#')

    def figure(path, label):
        return '<figure><figcaption>' + html.escape(label) + '</figcaption><a target="_blank" href="' + url(path) + '"><img loading="lazy" src="' + url(path) + '"></a></figure>'

    cards = []
    for sid in changed:
        s = sm[sid]
        meta = s.get('revision_v062', {})
        states = s.get('review_state_sequence', [])
        extra = ''.join(figure(st['path'], str(st['offset']) + '秒 · ' + st['label']) for st in states if st['path'] != s['presentation']['path'])
        cards.append('<section id="' + sid + '"><h2>' + html.escape(s['title']) + '</h2><p>' + html.escape(s.get('camera', s['framing'])) + '</p><div class="pair">' + figure(om[sid]['presentation']['path'], '上一版 · 保留历史') + figure(s['presentation']['path'], '本轮新候选 · 待作者审阅') + '</div>' + ('<div class="pair">' + extra + '</div>' if extra else '') + '<p>' + html.escape(s['action']) + '</p><p class="muted">' + html.escape(meta.get('note', s['presentation'].get('missing', '动态连续性另验'))) + '</p><a href="全片声音预览.html#t=' + str(s['start_second']) + '">带原配音与BGM看这一段 · ' + f'{int(s["start_second"]//60):02}:{s["start_second"]%60:05.2f}' + '</a></section>')
    groups = [
        ('接火把与最后抵抗', ['CY018B', 'CY021A', 'CY019', 'CY020', 'CY020B', 'CY020A', 'CY021', 'CY021B', 'CY022A', 'CY022A1', 'CY022']),
        ('破门与完整亮相', ['CY022C', 'CY023', 'CY024', 'CY024R']),
        ('本人化龙', ['CY027B', 'CY027B1', 'CY027B2', 'CY027B3']),
        ('站稳与牵挂', ['CY027G', 'CY028A', 'CY028A2']),
        ('脱力到主动靠近', ['CY029B', 'CY029C', 'CY029D', 'CY028', 'CY029A']),
    ]
    data = []
    for title, ids in groups:
        seq = []
        for sid in ids:
            s = sm[sid]
            states = s.get('review_state_sequence', []) or [dict(path=s['presentation']['path'], offset=0, label='代表状态')]
            for i, st in enumerate(states):
                end = states[i+1]['offset'] if i+1 < len(states) else s['seconds']
                seq.append(dict(title=s['title'] + ' · ' + st['label'], seconds=end-st['offset'], src=url(st['path']), changed=sid in changed))
        data.append(dict(title=title, shots=seq, start=sm[ids[0]]['start_second']))
    page = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · 关键动作重拍 v017</title><style>body{background:#111820;color:#edf1f5;font:17px/1.75 system-ui,"Microsoft YaHei";max-width:1400px;margin:auto;padding:28px}h1{font-size:32px}p{color:#c0ccda}a{color:#a6c7ff}section{margin:28px 0;padding:24px;background:#1b2633;border-radius:14px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0}img{width:100%;display:block;border-radius:8px}figcaption{padding:8px 0;font-size:14px}button,select{padding:10px 15px;margin:4px;border:1px solid #556476;border-radius:7px;background:#334457;color:white;cursor:pointer;font:inherit}.notice{border-left:4px solid #d5b181;padding:15px;background:#292b36}#film{max-height:68vh;object-fit:contain}.muted{color:#9eafc0;font-size:14px}nav{display:flex;flex-wrap:wrap;gap:16px}@media(max-width:850px){.pair{grid-template-columns:1fr}body{padding:14px}}</style>
<h1>让关键动作成为画面中心</h1><p>接火、滑脱、破门、化龙、牵挂与接抱：六处已按审查方向修订，原画和旧生成板保留。</p><p class="notice">当前为新静帧候选与连续摄影方案，待作者审阅。配音、BGM、镜长保持；静帧轮看不证明动作受力、变形、口型已经实现。尚未提交视频生成。</p><nav><a href="../../视频制作/生成板-v017/生成板.html">生成板 v017</a><a href="全片声音预览.html">全片声音与画面预览</a><a href="../全片张力审查-v016/审查.html">本轮审查依据</a><a href="验证结果.json">输入与时码核验</a></nav>
<section><h2>放回前后镜头里看</h2><select id="group" aria-label="选择连续段落"></select><p class="muted">按原镜长与状态时点轮看；这是构图和衔接预览，真实运动另验。</p><img id="film"><p id="caption"></p><button id="prev">上一状态</button><button id="play">按镜长轮看</button><button id="next">下一状态</button><a id="sound">带声音看完整段落</a></section>'''
    page += ''.join(cards)
    page += '''<script>const D=__DATA__;let g=0,i=0,t=null,playing=false;const $=id=>document.getElementById(id);D.forEach((v,j)=>{const o=document.createElement('option');o.value=j;o.textContent=v.title;$('group').append(o)});function show(){clearTimeout(t);let s=D[g].shots[i];$('film').src=s.src;$('caption').textContent=s.title+' · '+s.seconds.toFixed(2)+'秒 · '+(s.changed?'本轮修订':'前后保留镜');$('sound').href='全片声音预览.html#t='+D[g].start;if(playing)t=setTimeout(()=>{i=(i+1)%D[g].shots.length;show()},s.seconds*1000)}$('group').onchange=()=>{g=+$('group').value;i=0;show()};$('prev').onclick=()=>{i=(i+D[g].shots.length-1)%D[g].shots.length;show()};$('next').onclick=()=>{i=(i+1)%D[g].shots.length;show()};$('play').onclick=()=>{playing=!playing;$('play').textContent=playing?'暂停轮看':'按镜长轮看';show()};show();</script></html>'''
    (ROOT / FIX / '修正交接.html').write_text(page.replace('__DATA__', json.dumps(data, ensure_ascii=False)), 'utf-8')


def main():
    old, source = load(BASE), load(SOURCE)
    oldhash, h = sha(BASE), sha(SOURCE)
    assert len(source['shots']) == 133 and abs(source['total_seconds'] - 464.4) < 1e-6
    om = {s['id']: s for s in old['shots']}
    sm = {s['id']: s for s in source['shots']}
    assert [(s['id'], s['seconds'], s.get('subtitle_cues')) for s in old['shots']] == [(s['id'], s['seconds'], s.get('subtitle_cues')) for s in source['shots']]
    changed = [sid for sid in TARGETS if sm[sid] != om[sid]]
    assert set(TARGETS[:-1]) <= set(changed), ('Six reviewed nodes must be revised', changed)
    for sid in changed:
        s = sm[sid]
        assert (ROOT / s['presentation']['path']).is_file()
        states, preview = s.get('state_references', []), s.get('review_state_sequence', [])
        if states:
            assert [(v['path'], v['offset']) for v in states] == [(v['path'], v['offset']) for v in preview], (sid, 'State preview/input mismatch')
    for p in (ROOT / OLD).glob('*.json'):
        if p.name not in ['展开数据.json', '结构核验.json']:
            write(OUT + '/' + p.name, remap(load(p), oldhash, h))
    plan = load(OUT + '/批次计划.json')
    plan.update(version='v017', output=OUT + '/生成板.html')
    plan['navigation']['review'] = FIX + '/修正交接.html'
    plan['navigation']['previs'] = FIX + '/全片声音预览.html'
    cast = load(OUT + '/人物核对.json')
    direction = load(OUT + '/动态审查.json')
    for sid in changed:
        s = sm[sid]
        meta = s.get('revision_v062', {})
        note = meta.get('note', s['presentation'].get('missing', '本轮修订构图状态，非强制首帧；动作连续性另验。'))
        plan.setdefault('action_overrides', {})[sid] = s['action']
        plan.setdefault('shot_notes', {})[sid] = note
        plan.setdefault('execution_notes', {})[sid] = s.get('camera', s['framing']) + ' ' + note
        if sid == 'CY027B1':
            # The same camera sentence is already rendered verbatim by camera_zh.
            # Omit only that duplicate here; every action and constraint remains.
            plan['execution_notes'][sid] = note
        if meta.get('cast'):
            plan.setdefault('cast_overrides', {})[sid] = meta['cast']
            cast['shots'][sid] = dict(meta['cast'], basis='v062实际图像及动作进出联合核对；静帧不是动态验收')
        for batch in direction['batches'].values():
            if sid not in batch['shots']:
                continue
            rv = batch['shots'][sid]
            rv.update(camera_zh=s.get('camera', s['framing']), camera_en=meta.get('camera_en', EN[sid]), action_en=meta.get('action_en', EN[sid]), action_zh_override=s['action'])
            if meta.get('transition_zh'):
                rv['transition_zh'] = meta['transition_zh']
            if meta.get('transition_en'):
                rv['transition_en'] = meta['transition_en']
            if meta.get('effects_zh'):
                rv['effects_zh_override'] = meta['effects_zh']
    write(OUT + '/批次计划.json', plan)
    write(OUT + '/人物核对.json', cast)
    write(OUT + '/动态审查.json', direction)
    audit = load(OUT + '/对白复核.json')
    audit['localization_sha256'] = sha(OUT + '/日语译配.json')
    write(OUT + '/对白复核.json', audit)
    for name in ['配音对位方案.json', 'BGM剪辑方案.json', '实际BGM剪辑.json', '作者确认选曲.json']:
        write(FIX + '/' + name, remap(load(OLDFIX + '/' + name), oldhash, h))
    audio_hashes = {}
    for name in ['BGM试听.wav', 'BGM试听.mp3', '全片声音预览.mp3']:
        target = ROOT / FIX / name
        if not target.exists():
            shutil.copy2(ROOT / OLDFIX / name, target)
        assert sha(FIX + '/' + name) == sha(OLDFIX + '/' + name)
        audio_hashes[name] = sha(FIX + '/' + name)
    mix = load(FIX + '/实际BGM剪辑.json')
    mix.update(source_sha256=h, voice_plan_sha256=sha(FIX + '/配音对位方案.json'), bgm_plan_sha256=sha(FIX + '/BGM剪辑方案.json'))
    mix['visual_revision_audio_reuse'] = dict(from_manifest=OLDFIX + '/实际BGM剪辑.json', sha256=sha(OLDFIX + '/实际BGM剪辑.json'), reason='Only six visual action/camera nodes revised; all actual audio bytes and event content preserved.')
    assert mix['voice_events'] == load(OLDFIX + '/实际BGM剪辑.json')['voice_events']
    write(FIX + '/实际BGM剪辑.json', mix)
    run_renderer('build_generation_v014.py')
    run_renderer('build_previs_v014.py', 'build')
    review_page(old, source, changed)
    run_renderer('verify_generation_v014.py')
    board = load(OUT + '/展开数据.json')
    affected = [dict(id=b['id'], shots=[r['id'] for r in b['rows'] if r['id'] in changed], references=len(b['references']), selected=b['selected_model'], chars=b['models'][b['selected_model']]['chars']) for b in board['batches'] if any(r['id'] in changed for r in b['rows'])]
    report = dict(status='passed', source_sha256=h, source_not_modified_by_builder=sha(SOURCE) == h, previous_source_unchanged=sha(BASE) == oldhash, changed_shots={sid: dict(path=sm[sid]['presentation']['path'], sha256=sha(sm[sid]['presentation']['path'])) for sid in changed}, affected_batches=affected, audio_outputs_sha256=audio_hashes, audio_outputs_identical=True, timing_dialogue_unchanged=True, author_adoption=False, video_generated=False)
    write(FIX + '/画面修订核验.json', report)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
