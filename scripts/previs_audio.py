"""Candidate music view for the existing storyboard; source shot plan stays immutable."""
import hashlib, html, json
from pathlib import Path

def load_audio(root, data, plan):
    config_path=root/data.get('audio_arrangement','后期/BGM重选-v005/预演编排.json')
    config=json.loads(config_path.read_text(encoding='utf-8-sig'))
    assert config['shot_plan_sha256']==hashlib.sha256(plan.read_bytes()).hexdigest(), 'Music bindings need review after shot-plan changes'
    music={}
    for path in config['music_manifests']:
        manifest=json.loads((root/path).read_text(encoding='utf-8-sig'))
        for m in manifest['music']:
            assert m['id'] not in music, 'Duplicate candidate ID'
            music[m['id']]=m
    for m in music.values():
        f=root/m['path'];assert f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest()==m['sha256']
    ids=[s['id'] for s in data['shots']];by_id={s['id']:s for s in data['shots']};covered=[]
    for section in config['sections']:
        group=ids[ids.index(section['first_shot']):ids.index(section['last_shot'])+1];covered+=group
        section['start']=by_id[group[0]]['start_second'];section['end']=by_id[group[-1]]['end_second']
        for cid in section['candidates']:assert cid in music
        for sid in group:
            s=by_id[sid];s['bgm_section']=section;s['effect_design']=config['effects'][sid]
    assert covered==ids and set(config['effects'])==set(ids)
    for sid,override in config.get('shot_overrides',{}).items():
        assert sid in by_id
        assert len(override['candidates'])==len(set(override['candidates']))
        assert all(cid in music for cid in override['candidates'])
        shot=by_id[sid]
        shot['bgm_section']=dict(override,id='SHOT-'+sid,start=shot['start_second'],end=shot['end_second'],first_shot=sid,last_shot=sid)
    return config,music

def candidate_cards(section,music,shot_start):
    e=lambda s:html.escape(str(s),quote=True)
    cards=[]
    if not section['candidates']:
        return '<p class="sound-empty">此段暂不铺BGM，保留环境与动作声音。</p>'
    for cid in section['candidates']:
        m=music[cid]
        context=' · '.join(x for x in [m.get('display_title'),m.get('work','葬送的芙莉莲')] if x)
        cards.append(f'<div class="music-reference"><strong>{e(m["title"])}</strong><span class="muted">{e(context)}</span><div class="music-actions"><button class="music-audition" data-music="{e(cid)}">播放 / 继续此曲</button><a href="#music-library" data-start="{shot_start}">比较本画面候选 ↗</a></div></div>')
    return ''.join(cards)

def dialogue_audio(s,url):
    e=lambda t:html.escape(str(t),quote=True)
    if not s['dialogue_cues']:
        return '<p class="muted">'+('本镜无对白。' if s['dialogue']=='无对白' else '暂无本镜对应配音，以现行台词／字幕预演。')+'</p>'
    return ''.join(f'<label class="dialogue-sample">临时读稿 · {e(c["speaker"])}<audio class="standalone-audio" controls preload="none" src="{url(c["file"])}" aria-label="{e(s["id"])} 临时读稿 {e(c["speaker"])}"></audio></label>' for c in s['dialogue_cues'])
