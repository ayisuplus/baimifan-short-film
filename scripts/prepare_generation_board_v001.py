"""One-time editorial cleanup and reference-only generation grouping; no media calls."""
import copy, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text('utf-8-sig'))
def write(p, data):
    dst=ROOT/p; dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

p=read('镜头设计/shot-plan-v0.53r2.json'); s={x['id']:x for x in p['shots']}
p['version']='v0.53r3'; p['report_revision']='v053r3'; p['title']='《白米饭》带图分镜 v0.53r3 · 生成前说明核对'
p['source_manifest']='镜头设计/shot-plan-v0.53r2.json'
p['story_script']='剧本/白米饭-场景剧本-v0.53r3.md'
p['audio_arrangement']='后期/生成前复核-v001/预演编排-v053r3.json'
s['CY024']['framing']='拉远低位广角群像／GPT与八位正门援军错落站位'
s['CY024']['purpose']='看清GPT与八位正门援军，Kimi不在队伍，接分路救援。'
s['CY027D']['framing']='长阶广角群像，八人在下层，远处最高祭坛只有不透明暗月罩'
s['CY027D']['invariants']=[v.replace('九位各一人','八位下层同伴各一人，Kimi在罩内').replace('九位同伴沿长阶分层','八位下层同伴沿长阶分层') for v in s['CY027D']['invariants']]
s['CY027E1']['framing']='环境特写／贴近湿石板的雨滴与涟漪'
s['CY020']['sound']='Claude愤怒喊出原句；画外衣料摩擦、木架与锁链震动，不提前出现宝宝落地或身体撞击声。'
s['CY034']['sound']='尾乐在本镜前3秒内收尽；最后4秒（成片430–434秒）BGM静音，只留街市声与两人呼吸。'
k=s['CY024K0']; old=k['source_quote']; k['dialogue']=k['dialogue'].replace('Kimi（画外）','Kimi')
for c in k['subtitle_cues']: c['speaker']=c['speaker'].replace('Kimi（画外）','Kimi')
k['source_quote']=old.replace('Kimi（画外）','Kimi')
script=(ROOT/'剧本/白米饭-场景剧本-v0.53r2.md').read_text('utf-8-sig')
assert old in script
(ROOT/p['story_script']).write_text(script.replace(old,k['source_quote'],1),encoding='utf-8')
seq=set(p['music_direction']['sequence'])
p['music_direction']['sequence']=[x['id'] for x in p['shots'] if x['id'] in seq]
p['revision_notes']=p.get('revision_notes',[])
write('镜头设计/shot-plan-v0.53r3.json',p)
a=read('后期/片名确认-v001/预演编排-v053r2.json')
a['version']='v053r3-generation-review'; a['shot_plan']='镜头设计/shot-plan-v0.53r3.json'
a['shot_plan_sha256']=hashlib.sha256((ROOT/a['shot_plan']).read_bytes()).hexdigest()
write(p['audio_arrangement'],a)

# Only description corrections; assets and historical prompt bytes remain preserved.
assets=read('资产/assets.json')
if not (ROOT/'资产/历史/assets-before-generation-board-v001.json').exists():
    write('资产/历史/assets-before-generation-board-v001.json',assets)
for x in assets['assets']:
    if x['id']=='CHAR-CLAUDE': x['role']=next(m['role'] for m in p['masters'] if m['id']=='M-CL')
write('资产/assets.json',assets)

# Boundaries chosen around causal units and complete lines; not a blind 15s grid.
ends=[
('CY003A','初遇与递饭'),('CY004A','善意受阻与消息'),
('CY005','宫门放行与独座'),('CY008','求救、拒绝与追问'),('CY009A','决定独自前去与长殿目送'),
('CY012','等待与钻洞'),('CY016','察觉与试锁'),('CY016C','劝离与脚步逼近'),
('CY018','抓柴与受阻'),('CY019','铺柴与教主'),('CY021B','保护、推倒与抓袍'),('CY022B','登阶与点火'),
('CY023','黑焰、列阵与破门'),('CY024K0','正门指令与月下请求'),('CY024K3','破窗、循刃瞬移与护罩'),
('CY026B','试镣、骑士入场与首轮邀约'),('CY026D','基地与月背约定'),('CY024A','各路回应、抱紧宝宝与起咏'),
('CY024A2','截击与罩内安抚'),('CY024A7','聚水与俯冲'),('CY024A8','破顶与双向反应'),
('CY024B','结印、出击与撞盾'),('CY027','清场余波与降落'),('CY027B3','对峙与变身腾空'),
('CY027D0','天空省略与外敌逼近'),('CY027F0','守门、胜负与取钥匙'),('CY028A','撤罩、解锁与落脚'),
('CY029E','确认宝宝、初咏与父亲打断'),('CY029E4','选择继续与凝种'),('CY028','星火、脱力与接抱'),
('CY031','离殿与数日后'),('CY033','落座、接勺与热饮'),('CY034','第一口饭与安静收尾')]
allids=[x['id'] for x in p['shots']]; batches=[]; start=0
for i,(last,title) in enumerate(ends,1):
    stop=allids.index(last)+1; ids=allids[start:stop]; duration=sum(s[x]['seconds'] for x in ids)
    assert 0<duration<=15,(last,duration)
    batches.append({'id':f'GB{i:03d}','title':title,'shot_ids':ids,
      'group_reason':'保持本组动作因果与完整台词；切点落在镜头边界。',
      'handle_reason':'与下一组的时空或叙事阶段分开，保留剪辑余量；不增加正片时长。' if duration<15 else '',
      'status':'draft_not_submitted'})
    start=stop
assert start==len(allids)
plan={'version':'v001','title':'白米饭 · 生成板','source':'镜头设计/shot-plan-v0.53r3.json',
      'assets':'资产/assets.json','output':'视频制作/生成板-v001','request_seconds':15,
      'cast_review':'视频制作/生成板-v001/人物核对.json','sound_review':'视频制作/生成板-v001/声音核对.json',
      'navigation':{'home':'00_打开项目.html','previs':'镜头设计/带图分镜.html#previs','review':'后期/生成前复核-v001/审查报告.md'},
      'style':'沿用本片当前哥特式异世界动画母版及逐镜参考，人物设计、服装本色、眼色与画风一致。',
      'constraints':'按各镜起止状态连续表演，不重复已完成动作。现有图片用于身份、构图和状态参考，不把静帧终态当起帧。画内只出现本镜动作指定的人物，参考卡不表示全部入场。',
      'sound_policy':'说话语言为中文，原句只说规定次数。画内说话者自然口型，画外声不让在画人物代说；连续咏唱跨镜保持同一声线。环境音与动作音随动作发生；既有BGM与全片连续配音由后期统筹，不在每个15秒重新起乐。正式声线与口型待验。',
      'batches':batches,
      'speech_modes':{i:'说话者嘴部不在画面；声音连续，不让在画者代说' for i in ['CY003B','CY016B1','CY021','CY026A1','CY026D1','CY026E','CY028B','CY028C','CY029','CY029E2','CY029E3','CY029E4','CY029B1']},
      'execution_notes':{
       'CY016D':'下长阶过程剪辑省略，本镜从阶下抓木开始。',
       'CY020A':'本镜只演一次被推倒，落地后手肘开始撑地；撑起失败留到下一镜。',
       'CY021':'延续上一镜同一次撑地，完成唯一一次撑起失败，不再次摔倒。',
       'CY022':'展示火把接触柴堆与火焰蔓延；教主返回阶下的移动过程用后续切镜省略。',
       'CY024K4':'重点演见痛撤刀；双刃收后腰在下次罩内镜前用剪辑省略，后续双手已腾出。',
       'CY027F1':'钥匙开踝扣，第二扣重复操作用剪辑省略，结束两只踝扣均打开。',
       'CY027G':'中间腰链及另一腕扣用剪辑省略，重点是GPT先扶稳再开最后腕扣；结束五扣全开。'},
      'shot_notes':{
       'CY016D':'下长阶过程用切镜省略，本镜从阶下接抓木；不要2秒走完整长阶。',
       'CY020B':'参考图火把形制有历史差异，须与CY021A同一短柄火把统一，未解决前不冻结。',
       'CY020A':'推倒只发生一次，本镜结束在落地后手肘开始撑地；起身失败在CY021完成。',
       'CY021':'延续同一次撑地失败，不再摔倒。原句2秒为预算，正式表演待验。',
       'CY022':'先展示点柴接触与燃起；返下阶用下一场面剪辑省略，不要求4秒完整走完。',
       'CY024K0':'已按当前画面核对为Kimi现场说话；6秒含完整请求与投刃，口型与留白待验。',
       'CY024K4':'3秒重点是见痛撤刀；双刃收后腰可在后续罩内镜前省略，不做重复试镣。',
       'CY024A0':'静帧手位与动态要求相反：动态必须千问左臂抱小鱼、右手持扇；此图不能直接绑定强约束首帧。',
       'CY027F1':'先交代钥匙转动与踝扣打开，用剪辑省略第二扣重复操作。',
       'CY027G':'GPT扶稳先于最后腕扣解开；中间腰链与另一腕扣用剪辑省略，五扣均须已解除。',
       'CY031A':'先坐下后接勺；4秒含问答为预算，需正式读稿验证。'},
      'mix_notes':['七首曲从music_adoption.marks读取；源in/out未定，禁止按批次重播或自动循环。','Fear在204–410秒的206秒段落长于139.551701秒源曲，须乐句重编与留白。','430–434秒BGM静音，只留街市与呼吸。'],
      'global_gaps':['所有批次待作者审阅，尚未上传、冻结或提交。','正式声线、完整连续配音、音效与混音听审尚未完成；现有时码是预演预算。','模型模板已核对官方文档，具体执行入口、参数、账户能力及槽位绑定待现场核实。']}
write('视频制作/生成板-v001/批次计划.json',plan)
print(json.dumps({'shots':len(allids),'batches':len(batches),'film_seconds':p['total_seconds'],'request_seconds':len(batches)*15},ensure_ascii=False))
