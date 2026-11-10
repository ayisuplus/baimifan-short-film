"""Versioned spatial/transition revision. Run once; never replaces v0.5 sources."""
import copy, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / '镜头设计/shot-plan-v0.6.json'
if target.exists():
    raise SystemExit('v0.6 exists; inspect instead of regenerating adopted edits')
def write(path, value):
    (ROOT/path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
old = json.loads((ROOT/'镜头设计/shot-plan-v0.5.json').read_text(encoding='utf-8'))
d = copy.deepcopy(old)
script = (ROOT/old['story_script']).read_text(encoding='utf-8')
def replace(a,b):
    global script
    assert a in script, a
    script=script.replace(a,b)
replace('版本：v0.5｜2026-10-21｜全片接续复核：补足消息、交接与落座，合并重复动作。',
        '版本：v0.6｜2026-10-21｜空间复核：固定道具与高台，补足赶路、拉拽、落地、进殿与解锁过程。')
q_bowl='DeepSeek 把饭碗留在街边矮桌上，松开手，抬头望向远处的宫殿。'
replace('## S02｜宫殿·黄昏·内', q_bowl+'\n\n## S02｜宫殿·黄昏·外转内')
q_palace='暮色里，小鱼空着双手跑上宫殿外的长阶。紫色旗帜垂在高门两旁。'
replace('沉重的大门被推开。',q_palace+'\n\n沉重的大门被推开。')
replace('她缓缓站起。','她缓缓站起。金色座位仍在她身后的高台上，她没有走下台阶。')
q_basin='水盆固定在祭坛最下一级台阶外的右侧地面；腰前只有一道横链和一枚竖向长方锁，两腕分别固定在横木上。'
replace('柴薪还没有点燃。','柴薪还没有点燃。\n\n'+q_basin)
replace('小鱼沿左侧长椅旁的阴影走到祭坛，从侧面的台阶爬上去。','小鱼沿左侧长椅旁的阴影走到祭坛，从侧面的台阶爬上去。她站稳在木架左侧的窄阶边，双脚有支点，才能够到 Claude 腰前的锁。')
q_walk='从敞开的门内望向祭坛，ChatGPT 沿中央通道前行；千问从她身侧跑向阶下的小鱼，Perplexity 在右侧举杖，蓝光先到祭坛。'
replace('一道屏障隔开柴薪与 Claude，火焰随之被压灭。',q_walk+'\n\n一道屏障隔开柴薪与 Claude，火焰随之被压灭。')
q_support='Claude 仍有一只手腕扣在横木上。ChatGPT 从右侧扶住她的腰背和上臂，Perplexity 在左侧解除最后一个腕扣；木架始终留在祭坛最高的平台上。'
replace('Claude 的重量落进 ChatGPT 怀里，被稳稳接住。',q_support+'\n\nClaude 的重量落进 ChatGPT 怀里，被稳稳接住。')
replace('ChatGPT 把她轻轻放下。','ChatGPT 在同一祭坛平台上把她轻轻放下，没有抱她下楼。')
script += '\n- v0.6：补放碗与宫殿外景、被拽下、失守落地、沿通道推进、解除最后腕扣。水盆固定阶下右侧，腰链与站位统一；以门外升空替换旧屋顶对峙，不增加战斗。图像是静帧，门闩和动作音效仍待动态与声音阶段完成。\n'
(ROOT/'剧本/穿云-场景剧本-v0.6.md').write_text(script,encoding='utf-8')
snapshot=ROOT/'镜头设计/带图分镜-v0.5.html'
assert not snapshot.exists(), 'Snapshot exists; inspect before proceeding'
shutil.copy2(ROOT/'镜头设计/带图分镜.html',snapshot)
shots={s['id']:s for s in d['shots']}
paths={
 'A':'镜头设计/图像/空间修订A-地点与起飞-v001.png',
 'B':'镜头设计/图像/空间修订B-祭坛与锁链-v002.png',
 'C':'镜头设计/图像/空间修订C-阻拦与入场-v002.png',
 'D':'镜头设计/图像/空间修订D-托稳与落脚-v002.png',
 'E':'镜头设计/图像/S05B-粗分镜-v006.png',
 'F':'镜头设计/图像/空间修订F-解锁与站稳-v002.png'}
for path in paths.values(): assert (ROOT/path).exists(), path
def edit(id,**kw): shots[id].update(kw)
def picture(id,page,cell,visible,missing='静帧表示动作中的一个状态，连续动作尚待动态制作。'):
    s=shots[id]
    s.update(panel_index=cell,presentation=dict(path=paths[page],role='action',visible=visible,missing=missing,status='v0.6空间修订候选；实际图像已复核',show_as_main=True))
    s['refs']=[dict(path=paths[page],role=f'本镜空间修订原图第{cell+1}格'),*[r for r in s['refs'] if not r['path'].startswith('镜头设计/图像/')]]
    for k in ['page_size','panel_region','panel_rect_pixels','display_crop_normalized']:s.pop(k,None)
added=[]; after={}
def add(id,anchor,seconds,title,framing,action,entry,exit,quote,page,cell,visible,scene=None):
    s=copy.deepcopy(shots[anchor]);shots[id]=s
    for k in ['time_caption','split_screen_reveal']:s.pop(k,None)
    s.update(id=id,seconds=seconds,title=title,framing=framing,action=action,entry_state=entry,exit_state=exit,source_quote=quote,dialogue='无对白',dialogue_cues=[],purpose=title+'，补足前后状态间的关系。',sound='本版用既有BGM衔接；脚步和动作拟音尚未制作。',invariants=[],priority='normal')
    if scene:s.update(scene=scene,scene_title=next(x['title'] for x in d['scenes'] if x['id']==scene))
    picture(id,page,cell,visible)
    after.setdefault(anchor,[]).append(id);added.append(id)
    return s
add('CY004A','CY004',2,'放下饭碗','中景／沿街朝宫殿方向',q_bowl,'刚听见火祭命令，碗仍在手。','碗留在矮桌，小鱼空手离开。',q_bowl,'A',0,'矮桌上留着银色饭碗，小鱼双手已离开，朝远处宫殿迈步。')
add('CY004B','CY004A',2,'暮色里的长阶','远景／宫殿外景',q_palace,'小鱼已空手离开街口。','到达宫门，下一镜进入殿内。',q_palace,'A',1,'鲸鱼宝宝背向镜头沿宫殿长阶奔跑，夕光与紫旗明确地点。',scene='S02')
picture('CY010','A',2,'GPT站在金色座位旁的高台上；台阶向镜头方向下降。')
edit('CY010',action='GPT在座位旁起身，留在原高台上望向门口。',exit_state='GPT仍在高台；以暮色留影接夜间教堂外。')
picture('CY013','B',0,'祭坛木架与未燃柴薪在阶顶，金属水盆在阶下右侧地面。')
picture('CY015','B',1,'宝宝踩在木架左侧窄阶，双脚有支撑，踮身够到腰前方锁。')
picture('CY016','B',2,'宝宝用双手拉同一道横腰链，竖向长方锁仍挂在中间。')
picture('CY016A','B',3,'宝宝在同一侧阶垂头喘息，Claude仍受腕扣与单腰链固定；近景无水盆。')
add('CY016D','CY016C',2,'从侧阶被拽下','近景／侧阶动作关系','教徒抓住宝宝衣袖，将她从侧阶拽下；她伸手试图够住台阶。','返回教徒已经走到祭坛。','宝宝失去支点，接下一镜阶下撑地。','一只手抓住 DeepSeek，将她从祭坛上拽下来。','C',0,'黑袍抓住宝宝衣袖，宝宝从石阶失去平衡，Claude受束在后方。',scene='S04')
edit('CY017',action='承接拽下的结果，宝宝撑起身体，教主走近并说出自己的话。队尾已关门落闩；不再重复演拽下。',entry_state='宝宝刚被从侧阶拽下；队尾将门掩上。',sound='本版只保留对白字幕与BGM；门闩、衣料及吟唱是后续声音计划。')
shots['CY017']['dialogue_cues'][0]['offset']=1.5
shots['CY017']['presentation']['missing']='静帧显示阶下状态；门关闭和落闩尚未有独立动作画面，后续动态需落实，不宣称已画出。'
add('CY020A','CY020',2,'失守落地','低机位／由Claude视线落向阶下','从Claude喊声切到阶下，宝宝侧倒，一只手试图撑地；推开她的手退出画面。','宝宝已阻在阶前，黑袍围拢；Claude喊出别碰她。','宝宝失去站立能力，下一镜只抬头注意窗外信号。','DeepSeek 倒在台阶下。她撑住地面，想再站起来，手臂却软了下去。','C',1,'宝宝侧倒在阶下，目光低垂，后方Claude仍受束。')
picture('CY022A','C',2,'宝宝手指已与衣摆分离；教主握着第二支火把离开，阶下右侧盆中留着湿火把。')
edit('CY022A',title='衣摆从指间滑走',action='保留指尖刚刚脱离衣摆的结果，教主握火把继续走向柴薪。',exit_state='手已松开，第二支火把在教主手中；切点火结果。')
add('CY024A','CY024',2,'沿通道奔向祭坛','反向全景／从门内望向祭坛',q_walk,'九位援军已随GPT破门。','千问将到宝宝旁；屏障已开始在祭坛前形成。',q_walk,'C',3,'GPT背影沿通道前进，千问奔向阶下宝宝，Perplexity右侧举杖，Claude仍在远处。')
shots['CY024A']['invariants']=['本镜局部只清楚显示三位援军，其余八位在镜外；前镜十位入场者群像保留。','正门在摄影机身后，祭坛在前；仍未解除Claude束具。']
picture('CY027','E',0,'千问在阶下抱住宝宝，Perplexity维持屏障，GPT面向祭坛；高台上不再出现水盆。')
picture('CY027C','A',3,'教主在左、GPT在右，从敞开的教堂门口升空；屋顶完整。')
edit('CY027C',title='穿过正门升空',framing='外景／门口斜侧仰拍',action='两道身影从敞开的正门向外升起，教主左、GPT右；下一镜回堂内同伴起势，随后直接以夜空闪光省略激战。',entry_state='GPT与教主刚在殿内对峙。',exit_state='两人已离开教堂建筑范围，战斗在外部上空发生。',source_quote='ChatGPT 展开龙翼，两道身影掠出敞开的正门，升上钟楼上空。')
add('CY027G','CY027F',3,'先扶住，再解最后腕扣','中景／祭坛正面',q_support,'敌方已经全部倒地，援军走上祭坛。','最后腕扣正被解除，GPT已经扶住Claude。',q_support,'F',0,'Claude一只手仍扣在横木，GPT右侧扶住她，Perplexity左侧伸手解锁。')
picture('CY028','D',1,'两人抱持近景，Claude在左、GPT在右，失去束缚后身体被接住；后方为修正后的水平平台。','只取第二格两人近景，第一和第三格仍不采用；不以该近景确证动态托举过程。')
# Non-destructive close-up, after repairing frame 2's incorrect rising stairs.
shots['CY028']['display_crop_normalized']=[.34,0,.60,.68]
edit('CY028',framing='近景／保持Claude左、GPT右',action='最后腕扣已解除，GPT接稳Claude的重量；不再重复解锁动作。',entry_state='GPT已扶住Claude，最后一个腕扣正在松开。',exit_state='Claude在GPT怀里，下一镜在同一平台放下。')
picture('CY028A','F',1,'Claude左、GPT右，全身站在同一祭坛平台，GPT扶住上臂，左后木架腕扣已打开。')
shots['CY027G']['display_crop_normalized']=[.14,0,.57,1]
shots['CY028A']['display_crop_normalized']=[.14,0,.57,1]
edit('CY028A',framing='全景／同一祭坛平台',action='GPT在原平台将Claude放下并扶稳；Claude双脚站住，未移动到阶下。',entry_state='Claude已获救，由GPT接住。',exit_state='Claude左、GPT右站稳；接教主的喊声，再主动握手。')
for id,sec in {'CY005':3,'CY010':3,'CY016A':4,'CY017':5,'CY019':3,'CY024':3,'CY027':3,'CY028':3}.items():edit(id,seconds=sec)
sequence=[]
def append(id):
    sequence.append(shots[id])
    for new in after.get(id,[]):append(new)
for s in old['shots']:append(s['id'])
d['shots']=sequence
t=0
for i,s in enumerate(sequence):
    if not s['invariants']:
        s['invariants']=['人物沿用当前母版；本镜起止状态与相邻镜衔接，不重复动作。']
    s['invariants']=[v.replace('CY028之前Claude始终受束','CY027G解锁前Claude始终受束') for v in s['invariants']]
    s.update(start_second=t,end_second=t+s['seconds']);t+=s['seconds']
    nxt=sequence[i+1] if i+1<len(sequence) else None
    s['next_link']=f"接 {nxt['id']}：{s['exit_state']} → {nxt['entry_state']}" if nxt else '最后停留，结束。'
    s['editorial_review']={'version':'v006','status':'static_reviewed','dynamic_execution':'pending'}
    s['visual_prompt']=f"《穿云》{s['id']}。{s['action']} 保持当前角色母本与服装。开始：{s['entry_state']} 结束：{s['exit_state']}。图内无文字。此为后续动作计划，实际生图请求另存。"
    assert s['source_quote'] in script,s['id']
for scene in d['scenes']:
    ss=[s for s in sequence if s['scene']==scene['id']]
    scene.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)))
used={s['presentation']['path'] for s in sequence}
d['page_layouts']=[p for p in d['page_layouts'] if p['path'] in used]
for key in paths:
    d['page_layouts'].append(dict(path=paths[key],cols=1 if key in ['D','F'] else 2,rows=3 if key=='D' else 2,**({'max_panel_aspect':4.0} if key=='F' else {})))
d.update(version='v0.6',revision='v006',title='《穿云》带图分镜 v0.6',total_seconds=t,story_script='剧本/穿云-场景剧本-v0.6.md',subtitle=f'六场 · {len(sequence)} 镜 · {t//60} 分 {t%60} 秒。空间与动作接续修订。',origin_manifest='镜头设计/生成记录/空间修订-v006/输出归档.json',roughcut_preview='后期/静帧配乐-v002/试听.html')
d['continuity'].update(church='面向祭坛：正门在身后，左侧洞与侧道通左阶；木架在最高祭坛平台，水盆固定最下一级阶外右侧地面，不上高台。',rice='CY001—004持碗；CY004A放在街边矮桌；CY004B—030空手；数日后街市再持碗。',restraints='单横腰链、竖向长方锁、两腕扣固定。战后CY027G先扶稳解最后腕扣，CY028接住，CY028A在同一平台站稳。',rescue_sides='CY027G—028A—029A保持Claude左/GPT右；CY028用两人近景避开未采用整格的错误楼梯。CY030是离殿背面广角，左右反转属于反向视角。',combat='殿内对峙→CY027C穿正门升空→同伴迎敌→夜空闪光→尘埃与倒地。删除旧屋顶相对站位画面，不增加打斗。')
d['revision_notes']={'author_change':'复核空间穿帮与生硬切点，优化全片静帧。','previous_manifest':'镜头设计/shot-plan-v0.5.json','previous_html':'镜头设计/带图分镜-v0.5.html','added_ids':added,'retired_ids':old['revision_notes']['retired_ids'],'reviewed_shots':len(sequence),'reviewed_cuts':len(sequence)-1,'timing':f'237秒调整为{t}秒；缩短等待，新增关系镜，保留结尾与群像。','boundary':'静帧、镜间接续与文件核验；动态动作、门闩、声音表演和新版本实际听感仍待确认。'}
d['review_intro']='补齐空手赶路、被拉下、倒地、入殿推进与最后腕扣；统一水盆、腰链和祭坛位置。'
d['review_focus']='留意从街市到宫殿、侧阶到阶下、门口到祭坛、殿内到外部上空，以及战后解锁到站稳；群像与战斗省略保留。'
write('镜头设计/shot-plan-v0.6.json',d)
print(json.dumps({'shots':len(sequence),'seconds':t,'added':added},ensure_ascii=False))
