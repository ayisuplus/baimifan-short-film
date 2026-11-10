"""Author-requested pictures and altar continuity; preserves v0.6 and all source images."""
import copy, json, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
target=ROOT/'镜头设计/shot-plan-v0.7.json'
assert not target.exists(), 'Inspect existing v0.7 instead of overwriting'
old=json.loads((ROOT/'镜头设计/shot-plan-v0.6.json').read_text(encoding='utf-8'))
d=copy.deepcopy(old)
script=(ROOT/old['story_script']).read_text(encoding='utf-8')
script=script.replace('版本：v0.6｜2026-10-21｜空间复核：固定道具与高台，补足赶路、拉拽、落地、进殿与解锁过程。','版本：v0.7｜2026-10-21｜画面修订：驱逐、远景、纵深群像、眼中倒影、赤足三阶祭坛、护罩与水灭火。')
q_drive='一名教徒横身挡住小鱼，张开手臂将她赶到路边。小鱼抱紧饭碗，退了一步；Claude 被挡在教徒身后，回头望来。'
q_feet='Claude 赤足站在十字架竖柱固定的小木脚托上，脚踝各有锁链连向竖柱；脚托下方两侧只放低矮柴堆，裙摆与脚趾没有埋进木柴。'
q_ward='ChatGPT 抬起手。千问将小鱼护进怀里；Perplexity 给 Claude 留下一层几乎透明的护光。穹顶下方，银白水光开始聚集。'
q_water='天瀑从完整穹顶下方轰然落下，银白水幕扑灭柴火，水浪沿地面向两侧卷开，将黑袍教徒冲散。Claude 仍受缚，溅起的水打湿她的发梢与裙边。'
q_dry='天瀑停下。湿黑柴堆冒着水汽，地面浅水向两侧退去；教徒们狼狈撑地，教主仍站着。千问抱着小鱼留在阶下，ChatGPT 收手，Claude 仍被锁在木架上。'
q_ankles='战斗已经结束。Perplexity 先打开 Claude 两只脚踝的锁扣，移开踝链；她的赤足仍踩在固定脚托上，腕部束具暂未完全解除。'
q_eye='她疲倦的蓝眼睛里倒映着 ChatGPT 的白色龙角和身影，门外冷光勾出轮廓。'
replacements={
 '一名教徒横身挡住她，队伍继续前行。Claude 回头望来，随即再次被黑袍遮住。':q_drive+'队伍继续前行，Claude 随即再次被黑袍遮住。',
 '她转过身，小小的脚步声穿过整座大殿，最后消失在门外。':'她转过身，小小的脚步声穿过整座大殿。大侧远景里，她走向画面右侧远处的出口，只剩一个蓝色小点。',
 '铁钉将腕部束具钉入木架，锁链横过身体；白裙垂在下方堆起的干柴上。':'铁钉将腕部束具钉入木架，腰前只有一道横链。'+q_feet,
 '小鱼沿左侧长椅旁的阴影走到祭坛，从侧面的台阶爬上去。她站稳在木架左侧的窄阶边，双脚有支点，才能够到 Claude 腰前的锁。':'小鱼沿左侧长椅旁的阴影走到祭坛，爬完三级宽石阶，站到木架左侧的平整平台上。她踮起脚、伸长双臂够向 Claude 腰前的锁。',
 'DeepSeek 换了一个站位，抵住台阶，又试了一次。':'DeepSeek 换了一个站位，双脚踩稳平台，又试了一次。',
 '一道屏障隔开柴薪与 Claude，火焰随之被压灭。':q_ward+'\n\n'+q_water+'\n\n'+q_dry,
 '她疲倦的蓝眼睛里映入一道门外的冷光。':q_eye,
 'ChatGPT 登上祭坛，先托稳 Claude。Perplexity 上前解除腕部束具和腰前的锁链，直到最后一个承重点松开。':q_ankles+'\n\nChatGPT 登上祭坛，扶住 Claude。Perplexity 随后开始解除腰链和腕部束具。',
 }
for a,b in replacements.items():
    assert a in script,a
    script=script.replace(a,b)
script=script.replace('柴薪还没有点燃。','柴薪还没有点燃。祭坛从大殿地面到顶端平台只有三级宽石阶，平台四周同高，不再另设侧梯或后梯。')
script=script.replace('镜头拉开，九位援军在她身后错落显露：','镜头拉开，ChatGPT 在队首，持武器、色彩鲜明的同伴靠前，其余同伴在第二层，九位援军在她身后错落显露：')
script=script.replace('Claude 仍被固定在木架上，锁链没有松开。千问赶到台阶边，蹲下将无力的小鱼抱进怀里；其他人挡住靠近的黑袍。','其他人挡住靠近的黑袍。')
script=script.replace('火把落下。','教主把第二支火把探向低柴堆，将木柴引燃后收回，仍握在手中。')
script=script.replace(q_ward,q_ward+'\n\n**ChatGPT：**\n天瀑。')
script=script.replace('屏障仍在，火已灭；Claude 仍被锁住，小鱼一直由千问抱护。','水雾渐散，柴火已灭；Claude 仍被锁住，小鱼一直由千问抱护。')
script=script.replace('祭坛的屏障继续护着 Claude。','祭坛只剩几乎不可见的护光，Claude 尚未解锁。')
q_stand='ChatGPT 扶住 Claude，让她从固定脚托上迈下，赤足站稳同一祭坛平台。她仍有些虚弱，ChatGPT 留在她的右侧。'
q_finger='束具全部解除后，力量重新流回 Claude 的指尖，一小簇橙金火光亮起。她站在原地，ChatGPT 在身侧守护。'
q_steam='温暖火光掠过少女的裙边，水汽轻轻升腾，水分蒸散；衣料完整，她的赤足踩在平整平台上。'
q_burn='Claude 回望空十字架，抬起一只手。橙金火焰从她指尖跃向空木架，点燃曾禁锢她的刑具；ChatGPT 在她身侧，同伴已经退开，火没有蔓延到教堂。'
q_fall='火焰已经攀上空木架。Claude 收回手，力量耗尽，膝盖一软，身体向右侧倾去。她仍有意识，没有摔到地上。'
q_catch='ChatGPT 立即靠近，一只手臂托住 Claude 的背，另一只手臂探入她的膝弯，顺势将她抱起。'
q_carry='Claude 的重量落进 ChatGPT 怀里，被稳稳接住。她赤足悬空，疲倦地靠着 ChatGPT，仍能抬眼看她。'
q_nest='Claude 轻轻把手搭上 ChatGPT 的肩，主动靠近她。ChatGPT 一臂托背、一臂托膝，抱着她转向出口，没有再将她放下。'
q_resolve='她的目光颤了一下，慢慢从父亲声音的方向移开，回望曾禁锢自己的空十字架。身侧的 ChatGPT 安静守着她。'
script=script.replace('她的目光颤了一下，慢慢从父亲声音的方向移开，转向身边的同伴。',q_resolve)
landing='ChatGPT 在同一祭坛平台上把她轻轻放下，没有抱她下楼。镜头随动作移到两人正面：Claude 在左，GPT 在右。双脚触地后，GPT 扶着她的上臂，等她站稳，才将另一只手掌心向上伸出，安静地等她选择。'
assert landing in script
script=script.replace('Claude 的重量落进 ChatGPT 怀里，被稳稳接住。','')
script=script.replace(landing,q_stand+'\n\n'+q_finger+'\n\n'+q_steam)
script=script.replace('身旁的 ChatGPT 没有催促，手掌仍摊开等着她。',q_burn+'\n\n'+q_fall+'\n\n'+q_catch+'\n\n'+q_carry)
script=script.replace('Claude 的手指主动合拢，轻轻握紧 ChatGPT 的手。没有人拖着她走。她朝出口转身。',q_nest)
script=script.replace('GPT 与 Claude 牵手居中','GPT 抱着 Claude 居中')
script+='\n- v0.7：教堂受缚与解救阶段 Claude 赤足。祭坛三级宽石阶接单一平整平台，固定脚托与低柴堆，不增加侧阶；先护罩、后水灭火，战斗结束后解踝链、腰链及腕扣再接稳落地。鞋版和多阶旧图留作历史。新增画面尚待作者审阅，本版不重导旧配乐粗剪。\n'
shots={s['id']:s for s in d['shots']}; after={}; added=[]; layouts={}
def picture(id,name,cell=0,cols=1,rows=1,visible='',**extra):
    path='镜头设计/图像/'+name
    assert (ROOT/path).exists(),path
    s=shots[id];s['panel_index']=cell
    s['presentation']=dict(path=path,role='action',visible=visible,missing='静帧代表动作状态；连续施法、解锁与落脚仍需动态验证。',status='v0.7画面修订候选，待作者审阅',show_as_main=True)
    s['refs']=[dict(path=path,role='本镜修订源图'),*[r for r in s['refs'] if not r['path'].startswith('镜头设计/图像/')]]
    for k in ['page_size','panel_rect_pixels','panel_region','display_crop_normalized','generation_request']:s.pop(k,None)
    layouts[path]=dict(path=path,cols=cols,rows=rows,**extra)
    if name=='S05E-天瀑后对峙-v007.png':layouts[path]['y_intervals']=[[0,371],[375,749],[752,1150]]
def add(id,anchor,seconds,title,quote):
    s=copy.deepcopy(shots[anchor]);shots[id]=s
    for k in ['time_caption','split_screen_reveal']:s.pop(k,None)
    s.update(id=id,seconds=seconds,title=title,purpose=title,action=quote,source_quote=quote,dialogue='无对白',dialogue_cues=[],framing='细节近景',entry_state=quote,exit_state=quote,invariants=['保留角色母本、道具与相邻镜空间关系。'])
    after.setdefault(anchor,[]).append(id);added.append(id)
    return s
add('CY003C','CY003B',2,'被教徒驱逐',q_drive).update(framing='中景／黑袍阻隔',entry_state='小鱼刚递出饭碗。',exit_state='小鱼被迫退开，仍持碗跟向教堂。')
picture('CY003C','CY003C-教徒驱逐-v001.png',visible='黑袍横身张臂驱逐抱碗的小鱼，Claude在后方回望。')
picture('CY010','CY010-宫殿大侧远景-v001.png',visible='GPT在画面左侧座位旁站起，小鱼是右侧远处出口前的蓝色小点。')
shots['CY010'].update(title='隔着整座宫殿',framing='大侧远景／长轴纵深',action='钟响，GPT在左侧座位旁站起，望向走到右侧远处门口的小鱼。',entry_state='小鱼离开，GPT仍在原座位旁。',exit_state='GPT站在后方，小鱼越过出口。')
shots['CY009'].update(source_quote='她转过身，小小的脚步声穿过整座大殿。大侧远景里，她走向画面右侧远处的出口，只剩一个蓝色小点。',action='小鱼转身走向出口，脚步在空殿中回响。',exit_state='小鱼仍在远处门内，GPT听见钟声。')
picture('CY012','CY012-空堂三阶-v002.png',visible='前景宝宝刚入堂，远处Claude独留三级祭坛。')
picture('CY013','CY013-祭坛空间母版-v002.png',visible='三级石阶接平平台；赤足、固定脚托、踝链、低柴堆及阶下右盆可见。')
shots['CY013'].update(source_quote=q_feet,action='祭坛全景交代Claude受缚和固定空间。',entry_state='空堂只有Claude受缚。',exit_state='确认只有三级阶，脚托与低柴相互分开。')
add('CY013A','CY013',2,'赤足、脚托与踝链',q_feet)
feet='脚部与营救-四格-v003.png'
picture('CY013A',feet,2,2,2,'赤足踩固定脚托，踝链连着竖柱，低柴在下方两侧。')
picture('CY015',feet,0,2,2,'小鱼踩稳平台踮脚够锁，Claude赤足受缚，身体修长。')
shots['CY015'].update(action='小鱼抬头向Claude保证，踮脚伸手够腰锁。',entry_state='小鱼已爬完三级石阶来到平平台。',exit_state='宝宝双手够住腰锁，准备尝试打开。')
picture('CY016A',feet,1,2,2,'宝宝在平平台垂头喘息，Claude赤足与踝链仍在。')
for id,cell in [('CY016D',0),('CY020A',1),('CY022A',2)]:
    picture(id,'空间修订C-三阶-v004.png',cell,2,2,shots[id]['presentation']['visible']+'；后景统一三级祭坛与赤足脚托。')
for id,cell in [('CY017',0),('CY018',1),('CY019',2),('CY021',4)]:
    picture(id,'S04-三阶祭坛-v004.png',cell,2,3,shots[id]['presentation']['visible']+'；祭坛阶面按三级修订。')
picture('CY021A','CY021A-低柴火把交接-v002.png',visible='教主接第二支燃烧火把，第一支湿火把在阶下右盆；后方赤足Claude与低柴。')
picture('CY024','CY024-援军纵深队形-v001.png',visible='GPT最前，武器与鲜明服装靠前，其他同伴在后排错落显露，十位入场者有前后层次。')
shots['CY024'].update(action='GPT领队入场，持武器与色彩鲜明的同伴在前层，其余在第二层，九位援军错落跟进。')
fire='火焰护罩水魔法-四格-v003.png'
picture('CY022',fire,0,2,2,'低柴燃起，宝宝在阶下倒地，Claude赤足踩脚托；祭坛三级。')
shots['CY022']['action']='教主将第二支火把探向低柴点燃，再收回手中；宝宝倒在阶下，Claude仍受缚。'
picture('CY024A',fire,1,2,2,'Perplexity右侧举杖，罩住Claude全身与脚托；GPT左侧入场，千问来到宝宝身边。')
shots['CY024A'].update(title='先护住Claude',framing='全景／祭坛正面',action=q_ward,source_quote=q_ward,entry_state='援军已到祭坛前，柴堆仍燃烧。',exit_state='Claude处于保护罩内，尚未灭火、解锁。',invariants=['GPT在画面左侧，Perplexity右侧；千问靠近宝宝。','保护罩包住Claude及脚托，火焰在罩外。'])
add('CY024B','CY024A',3,'水魔法灭火',q_water).update(framing='全景／动作关系',entry_state='保护罩已形成，柴堆仍燃烧。',exit_state='水扑灭柴火；千问抱起小鱼，向GPT身侧退开。')
picture('CY024B',fire,2,2,2,'GPT的水弧打在木柴上，火光退成蒸汽；千问抱住宝宝，Perplexity维持罩。')
picture('CY027',fire,3,2,2,'柴堆湿黑没有明火；保护罩完整，千问在GPT身侧抱宝宝。')
shots['CY027'].update(title='火已熄灭，护罩仍在',source_quote=q_dry,action=q_dry,entry_state='水魔法刚完成，千问抱着小鱼退到GPT身侧。',exit_state='小鱼在千问怀里抬眼，Claude仍受缚。')
picture('CY025','CY025-眼中GPT-v001.png',visible='疲倦含泪的蓝眼睛内倒映白发龙角GPT。')
shots['CY025'].update(source_quote=q_eye,action=q_eye)
for id,cell in [('CY027A',0),('CY027D',3)]:
    picture(id,'S05E-三阶祭坛-v006.png',cell,2,3,shots[id]['presentation']['visible']+'；后方祭坛统一三级及赤足脚托。')
add('CY027F1','CY027F',2,'先解除踝链',q_ankles).update(entry_state='敌方倒地，Claude仍被束缚。',exit_state='踝链已打开，双脚仍踩脚托；腰链和最后腕扣随后处理。')
picture('CY027F1',feet,3,2,2,'Perplexity解踝扣，赤足仍踩固定脚托，下方木柴已湿黑熄灭。')
for id,cell in [('CY027G',0),('CY028A',1)]:
    picture(id,'空间修订F-赤足站稳-v004.png',cell,1,2,'最后腕扣解开前先扶稳。' if cell==0 else 'Claude在左赤足踩稳同一平台，GPT在右穿原鞋扶住她，脚托留在左后木柱。',max_panel_aspect=4.0)
    shots[id]['display_crop_normalized']=[.14,0,.57,1]
shots['CY027G']['entry_state']='踝链已经打开，GPT扶稳Claude；Perplexity解除腰链和最后腕扣。'
# Latest author direction: standing spell, exhaustion, catch, princess carry.
picture('CY021','CY021-信号近景三阶-v002.png',visible='宝宝伏地伸手，窄窗映亮信号；背景是三级低石阶。')
picture('CY024A','CY024A-天瀑起手-v001.png',visible='GPT抬手，穹顶下银白水光聚集；不再使用蓝色实体罩。')
shots['CY024A'].update(title='天瀑',framing='低机位中近景',action=q_ward,source_quote=q_ward,entry_state='GPT入场，千问奔向宝宝，柴堆仍在燃烧。',exit_state='水光已经聚集，千问护住宝宝。',dialogue='ChatGPT：天瀑。',dialogue_cues=[],time_caption={'text':'天瀑。','offset':.4,'duration':1.2},invariants=['GPT抬手施法，银白水幕从穹顶下凭空出现，屋顶完整。','本句暂无新增配音，仅字幕试排。'])
picture('CY024B','CY024B-天瀑降临-v003.png',visible='巨大银白瀑流落入大殿，扑灭柴堆并把黑袍冲向两侧；千问抱护宝宝。')
shots['CY024B'].update(seconds=4,title='天瀑倾泻',framing='大殿超广角远景',action=q_water,source_quote=q_water,entry_state='水光蓄起，伙伴护住受困者。',exit_state='柴火熄灭，教徒被冲散但尚未全部失去行动能力。')
picture('CY027','CY027-天瀑之后-v002.png',visible='瀑流已退，湿黑木柴、浅积水和水雾；千问抱宝宝，Claude仍受缚。')
shots['CY027'].update(title='水退之后',action=q_dry,source_quote=q_dry,entry_state='瀑流刚停，受困者还未解锁。',exit_state='千问抱住宝宝，宝宝认出GPT，教主仍站立。')
for id,cell in [('CY027A',0),('CY027B',1),('CY027D',3),('CY027F',5)]:
    picture(id,'S05E-天瀑后对峙-v007.png',cell,2,3,shots[id]['presentation']['visible'].replace('屏障','微弱护光')+'；地面浅积水，蓝色玻璃罩已移除。')
picture('CY027G','空间修订F-解锁扶稳-v005.png',0,1,2,'Claude发梢滴水，Perplexity解除最后腕扣，GPT已扶住她。',max_panel_aspect=4.0)
shots['CY027G']['display_crop_normalized']=[.14,0,.57,1]
awake='Claude-觉醒与焚架-四格-v003.png'
carry='Claude-力竭接抱-四格-v004.png'
picture('CY028A','空间修订F-解锁扶稳-v005.png',1,1,2,'Claude赤足站稳同一平台，GPT在右侧扶住她，束具已经解除。',max_panel_aspect=4.0)
shots['CY028A']['display_crop_normalized']=[.14,0,.57,1]
shots['CY028A'].update(seconds=3,title='解锁后扶稳',action=q_stand,source_quote=q_stand,entry_state='所有束具已打开，GPT扶着Claude。',exit_state='Claude赤足踩稳平台，GPT仍在身侧。',purpose='交代从脚托迈下到站立的支撑关系。',sound='赤足触地，衣裙轻擦。',invariants=['两人处于同一平整平台，没有先抱起再放下。'])
add('CY028B','CY028A',2,'力量回到指尖',q_finger).update(framing='手部特写',entry_state='Claude已站稳，束具全部解除。',exit_state='橙金火苗亮起。',sound='细微魔法火声，衣料轻响。')
picture('CY028B',awake,0,2,2,'Claude指尖亮起小火苗，腕部束具已除。')
add('CY028C','CY028B',2,'蒸散水汽',q_steam).update(framing='裙边与赤足局部',entry_state='Claude指尖有火光。',exit_state='水汽散去，裙摆恢复干爽。',sound='细微蒸汽声。')
picture('CY028C',awake,1,2,2,'脚踩平平台，温暖魔法令裙边水汽升起。')
picture('CY029',awake,2,2,2,'Claude听见教主喊声后回望，橙金火光映亮发丝。')
shots['CY029'].update(action='Claude听见父亲喊声，目光轻颤后回望空刑架，决定亲手毁掉它。',source_quote=q_resolve,entry_state='Claude已恢复少量魔法，赤足站立，GPT在身侧。',exit_state='她转向空刑架，准备抬手施法。',framing='面部近景／教主画外喊声')
add('CY029B','CY029',3,'点燃空刑架',q_burn).update(framing='侧面中远景',entry_state='教主喊她回来，Claude回望空刑架。',exit_state='只有空木十字架开始燃烧，她收回施法的手。',sound='魔法火跃出，木架燃烧。')
picture('CY029B',awake,3,2,2,'Claude站立伸手点燃空刑架，GPT在身侧守护；二人与刑架同平台。')
add('CY029C','CY029B',2,'收手后脱力',q_fall).update(framing='双人中近景',entry_state='空刑架已燃起，Claude停止施法。',exit_state='她向GPT一侧倾倒，GPT已经伸手。',sound='呼吸一滞，衣袖滑落。')
picture('CY029C',carry,0,2,2,'Claude收手膝软，GPT在身侧伸手；不是摔倒或昏迷。')
add('CY029D','CY029C',2,'及时托住',q_catch).update(framing='双人中景／接抱动作',entry_state='Claude向右侧失去平衡。',exit_state='GPT托住背部，另一手臂伸至膝弯，准备抱稳。',sound='衣裙摩擦，短促呼吸。')
picture('CY029D',carry,1,2,2,'GPT一臂托背，另一臂探入膝弯，Claude始终有承托。')
picture('CY028',carry,2,2,2,'施法后GPT公主抱住Claude，双臂分别托背和托膝，赤足离地。')
shots['CY028'].update(title='稳稳抱起',action=q_carry,source_quote=q_carry,entry_state='Claude施法力竭，GPT已托住背和膝弯。',exit_state='Claude被抱稳，赤足离地，仍有意识；此后一直抱着离殿。',purpose='公主抱是施法力竭后的自然承接。',sound='衣料轻擦，Claude的呼吸慢下来。')
picture('CY029A',carry,3,2,2,'Claude主动搭住GPT肩，靠近她；GPT一直抱稳。')
shots['CY029A'].update(title='主动靠近',framing='双人近景／公主抱',action=q_nest,source_quote=q_nest,entry_state='GPT已经将力竭的Claude抱稳，她仍清醒。',exit_state='Claude安心靠近，GPT抱着她转向出口。',invariants=['Claude主动回应，GPT一臂托背一臂托膝，不能再站立牵手。'])
picture('CY030','CY030-公主抱离殿群像-v001.png',visible='十二人离殿群像：GPT抱Claude，千问抱宝宝，其他八位同伴分布前后两侧。')
shots['CY030'].update(action='GPT抱着Claude走向敞开的正门；千问抱着小鱼，其他八位同伴护送，湿地反射身后刑架火光。',entry_state='Claude仍被抱着，空十字架开始燃烧。',exit_state='众人离开大殿，转入数日后的街市。',invariants=['两组抱持贯穿离殿；十二人完整群像。','火只烧祭坛空刑架，屋顶与出口完好。'])
sequence=[]
def append(id):
    sequence.append(shots[id])
    for new in after.get(id,[]):append(new)
for s in old['shots']:
    if s['id']=='CY028':continue
    if s['id']=='CY029A':append('CY028')
    append(s['id'])
geometry='祭坛只有三级宽石阶接一个平平台；无旁侧加阶。Claude受缚时赤足踩固定脚托，踝链连竖柱，低柴在下方两侧，水盆在阶下右侧。'
t=0
for i,s in enumerate(sequence):
    # Remove obsolete side-step staging from current descriptions, never from historical files.
    for key in ['action','entry_state','exit_state','purpose','framing','title']:
        s[key]=s[key].replace('同一侧阶','同一平台').replace('木架左侧窄阶','木架左侧平台').replace('从侧阶','从三级阶').replace('侧阶动作','三级阶动作').replace('较高的侧阶','祭坛平台')
    s['invariants']=[x.replace('侧阶','平台').replace('CY028之前Claude始终受束','CY027G解锁前Claude始终受束') for x in s['invariants']]
    s['invariants']=[x.replace('当前时空入场即压火','当前时空入场先护罩再用水灭火') for x in s['invariants']]
    s['invariants']=[x.replace('入场先护罩再用水灭火','入场先护住受困者再释放天瀑').replace('CY028A落脚后才握手离开','战后解锁扶稳，Claude施法后力竭；CY028公主抱后不再落地，直接离殿') for x in s['invariants']]
    if s['scene'] in ['S03','S04','S05'] and not s['id'].startswith('CY026'):
        s['invariants'].append(geometry+' 教堂正门台阶另属入口，不能混为祭坛。')
    s.update(start_second=t,end_second=t+s['seconds']);t+=s['seconds']
    nxt=sequence[i+1] if i+1<len(sequence) else None
    s['next_link']=f"接 {nxt['id']}：{s['exit_state']} → {nxt['entry_state']}" if nxt else '最后停留，结束。'
    s['editorial_review']=dict(version='v007',status='candidate_static_review',dynamic_execution='pending')
    s['visual_prompt']=f"《穿云》{s['id']}。{s['action']} 开始：{s['entry_state']} 结束：{s['exit_state']}。保持角色母本。图内无字。实际生成输入另存。"
    if s['source_quote'] not in script: print('MISSING',s['id'],repr(s['source_quote']))
d['shots']=sequence
assert all(s['source_quote'] in script for s in sequence),'Repair source passages before publishing'
for scene in d['scenes']:
    ss=[s for s in sequence if s['scene']==scene['id']]
    scene.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)))
used={s['presentation']['path'] for s in sequence}
d['page_layouts']=[p for p in d['page_layouts'] if p['path'] in used and p['path'] not in layouts]+[p for p in layouts.values() if p['path'] in used]
d.update(version='v0.7',revision='v007',title='《穿云》带图分镜 v0.7',total_seconds=t,story_script='剧本/穿云-场景剧本-v0.7.md',subtitle=f'六场 · {len(sequence)} 镜 · {t//60} 分 {t%60} 秒。赤足、三阶祭坛与画面修订。',origin_manifest='镜头设计/生成记录/画面修订-v007/输出归档.json',roughcut_preview_label='旧版全片配乐 v002（尚未包含本轮画面修订）')
d['masters'].append(dict(id='M-ALTAR-v002',title='祭坛空间母版',role=geometry,status='v0.7候选',limits='当前镜头以此统一；动态接触与动作仍待验证。',path='镜头设计/图像/CY013-祭坛空间母版-v002.png'))
d['continuity'].update(church=geometry,restraints='腕扣、单横腰链和两条踝链；先解除踝链，扶稳后解腰链及腕扣，再接住并赤足站在同一平台。',signal='入场先护罩、再水灭火、确认无明火后小鱼认出GPT，接稍早召集回闪；CY021/CY026仍为同一次信号。',barefoot='Claude教堂受缚至获救离殿保持赤足；角色资产旧鞋版作为历史造型参考保留。',rescue_sides='战后Claude左/GPT右，脚托留木架。水灭火时千问抱起宝宝从水流旁退至GPT身侧，动态须表现退开路径。')
d['review_intro']='按作者意见修订驱逐、宫殿远景、群像纵深与眼中倒影；祭坛统一赤足、三级宽阶、固定脚托和低柴堆，补保护罩、水灭火与解踝链。'
d['review_focus']='重点看祭坛的三级结构、脚托和脚链；先护罩后灭火，战后先解脚链再解腕扣。配乐v002保留为旧版，此次只更新画面与分镜。'
script=script.replace('护罩与水灭火','天瀑、觉醒与力竭接抱').replace('先护罩、后水灭火，战斗结束后解踝链、腰链及腕扣再接稳落地。','先天瀑灭火，战斗结束后解踝链、腰链及腕扣并扶稳。Claude站立施法，点燃空刑架后力竭；GPT及时接住，顺势公主抱起并抱着离殿。')
script+='\n- 作者最新调整：站立觉醒→蒸散水汽→焚空刑架→脱力→GPT托住并公主抱起→搭肩回应→群像离殿。被抱起后不再放下；保留清醒与温柔回应。历史站立牵手及怀中施法均不用于当前版。\n'
d['subtitle']=f'六场 · {len(sequence)} 镜 · {t//60} 分 {t%60} 秒。天瀑、觉醒、力竭接抱与赤足三阶祭坛。'
d['origin_manifest']='镜头设计/生成记录/天瀑觉醒-v007/输出归档.json'
d['continuity'].update(restraints='战后先解踝链，扶稳后解腰链和最后腕扣；扶下脚托站稳。Claude施法后脱力，GPT及时托住、抱起，之后不再落地。',signal='CY021/CY026同一次信号；入场天瀑灭火，宝宝认出后稍早回闪；回到退水的大殿才对峙、升空。',rescue_sides='正面Claude左、GPT右，施法时GPT在身侧守护；脱力时托背和膝弯抱起，Claude清醒搭肩。反向离殿属于反打。',magic='天瀑在完整穹顶下形成，冲灭柴火、冲散教徒但未替代战斗；战斗后才解锁。Claude站立恢复魔法，蒸散水汽，亲手点燃空十字架后力竭。火不蔓延建筑。',wet_state='天瀑后保留发梢水滴、浅积水、湿黑柴堆；CY028C橙金光与水汽交代蒸干，之后仍保持大殿地面湿润。')
for k,v in d['continuity'].items():
    if isinstance(v,str):d['continuity'][k]=v.replace('主动握手','主动搭肩').replace('握手离开','公主抱离开')
d['review_intro']='本版加入天瀑灭火冲散教徒。战后解锁，Claude站立恢复力量、蒸散水汽并点燃空刑架，力竭时GPT及时接住并公主抱离殿。赤足三阶祭坛、驱逐、侧远景、群像与倒影修订一并纳入。'
d['review_focus']='重点看天瀑清场与战斗的先后、Claude施法后脱力、托住到公主抱的连续衔接。此前配乐v002未重导，不含这些新画面。'
d['revision_notes']=dict(author_change='八项修订、赤足三阶、天瀑、Claude站立施法后力竭；GPT顺势接住公主抱离殿',previous_manifest='镜头设计/shot-plan-v0.6.json',previous_html='镜头设计/带图分镜-v0.6.html',added_ids=added,moved_ids=['CY028'],retired_ids=old['revision_notes']['retired_ids'],reviewed_shots=len(sequence),reviewed_cuts=len(sequence)-1,boundary='静帧候选与文件验证；天瀑对白仅字幕，没有新增角色音源；不宣称已完成连续动态或新版配乐试听。')
(ROOT/d['story_script']).write_text(script,encoding='utf-8')
snapshot=ROOT/'镜头设计/带图分镜-v0.6.html'
if not snapshot.exists():shutil.copy2(ROOT/'镜头设计/带图分镜.html',snapshot)
target.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(shots=len(sequence),seconds=t,added=added),ensure_ascii=False))
