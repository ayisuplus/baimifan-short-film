"""Render the project storyboard and a timed still-frame previs. Images are never modified."""
import argparse, hashlib, html, json, math, re, sys, wave
from pathlib import Path
from urllib.parse import quote

def e(s):
    return html.escape(str(s), quote=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--manifest", default="镜头设计/shot-plan-v0.56.json")
    args = ap.parse_args()
    root = args.root.resolve()
    manifest = root / args.manifest
    data = json.loads(manifest.read_text(encoding="utf-8-sig"))
    from previs_audio import load_audio, candidate_cards, dialogue_audio
    audio_config, music = load_audio(root, data, manifest)
    adopted_marks={}
    if data.get('music_adoption'):
        adopted=json.loads((root/data['music_adoption']).read_text(encoding='utf-8-sig'))
        adopted_marks=adopted['marks']
        assert set(adopted_marks)=={s['id'] for s in data['shots']}
        assert all(mid in music for mid in adopted_marks.values())
    shared = root.parent.parent / "OpenCut/toolkit/scripts/atlas"
    sys.path.insert(0, str(shared))
    from build_atlas import validate
    stats = validate(data, root)
    screenplay = (root / data["story_script"]).read_text(encoding="utf-8-sig")
    elapsed = 0
    for s in data["shots"]:
        assert s["source_quote"] in screenplay, f"Source passage missing: {s['id']}"
        assert s["start_second"] == elapsed, f"Timeline gap: {s['id']}"
        elapsed += s["seconds"]
        assert s["end_second"] == elapsed
        if "time_caption" in s:
            cap = s["time_caption"]
            assert cap["text"] and 0 <= cap["offset"] < s["seconds"]
            assert 0 < cap["duration"] <= s["seconds"] - cap["offset"]
        if "split_screen_reveal" in s:
            reveal = s["split_screen_reveal"]
            assert reveal["columns"] == len(reveal["offsets"]) == len(reveal["labels"])
            assert reveal["offsets"][0] == 0 and reveal["offsets"] == sorted(set(reveal["offsets"]))
            assert reveal["offsets"][-1] < s["seconds"]
        r = s["panel_region"]
        assert all(math.isfinite(r[k]) for k in ("x","y","w","h"))
        assert 0 <= r["x"] < 1 and 0 <= r["y"] < 1 and r["w"] > 0 and r["h"] > 0
        assert r["x"]+r["w"] <= 1.000001 and r["y"]+r["h"] <= 1.000001
        for c in s["dialogue_cues"]:
            with wave.open(str(root/c["file"]), "rb") as w:
                c["duration"] = w.getnframes()/w.getframerate()
                c["sample_rate"] = w.getframerate()
            assert c["offset"]+c["duration"] <= s["seconds"], f"Dialogue clipped: {s['id']}"
    assert elapsed == data["total_seconds"]
    assert len({s["id"] for s in data["shots"]}) == len(data["shots"])
    for scene in data["scenes"]:
        ss = [s for s in data["shots"] if s["scene"] == scene["id"]]
        assert scene["shot_ids"] == [s["id"] for s in ss]
        assert scene["seconds"] == sum(s["seconds"] for s in ss)
    invitations = [s for s in data["shots"] if s["id"].startswith("CY026") and s["id"] != "CY026"]
    assert invitations and all(s["scene"] == "S05" and "回闪" in s["framing"] for s in invitations)
    if data.get("revision") == "v009":
        ids = [s["id"] for s in data["shots"]]
        assert "CY026" not in ids and "CY015A" not in ids
        assert ids[ids.index("CY011"):ids.index("CY011")+3] == ["CY011","CY011A","CY012"]
        assert ids[ids.index("CY027B3")+1] == "CY027C"
        assert ids[ids.index("CY026E")+1] == "CY024A"
    if data.get("revision") in ("v010", "v011", "v012", "v013", "v014", "v015", "v016", "v017", "v018", "v019", "v020", "v021", "v022", "v023", "v024", "v025", "v026", "v027", "v028", "v029", "v030", "v031", "v032", "v033", "v034", "v035", "v036", "v037", "v038", "v039", "v040", "v041", "v042", "v045", "v046", "v047", "v048"):
        ids = [s["id"] for s in data["shots"]]
        for sequence in [["CY004B","CY004C","CY004D","CY005"], ["CY009","CY010","CY009A","CY010A"], ["CY022B",*(["CY022B2"] if data.get("revision") in ("v021", "v022", "v023", "v024", "v025", "v026", "v027", "v028", "v029", "v030", "v031", "v032", "v033", "v034", "v035", "v036", "v037", "v038", "v039", "v040", "v041", "v042", "v045", "v046", "v047", "v048") else []),*(["CY022B1"] if data.get('revision') in ('v016','v017','v018','v019','v020','v021','v022','v023','v024','v025','v026','v027','v028','v029','v030','v031','v032','v033','v034','v035','v036','v037','v038','v039','v040','v041','v042','v045','v046','v047','v048') else []),"CY026","CY022C","CY023","CY024",*(["CY024R"] if data.get("revision")=="v048" else []),*(["CY024K0","CY024K1",*(["CY024K1A"] if data.get("revision") in ("v042","v045", "v046", "v047", "v048") else []),"CY024K2",*(["CY024K2A"] if data.get("revision") in ("v046","v047", "v048") else []),"CY024K3","CY024K4"] if data.get("revision") in ("v041","v042", "v045", "v046", "v047", "v048") else ["CY024K1","CY024K2"] if data.get("revision")=="v040" else []),"CY023A","CY026A"], ["CY011","CY011A","CY012"], ["CY027B3","CY027C"], ["CY026E",*(["CY024A0"] if data.get("revision") in ("v037","v038", "v039", "v040", "v041", "v042", "v045", "v046", "v047", "v048") else []),"CY024A"]]:
            if 'CY024K00' in ids and 'CY024K0' in sequence:
                sequence.insert(sequence.index('CY024K0'), 'CY024K00')
            start = ids.index(sequence[0])
            assert ids[start:start+len(sequence)] == sequence, sequence
        assert "CY015A" not in ids
    for s in data["shots"]:
        for cue in s.get("subtitle_cues", []):
            assert cue["text"] and 0 <= cue["offset"] < s["seconds"]
            assert 0 < cue["duration"] <= s["seconds"] - cue["offset"]
    assert all(not s["dialogue_cues"] for s in data["shots"] if s["dialogue"] == "无对白")
    out = root/"镜头设计/带图分镜.html"
    def url(path):
        return quote("../"+str(path).replace("\\","/"), safe="/")
    def frame(s, cls=""):
        r=s["panel_region"]; w,h=s["page_size"]
        return f'<div class="frame {cls}" style="aspect-ratio:{r["w"]*w}/{r["h"]*h}"><img loading="lazy" src="{url(s["presentation"]["path"])}" alt="{e(s["presentation"]["visible"])}" style="width:{100/r["w"]:.7f}%;height:{100/r["h"]:.7f}%;left:{-100*r["x"]/r["w"]:.7f}%;top:{-100*r["y"]/r["h"]:.7f}%"></div>'
    def timecode(n):
        return f"{int(n)//60:02d}:{int(n)%60:02d}"
    css=(root/"scripts/storyboard.css").read_text(encoding="utf-8")
    js=(root/"scripts/storyboard-player.js").read_text(encoding="utf-8")
    music_js=(root/"scripts/storyboard-audio.js").read_text(encoding="utf-8")
    marks_js=(root/"scripts/storyboard-marks.js").read_text(encoding="utf-8")
    p=[f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(data["title"])}</title><style>{css}</style></head><body>']
    p.append('<header class="hero"><div class="wrap"><p class="eyebrow">穿云 / STORYBOARD 01</p><h1>一碗饭，一场赴约。</h1><p class="intro">从街市的第一次邀请，到教堂的破门营救，再回到阳光下的长椅。</p><div class="facts"><span><b>6</b> 场</span><span><b>34</b> 镜</span><span><b>02:56</b> 预演时长</span><span class="pill">粗分镜候选</span></div>')
    p.append(f'<nav><a href="#selection-overview">选曲总览</a><a href="#previs">播放预演</a><a href="#music-library">当前画面候选音乐</a><a href="#story">逐镜阅读</a><a href="{url(data["asset_atlas"])}">资产图册 ↗</a><a href="{url(data["story_script"])}">场景剧本 ↗</a></nav></div></header>')
    if data.get('roughcut_preview'):
        p.append(f'<div class="wrap"><p><a href="{url(data["roughcut_preview"])}">历史配乐粗剪 v002 · 69镜239秒 ↗</a> · 旧选曲仅供对照，扩充候选已在下方逐镜接入。</p></div>')
    p.append('<main class="wrap"><section id="previs" class="previs"><div class="section-head"><div><p class="eyebrow">画面 · 动作 · 台词 · BGM · 音效</p><h2>声音与画面预演台</h2></div><span id="play-status">已暂停</span></div><p class="muted">先播放音乐，再手动点击画面或切换镜头。音乐与画面独立控制；当前画面的候选集中在下方，切镜不会停乐。先在选曲总览确认已有选择，再进入当前画面试听。S01–S06是段落，CY编号是具体镜头。</p>')
    p.append('<section id="selection-overview" class="selection-overview"><div class="section-head"><h3>选曲总览</h3><strong id="selection-count"></strong></div><p class="muted">这里显示已经选定的音乐。段内只标记了一镜时，会注明具体镜号；需要整段沿用，再点“整段使用此曲”。</p><div id="selection-scenes"></div><div class="selection-tools"><button id="selection-undo" disabled>撤销上次选曲修改</button><button id="selection-export">导出当前选择</button></div><details id="selection-detail"><summary>逐镜选曲明细</summary><label><input type="checkbox" id="selection-only-marked" checked> 只看已选镜头</label><div class="selection-table-wrap"><table><thead><tr><th>段落</th><th>镜头</th><th>已选 BGM</th><th>操作</th></tr></thead><tbody id="selection-rows"></tbody></table></div></details></section>')
    p.append('<div class="quick-nav"><a class="overview-link" href="#selection-overview">选曲总览 ↑</a><label>快捷选镜 <select id="quick-shot" aria-label="快捷选择镜头">')
    for sc in data['scenes']:
        p.append(f'<optgroup label="{e(sc["id"])} · {e(sc["title"])}">')
        for shot in data['shots']:
            if shot['scene']==sc['id']:
                p.append(f'<option value="{e(shot["id"])}">{e(shot["id"])} · {timecode(shot["start_second"])} · {e(shot["title"])}</option>')
        p.append('</optgroup>')
    p.append('</select></label><div class="quick-current"><strong id="quick-current-shot"></strong><span id="quick-current-music">尚未选择音乐</span><span id="quick-marked-music">本镜已选 BGM：未标记</span></div></div>')
    p.append('<div class="screen"><div id="stage" class="frame" style="aspect-ratio:16/9"><img id="stage-image" alt=""></div><div class="overlay"><span id="stage-scene"></span><span id="stage-title"></span></div><div id="time-caption" class="time-caption" aria-live="off"></div><div id="subtitle" class="subtitle" aria-live="off"></div></div>')
    p.append('<div class="transport"><button id="prev" aria-label="上一镜">← 上一镜</button><button id="play" class="primary">播放画面</button><button id="next" aria-label="下一镜">下一镜 →</button><time id="clock">00:00 / 02:56</time><label class="voice"><input id="voice" type="checkbox">随画面临时读稿</label></div><input id="seek" class="seek" type="range" min="0" max="176" step="0.05" value="0" aria-label="预演时间"><div class="player-info"><p><b>动作</b><span id="stage-action"></span></p><p><b>声音</b><span id="stage-sound"></span></p><a id="shot-link" href="#CY001">查看本镜</a></div><p id="audio-status" class="muted" role="status">点击播放后启用本地临时读稿。对白原文保留；英文角色名使用中文近似读音。</p>')
    p.append('<div class="scene-jumps">')
    for sc in data["scenes"]:
        first=next(s for s in data["shots"] if s["scene"]==sc["id"])
        p.append(f'<button class="scene-jump" data-start="{first["start_second"]}"><small>{sc["id"]} · {sc["seconds"]} 秒</small>{e(sc["title"])}</button>')
    p.append('</div><div class="sound-deck"><section class="deck-panel"><h3>动作</h3><p id="deck-action"></p></section><section class="deck-panel"><h3>台词</h3><p id="deck-dialogue" class="dialogue"></p><div id="deck-dialogue-timing"></div><p id="deck-voice-state" class="muted"></p><div id="deck-dialogue-audio"></div></section><section id="music-library" class="deck-panel deck-bgm"><h3>BGM <small>当前镜头的选定结果与候选</small></h3><div class="music-mark-state"><strong id="music-mark-summary"></strong><p id="music-scene-choice"></p><a href="#selection-overview">查看本段与全片选择 ↑</a><p id="music-mark-storage" class="muted" role="status"></p></div><details class="audition-notes"><summary>本镜选曲参考</summary><p id="deck-bgm-note"></p></details><div class="music-transport"><h4>试听播放器 <small>播放不等于选定</small></h4><label>切换试听 <select id="music-select" aria-label="快捷选择候选音乐"><option value="">选择本镜候选</option></select></label><strong id="music-current">尚未选择音乐</strong><div class="music-progress"><input id="music-seek" type="range" min="0" max="1" step="0.1" value="0" disabled aria-label="音乐进度"><output id="music-clock">00:00 / 00:00</output></div><audio id="music-audio" preload="none"></audio><div class="music-settings"><label>试听音量 <input id="music-volume" type="range" min="0" max="1" step="0.01" value="0.28"></label><button id="music-resume" disabled>继续当前音乐</button><button id="music-stop">暂停音乐</button></div><p id="music-status" role="status">选择任意候选开始试听，画面保持当前位置。</p></div><div id="deck-bgm-list"></div></section><section class="deck-panel"><h3>音效 / 环境声</h3><p id="deck-effects"></p><p class="muted">设计说明 · 尚未制作音效音轨</p><details><summary>原始声音与同步说明</summary><p id="deck-source-sound"></p></details></section></div></section><section id="story"><div class="section-head"><div><p class="eyebrow">逐镜核对与试听</p><h2>每张画面下的声音</h2></div><span class="muted">点击画面，在预演里定位</span></div><p class="muted">画面下保留建议曲目和试听入口；同一画面的候选在预演台放在一起比较。点击画面定位镜头，音乐持续播放。</p>')
    for sc in data["scenes"]:
        page_links=' · '.join(f'<a href="{url(path)}">原图 {i+1} ↗</a>' for i,path in enumerate(sc['pages']))
        p.append(f'<section class="scene" id="{sc["id"]}"><div class="scene-head"><h3><span>{sc["id"]}</span> {e(sc["title"])}</h3><span>{page_links}</span></div><div class="shots">')
        for s in [x for x in data["shots"] if x["scene"]==sc["id"]]:
            p.append(f'<article class="shot" id="{s["id"]}"><header><span class="shot-id">{s["id"]}</span><span>{timecode(s["start_second"])}—{timecode(s["end_second"])}</span><strong>{s["seconds"]}s</strong></header><button class="shot-play" data-start="{s["start_second"]}" aria-label="在预演中查看 {s["id"]}">{frame(s)}</button><div class="shot-body"><h4>{e(s["title"])}</h4><p class="framing">{e(s["framing"])}</p><h5>动作</h5><p>{e(s["action"])}</p><h5>台词</h5><p class="dialogue">{e(s["dialogue"])}</p>'+dialogue_audio(s,url)+f'<h5>BGM · 选定结果</h5><p class="shot-choice">本镜已选：未选定</p><details><summary>查看本镜候选</summary><p class="muted">{e(s["bgm_section"]["note"])}</p>'+candidate_cards(s['bgm_section'],music,s['start_second'])+f'</details><h5>音效 / 环境声</h5><p>{e(s["effect_design"])}</p><p class="muted">设计说明 · 未制作音轨</p><details><summary>原始声音与同步说明</summary><p>{e(s["sound"])}</p></details><details><summary>画面限制与镜头接续</summary>')
            if "time_caption" in s:
                cap=s["time_caption"]
                p.append(f'<p>剪辑字幕：<b>{e(cap["text"])}</b> · {cap["offset"]}—{cap["offset"]+cap["duration"]} 秒（未写入原图）</p>')
            p.append(f'<dl><dt>图中实际可见</dt><dd>{e(s["presentation"]["visible"])}</dd><dt>画面限制</dt><dd>{e(s["presentation"]["missing"])}</dd><dt>开始状态</dt><dd>{e(s["entry_state"])}</dd><dt>结束状态</dt><dd>{e(s["exit_state"])}</dd><dt>下一镜</dt><dd>{e(s["next_link"])}</dd></dl><ul>')
            p.extend(f'<li>{e(x)}</li>' for x in s["invariants"])
            p.append('</ul></details><details><summary>来源与视觉参考</summary>')
            p.append(f'<blockquote>{e(s["source_quote"])}</blockquote><p class="muted">以上摘自既有场景剧本；镜头调度为本轮新增候选。</p><ul>')
            p.extend(f'<li><a href="{url(r["path"])}">{e(Path(r["path"]).name)}</a> · {e(r["role"])}</li>' for r in s["refs"])
            p.append('</ul></details></div></article>')
        p.append('</div></section>')
    p.append('</section><section class="notes"><h2>这版看什么</h2><p>'+e(data.get('review_focus','检查角色动作、镜头接续和整体节奏。'))+'</p><details><summary>连续性与制作边界</summary><ul>')
    p.extend(f'<li>{e(v)}</li>' for v in data["continuity"].values())
    media_note = '本版逐镜使用完整原画，旧分格仅作为历史参考；有意设计的快闪分屏保留。原始 PNG、版本、输入引用和完整提示词保存在项目生成记录中。' if data.get('revision') in ('v009','v010','v011','v012','v013','v014','v015','v016','v017','v018','v019','v020','v021','v022','v023','v024','v025','v026','v027','v028','v029','v030','v031','v032','v033','v034','v035','v036','v037','v038','v039','v040','v041','v042','v045','v046','v047','v048') else '本页采用未修改的整页生成图，通过显示视窗展示各格；原始 PNG、版本、输入引用和完整提示词保存在项目生成记录中。'
    if data.get('revision') in ('v031','v032','v033','v034','v035','v036','v037','v038','v039','v040','v041','v042','v045','v046','v047','v048'):
        media_note = '本版以独立原画为主，CY024A7云心和CY024A4火前局部使用声明的视窗；水滴沿用v0.30图。原始图片未作像素裁改，完整提示词及输入保存在项目生成记录中。'
    if data.get('revision') in ('v041','v042','v045','v046','v047','v048'):
        media_note = '本版以独立原画为主，CY024A7云心使用声明的视窗，CY024A4已换为固定脚托的新完整特写；水滴沿用v0.30图。原始图片未作像素裁改，完整提示词及输入保存在项目生成记录中。'
    if data.get('revision') in ('v045','v046','v047','v048'):
        media_note = '本版以独立原画为主，CY024A7云心使用声明的视窗，CY024A4为Kimi蹲下查看踝链的双人画面；水滴沿用v0.30图。原始图片未作像素裁改，完整提示词及输入保存在项目生成记录中。'
    if data.get('picture_revision') == 'v050':
        media_note = '本版CY024A7为独立俯冲俯视图，CY024A5A前移为破顶特写；GPT居中结印盘龙，再解印前指。纯水云海复用已生成候选，其余五张为新图。原图与输入记录保留；静帧不等于动作已经连续生成。'
    if data.get('picture_revision') == 'v051':
        media_note = '本版仅重构CY024A5A与CY024B的机位：贴近破口超广角迎拍、教主侧后低机位撞盾。其余129镜、时长、台词与七首BGM保持；v0.50原图与输入保留。新图待作者审阅，动态尚未制作。'
    if data.get('picture_revision') == 'v052':
        media_note = '本版修订蓝眼、黑焰火把、静止对视、攻击与洪流、战后俯视，并新增2.5秒窗外Kimi全身显形；原窗影改窗外举刃近景。罩边允许浅水低浪。132镜434秒，旧镜时长与七首BGM保持，Kimi新镜沿用已定专曲。原图和输入保留，连续动态尚未制作。'
    if data.get('picture_revision') == 'v053':
        media_note = '撞盾接洪流冲人，再接B3浅水环境余波与罩内安抚；CY028C改锁痕与微光，CY028B去除挂水。132镜434秒、对白与七首选曲保持；历史图和输入保留，新图待作者审阅，动态尚未制作。'
    if data.get('picture_revision') == 'v054':
        media_note = 'Kimi显形改为4秒正后方远景，月光从镜头左后侧流入，凝为面向完整彩窗的背影。起中终参考按时间切换静帧，仅说明状态，不是连续动画。132镜435.5秒；其他镜头时长、对白与七首选曲保持。旧侧面候选保留，新图待作者审阅。'
    p.append('<li>角色、服装和场景延续当前资产；小鱼身份以原始捧饭母本优先。四视图中的补全细节仍为候选。</li><li>'+media_note+'</li><li>静帧预演不等于视频已生成；正式配音、配乐重剪和连续动态仍待完成。</li></ul></details></section></main>')
    payload=[dict(s, image_url=url(s["presentation"]["path"]), state_references=[dict(v,url=url(v['path'])) for v in s.get('state_references',[])], audio=[dict(c,url=url(c["file"])) for c in s["dialogue_cues"]]) for s in data["shots"]]
    music_payload={k:dict(m,url=url(m['path'])) for k,m in music.items()}
    p.append(f'<footer class="wrap">《穿云》 · 带图分镜 {e(data["version"])} · 选曲总览与明确标记v010 · 原稿与历史资产保留</footer><script id="shot-data" type="application/json">'+json.dumps(payload,ensure_ascii=False).replace("</","<\\/")+'</script><script id="music-data" type="application/json">'+json.dumps(music_payload,ensure_ascii=False).replace('</','<\\/')+'</script><script>'+js+'</script><script>'+music_js+'</script><script>'+marks_js+'</script></body></html>')
    document="".join(p)
    film_title=data.get('film_title','穿云')
    document=document.replace('穿云 / STORYBOARD',e(film_title)+' / STORYBOARD').replace('《穿云》 · 带图分镜','《'+e(film_title)+'》 · 带图分镜')
    if data.get('film_title'):
        document=document.replace('<h1>一碗饭，一场赴约。</h1>','<h1>'+e(film_title)+'</h1>')
    if adopted_marks:
        frozen='<script id="adopted-music-data" type="application/json">'+json.dumps(adopted_marks,ensure_ascii=False).replace('</','<\\/')+'</script>'
        document=document.replace('<script id="shot-data"',frozen+'<script id="shot-data"',1)
    document=document.replace("<b>34</b>", f"<b>{len(data['shots'])}</b>").replace("<b>02:56</b>","<b>"+timecode(elapsed)+"</b>").replace("00:00 / 02:56","00:00 / "+timecode(elapsed)).replace('max="176"', f'max="{elapsed}"').replace("粗分镜 v0.1", "粗分镜 "+data["version"]).replace("带图分镜 v0.1", "带图分镜 "+data["version"])
    document=document.replace('<span class="pill">粗分镜候选</span>','<span class="pill">'+e(data["version"])+' · 粗分镜候选</span>')
    document=document.replace('STORYBOARD 01','STORYBOARD '+e(data['version']))
    document=document.replace(' · 粗分镜候选',' · 用曲已确认，剪辑待制作' if adopted_marks else ' · 声音试配中')
    document=document.replace('<div class="player-info">','<div class="player-info legacy-info">')
    document=document.replace('<p class="intro">从街市的第一次邀请，到教堂的破门营救，再回到阳光下的长椅。</p>','<p class="intro">从街市的第一次邀请，到教堂的破门营救，再回到阳光下的长椅。</p><p class="intro">'+e(data.get('review_intro','本版延续既有故事与角色。'))+'</p>')
    out.write_text(document,encoding="utf-8")
    report={"schema":1,"storyboard":str(out),"shots":stats["shots"],"duration_seconds":elapsed,"scenes":len(data["scenes"]),"dialogue_clips":sum(len(s["dialogue_cues"]) for s in data["shots"]),"source_passages_verified":len(data["shots"]),"video_produced":False,"image_editing":"none by renderer; original images displayed using declared regions","audio_review":"duration checked, actual listening pending","script_sha256":hashlib.sha256((root/data["story_script"]).read_bytes()).hexdigest()}
    used_music={cid for s in data['shots'] for cid in s['bgm_section']['candidates']}
    report.update(music_candidates=len(used_music),music_archived=len(music)-len(used_music),effects_descriptions=len(audio_config['effects']),music_status='author track choices adopted; source edits and mix pending' if adopted_marks else 'candidate not adopted',adopted_shots=len(adopted_marks))
    (root/("镜头设计/生成记录/结构核验-"+data.get("report_revision",data.get("revision","v001"))+"-声音预演-v012.json")).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__":
    main()
