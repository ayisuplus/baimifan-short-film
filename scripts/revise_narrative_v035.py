"""Apply author-approved narrative and shot continuity refinements, keeping v0.34 intact."""
import copy,json,hashlib,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/末轮叙事优化-v035';IMG='镜头设计/图像/末轮叙事优化-v035'
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,s):(R/p).write_text(s,encoding='utf-8')
def save(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not (R/'镜头设计/shot-plan-v0.35.json').exists()
o=json.loads(read('镜头设计/shot-plan-v0.34.json'));d=copy.deepcopy(o);by={s['id']:s for s in d['shots']}
script=read(o['story_script']);changed=set()
def change(sid,passage=None,**kw):
    global script
    q=by[sid]
    if passage is not None:
        prev=q['source_quote'];assert script.count(prev)==1,(sid,script.count(prev))
        script=script.replace(prev,passage,1);q['source_quote']=passage
    q.update(kw);changed.add(sid)
def new(sid,after,seconds,title,framing,passage,action,dialogue='无对白',speaker=None,text=None):
    global script
    base=copy.deepcopy(by[after])
    for k in ['cinematic_beats','time_caption','split_screen_reveal']:base.pop(k,None)
    base.update(id=sid,seconds=seconds,title=title,framing=framing,source_quote=passage,action=action,purpose=title,entry_state='承接上一镜的动作与视线。',exit_state='接下一镜，人物位置与身体状态连续。',dialogue=dialogue,dialogue_cues=[],subtitle_cues=[],sound='环境声与跨镜声音连续；尚未制作正式声音。',invariants=['角色服饰、既定站位与持物连续；Kimi维持护持、千问托抱小鱼。'] if sid=='CY027D0' else ['Claude已解缚并蒸干衣料，教主仍倒地，千问托抱小鱼。','星火咏唱一条人声跨镜连续；空刑架未重新燃烧。'],asset_ids=['ENV-CHURCH'])
    if text:base['subtitle_cues']=[dict(speaker=speaker,text=text,offset=0,duration=seconds)]
    script=script.replace(by[after]['source_quote'],by[after]['source_quote']+'\n\n'+passage,1)
    d['shots'].insert(d['shots'].index(by[after])+1,base);by[sid]=base;changed.add(sid)
change('CY009A',by['CY009A']['source_quote']+' 王座沿长殿轴线朝向出口，延续金色尖拱镂空靠背、宽弧形侧背和白坐垫；两扶手、座面与落地基座在侧后方透视中相互连接，不另造一把高椅。',action='修正近端王座透视与支撑；GPT站在座前，目送小鱼穿过长殿出口。')
fire_rule='祭薪为乌烬木，未点燃时是深色致密木料；遇火后黑色焰芯、暗紫细边的火舌迅速上长。火势主要向身体两侧攀升，热浪使Claude痛苦挣扎；不表现皮肤灼毁或衣裙烧穿。普通火盆和蜡烛仍是橙色。Kimi入场后立即隔开逼近身体的热焰，水雷仍可直接浇灭护辉外的乌烬木。最后星火仅点燃普通木刑架，橙金火色不改，不复燃脚边祭薪。'
change('CY022','近处，笔直的第二支火把触到刑架底部深黑色的乌烬木。木纹里的树脂裂隙先亮，随即吐出黑色焰芯、暗紫细边的火舌，与火把的橙色火焰形成区别。火势沿祭薪迅速扩开，热浪压向上方的Claude；火把收回，画外下行脚步渐远，教主返回长阶下段。',title='乌烬木，黑焰初起',action='橙色火把引燃深色乌烬木，黑芯紫边的焰舌扩开，教主收手下阶。',entry_state='教主已登顶，乌烬木尚未点燃，Claude仍受缚。',exit_state='特殊祭薪燃起黑焰；下一镜看Claude承受热浪。',sound='木纹骤裂，低沉火焰呼啸开始压住环境声；下阶脚步渐远。')
change('CY022B','热浪猛地顶上来。切Claude面部与肩背近景：她屏住一口气，眼角溢出泪，咬紧牙关，肩背本能地向后缩；双臂的动作被腕镣截住，链条绷紧发出一声锐响。她想抽回手，却没有余地，最后漏出一声压不住的痛苦喘息。黑焰虚焦掠过画面下缘，皮肤、头纱和衣裙仍完整。',title='热浪逼近，挣扎受阻',seconds=3,framing='面肩近景／腕镣与拉紧的链条入画',action='Claude屏息、咬牙，肩背紧绷，试图抽手却被腕镣拉住，痛苦喘息。',entry_state='黑焰开始升高，Kimi尚未到场。',exit_state='挣扎被束具截住；切祭坛大景，吟唱压过喘息。',sound='短促吸气、腕链锐响、受阻的喘息；不补喊叫台词。',next_link='接CY022B2：个体的痛苦被群体吟唱压住。')
change('CY022B2',by['CY022B2']['source_quote'].replace('高处低柴已经燃起','高处乌烬木黑焰已经攀起，暗紫焰边勾出两侧高耸的火舌，Claude困在中间、面部仍可辨认'),action='维持既定群体吟唱与站位，最高祭坛黑焰升高，普通火盆仍橙色。',entry_state='Claude挣扎未能挣脱，教主已下阶。',exit_state='黑焰与吟唱持续，切门外骑士列队。')
change('CY022B1','教堂外，风拉紧蓝金旗帜，大门仍闭，穹顶完整，尚未落雨。低机位先拍白银淡紫圣骑士从镜头两侧越向前方：甲靴踏过石面，前列向左右分开，一部分守住外院两侧通道，其余在正门前列出中央通道。长枪立定，金属碰响依次停下。指挥者此时留在镜头外。',title='甲靴越前，两翼列阵',framing='门前低机位中远景／先拍骑士行动，不露GPT',action='两列骑士从后方越前，分往两翼列队，侧口岗哨转身警戒，中央留空。',entry_state='夜风起，教堂门闭；援军正抵达。',exit_state='中央通道形成，GPT即将从画外迈入。',sound='甲靴齐步由后及前、甲片轻碰；最后两声枪尾触地接下一镜脚步。',next_link='接CY026：军阵先稳住，再揭示指挥者的步伐。')
change('CY026','镜头贴近石面，从侧后方只拍ChatGPT腰部以下。她的一只银白鞋先迈入画面，另一只接着向前；镜头低位跟随，白色裙摆与唯一的白鳞尾掠过两侧骑士的甲靴和枪杆。头脸、肩背与龙翼都在画框上方，暂不完整揭示。她穿过中央通道，走向仍然紧闭的教堂正门；同伴在画外跟随。',title='裙摆先至，迈步向门',framing='腰部以下局部揭示／侧后低机位腿部跟拍',action='只见GPT双腿、银白鞋、裙摆与尾部向前走过列队，头脸始终画外。',entry_state='两翼骑士已列阵，中路留空。',exit_state='GPT来到门前；切门内静默，再踹门揭示全身。',sound='两步清晰鞋跟声，衣料掠动；入场音乐预备声部抬起，不抢踹门重音。',next_link='接CY022C：门内视角听见脚步停下。')
early='说得平稳、短促，不必喊成战斗口号。她们没有停步，Kimi循GPT的视线望向高处Claude，抬起空手转向右侧柱廊；一道细薄月辉立即先抵达Claude的衣袖和裙边，把逼近身体的黑焰隔开。千问奔向小鱼。此刻保护已经起效，后续抬手与月辉近景是维持状态的展示，不能等长咏唱过半才开始救人。'
prev='说得平稳、短促，不必喊成战斗口号。她们没有停步，Kimi循GPT的视线望向高处Claude，抬起空手转向右侧柱廊；千问奔向小鱼。此时只建立救援方向，护盾尚未生成。'
assert prev in script;script=script.replace(prev,early)
change('CY024',action=by['CY024']['action'].replace('此处只布置方向，护盾还未生成','此处已先让细薄月辉抵达Claude衣袖裙边隔开热焰，后续展示持续护持'))
change('CY023A','AI先遣队越过门口后，预留的入口岗哨继续守住门外侧口，其余圣骑士从后方鱼贯入殿，沿两翼柱廊散开。中央主通道留给ChatGPT，岗哨与入殿队不是同一批人同时出现在两处。',action='入口岗哨留守，余队跨过门槛沿两翼柱廊入殿；中央留空。')
script=script.replace('由骑士跟进接入稍早的召集回闪。','由骑士跟进接入稍早的召集回闪。回闪是叙事插入，不计作现场继续焚烧的等待时间；现实中的Kimi保护已经开始。',1)
q=by['CY024A']['source_quote'];q=q.replace('振翼转为缓慢稳定的悬停后，她才抬掌起咏。','殿内潮湿空气凝成大小水珠，从低处和柱边缓缓向上漂浮，绕过振翼的气流，在她身前、身后形成疏密不同的纵深；不是雨向下落，也不从地板抽水。振翼转为缓慢稳定的悬停后，她才抬掌起咏。')
change('CY024A',q,action=by['CY024A']['action']+' 殿内凝结水珠向上漂浮，前中后景分层，不遮挡脸、翼和离地双脚。')
change('CY024A1',by['CY024A1']['source_quote'].replace('银白微光从月牙发出，沿长阶方向斜向上延伸','银白微光从月牙持续送出，维持入场时已抵达Claude的贴身保护'),title='Kimi维持月牙护持',action='Kimi保持抬手月牙，持续向高处Claude送出银白微光；保护早已起效。',entry_state='Kimi入场即开始护持，现切近展示来源。')
q=by['CY024A2']['source_quote'].replace('银白微光从右下方抵达肩侧','入场时已抵达的银白微光从右下方持续送到肩侧').replace('迎向火舌和热浪','迎向黑焰和热浪').replace('脚边低柴','脚边乌烬木祭薪')
change('CY024A2',q,title='黑焰环伺，月辉护身',action='黑焰沿身体两侧攀升，贴身月辉在受热处短暂亮起并隔开焰尖；Claude仍受缚、衣料完整。',entry_state='保护已起效，黑焰持续，现确认月辉只护人。',exit_state='Claude缓回一口气，黑焰未灭；接水珠合滴。')
q=by['CY024A4']['source_quote'].replace('切回Claude脚边的低柴局部：火焰仍在身体外侧翻动','切回Claude脚托和裙边的独立局部近景：乌烬木黑焰在身体外侧高高翻动').replace('火焰尚未熄灭','黑焰尚未熄灭')
change('CY024A4',q,title='黑焰贴近裙边，薄辉隔热',framing='独立脚托与裙边特写／赤足踝链和黑焰同框',action='黑色焰尖逼近裙边，被一线贴身月辉拨开，脚托、祭薪和石台仍在保护之外。',exit_state='黑焰持续但未接触身体；接教主抬眼听雷。')
q=by['CY024B']['source_quote'].replace('少量紫电间歇穿行于水幕内部','主水体旋卷成相互缠绕的液流，紫电沿液流内部的涡旋螺旋穿行；电弧时而被泡沫与厚水膜遮住，时而透过透明折面显现、发生折射，紫光从内部映亮周围气泡和水雾，不在水幕前贴一条完整折线').replace('洪水扑灭十字架下的低柴','洪水扑灭十字架下的乌烬木黑焰')
change('CY024B',q,action='水流与紫电同向旋卷，电弧藏入水层又透出，水雾内部受光；高位俯拍站位不变，主水势灭黑焰，末段紫电先收。')
outer='正门外，外院和侧廊传来密集脚步。镜头从教堂门槛内向外望：两侧回廊里赶来的黑袍教徒在外院汇成半包围，逼近已被踹开的正门。留守的圣骑士收拢到入口两侧，横枪封住门槛，向殿内发出一声示警。这是原本没有参加殿内仪式的外院教徒；被水雷击倒的那批没有重新站起。'
new('CY027D0','CY027E1',3,'外院教徒，围向正门','门槛内向外中远景／骑士前景、回廊敌人中景',outer,'外院教徒从两侧回廊汇聚到门前，岗哨横枪拦住；敌人仍在门外。')
by['CY027D0'].update(entry_state='水雷已退、上空激战；入口岗哨仍在。',exit_state='门外威胁明确，警报传入殿内，接援军转身守门。',sound='雨声中脚步骤密，甲片与长枪碰响，一声无词示警。',next_link='接CY027D反向：援军面向正门作第二道防线。')
change('CY027E1',exit_state='雨声里叠入外院脚步，切门槛外的新敌人。',next_link='接CY027D0：先交代新的敌人从外院来。')
q=by['CY027D']['source_quote'].replace('教堂内，各路 AI 娘沿长阶分层迎敌：','听到入口岗哨示警，教堂内的各路AI娘转向正门，在长阶下形成第二道防线，面对门外赶来的教徒：').replace('两翼圣骑士守住柱廊','留在殿内的两翼圣骑士守住柱廊')
change('CY027D',q,title='转向正门，守住救援通道',entry_state='外院教徒已在正门外聚集，岗哨发出示警。',action=q,exit_state='前排向入口前压支援门槛防线，后排维持救援与护人；接入口交战爆闪。')
script=script.replace('圣骑士在两翼柱廊用长枪压住黑袍，保持救援通道畅通。','门槛岗哨顶住第一波冲击，前排同伴赶到前中殿接应；少数突破门槛的黑袍立即被拦在入口附近，不能凭空出现在后排。',1)
change('CY027E2',by['CY027E2']['source_quote'].replace('窗内与门口交替闪出橙金、紫白魔法火光，几次短促爆闪和闷响带过殿内交战','闪光集中在正门、前中殿与邻近侧窗，几次短促爆闪和闷响带过阻击外院教徒的交战'),action='外景高俯拍，魔法爆闪集中正门和前中殿，带过对外院增援的阻击；后殿救援区不发生混战。')
change('CY027F',by['CY027F']['source_quote'].replace('教主与教徒已经倒地','教主与殿内教徒已经倒地，外院增援也在门口被击退或制服，入口岗哨重新拉开警戒线'),action=by['CY027F']['action'].replace('教主与教徒已经倒地','教主与殿内教徒已经倒地，外院增援被击退或制服，入口防线恢复'))
# Five shots carry one continuous 18-second incantation.
parts=[
('CY029E1','CY029E',4,'余烬中的微光','Claude面肩近景／稳住呼吸','Claude移开看向父亲的目光，转向空刑架。她缓缓吸气，抬起尚在发颤的手。声音很轻，却尽量把字说完整。','沉睡于灰烬中的微光啊，'),
('CY029E2','CY029E1',4,'教主听见她的选择','教主贴地近景／与前次伸手构图区分','切教主。他听见女儿的咏唱，原本伸向她的手慢慢僵住，指尖落下；眼神由挽留转为惊疑。他没有再开口，Claude的声音从画外继续。','回应我的呼唤。'),
('CY029E3','CY029E2',3,'颤抖的手腕','手腕、指节与衣袖局部特写','切Claude手腕与指节。刚解开束缚留下浅浅压痕，手指抖了一下；她用另一只手轻轻稳住手腕，再一点点松开指节。指端只有一粒尚未成形的微光，不是火种已离手。','循着尚未散去的余温，'),
('CY029E4','CY029E3',4,'小鱼攥紧衣襟','千问怀中小鱼反应特写','切千问怀里的DeepSeek。小鱼抬头望向祭坛上的Claude，听见她艰难却坚持的声音，攥紧千问衣襟，嘴唇轻轻抿住。千问的左臂始终稳稳托着她；此刻空刑架尚未燃起。','在我掌心，再燃一次——')]
for sid,after,seconds,title,framing,action,line in parts:
    passage=action+'\n\n**Claude'+('（画外）' if sid!='CY029E1' else '')+'：**\n'+line
    new(sid,after,seconds,title,framing,passage,action,'Claude'+('（画外）：' if sid!='CY029E1' else '：')+line,'Claude',line)
    by[sid]['sound']='Claude同一条虚弱而清楚的咏唱连续跨镜，留自然换气；细弱弦乐逐步起，不使用大招式合唱。'
    by[sid]['dialogue_timing_status']='estimated_cross_cut_voice_pending_readthrough'
change('CY029E',next_link='接CY029E1：父亲挽留后保留停顿，Claude转向空刑架，开始星火咏唱。')
star='切回Claude的指尖。她轻轻吐出法术的名字。\n\n**Claude：**\n星火。\n\n一粒橙金微光凝成小小火种，随她指尖轻送离开，与手之间留出空气间隙。她松开支撑手腕的另一只手，手指放松，不再持续输出火焰。星火只负责引燃空木架，不形成大型火球；头纱与衣料已干，脚边乌烬木仍熄灭。'
change('CY029B1',star,seconds=3,entry_state='四镜咏唱已连续进行15秒，手指已勉强稳住，空架未燃。',action='Claude念“星火”，指尖微光凝成单枚橙金火种并送出，双手随后放松。',dialogue='Claude：星火。',subtitle_cues=[dict(speaker='Claude',text='星火。',offset=0,duration=1.5)],sound='轻声念出法术名；微小燃亮声，后1.5秒留出火种离手和呼吸。',next_link='接CY029B2：最后音节落下，进入火种主观飞行。')
by['CY029E1']['next_link']='接CY029E2：咏唱跨切教主反应。'
by['CY029E2']['next_link']='接CY029E3：咏唱跨切手腕的身体代价。'
by['CY029E3']['next_link']='接CY029E4：咏唱跨切小鱼的担忧。'
by['CY029E4']['next_link']='接CY029B1：回指尖，说出星火，释放。'
d['continuity']['ritual_fire']=fire_rule
d['continuity']['claude_shield']='Kimi在CY024“护住她们”后即开始贴身月光保护；A1/A2展示持续维持与局部显形，不是迟到的初次施法。'+d['continuity']['claude_shield']
d['continuity']['paladins']='CY022B1先遣骑士分列外侧并留岗；CY026GPT局部迈步；破门后023A余队进入两翼，外侧岗哨一直保留。水雷清理殿内仪式教徒，027D0外院另一批教徒聚来，门槛岗哨拦住，027D同伴支援入口第二道防线。Kimi维持月辉、千问抱护不变，027F确认外院敌人被击退或制服。'
d['continuity']['water_volume']='CY024A殿内湿气凝滴向上漂浮，A3仍保留屋顶外水滴特写；两处都不抽干地板。B水与紫电同向旋卷，内部电弧有液体遮挡/折射/体积散射，不用表面贴线；落地及护人边界沿既定规则收尽。'
d['continuity']['star_spell']='CY029E父亲挽留结束→E1Claude起咒→E2教主反应→E3手腕→E4千问怀中小鱼→B1法术名和离手→B2火种主观→B空架橙金大火。咏唱18秒，五镜一条连续人声，仅念一次。小法术指输出规模，不限制跨镜时长。'
d['star_incantation']=dict(text='沉睡于灰烬中的微光啊，回应我的呼唤。循着尚未散去的余温，在我掌心，再燃一次——星火。',sequence=['CY029E1','CY029E2','CY029E3','CY029E4','CY029B1'],seconds=18,status='作者要求多镜头咏唱；本轮扩写候选，待实际试读',music='先留呼吸和雨声，薄弦在教主镜轻入，手部微光接单音，小鱼镜减弱低频；星火音节落下留微小点燃声，不复用GPT大招高潮。',voice='同一条人声连续跨切，只念一次；虚弱但字句清楚。')
# Update image references and freeze output provenance.
rows=json.loads(read(REC+'/输出映射.json'));records=[]
for row in rows:
    sid=row['id'];n=row['attempt'];dest=f'{IMG}/{sid}-v035-r{n}.png';req=f'{REC}/{sid}-请求-v{n:03}.json';spec=json.loads(read(req))
    active=not(sid=='CY027D0' and n==1)
    records.append(dict(shot_id=sid,attempt=n,original=row['source'],destination=dest,sha256=sha(R/dest),request=req,request_sha256=sha(R/req),inputs=[dict(path=p,sha256=sha(p)) for p in spec['referenced_image_paths']],status='candidate_pending_author_review' if active else 'rejected_wrong_opposite_cathedral'))
    if not active:continue
    q=by[sid];oldimage=q['presentation']['path'];w,h=Image.open(R/dest).size
    q.update(presentation=dict(path=dest,role='action',visible=q['action'],status='v0.35新候选，待作者审阅',missing='静帧只表达代表状态；连续动作、表演、运镜、水火雷与声音待动态制作验证。',show_as_main=True),page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0.,y=0.,w=1.,h=1.),generation_request=req,visual_prompt=spec['prompt'],refs=[dict(path=dest,role='本轮候选'),dict(path=req,role='实际输入冻结'),dict(path=oldimage,role='历史图或制作参考，保留')])
    changed.add(sid)
for sid in changed:by[sid]['editorial_review']=dict(version='v035',status='candidate_pending_author_review',dynamic_execution='pending')
d.update(version='v0.35',revision='v035',title='《穿云》带图分镜 v0.35 · 黑焰、入场与星火',subtitle='局部揭示入场 · 黑焰与护持 · 水雷融合 · 门外增援 · 星火跨镜咏唱',story_script='剧本/穿云-场景剧本-v0.35.md',source_manifest='镜头设计/生成记录/生成索引-v035.json')
d['review_intro']='王座透视修订；乌烬木黑焰与痛苦近景，Kimi入场先护持；骑士列队后以GPT腰腿局部登场；殿内水珠上浮与水雷缠绕；外院教徒来袭补齐守门因果；星火扩为18秒五镜咏唱。新图待作者审阅，声音和动态未制作。'
d['revision_notes']=dict(previous_manifest='镜头设计/shot-plan-v0.34.json',previous_html='镜头设计/带图分镜-v0.34.html',added_ids=[s['id'] for s in d['shots'] if s['id'] not in {x['id'] for x in o['shots']}],modified_ids=sorted(changed),boundary='本轮15张当前新图、1张门外空间中间稿；GPT既定长咒语、扇叶上行与换机位不变。全片增加20秒。')
elapsed=0
for s in d['shots']:s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
assert len(d['shots'])==114 and elapsed==379,(len(d['shots']),elapsed)
d['total_seconds']=elapsed
for sc in d['scenes']:
    ss=[s for s in d['shots'] if s['scene']==sc['id']];sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
script=script.replace('版本：v0.34｜2026-10-23｜修正扇叶地面向上飞行方向，飞行极特写与侧面仰拍撞击采用不同机位。','版本：v0.35｜2026-10-23｜王座、乌烬木黑焰、局部揭示登场、殿内水珠、水雷融合、外院增援与星火18秒跨镜咏唱。')
script=script.replace('## 教堂空间与光源 · v0.23','## 乌烬木与星火 · v0.35\n\n'+fire_rule+'\n\n星火咏唱分配：Claude起咒4秒、教主反应4秒、手腕局部3秒、小鱼反应4秒、指尖命名释放3秒，共18秒；人声连续跨镜。\n\n## 教堂空间与光源 · v0.23',1)
write(d['story_script'],script);save('镜头设计/shot-plan-v0.35.json',d)
save(d['source_manifest'],dict(version='v035',previous_index=o['source_manifest'],records=records))
shutil.copy2(R/'镜头设计/带图分镜.html',R/'镜头设计/带图分镜-v0.34.html')
p='scripts/build_storyboard.py';s=read(p).replace('shot-plan-v0.34.json','shot-plan-v0.35.json').replace('"v034")','"v034", "v035")').replace("'v034')","'v034','v035')");write(p,s)
p='00_打开项目.html';s=read(p).replace('v0.34','v0.35').replace('109 镜','114 镜').replace('5 分 59 秒','6 分 19 秒');write(p,s)
p='制作进度.md';s=read(p);header='## 2026-10-23：黑焰、入场、门外增援与星火（v0.35）\n\n已同步[剧本v0.35](剧本/穿云-场景剧本-v0.35.md)及[带图分镜](镜头设计/带图分镜.html)：CY009A修王座；CY022/B/B2/A2/A4同步乌烬木黑焰，B改痛苦近景，A4独立局部；Kimi在入场后即护持。CY022B1骑士先列队、CY026腰腿局部跟拍；CY024A补殿内上浮水珠，B强化水雷内部缠绕。CY027D0补外院教徒逼近门口，D/E2/F同步守门与解除威胁因果。\n\n作者嫌首版短咏唱不足切镜，星火扩为18秒五镜：Claude4、教主4、手腕3、小鱼4、火种3秒，接原主观飞行。四个咏唱反应镜及一处门外镜新增，痛苦镜加1秒、火种镜加1秒；当前114镜379秒（6分19秒），GPT既定咒语及扇叶两镜不变。\n\n内置imagegen制作15张当前候选，门外首版因对面建筑像第二教堂而留作拒绝稿，共16次输出。旧版本、封版与声音保留；静态检查不代替动态与听审，未制作新音视频。见[复核记录](镜头设计/生成记录/末轮叙事优化-v035/复核记录.md)。\n\n'
s=s.replace('## 2026-10-23：扇叶上行',header+'## 2026-10-23：扇叶上行',1);write(p,s)
print('v0.35:114shots379sec,15currentimages16outputs,star chant18sec.')

