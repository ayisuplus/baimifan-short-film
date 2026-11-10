"""Create the spatial-continuity and brazier revision from preserved v0.10."""
import json, copy, shutil, hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def read(p): return json.loads((root/p).read_text(encoding='utf-8'))
def write(p, data):
    q=root/p; q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if not (root/'镜头设计/带图分镜-v0.10.html').exists():
    shutil.copy2(root/'镜头设计/带图分镜.html',root/'镜头设计/带图分镜-v0.10.html')

d=read('镜头设计/shot-plan-v0.10.json')
script=(root/'剧本/穿云-场景剧本-v0.10.md').read_text(encoding='utf-8')
body, history=script.split('## 制作交接备注',1)
replacements=[
('版本：v0.10','版本：v0.11'),
('侧面超级大远景里，她立在近处，长殿的列柱与地砖线延伸向遥远出口','从王座端的侧后方看向长殿的超级大远景里，空王座仍靠近端短墙，她站在王座前；长殿两侧的列柱、彩窗与地砖线延伸向对端遥远出口'),
('身边就是低矮破洞','身边就是贴地的扁窄破洞，洞口低于蓬松鲸帽的自然高度'),
('她扒开狗洞边的碎石，低下头向里钻。','她扒开狗洞边的碎石，几乎贴着地面向里挤。石沿同时挤压帽顶和两侧，身体无法直接穿过。'),
('软帽脱开石沿。她将头肩从同一左侧墙洞挤入，双手撑住堂内地面，再把身体拖进来。','侧鳍在按压下脱开石沿，软帽仍被低矮洞顶压扁。她将头肩从同一左侧墙洞一点点挤入，双手撑住堂内地面，再把身体拖进来。'),
('高高的祭坛上','低台祭坛上'),
('两个相同的铜水盆对称放在祭坛最下一级台阶外的左右地面，中央通道留空；右盆用于接住第一支火把。','两个相同的铜火盆对称放在祭坛最下一级台阶外的左右地面，中央通道留空。盆里盛着炭火，是火祭的长明火源，与尚未点燃的十字架低柴分开；右盆稍后接住被撞落的第一支火把。'),
('最后一名教徒在队尾掩上正门，门闩落下。黑袍的阴影罩住小鱼，她突然回头，惊慌地看向逼近的教徒。画面切走，一只手抓住 DeepSeek，将她从祭坛上拽下来；只听见衣料与落地声。','最后一名教徒在队尾掩上正门，门闩落下。DeepSeek 看见持火者向柴薪靠近，松开没能打开的锁，急切地沿三级石阶冲下，奔向他的手臂。'),
('她摔在石阶上，撑起身子，望向正走近的教主。','她落到阶下，短暂半跪，一只手撑地、另一只脚已经踩稳，正要再次起身扑向持火者。教主从旁走近。'),
('一名持火者走向柴薪。DeepSeek 猛地撞上他的手臂，火把脱手，滚入一旁的水盆。','持火者继续走向柴薪。DeepSeek 撑起身子，猛地撞上他的手臂，火把脱手，落进右侧火盆的炭火里。'),
('火把的亮光骤退，水汽嘶声响起；四周的蜡烛仍然燃着。','火星猛地扬起，第一支火把仍在右盆中燃烧，却没能碰到十字架下的干柴；四周的蜡烛也仍然燃着。'),
('第一支湿透的火把仍留在祭坛右侧的水盆中。','第一支火把仍陷在祭坛右侧火盆的炭火中燃烧。'),
('教主轻蔑地俯视她，向前逼近，将她推开。','教主的脸、胸口与双脚正对小鱼，轻蔑地俯视她，向前逼近，将她推开。'),
('天瀑从夜空轰穿中央中殿的穹顶，碎石随水向两侧飞散。巨瀑落地，水浪扑灭低柴火，将黑袍教徒冲向两侧；教主以暗金力量挡开水流，仍稳站原地。后殿拱顶完整，Claude 仍受缚，发梢和裙边被溅湿。','天瀑从夜空轰穿中央中殿的穹顶，汹涌水墙席卷大半座殿堂，碎石随水向两侧飞散。洪水扑灭十字架下的低柴和两只火盆，把黑袍教徒与散乱长椅冲向两侧。ChatGPT 在靠入口的一侧；教主在她前方、祭坛下的中央地面，自己张开暗金护罩抵挡水流，脚步未动；千问抱着小鱼，受护光保护，位于教主侧旁靠柱的安全处。后殿拱顶完整，Claude 仍受缚，发梢和裙边被溅湿。'),
('天瀑停下，湿黑柴堆冒着水汽，浅水向两侧退去。教主没有挪动，暗金光仍分开脚边水流；ChatGPT 沿留空的通道走近，与他对视。千问抱着小鱼，Claude 尚未解锁。','天瀑停下，洪水沿敞开的正门与两侧通道排走，石地上只剩流动浅水。湿黑柴堆和火盆冒着水汽。教主仍在原位，暗金护罩逐渐消散；ChatGPT 从入口方向走近，在破碎穹顶正下方与他对视。远处才是三级低台祭坛。千问仍在教主侧旁的柱边抱护小鱼，Claude 尚未解锁。'),
('广角拉开九位援军的站位，八人从两侧迎上，千问留在祭坛附近，双臂抱护着小鱼。','广角拉开九位援军的前中后三层站位：Grok 与 Mistral 在前，Gemini、混元、智谱和 Perplexity 在中层迎敌，Kimi 与 Llama 从后方支援；千问留在侧旁柱边，双臂抱护着小鱼。'),
]
for old,new in replacements:
    assert old in body, old
    body=body.replace(old,new)
script=body+'## 制作交接备注'+history
script+='\n- v0.11 当前决定：双铜盆改为炭火盆，第一火把落右盆仍燃、第二火把点低柴；小鱼主动冲下阶阻止持火者，之后才被教主推倒。狗洞缩窄并保留鲸帽压扁卡住；王座端墙位置固定。天瀑覆盖大半殿，教主自张暗金护罩，原地与GPT在中殿破顶下对峙。CY027D按九位原卡重建。旧版水盆与拉拽备注仅作历史。\n'
(root/'剧本/穿云-场景剧本-v0.11.md').write_text(script,encoding='utf-8')

church='祭坛只有三级低宽石阶接一个平平台，无侧阶。Claude赤足踩固定脚托、踝链连竖柱；低柴分两侧。两只铜火盆在最下阶外左右同层地面，中央留空。天瀑前盆中炭火已燃，第一火把只落右盆；十字架低柴到CY022才被第二火把点燃。天瀑后两盆与柴火全部熄灭。'
torch='第一支火把落在右侧炭火盆，仍燃但未碰到低柴；宝宝抓袍尾后，教主接第二支火把、迈步扯脱衣摆，用它点燃低柴。第一支不复制到左盆。'
oldchurch=d['continuity']['church']
for s in d['shots']:
    for k in ['title','entry_state','action','exit_state','source_quote','visual_prompt','sound']:
        if k not in s: continue
        for old,new in replacements: s[k]=s[k].replace(old,new)
    s['invariants']=[church if x==oldchurch else torch if '第一支火把熄灭后留在盆内' in x else x.replace('面向祭坛时狗洞和绕行侧道在左、水盆在右','面向祭坛时狗洞和绕行侧道在左，火盆在阶下左右').replace('干柴全程未燃','本场十字架干柴尚未点燃') for x in s['invariants']]
ss={s['id']:s for s in d['shots']}
def edit(sid,**fields): ss[sid].update(fields)
edit('CY009A',framing='王座端侧后方超级大远景／沿长殿轴线望向出口',action='GPT站在近端空王座前；王座仍靠短端墙，长殿两侧彩窗与列柱通往对端出口，小鱼是尽头遥远的蓝色背影。')
ss['CY009A']['invariants']=['王座只在长殿一端的短墙前，出口在对端；长边为列柱和彩窗，不把王座移到侧墙。','GPT已站起，小鱼穿蓝鲸帽服装走向出口；守卫留在门外。']
for sid in ['CY010A','CY011','CY011A']:
    ss[sid]['invariants'].append('同一个贴地扁窄墙洞，低于鲸帽自然高度；帽顶与侧鳍受石沿挤压，宝宝必须贴地挤过。')
edit('CY011A',entry_state='侧鳍脱开凸石，帽顶仍被低洞顶压扁。',exit_state='双手撑地把身体拖入，随后才落地抬头。')
edit('CY016D',title='冲下台阶阻止持火者',entry_state='返回的教徒快步靠近，宝宝看见一名持火者奔向柴薪。',action='DeepSeek松开未打开的锁，沿三级石阶主动冲下，奔向持火者的手臂。',exit_state='她冲到阶下，落脚时短暂半跪，仍准备拦火把。',source_quote='DeepSeek 看见持火者向柴薪靠近，松开没能打开的锁，急切地沿三级石阶冲下，奔向他的手臂。',sound='急促脚步、落脚和衣料声；不再使用拉拽跌落音。')
edit('CY017',title='撑地再起',entry_state='小鱼主动跑下三阶，落脚后短暂半跪，正门已闩。',action='宝宝一手撑地、一脚踏稳准备起身；教主走近，说神明在等她的女儿；持火者继续靠近低柴。',exit_state='小鱼起身扑向持火者，十字架低柴未燃，双火盆已燃。',source_quote='她落到阶下，短暂半跪，一只手撑地、另一只脚已经踩稳，正要再次起身扑向持火者。教主从旁走近。')
edit('CY018',title='第一支火把落进炭火盆',entry_state='小鱼正撑地起身，持火者由祭坛右侧靠近低柴。',action='小鱼撞开持火者手臂，第一支火把脱手落入右侧火盆，炭火迸出火星。',exit_state='第一支火把仍在右盆燃烧，十字架下的干柴没有点燃。',source_quote='火把脱手，落进右侧火盆的炭火里。',sound='碰撞、金属盆沿声、炭火爆裂与火星；不出现入水或蒸汽声。')
edit('CY019',entry_state='第一支火把被撞进右火盆，小鱼转身挡住通往Claude的路。')
edit('CY020B',framing='小鱼后方贴地低角度／教主正面朝她',entry_state='Claude喊出制止，宝宝仍张臂挡在教主面前。')
edit('CY021A',purpose='交代第二支火把的来源；第一支仍留在右火盆，未点燃刑架低柴。',action='教徒将第二支燃着的火把交给教主；第一支留在右火盆炭块间继续燃烧。教主接牢，向低柴迈步。',sound='第二支火苗靠近、衣料摩擦，同一段吟唱不断。')
ss['CY021A']['invariants'][0]=torch
edit('CY022',entry_state='第二支火把在教主手中，小鱼已抓不住衣摆；第一支仍在右火盆的炭火中。')
edit('CY024B',title='天瀑席卷大殿',entry_state='千问已抱住小鱼，祭坛与同伴受护光保护，水光在中殿顶上汇聚。',exit_state='大半座殿堂被洪水席卷，低柴与两火盆全灭；教主靠自己的暗金护罩原地不动。')
edit('CY027',purpose='承接大范围天瀑，明确双方仍在中央破顶下同层地面，祭坛在远处。',entry_state='瀑流停止，洪水经开放出口退成浅水，教主护罩仍在。',exit_state='GPT走近教主，两人在破顶下对视；千问抱宝宝在侧旁柱边。')
edit('CY027A',entry_state='GPT已走到中央破顶下，正对原地抗水的教主。',exit_state='两人在同层湿地正面对峙，远处Claude仍受束；接GPT回应。')
edit('CY027D',framing='广角纵深群像／九位同伴分前中后三层',action='Grok持斧与Mistral持剑在前；Gemini、混元、智谱、Perplexity中层迎敌，Kimi与Llama后方支援。千问抱护小鱼，白银圣骑士守两翼平地柱廊。Claude仍受缚，GPT与教主在天上。')
ss['CY027D']['invariants'].append('九位各一人；Grok金色高双马尾，Gemini双侧发髻与蓝紫猫尾、双腿完整，Llama卫衣长裙，Perplexity眼镜耳机青外套；全部以已有设定卡为准。')
ss['CY027D']['asset_ids']=[a['id'] for a in read('资产/assets.json')['assets'] if any(n in a.get('name','') for n in ['Qwen','Grok','Kimi','Gemini','Perplexity','Mistral','Llama','混元','Zai-GLM'])]+['CHAR-DEEPSEEK','CHAR-CLAUDE','CHAR-CULTIST','CHAR-PALADIN','ENV-CHURCH']
d.update(title='《穿云》带图分镜 v0.11',version='v0.11',revision='v011',created='2026-10-22',story_script='剧本/穿云-场景剧本-v0.11.md',origin_manifest='镜头设计/shot-plan-v0.10.json',subtitle='火盆因果、窄洞挤入、大范围天瀑与九人群像')
d['continuity'].update(church=church,torches=torch,obstruction='发现持火者→主动冲下三阶→短暂半跪撑起→撞火把入右火盆→张臂挡教主→被推倒无力起身→抓袍尾→第二火把点燃低柴。',infiltration='贴地扁窄洞口等待→压扁鲸帽卡住→侧鳍脱开但帽顶仍受压→头肩挤入→双手拖入身体→空堂观察。',magic='天瀑冲破中央中殿并席卷大半大殿，低柴与双火盆全灭；教主在GPT前方、祭坛下，靠自身暗金护罩站稳。千问抱小鱼在侧旁柱边。水经出口排走，GPT走近，双方在破顶下对话再变身腾空。',palace=d['continuity']['palace']+' 王座固定近端短墙，出口在对端；CY009A从王座端侧后方沿轴线看向蓝色小鱼。')
d['review_intro']='本版修正王座端墙位置和窄洞挤入；铜盆改炭火盆，主动阻火到抓袍尾的动作重新衔接；天瀑扩为覆盖大半殿堂，教主自开护罩，破顶下对峙后升空；九人群像按角色卡重建。'
d['review_focus']='重点看CY009A—012空间、CY016D—022火把因果，以及CY024B—027A的站位；CY027D核对九人身份与肢体。原鲸帽卡住、雷雨省略和公主抱保留。'
d['roughcut_preview_label']='旧版静帧配乐 v002（69镜239秒，未包含v0.11改图；Victory决定保留）'
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.10.json',previous_html='镜头设计/带图分镜-v0.10.html',added_ids=[],repurposed_ids=[{'id':'CY016D','old':'拉拽下阶','new':'主动冲下阶阻止持火者'}],boundary='16镜独立改图候选；实际生成请求与返修全部保留。89镜286秒不变。旧配乐粗剪未重导，正式配音及动态待制作。')
for m in d['masters']:
    if m['id'].startswith('M-ALTAR'):
        m['status']='历史构图参考，火盆语义以M-ALTAR-v011为准'
        m['limits']='仅参考三级结构；旧盆中水与湿火把设定已被v0.11炭火盆取代。'
d['masters'].append({'id':'M-ALTAR-v011','title':'三级低台与双炭火盆','path':'镜头设计/图像/空间因果-v011/CY012-v011.png','role':church,'status':'v0.11候选待作者审阅','limits':'前天瀑火盆燃烧、低柴未燃；其他状态按镜头变化。近景允许遮挡，不新增台阶或铜盆。'})

records=read('镜头设计/生成记录/空间因果-v011/结果映射.json')
selected={}
for r in records:
    if r['id'] not in selected or r['take']>selected[r['id']]['take']: selected[r['id']]=r
for sid,r in selected.items():
    s=ss[sid]; old=s['presentation']['path']; job=read(r['request'])
    s['presentation']={'path':r['destination'],'role':'action','visible':s['action'],'status':'v0.11独立镜头候选，待作者审阅','missing':'静帧仅表达代表状态；连续挤入、走位、洪水退去与变身仍待视频验证。','show_as_main':True}
    s['generation_request']=r['request']; s['visual_prompt']=job['request']['prompt']
    s['refs']=[{'path':r['destination'],'role':'本轮独立原画候选'},{'path':r['request'],'role':'冻结的实际提示词与输入'},{'path':old,'role':'保留的上一版'}]
    s['editorial_review']={'version':'v011','status':'candidate_static_review','dynamic_execution':'pending'}
    s['panel_index']=0; s.pop('display_crop_normalized',None)
for sid in ['CY017','CY018','CY021A','CY022']:
    # These metadata prompts predate the brazier change; immutable requests remain in refs.
    if sid not in selected: ss[sid]['visual_prompt']='《穿云》'+sid+'。'+ss[sid]['action']+'。'+torch
elapsed=0
for i,s in enumerate(d['shots']):
    s['presentation']['visible']=s['action']
    s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
    s['next_link']='接 '+d['shots'][i+1]['id']+'：'+s['exit_state']+' → '+d['shots'][i+1]['entry_state'] if i+1<len(d['shots']) else '结束。'
d['total_seconds']=elapsed
d['page_layouts']=[{'path':s['presentation']['path'],'rows':1,'cols':1} for s in d['shots']]
for sc in d['scenes']:
    group=[s for s in d['shots'] if s['scene']==sc['id']]
    sc.update(shot_ids=[s['id'] for s in group],seconds=sum(s['seconds'] for s in group),pages=list(dict.fromkeys(s['presentation']['path'] for s in group)))
    sc['path']=sc['pages'][0]
missing=[s['id'] for s in d['shots'] if s['source_quote'] not in script]
assert not missing,missing
assert len(d['shots'])==89 and elapsed==286
write('镜头设计/shot-plan-v0.11.json',d)
for r in records:
    dest=root/r['destination']; orig=Path(r['original'])
    r['sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
    assert r['sha256']==hashlib.sha256(orig.read_bytes()).hexdigest()
    r['status']='candidate' if r==selected[r['id']] else 'superseded-preserved'
write('镜头设计/生成记录/空间因果-v011/归档校验.json',records)
print(json.dumps({'shots':len(d['shots']),'seconds':elapsed,'revised_shots':len(selected),'requests':len(records),'quote_check':'passed'},ensure_ascii=False))
