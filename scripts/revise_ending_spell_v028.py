"""Apply approved final answer and short incantation; keep expanded proposals separate."""
import copy,json,shutil,hashlib,re,html,wave
from pathlib import Path
from urllib.parse import urlsplit,unquote
R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/结尾与吟唱-v028'
(R/REC).mkdir(parents=True,exist_ok=True)
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,t):(R/p).write_text(t,encoding='utf-8')
def save(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
old=json.loads(read('镜头设计/shot-plan-v0.27.json'));d=copy.deepcopy(old);by={s['id']:s for s in d['shots']}
t=read(old['story_script'])
a=by['CY024A']
start=t.index(a['source_quote']);end=t.index('天瀑从夜空',start)
passage='''千问俯身，将小鱼护进怀里。

**千问：**
抱紧我。

小鱼攥住她的衣襟。千问抱稳她，向柱边侧身；Perplexity的护光先罩住高处祭坛上的Claude。

ChatGPT继续向前，缓缓抬手，掌心朝上。

**ChatGPT：**
汇于苍穹的万流，

银白水光在中殿穹顶外向中央聚拢。骑士退入两侧厚石柱之后，以白银护光挡住即将到来的侧向水浪，中央落水区保持净空。穹顶此时尚未破裂。

**ChatGPT：**
听我号令——

ChatGPT抬眼，手指微微收拢。确认小鱼与Claude均在保护之中，短停一拍，翻掌向下。

**ChatGPT：**
天瀑。

'''
t=t[:start]+passage+t[end:]
target='Claude 轻轻点头。小鱼把勺柄递向右侧'
assert target in t
t=t.replace(target,'Claude看向小鱼，轻轻点头，露出一点笑意。\n\n**Claude：**\n好。\n\n小鱼把勺柄递向右侧',1)
lines=t.splitlines();lines[2]='版本：v0.28｜2026-10-22｜结尾Claude新增“好”；天瀑采用已确认短咒语，护人及施法段延至8秒。长吟唱、吃饭近景及音乐方案仍在讨论。';t='\n'.join(lines)+'\n'
write('剧本/穿云-场景剧本-v0.28.md',t)
d.update(version='v0.28',revision='v028',title='《穿云》带图分镜 v0.28 · 结尾回应与天瀑吟唱',subtitle='结尾“好”；已确认短吟唱与8秒施法预算',story_script='剧本/穿云-场景剧本-v0.28.md',origin_manifest='镜头设计/shot-plan-v0.27.json',source_manifest='镜头设计/生成记录/生成索引-v028.json')
d['review_intro']='已确认的结尾“好”与短咒语写入当前稿，CY024A由2秒延至8秒。作者进一步提出长咒语配乐及第一口饭近景；具体新词与镜头为待讨论方案，尚未覆盖已确认文本。全部图片沿用，未生成声音或视频。'
d['review_focus']='检查护人→聚水吟唱→天瀑的8秒暂排，以及结尾邀请→Claude说“好”→接勺的自然衔接。'
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.27.json',previous_html='镜头设计/带图分镜-v0.27.html',added_ids=[],modified_ids=['CY024A','CY031A','CY032A'],boundary='96镜314秒；CY024A增加6秒，结尾“好”放入CY031A现有4秒；所有图片及其余对白保持。长咒语与吃饭近景为讨论项。')
a.update(seconds=8,title='护人、吟唱与天瀑',purpose='完成护人和清空落水区，以吟唱与聚水建立施法蓄势。',source_quote=passage.strip(),action='千问抱起小鱼说“抱紧我”，向柱边保护；Perplexity先护住Claude。GPT抬手吟唱“汇于苍穹的万流，听我号令——天瀑。”；水光在穹顶外汇聚，骑士进入两翼石柱后。GPT确认保护就位，翻掌下令，下一镜落水。',dialogue='千问：抱紧我。\nChatGPT：汇于苍穹的万流，听我号令——天瀑。',sound='护人动作与吟唱连续推进，聚水声渐强。短咒语音乐设计：起句低弦持续音进入，“听我号令”叠入弦乐上行，天瀑前短收声，落水与下一镜重音同步。仅声音设计，未制作配音、BGM或音效。',exit_state='Claude与小鱼均有保护，骑士避让到位；GPT翻掌说完“天瀑”，水光已聚于中殿穹顶外。')
a['time_caption'].update(text='此刻',offset=0.1,duration=1.7)
a['subtitle_cues']=[dict(speaker='千问',text='抱紧我。',offset=0,duration=1.1),dict(speaker='ChatGPT',text='汇于苍穹的万流，',offset=1.4,duration=2.6),dict(speaker='ChatGPT',text='听我号令——',offset=4.1,duration=1.9),dict(speaker='ChatGPT',text='天瀑。',offset=6.8,duration=1)]
a['cinematic_beats']=[dict(offset=0,intent='抱紧我，千问护住小鱼，Perplexity先护住Claude'),dict(offset=1.4,intent='GPT抬掌起句，穹顶外聚水；骑士沿两翼避让'),dict(offset=4.1,intent='听我号令，护罩稳定，中央净空'),dict(offset=6.3,intent='短停收声，GPT翻掌'),dict(offset=6.8,intent='天瀑，接下一镜水墙破顶')]
a['presentation']['missing']='当前静帧为既有施法代表状态，不能表达完整8秒护人、吟唱与翻掌。动作切点、口型、正式声音待执行。'
s=by['CY031A'];s.update(action=s['action']+' 小鱼问完，Claude看着她，轻轻点头说“好”，再接下一镜递勺。',dialogue='DeepSeek：你要吃一点吗？\nClaude：好。',exit_state='Claude已坐到右边，点头说“好”；勺仍由小鱼拿着，尚未转交。',sound='保留小鱼原邀请临时读稿；Claude的“好”轻轻接在问句后。新句仅暂排字幕，尚无配音。',source_quote='**DeepSeek：**\n你要吃一点吗？\n\nClaude看向小鱼，轻轻点头，露出一点笑意。\n\n**Claude：**\n好。',next_link='接CY032A：Claude已说“好”，小鱼才递勺，饭碗仍在膝上。')
for cue in s['dialogue_cues']:
 with wave.open(str(R/cue['file']),'rb') as wav: duration=wav.getnframes()/wav.getframerate()
 assert cue['offset']+duration<=3.15,(duration,cue)
s['subtitle_cues']=[dict(speaker='DeepSeek',text='你要吃一点吗？',offset=1,duration=2),dict(speaker='Claude',text='好。',offset=3.2,duration=0.7)]
s['dialogue_timing_status']='provisional_subtitles_pending_voice_readthrough'
by['CY032A'].update(entry_state='两人同坐长椅，小鱼问完，Claude已点头说“好”；勺仍在小鱼手里。',sound='邀请与回应均在上一镜结束；这里留勺柄轻触与市声。')
elapsed=0
for s in d['shots']:s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
d['total_seconds']=elapsed
for sc in d['scenes']:sc['seconds']=sum(s['seconds'] for s in d['shots'] if s['scene']==sc['id'])
save('镜头设计/shot-plan-v0.28.json',d)
snap=R/'镜头设计/带图分镜-v0.27.html'
if not snap.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snap)
save('镜头设计/生成记录/生成索引-v028.json',dict(version='v028',previous_index='镜头设计/生成记录/生成索引-v027.json',records=[],review=REC+'/复核记录.md',media_generated=False))
write(REC+'/复核记录.md','''# v0.28 结尾回应与已确认短吟唱

执行作者明确确认的两处：CY031A结尾加Claude“好”；CY024A采用“汇于苍穹的万流，听我号令——天瀑。”并由2秒延至8秒。千问先保护小鱼，Perplexity先保护Claude，骑士净空，吟唱覆盖动作。字幕暂排，正式读稿仍待制作及听审。小鱼现有邀请读稿与“好”的字幕预算不重叠。

96镜314秒（5分14秒），全部图片沿用；火种段延续作者本轮“这段就这样”的决定。旧版保留。无新图、视频或声音生成。

作者进一步提出嘴部吃饭特写及更长的魔法吟唱配乐；完整建议在本轮聊天讨论，尚未替换已确认短词或新增正式镜号。新建议不等于作者采用。
''')
p='scripts/build_storyboard.py';write(p,read(p).replace('shot-plan-v0.27.json','shot-plan-v0.28.json').replace('"v027")','"v027", "v028")').replace("'v027')","'v027','v028')"))
p='00_打开项目.html';write(p,read(p).replace('v0.27','v0.28').replace('5 分 08 秒','5 分 14 秒').replace('火种主观飞行与触木骤燃；对白保持','结尾回应与天瀑吟唱；8秒施法预算').replace('慢慢来 · 那个孩子 · Claude过来 · 我们走','结尾“好” · 汇于苍穹的万流，听我号令——天瀑'))
p='制作进度.md';x=read(p);i=x.index('## ')
write(p,x[:i]+'''## 2026-10-22：结尾回应与天瀑吟唱（v0.28）

作者确认结尾Claude新增“好”，并采用“汇于苍穹的万流，听我号令——天瀑。”。已同步[剧本v0.28](剧本/穿云-场景剧本-v0.28.md)与[当前分镜](镜头设计/带图分镜.html)：CY024A从2秒放宽到8秒，吟唱覆盖护人、聚水、骑士避让；CY031A原4秒内补“好”，小鱼原临时读稿保持，新增句仅字幕暂排。96镜314秒（5分14秒），全部图片保留，无新声音或视频生成。

作者对火种段表示“这段就这样”，本轮不再改该段。作者进一步提出吃饭嘴部特写、参考长咒语及配合BGM；具体长词、20—24秒节奏与嘴部近景仍为聊天建议，未替换当前短版，未新增正式镜号。

'''+x[i:])
assert len(d['shots'])==96 and elapsed==314
assert all(a['presentation']['path']==b['presentation']['path'] for a,b in zip(old['shots'],d['shots']))
assert [b['id'] for a,b in zip(old['shots'],d['shots']) if a['seconds']!=b['seconds']]==['CY024A']
print('Prepared v0.28:96 shots314 seconds; approved short spell and final reply; no image changes.')

