"""Create the v0.10 palace-paladin revision from the preserved v0.9 baseline."""
import json,copy,shutil,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def read(p): return json.loads((root/p).read_text(encoding="utf-8"))
def write(p,d):
    q=root/p;q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def snapshot(src,dst):
    if not (root/dst).exists(): shutil.copy2(root/src,root/dst)
snapshot("镜头设计/带图分镜.html","镜头设计/带图分镜-v0.9.html")
snapshot("资产/assets.json","资产/assets-before-paladins-v010.json")
snapshot("资产/资产图册.html","资产/资产图册-before-paladins-v010.html")
script=(root/"剧本/穿云-场景剧本-v0.9.md").read_text(encoding="utf-8")
script=script.replace("版本：v0.9","版本：v0.10")
script=script.replace("人物：DeepSeek、ChatGPT。宫殿内没有其他 AI 娘。","人物：DeepSeek、ChatGPT、宫门圣骑士。王座厅内没有其他 AI 娘；圣骑士守在外门。")
block="""两名白银盔甲、淡紫披风的圣骑士守在宫门，封闭头盔不露面容，各持一柄长枪。小鱼跑到长阶顶端，两柄枪交叉挡住去路。她急切地抬头。

殿内传来 ChatGPT 的声音。

**ChatGPT（画外）：**
让她进来。

圣骑士收起交叉的枪，将枪身竖直，退守门两侧。宫门向内打开，DeepSeek 从让出的通道跑进去。

"""
script=script.replace("沉重的大门被推开。DeepSeek 气喘吁吁地跑进来，已经顾不上带饭碗。",block+"DeepSeek 气喘吁吁地跑进来，已经顾不上带饭碗。")
old="她转过身，小小的脚步声穿过整座大殿，最后消失在门外。"
departure="她转过身，走向长殿尽头的出口，脚步声越来越远；她还没有走出宫门。"
script=script.replace(old,departure)
wide="ChatGPT 松开扶手，站到王座前。侧面超级大远景里，她立在近处，长殿的列柱与地砖线延伸向遥远出口；DeepSeek 已是尽头一个小小的蓝色背影。她目送小鱼越过门口，门外圣骑士不再阻拦。"
script=script.replace("切入黑暗，不提前展示她接下来的行动。",wide+"\n\n切入夜色，暂不展示她如何召集同伴。")
door="火光掠过空旷的中央通道，尽头正门已经关紧。冷光从门缝漏入，门板忽然一震。"
script=script.replace(door+"\n\n","",1)
script=script.replace("人物：ChatGPT、众 AI 娘、DeepSeek、Claude、教主、黑袍教徒。","人物：ChatGPT、众 AI 娘、白银圣骑士、DeepSeek、Claude、教主、黑袍教徒。",1)
assembly="与此同时，教堂外的夜色中，ChatGPT 与各路 AI 同伴已经到达。白银淡紫圣骑士手持长枪，在她们后方列成两列，面向紧闭的正门集结。镜头从队伍背后掠过，只交代剪影与规模；此刻穹顶完整，尚未下雨。"
script=script.replace("砰——！",assembly+"\n\n"+door+"\n\n砰——！",1)
entry="AI 先遣队越过门口后，圣骑士从她们身后鱼贯冲入。领头者沿柱廊转入两侧通道，后续队伍跨过门槛，中央主通道留给 ChatGPT。入口守军留下接应，不让全队挤到祭坛。"
script=script.replace("由援军群像接入稍早的召集回闪。",entry+"\n\n由骑士跟进接入稍早的召集回闪。",1)
script=script.replace("银白水光越过中殿穹顶，向中央聚拢。","银白水光越过中殿穹顶，向中央聚拢。骑士已经退入两侧厚石柱之后，以白银护光挡住侧向水浪，中央落水区保持净空。",1)
script=script.replace("教堂内，各路 AI 娘迎向涌来的教徒。","教堂内，各路 AI 娘迎向涌来的教徒。圣骑士在两翼柱廊用长枪压住黑袍，保持救援通道畅通。",1)
script=script.replace("战斗结束，雨渐停。ChatGPT 已恢复人形","圣骑士收住攻势，分守敞开的正门与两翼，照看倒地的教徒。\n\n战斗结束，雨渐停。ChatGPT 已恢复人形",1)
script=script.replace("教主留在地上，声音被留在空荡的教堂里。","教主留在地上，声音被留在空荡的教堂里。圣骑士留下控制教堂和守住两侧出口，不混入十二位核心角色的离殿队形。",1)
script=script.replace("宫殿内只有 ChatGPT；","王座厅只有 ChatGPT，外门由圣骑士守卫；")
script+="\n- v0.10：补圣骑士拦路与GPT画外放行；手部犹豫后起身，接侧面超级远景目送小鱼。旧CY026改教堂门前集结，正面群像后补CY023A骑士入场。两翼避让天瀑、迎敌与战后警戒贯通；邀约仍是稍早回闪。鲸帽卡住、仰视腾空、雷雨省略与公主抱保持。\n"
(root/"剧本/穿云-场景剧本-v0.10.md").write_text(script,encoding="utf-8")

d=read("镜头设计/shot-plan-v0.9.json")
ss={s["id"]:s for s in d["shots"]}
d.update(version="v0.10",revision="v010",created="2026-10-22",story_script="剧本/穿云-场景剧本-v0.10.md",origin_manifest="镜头设计/shot-plan-v0.9.json")
d["subtitle"]="宫门圣骑士、离殿超远景与教堂集结入场"
d["review_intro"]="本版补宫门拦路与画外放行、GPT起身目送的侧面超大远景、教堂外集结与骑士鱼贯入场。原有营救、雷雨省略和公主抱保留。"
d["review_focus"]="看宫门放行到求助是否顺畅，起身目送是否有足够空间距离，集结与入场是否有层次，骑士是否始终避开天瀑中央落点。"
d["roughcut_preview_label"]="旧版静帧配乐 v002（69镜239秒，尚未包含v0.10新画面与重排）"
d["revision_notes"].update(previous_manifest="镜头设计/shot-plan-v0.9.json",previous_html="镜头设计/带图分镜-v0.9.html",added_ids=["CY004C","CY004D","CY009A","CY023A"],repurposed_ids=[{"id":"CY026","old":"穿云箭集合信号，v0.9撤下","new":"当前时刻教堂门前集结，v0.10恢复镜号并换用途"}],boundary="新增及修订图片为独立imagegen候选；21段既有临时读稿沿用。让她进来仅字幕，正式配音待补；旧配乐粗剪未重导。")
d["revision_notes"]["retired_ids"]=[x for x in d["revision_notes"]["retired_ids"] if x!="CY026"]
d["revision_notes"]["retirement_reason"]="CY015A试扣并入CY016；旧发箭与窗闪仍撤下，CY026本版复用为门前集结。"
d["continuity"]["palace"]="外门两名白银淡紫封盔长枪圣骑士：拦路→GPT画外放行→让道→小鱼入殿。主厅对话只有两人；转身→手部犹豫→GPT站在王座前→侧面超远景目送。"
d["continuity"]["paladins"]="骑士在门外集结；GPT和AI先遣队破门进入后，骑士鱼贯沿柱廊分往两翼，留空天瀑落点；柱体与白银护光遮挡侧浪。迎敌守侧翼，战后控制门口和教徒。核心十二人离殿时，骑士留守。"
d["continuity"]["invitation"]+=" CY026为当前门前集结，不属于回闪；CY026A—E仍为稍早亲访。没有再次发箭召集。"
d["continuity"]["audio"]="新增GPT画外‘让她进来’已有字幕时点，尚无声音文件；不拿旧拒绝台词冒充。其余21段临时读稿沿用，配乐粗剪待重导。"
ss["CY004B"]["exit_state"]="小鱼跑到宫殿长阶顶端，来到守卫面前。"
ss["CY004B"]["asset_ids"]=["CHAR-DEEPSEEK","ENV-PALACE"]
ss["CY005"]["entry_state"]="宫门守卫已依照GPT画外命令让路，小鱼空手跨过门槛；GPT独坐王座。"
ss["CY005"]["purpose"]="从放行接入求助，建立王座与宝宝的距离。"
ss["CY005"]["invariants"]=["本镜王座厅只有小鱼与GPT；守卫留在镜头后方的外门。小鱼不携饭碗。"]
ss["CY007"]["entry_state"]="GPT听完求助，仍坐在王座上。"
ss["CY007"]["framing"]="GPT坐姿中近景"
ss["CY009"]["exit_state"]="小鱼仍在长殿内走向远处出口，钟声传来。"
ss["CY009"]["source_quote"]=departure
ss["CY010"]["entry_state"]="小鱼仍在远端长殿内，GPT独坐，远处钟声传来。"
ss["CY010"]["exit_state"]="GPT手指慢慢松开，接下一镜起身站到王座前。"
ss["CY022B"]["exit_state"]="Claude仍望着小鱼；切门外已经集结的援军。"
ss["CY022C"]["scene"]="S05";ss["CY022C"]["scene_title"]="召集、对抗与营救"
ss["CY022C"]["entry_state"]="门外援军已到，门内柴火仍燃，吟唱仍在。"
ss["CY024"]["exit_state"]="GPT与同伴越过门口向祭坛前行，后续骑士尚在门槛外。"
ss["CY024"]["sound"]="主角脚步后，长枪与甲片声由门外接近。"
new_info=[
("CY004C","S02","长枪拦路",3,"宫门前低机位中远景","小鱼刚跑到长阶顶端。","两名封闭头盔圣骑士交叉长枪，小鱼急停，空手抬头望向守卫。","小鱼被拦在门前，等待回应。","小鱼跑到长阶顶端，两柄枪交叉挡住去路。她急切地抬头。",["CHAR-DEEPSEEK","CHAR-PALADIN","ENV-PALACE"]),
("CY004D","S02","让她进来",3,"同轴略靠近宫门／画外声","两柄长枪仍交叉挡住小鱼。","GPT从殿内发声放行，骑士收枪竖直、让开通道；小鱼空手跨过门槛。","小鱼获准入殿，骑士留守外门。","圣骑士收起交叉的枪，将枪身竖直，退守门两侧。宫门向内打开，DeepSeek 从让出的通道跑进去。",["CHAR-DEEPSEEK","CHAR-GPT","CHAR-PALADIN","ENV-PALACE"]),
("CY009A","S02","长殿尽头的蓝点",6,"侧面超级大远景／近处GPT到远端蓝点的视线引导","GPT松开扶手，小鱼仍在出口附近。","GPT已起身站在近处王座前；长殿线条通向遥远的蓝色小鱼背影。视线由GPT缓缓移向出口，小鱼离去。","小鱼越过宫门，GPT仍站着目送；切夜晚教堂侧墙。",wide,["CHAR-GPT","CHAR-DEEPSEEK","ENV-PALACE"]),
("CY026","S05","教堂门前集结",3,"背侧低位大远景／当前时刻","祭坛柴火已燃，援军已来到紧闭教堂门外。","GPT与AI同伴在前，白银圣骑士持枪在后方两列集结，中央通道留空。","援军已到门前，正门仍闭，尚未天瀑。",assembly,["CHAR-GPT","CHAR-PALADIN","ENV-CHURCH"]),
("CY023A","S05","圣骑士鱼贯而入",3,"门内侧向低角度／队伍纵深","GPT和AI先遣队已经进入殿内，正门敞开。","圣骑士紧随先遣队跨过门槛，沿两侧柱廊冲入；后续队伍不断跟进，中央留空。","骑士已分守两翼；由甲片声切入稍早召集回闪。",entry,["CHAR-PALADIN","ENV-CHURCH"])
]
for sid,scene,title,seconds,framing,ent,action,ex,quote,assets in new_info:
    s=copy.deepcopy(ss["CY004B"])
    s.update(id=sid,scene=scene,scene_title=next(x["title"] for x in d["scenes"] if x["id"]==scene),title=title,seconds=seconds,framing=framing,purpose=title+"，补足动作与因果。",entry_state=ent,action=action,exit_state=ex,source_quote=quote,asset_ids=assets,dialogue="无对白",dialogue_cues=[],sound="脚步、甲片与环境声为制作提示，尚未制作音轨。",invariants=["骑士封闭头盔不露面，白银淡紫配色，持长枪。","场景时间与门的开合遵循前后镜；不重复召集和破门。"])
    if sid=="CY009A":
        s["invariants"]=["GPT已站起；小鱼在遥远出口，仍是蓝鲸母本造型。","王座高台只在近端，长殿地面同层；圣骑士守门，超远处不强调人物细节。"]
        s["sound"]="远去的脚步、钟声尾音，最后接教堂夜风。"
    ss[sid]=s
ss["CY004D"]["dialogue"]="ChatGPT（画外）：让她进来。"
ss["CY004D"]["subtitle_cues"]=[{"speaker":"ChatGPT（画外）","text":"让她进来。","offset":0,"duration":2.4}]
ss["CY004D"]["sound"]="GPT画外‘让她进来’；本版只有字幕，配音待补。收枪与甲片轻响待制作。"
ss["CY023A"]["time_transition"]="本镜结束切入稍早亲访回闪；骑士入场属于当前时间。"
ids=[s["id"] for s in d["shots"]]
ids.insert(ids.index("CY005"),"CY004C");ids.insert(ids.index("CY005"),"CY004D")
ids.insert(ids.index("CY010")+1,"CY009A")
ids.insert(ids.index("CY022C"),"CY026")
ids.insert(ids.index("CY024")+1,"CY023A")
d["shots"]=[ss[x] for x in ids]
for sid in ["CY024A","CY024B","CY027"]:
    ss[sid]["invariants"].append("骑士已进入两侧厚石柱后，护光挡侧浪；中央天瀑落点没有己方骑士。")
ss["CY027D"]["action"]="同伴在前景迎敌，千问抱着小鱼；白银圣骑士在两侧柱廊持长枪压住黑袍，Claude仍受缚。"
ss["CY027D"]["exit_state"]="两翼迎敌，中央救援通道保留；切教堂外爆闪省略交战。"
ss["CY027F"]["action"]+=" 圣骑士收住长枪，分守门口与两翼。"
ss["CY027F"]["exit_state"]="GPT人形落地，同伴走向祭坛；骑士留守出口和倒地教徒。"
ss["CY030"]["exit_state"]+=" 圣骑士留在教堂控制两翼与出入口，不随核心十二人加入街市结尾。"
for sid in ["CY027D","CY027F"]: ss[sid]["asset_ids"].append("CHAR-PALADIN")
paths={r["id"]:r["destination"] for r in read("镜头设计/生成记录/王宫骑士-v010/结果映射.json")}
paths["CY027D"]="镜头设计/图像/王宫骑士-v010/CY027D-v010-r3.png"
paths["CY023A"]="镜头设计/图像/王宫骑士-v010/CY023A-v010-r2.png"
for sid in ["CY004C","CY004D","CY009A","CY026","CY023A","CY027D","CY027F"]:
    s=ss[sid]; oldpath=s["presentation"]["path"]
    request="镜头设计/生成记录/王宫骑士-v010/"+sid+("-请求-v003.json" if sid=="CY027D" else "-请求-v002.json" if sid=="CY023A" else "-请求-v001.json")
    job=read(request)
    s["presentation"]={"path":paths[sid],"role":"action","visible":s["action"],"status":"v0.10独立镜头候选，待作者审阅","missing":"静帧只证明代表状态；连续走位、抬枪、运镜与声音待视频阶段实现。","show_as_main":True}
    if sid=="CY026": s["presentation"]["missing"]+=" 背向队形有遮挡，不把本镜当作九位同伴逐人身份验收；正面群像另镜交代。"
    s["generation_request"]=request;s["visual_prompt"]=job["request"]["prompt"]
    s["refs"]=[{"path":paths[sid],"role":"本版独立原画"},{"path":request,"role":"实际提交提示词与参考输入"}]
    if sid in ["CY027D","CY027F"]: s["refs"].append({"path":oldpath,"role":"保留的上一版"})
    if sid!="CY009A":s["refs"].append({"path":"资产/图像/CHAR-PALADIN-v001.png","role":"骑士共用造型"})
    s["panel_index"]=0;s.pop("display_crop_normalized",None)
    s["editorial_review"]={"version":"v010","status":"candidate_static_review","dynamic_execution":"pending"}
elapsed=0
for i,s in enumerate(d["shots"]):
    s["start_second"]=elapsed;elapsed+=s["seconds"];s["end_second"]=elapsed
    s["next_link"]=("接 "+d["shots"][i+1]["id"]+"："+s["exit_state"]+" → "+d["shots"][i+1]["entry_state"]) if i+1<len(d["shots"]) else "结束。"
d["total_seconds"]=elapsed
d["page_layouts"]=[{"path":s["presentation"]["path"],"rows":1,"cols":1} for s in d["shots"]]
for scene in d["scenes"]:
    group=[s for s in d["shots"] if s["scene"]==scene["id"]]
    scene["shot_ids"]=[s["id"] for s in group];scene["seconds"]=sum(s["seconds"] for s in group)
    scene["pages"]=list(dict.fromkeys(s["presentation"]["path"] for s in group));scene["path"]=scene["pages"][0]
assert all(s["source_quote"] in script for s in d["shots"]),[s["id"] for s in d["shots"] if s["source_quote"] not in script]
write("镜头设计/shot-plan-v0.10.json",d)
assets=read("资产/assets-before-paladins-v010.json")
assets["title"]="《穿云》资产图册 · v0.4"
assets["scope"]+=" 新增白银淡紫封盔长枪圣骑士，用于宫门守卫与教堂集结、冲入和警戒；四视图为本轮候选。"
assets["assets"].append({"id":"CHAR-PALADIN","name":"白龙宫殿圣骑士 · 四向全身","category":"群演","version":"v001","status":"候选待作者审阅","path":"资产/图像/CHAR-PALADIN-v001.png","role":"正面、左侧、背面、右侧全身；白银盔甲与淡紫披风，封闭头盔不露脸，长枪。宫门守卫与援军同一造型。","limits":"侧背结构是设计补全，不作为精确工程正交图。队伍枪距、披风碰撞与行进连续性待动态验证。","source":"资产/生成记录/CHAR-PALADIN-v001.json","related":[{"path":"资产/图像/CHAR-GPT-v003.png","role":"白银淡紫色系与纹饰参考"},{"path":"镜头设计/生成记录/王宫骑士-v010/CHAR-PALADIN-请求-v001.json","role":"实际生成请求"}]})
write("资产/assets.json",assets)
records=read("镜头设计/生成记录/王宫骑士-v010/结果映射.json")+read("镜头设计/生成记录/王宫骑士-v010/返修结果映射.json")
records.append(read("镜头设计/生成记录/王宫骑士-v010/门板返修结果.json"))
for r in records:
    r["sha256"]=hashlib.sha256((root/r["destination"]).read_bytes()).hexdigest()
    assert r["sha256"]==hashlib.sha256(Path(r["original"]).read_bytes()).hexdigest()
    r["status"]="candidate" if r["destination"] in paths.values() else "superseded-preserved"
    if r["id"]=="CHAR-PALADIN":r["status"]="candidate"
write("镜头设计/生成记录/王宫骑士-v010/归档校验.json",records)
write("资产/生成记录/CHAR-PALADIN-v001.json",{"engine":"built-in imagegen","request":"镜头设计/生成记录/王宫骑士-v010/CHAR-PALADIN-请求-v001.json","output":next(r for r in records if r["id"]=="CHAR-PALADIN"),"status":"候选待作者审阅","visual_review":"四向全身可见；全封闭头盔、长枪、白银淡紫；披风生成较长，以实际图为准。"})
print(json.dumps({"shots":len(d["shots"]),"seconds":elapsed,"new_images":len(records)},ensure_ascii=False))
