"""Derive v015 without changing historical manifests or media."""
import copy, json, shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def read(p): return json.loads((root/p).read_text(encoding='utf-8'))
def write(p,v): (root/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=read('镜头设计/shot-plan-v0.14.json')
script=(root/d['story_script']).read_text(encoding='utf-8')
notes=script.split('## 制作交接备注',1)[1]
body=script.split('## 制作交接备注',1)[0]
quotes={
'CY003C':'教徒猛地一掌拍翻小鱼手中的碗沿，白米饭撒向地面。小鱼仍攥住另一侧碗沿，惊愕地缩起肩膀；教徒嫌恶地挥手驱赶她，Claude 在黑袍身后担忧地回望。',
'CY004':'DeepSeek 跟到教堂台阶下，低低抱着已经空了的饭碗。门口一名教徒向里交代，声音落到她耳中。',
'CY004A':'DeepSeek 把空碗留在街边矮桌上，碗中仅余几粒饭。她眉头紧皱，担忧地抬头望向远处的宫殿。',
'CY021B':'贴近地面，只见小鱼的绒边袖口、前臂与小手攥紧教主黑金长袍的拖尾，衣料被拉出绷紧的褶皱。',
'CY022':'近处，笔直的第二支火把触到刑架底部的干柴，细木屑先亮起火苗，继而沿木纹燃开。火把收回，画外下行的脚步渐远；教主返回长阶下段，Claude 仍受缚于高处。',
'CY026C':'工业发射塔旁，钢架、储罐与管线延伸到远处。Grok 本就握着斧柄，她抬起下巴，嘴角一扬；回应落在同一个双人画面里。',
'CY025':'小鱼靠在千问怀里，疲倦地抬眼。蓝色眼睛中只映出白紫水龙腾空时模糊的光影，瞳孔仍清楚可见，泪光微微一颤。',
'CY027D':'教堂内，各路 AI 娘沿长阶分层迎敌：Grok、Gemini、Mistral在下层，GLM与Perplexity错后站在两侧；混元、Llama、Kimi退至后层，千问抱着小鱼留在中后层受保护的位置。两翼圣骑士守住柱廊，中央保留通向高处Claude的视线。'
}
for s in d['shots']:
 if s['id'] in quotes:
  assert s['source_quote'] in body,s['id']
  body=body.replace(s['source_quote'],quotes[s['id']])
  s['source_quote']=quotes[s['id']]
climb='背后低机位望去，教主握着第二支火把，一步一步踏上长阶，鞋底在石面敲出沉重回声；高处的Claude始终未被解开，小鱼留在下端。'
old='省略途中攀登，教主已到顶部平台，把第二支火把探向低柴堆，将木柴引燃后收回。小鱼仍远在长阶下端。镜尾教主转身开始下阶。'
assert old in body
body=body.replace(old,climb)
body=body.replace('版本：v0.14','版本：v0.15')
body=body.replace('广角拉开九位援军的前中后三层站位：Grok 与 Mistral 在前，Gemini、混元、智谱和 Perplexity 在中层迎敌，Kimi 与 Llama 从后方支援；千问留在侧旁柱边，双臂抱护着小鱼。','')
script=body+'## 制作交接备注'+notes+'\n\n- v0.15：掀饭后始终为空碗；新增教主登阶，接火把触柴局部特写。群像沿长阶分层、两翼圣骑士保留，宝宝蓝眼。Grok基地工业化。GPT救援段温柔沉稳、无害羞红晕；Claude羞红保留。天瀑后普通灯火全灭，后续空刑架剧情火焰仍按原稿。\n'
(root/'剧本/穿云-场景剧本-v0.15.md').write_text(script,encoding='utf-8')
by={s['id']:s for s in d['shots']}
new=copy.deepcopy(by['CY022A'])
new.update(id='CY022A1',title='教主登上长阶',seconds=3,framing='背后低角度中远景／脚步上行',purpose='用登阶动作连接阶下挣脱与顶部点火，交代高差和路程。',
entry_state='袍尾已从宝宝手中滑脱，教主握第二支火把来到长阶。',
action='教主持第二支火把，背向镜头逐级上行，足底踏实阶面；顶部刑架低柴尚未点燃。',
exit_state='教主继续向顶部前进；省略剩余路程接火把触柴特写。',dialogue='无对白',sound='鞋底逐级敲击石阶，火把燃烧，远处低吟。',dialogue_cues=[],source_quote=climb,asset_ids=['CHAR-PRIEST','CHAR-CLAUDE','ENV-CHURCH'])
new.pop('subtitle_cues',None)
d['shots'].insert(d['shots'].index(by['CY022A'])+1,new)
by[new['id']]=new
changes={
'CY003C':dict(title='白米饭被掀翻',framing='中近景／碗沿与飞散米饭',entry_state='宝宝举着满饭碗靠近Claude，教徒横身挡住。',
action='教徒猛地拍翻碗沿，米饭飞散；宝宝握住另一边，缩肩惊愕，Claude在后方担忧回望。',
exit_state='饭已撒落，宝宝仍握住空碗，被驱到路边。',sound='掌击金属碗沿的响声、米饭散落、宝宝短促吸气。'),
'CY004':dict(action='宝宝低抱空碗跟到门前，听见教徒交代献祭消息。',entry_state='白米饭已被打翻，宝宝抱着空碗追到教堂。',exit_state='听清危险后她转身离开，空碗仍在手中。'),
'CY004A':dict(action='宝宝把只剩几粒饭的空碗放上矮桌，焦急望向宫殿，随后跑去求援。',entry_state='宝宝抱着空碗离开教堂门口。',exit_state='空碗留在桌上，宝宝独自奔向宫殿。'),
'CY021B':dict(framing='贴地极近特写／小手与袍尾',action='只见宝宝的袖口、前臂和小手攥住黑金袍尾；衣料绷紧，身体与头部在画外。',exit_state='小手仍抓紧袍尾，教主停步接第二支火把。'),
'CY021A':dict(action='教主在长阶下端接牢笔直的第二支火把；火把头、轴与握柄保持同一直线。',exit_state='教主接牢第二支火把，准备迈步；宝宝仍攥着袍尾。'),
'CY022A':dict(framing='贴地中景／宝宝与离去的教主',action='教主转身迈向长阶，袍尾从宝宝伸出的手边滑脱；宝宝留在下端。',exit_state='宝宝未能留住教主；教主持火把开始登阶。'),
'CY022':dict(title='火把触上干柴',framing='局部特写／火把与木柴接触处',purpose='以火苗出现和画外下阶脚步完成点火、返回的因果连接。',
entry_state='省略余下路程，教主已登到顶部平台，第二支火把靠近刑架低柴。',
action='笔直的火把尖端触上低柴，细木屑起火，火苗沿木纹蔓延；火把收回，画外传来下阶脚步。',
exit_state='低柴燃起；教主开始返回下段，后续反应镜头期间走完余程。宝宝仍在下端，Claude仍受缚。',
sound='近处火苗呼声、木屑爆裂；火把收回后接渐远的下行脚步。'),
'CY026C':dict(framing='召集回闪／工业发射基地双人中景',action='钢架发射塔、储罐和管线旁，GPT邀请Grok；Grok握斧回应。火箭停在发射架，尚未发射。'),
'CY025':dict(action='宝宝疲惫抬眼；蓝色虹膜中仅有模糊白紫上升光影，泪光微颤，瞳孔不被倒影覆盖。'),
'CY027D':dict(framing='阶下中远景／纵深分层群像',action=quotes['CY027D'],entry_state='雨滴落地；同伴分散站稳在下、中、后层台阶，教徒从低处重新聚来。',exit_state='前排迎敌，后排支援、千问护宝宝，骑士守两翼；切教堂外爆闪省略交战。')
}
for sid,fields in changes.items(): by[sid].update(fields)
by['CY027D']['invariants'] += ['九位同伴沿长阶分层，不重复角色、不缺肢；DeepSeek为正常蓝色虹膜与黑色瞳孔，无红眼块。', 'Grok蓝眼，Gemini画面左粉紫右金黄，Mistral琥珀金，GLM灰黑，混元深青灰，千问蓝紫，Llama浅灰蓝，Perplexity青蓝，Kimi淡蓝紫。']
for sid in ('CY003C','CY004','CY004A'):
 by[sid]['invariants']=['CY003C掀饭后饭落地，CY004低抱空碗，CY004A空碗留桌；不再出现满碗。','宝宝不受直接身体伤害，教徒以掀饭和嫌恶驱逐表现敌意。','保持原有母本人物、街市与时段。']
blush=('CY027G','CY028A','CY029B','CY029C','CY029D','CY028','CY029A')
for sid in blush: by[sid]['invariants'].append('GPT温柔、沉稳、专注照顾Claude；无害羞红晕。Claude的自然羞红保留。')
d.update(title='《穿云》带图分镜 v0.15',version='v0.15',revision='v015',story_script='剧本/穿云-场景剧本-v0.15.md',origin_manifest='镜头设计/shot-plan-v0.14.json',subtitle='掀饭、登阶点火与分层迎敌群像')
d['continuity']['rice_bowl']='街市掀饭后宝宝始终拿空碗；空碗随后留在街边矮桌。数日后结尾为重新盛好的饭。'
d['continuity']['rescue_expression']='GPT救援段温柔沉稳，不羞红；Claude的羞红保留。'
d['review_intro']='修正掀饭后的空碗衔接、新增教主登阶与点柴特写；工业火箭基地、眼中模糊龙影、沿长阶展开的群像、蓝眼宝宝与GPT沉稳表情。多级祭坛及天瀑后熄灯规则延续。'
d['review_focus']='连看CY003C—004A饭碗、CY021B—022点火路线、CY025—027D瞳色与分层站位，以及CY027G—029A救援表情。'
d['roughcut_preview_label']='旧版静帧配乐v002（69镜239秒，未包含v0.15改图；Victory决定保留）'
records=read('镜头设计/生成记录/动作收尾-v015/结果映射.json')
choices=read('镜头设计/生成记录/动作收尾-v015/采用映射.json')
selected={r['id']:r for r in records if choices.get(r['id'])==r['take']}
assert len(selected)==17
for s in d['shots']:
 sid=s['id']
 if sid in selected:
  r=selected[sid];prev=s['presentation']['path']
  s['presentation']={'path':r['destination'],'role':'action','visible':s['action'],'status':'v0.15修订候选，待作者审阅','missing':'静帧动作代表状态；连续运动、正式声音待视频制作。','show_as_main':True}
  s.update(visual_prompt=r['input']['prompt'],generation_request=r['request'],panel_index=0,editorial_review={'version':'v015','status':'candidate_static_review','dynamic_execution':'pending'})
  s['refs']=[{'path':r['destination'],'role':'本轮独立镜头修订'},{'path':r['request'],'role':'冻结实际输入'},{'path':prev,'role':'上一版或邻镜空间参考'}]
  s.pop('display_crop_normalized',None)
 s['presentation']['visible']=s['action']
elapsed=0
for i,s in enumerate(d['shots']):
 s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
 s['next_link']='接 '+d['shots'][i+1]['id']+'：'+s['exit_state']+' → '+d['shots'][i+1]['entry_state'] if i+1<len(d['shots']) else '结束。'
d['total_seconds']=elapsed
for sc in d['scenes']:
 group=[s for s in d['shots'] if s['scene']==sc['id']]
 sc.update(shot_ids=[s['id'] for s in group],seconds=sum(s['seconds'] for s in group),pages=list(dict.fromkeys(s['presentation']['path'] for s in group)))
 sc['path']=sc['pages'][0]
d['page_layouts']=[{'path':s['presentation']['path'],'rows':1,'cols':1} for s in d['shots']]
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.14.json',previous_html='镜头设计/带图分镜-v0.14.html',added_ids=['CY022A1'],repurposed_ids=['CY022'],boundary='17镜独立改图（含新增登阶一镜）；90镜289秒。历史候选与冻结输入保留，旧配乐粗剪未重导。')
assert len(d['shots'])==90 and elapsed==289
assert all(s['source_quote'] in script for s in d['shots'])
archive=root/'镜头设计/带图分镜-v0.14.html'
if not archive.exists():shutil.copy2(root/'镜头设计/带图分镜.html',archive)
write('镜头设计/shot-plan-v0.15.json',d)
print('v015: 90 shots, 289 seconds, 17 images')
