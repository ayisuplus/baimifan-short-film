"""One-time, non-destructive document consolidation with byte-exact originals."""
from pathlib import Path
import json,hashlib,re,html
P=Path(__file__).resolve().parent.parent
H=P/'交接/历史文档/20261030-整理前'
assert not H.exists(),'One-time archive already exists; do not overwrite originals'
(H/'原件').mkdir(parents=True)
names=['当前交接与TODO-20261030.md','新对话交接-20261026.md','新对话交接-20261029.md','制作进度.md','00_打开项目.html','当前制作状态.json','AGENTS.md']
manifest=[]
def rewrite_link(m):
 t=m.group(1)
 if re.match(r'^(?:https?:|file:|[A-Za-z]:|/|#|mailto:)',t):return m.group(0)
 return ']('+ '../../../'+t+')'
for name in names:
 raw=(P/name).read_bytes();(H/'原件'/name).write_bytes(raw)
 s=raw.decode('utf-8-sig')
 if name.endswith('.md'):
  s='> 历史快照，停留在整理前的状态。文中“当前／最新／下一步”均是当时记录，不作为续作指令。现在请看 [项目首页](../../../README.md)。\n\n'+re.sub(r'\]\(([^\n)]+)\)',rewrite_link,s)
 elif name.endswith('.html'):
  s=s.replace('<meta charset="utf-8">','<meta charset="utf-8"><base href="../../../">',1)
  s=s.replace('<h1>白米饭</h1>','<h1>白米饭 · 历史入口</h1><p>此页只作历史对照。<a href="00_打开项目.html">返回当前项目入口</a></p>',1)
 (H/name).write_text(s,'utf8')
 manifest.append(dict(original=name,archive=str((H/'原件'/name).relative_to(P)),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)))
(H/'备份核验.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf8')
for name in names[:4]:
 (P/name).write_text(f'# 已归档：{name.removesuffix(".md")}\n\n现在统一从 [《白米饭》项目首页](README.md) 查看当前工程、完成情况和待办。\n\n本文件原来的完整内容已保存到 [历史快照](交接/历史文档/20261030-整理前/{name})，不再在此累加状态。旧链接仍可通过此页找到记录。\n','utf8')

state=dict(updated='2026-10-30',status='paused',pause_reason='用户要玩游戏，已清空本轮排队任务并卸载模型；须等用户明确恢复',auto_resume=False,project_root=str(P),handoff='README.md',todo='交接/接下来做什么.md',document_index='交接/文档导航.md',script_version='v0.69',timeline_baseline='v033_OpenCut_Picture_Return',resolve_project='《白米饭》',timeline_clips=118,timeline_frames=9059,timeline_fps=24,timeline_timecode='00:06:17:11',timeline_resolution=[1344,768],timeline_evidence='后期/迁回达芬奇-v033/迁移核验.json',work_in_progress='后期/全片画风与动作统一-v034',wip_installed=False,completed=dict(migration=True,full_film_audit=True,key_candidates=41,new_generated_videos=0,cpu_edited_clips=22,partial_previews=8),cancelled_jobs=65,gpu=dict(running=0,queued=0,models_unloaded=True,evidence='后期/全片画风与动作统一-v034/暂停核验.json'),voices_deferred=True,subtitles_deferred=True,bgm_deferred=True,upscale=False,export_allowed=False,next_action='等用户明确恢复；先审022/028，再按已通过关键帧小批生成视频、审动作、剪辑，最后回装新达芬奇时间线。禁止直接恢复全部65条。',historical_status='交接/历史文档/20261030-整理前/当前制作状态.json')
(P/'当前制作状态.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8')

header='''# 《白米饭》当前执行入口

**2026-10-30：用户要求暂停，让出 GPU 玩游戏。不得自动恢复生成、加载模型或提交已取消任务。**

- 当前状态唯一入口：[README.md](README.md)；待办：[接下来做什么](交接/接下来做什么.md)。
- 当前工程：达芬奇《白米饭》／`v033_OpenCut_Picture_Return`，118片段、9059帧、24fps。v034是进行中的素材与剪辑，尚未回装；不能把候选当成完整修订版。
- 本轮65条待运行任务已取消，最后028关键帧自然完成，模型卸载；字幕、配音、BGM继续暂缓，超分关闭。
- 下方所有“当前”“本节优先”均为历史决定，只在不违背本节和用户新指令时适用。作品约束及原决定保留，不据旧记录恢复作者已剪掉的时长。

---

'''
(P/'AGENTS.md').write_text(header+(P/'AGENTS.md').read_text('utf8'),'utf8')
(P/'交接/文档导航.md').write_text('''# 文档导航

日常只需要 [项目首页](../README.md)。想深入时，再按下表进入；版本号最大的文件不一定是当前工程。

| 想看什么 | 看这一份 | 边界 |
|---|---|---|
| 现在打开哪个工程、完成到哪 | [项目首页](../README.md) | 当前状态入口 |
| 下次具体怎么继续 | [接下来做什么](接下来做什么.md) | 包含暂停约束和制作顺序 |
| 故事、动作和台词 | [场景剧本 v0.69](../剧本/白米饭-场景剧本-v0.69.md) | 文字依据，时长不替代当前剪辑 |
| 日语台词和中文回译 | [日语对白 v0.69](../剧本/白米饭-日语对白-v0.69.md) | 本轮不改配音 |
| 角色长什么样、参考图 | [资产图册](../资产/资产图册.html) | 同时保留候选与采用状态 |
| 达芬奇迁回是否完整 | [v033 迁移说明](../后期/迁回达芬奇-v033/迁移说明.md) | 已保存的完整画面基线 |
| 本轮剪辑已做出的片段 | [分段预览](../后期/全片画风与动作统一-v034/edits/preview.html) | 8个小节，缺镜处分开，非完整新版 |
| 本轮问题与技术记录 | [v034 制作记录](../后期/全片画风与动作统一-v034/制作记录.md) | 逐镜审查、工作流、候选与回执 |
| 配音素材与历史选声 | [配音清单](../声音/正式配音准备-v006/配音清单.html) | 历史声音素材；未按新画面重同步 |
| 之前为什么这样改 | [历史文档](历史文档/README.md) | 只作溯源，不从旧“当前”续作 |

## 各目录的职责

- `剧本/`：故事与文字源；当前读 v0.69，旧稿留作对照。
- `资产/`：人物、服装和场景参考。
- `后期/`：按施工版本保存画面、审查、时间线证据。v033是当前工程，v034尚在制作。
- `声音/`：选声、录音、切分、试听；此次暂缓。
- `镜头设计/`、`视频制作/`：生成前的设计与批次历史，不能将其旧时码覆盖当前剪辑。
- `交接/`：当前待办、导航和历史快照。旧入口只做跳转，不再各写一套“最新”。
- `AGENTS.md`、`scripts/`、JSON、工作流与回执：执行与核验资料，日常看片无需逐个阅读。

原素材路径和历史工程没有搬动，避免达芬奇离线。当前页面由 `scripts/build_project_entry.py` 根据 `当前制作状态.json` 更新；新增状态不要再往旧交接和旧入口顶部不断叠加。
''','utf8')
(P/'交接/历史文档/README.md').write_text('''# 历史文档

这些记录用于追溯决定，不代表当前工程。请从 [项目首页](../../README.md) 继续。

2026-10-30 整理前的完整快照：

- [旧进度流水账](20261030-整理前/制作进度.md)
- [旧暂停交接与 TODO](20261030-整理前/当前交接与TODO-20261030.md)
- [10月29日交接](20261030-整理前/新对话交接-20261029.md)
- [10月26日交接](20261030-整理前/新对话交接-20261026.md)
- [旧网页入口](20261030-整理前/00_打开项目.html)
- [旧规则及历次决定](20261030-整理前/AGENTS.md)

可读副本已修正相对链接。`原件/` 保存整理前逐字节原文件，`备份核验.json` 记录哈希；没有删除原内容。后期各版本和媒体仍在原位置。
''','utf8')
print('Archived originals, redirected four outdated entry files, and created one current status source.')
