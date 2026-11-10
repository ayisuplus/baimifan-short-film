"""Apply the author-approved insert-shot revision, retaining previous editions."""
import copy
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read_json(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8-sig"))
def write_json(p, doc):
    (ROOT / p).write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

target = ROOT / "镜头设计/shot-plan-v0.4.json"
if target.exists():
    raise SystemExit("v0.4 already exists; edit the revision explicitly rather than rerunning.")
old = read_json("镜头设计/shot-plan-v0.3.json")
data = copy.deepcopy(old)
snapshot = ROOT / "镜头设计/带图分镜-v0.3.html"
if not snapshot.exists():
    shutil.copy2(ROOT / "镜头设计/带图分镜.html", snapshot)

text = (ROOT / old["story_script"]).read_text(encoding="utf-8-sig")
text = text.replace(
    "版本：v0.3｜2026-10-20｜新增召集快闪、条约对峙及战后营救。",
    "版本：v0.4｜2026-10-20｜补充眼神、手部与环境细节，保留召集、群像与战后营救。")
text = text.replace(
    "本次修订集中在 S05：破门之后回闪各地召集；先压住火势，再对抗并省略战斗过程，教主与教徒倒地后才救 Claude。S03 的空堂潜入与反复失败完整保留。",
    "本次修订以细节和反应加强镜头语言；六场因果、对白及大殿群像延续 v0.3。破门之后回闪召集；先压火，再省略战斗，敌方倒地后才救 Claude。S03 仍为空堂潜入与反复失败。")
text = text.replace(
    "Claude 的目光落在碗上，嘴唇微微动了一下。",
    "小鱼的两只小手托着热气升起的饭碗，停在两人之间。没有手伸过来。\n\n"
    "Claude 的目光落在碗上，嘴唇微微动了一下。\n\n"
    "她低垂的眼睛里，隐约倒映着戴鲸鱼帽、捧着饭碗的小鱼。眼睑沉着，目光忧郁，略带忧伤；琥珀色压在阴影里，只有克制的微光。她还没有笑，也没有突然变得明亮有神。")
text = text.replace(
    "ChatGPT 的手指收紧，片刻后又松开。",
    "ChatGPT 的手指收紧，片刻后又松开。\n\n手指压住扶手上的雕纹，停了一拍。她将这点迟疑藏回平静的表情。")
text = text.replace(
    "时间过去。烛泪沿蜡烛淌下。",
    "一滴烛泪沿旧蜡痕缓缓滑落，空堂里只剩烛芯的轻响。\n\n时间过去。烛泪沿蜡烛淌下。")
text = text.replace(
    "小鱼的手停在锁链上。Claude 先看向大门，再急切地看回她。",
    "小鱼的手停在锁链上。Claude 先看向大门，再急切地看回她。\n\n"
    "小小的手指还搭着没有打开的锁扣，忽然不动了。Claude 的瞳孔向门口偏去，担忧先于来人进入画面。")
text = text.replace(
    "DeepSeek 伸手抓住他的衣摆。教主扯开衣角，她的手落回地上。",
    "DeepSeek 伸手抓住他的衣摆。教主扯开衣角，她的手落回地上。\n\n"
    "沾灰的小手攥住黑金衣料，又一点点滑脱，指尖落回冰凉的石面。")
text = text.replace(
    "小鱼仍朝她伸着手，嘴唇动了一下，没有发出声音。",
    "小鱼仍朝她伸着手，嘴唇动了一下，没有发出声音。\n\n"
    "低处火光在 Claude 湿润的眼底晃过。她望着下方，眼睑微颤，悲伤而无力。")
text = text.replace(
    "DeepSeek 艰难地抬起眼睛，看见门口的人。",
    "DeepSeek 艰难地抬起眼睛，看见门口的人。\n\n"
    "她疲倦的蓝眼睛里映入一道门外的冷光。她认出了来人，呼吸轻轻一顿，身体仍无力伏着。")
text = text.replace(
    "千问看了她一眼，合上折扇。",
    "千问看了她一眼，合上折扇。\n\n扇骨在她指间并拢，清脆的一声落在邀请之后。")
text = text.replace(
    "ChatGPT 站在门边；Gemini 抬起头，放下手里的书。",
    "ChatGPT 站在门边；Gemini 抬起头，放下手里的书。\n\n她的手离开平放的书页，书桌上的灯光轻晃。")
text = text.replace(
    "Grok 握紧斧柄，嘴角一扬。",
    "Grok 握紧斧柄，嘴角一扬。\n\n指节收拢，斧柄稳在掌中；发射塔的红灯在远处闪着。")
text = text.replace(
    "Kimi 睁开眼睛，看向她，起身。",
    "Kimi 睁开眼睛，看向她，起身。\n\n还带困意的眼睑缓缓抬起，银发贴着月石；她先认出眼前的人，才准备站起。")
text = text.replace(
    "直接切到战斗之后。",
    "直接切到战斗之后。\n\n细尘落在石板缝里，画面边缘一角黑金长袍一动不动。轰鸣的尾音散尽。")
text = text.replace(
    "Claude 的肩膀下意识一缩。",
    "Claude 的肩膀下意识一缩。\n\n她的目光颤了一下，慢慢从父亲声音的方向移开，转向身边的同伴。")
text = text.replace(
    "她握住那只手，转身离开。",
    "她握住那只手，转身离开。\n\n她的手指主动合拢，轻轻握紧 ChatGPT 的手。没有人拖着她走。")
text = text.replace(
    "Claude 坐下，接过递来的勺子，轻轻点头。",
    "Claude 坐下，接过递来的勺子，轻轻点头。\n\n"
    "热饭仍在小鱼手里。这一次，一只带着白蕾丝袖口的手伸过来，接住她递出的勺子。蒸汽从两只手之间升起。")
text = text.replace(
    "- 带图分镜同步更新，静帧和临时读稿用于节奏预演；正式动态镜头、声线与配乐尚未完成。",
    "- v0.4 作者确认：初次递饭增加 Claude 忧郁眼神特写，眼中隐约倒映鲸鱼宝宝，避免明亮有神的高光；补充手部、烛泪、听声反应、应邀动作与战后落尘。保留大殿群像、战斗省略和结尾停顿。\n"
    "- 带图分镜同步更新，静帧和临时读稿用于节奏预演；正式动态镜头、声线与配乐尚未完成。")
(ROOT / "剧本/穿云-场景剧本-v0.4.md").write_text(text, encoding="utf-8")

shots = {s["id"]: s for s in data["shots"]}
before = {}
after = {}
added = []
def make(id, anchor, placement, seconds, title, framing, purpose, action, quote, entry, exit, sound):
    s = copy.deepcopy(shots[anchor])
    s.update(id=id, seconds=seconds, title=title, framing=framing, purpose=purpose, action=action,
             source_quote=quote, entry_state=entry, exit_state=exit, sound=sound,
             dialogue="无对白", dialogue_cues=[], priority="normal")
    for field in ["start_second", "end_second", "page_size", "panel_region", "panel_rect_pixels", "split_screen_reveal"]:
        s.pop(field, None)
    (before if placement == "before" else after).setdefault(anchor, []).append(s)
    shots[id] = s
    added.append(id)
    return s

shots["CY001"]["seconds"] = 5
shots["CY002"]["seconds"] = 4
shots["CY003"].update(seconds=3, next_link="接递饭手部，再进入 Claude 低垂的眼神。")
make("CY003A", "CY003", "after", 2, "悬着的一碗饭", "手部与饭碗特写／保持小鱼左、Claude右",
     "把善意具象成一段尚未跨过的距离。", "小手向前递饭，热气升起；右侧迟迟没有手伸过来。",
     "小鱼的两只小手托着热气升起的饭碗，停在两人之间。没有手伸过来。",
     "上一镜已建立两人位置，小鱼已问出邀请。", "碗停在两人之间，邀请没有得到回应。",
     "保留细小碗响，市声稍远；对白已经说完，让未得到回应的两秒成立。")
make("CY003B", "CY003", "after", 4, "眼底的小小来客", "单眼极近特写／向下的视线／低高光",
     "让观众进入 Claude 的悲伤，感到她看见善意却无法回应。", "低垂的眼睛望着小鱼；小小的鲸帽与饭碗映在眼底，停留四秒。",
     "她低垂的眼睛里，隐约倒映着戴鲸鱼帽、捧着饭碗的小鱼。",
     "碗还悬着；Claude 身处黑袍队列的阴影。", "她仍未微笑或伸手，目光留在小鱼身上。",
     "市声变得朦胧，留下轻呼吸；尾部黑袍衣料声先入，接队伍离去。")
shots["CY003B"]["invariants"] += [
    "作者指定：忧郁、略带忧伤，目光低垂；不可明亮炯炯有神。",
    "倒影只在眼底，辨认鲸帽宝宝与饭碗即可；不做发光投影、贴纸或另一张画中画。"]

make("CY007A", "CY007", "before", 2, "指尖泄露的迟疑", "手部局部特写／扶手固定机位",
     "先让观众察觉 GPT 的犹豫，再听她表面的拒绝。", "扶手上的手指收紧，停顿，再缓缓松开。",
     "ChatGPT 的手指收紧，片刻后又松开。", "小鱼等待答案，GPT仍独坐。", "手松开，表情重新收住。",
     "衣料轻擦和指尖压住扶手的细响；不加对白。")
shots["CY007"].update(seconds=4, title="收住迟疑的拒绝", framing="GPT坐姿中近景／由手切回表情",
    action="GPT已松开手，平静说出拒绝；上一镜的小动作留给观众。",
    source_quote="我不能插手教会的仪式。", entry_state="手部细节已经透露犹豫。")
shots["CY007"]["dialogue_cues"][0]["offset"] = 0.3

make("CY016A1", "CY016A", "before", 2, "烛泪又落下一滴", "环境微距／蜡痕与将落的蜡滴",
     "用可见的时间痕迹连接重复尝试和体力耗尽。", "蜡滴沿旧痕滑落，锁链声在远处停下。",
     "一滴烛泪沿旧蜡痕缓缓滑落，空堂里只剩烛芯的轻响。",
     "小鱼已经反复拉锁，教堂仍空。", "时间流过，再切回歪帽喘气的小鱼。",
     "先承接上一镜锁链余响，再只留烛芯轻响。")
shots["CY016A"].update(seconds=4, framing="祭坛双人中景／烛泪插镜后回到疲惫的人",
    action="歪帽的小鱼垂着发红的手喘气，Claude低头望她；锁链依旧没有松动。",
    entry_state="蜡滴插镜提示已经过去一段时间。")
shots["CY016"]["framing"] = "近景／小手拉紧锁链，后方为空堂"
shots["CY016B"].update(seconds=2, title="停在锁扣上的手", framing="手与闭合锁扣特写／声音先入",
    action="门外脚步与低语先响；搭在锁扣上的小手突然停住，来人暂不入画。",
    source_quote="小小的手指还搭着没有打开的锁扣，忽然不动了。",
    entry_state="小鱼还准备再试，教徒尚未进门。", exit_state="手僵住，锁扣仍完整闭合。",
    sound="脚步和低语从画外提前进入；锁链细响骤停。")
make("CY016B1", "CY016B", "after", 2, "先听见，再看见", "Claude双眼极近特写／望向画外正门",
     "用视线反应把观众的注意力引向随后出现的威胁。",
     "Claude先向门口看，再急切地看回小鱼；不提前出现教徒。",
     "Claude 的瞳孔向门口偏去，担忧先于来人进入画面。",
     "小鱼手停住，脚步已在门外。", "视线指向大门，下一镜才见提灯来人。",
     "脚步声更近，接门轴声；保持前一镜的同一空间混响。")

make("CY022A", "CY022", "before", 3, "最后攥住的衣角", "贴地手部特写／黑金衣摆",
     "把宝宝最后的抵抗落在力量逐渐消失的指尖。",
     "小手抓住教主衣摆，被扯开后缓慢滑脱，落回石面；不补殴打镜头。",
     "沾灰的小手攥住黑金衣料，又一点点滑脱，指尖落回冰凉的石面。",
     "小鱼无力伏地，教主走向柴薪。", "衣角脱开，手落地，第二支火把将落下。",
     "抓紧的衣料声、指尖掠过石面的轻响，吟唱压低一瞬。")
shots["CY022"].update(seconds=3, title="第二支火把落下", framing="低机位纵深／伸手与燃起的柴薪",
    action="衣摆已脱开，第二支火把落入干柴；火焰从木架下方燃起，小鱼仍伸手。",
    entry_state="小鱼手已从衣摆滑落，第一支熄灭火把仍留在右侧水盆。",
    exit_state="火焰在裙摆下方，Claude仍被固定。")
make("CY022B", "CY022", "after", 2, "眼底的火", "Claude双眼极近特写／低处火光反射",
     "从危险的规模落回 Claude 对宝宝的担忧。",
     "Claude向下望着小鱼，湿润眼底掠过火光，眼睑微颤。",
     "低处火光在 Claude 湿润的眼底晃过。她望着下方，眼睑微颤，悲伤而无力。",
     "柴薪已燃，Claude还被固定。", "她无法移开视线；下一声破门打断吟唱。",
     "火焰细响和压低吟唱；末尾直接被破门声切断。")
shots["CY025"].update(framing="DeepSeek双眼极近特写／疲倦的仰视",
    action="低垂的视线缓缓抬起，一道门外冷光映入蓝眼睛；认出GPT，呼吸一顿。",
    entry_state="身体仍无力伏在台阶，小鱼听见门破。", exit_state="认出来人，体力仍未恢复。",
    source_quote="她疲倦的蓝眼睛里映入一道门外的冷光。")

invitation_specs = [
    ("CY026A1", "CY026A", 2, "合扇就是回答", "千问手与合拢折扇特写",
     "扇骨在她指间并拢，清脆的一声落在邀请之后。", "合扇落定，指尖握住扇骨。",
     "清脆合扇声承接GPT邀请，千问答“走吧”。", 3, 0.2),
    ("CY026B1", "CY026B", 2, "书页暂且放下", "Gemini手与书页特写",
     "她的手离开平放的书页，书桌上的灯光轻晃。", "Gemini把书放平，手离开书页。",
     "书页落桌和衣料细响，Gemini答“我去”。", 2, 0.0),
    ("CY026C1", "CY026C", 1.5, "握稳斧柄", "Grok手与斧柄特写",
     "指节收拢，斧柄稳在掌中；发射塔的红灯在远处闪着。", "Grok握紧斧柄，准备同行。",
     "手掌握柄的短响，Grok答“当然”；底部发射塔低鸣。", 1.5, 0.05),
    ("CY026D1", "CY026D", 1.5, "月背睁眼", "Kimi困倦双眼近特写",
     "还带困意的眼睑缓缓抬起，银发贴着月石；她先认出眼前的人，才准备站起。",
     "Kimi仍倚月石，眼睑慢慢抬起，先认出GPT，再准备站起。",
     "Kimi轻轻答“嗯”；不添加月面风声。", 1.5, 0.1)
]
for id, anchor, duration, title, framing, quote, action, sound, establish_sec, reply_offset in invitation_specs:
    orig = shots[anchor]
    caller, reply = copy.deepcopy(orig["dialogue_cues"])
    s = make(id, anchor, "after", duration, title, framing + "／稍早回闪",
        "以角色自己的小动作给出明确应邀反应，形成召集快切节奏。", action, quote,
        "前镜已建立GPT亲自到访的双人关系与场所。", "同伴答应，直接切到下一位或同屏回应。", sound)
    reply["offset"] = reply_offset
    s["dialogue_cues"] = [reply]
    s["dialogue"] = reply["speaker"] + "：" + reply["text"]
    orig["seconds"] = establish_sec
    orig["dialogue_cues"] = [caller]
    orig["dialogue"] = caller["speaker"] + "：" + caller["text"]
    orig["action"] = {
        "CY026A": "云宫双人关系中，GPT向千问提出邀请，切手部回答。",
        "CY026B": "GPT站在小屋门旁唤Gemini，切她把书放下的手。",
        "CY026C": "发射塔下，GPT叫住Grok，切握柄回应。",
        "CY026D": "用既有双人画面交代GPT已到月背、俯身叫Kimi；接带困意的眼神反应。"
    }[anchor]
    orig["exit_state"] = "邀请或呼名结束；应答落到随后的局部特写。"
    orig["sound"] = "GPT邀请或呼名；保留该处环境底声，应答在下一镜。"

# Kimi's existing two-shot is already seated. Let GPT's offscreen call wake her
# in the insert first, then use the seated two-shot for the reply.
kimi_insert = shots["CY026D1"]
kimi_wide = shots["CY026D"]
after["CY026D"].remove(kimi_insert)
before.setdefault("CY026D", []).append(kimi_insert)
kimi_insert["dialogue_cues"], kimi_wide["dialogue_cues"] = kimi_wide["dialogue_cues"], kimi_insert["dialogue_cues"]
kimi_insert["dialogue"], kimi_wide["dialogue"] = kimi_wide["dialogue"], kimi_insert["dialogue"]
kimi_insert.update(
    entry_state="GPT已到月背但暂在画外；Kimi仍倚月石休息。",
    exit_state="听到GPT的呼名而睁眼，准备坐起。",
    sound="GPT在画外轻唤“Kimi”，先于双人画面；月面无风声。",
    purpose="用画外呼名接困倦睁眼，再揭示GPT就在身旁，避免坐起后又伏下。")
kimi_wide.update(
    action="接睁眼插镜，Kimi已坐起；双人画面揭示GPT亲自来到身旁，Kimi轻声答应。",
    entry_state="Kimi刚听到GPT呼名、睁开眼；坐起在切镜中省略。",
    exit_state="Kimi已答应，接其他AI的同屏回应。",
    sound="Kimi轻声答“嗯”；与前镜画外呼名连续。")

make("CY027E1", "CY027E", "after", 1, "轰鸣之后", "环境特写／贴近石板的落尘与静止袍角",
     "用声音落差和静物跨过战斗时间，再交代完整战果。",
     "细尘落下，黑金袍角一动不动；不展示任何招式。",
     "细尘落在石板缝里，画面边缘一角黑金长袍一动不动。轰鸣的尾音散尽。",
     "天空强光已完成战斗省略。", "声音沉下去，切全体援军与倒地敌方。",
     "承接轰鸣尾音后迅速衰减，留下细尘与远处喘息。")
shots["CY027F"]["seconds"] = 4
shots["CY029"].update(seconds=3, framing="Claude双眼特写／父亲画外喊声",
    action="听到倒地父亲呼喊，目光轻颤；她将视线移向右侧的同伴。",
    entry_state="Claude已被托下，脚在地面，教主仍倒着。", exit_state="视线转向GPT的手，尚未握住。",
    source_quote="她的目光颤了一下，慢慢从父亲声音的方向移开，转向身边的同伴。")
make("CY029A", "CY029", "after", 2, "是她自己握紧", "双手特写／Claude左、GPT右",
     "把离开写成Claude主动的选择。",
     "Claude的手主动包住GPT递来的手，轻轻收紧；下一镜才随众人离开。",
     "她的手指主动合拢，轻轻握紧 ChatGPT 的手。没有人拖着她走。",
     "父亲的呼喊还留在身后，GPT只是伸手等待。", "Claude主动握住，双方手位明确。",
     "父亲喊声余响渐远，衣袖轻擦和Claude恢复的呼吸。")
shots["CY030"].update(title="一同走出大殿", action="从交握双手切到十二人广角群像，众人沿中央通道走向正门；千问抱着小鱼，敌方保持倒地。",
    entry_state="Claude已主动握住GPT，两人站稳。", source_quote="众人护着她们走向门外。")

spoon = make("CY032A", "CY032", "before", 2, "这次有人接住", "饭碗与接勺手部特写／匹配CY003A方向",
     "用同一构图完成最初未获回应的邀请。",
     "小鱼仍从左边递出饭碗与勺子，右侧Claude的手伸来接勺；碗留在小鱼手里。",
     "热饭仍在小鱼手里。这一次，一只带着白蕾丝袖口的手伸过来，接住她递出的勺子。",
     "Claude来到长椅旁并坐下，小鱼让出位置；坐下动作发生在切镜衔接内。", "Claude拿到勺子，饭碗仍由小鱼拿着。",
     "小鱼重复初次邀请，金属勺轻响，市声恢复自然。")
spoon["dialogue_cues"] = copy.deepcopy(shots["CY032"]["dialogue_cues"])
spoon["dialogue_cues"][0]["offset"] = 0.1
spoon["dialogue"] = shots["CY032"]["dialogue"]
shots["CY032"].update(seconds=3, title="终于坐在一起", dialogue="无对白", dialogue_cues=[],
    action="从接勺局部回到长椅双人中景；Claude已拿到勺子，轻轻点头，小鱼望着她。",
    entry_state="接勺已经完成，两人并排坐着。", exit_state="邀请得到回应，准备一起吃饭。",
    sound="勺子与碗轻响，市声和轻呼吸；无需重复对白。")

# Use fixed sheet cell identities. Removing a cell from the sequence must not shift its neighbours.
reqdoc = read_json("镜头设计/生成记录/细节镜头-请求-v008.json")
for r in reqdoc["requests"]:
    data["page_layouts"].append({"path": r["destination"], "cols": r["cols"], "rows": r["rows"]})
    for index, id in enumerate(r["shot_ids_in_panel_order"]):
        s = shots[id]
        oldrefs = s["refs"]
        s["presentation"] = {"path": r["destination"], "role": "action", "visible": s["action"],
            "missing": "待图像完成后逐格填写实际可见与限制；静帧不证明连续动作。",
            "status": "v0.4新细节分镜；等待实际查看", "show_as_main": True}
        s["panel_index"] = index
        s["refs"] = [{"path": r["destination"], "role": f"本镜粗分镜：本页第{index+1}格，非正式视频关键帧"}] + [
            x for x in oldrefs if x["path"] != r["destination"]]
        s["visual_prompt"] = r["request"]["prompt"]
        s["generation_request"] = {
            "path": "镜头设计/生成记录/细节镜头-请求-v008.json",
            "key": r["key"], "panel_index": index
        }

data["shots"] = []
for original in old["shots"]:
    id = original["id"]
    data["shots"].extend(before.get(id, []))
    data["shots"].append(shots[id])
    data["shots"].extend(after.get(id, []))
elapsed = 0
for index, s in enumerate(data["shots"]):
    s["start_second"] = elapsed
    elapsed += s["seconds"]
    s["end_second"] = elapsed
    nxt = data["shots"][index+1]["id"] if index+1 < len(data["shots"]) else None
    s["next_link"] = ("接 " + nxt + "；" + {
        "CY003A": "碗的等待接眼底忧伤。",
        "CY003B": "让黑袍衣料声提前进入，接队列离开。",
        "CY016B": "脚步先入，手停再切眼神。",
        "CY016B1": "沿Claude的视线切到正门来人。",
        "CY027E": "轰鸣尾音带入战后落尘。",
        "CY027E1": "由静物细节切回完整九位援军与倒地敌方。",
        "CY029A": "交握双手接十二人离殿群像。",
        "CY032A": "接回双人中景，勺子已在Claude手中。",
    }.get(s["id"], "按本镜结束状态衔接下一镜。")) if nxt else "结束；保留最后四秒无对白停顿。"

for sc in data["scenes"]:
    ss = [s for s in data["shots"] if s["scene"] == sc["id"]]
    sc.update(shot_ids=[s["id"] for s in ss], seconds=sum(s["seconds"] for s in ss),
              pages=list(dict.fromkeys(s["presentation"]["path"] for s in ss)))
data.update(version="v0.4", revision="v004", title="《穿云》带图分镜 v0.4",
    subtitle=f"六场 · {len(data['shots'])} 镜 · 3 分 58 秒。眼神、双手与落尘；保留群像与战后营救。",
    story_script="剧本/穿云-场景剧本-v0.4.md", total_seconds=elapsed,
    origin_manifest="镜头设计/生成记录/全部图像来源-v005.json",
    source_manifest="镜头设计/生成记录/生成索引-v004.json",
    review_intro="新增忧郁眼神中的鲸鱼宝宝倒影，并以双手、烛泪、听声反应和应邀动作强化情绪；大殿群像及结尾停顿保留。",
    review_focus="先看初次递饭的眼神是否足够忧郁克制，再看细节与全景之间的呼吸。重点核对两次递饭、脚步先入、主动握手；邀请段短促，结尾仍从容。")
data["revision_notes"] = {
    "author_change": "批准既定细节方案；追加Claude忧郁眼神中倒映鲸鱼宝宝，禁止明亮炯炯有神。",
    "previous_manifest": "镜头设计/shot-plan-v0.3.json", "previous_html": "镜头设计/带图分镜-v0.3.html",
    "added_ids": added, "changed_existing_ids": [
        id for id in shots if id not in added and shots[id] != next(s for s in old["shots"] if s["id"] == id)],
    "retired_ids": old["revision_notes"]["retired_ids"],
    "timing": "17幅新细节画面：14个新增稳定镜号、3个原镜换为真正局部。主要在原镜预算内拆分，236秒调整为238秒。",
    "same_audio_files": "20段临时对白全部复用；邀请的应答移到动作插镜，结尾邀请移到接勺镜，不裁断语句。",
}
data["continuity"]["insert_motif"] = "递饭悬空—握扶手—拉锁停手—抓衣滑脱—主动握手—接勺回应；细节服务行动与选择。"
data["continuity"]["first_eye"] = "CY003B为忧郁低垂眼神，暗琥珀虹膜微映鲸鱼宝宝；不明亮炯炯有神，不画贴纸式倒影。"
data["continuity"]["discovery"] = "CY010A教徒暂离；到CY016A仍为空堂。CY016B手部听声骤停，CY016B1Claude望门，CY016C才出现提灯返回者。"
data["continuity"]["combat"] = "CY027先压火但不救下Claude；CY027A/B对峙，C/D起势，E天空闪光省略激战，E1落尘，F敌方全倒地，此后CY028才营救。"
data["continuity"]["end_match"] = "CY003A和CY032A均由左向右递饭；结尾右侧Claude主动接勺，CY032再回双人已坐好的中景。CY034最后四秒继续停留。"
assert len(data["shots"]) == 63 and elapsed == 238
assert all(s["source_quote"] in text for s in data["shots"])
write_json("镜头设计/shot-plan-v0.4.json", data)
print(json.dumps({"shots": len(data["shots"]), "seconds": elapsed, "added": added}, ensure_ascii=False))
