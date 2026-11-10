"""Apply approved long incantation, shield continuity and first-bite insert."""
import copy,json,hashlib,shutil,re
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];REC='镜头设计/生成记录/长吟唱护盾与结尾-v029';IMG='镜头设计/图像/长吟唱护盾与结尾-v029'
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,t):(R/p).write_text(t,encoding='utf-8')
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
cache=Path('C:/Users/36322/.codex/generated_images/01a162c1-6e38-7a10-aee7-5c8371c4830c')
shutil.copy2(cache/'exec-bdea48ab-943b-4314-a311-98b6d10e1dfe.png',R/IMG/'CY024B-v029-r1.png')
shutil.copy2(cache/'exec-6a5ae4de-9ca7-48de-a558-3a5613ce9f98.png',R/IMG/'CY024B-v029-r2.png')
originals=json.loads(read(REC+'/原图映射.json'))
originals['CY024B-r1']=str(cache/'exec-bdea48ab-943b-4314-a311-98b6d10e1dfe.png');originals['CY024B']=str(cache/'exec-6a5ae4de-9ca7-48de-a558-3a5613ce9f98.png')
save(REC+'/原图映射.json',originals)
old=json.loads(read('镜头设计/shot-plan-v0.28.json'));d=copy.deepcopy(old);by={s['id']:s for s in d['shots']};base=copy.deepcopy(by['CY024A'])
spell=['汇于苍穹的万流，','沉眠于云海的无尽潮汐。','循我的声音汇聚，','在此展开倾天之势。','让高悬的洪门洞开，','让焚身的烈火止息。','听我号令——','天瀑。']
quotes=[
'''千问俯身，将小鱼护进怀里。

**千问：**
抱紧我。

小鱼攥住衣襟，千问抱稳她退向侧柱；近旁圣骑士以白银护光挡住柱外来浪的方向。Perplexity已转到面向祭坛的右侧柱边，抬眼确认高处Claude的位置。ChatGPT沿中央通道继续向前，抬起手掌；第一句吟唱开始，画面转向她。

**ChatGPT：**
汇于苍穹的万流，''',
'''切右侧柱边的Perplexity：脸、持杖手与几何星形杖首同框。她把杖首指向高处Claude，青蓝光明确从杖首掠出，沿长阶方向斜向上延伸。她停在侧柱掩护下，没有瞬移到祭坛。

**ChatGPT（画外）：**
沉眠于云海的无尽潮汐。''',
'''切最高祭坛上的Claude。青蓝光从右下方到达，在她身前、头顶和两侧撑开局部弧形护盾，先隔开逼近的火舌与热浪。护盾下缘悬在石台之上，低柴堆留在盾外，底部保留水流通道；不是包住整座祭坛的封闭球。Claude抬眼看向来光，腕镣、腰链、踝链与固定脚托都未解除。

**ChatGPT（画外）：**
循我的声音汇聚，''',
'''切回ChatGPT，镜头缓缓靠近。衣摆与发梢被聚起的风托动，掌上水纹响应吟唱；真正的天瀑水体仍在中殿穹顶外汇聚，屋顶尚未破裂。骑士沿两翼进入厚石柱后，中央落水区净空。

**ChatGPT：**
在此展开倾天之势。
让高悬的洪门洞开，''',
'''短切弧盾中的Claude。她的目光从青蓝边缘光转向阶下，听见吟唱；身前护盾稳定，火舌仍在盾外低柴上跳动。此刻尚未落水，头纱与裙边仍干燥。

**ChatGPT（画外）：**
让焚身的烈火止息。''',
'''切回ChatGPT。她确认保护已就位，手指收拢。

**ChatGPT：**
听我号令——

音乐骤收，留出短暂空隙；手掌随最后的法术名翻下。

**ChatGPT：**
天瀑。'''
]
t=read(old['story_script'])
t=t.replace('说得平稳、短促，不必喊成战斗口号。她们没有停步，Perplexity 举杖护住祭坛，千问奔向小鱼。','说得平稳、短促，不必喊成战斗口号。她们没有停步，Perplexity循GPT的视线望向高处Claude，握杖转向右侧柱廊；千问奔向小鱼。此时只建立救援方向，护盾尚未生成。')
t=t.replace('从敞开的门内望向祭坛，ChatGPT 沿中央通道前行；千问跑向长阶下端的小鱼，Perplexity 在右侧举杖，蓝光先到高处祭坛。','从敞开的门内望向祭坛，ChatGPT沿中央通道前行；千问跑向长阶下端的小鱼，Perplexity在右侧柱边站定，准备施法。')
assert by['CY024A']['source_quote'] in t
t=t.replace(by['CY024A']['source_quote'],'\n\n'.join(quotes),1)
bquote='''天瀑从夜空轰穿中央中殿的穹顶，厚重连续的银白水幕覆盖中后景，主水体向下倾泻，落地激起宽阔水浪。大景不展示悬浮十字形、黑色杆件、成排人影或飞舞杂物；碎石落点和后墙长椅的受冲细节留给后续局部，不能用漂浮碎块装饰水势。洪水扑灭十字架下的低柴、六只铜火盆、中央环形烛式吊灯、后墙两只壁烛、两石座单烛及殿内火把。ChatGPT在靠入口的一侧；教主在她前方长阶下段的中央缓台，自己张开暗金护罩，脚步未动。千问抱着小鱼留在右侧柱边，由近旁圣骑士的白银护光与柱体挡住侧浪。高处Claude身前的青蓝弧盾承接前镜，冲向她的主水浪在弧面向两侧分开，贴地水从下缘通道浇灭低柴；盾边的细小水花溅湿她的发梢、头纱和裙边。Claude仍受缚，后殿拱顶完整；人物与护盾只在水幕遮挡间短暂可辨。'''
t=t.replace(by['CY024B']['source_quote'],bquote,1)
dquote=by['CY027D']['source_quote']+' Perplexity留在右侧后排柱边，杖首持续微亮，维持高处Claude身前的青蓝弧盾，不同时冲锋或双手持其他武器。'
t=t.replace(by['CY027D']['source_quote'],dquote,1).replace('祭坛只剩几乎不可见的护光，Claude 尚未解锁。','Claude身前弧盾只剩很淡的青蓝边缘光，束具仍未解除。')
fquote='''战斗结束，雨渐停。ChatGPT已恢复人形，从中殿破口下落到湿地，身旁水光散去。教主与教徒已经倒地，九位援军都在，千问仍抱着小鱼。确认落水、碎石与敌人威胁解除后，Perplexity先放低杖首，高处Claude身前的青蓝弧盾随之淡去；她再与GPT走向中央长阶，踏上首阶准备解锁。'''
t=t.replace(by['CY027F']['source_quote'],fquote,1)
mouth='''切Claude第一口饭的嘴部近景，画面带到鼻尖、嘴角、手与勺子。她将小口热饭送入口中，嘴唇轻轻合拢，空勺随即退出；只表现这一口，不停留展示咀嚼。饭碗仍由小鱼稳在膝上。'''
ending='''回到长椅上的两人。Claude已经吃下第一口，空勺放低到膝前，不再重复舀饭或送入口中。小鱼仰头望着她，笑起来；Claude回望小鱼，嘴角慢慢放松。最后四秒只留两人的呼吸与街市声，阳光落在肩上，结束。'''
t=t.replace('Claude 吃下一小口饭。DeepSeek 仰头看她，露出笑容。\n\n'+by['CY034']['source_quote'],mouth+'\n\n'+ending,1)
lines=t.splitlines();lines[2]='版本：v0.29｜2026-10-23｜采用长吟唱、24秒施法及音乐起伏；补护盾来源与成形、维持撤除；第一口饭近景2秒；天瀑改连续水幕。';t='\n'.join(lines)+'\n'
write('剧本/穿云-场景剧本-v0.29.md',t)
d.update(version='v0.29',revision='v029',created='2026-10-23',title='《穿云》带图分镜 v0.29 · 长吟唱、护盾与第一口饭',subtitle='24秒吟唱／护盾来源与撤除／连续水幕／两秒第一口饭',story_script='剧本/穿云-场景剧本-v0.29.md',source_manifest='镜头设计/生成记录/生成索引-v029.json',origin_manifest='镜头设计/shot-plan-v0.28.json')
d['review_intro']='作者确认长咒语、吃饭近景和音乐节奏；另明确天瀑用连续水幕遮住中后景并清掉杂物。新增护盾来源、成形与吟唱切镜；实际新图仍为待审候选，复用图与局部视窗明确标注。音乐、吟唱和动态均为执行设计，未制作音视频。'
d['review_focus']='先看Perplexity杖首发光→Claude局部弧盾→水幕分流灭柴→后排维持→战后撤盾，再看第一口饭近景→空勺放低→双人停留；吟唱贯穿24秒切镜，末尾收声后落水重音。'
newids=['CY024A1','CY024A2','CY024A3','CY024A4','CY024A5','CY034A']
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.28.json',previous_html='镜头设计/带图分镜-v0.28.html',added_ids=newids,modified_ids=['CY024','CY024A','CY024B','CY027D','CY027F','CY033','CY034'],boundary='102镜330秒；原CY024A8秒扩为六镜合计24秒。结尾原9秒拆为CY034A2秒+CY0347秒。原96镜仅CY024B/CY034替换主画面，历史保留。')
shield='Perplexity右柱位举杖，青蓝光离杖→Claude身前/头顶/两侧局部弧盾，底部离地、低柴在外→天瀑侧分流且贴地水灭柴，细水花仍可溅湿衣料→Perplexity后排持杖维持→战后放低杖撤盾→登阶解锁。不能写成Claude自己施法或整座祭坛封闭防水。'
d['continuity']['claude_shield']=shield
d['continuity']['water_curtain']='天瀑大景由连续水幕覆盖中后景；清除悬浮十字、杆件、重复人影与装饰性碎块。前景GPT、教主暗金护罩、千问抱小鱼仍可辨，高处Claude青蓝弧盾短暂透出。长椅及教徒受冲留CY024B1局部。'
d['continuity']['ending_first_bite']='CY031A说好→CY032A接勺→CY033旁景时画外舀起一小口→CY034A唯一第一口饭→CY034空勺已降低、小鱼笑、Claude回望，最后四秒停留。不重复送饭。'
d['music_direction']=dict(status='design_only_not_rendered',sequence=['CY024A','CY024A1','CY024A2','CY024A3','CY024A4','CY024A5','CY024B'],rule='连续同一段BGM，不随切镜重新起拍；避让吟唱，低弦→上行弦乐与无词合唱→低鼓→骤收→落水管弦重音；没有绑定或改动旧Victory粗剪音轨。',estimated_spell_sequence_seconds=24,voice_timing='subtitle_budget_only_pending_actual_readthrough')
def cue(text,start,duration,speaker='ChatGPT'):return dict(speaker=speaker,text=text,offset=start,duration=duration)
def setpic(s,id):
 p=IMG+'/'+id+'-v029-r1.png';req=REC+'/'+id+'-请求-v001.json'
 if id=='CY024B':p=IMG+'/CY024B-v029-r2.png';req=REC+'/CY024B-请求-v002.json'
 prev=s['presentation']['path']
 s['presentation']=dict(path=p,role='action',visible=s['action'],status='v0.29新静帧候选，待作者审阅',missing='静帧仅为动作代表状态，连续施法、口型、分水灭火与进食仍待动态验证。',show_as_main=True)
 s['generation_request']=req;s['visual_prompt']=json.loads(read(req))['prompt']
 s['refs']=[dict(path=p,role='本轮新静帧候选'),dict(path=req,role='实际冻结输入'),dict(path=prev,role='原图保留参考')]
 with Image.open(R/p) as im:w,h=im.size
 s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0.,y=0.,w=1.,h=1.),panel_index=0)
 s['editorial_review']=dict(version='v029',status='candidate_pending_author_review',dynamic_execution='pending')
specs=[
('CY024A',4,'护人，吟唱起句','低机位GPT中近景；千问声音画外接入','千问抱紧小鱼退到侧柱，Perplexity在右柱位举杖准备；镜头接GPT抬掌起句。',[cue('抱紧我。',0,1.1,'千问'),cue(spell[0],1.2,2.7)],'低弦持续音从GPT起句进入；保持千问与GPT不重叠，实际配音待制作。'),
('CY024A1',4,'护盾从杖首发出','Perplexity中近景／杖首与面部同框','Perplexity在右侧柱边将杖首指向高处，青蓝光明确从杖首斜向上发出；GPT画外吟唱不断。',[cue(spell[1],0.05,3.9)],'低弦连续，细小魔法音从杖首起；吟唱为同一条声音跨切，不重新起句。'),
('CY024A2',4,'青蓝弧盾护住Claude','祭坛人物中全景／右下方来光与下缘空隙可辨','青蓝光抵达Claude，在她身前、头顶与两侧展开离地弧盾；低柴在外，镣铐和脚托仍在。',[cue(spell[2],0.1,2.9)],'弦乐上行加入很轻的无词合唱，展开音克制，留清楚的画外吟唱。'),
('CY024A3',6,'水势随吟唱汇聚','GPT中近景／缓缓推近','GPT继续抬掌，衣摆与发梢轻扬，水纹响应；真正天瀑水体在完整中殿穹顶外汇聚，骑士沿两翼净空。',[cue(spell[3],0,2.8),cue(spell[4],3.05,2.9)],'上行弦乐持续，低鼓逐渐加入，合唱展开；全部为同一段BGM连续发展。'),
('CY024A4',3,'护盾中的Claude','Claude面部与肩部近景／护盾边缘入画','Claude在弧盾中抬眼听见阶下吟唱，受束状态不变；水尚未落下，火仍在盾外。',[cue(spell[5],0.1,2.8)],'合唱与弦乐接近高点，仍让吟唱清楚；不提前加入灭火声。'),
('CY024A5',3,'听我号令，天瀑','GPT低位中近景／收拢手指后翻掌','GPT确认保护就位，收拢手指；音乐短收，翻掌说出天瀑，下一镜水墙轰落。',[cue(spell[6],0,1.25),cue(spell[7],2,0.85)],'“听我号令”后音乐骤收，约0.7秒只留人声尾响与蓄水声；天瀑落字后接下一镜水墙与管弦重音。')]
block=[]
for idx,(id,seconds,title,framing,action,cues,sound) in enumerate(specs):
 s=copy.deepcopy(base)
 for k in ['time_caption','cinematic_beats','subtitle_cues']:s.pop(k,None)
 s.update(id=id,title=title,seconds=seconds,framing=framing,action=action,source_quote=quotes[idx],dialogue='\n'.join(c['speaker']+'：'+c['text'] for c in cues),dialogue_cues=[],subtitle_cues=cues,sound=sound+' 音乐/配音/音效尚未制作。',dialogue_timing_status='estimated_budget_pending_readthrough',entry_state=('回闪结束，救援队已入殿，护盾尚未形成。' if idx==0 else block[-1]['exit_state']),exit_state=['GPT起句，Perplexity已在右侧柱边准备。','青蓝光已离杖，斜向高处Claude。','弧盾已成形，Claude仍受束，低柴在盾外。','骑士净空，水体在屋顶外汇聚，弧盾稳定。','Claude受护且仍干燥，GPT准备最终命令。','GPT翻掌，法术名落下，接天瀑破顶。'][idx],purpose='让长吟唱与救援动作同步展开，交代保护来源、目标和发动时机。',next_link='接'+(specs[idx+1][0] if idx<5 else 'CY024B')+'，吟唱和音乐按连续段衔接。')
 s['invariants']=[shield,'屋顶直到CY024B才被水轰穿；此前Claude衣料干燥，普通火光未灭。','吟唱连续跨切，不因切到Perplexity或Claude而改变说话者。','GPT掌上水纹为施法光，不提前把真正水墙落入殿内。']
 s['presentation']['missing']='沿用既有GPT施法代表帧；本镜的连续动作、切点与声音仍待动态制作，图中不包含画外救护动作。'
 s['presentation']['visible']='既有GPT低位抬掌代表帧，头顶银白水纹光可见；图中不含千问和Perplexity的救护动作。'
 if id in ['CY024A1']:s['asset_ids']=['MULKZI2W3JZ5F','CHAR-CLAUDE','ENV-CHURCH']
 if id in ['CY024A2','CY024A4']:s['asset_ids']=['CHAR-CLAUDE','ENV-CHURCH']
 if id in ['CY024A3','CY024A5']:s['asset_ids']=['CHAR-GPT','ENV-CHURCH']
 if id in ['CY024A1','CY024A2']:setpic(s,id)
 if id=='CY024A4':
  donor=block[2];s['presentation']=copy.deepcopy(donor['presentation']);s['presentation'].update(visible='复用护盾成形图的Claude面部、肩部和弧盾局部视窗；无新图生成。',missing='原图局部视窗仅作反应构图预演，抬眼变化与连续护持待动态。')
  s['generation_request']=donor['generation_request'];s['visual_prompt']=donor['visual_prompt'];s['refs']=copy.deepcopy(donor['refs']);s['page_size']=donor['page_size']
  w,h=s['page_size'];s['panel_region']=dict(x=.32,y=.05,w=.43,h=.43);s['panel_rect_pixels']=[int(w*.32),int(h*.05),int(w*.43),int(h*.43)]
 if idx==0:s['time_caption']=dict(text='此刻',offset=.1,duration=1.7)
 block.append(s)
idx=d['shots'].index(by['CY024A']);d['shots'][idx:idx+1]=block
by['CY024']['action']+=' Perplexity循GPT视线望向高处，握杖转入右侧柱廊；此处只布置方向，护盾还未生成。'
by['CY024B'].update(action='连续厚重水幕覆盖中后景，清除悬浮杂物；水撞上Claude青蓝弧盾向侧面分流，贴地水灭低柴。教主暗金罩与千问所在右侧柱边银白护光各自独立。',source_quote=bquote,entry_state='吟唱结束，Claude的青蓝局部弧盾已成形，小鱼受柱体和骑士白银护光保护，中央落水区净空。',sound='天瀑落字后管弦与低鼓重音同步水墙轰落，水声居前；随后保持冲水与熄火嘶声，接CY024B1局部。声音设计未制作。')
setpic(by['CY024B'],'CY024B')
by['CY024B'].update(exit_state='水浪涌上最高祭坛石台，长椅尚未在大景中展示离墙。',next_link='接CY024B1：切最高祭坛后墙左侧长椅受冲局部，水浪在此才将长椅掀离原位。')
by['CY024B']['invariants']+=[shield,d['continuity']['water_curtain']]
by['CY027D'].update(action=dquote,source_quote=dquote);by['CY027D']['presentation']['missing']+=' 本轮补Perplexity持杖维持护盾的连续动作，旧静帧不能证明该动作已完成。'
by['CY027F'].update(action=fquote,source_quote=fquote,entry_state='敌人已倒地，威胁解除，Perplexity仍维持高处弧盾。',exit_state='Perplexity放低杖撤盾后，与GPT踏上首阶；接登顶解踝链。')
by['CY027F']['presentation']['missing']+=' 本轮补放低杖撤盾再起步，旧图作战后代表状态，撤盾待动态验证。'
by['CY033'].update(next_link='接CY034A：旁景期间Claude已从碗中舀起一小口饭；切嘴部特写，完成唯一第一口。')
m=copy.deepcopy(by['CY034'])
m.update(id='CY034A',title='第一口饭',seconds=2,framing='鼻尖、嘴角、手与勺子局部近景',action='小口饭送至唇边，嘴唇轻合，空勺退出；只吃这一口，不停留拍咀嚼。',source_quote=mouth,entry_state='Claude已接勺并舀起小口饭，碗仍由小鱼稳在膝上。',exit_state='第一口已吃下，空勺离开嘴部并开始放低。',next_link='接CY034：空勺已经降低，小鱼笑、Claude回望，最后四秒双人停留。',purpose='让初见被打断的一口饭真正完成。',dialogue='无对白',dialogue_cues=[],sound='留柔和街市声和轻微餐具声；不放大咀嚼声。音乐延续既有结尾温暖基调，未制作新音轨。')
m.pop('subtitle_cues',None);m['cinematic_beats']=[dict(offset=0,intent='勺中小口饭已到唇前'),dict(offset=.6,intent='饭入口、唇轻合'),dict(offset=1.2,intent='空勺退出并降低')]
setpic(m,'CY034A')
idx=d['shots'].index(by['CY034']);d['shots'].insert(idx,m)
end=by['CY034'];end.update(title='阳光里坐一会儿',seconds=7,action=ending,source_quote=ending,entry_state='Claude已吃下第一口，空勺降低，嘴唇合拢。',sound='前3秒留小鱼笑与Claude回望的呼吸；最后4秒街市与呼吸自然停留，尾乐轻收。无新对白，未制作新声音。')
end['cinematic_beats']=[dict(offset=0,intent='空勺已降低，小鱼仰头笑'),dict(offset=1.5,intent='Claude回望，表情放松'),dict(offset=3,intent='最后4秒双人定镜停留，不再舀饭')]
setpic(end,'CY034')
elapsed=0
for s in d['shots']:s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
d['total_seconds']=elapsed
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']];sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
save('镜头设计/shot-plan-v0.29.json',d)
records=[]
for key,original in originals.items():
 id='CY024B' if key.startswith('CY024B') else key
 rejected=key=='CY024B-r1';attempt=1 if id!='CY024B' or rejected else 2
 req=REC+'/'+id+'-请求-v00'+str(attempt)+'.json';dest=IMG+'/'+id+'-v029-r'+str(attempt)+'.png'
 request=json.loads(read(req))
 records.append(dict(shot_id=id,attempt=attempt,original=original,destination=dest,sha256=sha(R/dest),request=req,request_sha256=sha(R/req),inputs=[dict(path=p,sha256=sha(p)) for p in request['referenced_image_paths']],status='rejected_preserved' if rejected else 'candidate_pending_author_review',reason='作者认为水中悬浮杂物奇怪，明确改成连续水幕覆盖中后景。' if rejected else '本轮范围内新候选，待作者审阅。'))
save('镜头设计/生成记录/生成索引-v029.json',dict(version='v029',previous_index='镜头设计/生成记录/生成索引-v028.json',records=records,review=REC+'/复核记录.md'))
snap=R/'镜头设计/带图分镜-v0.28.html'
if not snap.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snap)
p='scripts/build_storyboard.py';write(p,read(p).replace('shot-plan-v0.28.json','shot-plan-v0.29.json').replace('"v028")','"v028", "v029")').replace("'v028')","'v028','v029')"))
p='00_打开项目.html';x=read(p).replace('v0.28','v0.29').replace('96 镜 · 5 分 14 秒','102 镜 · 5 分 30 秒').replace('结尾回应与天瀑吟唱；8秒施法预算','长吟唱24秒 · 护盾来源与连续水幕 · 第一口饭')
x=x.replace('<a href="镜头设计/图像/火种慢镜-v026/CY029B1', '<a href="镜头设计/带图分镜.html#CY024A1">本轮：长吟唱与护盾来源<small>Perplexity举杖→Claude弧盾→连续水幕；音乐起伏已写入分镜</small></a>\n<a href="镜头设计/带图分镜.html#CY034A">本轮：第一口饭近景<small>2秒吃饭近景→7秒双人收尾</small></a>\n<a href="镜头设计/图像/火种慢镜-v026/CY029B1',1)
write(p,x)
p='制作进度.md';x=read(p);i=x.index('## ')
write(p,x[:i]+'''## 2026-10-23：长吟唱、护盾来源、连续水幕与第一口饭（v0.29）

作者采用长吟唱全文、吃饭嘴部近景与音乐/切镜节奏。已同步[剧本v0.29](剧本/穿云-场景剧本-v0.29.md)与[当前分镜](镜头设计/带图分镜.html)。原CY024A八秒扩展成六镜合计24秒：起句→Perplexity举杖→Claude弧盾成形→GPT蓄势→Claude反应→收声翻掌。护盾只护人，底部离地、柴堆留在外，贴地水仍灭火；后排持杖维持、战后放低杖撤盾再登阶解锁。千问与小鱼的侧柱白银护光来自近旁骑士。

新增CY034A两秒第一口饭，CY034缩至七秒并改空勺已降低，保留最后四秒双人停留。全片102镜330秒（5分30秒）。对白字幕时间是估算，吟唱/配乐/音效与实际动态尚未制作。

作者指出首版天瀑水中悬浮杂物奇怪，明确选择连续水幕覆盖中后景；CY024B-r1保留为拒绝候选，当前引用r2，去掉漂浮十字、杆件和重复碎块。其余新图为待审候选。共五张当前新图（含天瀑修订、结尾收勺），两处GPT切镜复用旧代表帧，Claude反应复用护盾局部视窗。旧版与原封版不动。见[复核记录](镜头设计/生成记录/长吟唱护盾与结尾-v029/复核记录.md)。

'''+x[i:])
assert len(d['shots'])==102 and elapsed==330
assert sum(s['seconds'] for s in block)==24
assert m['seconds']+end['seconds']==9
for s in d['shots']:assert s['source_quote'] in t,s['id']
print('Prepared v0.29:102 shots330 seconds;24-second spell;2+7-second ending.')

