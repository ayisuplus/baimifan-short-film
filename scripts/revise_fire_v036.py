"""One-time v0.36 continuity migration. Original shots and media remain intact."""
import copy,json,hashlib,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/火焰伤后与星火-v036'
IMG='镜头设计/图像/火焰伤后与星火-v036'
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,s):(R/p).write_text(s,encoding='utf-8')
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not (R/'镜头设计/shot-plan-v0.36.json').exists(),'One-time migration already applied'
o=json.loads(read('镜头设计/shot-plan-v0.35.json'));d=copy.deepcopy(o);by={s['id']:s for s in d['shots']}
script=read(o['story_script']);changed=set()
def ch(sid,passage=None,**kw):
 global script
 s=by[sid]
 if passage is not None:
  old=s['source_quote'];assert script.count(old)==1,(sid,script.count(old));script=script.replace(old,passage,1);s['source_quote']=passage
 s.update(kw);changed.add(sid)
damage='Claude两侧外袖蕾丝边、外裙下缘和头纱尾端保留固定焦黑缺口，内层衣料完整遮蔽、原服装主色与胸腹纹样保留。灭火后至离殿均苍白无力、唇色淡，无羞红色块或红线；火光只作局部边光。月辉阻止后续伤害，不修衣；蒸干只去水，不修复焦损。数日后街市为已休养并更换清洁衣物。'
fire='乌烬木引燃后，黑色焰芯与暗紫焰边向中间连成连续火海，远景完全遮蔽Claude；近景从前后火舌的缝隙看见她痛苦挣扎和已烧焦的衣边。不能把火分列两侧给她留展示空位。CY024入场即由Kimi贴身月辉阻止继续伤害，身体外烈火仍包围并遮挡；水雷随后扑灭全部祭薪。最后星火点燃空木架为橙金色，脚边乌烬木不复燃。'
ch('CY022',by['CY022']['source_quote']+' 黑焰不是缓慢的小火苗：教主收回火把后，焰浪迅速连成一片，向刑架中央上卷。',action='橙色火把点燃乌烬木，黑焰迅速向中央连片上卷；此镜仍为点火起始局部。')
ch('CY022B','黑焰猛地从下方卷起。切到火中的Claude面肩特写：前后火舌包围她，胸以下与部分肩袖被厚重黑焰遮住，脸从火隙中短暂显露。她咬牙、流泪，肩背向后绷紧，手腕被镣铐截住，漏出痛苦喘息；外袖蕾丝边和头纱尾端已经焦黑破损，面颊沾少量烟灰。没有皮肤灼毁的画面。',title='火隙中的痛苦',framing='火中面肩特写／前景烈焰遮挡',action='火舌从前后包围并遮住胸肩，Claude痛苦挣扎，袖边焦损可见，腕链绷紧。',exit_state='火海持续，切远景只见烈焰与群体吟唱。')
ch('CY022B2','镜头拉开到教堂大景。教徒围着长阶和祭坛吟唱，教主立在下段，小鱼倒在阶下。最高石台上的乌烬木已连成高耸翻卷的黑焰火海，Claude全身与面孔都被遮住，只偶尔露出十字架上端；火没有向教徒或楼梯扩散。普通火盆仍是橙色，群体吟唱压住火中喘息。',title='黑焰吞没祭坛',action='远景用连续黑焰完全遮住Claude；教徒环列吟唱，普通火盆保持橙色。',exit_state='火海与吟唱持续，切门外骑士列队。')
ch('CY024A2','Kimi入场时已送到的银白月辉紧贴Claude的肩袖，受热处短暂显形。斜侧近景透过前后翻卷的黑焰，看见她苍白、汗湿的脸和焦损的袖边；火仍覆盖前景及身体大部，不因护持而自动退成两侧小火。薄月辉隔开继续逼近的热焰，她艰难缓回一口气。已经烧坏的衣料没有恢复，衣外祭薪仍在燃烧。',title='火海中的薄月辉',framing='胸肩斜侧近景／从火隙看脸与受热护辉',action='黑焰包围遮挡，贴身银白月辉在接触点亮起，Claude喘息稍缓；焦损保留。',exit_state='人物被护住但火海未灭，接水滴合流。')
ch('CY024A4','切脚托、踝链与裙边局部。黑焰充满前景并遮住大半脚托，只从火隙看到已经焦黑、参差缺损的外层裙摆和仍受缚的赤足。银白月辉沿衣边薄薄亮起，隔开新的焰尖；脚托与祭薪在保护外，身体内层衣料保持遮蔽。',title='焦损裙边，月辉隔焰',action='高火遮挡前景，火隙显示焦边缺口与薄月辉，火焰尚未熄灭。')
ch('CY024B',by['CY024B']['source_quote']+' 水势压灭整片黑焰后，Claude焦损的裙边才重新露出；月辉不修复衣物。')
ch('CY028B','束具已全部解除。Claude站在GPT身侧，垂下的手指轻轻发颤；指尖只有两三粒暗淡橙金光屑向内聚拢，没有完整火焰，更没有可飞出的火种。湿袖焦黑的边缘仍在滴水。她在此开始同一段咏唱，声音跨切下一镜。\n\n**Claude：**\n沉睡于灰烬中',title='起咏，微光初聚',action='指尖仅有极少暗淡光屑初聚，Claude从这里起咏；没有成熟火种。',entry_state='解锁后确认小鱼安全，衣料仍湿且焦损。',exit_state='初蓄不熄灭，开句跨切裙边水汽。')
ch('CY028C','咏唱的尾半句跨切Claude裙边。初蓄力量带出少量热息，湿衣与头纱的水汽轻轻升起；焦黑缺口仍清楚保留，蒸干不使衣物复原。赤足踩在平整平台，内层衣料保持遮蔽；暖流托起带焦边的纱尾。\n\n**Claude（画外，接上句）：**\n的微光啊，',title='微光余温，蒸散水汽',action='起咏初蓄带出热息蒸去水汽，固定焦损保留；不是另施一段火法。',entry_state='指尖初蓄、首句还没念完。',exit_state='衣料蒸干，初蓄保持；父亲呼唤使她短暂停声。')
ch('CY029',by['CY029']['source_quote']+'\n\nClaude的咏唱停在换气处，目光转向父亲。画外手中初蓄微光仍在，没有熄灭或重新起法。')
ch('CY029E',by['CY029E']['source_quote']+' Claude静默看着他，随后选择继续；这段停顿不重念已经说出的咒语。',sound='“过来”的尾音消散，留下呼吸与滴水声；Claude暂歇，初蓄保持。')
ch('CY029E1','Claude移开看向父亲的目光，转向空刑架。苍白的面颊没有红晕，唇色浅，疲惫的眼神仍坚持。她续上刚才被打断的咏唱，没有重新起句；手中的微光继续汇聚。\n\n**Claude：**\n回应我的呼唤。',title='停顿后，仍选择继续',action='Claude苍白地移开视线、续咒，手中初蓄不曾熄灭。')
ch('CY029E2','切教主。他听见女儿继续咏唱，原本伸向她的手慢慢僵住，指尖落下；眼神由挽留转为惊疑。他没有再开口，Claude的声音从画外继续。\n\n**Claude（画外）：**\n循着尚未散去的余温，',action='教主发现Claude没有回头，伸手僵住；画外咏唱继续。')
ch('CY029E3','切Claude手腕与指节。浅浅束具压痕仍在，焦黑袖口没有恢复。她用左手稳住发颤的右腕；指间的光屑已经凝成一枚有稳定焰芯的小小橙金火种。短焰舌轻轻摇动，火种仍停在指间尚未释放，不再重复初蓄微光的状态。\n\n**Claude（画外）：**\n在我掌心，',title='指间火种已经成形',action='左手托右腕；一枚橙金小火种已有稳定焰芯，停在指间未离手。',entry_state='同一份力量持续汇聚，手腕颤抖。',exit_state='火种成形并维持，切小鱼反应，不再回退为光点。')
ch('CY029E4','切千问怀里的DeepSeek。小鱼抬头望向祭坛上的Claude，听见她艰难却坚持的声音，攥紧千问衣襟，嘴唇轻轻抿住。千问的左臂始终稳稳托着她；空刑架尚未燃起，画外那枚火种仍在Claude指间维持。\n\n**Claude（画外）：**\n再燃一次——',action='小鱼攥紧衣襟望向Claude；画外咏唱续至命名前，已成火种维持。')
ch('CY029B1','切回Claude指尖，她轻轻吐出法术名字。\n\n**Claude：**\n星火。\n\n刚才已经成形的同一枚橙金火种随指尖轻送离开，与手之间拉开空气间隙；此处只释放，不再次凝种。她松开支撑右腕的左手，手指放松，不再输出火焰。焦损袖口和头纱仍在，脚边乌烬木保持熄灭。',action='念出星火，送出已在E3成形的同一枚火种；支撑手放松，无持续喷火。',entry_state='火种已经成形，仍在指间。',exit_state='单枚火种离手，接火种第一视角。')
parts={'CY028B':'沉睡于灰烬中','CY028C':'的微光啊，','CY029E1':'回应我的呼唤。','CY029E2':'循着尚未散去的余温，','CY029E3':'在我掌心，','CY029E4':'再燃一次——','CY029B1':'星火。'}
for sid,text in parts.items():
 s=by[sid];s['dialogue']='Claude：'+text;s['subtitle_cues']=[dict(speaker='Claude',text=text,offset=0,duration=s['seconds'])];s['dialogue_cues']=[]
 s['sound']='同一段Claude咏唱，只念本镜对应词段；028B/C首句跨切，029/E父亲呼唤时有意停声，E1续接不重念。薄弦与呼吸轻托，正式人声未制作。'
 s['dialogue_timing_status']='provisional_subtitles_pending_voice_readthrough'
affected=['CY022B','CY022B2','CY024A2','CY024A4','CY024B','CY027F1','CY027G','CY028A','CY028B','CY028C','CY029','CY029E1','CY029E3','CY029B1','CY029B','CY029C','CY029D','CY028','CY029A','CY030']
for sid in affected:
 s=by[sid]
 s['invariants']=[x.replace('Claude的自然羞红保留。','Claude苍白无力、无羞红。').replace('衣料完整','衣料焦损持续').replace('皮肤、头纱和衣裙仍完整','皮肤不表现灼毁，头纱和衣裙边缘保留焦损') for x in s['invariants']]
 s['invariants'].append(damage)
 if sid not in ['CY022B','CY022B2','CY024A2','CY024A4']:s['action']+=' Claude衣边焦损持续，脸出镜时苍白无羞红。'
 changed.add(sid)
for a,b in zip(['CY028A2','CY028B','CY028C','CY029','CY029E','CY029E1','CY029E2','CY029E3','CY029E4','CY029B1'],['CY028B','CY028C','CY029','CY029E','CY029E1','CY029E2','CY029E3','CY029E4','CY029B1','CY029B2']):by[a]['next_link']='接'+b+'：'+by[b]['title']+'；初蓄—成形—释放单向推进，父亲呼唤处有意停声。'
d['continuity']['ritual_fire']=fire;d['continuity']['claude_damage']=damage
d['continuity']['star_spell']='CY028B起咏初蓄→C热息蒸干→029/E父亲呼唤短暂停声但初蓄不熄→E1续咒→E2教主反应→E3指间成形→E4小鱼反应、火种维持→B1命名并释放→B2主观飞行→B空架燃起。咏唱与换气预算22秒，父亲插入6秒，片段总28秒，全文只念一次。'
d['star_incantation'].update(sequence=list(parts),seconds=22,interruption_ids=['CY029','CY029E'],interruption_seconds=6,sequence_elapsed_seconds=28,status='已采用原全文，本轮前移起咏与调整切镜；待实际试读',voice='全文一遍；首句跨028B/C，父亲呼唤时停声6秒（含反应），E1从下一句续上。',music='首句微光配稀薄持续音；父亲呼唤处音乐压低，E1继续细弦，E3成形配轻单音，B1命名送出留微小火声。')
# Replace obsolete current rules without touching historical files.
oldrule=o['continuity']['ritual_fire'];script=script.replace(oldrule,fire)
script=script.replace('星火咏唱分配：Claude起咒4秒、教主反应4秒、手腕局部3秒、小鱼反应4秒、指尖命名释放3秒，共18秒；人声连续跨镜。','星火咏唱从CY028B开始：B/C各2秒共用首句；父亲呼唤及反应6秒有意停声；E1续句4秒、E2教主反应4秒、E3火种成形3秒、E4小鱼反应4秒、B1命名释放3秒。咏唱与换气22秒，片段共28秒，全文一遍。')
script=script.replace('Claude羞红保留','Claude伤后苍白、无羞红（v0.36作者新决定覆盖旧备注）')
script=script.replace('版本：v0.35','版本：v0.36',1)
script=script.replace('## 乌烬木与星火 · v0.35','## 伤后状态与星火 · v0.36\n\n'+damage+'\n\n## 乌烬木与星火 · v0.36',1)
rows=json.loads(read(REC+'/输出映射.json'));records=[]
for row in rows:
 sid=row['id'];dest=row['destination'];req=f"{REC}/{sid}-请求-v{row.get('attempt',1):03}.json";spec=json.loads(read(req));s=by[sid];old=s['presentation']['path'];w,h=Image.open(R/dest).size
 records.append(dict(shot_id=sid,original=row['source'],destination=dest,sha256=sha(R/dest),request=req,inputs=[dict(path=p,sha256=sha(p)) for p in spec['referenced_image_paths']],status='candidate_pending_author_review' if row.get('active',True) else 'rejected_orange_ritual_flame'))
 if not row.get('active',True):continue
 s.update(presentation=dict(path=dest,role='action',visible=s['action'],status='v0.36新静帧候选，待作者审阅',missing='静帧已查看；动态火势、手势、声音与切点待制作。',show_as_main=True),page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0.,y=0.,w=1.,h=1.),generation_request=req,visual_prompt=spec['prompt'],refs=[dict(path=dest,role='本轮候选'),dict(path=req,role='冻结输入'),dict(path=old,role='保留的历史图')]);changed.add(sid)
for sid in changed:by[sid]['editorial_review']=dict(version='v036',status='candidate_pending_author_review',dynamic_execution='pending')
d.update(version='v0.36',revision='v036',title='《穿云》带图分镜 v0.36 · 火海、伤后与星火推进',subtitle='火海遮蔽 · 固定衣损 · 苍白虚弱 · 初蓄到成形',story_script='剧本/穿云-场景剧本-v0.36.md',source_manifest='镜头设计/生成记录/生成索引-v036.json',review_intro='火海遮住Claude，近景从火隙看痛苦；袖口裙摆焦损持续，救后苍白无羞红；028B起咏初蓄、E3成形、B1只释放。114镜379秒不变，新候选待审。',review_focus='火海覆盖与近景痛苦、焦损跨镜不复原、救后苍白、星火起咏和成形阶段分离。')
d['revision_notes']=dict(previous_manifest='镜头设计/shot-plan-v0.35.json',previous_html='镜头设计/带图分镜-v0.35.html',added_ids=[],modified_ids=sorted(changed),boundary='镜数顺序时长不变；GPT咏唱及扇叶动作不变；星火原词只念一遍，起点前移。')
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']];sc['pages']=list(dict.fromkeys(s['presentation']['path'] for s in ss));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
d['continuity']['rescue_expression']='GPT救援段温柔沉稳、不羞红；Claude受火后至离殿苍白虚弱、唇色淡，无羞红色块或红线。'
script=script.replace('王座、乌烬木黑焰、局部揭示登场、殿内水珠、水雷融合、外院增援与星火18秒跨镜咏唱。','火海遮蔽、持续衣损、伤后苍白；星火从028B起咏至E3成形，22秒咏唱与换气加6秒父亲插入。',1).replace('她慢慢移开目光，回望空十字架。身侧的 ChatGPT 安静守着她。','她仍望着空刑架，身侧的ChatGPT安静守着她。')
for rec in records:rec['request_sha256']=sha(R/rec['request'])
write(d['story_script'],script);save('镜头设计/shot-plan-v0.36.json',d);save(d['source_manifest'],dict(version='v036',previous_index=o['source_manifest'],records=records))
shutil.copy2(R/'镜头设计/带图分镜.html',R/'镜头设计/带图分镜-v0.35.html')
p='scripts/build_storyboard.py';s=read(p).replace('shot-plan-v0.35.json','shot-plan-v0.36.json').replace('"v035")','"v035", "v036")').replace("'v035')","'v035','v036')");write(p,s)
p='00_打开项目.html';write(p,read(p).replace('v0.35','v0.36'))
p='制作进度.md';s=read(p);header='## 2026-10-23：火海、衣损与星火阶段（v0.36）\n\n作者指出祭坛火未覆盖Claude、受火后服装完好及救后脸红穿帮，要求028B起咏初蓄、029E3已成形。本轮修订[剧本v0.36](剧本/穿云-场景剧本-v0.36.md)及[带图分镜](镜头设计/带图分镜.html)：远景连续黑焰遮住人物，近景穿火看挣扎；固定袖边、裙边与纱尾焦损贯穿离殿，救后苍白无羞红。月辉只防新增损伤，蒸干不修复衣物。\n\n星火全文不改，028B/C首句，父亲呼唤时短暂停声，E1续咒、E3已成形、B1只释放。22秒咏唱/换气预算加6秒父亲插入，原28秒片段不延长。114镜379秒（6分19秒）保持。19张内置imagegen候选，原图与旧版保留；未制作新声音或视频。见[复核记录](镜头设计/生成记录/火焰伤后与星火-v036/复核记录.md)。\n\n';s=s.replace('## 2026-10-23：黑焰、入场与星火（v0.35）',header+'## 2026-10-23：黑焰、入场与星火（v0.35）',1) if '## 2026-10-23：黑焰、入场与星火（v0.35）' in s else s.replace('## 2026-10-23：黑焰、入场、门外增援与星火（v0.35）',header+'## 2026-10-23：黑焰、入场、门外增援与星火（v0.35）',1);write(p,s)
print('v0.36 prepared:114 shots,379 seconds,19 image edits')
