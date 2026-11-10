"""One-time v0.33: airborne casting, Qwen single-leaf interception and wing continuity."""
import copy,hashlib,json,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/展翼与扇面-v033'; IMG='镜头设计/图像/展翼与扇叶-v033'
if (R/'镜头设计/shot-plan-v0.33.json').exists():raise SystemExit('v0.33 already exists: do not replay')
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,t):(R/p).write_text(t,encoding='utf-8')
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
old=json.loads(read('镜头设计/shot-plan-v0.32.json'));d=copy.deepcopy(old)
by={s['id']:s for s in d['shots']};ob={s['id']:s for s in old['shots']}
rows=json.loads(read(REC+'/输出映射.json'));records=[];chosen={}
(R/IMG).mkdir(parents=True,exist_ok=True)
for row in rows:
 sid=row['id'];n=row['attempt'];dest=f'{IMG}/{sid}-v033-r{n}.png';req=f'{REC}/{sid}-请求-v{n:03}.json'
 shutil.copy2(row['original'],R/dest);args=json.loads(read(req))
 records.append(dict(shot_id=sid,attempt=n,original=row['original'],destination=dest,sha256=sha(R/dest),request=req,request_sha256=sha(R/req),inputs=[dict(path=p,sha256=sha(p)) for p in args['referenced_image_paths']],status=row['status']))
 if row['status']=='candidate_pending_author_review':chosen[sid]=records[-1]
assert len(chosen)==17
wing='GPT人形原本就有两片淡紫白色膜质龙翼，根部在肩背，独立于手臂、袖子和白鳞尾。站立、扶人、接抱和行走时自然折拢；侧背全身要能读出翼骨或膜面轮廓，头肩近景可被头发遮挡或裁出画面。CY024A展开振翼升空，A5与B持续悬停，CY027降落后收翼；后续完整龙形变身仍保留，不把人形展翼写成第一次变龙。'
flight='GPT在完整穹顶下、靠入口的中殿前部升空，避开高中央吊灯、拱肋和后续主水柱；咏唱与水雷期间始终悬停在主水幕侧前方，水退后降落浅水再向教主走近。教主保持下段中央缓台，Claude仍在最高祭坛受缚；没有隔着完整屋顶直视外部云旋。'
fan='千问在面向祭坛的右侧柱边，以左前臂托小鱼臀腿、孩子贴左胸和胯；右手握原折扇，甩腕射出外缘一枚实体狭长扇叶。扇叶约一条扇褶宽，蓝底花纹、细金刃边，与母扇同材质；不是整把扇、半圆扇面、光刃复制体或多枚飞镖。原扇缺一叶，柄和其余扇叶仍在手中；命中后扇叶落向无人侧廊，不凭空回装。千问合拢余扇收回胸侧、继续护人，不把小鱼交给他人。'
new={}
new['CY024A']='''千问俯身，将小鱼护进怀里。

**千问：**
抱紧我。

小鱼攥住衣襟。千问退向右侧柱，把小鱼托稳在左前臂和左侧胯旁，孩子贴住胸口；右手腾出，摸到腰侧折扇。近旁圣骑士的白银护光挡住柱外，Kimi在同侧后方准备护持Claude。

镜头转向ChatGPT，由低机位全身景随她上升：背后的两片淡紫白色膜翼展开，一次有力的向下扇动扬起尘埃，裙摆与长发随风抬起，双脚清楚离地。她升到完整穹顶下方，避开中央吊灯与拱肋，停在靠入口、主落水区侧前方的高处。振翼转为缓慢稳定的悬停后，她才抬掌起咏。

**ChatGPT：**
盘踞于苍穹尽头，'''
new['CY024A9']='''教主仍在下段中央缓台。他仰头盯住空中的ChatGPT，抬手射出一道暗金术光，沿中央通道斜向上掠去，试图打断咏唱。他没有变身，也未张开护罩。

ChatGPT的第二句咏唱在此接入，声音持续跨过教主出手、千问发射、扇叶伴飞和Kimi护持的切镜；慢镜只改变视觉时间，不拖低或变调咏唱声音。'''
new['CY024A10']='''切千问手边的近景。她听见破空声，左臂仍牢牢托着小鱼，身体挡在孩子外侧；右手展开折扇，朝远离小鱼的方向甩腕。原扇最外侧的一枚狭长实体扇叶从固定处弹脱，带着原来的蓝底花纹和细金刃边飞出。镜头看清扇叶与母扇间的空隙：扇柄及其余扇叶还在她手里，只有外缘少了一叶。'''
new['CY024A11']='''切单枚扇叶的子弹时间特写：镜头沿其侧前方短暂伴飞，再作小幅旋绕，尖端、薄刃和花纹在浅景深里清晰，尘粒近乎凝住。只飞这一枚细长实体扇叶，不能画成整把扇子、半圆扇面或复制出来的光刃。

扇叶斜切进入教主术光与空中ChatGPT之间的拦截点。暗金术光保持从教主朝GPT的世界方向，镜头旋绕只改变观察角度，不让攻击倒飞。刃缘触及术光时恢复正常速度，一声清脆裂响，术光被劈散成两股，偏向无人空处并消失；扇叶随之斜落空侧廊。千问把余扇合拢收回胸侧，左臂始终未松开小鱼。

教主收回被震偏的手，发现两侧骑士已经封住接近路线。掩护仍在画外持续，Kimi继续施法；教主转向判断头顶雷声，逐步改为自保，而不是原地等待。'''
new['CY024A1']=ob['CY024A1']['source_quote'].replace('**ChatGPT（画外）：**','第二句咏唱从前面的阻击连续接来，至本镜念完；不重复起句。\n\n**ChatGPT（画外，跨镜完整句）：**')
new['CY024A2']=ob['CY024A2']['source_quote'].replace('ChatGPT仍在中殿入口方向抬掌蓄势','ChatGPT仍在中殿入口方向的高处振翼悬停、抬掌蓄势')
new['CY024A8']=ob['CY024A8']['source_quote'].replace('紧绷的眉眼第一次露出警觉','阻击失败后的眉眼更加紧绷，开始判断头顶的威胁').replace('衣袍干燥，脚步未动，暗金护罩尚未展开','衣袍干燥，脚步仍留在缓台，抬起另一只手准备护身；暗金护罩尚未展开')
new['CY024A5']=ob['CY024A5']['source_quote'].replace('切回ChatGPT。她抬眼，','切回空中ChatGPT的侧前方中近景。面部和施法手占主体，肩后可见缓慢扇动的膜翼；与升空镜的全身低机位明确区分。她垂眼，').replace('自己仍在靠入口、主落水柱前方的安全位置','自己仍悬停在靠入口、主落水柱侧前方的高处安全位置')
new['CY024B']=ob['CY024B']['source_quote'].replace('苍龙雷渊应声释放，','镜头切到殿内高位，从ChatGPT侧后上方斜俯拍，前景膜翼、中景下坠水雷、远处地面撞击构成清晰纵深。苍龙雷渊应声释放，').replace('ChatGPT在靠入口的一侧；','ChatGPT在靠入口的一侧高空振翼悬停，压掌引流，双脚远离地面，身体与翼尖都避开主水柱；').replace('GPT入口侧水纹把侧浪和雷支流导离自身','GPT在空中引导入口侧水纹，把侧浪和雷支流导离自身')
new['CY027']=ob['CY027']['source_quote'].replace('ChatGPT 从入口方向走近，','ChatGPT从入口侧高处缓缓下降，膜翼轻振制动，一只鞋尖先点入浅水、荡开小圈涟漪，另一只脚随之落稳；她收拢双翼，再从入口方向走近，')
new['CY028A']=ob['CY028A']['source_quote'].replace('ChatGPT 扶住 Claude，等她从固定脚托上迈下。','Kimi收好刚解开的束具，留在刑架旁让出位置。ChatGPT折拢膜翼，扶住Claude，等她从固定脚托上迈下。')
t=read(old['story_script'])
for sid,txt in new.items():
 if sid in ob:
  assert ob[sid]['source_quote'] in t,sid
  t=t.replace(ob[sid]['source_quote'],txt,1);by[sid]['source_quote']=txt
insert='\n\n'.join(new[sid] for sid in ['CY024A9','CY024A10','CY024A11'])
t=t.replace(new['CY024A'],new['CY024A']+'\n\n'+insert,1)
t=t.replace('GPT在下层中殿、千问抱宝宝在侧柱边。','GPT先在中殿升空咏唱、水雷后降落；千问抱宝宝在侧柱边，单手发射一枚扇叶阻击。')
lines=t.splitlines();lines[2]='版本：v0.33｜2026-10-23｜GPT展翼升空、千问单片扇叶阻击与子弹时间、斜俯拍水雷、退水降落及全片漏翼修订。';t='\n'.join(lines)+'\n'
t=t.replace('## 教堂空间与光源 · v0.23','## 龙翼与扇叶连续性 · v0.33\n\n'+wing+'\n\n'+fan+'\n\n## 教堂空间与光源 · v0.23',1)
write('剧本/穿云-场景剧本-v0.33.md',t)
def upd(sid,**kw):by[sid].update(kw)
upd('CY024A',title='展翼离地，空中起咏',seconds=7,framing='低机位全身广景随升／两翼与双脚离地清楚可见',purpose='建立飞行能力、高低距离与咏唱安全位置，千问先抱稳小鱼。',entry_state='回闪结束，GPT仍站中央通道；千问抱小鱼退柱边。',action='千问左臂托稳小鱼、右手腾出；GPT展开两片膜翼，下扇扬尘、双脚离地，避吊灯升至穹顶下方，悬停后才起句。',exit_state='GPT已在主水幕侧前方高空悬停并开始咏唱；教主抬眼。',sound='0—1.1秒千问抱紧我；1.1—4.2秒翼膜低沉振动与尘埃声，低弦起；4.2秒GPT第一句。正式声音未制作。',cinematic_beats=[dict(offset=0,intent='千问抱稳，右手腾出'),dict(offset=1.2,intent='双翼展开下扇，双脚离地'),dict(offset=4.2,intent='悬停后起句')],subtitle_cues=[dict(speaker='千问',text='抱紧我。',offset=0,duration=1.1),dict(speaker='ChatGPT',text='盘踞于苍穹尽头，',offset=4.2,duration=2.7)])
data=[('CY024A9',1,'教主仰射，主动打断','教主腰上近景／朝画面左上方出击','教主抬手射出一道暗金术光，瞄准高处GPT。','教主主动阻止，让长咏唱有对抗。',['CHAR-PRIEST','ENV-CHURCH']),('CY024A10',1,'一枚扇叶弹脱','千问近景／托抱手、持扇手及单叶离扇同框','千问左臂托小鱼、右手甩扇，弹出一枚狭长实体扇叶，原扇柄及其余扇叶仍在手里。','明确暗器来源与孩子持续被承托。',['MULKZI2W5366M','CHAR-DEEPSEEK','ENV-CHURCH']),('CY024A11',2,'单叶伴飞，截断术光','单片狭长扇叶微距／短暂伴飞和小幅旋绕／命中恢复速度','单片实体扇叶短暂慢速旋转，切入术光路径；命中恢复速度，术光裂散偏向空处，叶片斜落无人侧廊。','用可读的暗器轨迹表现千问掩护，慢镜是视觉强调。',['MULKZI2W5366M','CHAR-PRIEST','ENV-CHURCH'])]
for sid,secs,title,framing,action,purpose,assets in data:
 s=dict(id=sid,scene='S05',scene_title=by['CY024A']['scene_title'],title=title,seconds=secs,framing=framing,purpose=purpose,entry_state={'CY024A9':'GPT已经升空起咏，教主仍在下段缓台。','CY024A10':'术光正朝GPT飞去，千问左臂已经托稳小鱼。','CY024A11':'单枚实体扇叶已脱离母扇，暗金术光逼近空中GPT。'}[sid],action=action,exit_state={'CY024A9':'暗金术光斜向空中，切千问截击。','CY024A10':'实体单叶已离扇，余扇在右手，左臂仍托孩子。','CY024A11':'术光被截断，千问收回余扇继续护人，教主准备自保。'}[sid],dialogue='ChatGPT（画外、跨镜）：统御深流与雷鸣的',sound='同一句GPT画外咏唱连续，不因慢镜变速或变调；'+('扇叶命中前低压环境声，命中恢复速度、短促清脆裂响，随后接Kimi月辉细响。' if sid=='CY024A11' else '术光破空声。' if sid=='CY024A9' else '扇叶弹脱的单声金属轻响。'),next_link='',invariants=[wing,flight,fan,'教主术光始终射向高处GPT；单叶只去拦截，不转打教主。单叶无火焰或巨大法阵。'],asset_ids=assets,source_quote=new[sid],priority='normal',dialogue_cues=[],subtitle_cues=[dict(speaker='ChatGPT',text='统御深流与雷鸣的',offset=0,duration=secs)],dialogue_timing_status='estimated_cross_cut_voice_pending_readthrough')
 by[sid]=s
ix=d['shots'].index(by['CY024A'])+1;d['shots'][ix:ix]=[by[sid] for sid in ['CY024A9','CY024A10','CY024A11']]
upd('CY024A1',entry_state='千问的单叶已截住术光，GPT空中咏唱持续，Kimi开始护持。',dialogue='ChatGPT（画外，承前半句）：古老意志啊。',subtitle_cues=[dict(speaker='ChatGPT',text='古老意志啊。',offset=0,duration=3.9)])
by['CY024A1']['cinematic_beats']=[dict(offset=0,intent='第二句后半承前念完，月辉从指尖发出')]
by['CY024A2']['invariants'].append(flight)
upd('CY024A8',entry_state='教主拦截被千问破除，仍在缓台，衣料干燥，屋顶完整。',action='教主收回出击的手，听见闷雷后抬头判断威胁，另一只手准备护身；侧窗紫光掠过脸侧，护罩未展开。',purpose='由阻击失败转为防御，避免教主站着等待。')
upd('CY024A5',framing='空中侧前方中近景／脸、胸前压掌与肩后膜翼',entry_state='GPT在穹顶下主落水区侧前方悬停，Claude月辉与侧柱护光已就位。',action='GPT持续缓慢振翼悬停，垂眼确认保护；胸前收指祈愿，随招式最后一字翻掌压下。',exit_state='空中压掌完成，切殿内高位斜俯拍水雷倾泻。')
upd('CY024B',title='高空俯拍，水雷贯入殿内',seconds=5,framing='殿内高位斜俯拍／GPT侧后上方／膜翼前景与地面落点同框',purpose='同时读出GPT飞行高度、主水幕下坠纵深和地面承受冲击。',entry_state='GPT空中压掌，主水幕侧前方安全区与三处护人位置明确。',action='前景GPT振翼悬停在水柱外，水雷从上缘倾泻穿入中景，落向下方教主暗金罩与地面；清水灭柴，Claude薄月辉受冲才亮，末段紫电先收尽。',exit_state='落水高峰过去，紫电已收尽；下一镜清水余浪掀左后墙长椅。',cinematic_beats=[dict(offset=0,intent='最后渊字接破顶及水雷重音'),dict(offset=1,intent='斜俯拍读出前景翼/中景水/下方落点三层'),dict(offset=3.8,intent='魔法紫电退去，清水余浪延续')])
upd('CY027',title='退水降落，收翼走近',seconds=4,framing='低位中远景／鞋尖落浅水与收翼动作可见',entry_state='紫电与水幕结束，GPT仍在入口侧高空，浅水正在退去。',action='GPT振翼制动下降，鞋尖点水，另一只脚落稳，双翼收拢后走向原缓台上的教主。',exit_state='GPT已落地收翼，与教主隔短阶对视，接条约质问。',sound='水声退低，最后一次翼膜拍动，鞋尖水声与湿地脚步；不新增对白。')
upd('CY028A',action=by['CY028A']['action'].replace('Perplexity','Kimi')+' Kimi收好束具让开，GPT折翼扶人。')
by['CY028A']['asset_ids']=list(dict.fromkeys([x for x in by['CY028A']['asset_ids'] if x!='MULKZI2W3JZ5F']+['MULKZI2WMFNJE']))
# Current narrative fields only; frozen historic prompts/refs retain original versions.
for s in d['shots']:
 s['invariants']=[v.replace('GPT在下层中殿、千问抱宝宝在侧柱边。','GPT先升空咏唱、水雷后降落；千问在侧柱边抱护小鱼并单手发射扇叶阻击。') for v in s.get('invariants',[])]
 if 'CHAR-GPT' in s.get('asset_ids',[]) or s['id'] in chosen:s['invariants'].append(wing)
 if s['id'].startswith('CY024A') or s['id']=='CY024B':s['invariants'].append(flight)
for sid,rec in chosen.items():
 s=by[sid];p=rec['destination'];req=rec['request']
 with Image.open(R/p) as im:w,h=im.size
 vis=s['action']
 if sid in ['CY026','CY026B','CY027F','CY027G','CY028A','CY029B','CY029C','CY029D','CY028','CY030']:vis=ob[sid]['presentation']['visible']+' GPT原有膜翼已补入，站立或扶抱时折拢。'+('左侧解锁同伴已同步为Kimi。' if sid=='CY028A' else '')
 if sid=='CY024A':vis='GPT全身升空代表状态：两膜翼展开、双脚离地，未破屋顶。千问抱稳动作在画外。'
 if sid=='CY024A11':vis='单片细长实体扇叶在术光前的伴飞代表状态，尚未碰撞。'
 if sid=='CY027':vis='鞋尖初触浅水、两翼尚在制动的降落代表状态；收翼与走近待动态。'
 missing='静帧只表达代表状态；连续动作、咏唱、音效与动态切点待制作。'
 if sid=='CY024A11':missing='弹脱、旋转、撞击、术光分流和叶片落点须动态验证；静帧不证明命中。'
 s.update(presentation=dict(path=p,role='action',visible=vis,status='v0.33新静帧候选，待作者审阅',missing=missing,show_as_main=True),page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0.,y=0.,w=1.,h=1.),panel_index=0,generation_request=req,visual_prompt=json.loads(read(req))['prompt'],refs=[dict(path=p,role='本轮新静帧候选'),dict(path=req,role='冻结实际输入')]+([dict(path=ob[sid]['presentation']['path'],role='保留的旧版画面')] if sid in ob else []),editorial_review=dict(version='v033',status='candidate_pending_author_review',dynamic_execution='pending'))
 if sid in ['CY026','CY026B','CY027F','CY027G','CY028A','CY029B','CY029C','CY029D','CY028','CY030','CY024A','CY024A5','CY024B','CY027']:s['refs'].append(dict(path='资产/图像/四视图/CHAR-GPT-TURN-v001.png',role='原有膜翼造型参考'))
seq=['CY024A','CY024A9','CY024A10','CY024A11','CY024A1','CY024A2','CY024A3','CY024A6','CY024A7','CY024A4','CY024A8','CY024A5','CY024B','CY024B1','CY027','CY027A']
for a,b in zip(seq,seq[1:]):by[a]['next_link']='接'+b+'：'+by[b]['entry_state']
for k,v in d['continuity'].items():
 if isinstance(v,str):d['continuity'][k]=v.replace('GPT在下层中殿、千问抱宝宝在侧柱边。','GPT先升空咏唱、水雷后降落；千问在侧柱边抱护小鱼并单手发射扇叶阻击。')
d['continuity'].update(gpt_wings=wing,gpt_flight=flight,qwen_fan_intercept=fan,casting_cover='教主主动向高空出击→千问单枚扇叶截断→骑士封住接近路线并在画外保持掩护→教主听雷转防御。Perplexity不参与本次阻击。',bullet_time='只在单片实体扇叶离扇到命中前减速，命中恢复常速；咏唱独立连续。术光世界轨迹始终教主→GPT，摄影机绕扇叶不改变该方向。')
d.update(version='v0.33',revision='v033',created='2026-10-23',title='《穿云》带图分镜 v0.33 · 展翼与扇叶',subtitle='展翼升空 · 单叶暗器阻击 · 殿内俯拍水雷',story_script='剧本/穿云-场景剧本-v0.33.md',origin_manifest='镜头设计/shot-plan-v0.32.json',source_manifest='镜头设计/生成记录/生成索引-v033.json')
d['review_intro']='作者确认GPT升空咏唱与斜俯拍水雷，千问托抱小鱼、发射一枚实体扇叶阻击；已纠正整扇面光刃误解。A/A5独立构图；退水补降落，十处旧图补折翼，扶稳镜同步Kimi。新图为候选，实际动作与声音未制作。'
d['review_focus']='看左臂抱稳/右手单叶脱扇→子弹时间截术光→Kimi护持→GPT空中收咒→斜俯拍水雷→浅水降落；全片翼根、翼膜、袖子和尾巴要分清。'
d['revision_notes']=dict(previous_manifest='镜头设计/shot-plan-v0.32.json',previous_html='镜头设计/带图分镜-v0.32.html',added_ids=['CY024A9','CY024A10','CY024A11'],modified_ids=list(dict.fromkeys(list(new)+list(chosen))),boundary='既定咒语全文不改，新增动作与局部时长；17张当前候选，5张中间稿保留。原封版及旧版本原件保持。')
d['music_direction'].update(sequence=seq[:-2],estimated_spell_sequence_seconds=50,estimated_gpt_incantation_seconds=45.8,rule='千问抱紧我→展翼低鼓/风声→GPT悬停起咏；第二句跨教主出击、千问弹叶、单叶子弹时间与Kimi护持连续念出。慢镜压低环境、咏唱不变速，命中恢复音效。水珠/云旋/紫电/救赎句原节奏延续，收声0.8秒后渊字接落水重音。正式音乐音效尚未制作。',incantation_bridge=dict(ids=['CY024A9','CY024A10','CY024A11','CY024A1'],text='统御深流与雷鸣的古老意志啊。',seconds=8,rule='前半句4秒跨三镜，后半句4秒在Kimi镜收尾，只念一次。'))
elapsed=0
for s in d['shots']:s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
d['total_seconds']=elapsed
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']];sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
assert len(d['shots'])==108 and elapsed==358
assert by['CY024A']['presentation']['path']!=by['CY024A5']['presentation']['path']
assert d['music_direction']['approved_incantation']==old['music_direction']['approved_incantation']
for s in d['shots']:assert s['source_quote'] in t,s['id']
save('镜头设计/shot-plan-v0.33.json',d)
save('镜头设计/生成记录/生成索引-v033.json',dict(version='v033',previous_index='镜头设计/生成记录/生成索引-v032.json',records=records,review=REC+'/复核记录.md'))
snap=R/'镜头设计/带图分镜-v0.32.html'
if not snap.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snap)
p='scripts/build_storyboard.py';write(p,read(p).replace('shot-plan-v0.32.json','shot-plan-v0.33.json').replace('"v032")','"v032", "v033")').replace("'v032')","'v032','v033')"))
p='00_打开项目.html';x=read(p).replace('v0.32','v0.33').replace('105 镜','108 镜').replace('5 分 49 秒','5 分 58 秒').replace('护人及长吟唱43秒','护人、升空及咏唱50秒').replace('镜头设计/图像/火种慢镜-v026/CY029B-v026-r1.png',chosen['CY029B']['destination'])
x=x.replace('<a href="镜头设计/带图分镜.html#CY024A6">','<a href="镜头设计/带图分镜.html#CY024A">本轮：展翼升空与单叶阻击<small>千问单片实体扇叶 · 子弹时间 · GPT空中收咒 · 斜俯拍水雷 · 退水降落</small></a>\n<a href="镜头设计/带图分镜.html#CY024A6">',1)
write(p,x)
p='制作进度.md';x=read(p);i=x.index('## ')
write(p,x[:i]+'''## 2026-10-23：展翼升空、单片扇叶阻击与俯拍水雷（v0.33）

作者确认升空/阻击/俯拍方案，并进一步纠正千问发射的是单片实体扇叶、不是整扇面光刃。已同步[剧本v0.33](剧本/穿云-场景剧本-v0.33.md)及[带图分镜](镜头设计/带图分镜.html)。CY024A低机位全身展翼升空，CY024A5独立空中收咒近景，CY024B殿内高位斜俯拍水雷落点，CY027鞋尖触水后收翼走近。

新增CY024A9教主主动出击、CY024A10千问左臂托抱/右手弹出单叶、CY024A11单叶子弹时间截击，共4秒；咏唱第二句连续跨切，不随画面慢放变调。千问母扇留在手里缺一叶，实体扇叶命中术光后落向无人侧廊，不回装。Perplexity不承担阻击，Kimi护持职责保持。

全片105镜逐镜检查龙翼，45个相关镜分类记录；另修CY026、CY026B、CY027F、CY027G、CY028A、CY029B、CY029C、CY029D、CY028、CY030十处漏翼。CY028A同时清除旧Perplexity残留，承接Kimi解锁。近景裁切及合理遮挡保留，未批量重画。当前17张新候选，5张中间稿保留；旧版和原画面封版不动。

108镜358秒（5分58秒）；护人、升空和咏唱50秒，GPT实际咏唱预算约45.8秒，仍待正式试读。静帧不能证明拍翼、弹叶、伴飞、撞击、落水和降落连续运动；本轮没有生成视频、配音或BGM。见[复核记录](镜头设计/生成记录/展翼与扇面-v033/复核记录.md)。

'''+x[i:])
print('v033:108shots358seconds,17current images,22 attempts,50second launch+chant')
