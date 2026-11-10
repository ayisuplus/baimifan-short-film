"""Freeze v0.9 editorial revision and one-image-per-shot generation requests."""
import copy,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1]
target=R/'镜头设计/shot-plan-v0.9.json'
assert not target.exists(),'Inspect existing v0.9 rather than overwrite'
d=json.loads((R/'镜头设计/shot-plan-v0.8.json').read_text(encoding='utf-8'))
old=copy.deepcopy(d); shots={s['id']:s for s in d['shots']}
script=(R/d['story_script']).read_text(encoding='utf-8').replace('版本：v0.8｜2026-10-21','版本：v0.9｜2026-10-22')
q={
 'wait':'DeepSeek 躲在教堂本体侧墙的阴影里，身边就是低矮破洞。她等到最后一盏灯转入侧院，才挪到洞口。',
 'snag':'鲸鱼帽子的侧鳍被凸出的石沿挂住。DeepSeek 卡在洞口，皱眉屏住呼吸，两只小手把软帽往下压，试着让侧鳍脱开。',
 'crawl':'软帽脱开石沿。她将头肩从同一左侧墙洞挤入，双手撑住堂内地面，再把身体拖进来。',
 'notice':'Claude 低头看见远处的 DeepSeek，先是一怔，随即忧虑地轻轻摇头，示意她不要靠近。',
 'pull':'DeepSeek 踮起脚试着掰锁，扣锁纹丝不动。她改为握紧腰前横链往外拉，锁链撞上木架，发出清脆的响声。',
 'breath':'DeepSeek 倒在台阶下，手肘撑住地面，想再站起来，手臂却软了下去。她喘着气，望向身旁教主的袍尾。',
 'up':'从湿石地面向上仰望，白紫水龙和黑金鸦翼教主沿高耸石柱之间拔地腾空，一前一后穿过中殿已经破开的穹顶。',
 'above':'两人已经来到教堂上空。白紫水龙盘起长身，黑金鸦翼教主悬在对面，两道力量隔着夜空对峙。',
 'outside':'从高处俯视雨中的整座教堂和周围空地。中殿破口露出殿内闪光，后殿拱顶仍完整。窗内与门口交替闪出橙金、紫白魔法火光，几次短促爆闪和闷响带过殿内交战；建筑没有持续起火。'
}
replacements={
 shots['CY010A']['source_quote']:q['wait'],
 '鲸鱼帽子被石沿挂住，她停下来，用两只手把帽子扯过来，继续往里挤。':q['snag']+'\n\n'+q['crawl'],
 'Claude 看见她，先是惊讶，随即急切地摇头。':'',
 '她踮起脚，先试着掰开身前锁链上的扣锁。小小的手指找不到能够打开的地方。\n\n她又抓住横在 Claude 身前的锁链，用力往外拉。\n\n锁链撞上木架，发出清脆的响声。':q['pull'],
 'DeepSeek 倒在台阶下。她撑住地面，想再站起来，手臂却软了下去。':q['breath'],
 '教堂外，一声尖锐的鸣响划过夜空。高处的窄窗短暂映亮，随即归于黑暗。此时不揭示信号的来源。':'',
 '最后，ChatGPT 回到宫殿高台，抬手将一道信号光送上夜空。这就是 CY021 中映亮教堂窄窗的同一次集合信号，重复同一声短鸣，不再发第二次。':'',
 '信号短鸣收尾，硬切回教堂并恢复空旷的殿内回声。':'最后一声回应落下，硬切回教堂并恢复空旷的殿内回声。',
 shots['CY027C']['source_quote']:q['up']+'\n\n'+q['above'],
 shots['CY027E2']['source_quote']:q['outside'],
 'ChatGPT 发出召集信号，最终带其他 AI 娘到场。':'ChatGPT 亲自邀约，最终带其他 AI 娘到场。'
}
for a,b in replacements.items():
 assert a in script,a
 script=script.replace(a,b)
anchor='她落在教堂内侧的地上，忍住声音，抬起头。'
script=script.replace(anchor,anchor+'\n\n'+q['notice'])
script+='\n\n- v0.9：恢复鲸帽挂石沿→脱开钻入；空堂空间与Claude察觉分开；试锁并入拉链，保留听声停手；撤下集合信号，亲访邀约回闪直接回当前救援；新增殿内向上腾空，教堂外战斗省略改远俯视。分格镜逐镜独立重画，旧稿保留。\n'
def upd(id,key,**kw):
 shots[id].update(action=q[key],source_quote=q[key],**kw)
def add(id,anchor,key,seconds,title,framing):
 s=copy.deepcopy(shots[anchor]);s.update(id=id,seconds=seconds,title=title,framing=framing,purpose=title,action=q[key],source_quote=q[key],dialogue='无对白',dialogue_cues=[])
 s.pop('time_caption',None);shots[id]=s
upd('CY010A','wait',exit_state='最后一盏灯消失，宝宝挪到同一墙洞，尚未钻入。')
upd('CY011','snag',seconds=3,framing='洞口内侧贴地近景',entry_state='宝宝探头进入，软鲸帽侧鳍碰上凸石。',exit_state='帽子仍被石沿挂住，小手向下压住软帽。')
add('CY011A','CY011','crawl',2,'脱开石沿，挤进空堂','洞口内侧低位侧近景')
shots['CY011A'].update(entry_state='侧鳍在小手按压下脱开凸石。',exit_state='身体穿过同一左侧墙洞，轻落地，准备抬头观察。')
shots['CY012'].update(framing='空堂空间远景／宝宝在左前景',entry_state='宝宝已从左侧墙洞入殿，蹲在洞内侧。',action='宝宝抬头观察空长椅、中央通道和远处祭坛；堂内只有受缚的Claude。',exit_state='视线落在Claude身上，接她察觉宝宝的反应。')
upd('CY013','notice',seconds=3,title='她发现了宝宝',framing='宝宝视线方向的Claude中近景／略仰视',purpose='接空间远景，转入Claude的担心。',entry_state='Claude察觉侧墙传来轻响，低头看向宝宝。',exit_state='她轻轻摇头，但宝宝仍准备靠近。')
upd('CY016','pull',seconds=5,title='试锁，再拉链',entry_state='宝宝站上平台，手刚够到腰前扣锁。',exit_state='拉链无果，她换站位继续尝试；教徒尚未返回。',framing='双人侧近景／宝宝试扣转为拉紧横链')
upd('CY021','breath',seconds=2,title='还想站起来',entry_state='宝宝被推倒在阶下，教主就在旁边。',exit_state='她站不起来，转而伸手抓住身旁袍尾。',sound='急促喘息、衣料擦地；没有信号鸣响。',framing='贴地近景／宝宝撑地')
shots['CY026E'].update(title='各路回应',exit_state='五格都亮，回应结束，直接切回当前教堂施法。')
add('CY027B3','CY027B2','up',3,'穿过破顶腾空','殿内贴地大仰角／垂直向上')
shots['CY027B3'].update(entry_state='白紫水龙与鸦翼教主已在中殿完成变身。',exit_state='双方穿过已有中殿破口，接外景空中对峙。',sound='龙躯掠空、羽翼振动，回声随穿顶开阔。')
upd('CY027C','above',seconds=2,framing='教堂外空中中远景',entry_state='两人已穿过中殿破口，来到屋顶上方。',exit_state='双方凌空相对，宝宝抬头看见水龙。')
upd('CY027E2','outside',framing='高空斜俯视大远景／教堂与周边空地',purpose='在整体空间内，用闪光和声音省略殿内交战。')
ids=[s['id'] for s in old['shots'] if s['id'] not in ['CY015A','CY026']]
ids.insert(ids.index('CY011')+1,'CY011A');ids.insert(ids.index('CY027C'),'CY027B3')
seq=[shots[i] for i in ids];t=0
for i,s in enumerate(seq):
 if s['source_quote'] not in script and s['source_quote'] in replacements:
  s['source_quote']=replacements[s['source_quote']]
 assert s['source_quote'] in script,(s['id'],s['source_quote'])
 s.update(start_second=t,end_second=t+s['seconds']);t+=s['seconds']
 nxt=seq[i+1] if i+1<len(seq) else None
 s['next_link']=f"接 {nxt['id']}：{s['exit_state']} → {nxt['entry_state']}" if nxt else '结束。'
 s['invariants']=[v for v in s['invariants'] if not any(x in v for x in ['信号','穿云尖鸣','同一次鸣响'])]
 s['editorial_review']=dict(version='v009',status='candidate_static_review',dynamic_execution='pending')
 s['visual_prompt']=f"《穿云》{s['id']}。{s['action']} 开始：{s['entry_state']} 结束：{s['exit_state']}。人物设计延续原图，画面无字。"
d['shots']=seq;d['continuity'].pop('signal',None)
d['continuity']['invitation']+=' 亲访和逐一回应是召集的全部因果；取消发箭与窄窗信号，回闪在最后回应后结束。'
d['continuity']['infiltration']='侧墙等待→鲸帽侧鳍挂石沿、双手压软帽→脱开钻入→空堂空间→Claude发现宝宝。帽子卡住必须在画面中可见。'
d['continuity']['combat']='变身→殿内贴地向上腾空穿破口→外景空中对峙→宝宝龙影→原天空雷雨→地板雨滴→同伴迎敌→教堂远俯视爆闪→战后。'
d.update(version='v0.9',revision='v009',created='2026-10-22',title='《穿云》带图分镜 v0.9',total_seconds=t,story_script='剧本/穿云-场景剧本-v0.9.md',source_manifest='镜头设计/生成记录/生成索引-v009.json',origin_manifest='镜头设计/生成记录/逐镜独立-v009/输出归档.json',subtitle=f'六场 · {len(seq)} 镜 · {t//60} 分 {t%60} 秒。恢复鲸帽卡住、合并重复动作、独立单镜重画。',roughcut_preview_label='旧版配乐粗剪 v002（未包含当前v0.9调整）',review_intro='恢复鲸帽受阻与脱开，分开空间交代和人物反应；删重复试锁与集合信号，增加殿内仰视腾空，战斗外景改远俯视。',review_focus='核对鲸帽触石、人物视线、试锁与听声停手差别、腾空方向、教堂远俯视。逐镜独立图为新候选，动态仍待制作。')
d['revision_notes']=dict(previous_manifest='镜头设计/shot-plan-v0.8.json',previous_html='镜头设计/带图分镜-v0.8.html',added_ids=['CY011A','CY027B3'],retired_ids=old['revision_notes']['retired_ids']+['CY015A','CY026'],retirement_reason='CY015A试扣并入CY016；CY026发箭与CY021窗闪因亲访邀约已完成而撤下。',boundary='静帧图像与剧本重排，沿用临时声音；未重导配乐粗剪，作者待审阅。')
layouts={p['path']:p for p in old['page_layouts']}
jobs=[];outdir=R/'镜头设计/图像/独立镜头-v009';outdir.mkdir(parents=True,exist_ok=True)
rec=R/'镜头设计/生成记录/逐镜独立-v009';rec.mkdir(parents=True,exist_ok=True)
special={
 'CY011':'重构画面：镜头在墙洞内侧贴地，宝宝仅头和肩探进来，身体仍在洞外；软鲸帽的一只侧鳍明确勾在洞口上沿向内突出的石角，帽子被扯偏，宝宝皱眉，双手向下压软帽想解困。画出帽布和凸石接触受力点。她还没钻进来。',
 'CY011A':'镜头位置和洞口与参考右上格相同；帽子已松脱，头肩朝画面右方钻入暖光内堂，身体还从左侧墙洞挤入。双手撑地，动作接上一镜。',
 'CY013':'彻底改变原远景构图：从宝宝目光方向略仰视Claude的胸部以上中近景。Claude橙发、花饰和头纱，背靠木架，手臂向两边受缚伸出画外；低头望画外左下方宝宝，惊讶转为担忧，微微摇头。不是幼童脸，无笑容。无其他人入画。不需要看到脚、台阶、全十字架。',
 'CY021':'保留宝宝灰尘沾衣、伏地撑肘的努力与眼泪；去掉窗外强蓝色信号光，窗户暗淡。构图缩近宝宝，画面右边缘可见教主垂下的黑金袍尾，宝宝尚未抓住，下一镜才抓。地板此时干燥无积水，天瀑尚未发生。',
 'CY027B3':'全新机位：摄像机放在教堂中殿地板，镜头垂直朝上。高耸石柱与破裂穹顶边缘形成向上汇聚的透视。白紫长身水龙近处掠过镜头向穹顶洞口上升，黑金鸦翼人形教主稍远也升向同一个破口，可见两者腹部或背下方的缩短透视，水滴和披袍向下拖曳。洞外夜空。不是屋顶上方平视对峙，不要人形GPT和龙同时出现。',
 'CY027E2':'将参考教堂改成从高空斜上方俯视的大远景，镜头比原图拉远，完整教堂和四周空地可见，教堂只占画面约一半。保留双塔正门、长中殿、后殿结构，中央中殿穹顶有已被天瀑冲开的一个破口，后殿屋顶完整。雨夜、门窗及破口短暂透出魔法爆闪，无天空战斗人物，无整座建筑持续燃烧。'
}
for s in seq:
 src=s['presentation']['path'];layout=layouts[src]
 if layout['cols']*layout['rows']==1 and s['id'] not in special:continue
 n=s['panel_index'];row=n//layout['cols']+1;col=n%layout['cols']+1
 selection=f"第一张参考是{layout['rows']}行{layout['cols']}列的旧分镜页，仅取第{row}行第{col}列的这一镜作人物、场景和构图依据，忽略其他格。" if layout['cols']*layout['rows']>1 else '第一张参考是本镜旧稿，沿用其人物与世界美术。'
 prompt=f"为哥特式异世界动画短片《穿云》重画一个独立镜头：{s['id']}，{s['title']}。输出一张完整16:9横向电影静帧，精细绘制、清晰细节，延续参考的精致日系动画插画、体积光、材质笔触。{selection}这是重新绘制单幅原画，不是裁切放大参考，不是拼版，不要边框、分格、标题或任何文字。\n镜头：{s['framing']}。动作：{s['action']}\n{special.get(s['id'],'保持所选格的主体、表情与站位，完整重构为16:9单帧。')}"
 refs=[str(R/src)]
 if s['id'] in ['CY011','CY011A']:
  refs.append(str(R/'概念参考/02-DeepSeek-母版概念参考.webp'));prompt+=' 第二张仅作宝宝身份参考：圆脸、鲸帽、短小身形；不带饭碗。'
 if s['id']=='CY013':refs.append(str(R/'概念参考/01-Claude-母版概念参考.webp'));prompt+=' 第二张仅作Claude脸、头发、花饰和头纱身份母本。'
 if s['scene'] in ['S03','S04','S05'] and not s['id'].startswith('CY026'):
  prompt+=' 若画面能看到祭坛，只能有三级宽低石阶接单一平平台，无侧阶；阶下左右各一个铜盆。Claude受缚时赤足踩竖柱脚托，低柴在两侧；近景不必硬塞全坛。'
 if s['id'] in ['CY003B']:prompt+=' 眼神忧郁低垂，暗琥珀虹膜里的宝宝倒影柔和微弱，不画炯炯有神的高亮眼睛。'
 if s['id']=='CY027E':prompt+=' 保留参考该格天空与两侧钟楼的构图，不画交战人物；雨线和一道云间闪电暗示战斗。'
 if s['id']=='CY027B1':prompt+=' 定格在白紫龙躯已经显形、少女人形正在水光中消散的变身瞬间；不是召唤一条独立宠物龙。'
 if s['id']=='CY027D':prompt+=' 九位各具特征的AI同伴错落迎敌，其中千问留在后侧抱护蓝鲸宝宝；GPT已经在天上，不出现在堂内队伍。'
 args=dict(prompt=prompt,referenced_image_paths=refs,transparent_background=False)
 job=dict(id=s['id'],source=src,source_panel=n,destination=f"镜头设计/图像/独立镜头-v009/{s['id']}-v009.png",request=args)
 jobs.append(job)
 (rec/f"{s['id']}-请求.json").write_text(json.dumps(job,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Important altered shots first; every remaining crop is still queued exactly once.
priority=['CY011','CY011A','CY013','CY021','CY027B3','CY027E2','CY016','CY010A','CY027C']
jobs.sort(key=lambda j:priority.index(j['id']) if j['id'] in priority else 100+ids.index(j['id']))
(rec/'计划.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for sc in d['scenes']:
 ss=[s for s in seq if s['scene']==sc['id']];sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)))
used={s['presentation']['path'] for s in seq};d['page_layouts']=[p for p in old['page_layouts'] if p['path'] in used]
(R/d['story_script']).write_text(script,encoding='utf-8')
snapshot=R/'镜头设计/带图分镜-v0.8.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
target.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(shots=len(seq),seconds=t,generation_jobs=len(jobs),order=[j['id'] for j in jobs]),ensure_ascii=False))
