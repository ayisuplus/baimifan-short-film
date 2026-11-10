"""Rebuild the existing asset atlas from its single JSON source; keep media intact."""
import argparse
import html
import json
import os
import re
from pathlib import Path
from urllib.parse import quote

parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, required=True)
args = parser.parse_args()
root = args.root.resolve()
data = json.loads((root / "资产/assets.json").read_text(encoding="utf-8"))
out = root / "资产/资产图册.html"
# Retain the established atlas appearance and search interaction.
previous = out.read_text(encoding="utf-8")
style = re.search(r"<style>(.*?)</style>", previous, re.S).group(1)
script = re.search(r"<script>(.*?)</script>", previous, re.S).group(1)
e = lambda value: html.escape(str(value), quote=True)

def url(value):
    path = root / value
    assert path.is_file(), f"Missing asset reference: {value}"
    return quote(os.path.relpath(path, out.parent).replace("\\", "/"), safe="/")

parts = [f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(data["title"])}</title><style>{style}</style><main><header><small>ASSET ATLAS · 图片与元信息共用一份数据源</small><h1>{e(data["title"])}</h1><p>{e(data["scope"])}</p><p>{len(data["assets"])} 项参考 · 点击图片查看原尺寸，来源与历史版本保留</p></header><input aria-label="搜索资产" placeholder="搜索名称、类别或状态" id="search"><div class="grid">']
assert len({a["id"] for a in data["assets"]}) == len(data["assets"])
for a in data["assets"]:
    image_url = url(a["path"])
    searchable = " ".join(a[k] for k in ("name", "category", "status"))
    parts.append(f'<article data-search="{e(searchable)}" id="{e(a["id"])}"><a href="{image_url}"><img loading="lazy" src="{image_url}" alt="{e(a["name"])}"></a><div class="body"><small>{e(a["category"])} · {e(a["version"])}</small><h2>{e(a["name"])}</h2><b>{e(a["status"])}</b><p>{e(a["role"])}</p><p class="muted">限制：{e(a["limits"])}</p><details><summary>编号、来源与附属参考</summary><p>{e(a["id"])}</p><a href="{url(a["source"])}">来源记录</a><ul>')
    parts.extend(f'<li><a href="{url(r["path"])}">{e(r["role"])}</a></li>' for r in a.get("related", []))
    parts.append('</ul></details></div></article>')
parts.append('</div>')
if data.get('sound_manifest'):
    sound = json.loads((root / data['sound_manifest']).read_text(encoding='utf-8'))
    auditions = {}
    if data.get('voice_auditions'):
        audition_record = json.loads((root / data['voice_auditions']).read_text(encoding='utf-8'))
        auditions = {r['role']: r for r in audition_record['results'] if r.get('path')}
    plan = json.loads((root / sound['dialogue_source']).read_text(encoding='utf-8'))
    cues = [(shot['id'], cue) for shot in plan['shots'] for cue in shot.get('dialogue_cues', [])]
    parts.append('<section id="sound"><h1>声音候选 · 配乐与角色试音</h1>')
    parts.append(f'<p>{e(sound["conclusion"])}</p><p>{e(sound["listening_status"])}</p>')
    if sound.get('rights_note'):
        parts.append(f'<details><summary>本轮使用范围核对</summary><p>{e(sound["rights_note"])}</p></details>')
    if sound.get('music_trial'):
        trial = json.loads((root / sound['music_trial']).read_text(encoding='utf-8'))
        parts.append(f'<article id="victory-trial" data-search="Victory 援军登场 试配"><div class="body"><h2>{e(trial["title"])}</h2><p>13 秒 · 破门 → 援军群像 → 压火 → 宝宝认出 GPT。现有静帧配乐试剪，非正式动态视频。</p><video controls playsinline preload="metadata" src="{url(trial["path"])}" style="width:100%;max-height:70vh;background:#111"></video><p>{e(trial["review_status"])}</p><details><summary>截取位置与试剪记录</summary><p>{e(trial["edit"])}</p><p>本地源音频 02:07.28–02:20.28；切点待试听。</p><a href="{url(sound["music_trial"])}">来源与记录</a></details></div></article>')
    parts.append('<h2>配乐试听</h2><div class="grid">')
    for m in sound['music']:
        audio = f'<audio controls preload="metadata" src="{url(m["path"])}" style="width:100%"></audio>' if m.get('path') else f'<p>{e(m.get("audition_note", "原站下载暂未成功，请打开作者页面试听。"))}</p>'
        if m.get('recognition_evidence'):
            audio += f'<p class="muted">熟悉度线索：{e(m["recognition_evidence"])}</p>'
        if m.get('catalog_source'):
            audio += f'<p><a href="{e(m["catalog_source"])}" target="_blank" rel="noopener">官方曲库目录</a></p>'
        excerpt_note = m.get('excerpt_note', '尚未锁定乐句截取位置。')
        parts.append(f'<article data-search="{e(m["title"])} 配乐 BGM"><div class="body"><small>{e(m["id"])} · {e(m["status"])}</small><h2>{e(m["title"])}</h2><p>{e(m["description"])}</p><p>{e(m["role"])}</p>{audio}<p><a href="{e(m["source"])}" target="_blank" rel="noopener">作者／发行页面与试听</a></p><details><summary>来源与使用说明</summary><p>{e(m["attribution"])}</p><a href="{e(m["license_url"])}">使用说明／权利核对</a><p>{e(excerpt_note)}</p></details></div></article>')
    parts.append('</div><h2>角色声线与首句试音</h2>')
    parts.append(f'<p>{len(cues)} 段对白 · {len(sound["casting"])} 位说话角色；其他援军保留无对白反应。台词直接读取当前分镜。</p><div class="grid">')
    for c in sound['casting']:
        actual = [(sid, cue['text']) for sid, cue in cues if cue['speaker'] == c['role']]
        first = next(text for sid, text in actual if sid == c['first_shot'])
        sample = auditions.get(c['role'])
        status = c.get('review_status') or ('首句试音已生成 · 待听审' if sample else c['status'])
        parts.append(f'<article id="voice-{e(c["role"].lower())}" data-search="{e(c["role"])} 声线 配音"><div class="body"><small>{e(status)}</small><h2>{e(c["role"])}</h2><p>{e(c["voice_direction"])}</p><blockquote>{e(first)}</blockquote><p>{e(c["first_acting"])}</p>')
        if sample:
            feedback = c.get('author_feedback', '听感、吐字和角色贴合度尚未验收。')
            note = sample.get('sample_note', '历史首句样本 · 本地 VoxCPM2，未使用博主参考音频。')
            parts.append(f'<audio controls preload="metadata" src="{url(sample["path"])}" style="width:100%"></audio><p class="muted">{e(note)}</p>')
            if sample.get('reference_path'):
                label = sample.get('reference_label', '博主角色参考 · 原片 2.15–6.8 秒回答')
                parts.append(f'<p>{e(label)}</p><audio controls preload="metadata" src="{url(sample["reference_path"])}" style="width:100%"></audio>')
            for alternative in sample.get('alternatives', []):
                parts.append(f'<p><b>{e(alternative["label"])}</b></p><audio controls preload="metadata" src="{url(alternative["path"])}" style="width:100%"></audio>')
            if sample.get('previous_path'):
                previous_label = sample.get('previous_label', '对照：v001 旧版及历史反馈')
                parts.append(f'<details><summary>{e(previous_label)}</summary><audio controls preload="metadata" src="{url(sample["previous_path"])}" style="width:100%"></audio><p>{e(feedback)}</p></details><p>{e(sample.get("review_note", "新版音色、吐字与情绪待听审。"))}</p>')
            else:
                parts.append(f'<p><b>听审：</b>{e(feedback)}</p>')
            if sample.get('workflow_review'):
                parts.append(f'<p><a href="{url(sample["workflow_review"])}">声线工作流核对与对照说明</a></p>')
        if c.get('contrast_shot'):
            second = next(text for sid, text in actual if sid == c['contrast_shot'])
            parts.append(f'<p>首句通过后再测：{e(second)}<br>{e(c["contrast_acting"])}</p>')
        parts.append('<details><summary>本片全部台词</summary><ul>')
        parts.extend(f'<li>{e(sid)} · {e(text)}</li>' for sid, text in actual)
        parts.append('</ul></details></div></article>')
    parts.append('</div><h2>已有作品与音源线索</h2><p>用途见各项记录；已用参考和检索线索分别标明，不代表已取得对外使用授权。</p><div class="grid">')
    for r in sound['voice_references']:
        parts.append(f'<article data-search="{e(r["role"])} {e(r["creator"])} 音源"><div class="body"><small>{e(r["creator"])}</small><h2>{e(r["title"])}</h2><p>{e(r["finding"])}</p><p class="muted">证据：{e(r["evidence"])}</p><a target="_blank" rel="noopener" href="{e(r["url"])}">查看原作品</a></div></article>')
    parts.append('</div><h2>音乐接续方案</h2>')
    for cue in sound['cue_design']:
        parts.append(f'<p><b>{e(" / ".join(cue["scenes"]))}</b> · {e(cue["direction"])}</p>')
    parts.append(f'<details><summary>本轮执行状态</summary><p>{e(sound["generation_status"])}</p><p>{e(sound["search_status"])}</p><a href="{url(data["sound_manifest"])}">来源与执行记录</a></details></section>')
parts.append(f'</main><script>{script}</script></html>')
out.write_text("".join(parts), encoding="utf-8")
print(json.dumps({"assets": len(data["assets"]), "path": str(out)}, ensure_ascii=False))
