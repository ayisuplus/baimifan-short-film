"""Versioned fire-ritual revision; existing media and music marks are retained."""
import copy, hashlib, json, re, shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/火祭因果-v040'
IMG='镜头设计/图像/火祭因果-v040'
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,s):(R/p).parent.mkdir(parents=True,exist_ok=True);(R/p).write_text(s,encoding='utf-8')
def save(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
assert not (R/'镜头设计/shot-plan-v0.40.json').exists(), 'Version already exists; preserve current revision.'
old=json.loads(read('镜头设计/shot-plan-v0.39.json'))
d=copy.deepcopy(old);by={s['id']:s for s in d['shots']}
script=read(old['story_script'])
# New causal rules replace obsolete global instructions, including per-shot invariants.
torches='全段只有一支手持火把：教徒铺柴完毕后，CY021A教主右手接过；CY019小鱼张臂挡路；CY020B教主左手推开她、右手持火；随后抓袍失败、教主登顶点燃高柴，返回下段缓台。没有火把落盆或第二支火把。'
wood='祭前脚托两侧只有低矮底柴。全体教徒去侧院柴库取乌烬木，每人一根，返回后依次铺到Claude腰腹；脸、胸口和受缚双臂仍露出。CY024K1—K2由Kimi暗月破开高柴、向两侧推散，随即形成贴身月辉；残柴仍燃，直到水雷灭火。脚托、刑架和束具始终完整；灭火后散湿木不挡接近解锁的落脚位。'
obs='宝宝开锁失败后冲下长阶，先抓木被推开，撑起再拦腿被踢开；她再次起身，张开双臂用身体挡住持火教主，没有魔法屏障。教主推开她后，仍接倒地、抓袍、衣角滑脱。教主右手持同一支火把登顶点燃高柴，返回下段缓台。'
lighting='苍龙雷渊前六火盆、中央环形烛式吊灯、两后墙壁烛和两石座单烛发暖光。祭前低柴、回堂后高柴，到CY022才点燃。Kimi破柴后两侧与脚下散柴仍燃紫黑火；CY024B后所有普通灯火与残柴熄灭。冷月光照明，后殿拱顶完整；最后空刑架星火不重新点亮普通灯具。'
def clean(t):
    t=t.replace('到侧院休息','到侧院柴库取乌烬木').replace('去侧院休息','去侧院柴库取乌烬木').replace('休息回来的教徒提着灯','取柴回来的教徒每人抱一根乌烬木、由前列提灯')
    t=t.replace('第二支火把','这支火把').replace('第二火把','火把')
    t=t.replace('直接浇灭低柴','直接浇灭已被Kimi推散的残柴')
    t=t.replace('低柴已熄灭','散柴已熄灭').replace('教堂内低柴已燃','教堂内高柴已燃')
    return t
# Replace complete invariant sentences instead of retaining contradictory torch instructions.
for s in d['shots']:
    inv=[]
    for v in s['invariants']:
        if v.startswith('第一支火把落在'):v=torches
        elif v.startswith('宝宝登顶尝试开锁'):v=obs
        elif v.startswith('苍龙雷渊前六火盆'):v=lighting
        else:v=clean(v)
        inv.append(v)
    s['invariants']=inv
for k in ['magic','lighting','altar_lighting_v023']:d['continuity'][k]=lighting
d['continuity'].update(torches=torches,obstruction=obs,ritual_wood=wood,
 discovery='CY010A教徒集体去取乌烬木，留出潜入窗口；CY016B听见抱柴队伍返回；CY016C每人一根木头入堂。',
 doors='教徒由侧门去侧院柴库取乌烬木，按仪式经正门列队回堂；小鱼钻左侧墙洞。CY016D队尾关门落闩，CY023踹开，之后正门开放。',
 remaining_image_sync='v0.40按搬柴、逐次阻拦及Kimi暗月破柴方案更新相关画面；旧图和中间方案保留，新图待作者审阅。其余已确认静帧继续沿用。',
 kimi_dark_moon='CY024护住她们→CY024K1暗月裂开高柴→CY024K2木块向两侧散落、银白轮缘闭合为贴身月辉→CY023A骑士跟进→召集回闪。两项动作连续完成，保护先于长咏唱；Kimi始终在右侧柱边遥控，未瞬移登台。',
 water_impact_insert='水雷扑灭所有残柴与普通灯火；高柴此前已由Kimi破开，CY024B1保留大水掀走长椅。水冲柴小浪镜CY024B2撤出本版，不接入镜序。',
 claude_shield='Kimi在入场命令后立即暗月裂柴、紧接贴身月辉护持，CY024K1—K2连成一次出手。月辉只护Claude，不罩刑架或木柴；A1/A2维持保护，水雷可直接扑灭两侧残柴，战后撤辉再登阶解锁。')
# New shots clone only a plain still-shot schema.
def newshot(id,base,seconds):
    s=copy.deepcopy(by[base]);s.update(id=id,seconds=seconds,dialogue='无对白',dialogue_cues=[])
    for k in ['subtitle_cues','time_caption','final_static_review','final_review_exception','split_screen_reveal']:s.pop(k,None)
    by[id]=s
    return s
newshot('CY017A','CY017',2)
newshot('CY018B','CY018',3)
newshot('CY024K1','CY024A1',3)
newshot('CY024K2','CY024A2',3)
# Every changed action has a screenplay passage, stage state and audio note.
changes={
'CY016C':('人手一木，返回教堂','门被推开。取柴回来的教徒每人横抱一根粗黑色乌烬木，前列有人一臂托木、一手提灯，沿中央通道列队进入。他们看见了站在Claude身旁的小鱼。','教徒取柴返回，柴堆尚低。','队列朝祭坛继续走，小鱼被发现。','密集脚步、粗木互碰、提灯轻响'),
'CY016D':('抓住第一根木头','最后一名教徒在队尾掩门落闩。DeepSeek松开没能打开的锁，急切地沿长阶冲到下端，双手抓住一名搬柴教徒怀中乌烬木伸出的那一端，想拦住他。','小鱼在高处开锁失败，看见抱柴队列。','她抓牢一根木头，教徒仍要前进。','下阶脚步、抓木摩擦、急喘；没有手持火焰'),
'CY017':('被推开，还想阻止','教徒一臂抱稳木头，另一只手将小鱼推到一旁。她失去重心半跪撑地，另一只手仍朝被带走的木头伸着；更多黑袍从身边经过，踏上长阶。','小鱼抓木阻拦。','她撑地半跪，搬柴队伍没有停。','衣料推擦、膝掌落地、木头与脚步不断'),
'CY017A':('一根接一根','祭坛上，一双黑金袍袖里的手把乌烬木横放下去。后一名教徒抱着下一根等在旁边。木头相继落下，先遮住脚凳和脚踝，又沿白裙往上堆。','教徒陆续登上最高祭坛。','底柴累积成堆，脚凳逐渐被遮住。','厚木落堆闷响、树皮摩擦，落点清楚'),
'CY018':('拦住下一个，又被踢开','小鱼撑起身，又扑向另一名搬柴教徒，抱住他的小腿。对方怀里仍抱着木头，用靴子将她拨踢到一旁；她滑倒在阶下，手还朝那条腿伸着。黑袍继续向上。','小鱼从第一次推开中撑起，再拦另一人。','她第二次倒下，队伍继续铺柴。','靴底拨踢、衣料擦地、短促气声；不夸张重击'),
'CY018B':('柴堆吞没白裙','最后一根乌烬木被放上去。低机位看，粗黑木堆一直压到Claude腰腹，把白裙下半部和脚凳吞没；她的脸、胸口和受缚双臂还露在上方。教徒空手退下，所有柴尚未点燃。','两次阻拦都没能让铺柴停下。','柴堆完成，Claude腰腹以下被遮住，教徒退开。','最后一根木头落定，退下脚步，吟唱渐起'),
'CY021A':('教主接过火把','Claude的父亲穿着教主礼服走到长阶下端。一名教徒递来燃着的火把，教主右手接牢，抬头望向被高柴围住的Claude。\n\n**教主：**\n我的女儿，神明在等你。','教徒铺柴完毕，教主准备执行火祭。','教主持唯一一支火把；小鱼看见后再次站起。','火苗近响、吟唱底声，教主平静说话'),
'CY019':('最后一次，张开双臂','小鱼看见教主接过火把，双手撑地，踉跄站起来，重新挪到长阶下端中央，张开双臂挡住通往Claude的路。帽子歪了，腿在发抖，她用身体挡路，没有施放魔法。\n\n**教主：**\n让开。','她被踢倒；教主已经接火准备登阶。','她站稳张臂，坚持不让。','衣料摩擦、颤抖呼吸，教主短促命令'),
'CY020B':('持火的父亲推开她','从小鱼身后贴地仰拍，她张开双臂，挡在高大的教主面前。教主右手把唯一的火把举在远离孩子的一侧，左手将她推开。她失衡偏向一旁，教主的脚步没有停。','小鱼用身体挡在教主面前。','她被推得失衡，火把始终在教主右手。','一步逼近、衣料推擦、急促吸气'),
'CY022A1':('一步一步登阶','背后低机位望去，教主右手握着同一支火把，一步一步踏上长阶。鞋底敲出沉重回声；高处Claude腰腹以下陷在黑木堆里，小鱼留在下端。','衣角从小鱼手里滑脱。','教主登上最高祭坛，靠近高柴下侧。','沉重登阶声、火把呼声、吟唱不断'),
'CY022':('点燃高柴','近处，教主将右手火把压向高高堆起的乌烬木下侧。普通橙火碰到黑木，树脂裂隙先亮，随即吐出黑色焰芯、暗紫细边的火舌，沿层叠木缝向上窜。教主收回火把，返回长阶下段；高柴的火焰迅速连成一片，卷向刑架中央。','高柴围住Claude腰腹，尚未点燃。','高柴整体起火，教主退回下段缓台。','火头触木、树脂爆响、黑焰低吼，退阶脚步'),
'CY024K1':('月之暗面，裂柴','Kimi在右侧柱边抬起空手。彩窗透来的冷月光沿她指尖聚成一轮暗月，深黑月面只留细银白轮缘。她收拢手指，月影越过长阶，钻入高柴缝隙；木纹沿银白细线裂开，整座柴堆向两侧松动，刑架和束具丝毫未动。','GPT刚命令护住她们，高柴仍燃。','高柴已裂开，木块开始朝外下方散落。','低沉月影掠过、密集木裂声；没有流水声'),
'CY024K2':('暗面破柴，月辉护身','切回Claude。高柴被月影从中央向两侧推开，粗木翻落在脚凳外围；她焦黑破边的白裙和完整脚凳重新露出，镣铐仍在。紧接着，暗月的银白轮缘沿她肩膀、衣袖和裙摆合成薄薄的贴身月辉。火焰仍在身体之外的残柴上燃烧，月辉隔住逼近的焰尖，不包住木架。破柴与护身连成一次出手，没有停下来等待长咏唱。','Kimi月影已裂开柴堆。','高柴变为两侧低散柴，Claude已受贴身月辉保护。','木块向外落地、银白护光轻鸣、外围火焰仍响')
}
for id,(title,quote,entry,exit,sound) in changes.items():
    s=by[id];s.update(title=title,source_quote=quote,action=quote.split('\n\n**')[0],entry_state=entry,exit_state=exit,sound=sound,purpose=title+'，补足行动因果。')
    if id in ['CY017','CY017A','CY018','CY018B','CY024K1','CY024K2']:
        s.update(dialogue='无对白',dialogue_cues=[]);s.pop('subtitle_cues',None)
by['CY021A'].update(seconds=5,dialogue='教主：我的女儿，神明在等你。',dialogue_cues=copy.deepcopy(next(s for s in old['shots'] if s['id']=='CY017')['dialogue_cues']))
by['CY019']['framing']='下段阶下正面全景，张臂的孩子与高处柴堆同框'
by['CY017A']['framing']='最高祭坛铺柴手部近景'
by['CY018B']['framing']='最高祭坛低机位中景，黑木堆压满前景'
by['CY024K1']['framing']='右侧柱边Kimi近中景，远处高祭坛同框'
by['CY024K2']['framing']='最高祭坛正面近中景，木块朝两侧落下'
by['CY024K1']['asset_ids']=copy.deepcopy(by['CY024A1']['asset_ids'])
by['CY024K2']['asset_ids']=copy.deepcopy(by['CY024A2']['asset_ids'])
# Full S04 replacement, retaining unchanged dialogue passages and their original images.
s04=['## S04｜教堂祭坛·夜·内','人物：DeepSeek、Claude、教主、黑袍教徒。']
for id in ['CY016D','CY017','CY017A','CY018','CY018B','CY021A','CY019']:
    s04.append(by[id]['source_quote'])
s04+=['语气短促，带着习惯别人服从的口气。小鱼没有让。',
'教主一步步逼近小鱼。衣袍摩擦声压过她的喘息。画面留在 Claude 的脸上，她的目光随着下方的动静一次次移动。',
'**Claude：**\n别碰她！','她猛然挣扎，木架与锁链一同震响。',
by['CY020B']['source_quote'],by['CY020A']['source_quote'],'Claude望着她，再看向父亲。',
by['CY021']['source_quote'],'声音比“别碰她”低下来；她试着叫住父亲，让他听进去。教主没有回答。',
by['CY021B']['source_quote'],'教主继续迈步。衣料从指间滑脱，小鱼的手落回冰凉的石面。',
by['CY022A1']['source_quote'],by['CY022']['source_quote'],'小鱼仍朝她伸着手，嘴唇动了一下，没有发出声音。',
by['CY022B']['source_quote'],'吟唱逐渐增强，盖过木柴的爆裂声。',by['CY022B2']['source_quote'],
'吟唱在这个大景别中汇成低沉的人声，跨切到随后殿外风起的画面。画外风声渐强；到破门前切回教堂内部，吟唱重新清楚，随破门声骤然中断。']
a=script.index('## S04｜');b=script.index('## S05｜')
script=script[:a]+'\n\n'.join(s04)+'\n\n'+script[b:]
script=script.replace('仪式尚未正式开始。教徒们暂时离开教堂，到侧院休息。最后一盏提灯从门口转过，脚步与低声交谈渐渐远去。','仪式尚未正式开始。侧院柴库传来召令，教徒们依仪式集体离堂，每人须取一根乌烬木再列队回堂。最后一盏提灯从侧门转过，脚步渐远。\n\n**教徒（画外）：**\n取乌烬木，一人一根。')
script=script.replace('脚托下方两侧只放低矮柴堆','脚托下方两侧只放预先铺好的低矮底柴')
script=script.replace('；右盆稍后接住被撞落的第一支火把','')
script=script.replace('这时，门外传来熟悉的脚步和低语。','这时，门外传来熟悉的脚步、木头磕碰与低语。')
script=script.replace('门被推开。休息回来的教徒提着灯走进教堂，灯光沿中央通道扫向祭坛。\n\n他们看见了站在 Claude 身旁的小鱼。',by['CY016C']['source_quote'])
script=script.replace('后面的黑袍越过他，朝祭坛快步走来。','后面的黑袍抱着木头越过他，朝祭坛走来。')
oldprotect='说得平稳、短促，不必喊成战斗口号。她们没有停步，Kimi循GPT的视线望向高处Claude，抬起空手转向右侧柱廊；一道细薄月辉立即先抵达Claude的衣袖和裙边，把逼近身体的黑焰隔开。千问奔向小鱼。此刻保护已经起效，后续抬手与月辉近景是维持状态的展示，不能等长咏唱过半才开始救人。'
newprotect='说得平稳、短促。她们没有停步，千问奔向小鱼；Kimi循GPT的视线望向高处Claude，转到右侧柱旁，立即出手。\n\n'+by['CY024K1']['source_quote']+'\n\n'+by['CY024K2']['source_quote']
assert oldprotect in script
script=script.replace(oldprotect,newprotect)
# Align old source excerpts with edits to overlapping paragraphs.
for s in d['shots']:
    if s['id'] not in changes and oldprotect in s.get('source_quote',''):
        s['source_quote']=s['source_quote'].replace(oldprotect,newprotect)
# Header/global paragraphs are current rules; historical appendix is preserved separately.
marker='## 历史制作交接备注'
main,sep,hist=script.partition(marker)
main=clean(main)
main=re.sub(r'宝宝登顶尝试开锁，随后冲下长阶[^\n]+',obs,main,count=1)
main=re.sub(r'苍龙雷渊前六火盆、一盏中央环形烛式吊灯[^\n]+',lighting,main,count=1)
main=main.replace('身体外烈火仍包围并遮挡；水雷随后扑灭全部祭薪','暗月先破开高柴，身体外的散柴仍燃；水雷随后扑灭全部祭薪')
main=main.replace('身体以外的清水直接抵达石台与低柴，把火浇灭','身体以外的清水直接抵达石台与已被Kimi推散的残柴，把火浇灭')
main=main.replace('## 乌烬木与星火 · v0.36','## 乌烬木、暗月与星火 · v0.40\n\n'+wood)
script=main+(sep+hist if sep else '')
script=script.replace('版本：v0.39｜2026-10-23｜收尾审查；画面沿用v0.38，补回两句已定咒语，清理旧说明。','版本：v0.40｜2026-10-24｜搬柴火祭、两次阻拦、最后张臂；Kimi暗月破柴与贴身护盾。新画面待作者审阅。',1)
# Sync exact quotations changed by the general edits.
for s in list(by.values()):
    if s['id'] not in changes:
        q=clean(s['source_quote']).replace('脚托下方两侧只放低矮柴堆','脚托下方两侧只放预先铺好的低矮底柴').replace('；右盆稍后接住被撞落的第一支火把','').replace('身体以外的清水直接抵达石台与低柴，把火浇灭','身体以外的清水直接抵达石台与已被Kimi推散的残柴，把火浇灭')
        s['source_quote']=q
# Departure motivation is audible; new voice is not fabricated from old takes.
by['CY010A'].update(action='小鱼在侧墙洞口等待；听见“一人一根”的取柴召令，见最后提灯转入柴库才动身。',dialogue='教徒（画外）：取乌烬木，一人一根。',dialogue_cues=[],subtitle_cues=[dict(speaker='教徒（画外）',text='取乌烬木，一人一根。',offset=0,duration=3.8)])
by['CY010A']['sound']='画外取柴召令（新增，待配音）、脚步远去、夜风与教堂灯火。'
by['CY024']['action']='GPT入殿命令“护住她们”；千问奔向小鱼，Kimi转向右侧柱边准备立即暗月破柴。'
by['CY024']['exit_state']='两人立即分工，切Kimi暗月裂柴；保护在随后连续两镜内完成。'
by['CY024A1']['action']='Kimi在右侧柱边维持银白月辉；远处高柴已由她推散为低残柴，火焰仍燃，Claude被贴身保护。'
by['CY024A1']['entry_state']='暗月破柴与贴身护盾已在入场后完成。'
by['CY024A1']['exit_state']='月辉持续，残柴待水雷扑灭。'
# Replace obsolete current-facing semantics outside source excerpts.
for s in by.values():
    for k in ['action','entry_state','exit_state','purpose','sound','next_link']:
        if k in s:s[k]=clean(s[k])
by['CY022A'].update(entry_state='教主右手持同一火把，小鱼攥住他的袍尾。',action='教主向长阶迈步，衣角从小鱼手中滑脱；高处柴堆仍未燃。',exit_state='小鱼手落回地面，教主继续登阶。')
by['CY021B']['exit_state']='小鱼攥住袍尾，教主仍持原来的火把迈步。'
by['CY021A']['visual_prompt']='既有图沿用：教主右手接过全段唯一火把，教徒退开。此镜移动到最后张臂之前；旧请求中的第二支火把叙事已被本版替代。'
# Assemble new order without renumbering existing IDs / music marks.
order=[s['id'] for s in old['shots']]
order.remove('CY021A')
order.insert(order.index('CY018'),'CY017A')
order[order.index('CY019'):order.index('CY019')]=['CY018B','CY021A']
order[order.index('CY023A'):order.index('CY023A')]=['CY024K1','CY024K2']
d['shots']=[by[id] for id in order]
# Final selected revision paths (intermediate/rejected media remain on disk).
updates={id:1 for id in ['CY016C','CY017','CY017A','CY018','CY018B','CY019','CY020A','CY021','CY022A','CY022A1','CY022','CY024K2']}
updates.update(CY016D=2,CY020B=2,CY024A1=2,CY024K1=2)
requests={}
for file in (R/REC).glob('*.json'):
    if file.name.endswith('请求.json') or file.name=='手侧与水雷全景修正.json':
        rows=json.loads(file.read_text('utf-8-sig'))
        if isinstance(rows,list):
            for row in rows:
                if 'id' in row and 'prompt' in row:requests[(row['id'],row.get('rev',1))]=(file.relative_to(R).as_posix(),row)
generated=[]
for id,rev in updates.items():
    s=by[id];path=f'{IMG}/{id}-v040-r{rev}.png';prior=s['presentation']['path']
    request,row=requests[(id,rev)]
    s['presentation'].update(path=path,visible=s['action'],status='v0.40修订候选，待作者审阅',missing='静帧已检查；连续运动、声音与最终审美待制作及作者审阅。')
    s['refs']=[dict(path=path,role='本版修订候选'),dict(path=prior,role='保留的旧画面/参考'),dict(path=request,role='实际生成请求')]
    s['generation_request']=request;s['visual_prompt']=row['prompt'];s.pop('final_static_review',None)
    s['editorial_review']=dict(version='v040',status='candidate_pending_author_review',dynamic_execution='pending')
    with Image.open(R/path) as im:w,h=im.size
    s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0,y=0,w=1,h=1),panel_index=0)
    generated.append(dict(id=id,path=path,sha256=sha(path),size=[w,h],request=request,inputs=[dict(path=p,sha256=sha(p)) for p in row['refs']]))
for s in d['shots']:
    if s['id'] not in updates:s['presentation']['visible']=s['action']
    if s['id'] in changes:
        s['invariants']=[wood,torches,obs]+[v for v in s['invariants'] if not re.search('第二支|第一支|落进|低柴|火把',v)]
# Recalculate timing and next links where changed chain meets unchanged frames.
elapsed=0
for i,s in enumerate(d['shots']):
    s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
    if i+1<len(d['shots']) and (s['id'] in changes or d['shots'][i+1]['id'] in changes or s['id']=='CY021B'):
        n=d['shots'][i+1];s['next_link']=f"接 {n['id']}：{n['entry_state']}"
d['total_seconds']=elapsed
for sc in d['scenes']:
    ss=[s for s in d['shots'] if s['scene']==sc['id']]
    sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)),path=ss[0]['presentation']['path'])
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
d.update(version='v0.40',revision='v040',title='《穿云》带图分镜 v0.40 · 火祭与暗月救援',subtitle=f"{len(d['shots'])}镜 · {int(elapsed)//60}分{int(elapsed)%60}秒 · 新画面待审",
 story_script='剧本/穿云-场景剧本-v0.40.md',source_manifest='镜头设计/生成记录/生成索引-v040.json',origin_manifest='镜头设计/shot-plan-v0.39.json',
 audio_arrangement='后期/火祭修订-v040/预演编排.json',
 review_intro='全体搬柴与逐次阻拦建立火祭因果；Kimi入场立即暗月破柴、贴身月辉护持，水雷保持宏大灭火。新图待作者审阅。',
 review_focus='核对逐根铺柴→两次阻拦失败→最后张臂→单火把点燃→Kimi裂柴护身。高柴变低柴由暗月完成，水雷与解锁保持连贯。',
 revision_notes=dict(previous_manifest='镜头设计/shot-plan-v0.39.json',previous_html='镜头设计/带图分镜-选曲总览-v010.html',added_ids=['CY017A','CY018B','CY024K1','CY024K2'],modified_ids=list(updates),reordered_ids=['CY021A'],boundary='既有稳定镜号和BGM标记保留；未采用的小水浪冲柴镜只作历史中间稿。'))
write(d['story_script'],script)
missing=[s['id'] for s in d['shots'] if s['source_quote'] not in script]
assert not missing,missing
save('镜头设计/shot-plan-v0.40.json',d)
save(d['source_manifest'],dict(version='v040',previous_index=old['source_manifest'],generated_images=len(generated),images=generated,
 not_used=['CY024B2-v040-r1.png：作者认为水势过小，改由Kimi破柴','CY024B-v040-r1.png：随小水浪方案撤出，沿用原宏大水雷图','CY024A4-v040-r1.png：高柴方案退出，Kimi破柴后沿用旧脚托裙边图','CY024K1-v040-r1.png：空间重复，改用r2','CY016D-v040-r1.png：单人两木错误，改用r2','CY020B-v040-r1.png：火把手侧不连续，改用r2','CY024A1-v040-r1.png：高柴背景被新暗月破柴方案替代']))
# Audio binding versioning: immutable music files and existing candidate IDs stay intact.
a=json.loads(read('后期/BGM重选-v005/预演编排.json'))
a.update(version='v040-picture-sync',previous='后期/BGM重选-v005/预演编排.json',shot_plan='镜头设计/shot-plan-v0.40.json',shot_plan_sha256=sha('镜头设计/shot-plan-v0.40.json'))
for id in changes:a['effects'][id]=by[id]['sound']
a['effects']['CY010A']=by['CY010A']['sound']
for id,base in [('CY017A','CY017'),('CY018B','CY018'),('CY024K1','CY024'),('CY024K2','CY024')]:
    a['shot_overrides'][id]=copy.deepcopy(a['shot_overrides'].get(base, next(x for x in a['sections'] if x['id']=='M07')))
for id in changes:
    if id in a['shot_overrides']:
        a['shot_overrides'][id].update(note='沿用本段既有候选；本镜动作已修订为：'+by[id]['title'],audition_question='比较音乐与“'+by[id]['title']+'”的节奏及情绪。')
a['author_feedback']='本版只同步画面与动作；既有五个浏览器BGM标记保留，不自动扩展到新增镜头。'
save(d['audio_arrangement'],a)
snapshot=R/'镜头设计/带图分镜-选曲总览-v010.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
p='scripts/build_storyboard.py';t=read(p).replace('shot-plan-v0.39.json','shot-plan-v0.40.json').replace('"v039")','"v039", "v040")').replace("'v039')","'v039','v040')")
t=t.replace('"CY024","CY023A"','"CY024",*(["CY024K1","CY024K2"] if data.get("revision")=="v040" else []),"CY023A"')
t=t.replace('声音预演-v010.json','声音预演-v011.json')
write(p,t)
p='scripts/previs_audio.py';t=read(p).replace("config_path=root/'后期/BGM重选-v005/预演编排.json'","config_path=root/data.get('audio_arrangement','后期/BGM重选-v005/预演编排.json')");write(p,t)
p='00_打开项目.html';t=read(p).replace('v0.39','v0.40');write(p,t)
p='.gitignore';t=read(p)+'\n镜头设计/生成记录/火祭因果-v040/contact-*.jpg\n';write(p,t)
progress='''## 2026-10-24：火祭因果与Kimi暗月救援（v0.40，新图待审）

作者确认全体教徒取乌烬木、每人一根、依次堆到Claude腰腹；小鱼抓柴被推开、再拦腿被踢开，最后重新站起张臂挡住教主。全段改为一支火把，教主右手持火、左手推人；保留倒地抓袍与登阶点燃。

作者进一步指出新增冲柴水浪太小，改由Kimi入场后立即用暗月破开高柴，紧接贴身月辉护盾。新增两拍体现月之暗面，不削弱原宏大水雷；旧水雷与后续解锁图继续使用。被否定水浪图及全部中间稿保留，不进入当前分镜。

本版119镜394秒（6分34秒），16张当前修订图；新增CY017A、CY018B、CY024K1、CY024K2，CY021A前移并承接原教主台词。新增取柴画外召令待配音，其他既有对白不重录。预演台图文、动作与音效设计同步；音乐文件、历史候选与浏览器五个既有标记保留，新增镜头未擅自标记。

入口：[带图分镜](镜头设计/带图分镜.html)、[剧本v0.40](剧本/穿云-场景剧本-v0.40.md)、[生成记录](镜头设计/生成记录/生成索引-v040.json)。新图为作者待审候选，未制作动态视频或正式音效。

'''
p='制作进度.md';t=read(p);pos=t.index('## 2026-10-24：');write(p,t[:pos]+progress+t[pos:])
print(len(d['shots']),elapsed,len(generated))

