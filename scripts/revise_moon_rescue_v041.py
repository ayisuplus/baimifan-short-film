"""Apply the approved small moon-blade rescue to the existing storyboard, preserving history."""
import copy, hashlib, json, re, shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
IMG='镜头设计/图像/月刃救援-v041'
REC='镜头设计/生成记录/月刃救援-v041'
PLAN='镜头设计/shot-plan-v0.41.json'
def read(p): return (R/p).read_text('utf-8-sig')
def write(p,t): (R/p).parent.mkdir(parents=True,exist_ok=True);(R/p).write_text(t,encoding='utf-8')
def load(p):return json.loads(read(p))
def save(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
assert not (R/PLAN).exists(),'Do not overwrite an existing revision'
old=load('镜头设计/shot-plan-v0.40.json');d=copy.deepcopy(old)
by={s['id']:s for s in d['shots']};script=read(old['story_script'])
route='Kimi与GPT在稍早的月背邀约中约定分路：GPT带八位同伴走正门，Kimi独自绕到刑架背后彩窗。CY024K0画外短咏→K1从后墙偏左高窗破入→K2明刃先护两人→K3暗刃实体劈拨柴→K4试腕镣见痛收刀。随后始终守在最高祭坛，不回柱边或下层队伍。'
shield='明刃先形成覆盖Kimi和Claude的相连窄结界，边界从身体与外侧柴堆之间展开；暗刃可由内向外切出，柴火留在结界外。破柴后护罩包住两人及脚托落脚区，低散柴全在外。水雷中双刃交架承压，主水柱落在下段；侧浪绕盾浇灭外侧残柴，魔法雷在盾外偏转。盾不修衣，少量无电细雾可透入沾湿发梢衣边。战后危险解除才撤盾、收刃、接钥匙。'
pose='Claude解锁前始终直立受缚：双腕横向固定在横木，双腿自然向下，双踝仍锁着，赤足踩窄固定脚托。脚托只承脚底，不是座板；不坐下、不跪坐。先解踝链，GPT扶稳后解最后腕扣，再扶下脚托。'
weapons='Kimi采用作者确认r3小尺寸圆月双刃：人物右手暗刃、左手明刃，圆润月牙外形、内侧握柄，直径约前臂长。明刃护持，暗刃劈拨，水雷到来两刃交架；战后双刃扣回后腰固定环，空手用钥匙解锁。'
window='Kimi打破刑架背后偏左蓝色彩窗的上部一格，窗棂与其他玻璃保留；缺口之后持续存在。碎玻璃沿墙两侧落下，远离Claude和中央落脚位。后殿拱顶仍完整，破窗可能进风和少量雨雾，战后雨停再蒸干衣物。'
wood='祭前脚托两侧只有低矮底柴。教徒每人一根乌烬木，依次堆到Claude腰腹，脸、胸口和受缚双臂露出。点燃后Kimi先保护两人，再以实体暗刃劈开并向两侧外下方拨散木头；残柴仍燃，水雷才灭火。刑架、脚托与所有束具完整，中央留出战后解锁落脚位。'
fire='CY022点燃高柴，黑芯暗紫边火焰向上蔓延。Kimi在CY024K2先撑盾、K3才劈拨；之后中央净空、火只留两侧低散柴，水雷扑灭全部祭薪与普通灯火。最后空刑架星火为橙金色，不点燃湿柴或普通灯具。'
unlock='试刀触及腕镣时束具符纹亮起，Claude痛得缩肩，Kimi立即收刀，不能暴力破坏。战后GPT从倒地教主腰间取原钥匙，独自登阶交给Kimi。Kimi撤盾并将双刃固定后腰，使用钥匙正常解除锁芯，不触发抗破坏符纹；先踝链，再由GPT扶稳后解腰链和腕扣。'
newrules=dict(kimi_dark_moon=route,claude_shield=shield,ritual_wood=wood,ritual_fire=fire,restraints=unlock,
 kimi_weapons=weapons,claude_standing=pose,rear_window=window,
 hall_ensemble='九位援军总数不变：八位随GPT由正门进入，Kimi由后窗进入。迎敌时八位在下层，Kimi在最高祭坛；解锁后离殿重新汇合。',
 support_roles='Kimi负责后窗突入、先护后劈、持续护盾、战后钥匙解锁。Perplexity仍持杖警戒；千问抱护小鱼并保持原扇叶阻击。',
 remaining_image_sync='v0.41更新月刃救援与受影响群像、保护细节、战后衔接；r1普通弯刀、r2过大圆刃、坐姿等错误中间稿保留但不进入当前预演。新动作画面待作者审阅。',
 wet_state='中央中殿露天，后殿拱顶完整但偏左高窗已有破口；雨和水雷细雾使衣发沾湿。战后雨停，护罩撤去后蒸干，不再安排淋雨。')
for k,v in newrules.items():
 if k in old['continuity']:script=script.replace(old['continuity'][k],v)
 d['continuity'][k]=v
changes={}
def change(id,title,quote,entry,exit,sound,seconds=None,framing=None,dialogue=None):
 s=by[id];changes[id]=quote
 s.update(title=title,source_quote=quote,action=quote.split('\n\n**')[0],entry_state=entry,exit_state=exit,sound=sound,purpose=title+'，明确救援因果。')
 if seconds is not None:s['seconds']=seconds
 if framing:s['framing']=framing
 if dialogue is not None:
  s.update(dialogue=dialogue,dialogue_cues=[]);s.pop('subtitle_cues',None)
  if dialogue!='无对白':
   speaker,text=dialogue.split('：',1);s['subtitle_cues']=[dict(speaker=speaker,text=text,offset=0.2,duration=s['seconds']-0.4)]
def new(id,base,seconds):
 s=copy.deepcopy(by[base]);s.update(id=id,seconds=seconds,dialogue='无对白',dialogue_cues=[])
 for k in ['subtitle_cues','time_caption','final_static_review','final_review_exception','split_screen_reveal']:s.pop(k,None)
 by[id]=s
for id,base,seconds in [('CY024K0','CY024K1',4),('CY024K3','CY024K2',4),('CY024K4','CY024K2',3),('CY024B3','CY024B',3),('CY027F0','CY027F',2),('CY027F2','CY027G',3)]:new(id,base,seconds)
change('CY024K0','彩窗后的画外短咏','刑架背后偏左高窗仍然完整，蓝玻璃上掠过一线银白月弧。人没有露面，一句低声咏唱从窗外传来。\n\n**Kimi（画外）：**\n月之暗面，借我锋芒。','GPT正门牵制，高柴仍燃。','声音将注意力引向后窗。','短咏前压低配乐，玻璃细鸣、殿内火声',framing='后墙高窗仰拍特写，刑架顶端在下沿',dialogue='Kimi（画外）：月之暗面，借我锋芒。')
change('CY024K1','破窗，落向刑架左侧','银白月弧骤亮。Kimi双持一暗一明的小圆月刃，从刑架背后偏左彩窗的上部破入，身体斜向下扑向最高祭坛左侧空石地。碎玻璃被刃缘月光带向墙侧，避开Claude；高柴仍燃，尚未劈动。','窗外短咏结束，Kimi已就位。','Kimi落在刑架左侧，立即准备撑盾。','清脆破窗、衣摆破风、轻落地',seconds=3,framing='祭坛侧低机位中全景，破窗路径与Claude同框',dialogue='无对白')
change('CY024K2','明月先护住两人','Kimi落稳后先举起左手明月刃，银白结界从Claude衣料与外侧高柴之间展开，再与自己身周相连，把两个人和脚托落脚区护住。右手暗月刃暂低垂；木柴还没有劈开，火焰被隔在结界外。','Kimi落地，高柴仍围住Claude腰腹。','两人先获得保护，高柴完整留在外侧。','明刃清鸣、结界展开，外围紫黑火继续',framing='最高祭坛正面中全景，护罩边界与未破高柴可辨',dialogue='无对白')
change('CY024K3','暗月劈柴，向外拨开','明刃继续护持。Kimi压低重心，右手暗刃切进乌烬木接缝，再用月牙内缘勾住松开的木段，向两侧外下方劈拨。木头贴地滚落，避开刑架与束具；Claude直立的裙摆、锁着的脚踝和脚下窄脚托逐渐露出。散柴仍燃紫黑火，全部留在结界外。','两人已在结界内，高柴尚完整。','中央让空，Claude仍直立受缚，两侧低散柴继续燃烧。','实体木裂、刃口划木、低处滚木，不用爆炸声',framing='祭坛近全景，刀刃接木、站姿与脚托同框',dialogue='无对白')
change('CY024K4','腕镣反噬，立刻收刀','Kimi用右手暗刃轻试Claude腕镣的接缝。铁扣上的细小符纹突然亮起，Claude痛得闭眼缩肩。Kimi立刻收回刀锋，改为继续守住她；腕镣没有断开，明刃始终维持保护。','柴已清开，Claude仍受缚。','发现束具抗破坏，停止暴力开锁，等待战后钥匙。','金属轻触、符纹短鸣、短促吸气；不增加伤口',framing='腕扣与两人反应的近景',dialogue='无对白')
change('CY024A1','祭坛上的守护者','切最高祭坛左侧的Kimi。她已经停下试镣，左手明刃贴近胸前维持两人的银白结界，右手暗刃低垂戒备。Claude直立在刑架上，残柴只在罩外低处燃烧；Kimi侧耳听向中殿雷声。\n\n第二句咏唱从前面的阻击连续接来，至本镜念完；不重复起句。\n\n**ChatGPT（画外，跨镜完整句）：**\n统御深流与雷鸣的古老意志啊。','Kimi已停下试镣，始终守在Claude旁。','明刃护持不断，准备承接水雷。','GPT画外咏唱承接，护罩低鸣，外围燃柴声',framing='祭坛Kimi中近景，Claude在右侧受缚')
change('CY024A2','护罩内，缓回一口气','透过银白结界看Claude苍白汗湿的脸。她仍直立，双腕固定横木；外围两侧残柴的黑焰映出紫边，中央已经清开。结界隔开继续逼近的热焰，她缓回一口气，焦损的袖边与头纱没有恢复。\n\n**ChatGPT（画外）：**\n循吾之声，自漫长的沉眠中苏醒。','明刃护罩已经维持。','Claude受到保护但仍虚弱受缚。','咏唱继续，呼吸渐稳，火声留在罩外',framing='Claude侧面近景，银白罩缘在前景')
change('CY024A4','窄脚托上，双踝仍锁着','切脚托、踝链与裙边局部。Claude双腿自然垂直，双踝仍锁着，赤足踩窄固定脚托；这不是座板。中央柴已经让开，银白罩缘沿落脚区外侧延伸，紫黑火只在边缘散柴上燃烧。外裙焦损保留，内层衣料完整。\n\n**ChatGPT（画外）：**\n令灼烧无辜的烈焰，在奔流中止息；','中央柴已拨散，盾覆盖脚托区。','脚托与踝链完整，残柴仍在罩外等水雷灭火。','承接咏唱、低火声',framing='脚托与两只踝扣特写')
water=by['CY024B']['source_quote'];start=water.index('高处Claude的贴身月辉');end=water.index(' 魔法雷支流',start)
water=water[:start]+'最高祭坛上，Kimi守在Claude左侧，双刃交架，银白结界将两人和脚托落脚区包住。Claude双腕与双踝仍锁着，直立踩在窄脚托上。厚重侧浪撞向罩面后绕向外侧，将已被暗刃拨开的散柴直接浇灭；结界内不留燃木。少量无电细雾沾湿发梢、头纱与衣边。后殿拱顶完整，偏左高窗破口保留；两人只在水幕间隙短暂可辨。'+water[end:]
water=water.replace('Claude贴身月辉','两人银白结界').replace('月辉不修复衣物','结界不修复衣物').replace('下一镜长椅只受清水余浪冲击','接承压近景，紫电先收尽后长椅只受清水余浪冲击')
change('CY024B','宏大水雷，双人护罩',water,'GPT空中压掌，Kimi已护住两人。','水雷灭掉罩外残柴，盾承受侧浪。','单柱水雷轰鸣、撞罩分流与雷声，保持原规模')
change('CY024B3','双月交架，顶住水势','水雷侧浪抵达最高祭坛。Kimi后脚抵地，双臂交架，将一暗一明的圆月刃扣在胸前，银白罩面被厚重水幕压出一圈圈涟漪。Claude在她身后直立受缚，脚踩窄脚托，腕踝锁扣完整。水和魔法雷被导向罩外，散柴已经熄灭；紫电先收尽，再接清水余浪。','厚重侧浪撞向祭坛。','两人安全，残柴全湿，紫电收尽。','近处压水轰响、盾面低鸣、Kimi用力呼吸',framing='祭坛低机位近全景，交架双刃和站立Claude同框',dialogue='无对白')
change('CY027D','八人守门，Kimi守祭坛','听见入口岗哨示警，八位同伴在长阶下形成第二道防线，千问仍抱着小鱼。两翼骑士守住柱廊，前排迎向门外教徒；Kimi没有离开最高祭坛，始终在Claude左侧维持双人结界。Perplexity持杖警戒，不承担Claude护持；后墙偏左高窗缺口仍在。','外院教徒逼近，殿内水雷已退。','入口被守住，Kimi持续护住仍受缚的Claude。','门口搏击与骑士示警，祭坛护罩轻鸣',framing='长阶广角群像，八人在下层，远处Kimi与Claude同处祭坛')
change('CY027F','战斗结束，先取钥匙','战斗结束，雨渐停。ChatGPT已恢复人形，落到湿地。教主与教徒倒地，八位同伴在下层收住攻势，千问仍抱着小鱼；第九位Kimi继续留在最高祭坛守护Claude。GPT望向教主腰间，准备取钥匙后独自登阶。','内外敌人均已被制服。','GPT准备取钥匙，Kimi仍在祭坛，不能重复出现在队伍里。','战后滴水、喘息，远处脚步',framing='中殿战后群像，Kimi在画外高祭坛')
change('CY027F0','从教主腰间取下钥匙','ChatGPT俯身，从倒地教主腰间的扣环上取下黑铁钥匙。钥匙离开腰带，齿形在冷月光里清楚一闪；她握住它，独自朝长阶走去。','教主倒地，钥匙仍在腰间。','GPT带着原钥匙登阶。','钥匙环与扣钩轻响、涉浅水脚步',framing='教主腰带与GPT取钥匙的手部特写',dialogue='无对白')
change('CY027F2','收刃，接过钥匙','省略登阶过程，GPT来到最高祭坛，与一直守在Claude左侧的Kimi会合。确认危险解除，Kimi撤去结界，将双月刃扣入后腰固定环，腾出双手。GPT把从教主处取来的黑铁钥匙交到她掌心；Claude此时仍直立，双腕与双踝都锁着。','GPT携钥匙登顶，Kimi仍在原位。','护罩撤去，双刃收好，Kimi拿到钥匙。','护罩轻散、收刃卡扣、钥匙落掌',framing='祭坛三人中景，交钥匙与后腰收刃可见',dialogue='无对白')
change('CY027F1','用钥匙先解踝链','Kimi蹲在Claude脚托旁，用原钥匙打开两只踝扣并移开短链。锁芯正常转动，抗破坏符纹没有亮起；Claude的赤足仍踩着固定脚托，双腕暂未解除。','Kimi已收刃并接到钥匙。','双踝解除，双腕仍锁，GPT即将扶稳。','钥匙转动、锁舌轻响、链条放下',framing='两只踝扣与钥匙操作近景')
change('CY027G','先扶稳，再开最后腕扣','GPT从画面右侧扶住Claude腰背和上臂。Kimi在左侧用原钥匙解除腰链，再打开最后一个腕扣；符纹没有被暴力触发。Claude身体仍由脚托和GPT承托，没有突然跌落，木架留在最高祭坛。','双踝已解，GPT先扶住。','最后腕扣打开，准备扶下脚托。','锁舌与链条轻响、衣料摩擦',framing='祭坛三人近中景，扶稳与最后开锁同框')
# Source passages updated in place; retain all unaffected screenplay material.
oldby={s['id']:s for s in old['shots']}
for id,q in changes.items():
 if id in oldby:
  assert oldby[id]['source_quote'] in script,id
  script=script.replace(oldby[id]['source_quote'],q)
for anchor,ids in [('CY024',['CY024K0']),('CY024K2',['CY024K3','CY024K4']),('CY024B',['CY024B3']),('CY027F',['CY027F0','CY027F2'])]:
 q=by[anchor]['source_quote'];script=script.replace(q,q+'\n\n'+'\n\n'.join(by[id]['source_quote'] for id in ids),1)
# Invitation remains a flashback; it reveals the previously agreed separate route.
q=by['CY026D']['source_quote'];newq=q+'\n\n**ChatGPT：**\n我走正门。她背后的彩窗，交给你。'
script=script.replace(q,newq,1)
by['CY026D'].update(source_quote=newq,seconds=7,action=q+' GPT低声交代分路，Kimi点头。',dialogue='ChatGPT：我走正门。她背后的彩窗，交给你。 Kimi：嗯。',dialogue_cues=[],subtitle_cues=[dict(speaker='ChatGPT',text='我走正门。她背后的彩窗，交给你。',offset=0.2,duration=5.3),dict(speaker='Kimi',text='嗯。',offset=5.7,duration=1)],exit_state='Kimi同意从Claude背后的彩窗突入。')
changes['CY026D']=newq
script=script.replace('版本：v0.40｜2026-10-24｜搬柴火祭、两次阻拦、最后张臂；Kimi暗月破柴与贴身护盾。新画面待作者审阅。','版本：v0.41｜2026-10-24｜小圆月双刃、后窗突入、先护后劈、双刃承压与钥匙解锁。新动作画面待作者审阅。')
script=script.replace('## 乌烬木、暗月与星火 · v0.40','## 乌烬木、月刃与星火 · v0.41')
script=script.replace('九位援军在她身后错落显露：千问、Gemini、Grok、Kimi、混元、Llama、智谱、Mistral、Perplexity','八位援军在她身后错落显露：千问、Gemini、Grok、混元、Llama、智谱、Mistral、Perplexity；Kimi按事先约定绕向后窗')
script=script.replace('说得平稳、短促。她们没有停步，千问奔向小鱼；Kimi循GPT的视线望向高处Claude，转到右侧柱旁，立即出手。','说得平稳、短促。她们没有停步，千问奔向小鱼；Kimi的后窗突入与正门行动配合。')
script=script.replace('Kimi在右侧柱边站定，持续维持已抵达Claude的贴身月辉','Kimi已从后窗进入，在最高祭坛维持两人的结界')
script=script.replace('Kimi已经在同侧后方持续护持Claude','Kimi已经在最高祭坛持续护住自己与Claude')
script=script.replace('广角中九位 AI 娘都在','广角中八位 AI 娘在下层，Kimi留在画外最高祭坛')
script=script.replace('已在顶部平台的ChatGPT扶稳Claude。Kimi 随后开始解除腰链和腕部束具。','已在顶部平台的ChatGPT扶稳Claude。Kimi随后用原钥匙解除腰链和腕部束具。')
script=script.replace('贴近Claude轮廓的银白月辉','最高祭坛覆盖Kimi与Claude的银白结界')
script=script.replace('人物、贴身月辉','人物、银白结界')
# Remove stale sentences from all current-facing shot metadata, retaining historic references.
old_rule_values={old['continuity'][k]:v for k,v in newrules.items() if k in old['continuity']}
def clean(t):
 for a,b in old_rule_values.items():t=t.replace(a,b)
 t=t.replace('Kimi在右侧柱边站定，持续维持已抵达Claude的贴身月辉','Kimi在最高祭坛维持两人的结界')
 t=t.replace('Kimi已经在同侧后方持续护持Claude','Kimi已经在最高祭坛持续护住自己与Claude')
 t=t.replace('贴近Claude轮廓的银白月辉','最高祭坛覆盖Kimi与Claude的银白结界')
 return t
for s in by.values():
 for k in ['action','entry_state','exit_state','purpose','sound','next_link','source_quote']:
  if k in s:s[k]=clean(s[k])
 inv=[]
 for v in s['invariants']:
  if 'Kimi' in v or '贴身' in v or '九位援军' in v or '九位AI' in v:continue
  inv.append(clean(v))
 s['invariants']=list(dict.fromkeys([pose]+([route,shield,weapons,window] if s['scene']=='S05' else [])+inv))
 # Current metadata can no longer claim the replaced choreography was accepted.
 if s['id'] in changes:s.pop('final_static_review',None)
by['CY024'].update(action='GPT带八位同伴由正门进入，下令护住她们；Kimi按事先约定从后窗接近。',entry_state='正门已破，Kimi不在正门队伍中。',exit_state='千问奔向小鱼，后窗传来短咏。')
by['CY026D']['title']='月背约定，两路救援'
for k in ['invitation','paladins','water_curtain','storm_release','magic','lighting','altar_lighting_v023']:d['continuity'][k]=clean(d['continuity'][k])
d['continuity']['invitation']+=' 月背双人镜补充分路约定，作为稍早计划的揭示；不是临场另行商量。'
script=clean(script)
# New stable IDs inserted without renumbering any existing BGM mark target.
order=[s['id'] for s in old['shots']]
order.insert(order.index('CY024K1'),'CY024K0')
order[order.index('CY023A'):order.index('CY023A')]=['CY024K3','CY024K4']
order.insert(order.index('CY024B1'),'CY024B3')
order[order.index('CY027F1'):order.index('CY027F1')]=['CY027F0','CY027F2']
d['shots']=[by[id] for id in order]
updates={'CY024':1,'CY024K0':2,'CY024K1':1,'CY024K2':2,'CY024K3':3,'CY024K4':2,'CY024A1':2,'CY024A2':1,'CY024A4':1,'CY024B':1,'CY024B3':1,'CY027D':1,'CY027F':1,'CY027F0':1,'CY027F2':2,'CY028A':1}
requests={}
for f in sorted((R/REC).glob('*.json')):
 rows=load(f.relative_to(R))
 if isinstance(rows,dict):rows=[rows]
 for row in rows:
  if isinstance(row,dict) and 'prompt' in row:requests[(row['id'],row.get('rev',1))]=(f.relative_to(R).as_posix(),row)
generated=[]
for id,rev in updates.items():
 s=by[id];p=f'{IMG}/{id}-v041-r{rev}.png';prior=s['presentation']['path'];req,row=requests[(id,rev)]
 s['presentation'].update(path=p,role='action',visible=s['action'],status='v0.41修订候选，待作者审阅',missing='静帧已检查；动态接触、精确动作轨迹、正式声音及最终审美仍待验收。')
 s['refs']=[dict(path=p,role='当前修订候选'),dict(path=prior,role='历史画面保留'),dict(path=req,role='实际生成请求')]
 s.update(visual_prompt=row['prompt'],generation_request=req,editorial_review=dict(version='v041',status='candidate_pending_author_review',dynamic_execution='pending'))
 s.pop('final_static_review',None)
 with Image.open(R/p) as im:w,h=im.size
 s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0,y=0,w=1,h=1),panel_index=0)
 generated.append(dict(id=id,path=p,sha256=sha(p),size=[w,h],request=req,inputs=[dict(path=q,sha256=sha(q)) for q in row['refs']]))
elapsed=0
for i,s in enumerate(d['shots']):
 s.update(start_second=elapsed);elapsed+=s['seconds'];s['end_second']=elapsed
 if i+1<len(d['shots']):s['next_link']='接 '+d['shots'][i+1]['id']+'：'+d['shots'][i+1]['entry_state']
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']]
 sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)),path=ss[0]['presentation']['path'])
d.update(version='v0.41',revision='v041',title='《穿云》带图分镜 v0.41 · 双月刃救援',total_seconds=elapsed,
 subtitle=f'{len(d["shots"])}镜 · {elapsed}秒 · 新动作画面待审',story_script='剧本/穿云-场景剧本-v0.41.md',source_manifest='镜头设计/生成记录/生成索引-v041.json',origin_manifest='镜头设计/shot-plan-v0.40.json',audio_arrangement='后期/月刃救援-v041/预演编排.json',
 review_intro='Kimi独走后窗，先护住两人再以小圆月暗刃劈柴；水雷承压后取钥匙解锁。Claude解锁前始终直立在窄脚托上。',
 review_focus='核对后窗突入→先护后劈→试镣停手→双刃承压→取钥匙与收刃→解锁。新画面与新增台词待审，已选BGM不变。',
 revision_notes=dict(previous_manifest='镜头设计/shot-plan-v0.40.json',added_ids=[id for id in order if id not in oldby],modified_image_ids=list(updates),boundary='r3武器比例已获作者确认；本轮新动作画面仍为候选。旧图、拒绝稿、镜号、音乐标记均保留。'))
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
write(d['story_script'],script)
assert all(s['source_quote'] in script for s in d['shots']),[s['id'] for s in d['shots'] if s['source_quote'] not in script]
save(PLAN,d)
save(d['source_manifest'],dict(version='v041',previous_index=old['source_manifest'],generated_images=len(generated),images=generated,not_used=['KIMI双刃r1普通弯刀被否定','KIMI双刃r2尺寸过大，改r3','CY024K3r1错误坐姿；r2缺踝扣；改r3','CY024K4r1多余手臂，改r2','CY024K2r1火色错误，改r2','CY027F2r1腕位与钥匙错误，改r2']))
a=load(old['audio_arrangement']);a.update(version='v041-picture-sync',previous=old['audio_arrangement'],shot_plan=PLAN,shot_plan_sha256=sha(PLAN))
for s in d['shots']:a['effects'][s['id']]=s['sound']
for id,base in [('CY024K0','CY024K1'),('CY024K3','CY024K2'),('CY024K4','CY024K2'),('CY024B3','CY024B'),('CY027F0','CY027F'),('CY027F2','CY027G')]:
 if base in a['shot_overrides']:a['shot_overrides'][id]=copy.deepcopy(a['shot_overrides'][base])
for id in list(changes)+['CY024','CY026D']:
 if id in a['shot_overrides']:a['shot_overrides'][id].update(note='沿用既有候选；当前动作：'+by[id]['title'],audition_question='比较音乐与本镜动作及对白的配合。')
a['author_feedback']='既有选曲与本机五个标记保留，新增镜头不自动标记；新增画外短咏和分路对白待配音。'
save(d['audio_arrangement'],a)
snapshot=R/'镜头设计/带图分镜-火祭-v040.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
p='scripts/build_storyboard.py';t=read(p).replace('shot-plan-v0.40.json','shot-plan-v0.41.json').replace('"v040")','"v040", "v041")').replace("'v040')","'v040','v041')")
t=t.replace('*(["CY024K1","CY024K2"] if data.get("revision")=="v040" else [])','*(["CY024K0","CY024K1","CY024K2","CY024K3","CY024K4"] if data.get("revision")=="v041" else ["CY024K1","CY024K2"] if data.get("revision")=="v040" else [])').replace('声音预演-v011.json','声音预演-v012.json')
write(p,t)
write('00_打开项目.html',read('00_打开项目.html').replace('v0.40','v0.41'))
assets=load('资产/assets.json')
for a in assets['assets']:
 if a['id']=='MULKZI2WMFNJE':
  a['related'].append(dict(path=f'{IMG}/KIMI双刃-v041-r3.png',role='作者确认小圆月双刃：右暗左明，造型及比例采用；人物原卡仍保留'))
  a['related'].append(dict(path=f'{REC}/月刃比例修订请求.json',role='武器比例实际生成请求'))
  a['limits']+=' 本片双持小圆月刃沿用r3附属参考；战后固定后腰再解锁，不更换已定服装。'
save('资产/assets.json',assets)
progress=f'''## 2026-10-24：后窗双月刃救援（v0.41，新动作画面待审）

作者确认r3小圆月双刃，右暗左明。Kimi与GPT稍早约定分路，画外短咏后从刑架背后偏左高窗突入，先护住两人，再实体劈拨柴火；试腕镣引痛立即停手，水雷中双刃交架。战后GPT取教主原钥匙、独自登阶，Kimi撤盾收刃后接钥匙，接回先踝后腕的解锁。修正作者指出的错误坐姿：Claude解锁前直立受缚，赤足踩窄脚托。

本版{len(d['shots'])}镜{elapsed}秒，16张修订画面接入；新增六个稳定镜号，旧候选与拒绝稿保留。当前[预演台](镜头设计/带图分镜.html)与[剧本v0.41](剧本/穿云-场景剧本-v0.41.md)同步，资产图册附属参考加入已确认双刃。既有BGM文件与标记保留；新增台词以字幕预演，未制作配音、正式音效或动态视频。

'''
t=read('制作进度.md');i=t.index('## 2026-10-24：');write('制作进度.md',t[:i]+progress+t[i:])
print(json.dumps(dict(shots=len(d['shots']),seconds=elapsed,images=len(generated)),ensure_ascii=False))
