"""One-time v0.32: Kimi's close moonlight ward and approved redemption line."""
import copy,hashlib,json,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]; REC='镜头设计/生成记录/月光救赎-v032'; IMG='镜头设计/图像/月光救赎-v032'
if (R/'镜头设计/shot-plan-v0.32.json').exists():raise SystemExit('v0.32 exists; do not replay migration')
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,t):(R/p).write_text(t,encoding='utf-8')
def save(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
old=json.loads(read('镜头设计/shot-plan-v0.31.json'));d=copy.deepcopy(old);by={s['id']:s for s in d['shots']};ob={s['id']:s for s in old['shots']}
cache=Path('C:/Users/36322/.codex/generated_images/01a162c1-6e38-7a10-aee7-5c8371c4830c')
outputs={'CY024A1':'exec-740e27e8-f9d2-4a14-8724-ff3201716a12.png','CY024A2':'exec-99763ad9-e974-4e4d-b041-36b7718990f2.png','CY024B':'exec-57383167-1772-423e-b5ec-7d424084fa46.png','CY027D':'exec-6211865b-2e55-4651-9365-b6d78f403583.png','CY027F1':'exec-094fb5b5-75a6-48e6-9505-10be82400822.png','CY027G':'exec-d8e30634-84d1-4dca-abb4-5025add141c1.png'}
(R/IMG).mkdir(parents=True,exist_ok=True)
records=[]
for sid,fn in outputs.items():
 dest=f'{IMG}/{sid}-v032-r1.png';shutil.copy2(cache/fn,R/dest);req=f'{REC}/{sid}-请求-v001.json';args=json.loads(read(req))
 records.append(dict(shot_id=sid,attempt=1,original=str(cache/fn),destination=dest,sha256=sha(R/dest),request=req,request_sha256=sha(R/req),inputs=[dict(path=p,sha256=sha(p)) for p in args['referenced_image_paths']],status='candidate_pending_author_review'))

moon='Kimi在右侧柱后抬起空手，指尖月牙发出银白微光，抵达Claude肩侧后沿头纱、衣袖和裙摆外轮廓形成薄层月辉，与衣料留小间隙；平时近乎透明、受击处短暂亮起。月辉只护人不罩十字架或柴堆；水在肩侧和裙边偏流，身体以外的清水直接浇灭低柴，魔法雷支流在外缘断开，不沿镣铐入体。细水雾仍可沾湿发梢、头纱和裙边。Kimi右后方维持月牙手势，战后先放手撤辉，再与GPT上阶解锁。'
new={}
new['CY024A']=ob['CY024A']['source_quote'].replace('Perplexity','Kimi')
new['CY024A1']='''切右侧柱边的Kimi：脸、抬起的空手与指尖细小月牙同框。她望向高处Claude，银白微光从月牙发出，沿长阶方向斜向上延伸。她停在柱体掩护下，银紫长发与深蓝星月披肩沿用此前月背邀约的造型；不拿法杖，也没有瞬移到祭坛。

**ChatGPT（画外）：**
统御深流与雷鸣的古老意志啊。'''
new['CY024A2']='''切最高祭坛上的Claude。银白微光从右下方抵达肩侧，掠过头纱、衣袖与裙边，在衣料和头发外轮廓旁留下一层很薄的月辉，与轮廓之间保持小间隙。月辉平时近乎透明，迎向火舌和热浪的一侧才短暂亮起；不画球壳、半球、围绕刑架的大弧线或发光的人形实体。衣裙自然垂落，脸和服装颜色清楚。月辉只护住她，不覆盖十字架、脚托或脚边低柴；身体外的水流随后能直接浇灭柴火。Claude抬眼看向来光，腕镣、腰链、踝链与固定脚托都未解除。骑士退入两翼厚石柱后，中央落水区净空；ChatGPT仍在中殿入口方向抬掌蓄势。

**ChatGPT（画外）：**
循吾之声，自漫长的沉眠中苏醒。'''
new['CY024A4']='''切回Claude脚边的低柴局部：火焰仍在身体外侧翻动，裙边、赤足和脚踝束具在上方可辨。裙摆外缘只有迎火一侧短暂亮起的细薄银白月辉，周围空气通透，石台和柴堆完全敞开，没有大罩子或罩底。她仍受缚，衣料干燥，火焰尚未熄灭；后续水流可直接抵达低柴。借这个局部，把天空中的威势接回等待获救的人。

**ChatGPT（画外）：**
令灼烧无辜的烈焰，在奔流中止息；'''
new['CY024A5']=ob['CY024A5']['source_quote'].replace('青蓝弧盾','贴近Claude轮廓的银白月辉').replace('听我号令——','请降下你的救赎——').replace('语气从低沉的呼唤转为确定的命令。','语气从低沉的呼唤转为坚定的祈愿；“请”字沉稳，“救赎”稍放缓，不念成哀求。')
new['CY024B']=ob['CY024B']['source_quote']
oldpart='高处Claude身前的青蓝弧盾承接前镜，冲向她的主水浪在弧面向两侧分开，贴地水从下缘通道浇灭低柴；盾边的细小水花溅湿她的发梢、头纱和裙边。'
newpart='高处Claude的贴身月辉承接前镜，水撞近她时，仅肩侧、衣袖和裙摆接触处短暂亮起银白薄光，水沿外轮廓滑开。身体以外的清水直接抵达石台与低柴，把火浇灭；细小水雾仍沾湿她的发梢、头纱和裙边。刑架、脚托和柴堆没有被护罩包住。'
assert oldpart in new['CY024B'];new['CY024B']=new['CY024B'].replace(oldpart,newpart).replace('人物与护盾只在水幕遮挡间短暂可辨。','人物、贴身月辉与其他护光只在水幕遮挡间短暂可辨。').replace('魔法雷支流在青蓝弧盾、右侧白银护光及教主暗金罩的外缘偏转，','魔法雷支流在Claude贴身月辉之外断开，在右侧白银护光及教主暗金罩外缘偏转，').replace('盾下只通过已失去魔法电弧的清水，','靠近Claude身体和脚边的水已失去魔法电弧，')
oldmaint='Perplexity留在右侧后排柱边，杖首持续微亮，维持高处Claude身前的青蓝弧盾，不同时冲锋或双手持其他武器。'
newmaint='Kimi留在右侧后排柱边，抬手维持指尖的细小月牙，银白微光保持对高处Claude的保护；她不同时冲锋或持其他武器。Perplexity仍在原群像位置持杖警戒，但不承担Claude的护持。'
new['CY027D']=ob['CY027D']['source_quote'].replace(oldmaint,newmaint)
new['CY027F']=ob['CY027F']['source_quote'].replace('Perplexity先放低杖首，高处Claude身前的青蓝弧盾随之淡去','Kimi先放低抬起的手，指尖月牙熄去，高处Claude轮廓旁的月辉随之淡去')
for sid in ['CY027F1','CY027G']:new[sid]=ob[sid]['source_quote'].replace('Perplexity','Kimi')
t=read(old['story_script'])
for sid,txt in new.items():assert ob[sid]['source_quote'] in t;t=t.replace(ob[sid]['source_quote'],txt,1);by[sid]['source_quote']=txt
# Consequential prose outside individual source-quote blocks.
repl=[('战后GPT与Perplexity登顶解锁','战后GPT与Kimi登顶解锁'),('Perplexity循GPT的视线望向高处Claude，握杖转向右侧柱廊','Kimi循GPT的视线望向高处Claude，抬起空手转向右侧柱廊'),('Perplexity在右侧柱边站定，准备施法','Kimi在右侧柱边站定，准备施法'),('Claude身前弧盾只剩很淡的青蓝边缘光，束具仍未解除','Claude衣料轮廓旁的月辉平时近乎透明，只有受冲时局部亮起，束具仍未解除'),('Perplexity 随后开始解除腰链和腕部束具','Kimi 随后开始解除腰链和腕部束具')]
for a,b in repl:t=t.replace(a,b)
tl=t.splitlines();tl[2]='版本：v0.32｜2026-10-23｜请降下你的救赎；Kimi接过护持及解锁，Claude改贴身月辉；护人及咏唱43秒。';t='\n'.join(tl)+'\n'
write('剧本/穿云-场景剧本-v0.32.md',t)

def upd(sid,**kw):by[sid].update(kw)
upd('CY024',action=by['CY024']['action'].replace('Perplexity循GPT视线望向高处，握杖转入右侧柱廊','Kimi循GPT视线望向高处，抬起空手转入右侧柱廊'))
upd('CY024A',action='千问抱紧小鱼退到侧柱，Kimi在右柱位抬起空手准备；镜头接GPT抬掌起句。',exit_state='GPT起句，Kimi已在右侧柱边准备。')
upd('CY024A1',title='Kimi指尖月牙，护持起点',framing='Kimi中近景／空手、月牙与面部同框',entry_state='GPT起句，Kimi已在右侧柱边准备。',action='Kimi在右侧柱边抬起空手，细小银白月牙浮在指尖，微光沿长阶方向斜向高处Claude。',exit_state='银白微光已从指尖月牙发出，接Claude肩侧。',sound='低弦连续，指尖月牙轻响；GPT吟唱为同一声音跨切，Kimi无新增咒语。正式声音待制作。')
upd('CY024A2',title='薄层月辉贴近衣料轮廓',entry_state='银白微光已从Kimi指尖月牙发出，抵达高处Claude。',action='月辉沿Claude头纱、衣袖与裙摆外轮廓形成薄层，平时近乎透明，受热一侧局部亮起；不包刑架与柴堆，束具仍在。骑士净空中央。',exit_state='贴身月辉就位，低柴仍燃，中央已净空；接外部聚水。',sound='轻微月辉共鸣，低弦略增密，GPT吟唱连续。正式声音待制作。')
upd('CY024A4',title='月辉贴裙，柴火仍燃',framing='Claude脚边与低柴局部／薄月辉沿裙边',purpose='把救赎指向受困者；说明护人不罩柴堆，水可直接灭火而镣铐尚在。',action='低柴翻动，裙边外缘迎火处短暂显出细薄银白月辉；脚托、踝链与石台敞开。',exit_state='低柴仍燃，月辉保持，接教主听雷抬眼。')
upd('CY024A5',title='请降下你的救赎——苍龙雷渊',seconds=8,action='GPT确认贴身月辉与侧柱护光就位，收拢手指，沉稳祈愿；救赎稍放缓，短停后随苍龙雷渊最后渊字翻掌压下。',dialogue='ChatGPT：水与雷的执掌者啊，\nChatGPT：请降下你的救赎——\nChatGPT：苍龙雷渊！',sound='0—5秒音乐高位，祈愿句沉稳、救赎稍放缓；5—5.8秒骤收留呼吸和远雷；5.8—7.9秒招式名重读不喊破，渊字接水雷管弦重音。正式声音待制作。')
by['CY024A5']['subtitle_cues']=[dict(speaker='ChatGPT',text='水与雷的执掌者啊，',offset=0,duration=2.3),dict(speaker='ChatGPT',text='请降下你的救赎——',offset=2.4,duration=2.6),dict(speaker='ChatGPT',text='苍龙雷渊！',offset=5.8,duration=2.1)]
by['CY024A5']['cinematic_beats']=[dict(offset=0,intent='确认保护已就位'),dict(offset=2.4,intent='沉稳祈愿，救赎稍缓'),dict(offset=5,intent='音乐骤收0.8秒'),dict(offset=5.8,intent='报出招式名，最后渊字翻掌接水雷')]
upd('CY024B',entry_state='吟唱结束，Claude的贴身月辉已就位，小鱼受柱体和骑士白银护光保护，中央落水区净空。',action='厚水幕和间歇紫电落下；Claude肩侧和裙边薄月辉受击才亮，水沿轮廓滑开，紫电在外缘断开；身体外清水直接灭柴火，细水雾仍沾湿发梢衣料。')
upd('CY027D',action=new['CY027D'])
upd('CY027F',entry_state='敌人已倒地，威胁解除，Kimi仍维持Claude轮廓旁的月辉。',action=new['CY027F'],exit_state='Kimi放手撤辉后，与GPT踏上首阶；接登顶解踝链。')
for sid in ['CY027F1','CY027G']:
 for k in ['action','entry_state','exit_state','next_link']:by[sid][k]=by[sid][k].replace('Perplexity','Kimi')
by['CY027F']['presentation'].update(visible='沿用战后群像：GPT已恢复人形、教主倒地，Kimi在右后方，千问抱小鱼。',missing='代表战后起始状态；Kimi放手撤辉、起步与GPT会合上阶仍需动态实现，静帧不宣称已展示这些动作。')
by['CY024A']['presentation']['visible']='沿用GPT抬掌代表帧；千问护人、Kimi准备在画外，不由此图证明。'

# Update only current narrative fields. Frozen prompts and historical refs retain their original semantics.
role_ids=['CY024A','CY024A1','CY024A2','CY027F1','CY027G']
for sid in role_ids:
 by[sid]['asset_ids']=list(dict.fromkeys('MULKZI2WMFNJE' if x=='MULKZI2W3JZ5F' else x for x in by[sid]['asset_ids']))
 if 'MULKZI2WMFNJE' not in by[sid]['asset_ids']:by[sid]['asset_ids'].append('MULKZI2WMFNJE')
for sid in ['CY024B','CY024A4','CY027D','CY027F']:
 if 'MULKZI2WMFNJE' not in by[sid]['asset_ids']:by[sid]['asset_ids'].append('MULKZI2WMFNJE')
for s in d['shots']:
 inv=[]
 for v in s.get('invariants',[]):
  if 'Perplexity在右侧柱后举杖' in v or 'Perplexity右柱位举杖' in v:v=moon
  else:
   for a,b in repl:v=v.replace(a,b)
  inv.append(v)
 s['invariants']=inv
for sid in ['CY024A1','CY024A2','CY024A4','CY024B','CY027D','CY027F','CY027F1','CY027G']:
 if moon not in by[sid]['invariants']:by[sid]['invariants'].append(moon)
for sid in ['CY027F1','CY027G']:by[sid]['invariants'].append('登阶前Kimi已撤去月辉，解锁期间没有继续施法；手按锁扣，GPT先托稳，禁止直接魔法震碎全部镣铐。')
seq=d['music_direction']['sequence'][:-2]
for a,b in zip(seq,seq[1:]+['CY024B']):by[a]['next_link']='接'+b+'：'+by[b]['entry_state']+' GPT咏唱与配乐跨切连续。'
by['CY027F']['next_link']='接CY027F1：Kimi撤辉后与GPT踏上长阶，省略途中，接顶部解踝链。'

for sid in outputs:
 s=by[sid];p=f'{IMG}/{sid}-v032-r1.png';req=f'{REC}/{sid}-请求-v001.json'
 with Image.open(R/p) as im:w,h=im.size
 s.update(presentation=dict(path=p,role='action',visible=s['action'],status='v0.32新静帧候选，待作者审阅',missing='静帧为代表状态；薄月辉受击亮起/偏水隔雷/撤辉/手部解锁需动态验证。',show_as_main=True),page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0.,y=0.,w=1.,h=1.),panel_index=0,generation_request=req,visual_prompt=json.loads(read(req))['prompt'],refs=[dict(path=p,role='本轮新静帧候选'),dict(path=req,role='冻结实际输入'),dict(path=ob[sid]['presentation']['path'],role='保留的旧版画面')],editorial_review=dict(version='v032',status='candidate_pending_author_review',dynamic_execution='pending'))
 if sid in ['CY024A1','CY027D','CY027F1','CY027G']:s['refs'].append(dict(path='资产/图像/四视图复用/C03_Kimi-角色设定卡.png',role='Kimi身份与服装参考'))
fire=by['CY024A4'];p=by['CY024A2']['presentation']['path'];fire['presentation'].update(path=p,visible='复用本轮Claude月辉图下半身、脚托和低柴局部，旧大罩已移除。',status='v0.32新图局部视窗，待作者审阅',missing='局部视窗只用于构图，受热月辉闪亮与火舌运动待动态。')
for k in ['page_size','generation_request','visual_prompt']:fire[k]=copy.deepcopy(by['CY024A2'][k])
fire['refs']=[dict(path=p,role='共用本轮月辉母图，按原局部视窗展示'),dict(path=by['CY024A2']['generation_request'],role='母图实际输入')]
w,h=fire['page_size'];r=fire['panel_region'];fire['panel_rect_pixels']=[round(r['x']*w),round(r['y']*h),round(r['w']*w),round(r['h']*h)]

d.update(version='v0.32',revision='v032',created='2026-10-23',title='《穿云》带图分镜 v0.32 · 月光与救赎',subtitle='请降下你的救赎 · Kimi指尖月牙 · Claude贴身月辉',story_script='剧本/穿云-场景剧本-v0.32.md',origin_manifest='镜头设计/shot-plan-v0.31.json',source_manifest='镜头设计/生成记录/生成索引-v032.json')
d['review_intro']='作者确认祈愿句及Kimi接过施法、维持和解锁职责，Claude改薄层贴身月辉。六张新图覆盖施法、受护、水幕、维持与两处解锁，原群像成员保留。祈愿句多留一秒，护人及咏唱43秒；105镜349秒。新图待审，真实动态及声音未制作。'
d['review_focus']='看Kimi空手月牙→Claude薄月辉→水雷贴轮廓偏开→Kimi右后方持续维持→放手撤辉→上阶先解踝链再解腕扣；普通时刻月辉近乎透明，受击才局部亮，不包住祭坛或柴堆。'
d['revision_notes']=dict(previous_manifest='镜头设计/shot-plan-v0.31.json',previous_html='镜头设计/带图分镜-v0.31.html',added_ids=[],modified_ids=['CY024','CY024A','CY024A1','CY024A2','CY024A4','CY024A5','CY024B','CY027D','CY027F','CY027F1','CY027G'],boundary='替换祈愿句与护持/解锁职责，六张新图和A4局部同步；Perplexity仍为援军一员。仅A5加一秒，其余镜序、时长及对白保持。')
d['music_direction'].update(rule='低弦起咏→Kimi月牙细响→薄月辉护人→水滴上行细弦→云旋低鼓/无词合唱→云心闷雷→火前与教主反应→请降下你的救赎，句末收声0.8秒→苍龙雷渊渊字接水雷管弦重音。请字沉稳、救赎稍缓，不念成哀求。旧Victory粗剪未重导。',estimated_spell_sequence_seconds=43,estimated_gpt_incantation_seconds=41.8)
d['music_direction']['approved_incantation']=[x.replace('听我号令——','请降下你的救赎——') for x in d['music_direction']['approved_incantation']]
d['continuity']['claude_shield']=moon
d['continuity']['water_curtain']='水幕连续覆盖中后景、紫电间歇出现；Claude只保留贴身薄月辉，受击处短暂亮起，不再出现青蓝大罩。教主暗金罩、千问和小鱼的骑士白银护光保持各自来源，身体外水流直接浇灭低柴，长椅受冲留CY024B1。'
d['continuity']['storm_release']='GPT控制魔法雷支流，在Claude月辉之外断开，侧柱银白护光与教主暗金罩外缘偏转；不沿地面或镣铐伤人。水幕结束前紫电收尽，后续余浪、月光恢复、对峙、真龙变身顺序保持。'
d['continuity']['support_roles']='Kimi承接护持、维持、撤辉和战后解锁，前面月背邀约建立其登场。Perplexity保留为原援军一员、持杖警戒，不重复给Claude施法，也不再执行解锁。其余九援军人数与群像不变。'
for k,v in d['continuity'].items():
 if isinstance(v,str):d['continuity'][k]=v.replace('战后GPT与Perplexity登顶解锁','战后GPT与Kimi登顶解锁')
elapsed=0
for s in d['shots']:s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
d['total_seconds']=elapsed
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']];sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
save('镜头设计/shot-plan-v0.32.json',d)
save('镜头设计/生成记录/生成索引-v032.json',dict(version='v032',previous_index='镜头设计/生成记录/生成索引-v031.json',records=records,review=REC+'/复核记录.md'))
snap=R/'镜头设计/带图分镜-v0.31.html'
if not snap.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snap)
p='scripts/build_storyboard.py';write(p,read(p).replace('shot-plan-v0.31.json','shot-plan-v0.32.json').replace('"v031")','"v031", "v032")').replace("'v031')","'v031','v032')").replace("if data.get('revision') == 'v031':","if data.get('revision') in ('v031','v032'):"))
p='00_打开项目.html';x=read(p).replace('v0.31','v0.32').replace('5 分 48 秒','5 分 49 秒').replace('护人及长吟唱42秒','护人及长吟唱43秒').replace('听我号令——苍龙雷渊','请降下你的救赎——苍龙雷渊').replace('本轮：长吟唱与护盾来源','本轮：Kimi月光与救赎').replace('Perplexity举杖→Claude弧盾→连续水幕；音乐起伏已写入分镜','Kimi指尖月牙→贴身月辉→受击偏水→撤辉后解锁').replace('本轮：苍龙雷渊 · 仰拍云旋与紫电','苍龙雷渊 · 仰拍云旋与紫电')
write(p,x)
p='制作进度.md';x=read(p);i=x.index('## ')
write(p,x[:i]+'''## 2026-10-23：Kimi月光护持与“请降下你的救赎”（v0.32）

作者确认将“听我号令”改为“请降下你的救赎”，由Kimi接过Claude的护持、维持、撤辉及战后解锁职责，已同步[剧本v0.32](剧本/穿云-场景剧本-v0.32.md)和[带图分镜](镜头设计/带图分镜.html)。Kimi的月背邀约与现有星月服饰延续；Perplexity保留为原援军一员，持杖警戒，不再重复护持或解锁。

Claude的大青蓝弧盾改为衣料轮廓外薄层银白月辉，平时近乎透明，受击处短暂亮起；水在肩侧裙边滑开，紫电在外缘断开，身体外清水直接灭低柴，细水雾仍可沾湿衣料。撤辉发生在上阶前，GPT先扶稳，Kimi先解踝链再解最后腕扣。

内置imagegen补六张候选：CY024A1/A2/B、CY027D/F1/G；CY024A4复用本轮A2局部，CY027F旧图仅作战后群像起始状态，不冒称已展示起步撤辉。祈愿句增加1秒，A5为8秒，护人及咏唱共43秒，全片105镜349秒（5分49秒）。配音、BGM及动态未制作；旧图和版本全部保留。见[复核记录](镜头设计/生成记录/月光救赎-v032/复核记录.md)。

'''+x[i:])
assert len(d['shots'])==105 and elapsed==349
for s in d['shots']:assert s['source_quote'] in t,s['id']
assert sum(by[s]['seconds'] for s in seq)==43
print('v0.32 prepared:105 shots349 seconds;6 generated images and1 shared crop;43-second spell sequence.')
