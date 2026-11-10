"""Versioned camera/light revision; preserves v014 sound samples and timing."""
import copy, hashlib, html, json, os, re, shutil
from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
OLD='视频制作/生成板-v014'
OUT='视频制作/生成板-v015'
FIX='后期/张力与机位-v015'
OLDFIX='后期/生成前修正-v014'
SOURCE='镜头设计/shot-plan-v0.60.json'
REQ='镜头设计/生成记录/张力与机位-v060/请求.json'
def load(p):return json.loads((ROOT/p).read_text('utf-8-sig'))
def write(p,d):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def remap(d,oldhash,newhash):
    if isinstance(d,dict):return {k:remap(v,oldhash,newhash) for k,v in d.items()}
    if isinstance(d,list):return [remap(v,oldhash,newhash) for v in d]
    if isinstance(d,str):
        return d.replace(OLD,OUT).replace(OLDFIX,FIX).replace('镜头设计/shot-plan-v0.59.json',SOURCE).replace(oldhash,newhash)
    return d
CHANGES={
'CY019':dict(
 camera='50mm同轴侧后机位，略俯向小鱼；教主暗袍占画右前景，小鱼画左中景；轻随起身升高后收停。',
 framing='教主侧后遮挡式中全景，小鱼张臂全身偏左，长阶斜向退到背景',
 action='小鱼双手撑地、踉跄站起，在长阶下端张臂挡住教主去路。她位于画左，望向画右上方教主，腿微颤、眼含泪；右前景仅教主暗袍与身体边缘，不露嘴。高处Claude在弱焦背景；无魔法、尚未推搡。',
 note='本图为起身后的张臂终态，不强制首帧。右侧暗袍为同一教主，画内只露局部，原句让开由画外嘴部发声。',
 cast=dict(visible=['DeepSeek','教主','Claude'],offscreen=[],reflection=[],note='教主仅画右袍肩/侧身，不露脸或嘴；高处Claude虚焦且柴堆遮下半身。教主原句仍按画外方式，不让小鱼代说。'),
 en='From the priest side/rear at 50mm, follow the child rising then stop. His cropped dark robe occludes screen right; the child blocks left middle-ground. Altar remains soft and dim.'),
'CY020B':dict(
 camera='孩子眼高肩后略仰，65mm固定近景；小鱼左下前景，教主右上，视线互对；保持同侧轴线。',
 framing='小鱼肩后略仰近景，教主脸与胸口压入右侧',
 action='承接小鱼张臂，镜头贴近她左后肩。小鱼画左望右上，教主画右垂眼望左下，肩膀放松，双唇闭合。教主右手持唯一短柄黑铁笼火把，黑紫焰偏边，左手仍垂下；两人留有距离。只凝视，不前冲、不推、不摔。',
 note='火把是短柄铁笼式，黑紫焰；右手持火、左手垂下。脸部侧光，眉眼有阴影，背景与金饰收暗，不能改成英雄展示。',
 cast=dict(visible=['DeepSeek','教主'],offscreen=['Claude'],reflection=[],note='小鱼左下只见鲸帽后侧、侧脸与张臂局部；教主右侧脸胸口与垂手。无接触。'),
 en='Fixed 65mm from child eye height over her shoulder, slight upward angle; child lower-left, priest upper-right looking down-left. Right hand keeps the short basket torch; left hand hangs. No shove yet.'),
'CY020A':dict(
 camera='同轴贴地约20cm、50mm斜侧近景；小鱼左侧脸与手肘成斜线，教主袍靴压画右；落地轻顿后收稳。',
 framing='贴地斜侧中近景，小鱼左前景与教主右侧袍靴同框',
 action='开头承对视，教主左手只推开一次、右手仍持火把。小鱼向画左失衡落地，手肘着地后开始撑地，眼睛清醒、含泪喘息，望向画右教主。镜末右侧仅袍角和靴形成近距离威胁，靴不踩她；本图是落地终态。撑起失败留下一镜，不重复摔落。',
 note='只有一次推倒；图示落地终态，非强制首帧。左手推后退出取景，右手与火把在画外仍持续持有。靴不踢踩孩子，尚未抓袍。',
 cast=dict(visible=['DeepSeek','教主'],offscreen=['Claude'],reflection=[],note='教主开头左手推开，落地后仅画右靴/袍角；头、右手火把在画外。小鱼清醒撑肘。'),
 en='Same side of axis, low oblique 50mm camera. One left-hand shove at entry, then child falls left and begins bracing her elbow. Right-edge robe and boot loom without kicking or stepping on her. Image is the landing end-state.'),
'CY024A0':dict(
 camera='从被抱小鱼鲸帽后肩、孩子眼高略仰65mm紧近景；千问脸在右上，孩子抓衣小手在下缘，背景虚化；末尾只轻随抬眼。',
 framing='小鱼肩后略仰的千问头肩紧近景，面部自然透视',
 action='千问在画外继续用左臂承托小鱼、右手低持合扇；镜内不露成人手臂和扇子。她微俯身看向小鱼，完整说抱紧我，小鱼抓紧衣襟靠近。末尾千问抬眼向GPT，镜头轻随，不拉成全身；孩子始终不落地。',
 note='成人双手、承托前臂和合扇均在画外；左抱右扇由连续调度维持，不因遮挡宣称手位已目视验收。本图为说话中的构图参考，不锁死首帧表情。',
 cast=dict(visible=['Qwen','DeepSeek'],offscreen=['GPT','Kimi','Claude'],reflection=[],note='仅千问头肩、孩子鲸帽后脑与抓衣小手；成人双手与合扇不入画。'),
 en='Intimate 65mm over-child-shoulder head-and-shoulders close-up, slightly upward. Natural Qwen face upper-right, child clutching collar below. Adult forearms, hands and closed fan remain outside crop. Left-arm support and right-hand fan continue offscreen; slight eye rise at end.')
}
def run_renderer(name,entry='main'):
    file=ROOT/'scripts'/name
    text=file.read_text('utf-8').replace(OLD,OUT).replace(OLDFIX,FIX).replace('镜头设计/shot-plan-v0.59.json',SOURCE)
    ns={'__file__':str(file),'__name__':'v015_version_adapter'}
    exec(compile(text,str(file),'exec'),ns)
    return ns[entry](ROOT) if entry=='build' else ns[entry]()
def main():
    old=load('镜头设计/shot-plan-v0.59.json');source=copy.deepcopy(old);sm={x['id']:x for x in source['shots']}
    jobs=load(REQ);q=load('镜头设计/生成记录/张力与机位-v060/千问补修.json')
    for j in jobs:j['selected_for_v015']=j['id']!='CY024A0';j['status']='candidate_pending_author_review' if j['selected_for_v015'] else 'rejected_left_hand_fan'
    q.update(selected_for_v015=True,status='candidate_pending_author_review');jobs.append(q)
    write(REQ,jobs[:-1]);write('镜头设计/生成记录/张力与机位-v060/千问补修.json',q)
    selected={j['id']:j for j in jobs if j['selected_for_v015']}
    for sid,c in CHANGES.items():
        s=sm[sid];s['previous_presentation_v059']=copy.deepcopy(s['presentation'])
        s['presentation'].update(path=selected[sid]['project_output'],visible=c['action'],status='机位光影修订候选，待作者审阅',missing='静帧不证明动作口型；画外手位须动态连续性验收')
        s.update(framing=c['framing'],camera=c['camera'],action=c['action'],source_quote=c['action'],visual_prompt=selected[sid]['prompt'],generation_request=REQ)
        s['refs'].insert(0,dict(path=selected[sid]['project_output'],role='v060机位光影候选；历史图保留'))
        s['final_static_review']=dict(version='v060',status='pending_author_review',review=FIX+'/视觉复核.md')
        s['invariants'].append(c['note'])
        if sid!='CY024A0':s['invariants'].append('对峙轴线：小鱼画左、教主画右；窄冷侧光突出脸手，降低金饰和地面反光，保留既有蜡烛/火盆位置。')
    source.update(version='v0.60',revision='v060',previous_source='镜头设计/shot-plan-v0.59.json',subtitle='133镜 · 464.4秒 · 4张机位光影新候选',roughcut_preview=FIX+'/全片声音预览.html',audio_repair_plan=FIX+'/配音对位方案.json')
    source['revision_notes']=dict(scope='作者要求优化小鱼教主对峙光影构图，选择千问小鱼肩后略仰拍。4张新候选，镜长/对白/音轨不变。',rejected_qwen='镜头设计/图像/生成前修正-v059/CY024A0-r3-v059.png',source_sha256=sha('镜头设计/shot-plan-v0.59.json'))
    write(SOURCE,source);h=sha(SOURCE);oldh=sha('镜头设计/shot-plan-v0.59.json')
    for f in (ROOT/OLD).glob('*.json'):
        if f.name in ['展开数据.json','结构核验.json']:continue
        d=remap(load(f),oldh,h);write(OUT+'/'+f.name,d)
    plan=load(OUT+'/批次计划.json');plan.update(version='v015',output=OUT+'/生成板.html')
    for sid,c in CHANGES.items():
        plan['action_overrides'][sid]=c['action'];plan['shot_notes'][sid]=c['note'];plan['execution_notes'][sid]=c['camera']+' '+c['note']
        plan['cast_overrides'][sid]=c['cast']
    plan['navigation']['review']=FIX+'/修正交接.html'
    plan['speech_modes']['CY019']='教主嘴部在画外；只听原句，不补脸或口型，不让画内小鱼代说。'
    # The rest of the confrontation retains its stronger composition, with a matching light hierarchy.
    for sid in ['CY020','CY021','CY021B','CY022A']:
        plan['shot_notes'][sid]=plan['shot_notes'].get(sid,'')+' 与新对峙镜衔接：保留当前构图动作；后期轻收地面与金饰高光，人物肤色及原光源位置保持。'
    write(OUT+'/批次计划.json',plan)
    cast=load(OUT+'/人物核对.json')
    for sid,c in CHANGES.items():cast['shots'][sid]=dict(c['cast'],basis='v060实际画面与动态进出镜联合核对')
    write(OUT+'/人物核对.json',cast)
    direction=load(OUT+'/动态审查.json')
    for batch in direction['batches'].values():
        for sid,r in batch['shots'].items():
            if sid in CHANGES:
                c=CHANGES[sid];r.update(camera_zh=c['camera'],camera_en=c['en'],action_en=c['en'])
                if sid=='CY019':r['transition_zh']='承被踢倒后撑起；教主袍边压入右前景，原句让开来自画外嘴部，尚未推搡。'
    write(OUT+'/动态审查.json',direction)
    audit=load(OUT+'/对白复核.json');audit['localization_sha256']=sha(OUT+'/日语译配.json');write(OUT+'/对白复核.json',audit)
    for name in ['配音对位方案.json','BGM剪辑方案.json','实际BGM剪辑.json','作者确认选曲.json']:
        write(FIX+'/'+name,remap(load(OLDFIX+'/'+name),oldh,h))
    # Reuse actual audio byte-for-byte: no event, cue, source segment, gain or duration changed.
    for name in ['BGM试听.wav','BGM试听.mp3','全片声音预览.mp3']:
        if not (ROOT/FIX/name).exists():shutil.copy2(ROOT/OLDFIX/name,ROOT/FIX/name)
        assert sha(FIX+'/'+name)==sha(OLDFIX+'/'+name)
    mix=load(FIX+'/实际BGM剪辑.json')
    mix.update(source_sha256=h,voice_plan_sha256=sha(FIX+'/配音对位方案.json'),bgm_plan_sha256=sha(FIX+'/BGM剪辑方案.json'))
    mix['visual_revision_audio_reuse']=dict(from_manifest=OLDFIX+'/实际BGM剪辑.json',sha256=sha(OLDFIX+'/实际BGM剪辑.json'),reason='Only camera/images revised; identical event content and output bytes verified.')
    assert mix['voice_events']==load(OLDFIX+'/实际BGM剪辑.json')['voice_events']
    write(FIX+'/实际BGM剪辑.json',mix)
    run_renderer('build_generation_v014.py')
    run_renderer('build_previs_v014.py','build')
    review_page(old,source)
    run_renderer('verify_generation_v014.py')
    checks={sid:dict(old_image=next(x for x in old['shots'] if x['id']==sid)['presentation']['path'],new_image=sm[sid]['presentation']['path'],sha256=sha(sm[sid]['presentation']['path'])) for sid in CHANGES}
    assert [(x['id'],x['seconds'],x.get('subtitle_cues')) for x in old['shots']]==[(x['id'],x['seconds'],x.get('subtitle_cues')) for x in source['shots']]
    write(FIX+'/画面修订核验.json',dict(status='passed',changed_shots=checks,timing_dialogue_unchanged=True,audio_outputs_identical=True,author_adoption=False,video_generated=False))
def review_page(old,new):
    om={s['id']:s for s in old['shots']};sm={s['id']:s for s in new['shots']}
    def url(p):return quote(os.path.relpath(ROOT/p,ROOT/FIX).replace('\\','/'),safe='/#')
    cards=[]
    for sid,c in CHANGES.items():
        cards.append('<section><h2>'+html.escape(sm[sid]['title'])+'</h2><p>'+html.escape(c['camera'])+'</p><div class="pair"><figure><figcaption>上一版'+(' · 作者已否定' if sid=='CY024A0' else '')+'</figcaption><img src="'+url(om[sid]['presentation']['path'])+'"></figure><figure><figcaption>新机位候选 · 待审阅</figcaption><img src="'+url(sm[sid]['presentation']['path'])+'"></figure></div><p>'+html.escape(c['note'])+'</p><a href="全片声音预览.html#t='+str(sm[sid]['start_second'])+'">带原配音与BGM看这一段</a></section>')
    seq=['CY019','CY020','CY020B','CY020A','CY021','CY021B','CY022A','CY024A0']
    data=[dict(id=sid,title=sm[sid]['title'],seconds=sm[sid]['seconds'],src=url(sm[sid]['presentation']['path']),changed=sid in CHANGES) for sid in seq]
    page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · 光影与机位对照 v015</title><style>body{background:#10151f;color:#e9eef7;font:17px/1.7 system-ui;margin:auto;max-width:1400px;padding:28px}h1{font-size:32px}p{color:#bdc9da}a{color:#91bdff}section{margin:32px 0;padding:24px;background:#192131;border-radius:16px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0}img{width:100%;display:block;border-radius:8px}figcaption{padding:8px 0;color:#a5b8d0}button{background:#30517d;color:white;border:0;border-radius:8px;padding:10px 18px;cursor:pointer;margin:4px}.notice{border-left:4px solid #d5ad65;padding:14px;background:#2c2830}#film{max-height:69vh;object-fit:contain;background:#080b11}small{color:#9caec6}@media(max-width:850px){.pair{grid-template-columns:1fr}body{padding:14px}}</style>
<h1>把冲突从背景里拉出来</h1><p>三张对峙镜头重构，千问改为小鱼肩后略仰拍。保留原镜号、剧情、对白、镜长与已完成声音。</p>
<p class="notice">当前是新画面候选，尚未作为作者采用或视频准入通过。原千问r3被作者否定；本版成人手与扇子在画外，左抱右扇仍须动态验证。</p>
<nav><a href="../../视频制作/生成板-v015/生成板.html">生成板 v015</a> · <a href="全片声音预览.html#t=142.5">带声音看完整对峙</a> · <a href="../生成前修正-v014/修正交接.html">此前水龙、参考与声音修正</a> · <a href="视觉复核.md">独立视觉复核</a></nav>
<section><h2>顺着镜头看</h2><p>这段静帧轮看用于比较构图和光影，不代表实际运动。最后一张千问属于后续保护段。</p><img id="film"><p id="caption"></p><button id="prev">上一镜</button><button id="play">按镜长轮看</button><button id="next">下一镜</button><div id="shots"></div></section>'''+''.join(cards)+'''<p>“别碰她”、撑地失败、抓袍与离开镜头保留现有构图，后期轻收过亮地面和金饰，保持原光源方向；不批量重画已有效的表演。所有新图由内置 imagegen 生成，原件与拒用候选保留。</p><script>const D=__DATA__;let i=0,t=null,playing=false;function show(){clearTimeout(t);document.getElementById('film').src=D[i].src;document.getElementById('caption').textContent=D[i].title+' · '+D[i].seconds+'秒 · '+(D[i].changed?'本轮新候选':'保留原构图');if(playing)t=setTimeout(()=>{i=(i+1)%D.length;show()},D[i].seconds*1000)}document.getElementById('prev').onclick=()=>{i=(i+D.length-1)%D.length;show()};document.getElementById('next').onclick=()=>{i=(i+1)%D.length;show()};document.getElementById('play').onclick=()=>{playing=!playing;document.getElementById('play').textContent=playing?'暂停轮看':'按镜长轮看';show()};D.forEach((s,j)=>{const b=document.createElement('button');b.textContent=s.title;b.onclick=()=>{i=j;show()};document.getElementById('shots').append(b)});show();</script></html>'''
    (ROOT/FIX/'修正交接.html').write_text(page.replace('__DATA__',json.dumps(data,ensure_ascii=False)),'utf-8')
if __name__=='__main__':main()
