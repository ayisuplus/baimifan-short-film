"""Render the two human entrypoints from the single current-status JSON."""
from pathlib import Path
import json,html
P=Path(__file__).resolve().parent.parent
s=json.loads((P/'当前制作状态.json').read_text('utf8'))
c=s['completed']
status=s.get('status')
archived=status=='archived'
paused=status=='paused'

if archived:
    headline=f"**已定档存档（{s.get('archive_date','—')}）。** {s.get('archive_reason','')}"
    status_line='已定档存档，等作者重新开工'
    note=('定档不等于取消：素材、剧本、时间线全部保留在原位，一个字节都没删。'
          '以后要接着做，从 [定档说明](交接/定档说明.md) 第五节的顺序进——'
          '**先定风格基准图与角色/场景参考图，再谈批量生成**。')
else:
    headline=('**已暂停，显卡已让出。** '+s.get('pause_reason','')) if paused else '**制作中。**'
    status_line='已暂停，显卡已让出' if paused else '制作中'
    note='当前整片仍是达芬奇 v033；v034 还没有回装，不能当成已完成新版。'

rows=[]
if archived:
    rows.append(('这片子现在的状态与根因复盘','[定档说明](交接/定档说明.md)'))
rows.append(('看当前完整剪辑','达芬奇项目 **%s** → 时间线 **`%s`**'%(s['resolve_project'],s['timeline_baseline'])))
rows.append(('连看全片（6分17.5秒无声粗剪）','[全片铺片基线](交接/全片铺片基线.md)'))
if archived:
    rows.append(('以后回来怎么接着做','[定档说明](交接/定档说明.md) 第五节'))
else:
    rows.append(('看下一步要做什么','[接下来做什么](交接/接下来做什么.md)'))
rows.append(('现在到底还缺什么','[当前缺口清单](交接/当前缺口清单.md)'))
rows.append(('全片画风是否统一、哪些镜头要重画','[全片画风统一审查](交接/全片画风统一审查.md)'))
rows.append(('后期那98个目录都是什么、哪个是现行版','[后期目录索引](交接/后期目录索引.md)'))
rows.append(('找剧本、角色、声音或历史版本','[文档导航](交接/文档导航.md)'))
table='\n'.join('| %s | %s |'%r for r in rows)

if archived:
    salvage='\n'.join('- %s'%x for x in s.get('salvageable',[]))
    obsolete='\n'.join('- %s'%x for x in s.get('obsolete',[]))
    steps=(
        '1. 读[定档说明](交接/定档说明.md)、[当前缺口清单](交接/当前缺口清单.md)、[全片画风统一审查](交接/全片画风统一审查.md)。\n'
        '2. 打开[全片铺片基线](交接/全片铺片基线.md)连看一遍 6 分 17.5 秒，确认哪些段落还有救。\n'
        '3. **不要**续跑 v034 的旧任务或 12 条 pending——它们继承的是作废的风格基准。\n'
        '4. 重做时先只做「风格基准组」：1 张定调用画面 + 3–4 张角色/场景/光线参考图，交作者确认后再往下。\n'
        '5. 基准确认后，才谈批量生成与时间线重铺；届时新建版本记录，不复用旧 seed 队列。')
    blocks=f"""
## 定档期间的硬约束

- 不自动恢复 GPU、ComfyUI、RunningHub，不提交任何生成任务——生成闸门只认 `status=active`，当前是 `archived`。
- 不自动重铺时间线、不回装候选、不导出母版。
- 不删除、不移动、不改名任何已有素材与文档。

## 保留可用的

{salvage}

## 明确作废的

{obsolete}

## 以后回来接着做的顺序

{steps}
"""
else:
    blocks=f"""
## 这轮实际做到哪里

- **已迁回达芬奇并保存**：{s['timeline_clips']} 个片段，{s['timeline_frames']} 帧，{s['timeline_fps']}fps，时长 **{s['timeline_timecode']}**。原有时间线和 OpenCut 版本保留。
- **已完成全片问题审查**，正在按二维哥特画风修正空间、动作、特效和剪辑节奏。
- **本轮产物**：{c['key_candidates']} 张关键帧候选、{c['cpu_edited_clips']} 条 CPU 剪辑素材，以及 {c['partial_previews']} 个不完整小节预览。
- **尚未完成**：新视频补生成（目前 {c['new_generated_videos']} 条完成）、完整分段动态验收、v034 新时间线回装。候选图不等于已采用视频。
- **暂停已落实**：{s['cancelled_jobs']} 条排队任务已取消，运行队列为零，模型已卸载；不会自动恢复。已生成文件完整保留。
"""

readme=f"""# 《白米饭》｜从这里开始

{headline}

{note}

## 现在看哪里

| 你要做什么 | 打开这里 |
|---|---|
{table}

也可以双击 [00_打开项目.html](00_打开项目.html)，内容与本页同步。以后不用逐个翻“交接”“进度”或猜哪个版本最新。
{blocks}
## 版本只记这几个

| 版本 | 用途 |
|---|---|
| **达芬奇 v033** | 当前可打开的完整画面基线（{s['timeline_clips']} 片段 / {s['timeline_timecode']}） |
| **v034（已定档）** | 本轮审查与候选；素材作废，保留作溯源 |
| **OpenCut v035** | 全片连看用恢复副本（118 片段 / 0 空隙 / 6:17.5） |

剧本读 [场景剧本 v0.69](剧本/白米饭-场景剧本-v0.69.md)，台词读 [日语对白 v0.69](剧本/白米饭-日语对白-v0.69.md)，人物看 [资产图册](资产/资产图册.html)。其余旧“当前”“最新”记录已列入 [历史文档](交接/历史文档/README.md)，仅作溯源。
"""
(P/'README.md').write_text(readme,'utf8')

if archived:
    cards=(
        '<a class="card" href="交接/定档说明.md">定档说明<br><small>决定、根因复盘、以后接着做的顺序</small></a>'
        '<a class="card" href="交接/全片铺片基线.md">全片铺片基线<br><small>6分17.5秒无声粗剪，118片段、0空隙</small></a>'
        '<a class="card" href="交接/当前缺口清单.md">当前缺口清单<br><small>素材实测与真实缺口分层</small></a>'
        '<a class="card" href="交接/全片画风统一审查.md">全片画风统一审查<br><small>逐镜定级与偏离清单</small></a>'
        '<a class="card" href="剧本/白米饭-场景剧本-v0.69.md">当前剧本 v0.69<br><small>故事、动作与台词</small></a>'
        '<a class="card" href="交接/文档导航.md">资料与历史导航<br><small>角色图册、声音、后期目录索引</small></a>')
    body=f"""
<section><h2>定档存档 · {s.get('archive_date','—')}</h2><p>{html.escape(s.get('archive_reason',''))}</p><p class="muted">定档不等于取消：素材、剧本、时间线全部保留在原位。以后要接着做，从
<a href="交接/定档说明.md">定档说明</a> 第五节的顺序进——先定风格基准图与参考图，再谈批量生成。</p></section>
<div class="grid">{cards}</div>
<section><h2>定档期间的硬约束</h2><table><tr><th>不生成</th><td>不自动恢复 GPU、ComfyUI、RunningHub，不提交任何生成任务（生成闸门只认 <code>status=active</code>，当前是 <code>archived</code>）</td></tr><tr><th>不动工程</th><td>不自动重铺时间线、不回装候选、不导出母版</td></tr><tr><th>不删不改</th><td>不删除、不移动、不改名任何已有素材与文档</td></tr></table></section>
<section><h2>片子的基线事实</h2><table><tr><th>完整画面</th><td>达芬奇 v033 · {s['timeline_clips']} 片段 · {s['timeline_fps']}fps · {s['timeline_timecode']}</td></tr><tr><th>连看入口</th><td>OpenCut「白米饭 · 全片画面 v035」恢复副本 · 118 片段 · 0 空隙 · 6:17.5 · 无声无字幕</td></tr><tr><th>声音</th><td>9 角色声线已选定，缺 12 句录音（GPT 9、小鱼 3）</td></tr></table><p class="muted">这条时间线是「现有最好素材的连看」，不是画风统一后的成片；画风统一要落到成片必须重跑视频。</p></section>
"""
else:
    body=f"""
<section><h2>当前完整剪辑：达芬奇 v033</h2><p>打开项目 <strong>《白米饭》</strong>，选择时间线<br><code>{html.escape(s['timeline_baseline'])}</code></p><p>{s['timeline_clips']} 个片段 · {s['timeline_fps']}fps · {s['timeline_timecode']} · 已保存核验</p><p class="muted">v034 尚未回装。OpenCut v032 和旧时间线保留作备份。</p></section>
<div class="grid"><a class="card" href="交接/接下来做什么.md">接下来做什么<br><small>暂停边界、优先顺序与验收要求</small></a><a class="card" href="交接/当前缺口清单.md">当前缺口清单<br><small>还缺什么、缺哪些素材</small></a><a class="card" href="剧本/白米饭-场景剧本-v0.69.md">当前剧本 v0.69<br><small>故事、动作与台词</small></a><a class="card" href="交接/文档导航.md">资料与历史导航<br><small>角色图册、声音、工程记录</small></a></div>
<section><h2>本轮完成情况</h2><table><tr><th>已完成</th><td>迁回达芬奇；全片审查；{c['key_candidates']} 张关键帧候选；{c['cpu_edited_clips']} 条剪辑素材</td></tr><tr><th>尚未完成</th><td>新视频补生成、完整动态验收、新时间线回装</td></tr><tr><th>暂停状态</th><td>{s['cancelled_jobs']} 条排队任务取消；队列为空，模型已卸载，不自动恢复</td></tr><tr><th>稍后处理</th><td>字幕、配音、BGM；超分仍关闭</td></tr></table><p class="muted">关键帧候选不等于通过的视频。当前完整工程仍是上方 v033。</p></section>
"""

page=f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · 当前项目入口</title><style>
*{{box-sizing:border-box}}body{{max-width:1000px;margin:40px auto;padding:0 24px 40px;background:#101722;color:#ecedf2;font:16px/1.8 system-ui,sans-serif}}a{{color:#a6d6ff}}h1{{font-size:34px;margin-bottom:0}}h2{{font-size:22px}}section{{background:#1b2635;padding:22px 26px;border:1px solid #314051;border-radius:14px;margin:22px 0}}.status{{color:#e5c89c}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}.card{{display:block;padding:18px;background:#253549;border-radius:10px;text-decoration:none}}small,.muted{{color:#afbdcc}}code{{color:#f1d4a9;overflow-wrap:anywhere}}table{{width:100%;border-collapse:collapse}}td,th{{padding:12px 0;text-align:left;border-bottom:1px solid #314051}}@media(max-width:650px){{.grid{{grid-template-columns:1fr}}body{{margin-top:20px;padding:0 16px}}section{{padding:18px}}}}</style></head><body>
<h1>白米饭</h1><p class="status">{status_line} · {s['updated']}</p>
{body}
<p><a href="README.md">文字版项目首页</a> · <a href="交接/定档说明.md">定档说明</a> · <a href="交接/文档导航.md">文档导航</a> · <a href="资产/资产图册.html">人物资产图册</a> · <a href="交接/历史文档/README.md">历史记录</a></p></body></html>"""
(P/'00_打开项目.html').write_text(page,'utf8')
print('Updated README.md and 00_打开项目.html from 当前制作状态.json (status=%s)'%status)
