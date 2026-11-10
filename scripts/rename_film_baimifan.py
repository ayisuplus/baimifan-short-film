"""Adopt the author's title without migrating IDs, media paths or browser storage."""
import copy,hashlib,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];REC='后期/片名确认-v001'
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def save(p,v):
 f=R/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
base=read('镜头设计/shot-plan-v0.53r1.json');p=copy.deepcopy(base)
for old,new in [('镜头设计/带图分镜.html','镜头设计/带图分镜-旧题穿云-v053r1.html'),('00_打开项目.html','00_打开项目-旧题穿云.html')]:
 if not (R/new).exists():shutil.copy2(R/old,R/new)
p.update(version='v0.53r2',report_revision='v053r2',film_title='白米饭',title='《白米饭》带图分镜 v0.53r2 · 片名确认',source_manifest='镜头设计/shot-plan-v0.53r1.json',story_script='剧本/白米饭-场景剧本-v0.53r2.md',audio_arrangement=REC+'/预演编排-v053r2.json',music_adoption=REC+'/作者确认选曲-v053r2.json')
p['revision_notes']=dict(previous_manifest=p['source_manifest'],modified_image_ids=[],added_ids=[],moved_ids=[],boundary='作者正式将片名改为《白米饭》。仅改片名及显示入口，全部镜头、对白、图像、声音与选曲保持。旧目录、稳定ID、历史文件名和浏览器存储键保留。')
script=(R/base['story_script']).read_text(encoding='utf-8').replace('# 《穿云》场景剧本','# 《白米饭》场景剧本',1).replace('版本：v0.53r1','版本：v0.53r2',1)
(R/p['story_script']).write_text(script,encoding='utf-8');out='镜头设计/shot-plan-v0.53r2.json';save(out,p)
adopt=read(base['music_adoption']);adopt.update(version='v053r2',film_title='白米饭',previous=base['music_adoption'],source_plan=out,source_plan_sha256=sha(R/out));save(p['music_adoption'],adopt)
audio=read(base['audio_arrangement']);audio.update(version='v053r2-title-baimifan',film_title='白米饭',shot_plan=out,shot_plan_sha256=sha(R/out),adopted_music=p['music_adoption'],previous=base['audio_arrangement']);save(p['audio_arrangement'],audio)
assets=read('资产/assets.json');assets['title']=assets['title'].replace('《穿云》','《白米饭》');save('资产/assets.json',assets)
rules=R/'AGENTS.md';text=rules.read_text(encoding='utf-8');text=text.replace('# 《穿云》制作规则','# 《白米饭》制作规则',1).replace('AI 娘短片《穿云》','AI 娘短片《白米饭》',1)
note='\n## 正式片名（2026-10-25）\n\n作者确认片名为《白米饭》，旧题《穿云》停用。现有穿云目录、CY镜号、历史文件及浏览器选曲存储键保留，仅用于稳定引用，不代表作品仍使用旧题。新内容与对外展示统一使用《白米饭》。\n'
if '## 正式片名（2026-10-25）' not in text:text+=note
rules.write_text(text,encoding='utf-8')
progress=R/'制作进度.md';text=progress.read_text(encoding='utf-8').replace('# 《穿云》制作进度','# 《白米饭》制作进度',1).replace('更新：2026-10-25。片名暂定。','更新：2026-10-25。正式片名：《白米饭》。',1)
note='\n## 2026-10-25：正式改名《白米饭》（v0.53r2，当前入口）\n\n作者确认本片与川渝已无关联，正式改名《白米饭》。预演标题、项目首页、资产图册、当前剧本及选曲导出名同步；132镜434秒、图片、对白、BGM与终审结论不变。旧目录、历史文件名、CY镜号及浏览器选曲键继续保留以保障引用。当前剧本为[白米饭-场景剧本-v0.53r2](剧本/白米饭-场景剧本-v0.53r2.md)。\n'
if '## 2026-10-25：正式改名《白米饭》' not in text:text=text.replace('正式片名：《白米饭》。','正式片名：《白米饭》。\n'+note,1)
progress.write_text(text,encoding='utf-8')
report=R/'后期/最终审查-v053/最终审查与交接.md';text=report.read_text(encoding='utf-8').replace('# 《穿云》最终审查与交接','# 《白米饭》最终审查与交接',1).replace('当前入口：**v0.53r1','当前入口：**v0.53r2',1).replace('主计划为[shot-plan-v0.53r1.json](../../镜头设计/shot-plan-v0.53r1.json)','主计划为[shot-plan-v0.53r2.json](../../镜头设计/shot-plan-v0.53r2.json)')
if '片名确认补记：' not in text:text=text.replace('## 文案与叙事结论','片名确认补记：作者于同日正式改名《白米饭》。v0.53r2仅更新片名与展示入口，下文v0.53r1审查证据及结论继续适用。\n\n## 文案与叙事结论',1)
report.write_text(text,encoding='utf-8')
entry='''<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>白米饭 · 制作入口</title>
<style>body{max-width:760px;margin:8vh auto;padding:28px;background:#f3eee5;color:#292c30;font:18px/1.8 system-ui,'Microsoft YaHei',sans-serif}h1{font-size:42px}a{display:block;padding:20px 26px;margin:16px 0;border:1px solid #dcd3c5;border-radius:10px;color:inherit;text-decoration:none;background:#fffaf3}small{display:block;opacity:.75;font-size:14px}</style>
<h1>白米饭</h1><p>从一碗饭开始，回到一碗饭。</p><p><strong>v0.53r2 · 132镜 · 7分14秒 · 七首用曲已定</strong></p>
<a href="镜头设计/带图分镜.html#selection-overview">选曲总览与预演台<small>132镜归属保持 · Kimi出场9镜使用 let the stars fall down</small></a>
<a href="剧本/白米饭-场景剧本-v0.53r2.md">当前场景剧本<small>正式片名《白米饭》 · 既定对白与咏唱保持</small></a>
<a href="资产/资产图册.html">资产图册<small>人物与场景素材</small></a>
<a href="后期/最终审查-v053/最终审查与交接.md">最终审查与后续交接<small>全片静帧、文案与用曲复核 · 局部修图与动态声音待办</small></a>
<details><summary>历史制作记录</summary><a href="00_打开项目-旧题穿云.html">旧题阶段制作入口<small>仅供追溯；当前方案以本页为准</small></a></details></html>
'''
(R/'00_打开项目.html').write_text(entry,encoding='utf-8')
assert p['shots']==base['shots'];assert adopt['marks']==read(base['music_adoption'])['marks']
save(REC+'/改名记录.json',dict(date='2026-10-25',title='白米饭',previous_title='穿云',current_plan=out,current_script=p['story_script'],shots=132,seconds=434,protected='全部shots逐项相等，选曲marks相等；不迁移目录与存储键'))
print('Title updated: 白米饭; 132 shots unchanged')
