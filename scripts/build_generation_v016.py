"""Rebind three fan shots to closer camera and cyan-violet magic, preserving audio."""
import copy,hashlib,html,json,os,shutil
from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
OLD='视频制作/生成板-v015';OUT='视频制作/生成板-v016'
OLDFIX='后期/张力与机位-v015';FIX='后期/扇子法术-v016'
BASE='镜头设计/shot-plan-v0.60.json';SOURCE='镜头设计/shot-plan-v0.61.json'
REQ='镜头设计/生成记录/扇子法术-v061/请求.json'
MAGIC='青紫魔力沿既有金线/扇骨汇聚至单枚实体扇叶；飞行时仅薄光包边和短尾迹，碰撞时局部压亮碎散。蓝底花纹和细金实体刃始终可读，不变纯光刃、不复制多枚、不加巨大法阵。'
CHANGES={
'CY024A10':dict(
 framing='右手扇轴与解锁叶根极近斜侧特写，扇面越过画框',
 camera='贴近扇轴、沿扇骨斜拍，85mm近摄感；前景扇骨虚化，拇指/轴扣与外缘单叶解锁处清晰，轻随右腕上挑。',
 action='右拇指拨扣，甩腕开扇；青紫魔力从扇轴沿既有金色扇骨依次亮起，汇到外缘唯一实体叶，冷色微光映亮指尖。1.15秒叶根卡扣解锁、叶尖抬起；1.35秒同一叶才斜向上脱离，立即接伴飞。右手仍握余扇，左臂在画外托稳小鱼。',
 note='本图为魔力汇聚与解锁中的状态参考，不是闭扇首帧。仅最外一条扇褶宽的实体叶脱离；扇轴/手柄/其余扇面留手中，魔法不遮花纹。',
 effects='0.1秒扇轴短咔；0.2–0.9秒扇骨展开与轻微魔力嗡鸣；1.15秒卡扣响，1.35秒弹脱破空。避让GPT原速跨镜咏唱。',
 en='Oblique extreme macro beside the right-hand fan pivot; thumb unlocks, ribs spread and cyan-violet energy follows gold ribs into ONE outer physical leaf. At 1.15s the latch opens; at 1.35s the same narrow leaf releases upward. Fan stays in right hand; left arm supports child offscreen.'),
'CY024A11':dict(
 framing='刃尖贴近镜头的极特写，右上近尖与左下远尾形成透视缩短',
 camera='在刃尖侧前下方倒退伴飞，近刃清晰、方尾退远虚化；不绕叶、不滚转相机，背景柱廊竖向参照保持。',
 action='同一实体扇叶从左下向右上爬升，刃尖逼近镜头，叶尾向左下退远。青紫薄光贴住细金刃边，短尾迹只留在叶尾后方；叶面微旋仍读得出蓝底花纹。柱廊虚焦掠过，无敌方术矛或碰撞火花；接触前不下坠。',
 note='只一枚实体叶；薄光不是另一枚光刃。近尖远尾体现距离，背景仅作速度/高度参照，不能用歪斜柱线代替爬升。',
 effects='细促破风叠轻微法术尾音，尚无撞击声；GPT咏唱保持自然原速，子弹时间只改变视觉。',
 en='Track just ahead and below one ascending physical leaf. Tip upper-right near lens, square tail receding lower-left. A thin cyan-violet envelope hugs the gold edge with a short wake behind the tail; floral surface stays visible. No enemy spear or impact yet, no descent or camera roll.'),
'CY024A12':dict(
 framing='同轴约70度侧面低机位碰撞近景，比伴飞稍宽，交汇点占主位',
 camera='同侧绕开约70度低位定住两条上行轨迹交汇点；接触瞬间轻震，碰撞失速后才随叶片稍下倾。',
 action='扇叶从左下向右上击中从右下射向左上的唯一暗金术矛侧面。接触瞬间恢复常速，青紫薄光在接触处压成小弧面，白青亮点与少量青紫光屑局部碎散，实体叶保持完整；暗金术光偏折并向无人空处消散。撞后叶片失速才落向空侧廊；不提前下坠、不爆成满屏光团。',
 note='本图为首次接触瞬间，后续偏散/失速/坠落须按顺序演出。与前镜为同一枚实体叶，沿用相同材质花纹，不做叶宽或花纹形变插值。碎散的是魔力薄膜，不是实体扇叶碎片；不增加新的弹体或巨大法阵。',
 effects='一次清脆撞响加短促魔力碎散，尾音压为罩外闷声，接Kimi护持；同一句GPT咏唱跨切不断。',
 en='Cut about 70 degrees to a slightly wider low side view. One rising leaf strikes one oppositely rising dark-gold spear. Cyan-violet sheath compresses locally into a crescent, a small white-cyan core and a few magical shards; physical leaf remains whole. Spear deflects and disperses; only AFTER contact does the stalled leaf fall.')
}
def load(p):return json.loads((ROOT/p).read_text('utf-8-sig'))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def write(p,d):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def remap(d,oldh,h):
    if isinstance(d,dict):return {k:remap(v,oldh,h) for k,v in d.items()}
    if isinstance(d,list):return [remap(v,oldh,h) for v in d]
    if isinstance(d,str):return d.replace(OLD,OUT).replace(OLDFIX,FIX).replace(BASE,SOURCE).replace(oldh,h)
    return d
def run_renderer(name,entry='main'):
    path=ROOT/'scripts'/name
    text=path.read_text('utf-8').replace('视频制作/生成板-v014',OUT).replace('后期/生成前修正-v014',FIX).replace('镜头设计/shot-plan-v0.59.json',SOURCE)
    ns={'__file__':str(path),'__name__':'v016_adapter'};exec(compile(text,str(path),'exec'),ns)
    return ns[entry](ROOT) if entry=='build' else ns[entry]()
def update_script():
    p=ROOT/'剧本/白米饭-场景剧本-v0.59.md';text=p.read_text('utf-8')
    text=text.replace('版本：v0.59｜2026-10-26｜','版本：v0.60｜2026-10-27｜扇子近摄与青紫法术修订；其余剧情对白不变。历史基线：')
    text=text.replace('执行说明：原有镜头与声音时长以v0.57原速修复源为基线；内心戏两句已生成干声（待听审），术名改名后该句需以新日语「蒼竜出海（そうりゅうしゅつかい）」重新录制/替换。450.9秒旧声音预览尚不包含本段。下文历史章节中的旧试读秒数不作为当前执行时码。','执行说明：当前镜头源v0.61、生成板v016，共133镜464.4秒、63句原速日语。内心戏与新版术名已并入声音预览；本轮只改三张扇子机位与法术表现，配音/BGM保持。下文历史秒数不作为当前执行时码。')
    start=text.index('切千问右手与扇轴的极近特写')
    end=text.index('\n\n',text.index('千问在画外合拢余扇收回胸侧',start))
    paragraphs=[
'切千问右手扇轴与外缘叶根的极近斜侧特写，沿扇骨贴近拍摄，扇面越过画框。拇指拨扣后，扇骨依次展开；青紫魔力从轴心沿既有金线亮起，汇向唯一外缘实体叶，冷光映亮指尖。蓝底花纹、细金刃和手柄仍清楚，光不覆盖整张扇面。',
'外缘叶根卡扣解锁，叶尖微抬；同一枚狭长实体叶在镜末斜向上脱离，立即接伴飞。扇轴、柄与余扇始终留在右手，左臂画外持续托住小鱼，不换抱。镜长1.5秒，0.1秒轴扣、0.2–0.9秒展开、1.15秒叶扣、1.35秒释放；轻微法术嗡鸣避让GPT咏唱。',
'切刃尖侧前下方的贴近伴飞极特写。尖端在右上逼近镜头，方形叶尾向左下退远虚化；同一实体叶持续由左下向右上爬升。青紫薄光贴住金刃，短尾迹留在叶尾后方，原蓝底花纹可读。背景柱廊虚焦掠过，竖向参照保持，不滚转相机。此镜无敌方术矛或撞击，子弹时间只影响画面，GPT咏唱原速连续。',
'切同轴约70度的侧面低机位撞击近景，比上一镜稍宽，留少量柱廊和高处石檐交代半空。扇叶左下至右上、暗金术矛右下至左上，两条上升轨迹交汇。接触瞬间恢复常速，青紫薄光在接触处压成小弧面，白青亮点及少量青紫光屑局部碎散；实体扇叶完整，术光偏折并向无人空处消散。碰撞失速后，叶片才落向空侧廊，不提前下坠、不复制光刃或多弹、不加巨大法阵。千问在画外合拢余扇收回胸侧，左臂始终未松开小鱼。'
]
    text=text[:start]+'\n\n'.join(paragraphs)+text[end:]
    out=ROOT/'剧本/白米饭-场景剧本-v0.60.md';out.write_text(text,'utf-8')
def main():
    update_script();old=load(BASE);source=copy.deepcopy(old);sm={s['id']:s for s in source['shots']}
    jobs=load(REQ);chosen={j['id']:j for j in jobs if j.get('selected_for_v016')}
    assert set(chosen)==set(CHANGES)
    for sid,c in CHANGES.items():
        s=sm[sid];s['previous_presentation_v060']=copy.deepcopy(s['presentation'])
        s['presentation'].update(path=chosen[sid]['project_output'],visible=c['action'],status='扇子近摄与法术新候选，待作者审阅',missing='动作、魔法随动和接触后的失速须动态验证')
        s.update(framing=c['framing'],camera=c['camera'],action=c['action'],source_quote=c['action'],sound=c['effects'],visual_prompt=chosen[sid]['prompt'],generation_request=REQ)
        s['refs'].insert(0,dict(path=chosen[sid]['project_output'],role='v061当前候选'))
        s['invariants']=[v.replace('飞行镜无术光，碰撞镜才出现敌方术光。','飞行镜带自身青紫薄光但无敌方术矛；碰撞镜才出现敌方暗金术光。') for v in s['invariants']]
        s['invariants'] += [MAGIC,c['note']]
        s['final_static_review']=dict(version='v061',status='pending_author_review',review=FIX+'/视觉复核.md')
    source['continuity']['qwen_fan_intercept']=source['continuity']['qwen_fan_intercept'].replace('两秒含','1.5秒含')+' '+MAGIC
    source['continuity']['bullet_time']=source['continuity']['bullet_time'].replace('飞行镜无术光，碰撞镜才出现敌方术光。','飞行镜带自身青紫薄光但无敌方术矛；碰撞镜才出现敌方暗金术光。')
    source['continuity']['qwen_hand_review']='当前A0-v060-r2为肩后头肩紧近景，成人手与扇画外；左臂托抱右手持扇由连续调度约束，A10只见右手，不能无交代换抱。'
    source.update(title='《白米饭》带图分镜 v0.61 · 扇子法术近摄',version='v0.61',revision='v061',previous_source=BASE,story_script='剧本/白米饭-场景剧本-v0.60.md',subtitle='133镜 · 464.4秒 · 扇子三镜近摄与青紫法术候选',roughcut_preview=FIX+'/全片声音预览.html',audio_repair_plan=FIX+'/配音对位方案.json')
    source['revision_notes']=dict(scope='作者确认扇子更贴近与青紫魔力三阶段方案；3镜图与说明更新，镜长对白音轨保持。',previous_source_sha256=sha(BASE),previous_script_sha256=sha('剧本/白米饭-场景剧本-v0.59.md'))
    write(SOURCE,source);h=sha(SOURCE);oldh=sha(BASE)
    for p in (ROOT/OLD).glob('*.json'):
        if p.name not in ['展开数据.json','结构核验.json']:write(OUT+'/'+p.name,remap(load(p),oldh,h))
    plan=load(OUT+'/批次计划.json');plan.update(version='v016',output=OUT+'/生成板.html')
    for sid,c in CHANGES.items():
        plan['action_overrides'][sid]=c['action'];plan['shot_notes'][sid]=c['note']
        plan['execution_notes'][sid]=c['camera']+' '+MAGIC+' '+c['note']
    plan['navigation']['review']=FIX+'/修正交接.html';write(OUT+'/批次计划.json',plan)
    d=load(OUT+'/动态审查.json')
    for sid,c in CHANGES.items():
        d['batches']['GB019']['shots'][sid].update(camera_zh=c['camera'],camera_en=c['en'],action_en=c['en'],effects_zh_override=c['effects'],effects_en='Soft magical resonance follows the physical motion; existing Japanese chant remains continuous at natural rate.')
    write(OUT+'/动态审查.json',d)
    audit=load(OUT+'/对白复核.json');audit['localization_sha256']=sha(OUT+'/日语译配.json');write(OUT+'/对白复核.json',audit)
    for name in ['配音对位方案.json','BGM剪辑方案.json','实际BGM剪辑.json','作者确认选曲.json']:write(FIX+'/'+name,remap(load(OLDFIX+'/'+name),oldh,h))
    for name in ['BGM试听.wav','BGM试听.mp3','全片声音预览.mp3']:
        if not (ROOT/FIX/name).exists():shutil.copy2(ROOT/OLDFIX/name,ROOT/FIX/name)
        assert sha(FIX+'/'+name)==sha(OLDFIX+'/'+name)
    mix=load(FIX+'/实际BGM剪辑.json');mix.update(source_sha256=h,voice_plan_sha256=sha(FIX+'/配音对位方案.json'),bgm_plan_sha256=sha(FIX+'/BGM剪辑方案.json'))
    mix['visual_revision_audio_reuse']=dict(from_manifest=OLDFIX+'/实际BGM剪辑.json',sha256=sha(OLDFIX+'/实际BGM剪辑.json'),reason='Three visual fan shots only; all audio outputs byte-identical; added magical SFX remain specified, not rendered.')
    assert mix['voice_events']==load(OLDFIX+'/实际BGM剪辑.json')['voice_events'];write(FIX+'/实际BGM剪辑.json',mix)
    run_renderer('build_generation_v014.py');run_renderer('build_previs_v014.py','build');review_page(old,source)
    assert [(s['id'],s['seconds'],s.get('subtitle_cues')) for s in old['shots']]==[(s['id'],s['seconds'],s.get('subtitle_cues')) for s in source['shots']]
    write(FIX+'/画面修订核验.json',dict(status='passed',source_sha256=h,changed_shots={sid:dict(path=sm[sid]['presentation']['path'],sha256=sha(sm[sid]['presentation']['path'])) for sid in CHANGES},audio_outputs_identical=True,timing_dialogue_unchanged=True,author_adoption=False,video_generated=False))
    run_renderer('verify_generation_v014.py')
def review_page(old,new):
    om={s['id']:s for s in old['shots']};sm={s['id']:s for s in new['shots']}
    def url(p):return quote(os.path.relpath(ROOT/p,ROOT/FIX).replace('\\','/'),safe='/#')
    cards=[]
    for sid,c in CHANGES.items():
        cards.append('<section><h2>'+html.escape(sm[sid]['title'])+'</h2><p>'+html.escape(c['camera'])+'</p><div class="pair"><figure><figcaption>上一版</figcaption><img src="'+url(om[sid]['presentation']['path'])+'"></figure><figure><figcaption>近摄与法术新候选</figcaption><img src="'+url(sm[sid]['presentation']['path'])+'"></figure></div><p>'+html.escape(c['action'])+'</p><a href="全片声音预览.html#t='+str(sm[sid]['start_second'])+'">带原配音与BGM看这一镜</a></section>')
    seq=['CY024A0','CY024A9','CY024A10','CY024A11','CY024A12','CY024A1']
    data=[dict(title=sm[sid]['title'],seconds=sm[sid]['seconds'],src=url(sm[sid]['presentation']['path'])) for sid in seq]
    page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · 扇子近摄与法术 v016</title><style>body{background:#111521;color:#edf1ff;font:17px/1.7 system-ui;max-width:1400px;margin:auto;padding:28px}h1{font-size:32px}p{color:#bfcae0}a{color:#a3baff}section{margin:28px 0;padding:24px;background:#1b2334;border-radius:16px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0}img{width:100%;display:block;border-radius:8px}figcaption{padding:8px 0}button{padding:10px 16px;margin:4px;border:0;border-radius:8px;background:#4a477b;color:white;cursor:pointer}.notice{border-left:4px solid #a193fa;padding:16px;background:#26243b}#film{max-height:68vh;object-fit:contain}@media(max-width:850px){.pair{grid-template-columns:1fr}body{padding:14px}}</style>
<h1>开扇蓄力 → 贴刃伴飞 → 半空截击</h1><p>镜头更贴近，青紫魔力沿同一枚实体扇叶连续变化。扇面花纹、金属刃与原动作因果保留。</p>
<p class="notice">三张新候选待作者审阅。配音、BGM、镜长不变；魔力嗡鸣与碎散音效仅已设计，尚未制作。静帧不证明飞行、接触与失速已经实现。</p>
<nav><a href="../../视频制作/生成板-v016/生成板.html">生成板 v016</a> · <a href="全片声音预览.html#t=263.05">带声音看连续段落</a> · <a href="../张力与机位-v015/修正交接.html">此前对峙与千问修订</a> · <a href="视觉复核.md">独立视觉复核</a> · <a href="../../镜头设计/生成记录/扇子法术-v061/请求.json">生成提示词与来源</a></nav>
<section><h2>前后镜头连看</h2><p>用于检查画面衔接；千问叮嘱后中间有GPT展翼镜，此处缩略轮看省略，完整顺序见带声音预览。</p><img id="film"><p id="caption"></p><button id="prev">上一镜</button><button id="play">按镜长轮看</button><button id="next">下一镜</button><div id="shots"></div></section>'''+''.join(cards)+'''<script>const D=__DATA__;let i=0,t=null,playing=false;function show(){clearTimeout(t);document.getElementById('film').src=D[i].src;document.getElementById('caption').textContent=D[i].title+' · '+D[i].seconds+'秒';if(playing)t=setTimeout(()=>{i=(i+1)%D.length;show()},D[i].seconds*1000)}document.getElementById('prev').onclick=()=>{i=(i+D.length-1)%D.length;show()};document.getElementById('next').onclick=()=>{i=(i+1)%D.length;show()};document.getElementById('play').onclick=()=>{playing=!playing;document.getElementById('play').textContent=playing?'暂停轮看':'按镜长轮看';show()};D.forEach((s,j)=>{const b=document.createElement('button');b.textContent=s.title;b.onclick=()=>{i=j;show()};document.getElementById('shots').append(b)});show();</script></html>'''
    page=page.replace('#t=263.05','#t='+str(sm['CY024A9']['start_second']))
    (ROOT/FIX/'修正交接.html').write_text(page.replace('__DATA__',json.dumps(data,ensure_ascii=False)),'utf-8')
if __name__=='__main__':main()
