"""Render the GB001 research pilot. Never changes the full-board plan or media."""
import hashlib
import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '视频制作/生成板-v002-试写'
source = ROOT / '镜头设计/shot-plan-v0.53r3.json'
shots = json.loads(source.read_text('utf-8'))['shots'][:4]
assets = {a['id']: a for a in json.loads((ROOT / '资产/assets.json').read_text('utf-8'))['assets']}
identity_assets = [assets['CHAR-DEEPSEEK'], assets['CHAR-CLAUDE']]
assert all('四视图/' in a['path'] for a in identity_assets), '身份输入必须为四视图'
paths = [a['path'] for a in identity_assets] + [s['presentation']['path'] for s in shots]
roles = ['小鱼四视图 v003：身份、服装、头身比例；不含饭碗', 'Claude四视图 v001：身份、服装、左侧花饰与头纱', '第1镜：街市空间、日光和远景布局', '第2镜：黑袍夹框与Claude中近景', '第3镜：过肩关系；举碗为过程中的状态', '第4镜：双手、饭碗与无人接住的距离']
refs = []
for slot, (path, role) in enumerate(zip(paths, roles), 1):
    file = ROOT / path
    assert file.is_file(), path
    ref = dict(slot=slot, path=path, purpose=role, usage='普通参考图，非首尾帧', sha256=hashlib.sha256(file.read_bytes()).hexdigest())
    if slot <= 2:
        ref.update(asset_id=identity_assets[slot-1]['id'], asset_status=identity_assets[slot-1]['status'], asset_limits=identity_assets[slot-1]['limits'])
    refs.append(ref)
prompts = {m: (OUT / f'GB001-{m}.txt').read_text('utf-8') for m in ['seedance25', 'minimax-h3']}
assert len(prompts['minimax-h3']) <= 7000
assert all(p.count('你要吃一点吗？') == 1 for p in prompts.values())
assert [s['id'] for s in shots] == ['CY001', 'CY002', 'CY003', 'CY003A']
assert sum(s['seconds'] for s in shots) == 14
assert len(refs) == 6
sections = ['subject_definitions:', 'summary:', 'retention_analysis:', 'detailed_description:', 'overall_soundscape:', 'non_diegetic_music:']
indices = [prompts['minimax-h3'].index(s) for s in sections]
assert indices == sorted(indices)
manifest = dict(status='仅GB001研究试写，待作者审阅；其余32批未迁移', source=str(source.relative_to(ROOT)).replace('\\', '/'), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), request_seconds=15, film_range=[0, 14], discard_range=[14, 15], shot_ids=[s['id'] for s in shots], references=refs, prompt_chars={m:len(p) for m,p in prompts.items()}, checks=['身份槽位绑定资产图册四视图，6份参考路径和哈希', '两稿对白仅一次', '14秒成片+1秒余量', 'H3六节顺序与7000字符内'], media_generation='未上传、未调用模型、未生成或试听', remaining='完整生成板编译器及其余批次尚未迁移；提示词格式与实生成质量需区分')
(OUT / '试写核验.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
cards = ''.join(f'<figure><img src="../../{quote(r["path"])}"><figcaption><b>图片{r["slot"]}</b> · {html.escape(r["purpose"])}</figcaption></figure>' for r in refs)
old = (ROOT / '视频制作/生成板-v001/提示词/GB001-seedance25.txt').read_text('utf-8')
doc = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>白米饭 · GB001 多参考与连续镜头试写</title>
<style>body{margin:0;background:#10151c;color:#e7e9ef;font:16px/1.65 system-ui}main{max-width:1250px;margin:auto;padding:32px}a{color:#90d1f2}h1{font-size:30px;margin-bottom:8px}.muted{color:#acb8c9}.notice{background:#283226;padding:14px;border-left:4px solid #a8c478}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}figure{margin:0;background:#1b2531;border-radius:8px;overflow:hidden}img{width:100%;aspect-ratio:1.78;object-fit:contain;background:#090d12}figcaption{padding:12px}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:12px;border-bottom:1px solid #394451}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#1b2531;padding:20px;border-radius:10px;font:15px/1.8 system-ui}button,select{background:#26384a;color:white;border:1px solid #64849c;padding:10px;border-radius:6px;margin:6px 10px 6px 0}summary{cursor:pointer} @media(max-width:800px){.grid{grid-template-columns:1fr}main{padding:16px}}</style>
<main><a href="../生成板-v001/生成板.html#GB001">← 原生成板v001</a><h1>GB001 · 把相遇连成一个动作过程</h1>
<p class="notice">研究试写：仅此一批，6张参考、4个镜头、15秒请求。原片0–14秒用于正片，14–15秒剪除。原台词、镜序、采用图保留；新增动态调度待审。未生成视频，其余32批仍是旧稿。</p>
<p>捧饭前行 → 被队伍挡住 → 视线相接 → 一次递碗 → 无人接住。素材负责身份和空间，提示词负责变化过程。</p>
<h2>一次上传的参考素材包</h2><p class="muted">以下为计划槽位，执行时必须与实际上传顺序绑定。六张均为参考用途；没有指定首尾帧。图片1、2为人物四视图，约束身份和服装；图片3至6约束构图、动作状态与饭碗。四视图中的四个角度是同一人物，不能生成四人同场。资产图册目前仍标记这两张为“候选待作者审阅”，此处复用为待审输入，不更改资产采用状态。</p>__CARDS__
<h2>镜头之间如何接上</h2><table><thead><tr><th>时间／参考图片</th><th>动作与运镜</th><th>与前后镜的联系</th></tr></thead><tbody>
<tr><td>0–5秒 · 图片3</td><td>眼高侧跟；小鱼停步时摄影机随之减速</td><td>抬眼看右侧，下一镜揭示她看见的人</td></tr>
<tr><td>5–9秒 · 图片4</td><td>有意定镜；Claude回头，黑袍近景继续移动</td><td>脚步、衣料声不断；视线落向左下方的小鱼</td></tr>
<tr><td>9–12秒 · 图片5</td><td>同轴过肩反打；随邀请缓慢小幅前移</td><td>一回举碗；对白结束时碗停在两人之间</td></tr>
<tr><td>12–14秒 · 图片6</td><td>碗沿高度与手位匹配切近景；前移收停</td><td>不重新举碗；等待成为重点，下一批接Claude眼底所见</td></tr>
<tr><td>14–15秒 剪辑余量</td><td>自然蒸汽与呼吸微动</td><td>不新增动作，后期剔除</td></tr></tbody></table>
<h2>完整提示词</h2><select id="model" aria-label="模型"><option value="seedance25">Seedance 2.5 · 中文多参考</option><option value="minimax-h3">MiniMax H3 · 官方Ref2VA结构</option></select><button id="copy">复制当前提示词</button><a id="download" download>下载TXT</a><span id="status" role="status"></span><pre id="prompt"></pre>
<p><a href="../生成板-v001/生成板.html#GB001">查看保留的历史初稿</a></p>
<h2>依据与边界</h2><p><a href="研究与改写说明.md">研究与改写说明</a> · <a href="试写核验.json">素材与结构核验</a></p><p class="muted">H3英文六节采用官方全参考提示词格式，中文台词保持原文。这是文本格式，不代表新增六个API参数；本地/云端实际入口支持的多图能力仍需提交前核实。时间戳是控制意图，不是逐帧保证。</p></main>
<script>const prompts=__DATA__;const selector=document.querySelector('#model');function render(){document.querySelector('#prompt').textContent=prompts[selector.value];document.querySelector('#download').href='GB001-'+selector.value+'.txt';document.querySelector('#status').textContent='';}selector.onchange=render;document.querySelector('#copy').onclick=async()=>{try{await navigator.clipboard.writeText(prompts[selector.value]);document.querySelector('#status').textContent='已复制';}catch(e){document.querySelector('#status').textContent='请下载TXT或选中文字复制';}};render();</script></html>'''
doc = doc.replace('__CARDS__', '<div class="grid">'+cards+'</div>').replace('__OLD__', html.escape(old)).replace('__DATA__', json.dumps(prompts, ensure_ascii=False).replace('</', '<\\/'))
(OUT / '生成板试写.html').write_text(doc, encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=False, indent=2))
