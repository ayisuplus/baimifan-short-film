import json, subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
assert json.loads((OUT/'时间线核对.json').read_text('utf8'))['passed']
url='http://127.0.0.1:8978/editor/ae0f78d7-610f-40c9-9a18-cea6be2a24be'
report='后期/小鱼脱手与二维统一-v030/修订说明.md'
banner=f'''## 2026-10-30 当前：小鱼脱手与二维统一 v030

作者认可v029二维画风为全篇方向，本轮仅改037/041。037重绘并重新动画为推离、失衡、撑地、抬头；041重点修小鱼抓袍—衣料绷紧—脱手落地—教徒背向登阶，点火和Claude反应同时二维化，保留原情绪设计。037仍68帧，041仍288帧，内部改为68/70/84/66帧。其他115段内容/位置/长度逐项不变；117段、9142帧，重载核对保存。原v029保留。本机Qwen2.1+H3，超分关闭。未访问Resolve，声音字幕暂缓。入口：[OpenCut v030]({url})、[修订说明]({report})。从1:57:20复看至2:18:13，作者动态终验待定。本节优先于下方历史。

'''
for name in ['AGENTS.md','新对话交接-20261029.md']:
    f=ROOT/name
    old=f.read_text('utf8')
    if not old.startswith(banner):f.write_text(banner+old,encoding='utf8')
statefile=ROOT/'当前制作状态.json'
s=json.loads(statefile.read_text('utf8'))
s['updated']='2026-10-30'
s['next_action']='复看v030的1:57:20–2:18:13：037推离撑地，041抓袍脱手与教徒离开，二维画风已统一；声音字幕暂缓。'
s['entries'].insert(0,{'name':'小鱼脱手与二维统一v030','path':report})
e=s['independent_editor']
e.update(url=url,project='白米饭｜小鱼脱手与二维统一 v030',frames=9142,fps=24,source_segments=117,reload_verified=True,export_verified=False,resolve_accessed_this_turn=False,receipt=report,previous_project_url='http://127.0.0.1:8978/editor/ab9aef66-c176-4b46-970a-c1cfa7464dc5',new_silent_clips=2,author_edits_preserved=True,current_observed_date='2026-10-30')
s['approved_visual_direction']={'reference':'后期/Claude二维画风去重-v029/Claude-二维关键帧.png','author_approved':True,'description':'清晰墨线、哑光平涂、硬边二维赛璐璐，哥特式背景；本轮只实施037/041，不批量重生全片'}
s['xiaoyu_release_v030']={'installed':True,'author_review_pending':True,'targets':['037','041'],'041_action_focus':'小鱼抓袍子、教徒离开','041_parts_frames':[68,70,84,66],'upscale':False,'other115_clips_preserved':True}
statefile.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
home=ROOT/'00_打开项目.html'
html=home.read_text('utf8')
section=f'<section><h2>当前：小鱼脱手与二维统一 v030</h2><p>037、041按已认可二维画风重制；抓紧衣袍、拉紧、脱手、落手、教徒登阶动作衔接。117段、6分20秒22帧，其他115段保持，原v029保留。从1:57:20复看至2:18:13；声音字幕暂缓。</p><p><a href="{url}">打开OpenCut v030</a> · <a href="{report}">修订说明</a></p></section>'
html=html.replace('<h1>白米饭</h1>','<h1>白米饭</h1>'+section,1)
home.write_text(html,encoding='utf8')
# Preserve unrelated pre-existing AGENTS.md worktree edits; stage our banner over HEAD only.
head=subprocess.check_output(['git','show','HEAD:AGENTS.md'],cwd=ROOT).decode('utf8')
blob=subprocess.check_output(['git','hash-object','-w','--stdin'],cwd=ROOT,input=(banner+head).encode('utf8')).decode().strip()
subprocess.run(['git','update-index','--cacheinfo','100644,'+blob+',AGENTS.md'],cwd=ROOT,check=True)
print(url)
