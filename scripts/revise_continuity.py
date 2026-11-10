"""Apply the full-sequence v0.5 editorial pass, preserving v0.4 and stable IDs."""
import copy
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8-sig"))
def write(p, value):
    (ROOT / p).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

target = ROOT / "镜头设计/shot-plan-v0.5.json"
if target.exists():
    raise SystemExit("v0.5 already exists; preserve the migration input.")
old = read("镜头设计/shot-plan-v0.4.json")
data = copy.deepcopy(old)
snapshot = ROOT / "镜头设计/带图分镜-v0.4.html"
if snapshot.exists():
    raise SystemExit("v0.4 snapshot already exists; inspect before proceeding.")
shutil.copy2(ROOT / "镜头设计/带图分镜.html", snapshot)
script = (ROOT / old["story_script"]).read_text(encoding="utf-8-sig")
def replace(a, b):
    global script
    assert a in script, a
    script = script.replace(a, b)

replace("版本：v0.4｜2026-10-20｜补充眼神、手部与环境细节，保留召集、群像与战后营救。",
        "版本：v0.5｜2026-10-21｜全片接续复核：补足消息、交接与落座，合并重复动作。")
replace("本次修订以细节和反应加强镜头语言；六场因果、对白及大殿群像延续 v0.3。",
        "本版重新核对全部镜头的因果、时间、空间与持物状态；删并重复反应，补足必要动作。")
replace("DeepSeek 仍举着饭碗。\n\n教堂的门缓缓合上。街市的声音随着关门声压低。",
        "DeepSeek 跟到教堂台阶下，仍举着饭碗。门口一名教徒向里交代，声音落到她耳中。\n\n"
        "**教徒（画外）：**\n今夜，为 Claude 行火祭。\n\n"
        "她抬头看向门缝。教堂的门缓缓合上，将 Claude 和那句命令一起关在里面。街市的声音随着关门声压低。")
replace("ChatGPT 的手指收紧，片刻后又松开。\n\n手指压住扶手上的雕纹，停了一拍。她将这点迟疑藏回平静的表情。",
        "ChatGPT 的手指压紧扶手上的雕纹，停了一拍。\n\n她将这点迟疑藏回平静的表情；手仍留在扶手上。")
replace("时间过去。烛泪沿蜡烛淌下。她的帽子歪了，额前的头发贴在脸上，手指已经发红；可锁链始终没有松开。",
        "再回到两人时，小鱼的帽子已经歪了，额前的头发贴在脸上，手指发红；可锁链始终没有松开。")
replace("小鱼的手停在锁链上。Claude 先看向大门，再急切地看回她。\n\n"
        "小小的手指还搭着没有打开的锁扣，忽然不动了。Claude 的瞳孔向门口偏去，担忧先于来人进入画面。",
        "小小的手指还搭着没有打开的锁扣，忽然不动了。Claude 的瞳孔向门口偏去，担忧先于来人进入画面。")
replace("一只手抓住 DeepSeek，将她从祭坛上拽下来。\n\n她摔在石阶上，翻身爬起，扑向锁链。教徒再次把她推开。",
        "最后一名教徒在队尾掩上正门，门闩落下。随着这声闷响，一只手抓住 DeepSeek，将她从祭坛上拽下来。\n\n"
        "她摔在石阶上，撑起身子，望向正走近的教主。")
replace("Claude 没有回应。DeepSeek 撑起身子，顺着声音望过去。",
        "Claude 没有回应。DeepSeek 循声抬头。")
replace("火光熄灭，短暂的黑暗里响起水汽的嘶声。",
        "火把的亮光骤退，水汽嘶声响起；四周的蜡烛仍然燃着。")
replace("吟唱重新响起，逐渐盖过木柴的爆裂声。",
        "吟唱逐渐增强，盖过木柴的爆裂声。")
replace("教主接过重新点燃的火把，走到柴薪前。\n\nDeepSeek 伸手抓住他的衣摆。教主扯开衣角，她的手落回地上。\n\n"
        "沾灰的小手攥住黑金衣料，又一点点滑脱，指尖落回冰凉的石面。",
        "另一名教徒递来第二支燃着的火把，教主伸手接过。第一支湿透的火把仍留在祭坛右侧的水盆中。\n\n"
        "教主走向柴薪。沾灰的小手攥住他的黑金衣摆，他继续迈步；衣料从指间滑脱，小鱼的手落回冰凉的石面。")
replace("她们没有停步。\n\nDeepSeek 艰难地抬起眼睛，看见门口的人。\n\n"
        "她疲倦的蓝眼睛里映入一道门外的冷光。她认出了来人，呼吸轻轻一顿，身体仍无力伏着。\n\n"
        "几位同伴先护住小鱼。Perplexity 抬起法杖，一道屏障隔开柴薪与 Claude，火焰随之被压灭。Claude 仍被固定在木架上，锁链没有松开。\n\n"
        "屏障的冷光掠过 ChatGPT 的脸，接入稍早的召集回闪。此段发生在小鱼独自营救期间；画面色调略偏冷，声音以同一段邀请串联。",
        "她们没有停步。Perplexity 边进门边举杖，屏障声立即压入，冷光越过同伴照向祭坛。\n\n"
        "一道屏障隔开柴薪与 Claude，火焰随之被压灭。Claude 仍被固定在木架上，锁链没有松开。千问赶到台阶边，蹲下将无力的小鱼抱进怀里；其他人挡住靠近的黑袍。\n\n"
        "小鱼靠在千问怀里，艰难地抬眼。她疲倦的蓝眼睛里映入一道门外的冷光。她认出了来人，呼吸轻轻一顿，身体仍无力。\n\n"
        "以小鱼的认出接入稍早的召集回闪。云宫画面上短暂出现“稍早”二字；此段发生在小鱼独自营救期间，GPT 此刻没有离开教堂。")
replace("千问看了她一眼，合上折扇。\n\n扇骨在她指间并拢，清脆的一声落在邀请之后。",
        "千问看了她一眼。扇骨在她指间并拢，清脆的一声落在邀请之后。")
replace("ChatGPT 站在门边；Gemini 抬起头，放下手里的书。\n\n她的手离开平放的书页，书桌上的灯光轻晃。",
        "ChatGPT 站在门边；Gemini 的书已经摊在桌上。她抬头迎上来人的视线，手停在书页边；回答与表情留在同一个双人画面里。")
replace("Grok 握紧斧柄，嘴角一扬。\n\n指节收拢，斧柄稳在掌中；发射塔的红灯在远处闪着。",
        "Grok 本就握着斧柄，她抬起下巴，嘴角一扬；回应落在同一个双人画面里。发射塔的红灯在远处闪着。")
replace("Kimi 睁开眼睛，看向她，起身。\n\n还带困意的眼睑缓缓抬起，银发贴着月石；她先认出眼前的人，才准备站起。",
        "还带困意的眼睑缓缓抬起，银发贴着月石。Kimi 听到呼名，先睁眼，再撑着月石坐起；视野放宽，才看见俯身等她的 ChatGPT。")
replace("鸣响与上一场教堂窗外的声音相接，作为集合信号。",
        "这就是 CY021 中映亮教堂窄窗的同一次集合信号，重复同一声短鸣，不再发第二次。")
replace("立即回到教堂。屏障仍在，火已灭；Claude 仍被锁住。",
        "信号短鸣收尾，硬切回教堂并恢复空旷的殿内回声。画面短暂标注“此刻”。屏障仍在，火已灭；Claude 仍被锁住，小鱼一直由千问抱护。")
replace("两侧错落站立，放下武器，千问仍抱着小鱼。",
        "有人站立，有人坐低或半蹲歇息，都已收住攻势；千问仍抱着小鱼。")
replace("ChatGPT 登上祭坛，托住 Claude。援手击断束具与木架的连接，解开横在身体上的锁链。\n\nClaude 坠下来，被稳稳接住。",
        "ChatGPT 登上祭坛，先托稳 Claude。Perplexity 上前解除腕部束具和腰前的锁链，直到最后一个承重点松开。\n\n"
        "Claude 的重量落进 ChatGPT 怀里，被稳稳接住。\n\n"
        "ChatGPT 把她轻轻放下。镜头随动作移到两人正面：Claude 在左，GPT 在右。双脚触地后，GPT 扶着她的上臂，等她站稳，才将另一只手掌心向上伸出，安静地等她选择。")
replace("她看见被同伴抱起的小鱼，看见身边有人正向自己伸手。\n\n她握住那只手，转身离开。\n\n"
        "她的手指主动合拢，轻轻握紧 ChatGPT 的手。没有人拖着她走。",
        "身旁的 ChatGPT 没有催促，手掌仍摊开等着她。\n\n"
        "Claude 的手指主动合拢，轻轻握紧 ChatGPT 的手。没有人拖着她走。她朝出口转身。")
replace("DeepSeek 缠着绷带，坐在街边长椅上，腿还够不到地。她抱着一碗热饭，小口地吃着。",
        "画面短暂标注“数日后”。DeepSeek 已能安稳地坐在街边长椅上，腿还够不到地，衣服已经洗净。她抱着一碗热饭，右侧留着一个空位。")
replace("DeepSeek 立刻往旁边挪，拍了拍空出来的位置，把饭碗递过去。",
        "DeepSeek 往左挪出位置，左臂稳住膝上的饭碗，右手握着勺柄望向 Claude。Claude 从画面右侧靠近，扶着长椅慢慢坐下；她的手里还没有餐具。")
replace("Claude 坐下，接过递来的勺子，轻轻点头。\n\n"
        "热饭仍在小鱼手里。这一次，一只带着白蕾丝袖口的手伸过来，接住她递出的勺子。蒸汽从两只手之间升起。",
        "Claude 轻轻点头。小鱼把勺柄递向右侧，她伸手握住勺柄，小鱼才松开。饭碗仍稳在小鱼膝上；这一次，递出去的善意有人接住。蒸汽从两只手之间升起。")
replace("有人将一杯热饮放进她手里，她接过，靠在同伴身旁。",
        "Grok 将一杯热饮放进她手里，她接过，靠在同伴身旁。")
replace("- 带图分镜同步更新，静帧和临时读稿用于节奏预演；正式动态镜头、声线与配乐尚未完成。",
        "- v0.5 全片复核：新增第二支火把交接、落脚扶稳与长椅落座三处关系镜；合并 Gemini 书页、Grok 握柄和旧结尾双人持勺三镜。初遇增加画外火祭消息；回堂补关门，援军边入场边压火，回闪与数日后有简短时间提示。所有动作只发生一次。\n"
        "- 带图分镜同步更新，静帧和临时读稿用于节奏预演；正式动态镜头、声线与配乐尚未完成。")
(ROOT / "剧本/穿云-场景剧本-v0.5.md").write_text(script, encoding="utf-8")

shots = {s["id"]: s for s in data["shots"]}
def edit(id, **values):
    shots[id].update(values)
def picture(id, visible=None, missing=None):
    if visible:
        shots[id]["presentation"]["visible"] = visible
    if missing:
        shots[id]["presentation"]["missing"] = missing
def add(id, anchor, seconds, title, framing, action, entry, exit, quote, cell, visible, missing):
    s = copy.deepcopy(shots[anchor])
    for key in ("start_second", "end_second", "panel_region", "panel_rect_pixels", "page_size", "time_caption"):
        s.pop(key, None)
    s.update(
        id=id, seconds=seconds, title=title, framing=framing,
        action=action, entry_state=entry, exit_state=exit,
        source_quote=quote, dialogue="无对白", dialogue_cues=[],
        panel_index=cell, priority="normal",
        presentation={"path":"镜头设计/图像/连续性-动作衔接-v001.png",
                      "role":"action","visible":visible,"missing":missing,
                      "status":"粗分镜候选；v0.5补足动作接续","show_as_main":True},
        refs=[
            {"path":"镜头设计/图像/连续性-动作衔接-v001.png","role":f"v0.5接续原图第{cell+1}格"},
            *[r for r in shots[anchor]["refs"] if not r["path"].startswith("镜头设计/图像/")],
        ],
    )
    shots[id]=s
    return s

durations = {
    "CY004":6,
    "CY005":4,"CY006":6,"CY008":4,"CY009":5,
    "CY010A":4,"CY013":4,"CY015":4,"CY016A":5,
    "CY017":7,"CY018":4,"CY019":4,"CY020":5,"CY021":4,"CY022A":2,"CY022":4,
    "CY023":2,"CY026B":4,"CY026C":4,"CY026D1":2,"CY026D":3,"CY026E":4,
    "CY027D":3,"CY027E1":2,"CY029":4,"CY029A":3,
}
for id, sec in durations.items():
    edit(id, seconds=sec)
edit("CY003", action="小鱼看看 Claude，再看看碗，举碗问出邀请；句尾切到悬停的饭碗。",
     sound="一句邀请完整说完；两秒等待单独落在 CY003A，不在本镜再重复。")
edit("CY004", title="门内传出的火祭消息", purpose="同时交代两人被分开，以及小鱼为什么去求助。",
     entry_state="Claude尚未回应；黑袍从眼神特写画外横过，挡住两人视线。",
     action="黑袍遮挡接到教堂门口全景，小鱼追到台阶下；门口教徒的火祭命令清楚传来。小鱼愣住，门在句尾合上。",
     exit_state="小鱼听见Claude今夜将被火祭，留在门外；碗仍在自己手里。",
     source_quote="DeepSeek 跟到教堂台阶下，仍举着饭碗。门口一名教徒向里交代，声音落到她耳中。",
     dialogue="教徒（画外）：今夜，为 Claude 行火祭。",
     dialogue_cues=[{"speaker":"教徒","text":"今夜，为 Claude 行火祭。","offset":0.4,
                     "file":"镜头设计/临时声音/CY004-对白-v005.wav","status":"temporary_readthrough"}],
     sound="近处教徒的一句交代越过台阶传到小鱼耳中；句尾合门声压住街市，下一场以急促脚步接入。")
picture("CY004", missing="原图是门尚未合拢的代表瞬间；火祭消息由画外对白补足，黑袍遮挡、追随和合门是后续动态动作。")
edit("CY005", entry_state="同日黄昏，小鱼已听见火祭命令，放下饭碗后赶到宫殿；GPT独坐。",
     exit_state="小鱼跑到座位前停下，空手抬头求助。")
edit("CY007A", source_quote="ChatGPT 的手指压紧扶手上的雕纹，停了一拍。",
     action="手指压紧扶手雕纹，停一拍；不另演一次先松后紧。",
     exit_state="手仍按在扶手上，切回她收住情绪的表情。")
edit("CY007", action="手仍留在扶手上，GPT压住迟疑，以平静表情说出拒绝。",
     entry_state="扶手上的紧握已透露犹豫；GPT仍坐着。")
edit("CY010A", entry_state="夜色已深，仪式尚未开始。小鱼躲在教堂侧墙，教徒从正门出来去侧院休息。",
     exit_state="最后一盏灯转入侧院，正门合上；小鱼确认再无人经过。")
edit("CY013", purpose="建立十字架、锁链、未燃干柴和右侧水盆，给后来救援与火把动作留依据。",
     action="从小鱼视线切祭坛正面：Claude被束具固定，脚下干柴未燃；右侧水盆同框。")
edit("CY016A", source_quote="再回到两人时，小鱼的帽子已经歪了，额前的头发贴在脸上，手指发红；可锁链始终没有松开。")
edit("CY016B1", action="Claude只将视线偏向正门并停住；顺着她的视线切返回的提灯。",
     exit_state="视线仍指着门口；不在本镜又回看小鱼。")
edit("CY017", action="队尾关门、门闩落下；教徒把小鱼从祭坛拽到石阶。她撑起身，教主走近，说完自己的话，持火者随之上前。",
     source_quote="她摔在石阶上，撑起身子，望向正走近的教主。",
     entry_state="返回者已沿中央通道逼近；队尾仍在正门处。",
     exit_state="正门已闩；教主站在祭坛前，小鱼撑地，第一名持火者向右侧柴薪走来。",
     sound="门轴与落闩声先响，接拉扯、衣料及轻摔声；随后教主对白，吟唱渐起。")
shots["CY017"]["dialogue_cues"][0]["offset"] = 3.5
picture("CY017", missing="静帧交代小鱼落在石阶与教主站位；关门、拉拽及门闩声尚属动态/声音计划，不把一帧当作整段完成。")
add("CY021A","CY022",3,"另一支火把","中景／手部交接与祭坛同框",
    "教徒从右侧将第二支燃着的火把交给左侧教主；水盆里的第一支仍熄灭。教主接牢，向柴薪迈步。",
    "小鱼伏在阶下，Claude仍被固定，柴薪未燃，第一支火把在右侧水盆。",
    "第二支火把由教主持有，他走到小鱼能触到衣摆的位置。",
    "另一名教徒递来第二支燃着的火把，教主伸手接过。第一支湿透的火把仍留在祭坛右侧的水盆中。",
    0,
    "右侧教徒手持一支燃着的火把，左侧教主张手接取；右下水盆中另一支湿火把冒汽；远处Claude仍受束，干柴未燃，左下宝宝伏地。",
    "定格于交接尚未完成的接触前；教主握牢、迈步与点火需连续动态表现。")
shots["CY021A"]["purpose"] = "让第二次点火有明确的物件来源，并保持第一支火把入水的结果。"
shots["CY021A"]["sound"] = "火苗声靠近，衣料轻擦；同一段吟唱不断，水盆残留极轻的汽声。"
shots["CY021A"]["invariants"] = [
    "第一支火把留在祭坛右侧水盆，第二支从教徒转交教主，不能把第一支瞬间复燃。",
    "此时柴薪仍未点，Claude仍受束，小鱼不能站起。",
]
edit("CY022A", source_quote="衣料从指间滑脱，小鱼的手落回冰凉的石面。",
     action="教主向前迈步，小鱼最后抓住衣摆；同一次动作中布料滑脱，小手落地。",
     entry_state="教主已接过第二支火把，走到小鱼旁；宝宝只能伸手。")
edit("CY022", source_quote="火焰沿干柴向上攀升。Claude 低头望着小鱼，眼泪落在被烟熏脏的白裙上。",
     entry_state="第二支燃着的火把在教主手中，小鱼已经抓不住衣摆；第一支仍在水盆。",
     action="教主将手中第二支火把落向干柴，火从木架下沿燃起；切内持续保留地上小鱼向Claude伸手的空间关系。")
edit("CY023", entry_state="教徒回堂时闩住的正门紧闭；祭坛已着火，吟唱继续。")
edit("CY024", purpose="看清GPT的号召力，同时让压火先于停步寒暄发生。",
     action="九位援军从GPT身后显露，边进门边分开；Perplexity立即举杖，屏障声与冷光先朝祭坛推进。",
     exit_state="援军正向祭坛推进，压火已经开始，千问奔向倒地小鱼。",
     sound="脚步不停；入镜即起法杖的屏障声，接到下一镜的火势熄灭声。")
picture("CY024", missing="现图证明十位入场者身份；跨步、举杖与祭坛方向的压火声光尚待动态表现，不安排原地摆阵停顿。")
edit("CY027", entry_state="压火随援军入场已经启动；小鱼仍在台阶，Claude尚受束。",
     action="屏障迅速压灭干柴上的火；千问蹲下抱起小鱼，其他人拦住教徒，GPT继续走向祭坛。",
     exit_state="火灭、Claude仍固定在屏障内；小鱼由千问抱护，未恢复站立能力。",
     sound="承接前镜屏障声，木柴爆裂转为熄灭余声；宝宝喘息进入下一镜。")
edit("CY025", entry_state="火已压灭，小鱼的上身由千问抱住、托稳，仍然虚弱。",
     action="只见小鱼的脸与疲倦蓝眼；她依在怀里抬眼，认出走来的GPT，呼吸轻轻一顿。",
     exit_state="她确认GPT还是来了；借这个疑问切到稍早的邀约。",
     sound="小鱼轻喘，殿内声场渐收；随后云宫风声接入，回闪开始。")
picture("CY025", missing="近脸图未包含千问的手臂，抱护状态由前镜CY027建立；不据眼神图让宝宝重新趴回地面。")
edit("CY026A", source_quote="云海环绕的宫殿，千问站在栏前，手中展开折扇。ChatGPT 从光门走来，与她相对。",
     action="回到稍早的云宫，GPT站到千问面前问出邀请；千问听完，下一镜才合扇回应。",
     entry_state="时间回到小鱼独自营救期间；GPT已到云宫，千问仍拿着展开的扇。",
     exit_state="GPT的邀请说完，千问决定回应；扇尚未合起。",
     time_caption={"text":"稍早","offset":0,"duration":2})
shots["CY026B"]["dialogue_cues"].extend(copy.deepcopy(shots["CY026B1"]["dialogue_cues"]))
shots["CY026B"]["dialogue_cues"][1]["offset"] = 2
edit("CY026B", action="同一个双人镜内，GPT呼名，Gemini从已经摊开的书上抬眼回应。",
     source_quote="ChatGPT 站在门边；Gemini 的书已经摊在桌上。",
     dialogue="ChatGPT：Gemini。　Gemini：我去。",
     entry_state="回闪继续，Gemini坐在摊开的书前，GPT站到桌旁。",
     exit_state="Gemini已答应；书仍在桌上，不再重演放书。",
     sound="呼名、短停、回应完整留在本镜；室内灯火与纸页微响，不另切书页特写。")
shots["CY026C"]["dialogue_cues"].extend(copy.deepcopy(shots["CY026C1"]["dialogue_cues"]))
shots["CY026C"]["dialogue_cues"][1]["offset"] = 1.9
edit("CY026C", source_quote="Grok 本就握着斧柄，她抬起下巴，嘴角一扬；回应落在同一个双人画面里。",
     action="GPT在发射基地叫出名字，Grok握着原本就在手中的斧柄，扬起下巴回答。",
     dialogue="ChatGPT：Grok。　Grok：当然。",
     exit_state="Grok已经答应，握持未改变，直接接寂静月背。",
     sound="火箭基地低频机械声托住两句回应；切月背时迅速收掉环境低频。")
edit("CY026D1", source_quote="还带困意的眼睑缓缓抬起，银发贴着月石。",
     action="月背的Kimi仍伏在月石边，听见GPT画外呼名，困倦的眼睛缓缓睁开。")
edit("CY026D", source_quote="Kimi 听到呼名，先睁眼，再撑着月石坐起；视野放宽，才看见俯身等她的 ChatGPT。",
     action="接坐起后的双人关系镜：GPT俯身等着，Kimi已经认出她，轻声应答；不再躺回去或重演醒来。",
     entry_state="Kimi已睁眼，坐起动作在切镜间简略省去。",
     exit_state="Kimi坐起并答应同行，接其余伙伴回应。")
shots["CY026D"]["dialogue_cues"][0]["offset"] = 0.5
edit("CY026", sound="与CY021同一集合信号短鸣的来源回放；鸣响收尾即硬切教堂回声，不新增第二次发射。",
     exit_state="回闪结束，切回刚压灭火的教堂；现实中的GPT一直在场。")
edit("CY027A", entry_state="回到此前刚压火后的此刻；Claude仍受束，小鱼在千问怀里，教主挡住通道。",
     time_caption={"text":"此刻","offset":0,"duration":1.8})
edit("CY027D", action="广角给足九位援军：八人分向两侧迎敌，千问抱紧小鱼留在祭坛附近；Claude仍在屏障内。",
     exit_state="八人迎战、千问留守，随后用夜空强光跨过战斗过程。")
edit("CY027F", entry_state="战斗已过，教主与教徒全员倒地；九位盟友清醒，姿态有站立、坐低与半蹲，千问仍抱小鱼。",
     action="广角明确倒地敌人、九位援军与抱护小鱼；GPT从敞开正门收翼归来，向仍受束的Claude走去。",
     exit_state="敌方已无力阻拦，GPT到达祭坛，Claude尚未解开。")
edit("CY028", source_quote="ChatGPT 登上祭坛，先托稳 Claude。Perplexity 上前解除腕部束具和腰前的锁链，直到最后一个承重点松开。",
     action="GPT先以双臂承住Claude，再由Perplexity解除腕部与腰前束具；最后接点松开，Claude的重量安全落进GPT怀里。",
     exit_state="Claude完全离开木架，被GPT抱稳；双脚还没有落地。")
add("CY028A","CY028",4,"落脚之后，等她选择","中全景／随放下动作移到两人正面",
    "GPT轻轻放下Claude，等双脚着地后扶稳她的上臂，再摊开另一只手掌等待；镜头重新建立Claude左、GPT右。",
    "Claude已被安全接住，尚在GPT怀中；敌方均倒地。",
    "Claude双脚触地站稳，GPT一手扶护、一手张掌；Claude尚未主动握住。",
    "双脚触地后，GPT 扶着她的上臂，等她站稳，才将另一只手掌心向上伸出，安静地等她选择。",
    1,
    "Claude在左、GPT在右，两人全身与脚下地面可见；Claude双脚着地，GPT扶着上臂并摊开另一只手。空木架留着松开的链条，柴薪熄灭，背景黑袍倒地。",
    "图为已经落脚的代表状态；从抱持到脚接地、转到两人正面的摄影机跟移须在本镜动态落实。")
shots["CY028A"]["purpose"] = "把被接住、重新站稳和自主选择接成一个清楚的过程。"
shots["CY028A"]["sound"] = "衣裙轻擦与鞋底着地声，扶稳后空出短停；教主的喊声留到下一镜再起。"
shots["CY028A"]["invariants"] = [
    "Claude在左、GPT在右，镜内跟移建立新朝向；后续眼神向右接张开的手。",
    "所有束具已经解除，空木架和松链留在后方；衣服仍有灰迹。",
    "GPT只扶护、张掌，尚未握手或拖行；小鱼仍在千问怀里，敌人不能站起。",
]
edit("CY029", entry_state="上一镜已建立Claude双脚落地、GPT在她右侧等待；教主仍倒地。",
     action="父亲喊声从画外传来，Claude眼神轻颤；句尾她将目光转向画面右侧GPT的开放手掌。",
     exit_state="她的目光已离开父亲方向，准备自己伸手；握手未开始。")
edit("CY029A", source_quote="Claude 的手指主动合拢，轻轻握紧 ChatGPT 的手。没有人拖着她走。",
     entry_state="Claude看见GPT右侧张开的掌心；她已站稳，双方尚未握住。",
     action="Claude从画面左侧主动伸手合拢，握住右侧GPT等待的手；停一拍，才切群像离开。")
edit("CY031", source_quote="DeepSeek 已能安稳地坐在街边长椅上，腿还够不到地，衣服已经洗净。",
     entry_state="数日后，伤后休养已过去；小鱼在明亮街市长椅上，饭碗重新出现。",
     action="小鱼独坐，膝上捧着热饭，身边空位清楚可见；听到脚步，她向右看。",
     exit_state="小鱼望向右侧来人，空位尚无人坐。",
     time_caption={"text":"数日后","offset":0,"duration":2})
picture("CY031", visible="干净鲸帽宝宝坐在木长椅左侧，怀里有热饭，右侧空位可见；画面没有明确绷带。",
        missing="以数日后字幕说明休养间隔；不凭画面声称有绷带，尚未展示Claude到来。")
add("CY031A","CY032A",4,"为她留出的座位","长椅双人中全景／小鱼左、Claude右",
    "Claude从右侧靠近、扶椅坐下；小鱼往左让位，左臂稳住碗，右手握勺问出同一句邀请。Claude还没有拿勺。",
    "小鱼看向右侧来人，长椅右侧仍空，碗在她膝上。",
    "Claude已坐到小鱼右边，点头接受邀请；勺仍由小鱼拿着，尚未转交。",
    "Claude 从画面右侧靠近，扶着长椅慢慢坐下；她的手里还没有餐具。",
    2,
    "小鱼在长椅左侧，碗在膝上，手握勺柄；Claude在右侧俯身扶椅落座，手中没有勺。背景沿用阳光市场。",
    "定格为落座中段；走近、让位、坐稳与点头要在动态完成，不能把本图解释成已经接勺。")
shots["CY031A"]["purpose"] = "补足重逢和空间交接，让结尾的回应发生在观众看见的相遇之后。"
shots["CY031A"]["dialogue"] = "DeepSeek：你要吃一点吗？"
shots["CY031A"]["dialogue_cues"] = copy.deepcopy(shots["CY032A"]["dialogue_cues"])
shots["CY031A"]["dialogue_cues"][0]["offset"] = 1
shots["CY031A"]["sound"] = "脚步停在长椅旁、木椅轻响；同一句邀请在她落座时响起，句尾留给Claude点头。"
shots["CY031A"]["invariants"] = [
    "小鱼左、Claude右，不改递物方向；只有一碗饭、一把勺。",
    "碗由小鱼左臂与膝盖稳住，右手拿勺；Claude落座时不提前持勺。",
    "数日后的清洁服装延续现有结尾图，不添加不存在的绷带。",
]
edit("CY032A", dialogue="无对白", dialogue_cues=[],
     source_quote="小鱼把勺柄递向右侧，她伸手握住勺柄，小鱼才松开。饭碗仍稳在小鱼膝上；这一次，递出去的善意有人接住。",
     entry_state="两人已经同坐长椅，小鱼说完邀请，Claude已点头；勺仍在小鱼手里。",
     action="小鱼向右递勺柄，Claude握住柄后宝宝松手；接点清楚，饭碗不离开宝宝膝上。",
     exit_state="Claude独自持勺，小鱼双手重新稳住饭碗。",
     sound="邀请已在上一镜完整说完；这里只留勺柄轻触与市声，让接受这一动作落地。")
edit("CY033", source_quote="Grok 将一杯热饮放进她手里，她接过，靠在同伴身旁。",
     entry_state="Claude已接过勺，长椅二人仍在同一街市；切到不远处旁观的GPT与Grok。")

retired = [
    {"id":"CY026B1","merged_into":"CY026B","reason":"书本已在桌上，反应和应答并入双人镜，避免重复放书。"},
    {"id":"CY026C1","merged_into":"CY026C","reason":"握柄动作重复；同一双人镜保留扬头回应和基地环境。"},
    {"id":"CY032","merged_into":["CY031A","CY032A","CY034"],"reason":"落座移到新关系镜，接勺由细节完成，第一口饭留末镜；删除重复已坐好持勺。"},
]
order = [
    "CY001","CY002","CY003","CY003A","CY003B","CY004",
    "CY005","CY006","CY007A","CY007","CY008","CY009","CY010",
    "CY010A","CY011","CY012","CY013","CY015","CY015A","CY016","CY016A1","CY016A","CY016B","CY016B1","CY016C",
    "CY017","CY018","CY019","CY020","CY021","CY021A","CY022A","CY022","CY022B",
    "CY023","CY024","CY027","CY025","CY026A","CY026A1","CY026B","CY026C","CY026D1","CY026D","CY026E","CY026",
    "CY027A","CY027B","CY027C","CY027D","CY027E","CY027E1","CY027F","CY028","CY028A","CY029","CY029A","CY030",
    "CY031","CY031A","CY032A","CY033","CY034",
]

# Every cut has an explicit editorial reason; no generic "continue next shot" text.
cuts = [
    ("CY001","以宝宝停步接被黑袍包围的Claude，先建立看与被看的关系。"),
    ("CY002","顺Claude向下的视线切宝宝眼高的过肩镜，保持小鱼左、Claude右。"),
    ("CY003","邀请一句说完，切仍悬着的饭碗；等待由下一镜承担。"),
    ("CY003A","从没人接的碗切到接收者的眼睛，倒影保留同一个宝宝与饭碗。"),
    ("CY003B","黑袍衣料声先进入，遮挡视线接门口远景；Claude始终未接饭。"),
    ("CY004","火祭消息与关门完成动机，同日黄昏省去赶路，接空手冲入宫殿。"),
    ("CY005","小鱼跑停后切近景，脚步变成喘息；GPT仍在座位上。"),
    ("CY006","求助句尾留出等待，切扶手上的手，先泄露迟疑。"),
    ("CY007A","同一坐姿由手切脸；手不先松后再紧，平静的拒绝压住迟疑。"),
    ("CY007","拒绝句完整结束再切宝宝反应，不插另一处动作。"),
    ("CY008","视线低落接擦脸和决定离开，情绪从请求变为行动。"),
    ("CY009","让脚步真正离开殿门，再切只剩GPT的空殿；不提前揭示邀约。"),
    ("CY010","钟声尾音接教堂夜外；仍只跟随小鱼，GPT的后续暂时藏住。"),
    ("CY010A","最后一盏灯走远后才开始钻洞；保持同一侧墙方向。"),
    ("CY011","宝宝与帽一起穿洞，切洞口内侧落地；不从别的入口出现。"),
    ("CY012","沿宝宝望向祭坛的视线切Claude，确认整座教堂暂时无人。"),
    ("CY013","给出束缚与干柴后，省去部分步行，接宝宝沿左侧台阶抵达。"),
    ("CY015","指洞口的保证结束，注意力落到她即将碰到的腰前锁扣。"),
    ("CY015A","同一只闭锁仍打不开，手从掰扣改握链条；没有先解开再锁回。"),
    ("CY016","拉链回声持续到蜡滴，利用环境插镜跨过一段重复失败时间。"),
    ("CY016A1","同一烛光下回到疲惫二人；以帽子歪斜而非第二次解释说明耗时。"),
    ("CY016A","宝宝缓一口气、准备再试，切锁扣上的手；门外脚步这才开始。"),
    ("CY016B","手停与锁链声断开，接Claude朝正门看的眼睛；来人仍未入画。"),
    ("CY016B1","沿持续望门的视线切大门，脚步逐渐变清楚，返回者首次出现。"),
    ("CY016C","来人沿中央通道逼近；下一镜队尾关门声与抓住宝宝衔接。"),
    ("CY017","落闩、拽下、教主宣告后，接右侧持火者；宝宝仍能挣扎起身阻止。"),
    ("CY018","第一支入水熄灭，宝宝借瞬间转身跑回Claude前方，空间不跳到门口。"),
    ("CY019","黑袍逼近时留在Claude反应上，冲撞声交代画外发生的伤害。"),
    ("CY020","她向下的目光接倒在石阶的宝宝；伤势是刚才画外冲突的结果。"),
    ("CY021","集合信号只留窗闪和短鸣，不揭来源；宝宝倒地状态接教主取第二支火把。"),
    ("CY021A","第二支由教主持有后才向前走，切宝宝够得到的衣摆；第一支留水盆。"),
    ("CY022A","衣摆从同一次抓握中滑脱，接教主手中火把落柴；宝宝不再重新抓一次。"),
    ("CY022","柴薪已燃后切Claude眼中火光，空间方向仍指向下方宝宝。"),
    ("CY022B","忧伤眼神与吟唱被破门声突然截断，危险随声音转折。"),
    ("CY023","门被踢开接更宽的入口群像，抬脚落地与援军前进连续。"),
    ("CY024","援军一边入场一边起屏障，下一镜立即确认火灭；不先停下来对看。"),
    ("CY027","确认屏障护住Claude、千问抱住宝宝，才切宝宝近脸认出GPT。"),
    ("CY025","认出来人的眼神提出她为何出现的疑问，以『稍早』进入答案。"),
    ("CY026A","邀请说完才切合扇回应，扇的开到合只发生一次。"),
    ("CY026A1","合扇声作节拍，切小屋双人镜；继续同一段稍早邀约。"),
    ("CY026B","Gemini的应答在双人镜结束后才切基地，不再重复书页动作。"),
    ("CY026C","Grok扬头回应后收掉基地低频，切月背静眼和GPT轻声呼名。"),
    ("CY026D1","先醒眼，切更宽的已坐起双人图；允许省去撑起的中间动作，不倒退躺回。"),
    ("CY026D","Kimi应答结束，切其余五位累积回应；GPT的召集声继续。"),
    ("CY026E","五位反应都露出后，切信号来源；保留最后全分屏的短停。"),
    ("CY026","同一集合鸣响收尾，硬切『此刻』及教堂回声；不是又一次发令。"),
    ("CY027A","教主整句说完，按对视轴线切GPT近脸，Claude依然在屏障内受束。"),
    ("CY027B","『聒噪』句尾翼根展开，借动作方向省略掠过正门的路程，切完整屋顶上方。"),
    ("CY027C","空中二人对峙起势，切殿内九位伙伴各自迎敌，两处战斗同时开始。"),
    ("CY027D","八人迎上、千问留守后即切夜空强光，不逐招追拍。"),
    ("CY027E","强光与轰鸣跨过交锋过程，落到黑袍静止和石缝尘埃。"),
    ("CY027E1","轰鸣尾声沉下去，拉回广角交代双方结果；特写不替代战后全貌。"),
    ("CY027F","先确认敌方全倒地，GPT才上祭坛解救；千问继续抱宝宝。"),
    ("CY028","Claude完全离架并被抱稳后，才接放下、脚触地、扶稳的关系镜。"),
    ("CY028A","新朝向和张开的手建立后，父亲喊声触发眼神反应；尚未先握手。"),
    ("CY029","父亲喊完、Claude转向右侧掌心，再切她从左侧主动握住的动作。"),
    ("CY029A","握紧停一拍再切十二人离殿；宝宝仍由千问抱，敌人仍倒地。"),
    ("CY030","门外月光淡出，街市声重新进入；『数日后』明确换日和休养间隔。"),
    ("CY031","宝宝向右看后，切白裙来人与长椅同框；先把空位变成有人来坐。"),
    ("CY031A","邀请与点头结束、两人坐稳，才切从左到右递出的勺柄。"),
    ("CY032A","Claude已经持勺，转旁观者GPT接饮；两次接物形成轻柔呼应，不重演落座。"),
    ("CY033","GPT放松的目光回到长椅，Claude开始第一口饭；不是突然换一处街市。"),
    ("CY034","第一口饭之后保留最后四秒无对白停顿，再淡出结束。"),
]
assert [x[0] for x in cuts] == order
data["shots"] = [shots[id] for id in order]
picture("CY007A", missing="定格为手指压紧扶手；只保留同一次紧握，不再追加松开又按紧。停顿由动态落实。")
picture("CY007", missing="手仍留在扶手上，与前镜连续；本镜承担拒绝时的表情和对白，不补重复松手。")
picture("CY016B1", missing="眼睛望向门口的关键瞬间可见；听见脚步后转向门口的运动仍待动态，不追加回看宝宝。")
picture("CY026B", missing="双人图中书已在桌上；只需抬眼、应答与轻微表情，不补放书或起身的重复插镜。")
picture("CY026C", missing="双人图中Grok已经握斧；只需扬头回应，不另演重新握紧的特写。")
shots["CY027D"]["presentation"]["visible"] = shots["CY027D"]["presentation"]["visible"].replace("双臂抱着小鱼、双脚离地", "双臂抱着小鱼，小鱼双脚离地")
for s in data["shots"]:
    s["invariants"] = [
        x.replace("后续另接重新点燃的火把", "CY021A另接第二支燃着的火把")
         .replace("当前时空先压火；Claude全程仍被固定，等教主和教徒全部倒地后才解除束具。",
                  "当前时空入场即压火；CY028之前Claude始终受束，敌人全倒地后才解救，CY028A落脚后才握手离开。")
         .replace("小鱼干净绷带、短腿悬空", "小鱼衣服洗净、短腿悬空")
        for x in s["invariants"]
    ]
clock = 0
edges = []
for i, (s, (_, note)) in enumerate(zip(data["shots"], cuts)):
    s["start_second"] = clock
    clock += s["seconds"]
    s["end_second"] = clock
    next_id = order[i+1] if i+1 < len(order) else None
    s["next_link"] = (f"接 {next_id}：{note}" if next_id else note)
    s["visual_prompt"] = (
        f"《穿云》{s['id']}，{s['framing']}。延续当前人物母本、服装与哥特式异世界画风。\n"
        f"开始：{s['entry_state']}\n动作：{s['action']}\n结束：{s['exit_state']}\n"
        f"连续性：{'；'.join(s['invariants'])}\n下一镜：{s['next_link']}\n"
        "图像内不写提示词、镜号或说明；对白与时间提示由剪辑层添加。本段为后续制作计划，实际生图输入另行冻结。"
    )
    s["editorial_review"] = {"version":"v005","status":"reviewed","dynamic_execution":"pending"}
    if next_id:
        edges.append({"from":s["id"],"to":next_id,"decision":note,"status":"reviewed; static plan, dynamic execution pending"})
    assert s["source_quote"] in script, (s["id"], s["source_quote"])
for scene in data["scenes"]:
    ss = [s for s in data["shots"] if s["scene"] == scene["id"]]
    scene["shot_ids"] = [s["id"] for s in ss]
    scene["seconds"] = sum(s["seconds"] for s in ss)
    scene["pages"] = list(dict.fromkeys(s["presentation"]["path"] for s in ss))
paths = {s["presentation"]["path"] for s in data["shots"]}
data["page_layouts"] = [p for p in data["page_layouts"] if p["path"] in paths]
data["page_layouts"].append({"path":"镜头设计/图像/连续性-动作衔接-v001.png","cols":1,"rows":3})
data.update(
    version="v0.5", revision="v005", created="2026-10-21",
    title="《穿云》带图分镜 v0.5",
    subtitle=f"六场 · {len(order)} 镜 · 3 分 57 秒。补足接续，删并重复，让救援与选择连贯发生。",
    story_script="剧本/穿云-场景剧本-v0.5.md",total_seconds=clock,
    source_manifest="镜头设计/生成记录/生成索引-v005.json",
    origin_manifest="镜头设计/生成记录/全部图像来源-v006.json",
    review_intro="全片重新梳理：补火把交接、落脚扶稳与长椅落座；合并三处重复反应。初遇的忧郁眼神、九位援军与战后群像保留。",
    review_focus="从头播放，留意火祭消息如何引出求助、关门与破门、两支火把、入场同时压火、稍早与此刻的切换，以及脚触地后主动握手、先落座后接勺。",
)
data["continuity"].update(
    signal="CY021窗闪与CY026发射是同一次信号。入场即压火，CY027确认灭火、抱护后才到CY025认出，再以『稍早』回闪邀约；CY027A『此刻』回教堂。",
    invitation="GPT亲访四地；千问双人镜接合扇；Gemini与Grok在各自双人镜内完整回应；Kimi先醒眼再坐起应答。邀请回闪内不再重复放书或握柄。",
    restraints="空堂尝试至CY027F战后结果，Claude始终受束。CY028先托稳再完全解除、抱住；CY028A双脚落地后才到父亲喊声及主动握手。",
    end_match="CY031空座→CY031A从右到来、让位、落座及邀请→CY032A从左向右交勺→CY034吃饭。只一只碗、一把勺；末镜最后四秒静留。",
    doors="CY010A教徒去侧院休息并带上门，宝宝钻左侧洞；CY016C回堂推门，CY017队尾关门落闩；CY023才踹开。之后正门保持开放，空战不穿屋顶。",
    torches="CY018第一支入右侧水盆；CY021A教徒把另一支燃着的火把交给教主；CY022落柴点火。第一支一直浸在水盆，不复燃。",
    knowledge="CY004教徒画外火祭命令提供消息与姓名；CY006求助来自亲耳听见，不凭空得知。",
    rescue_sides="CY028接下后，CY028A跟随放下动作到二人正面，建立Claude左/GPT右；CY029目光向右，CY029A由左握右，CY030用离殿全景重新交代整体方向。",
)
data["revision_notes"] = {
    "author_change":"增加镜头后重新审查全部前后逻辑，允许修改、增补和删并。",
    "previous_manifest":"镜头设计/shot-plan-v0.4.json",
    "previous_html":"镜头设计/带图分镜-v0.4.html",
    "added_ids":["CY021A","CY028A","CY031A"],
    "retired_ids":old["revision_notes"]["retired_ids"] + retired,
    "order_change":"CY027压火与抱护提前到CY025认出之前；入场镜即开始压火。",
    "reviewed_shots":len(order),"reviewed_cuts":len(edges),
    "timing":f"原238秒重新分配为{clock}秒；为关键交接留时，压缩重复等待，末镜9秒及离殿6秒保留。",
    "audio":"原20段读稿保留，三段应答/邀请随剪辑迁移；新增一段火祭消息。句子不跨切点裁断。",
    "boundary":"全片静帧、计划动作和62处切点已复核；不能据此宣称连续动态、音效或声音表演已经验收。",
}
write("镜头设计/shot-plan-v0.5.json", data)
write("镜头设计/生成记录/全片接续复核-v005.json",{
    "manifest":"镜头设计/shot-plan-v0.5.json","reviewed_shots":len(order),
    "reviewed_cuts":len(edges),"cuts":edges,"retired":retired,
    "independent_review":"asset_review reviewed full v0.4 sequence and agreed on the three additions and three mergers.",
    "not_proven":"Dynamic action execution, actual SFX and audio performance."
})
print(json.dumps({"shots":len(order),"seconds":clock,"scenes":{s["id"]:s["seconds"] for s in data["scenes"]}},ensure_ascii=False))
