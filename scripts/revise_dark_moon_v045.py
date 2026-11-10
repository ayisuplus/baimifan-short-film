"""Publish the author's dark-moon teleport rescue revision; preserve historical media and music."""
import copy, hashlib, json, re, shutil, sys
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/暗月瞬临-v045'
IMG='镜头设计/图像/暗月瞬临-v045'
PLAN='镜头设计/shot-plan-v0.45.json'
def read(p): return (R/p).read_text('utf-8-sig')
def load(p): return json.loads(read(p))
def write(p,t):
 (R/p).parent.mkdir(parents=True,exist_ok=True)
 (R/p).write_text(t,encoding='utf-8')
def save(p,v): write(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256((R/p).read_bytes()).hexdigest()
if '--resume' not in sys.argv:
 assert not (R/PLAN).exists(), 'One-time revision already exists'
 old=load('镜头设计/shot-plan-v0.42.json');d=copy.deepcopy(old)
 script=read(old['story_script'])
 ct={
 'restraints':'试刀触及腕镣时符纹反噬，Claude吃痛，Kimi立刻收刀并将双刃扣回后腰，转而抱托、拭汗及查看束具接触处，不再强拆。战后GPT取教主原钥匙，Kimi确认安全撤去暗月罩后接钥匙；先踝链，再由GPT扶稳后解腰链及腕扣。',
 'wet_state':'中央中殿露天，后殿拱顶完整，十字架正后中央高窗被明刃击穿。入罩前的汗湿与衣发状态保留；暗月罩隔绝洪水与魔法雷。战后撤罩，潮湿殿内的水雾轻沾衣边，再接后续蒸干；所有烛火和散柴均已熄灭。',
 'claude_shield':'明刃穿正后中央高窗、钉入柴堆外缘作为瞬移坐标；Kimi循刃瞬临，左手回收明刃并让气浪沿地面向外震开重柴，Claude与刑架中心保持平静。右手暗刃再展开完全不透明的深靛暗月罩，包住两人、刑架及脚托，全部燃木在外。罩体施放后持续维持，试镣后可收刃空手照顾；受巨浪压迫时Kimi空掌抵内壁并抱托Claude。外景只见暗壳，内景只见暗膜内侧，不透看外界。安全确认后才撤罩接钥匙。',
 'kimi_dark_moon':'Kimi与GPT稍早约定分路，GPT带八位同伴走正门。Kimi在十字架正后中央高窗外的月光中显现剪影，画外短咏；K1明刃力量破窗特写→K1A钉入柴堆外缘→K2循刃瞬移、收明刃、向外爆气震柴→K3右暗刃闭合不透明暗月罩→K4试镣见痛收刀。此后始终留在最高祭坛内照顾Claude，不回下层队伍。',
 'kimi_weapons':'沿用作者确认的小尺寸圆月双刃，右手暗刃、左手明刃，圆润月牙外形、内侧握柄。明刃负责穿窗定位，Kimi瞬移时立即以左手回收；右暗刃施放不透明暗月护罩。试镣后双刃扣回后腰，空手抱托与查看束具，罩持续维持。洪浪中不再交叉双刃；战后武器仍收好，空手接钥匙解锁。',
 'rear_window':'唯一破口位于十字架正后中央高窗，明刃撞击造成宽阔纵向不规则缺口和放射裂纹，外石框与下部窗棂保留。左右窗完整。K1特写展示玻璃冲向镜头的力量，碎片随后落在后墙及刑架后方，避开Claude与前方落脚区；后续不悬浮、不补回玻璃。罩内镜头看不到窗，罩外及撤罩后继续保留中央缺口。后殿拱顶完整。',
 'kimi_fx':'月下模糊剪影与画外咏唱→明刃冲破中央彩窗→插入外缘柴木→循刃瞬移并立即回收、地面气浪向两侧推柴→暗刃扫起深靛不透明月幕并闭合。没有踏月台阶、落脚发光阵纹或插地阵眼。罩外只见有体积的暗壳与局部银边，罩内为无拼缝的暗膜；侧浪高过罩顶，压迫外壳，内景以手掌抵壁与抱护表现承重。危险解除后暗膜散尽，不修复衣服。',
 'support_roles':'Kimi负责明刃定位瞬移、震柴、暗刃护罩、罩内抱护照顾及战后钥匙解锁；GPT负责以巨量水雷灭掉罩外散柴。Perplexity持杖警戒，千问抱护小鱼并保持原扇叶阻击。'
 }
 replacements={old['continuity'][k]:v for k,v in ct.items()}
 def rewrite(v):
  if isinstance(v,str):
   for a,b in replacements.items(): v=v.replace(a,b)
   return v
  if isinstance(v,list): return [rewrite(x) for x in v]
  if isinstance(v,dict): return {k:rewrite(x) for k,x in v.items()}
  return v
 d=rewrite(d);script=rewrite(script)
 d=json.loads(json.dumps(d,ensure_ascii=False).replace('天瀑前干燥；天瀑后湿贴发丝肩背；CY028C随衣料蒸干','入罩前保留汗湿发丝；暗月罩隔绝天瀑直冲，撤罩后仅殿内水雾轻沾衣发；CY028C随衣料蒸干'))
 by={s['id']:s for s in d['shots']}
 spec={
 'CY024K0':('中央窗外，月下剪影','十字架正后中央高窗仍然完整。月光中浮现Kimi模糊的头肩与长发剪影，隔着蓝色彩玻璃看不清面容。画外短咏从窗外传来，她在镜末抬起左手明刃，准备甩入殿内；左右窗没有破损，也没有护罩或阵纹。','远处短咏、殿内火声；末尾压低环境声，给刀锋破窗留反差','仰拍中央高窗，月下模糊剪影与前景刑架形成纵深'),
 'CY024K1':('明刃破窗，玻璃迎面炸开','切中央彩窗的近距离特写。Kimi从窗外甩出的明刃斜向下撞入玻璃，刀锋先顶裂受力点，窗棂局部折断，厚蓝玻璃沿放射裂纹炸开。近处碎片冲过镜头形成速度与纵深，明刃穿过宽阔纵向破口飞向柴堆外缘；外石框和下部窗棂保留，左右窗完整。Kimi本人不穿窗，玻璃随后落在刑架后方与后墙边，避开Claude。','一记硬脆撞击→密集玻璃爆裂→刀锋掠过镜头→碎片坠地尾响','刀刃撞穿玻璃的力量特写，近处碎片与明刃同框'),
 'CY024K1A':('明刃钉柴，瞬移坐标亮起','明刃下尖钉入柴堆前侧外缘的一根乌烬木，木纤维裂开。银光从刀与木头的接触点短促亮起，作为瞬移坐标；刀插在木上，不插地，也不展开保护罩。高柴仍在燃烧，Kimi尚未现身。','刀尖入木的闷硬声、木纤维裂响、短促银光低鸣','外缘柴木与单枚明刃近景，人物暂不入画'),
 'CY024K2':('循刃瞬临，爆气震开柴堆','银光一闪，Kimi在柴堆前侧外缘循明刃瞬移现身，左手握回明刃。她压低重心，气浪沿石面向两侧外下方爆开，将重柴成片推开；木头翻滚、刮地、撞击，Claude与刑架所在的中央保持平静。Kimi双脚落在腾出的石地上，右手暗刃朝外低垂，刀口远离Claude。此时尚未闭罩，残柴在两侧继续燃烧；Claude仍直立受缚，腕踝扣与固定脚托露出。身影只有少量消散的银色余光，不出现第二个身体。','短促瞬移吸气声→低频爆气→重木刮石翻落；不延长成漂浮碎片','低机位中全景，左前Kimi现身，重柴向两侧推出，后方Claude平静留中'),
 'CY024K3':('暗刃挥起，暗月闭合','Kimi退到Claude身前，右手暗刃划出一道向上的弧，深靛月幕从净空石地升起，将两人、刑架和固定脚托完全包住。全部燃木留在外面。关键帧选择刚闭合的罩外视角：只见不透明暗月壳与局部银色边光，不能看见人物或十字架剪影；护罩施放后持续维持，不需要一直手持暗刃。没有地面法阵、悬浮光环或透明球面。','暗刃短扫、低沉闭合声；闭罩瞬间外界火声被隔远','罩外低机位，完整不透明暗月壳与外围散柴'),
 'CY024K4':('罩内试镣，见痛收刀','切入暗月罩内。Kimi从侧下方以右手暗刃轻试Claude腕镣接缝，腕扣细小紫纹反噬，Claude吃痛；她立即把刀退到自己外侧髋边，刃口朝外下，担忧地看锁扣。关键帧停在已经收刀的一刻。确认不能强拆后，她将一明一暗两刃扣回后腰，腾出双手照顾Claude；护罩保持。背景只见暗膜内侧，不透出教堂、烛火或窗。','轻触金属、腕镣短刺鸣、立刻收刀；镜末两声后腰卡扣','罩内近中景，暗刃已退离身体，腕扣残余紫纹与关切眼神'),
 'CY024A1':('抱住她，先让她缓一口气','罩内，Kimi已经收好双刃，空手靠到Claude身前偏左，托住肩背，另一只手轻扶上臂，额侧贴近她的头。Claude仍直立受缚，双腕没有离开横木，只把头轻轻靠向Kimi的肩，缓下一口气。Kimi听向罩外雷声，同时继续托稳她；没有解锁，也没有将她抱离脚托。\\n\\nGPT第二句咏唱从前面的阻击连续接来，至本镜念完，不重复起句。','承前GPT咏唱、衣料轻擦、Claude缓慢呼吸；罩外雷声隔着暗膜传入','罩内贴近双人中景，额侧相贴、托肩背，锁着的双腕保留在画面中'),
 'CY024A2':('拭汗拨发，确认她的状态','Kimi轻轻拨开Claude额前汗湿的发丝，指尖拭去鬓侧汗水；另一只手拨开落在领侧的发梢，查看肩侧衣料焦损与可见皮肤。Claude疲惫地望向她，把头微微靠向触碰。检查不掀衣、不拉扯束具，腕扣仍锁着，焦损衣料没有恢复。暗膜内侧遮住全部外景，柔和冷光托出两人的表情。','连续咏唱与轻缓呼吸、发丝衣料细响，无新增对白','罩内面部与肩侧近景，拭汗、拨发和目光交流'),
 'CY024A4':('蹲下查看踝链','Kimi在脚托旁蹲下，一只空手轻托Claude踝扣上方的小腿，另一只手查看外侧链环与锁扣连接，动作轻，不强拉、不解锁。Claude双腿垂直，双踝仍锁，赤足稳踩十字架立柱上的窄脚托。镜头带到Kimi专注的脸与双手，双刃收在后腰；衣裙自然垂落，原有白金纹样和黑色焦损保持。罩内石地净空，没有燃木和外界窗光。','承前咏唱、轻微链环接触声、短暂停顿；无钥匙声','罩内侧面中近景，Kimi蹲下查看踝链，保留脸、双手与固定脚托'),
 'CY024B3':('巨浪压上暗月','罩外低机位。厚重水墙从左侧扑上最高祭坛，水量压满左半与画面上方，高过整个暗月罩。完全不透明的深靛罩体迎水面被压扁、局部内凹，银色应力纹只在接触区短暂亮起；厚水从罩顶与两侧绕流，外缘散柴被浇灭卷走。人物和十字架不透出来。魔法紫电始终在罩外，随主水势先收尽，接罩内抱护承压。','巨量水体低频轰击、暗膜绷紧声、绕流持续轰鸣','罩外低位广角，巨浪占左侧与顶部，右下不透明暗月承压'),
 'CY027F2':('暗月散尽，接过钥匙','GPT携教主原钥匙来到最高祭坛。确认危险解除，Kimi让暗月罩散尽；双刃早已收在后腰，双手腾出，接过GPT递来的黑铁钥匙。Claude仍直立踩固定脚托，腕踝锁扣未开。身后的中央彩窗破口保留，左右窗完整，所有烛火和散柴都已熄灭，湿石面只有冷月反光。','暗膜低鸣收尽、钥匙落掌、殿内余水滴落；不重复收刃音','战后双人前景交钥匙，Claude受缚与中央破窗在后景')
 }
 for sid,(title,action,sound,framing) in spec.items():
  s=by[sid];before=s['source_quote']
  action=action.replace('\\n','\n')
  assert s['action'] in before,sid
  after=before.replace(s['action'],action)
  assert before in script,sid
  script=script.replace(before,after).replace(s['title'],title)
  s.update(title=title,action=action,source_quote=after,sound=sound,framing=framing,purpose='交代'+title+'的动作与情绪。',cinematic_beats=[dict(offset=0,intent=action.split('。')[0])])
  s['presentation']['visible']=action
 # Keep GPT's established great-water action, replace only altar/ward details.
 s=by['CY024B'];before=s['source_quote'];action=s['action']
 start=action.index('最高祭坛上，');end=action.index('水幕结束前',start)
 action=action[:start]+'最高祭坛上，不透明深靛暗月罩覆盖Kimi、Claude、刑架与脚托，罩外视角不见人物和十字架。厚重侧浪压向暗壳，绕向外侧，浇灭已被瞬移气浪震开的残柴；燃木全在罩外，魔法雷也在罩外偏转。罩不修复衣服，罩内保持无电净空。后殿拱顶完整，正后中央高窗破口保留。'+action[end:]
 action=action.replace('两人银白结界','两人暗月罩').replace('接承压近景','接罩外受压与罩内抱护近景')
 after=before.replace(s['action'],action);assert before in script;script=script.replace(before,after)
 s.update(action=action,source_quote=after,title='宏大水雷，暗月隔绝',cinematic_beats=[dict(offset=0,intent='主水柱轰落下段金罩，侧浪冲上暗月壳')]);s['presentation']['visible']=action
 for sid in ['CY027','CY027A','CY027D']:
  s=by[sid];before=s['source_quote']
  action=s['action'].replace('后墙偏左高窗缺口','正后中央高窗缺口')
  if sid=='CY027D':
   action='听见入口示警，八位同伴在长阶下形成第二道防线，千问仍抱着小鱼。两翼骑士守住柱廊，前排迎向门外教徒。远处最高祭坛的不透明暗月罩持续存在，Kimi在内守着Claude，没有回到队伍；外景看不到二人与刑架。Perplexity持杖警戒，中央高窗破口保留，左右窗完整。'
  else:
   action+=' 最高祭坛仍被不透明暗月罩完整包住，罩外看不到Kimi、Claude和刑架；正后中央窗破口持续存在，左右窗完整。'
  after=before.replace(s['action'],action);assert before in script;script=script.replace(before,after);s.update(action=action,source_quote=after,cinematic_beats=[dict(offset=0,intent=action.split('。')[0])]);s['presentation']['visible']=action
 # Insert one short interior impact response with stable ID.
 n=copy.deepcopy(by['CY024B3']);n.update(id='CY024B3A',title='罩内抱紧，空掌撑住暗膜',seconds=2,dialogue='无对白',dialogue_cues=[],framing='罩内双人中景，抵壁手掌、抱护与受缚脚托同框',purpose='把罩外巨浪的压力落实到Kimi的承重与对Claude的保护。',entry_state='罩外厚水墙压住暗月，Kimi刚由脚托旁起身靠回Claude。',exit_state='暗膜稳住，两人安全，接殿外清水余浪。')
 for k in ['subtitle_cues','time_caption','split_screen_reveal','dialogue_timing_status']: n.pop(k,None)
 n['action']='暗月罩内壁被水压顶出凹痕，Kimi立刻靠回Claude身前，左臂托护她的肩背，右手空掌抵住迎水侧暗膜，双脚压实石地。她咬紧牙关，身体向冲击方向倾斜，仍让Claude把头靠在自己肩侧。Claude直立受缚，腕踝与固定脚托没有松脱。两刃始终在后腰；内景只见不透明暗膜的受压褶皱和局部银纹，看不到外面水墙，也没有水、电或燃木进入。'
 n['sound']='罩外轰鸣被压闷，手掌抵壁的绷紧声、衣料与急促呼吸；没有新增台词'
 n['source_quote']=n['action'];n['cinematic_beats']=[dict(offset=0,intent='内壁压近，靠回抱住'),dict(offset=.6,intent='空掌撑壁，Claude靠肩'),dict(offset=1.5,intent='稳住，接余浪')]
 idx=d['shots'].index(by['CY024B3']);d['shots'].insert(idx+1,n);by[n['id']]=n
 script=script.replace(by['CY024B3']['source_quote'],by['CY024B3']['source_quote']+'\n\n'+n['source_quote'])
 states={
 'CY024K0':('中央高窗完整，Kimi尚在窗外。','窗外剪影抬手，接明刃穿窗。'),
 'CY024K1':('明刃由窗外飞向中央彩窗。','明刃穿入殿内，中央玻璃留下宽阔破口。'),
 'CY024K1A':('明刃离开窗，飞向柴堆外缘。','明刃钉木，瞬移坐标亮起。'),
 'CY024K2':('明刃钉柴，Kimi循刃瞬移。','重柴向两侧散开，明刃回左手，Claude中心平静，尚未闭罩。'),
 'CY024K3':('重柴已让开，Kimi持双刃守在Claude身前。','暗月完全闭合，外景看不到二人；接罩内试镣。'),
 'CY024K4':('罩内Kimi持双刃，Claude仍直立受缚。','不能强拆，双刃收回后腰，空手转为照顾。'),
 'CY024A1':('罩体维持，Kimi双刃已收好，Claude仍受缚。','托抱使Claude缓下一口气，接拭汗拨发。'),
 'CY024A2':('Claude靠近Kimi缓过气，腕扣未开。','拭去汗水，确认焦损与束具状态。'),
 'CY024A4':('罩内安静，双刃已收好。','踝链不能强拆，Kimi准备起身，等待钥匙。'),
 'CY024B3':('巨量侧浪抵达暗月罩。','外壳受压但未破，接罩内抱护。'),
 'CY027F2':('GPT携钥匙到最高祭坛，暗月罩仍在。','暗月撤去，Kimi接钥匙，接先解踝链。')}
 for sid,(a,b) in states.items():by[sid].update(entry_state=a,exit_state=b)
 updates={sid:1 for sid in ['CY024K0','CY024K1','CY024K1A','CY024K2','CY024K3','CY024K4','CY024B','CY024B3','CY024B3A','CY027','CY027A','CY027D','CY028A']}
 updates.update(CY024A1=3,CY024A2=2,CY024A4=3,CY027F2=2)
 requests={}
 for f in sorted((R/REC).glob('*.json')):
  rows=load(f.relative_to(R));rows=rows if isinstance(rows,list) else [rows]
  for row in rows:
   if isinstance(row,dict) and 'prompt' in row:requests[(row['id'],row['rev'])]=(f.relative_to(R).as_posix(),row)
 images=[]
 for sid,rev in updates.items():
  s=by[sid];path=f'{IMG}/{sid}-v045-r{rev}.png';req,row=requests[(sid,rev)]
  prior=s['presentation']['path']
  s['presentation'].update(path=path,visible=s['action'],status='v0.45作者方案修订候选，待画面审阅',missing='静帧已查看；瞬移、接刃、玻璃落地、抱护受力与洪水动态未制作。')
  s['refs']=[dict(path=path,role='本轮修订候选'),dict(path=req,role='实际生成请求')]+([] if sid=='CY024B3A' else [dict(path=prior,role='历史画面保留')])
  s.update(generation_request=req,visual_prompt=row['prompt'],editorial_review=dict(version='v045',status='candidate_pending_author_review',dynamic_execution='pending'))
  with Image.open(R/path) as im:w,h=im.size
  s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0,y=0,w=1,h=1),panel_index=0)
  images.append(dict(id=sid,path=path,sha256=sha(path),size=[w,h],request=req,inputs=[dict(path=q,sha256=sha(q)) for q in row['refs']]))
 # Consistency rules are shared with all revised shots.
 for sid in updates:
  s=by[sid]
  s['invariants']=list(dict.fromkeys(s['invariants']+[ct['claude_shield'],ct['kimi_weapons'],ct['rear_window']]))
 elapsed=0
 for i,s in enumerate(d['shots']):
  s.update(start_second=elapsed,end_second=elapsed+s['seconds']);elapsed+=s['seconds']
  if i+1<len(d['shots']):s['next_link']='接 '+d['shots'][i+1]['id']+'：'+d['shots'][i+1]['entry_state']
 for sc in d['scenes']:
  ss=[s for s in d['shots'] if s['scene']==sc['id']]
  sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)),path=ss[0]['presentation']['path'])
 d.update(version='v0.45',revision='v045',picture_revision='v045',title='《穿云》带图分镜 v0.45 · 暗月瞬临与罩内抱护',subtitle=f'{len(d["shots"])}镜 · {elapsed}秒 · 新图待作者审阅',total_seconds=elapsed,story_script='剧本/穿云-场景剧本-v0.45.md',source_manifest='镜头设计/生成记录/生成索引-v045.json',origin_manifest='镜头设计/shot-plan-v0.42.json',audio_arrangement='后期/暗月瞬临-v045/预演编排.json',review_intro='月下剪影，明刃力量破窗并钉柴，循刃瞬移震开重柴，暗刃闭合不透明月幕。罩内收刃抱托、拭汗、查踝链；罩外巨浪，罩内抱护承压。',review_focus='核对明刃唯一性、中央破窗、罩内外不透明规则、抱护时腕踝仍锁住及固定脚托。新图候选待审；动态、正式特效音未制作，原BGM选择保留。',revision_notes=dict(previous_manifest='镜头设计/shot-plan-v0.42.json',added_ids=['CY024B3A'],modified_image_ids=list(updates),boundary='作者已确认新动作方向；v043/v044讨论候选不进入当前页；17张本轮图待作者画面审阅。'))
 d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
 script=re.sub(r'版本：v0\.42[^\n]*','版本：v0.45｜2026-10-24｜明刃穿窗瞬移、暗月不透明护罩与罩内抱护。新图待审。',script,count=1)
 script=script.replace('## 月相特效连续性 · v0.42','## 暗月瞬临连续性 · v0.45')
 assert all(s['source_quote'] in script for s in d['shots'])
 save(PLAN,d);write(d['story_script'],script)
 save(d['source_manifest'],dict(version='v045',previous_index=old['source_manifest'],generated_images=len(images),images=images,not_used=['v043月引拖柴与v044踏月阵眼方向经讨论退出，未接入当前页','A1r1站姿与砖墙背景退出；A1r2背景修正请求未提交，作者改为抱护','A2r1/A4r1静态插镜改为人物照顾互动','A4r2新增酒红衣纹，r3局部恢复白金纹样','F2r1错误复燃蜡烛，r2全部熄灭'],engine='built-in image_gen',mode='reference edit',transparent_background=False))
else:
 old=load('镜头设计/shot-plan-v0.42.json');d=load(PLAN)
 by={s['id']:s for s in d['shots']}
 images=load(d['source_manifest'])['images']
 spec=d['revision_notes']['modified_image_ids']
 elapsed=d['total_seconds']
a=load(old['audio_arrangement']);a.update(version='v045-picture-sync',previous=old['audio_arrangement'],shot_plan=PLAN,shot_plan_sha256=sha(PLAN))
# CY024B3A inherits M09, which already covers its adjacent shots.
for sid,override in a['shot_overrides'].items():
 if sid in d['revision_notes']['modified_image_ids']:
  override['note']='沿用既有候选；当前动作：'+by[sid]['title']
for sid in d['revision_notes']['modified_image_ids']:a['effects'][sid]=by[sid]['sound']
a['author_feedback']='126个原镜音乐候选、音频文件和本机选曲标记保留；新增CY024B3A沿用相邻候选，不自动标记。新增音效仅设计，未制作音轨。'
save(d['audio_arrangement'],a)
snapshot=R/'镜头设计/带图分镜-月相阵纹-v042.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
t=read('scripts/build_storyboard.py').replace('shot-plan-v0.42.json','shot-plan-v0.45.json')
t=t.replace('"v042")','"v042", "v045")').replace("'v042')","'v042','v045')")
t=t.replace('data.get("revision")=="v042"','data.get("revision") in ("v042","v045")')
write('scripts/build_storyboard.py',t)
write('00_打开项目.html',read('00_打开项目.html').replace('v0.42','v0.45'))
progress='''## 2026-10-24：暗月瞬临与罩内抱护（v0.45，新图待审）

作者最终确认正后中央窗外月下剪影，明刃力量破窗特写、钉入柴堆外缘，Kimi循刃瞬移并回收明刃，向外爆气震柴，再以暗刃展开完全不透明的深靛护罩。v043月引拖柴和v044踏月阵眼候选保留但不进入当前预演。明刃定位、暗刃护罩；试镣吃痛后双刃收后腰，转为托抱、拭汗拨发、查看踝链；新增2秒罩内抱护承压。Claude始终直立受缚、踩固定脚托，解锁仍等原钥匙。罩外不透人物，罩内不见外景，中央破窗与侧窗完整状态同步到战后。

当前127镜420.5秒，17张当前修订图。原126镜对白及BGM候选保留，本机选择不自动扩展；新增镜沿用相邻候选，不替作者选曲。当前预演入口与场景剧本v0.45同步，旧页存为月相阵纹v042。实际提示词/输入哈希、旧候选和局部修正均留存。仅静帧及声音设计说明，未制作动态视频、正式音效或新增配音。

'''
p=read('制作进度.md');pos=p.index('## 2026-10-24：');write('制作进度.md',p[:pos]+progress+p[pos:])
rows=[];selected={x['path'] for x in images}
for f in sorted((R/IMG).glob('*.png')):
 q=f.relative_to(R).as_posix()
 with Image.open(f) as im:size=list(im.size)
 rows.append(dict(path=q,bytes=f.stat().st_size,sha256=sha(q),size=size,status='current_candidate_pending_author_review' if q in selected else 'superseded_preserved'))
save(REC+'/文件核验.json',rows)
print(json.dumps(dict(shots=len(d['shots']),seconds=elapsed,selected_images=len(images),stored_images=len(rows)),ensure_ascii=False))
