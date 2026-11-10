"""Author's detail, eyeline, exterior entrance and restrained shield-side water revision."""
import copy, hashlib, json, shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/细节与显形-v052'
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def save(p,v):
 q=R/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=load('镜头设计/shot-plan-v0.51.json');p=copy.deepcopy(base)
old={s['id']:s for s in base['shots']};by={s['id']:s for s in p['shots']}
script=(R/base['story_script']).read_text(encoding='utf-8')
actions={
'CY021A':'Claude的父亲穿着教主礼服走到长阶下端。一名教徒递来唯一的仪式火把，杯口燃着黑芯、暗紫细边的火焰；教主右手接牢，抬头望向被高柴围住的Claude。固定火盆和蜡烛仍是普通暖色火，不随仪式火把变黑。',
'CY020B':'固定机位从小鱼侧面看向教主。小鱼站在长阶下端，双臂仍张开挡路，抬头直视教主；教主高她一截，垂眼看她，嘴角带一点轻蔑，肩膀放松，身体没有前冲。右手持同一支黑焰火把，左臂垂下，两人之间留有距离。这一镜只保持相互凝视，不推、不摔，不以夸张透视拉长肢体。',
'CY020A':'接上一镜静止对视，切近阶下。教主左手从画边推开挡路的小鱼，右手仍持火；小鱼失衡倒向同一片地面。落地后她用手肘撑地，想再站起来，手臂却软下去，喘着气望向身旁教主的袍尾。现有静帧只表示倒地后的终态，推开起点与落地轨迹留待动态制作，不把静态对视误当成已经推过。',
'CY022A':'教主右手持同一支黑焰仪式火把，向长阶迈步，衣角从小鱼手中滑脱；高处柴堆仍未燃。普通固定火盆、蜡烛火色不变。',
'CY022A1':'背后低机位沿长阶中轴望向Claude。教主右手握着同一支黑焰仪式火把，头、肩、骨盆及双脚都朝向最高祭坛，背对镜头一步一步上阶；不回头，不侧身偏向画面右侧。前脚踩上高一级石阶，后脚跟进，披风顺背向下拖曳。高处Claude直立受缚，腰腹以下仍陷在黑木堆里，小鱼留在下端。固定火盆与蜡烛仍是普通暖色火。',
'CY022':'近处，教主将右手黑焰火把压向高高堆起的乌烬木下侧。同一种黑芯暗紫细边的火舌从火把接入木缝，树脂裂隙亮起细小余烬，黑焰沿层叠乌烬木向上蔓延，不再先有橙色火头再变黑。教主收回同一支火把，返回长阶下段；高柴的黑焰迅速连成一片，卷向刑架中央。',
'CY024K00':'切到教堂正后中央高窗外。Kimi在月光照亮的空中从稀薄暗影里凝成完整身形，头饰至靴尖全部入画，长发与裙摆被夜风向左牵起；她面朝右侧完整的蓝色中央彩窗，神情清醒而专注。左手低持小尺寸明刃，右手低持暗刃，双脚悬空，不踩月环，也不落到窗台。实月在身后远空，近处外墙与扶壁建立高度，少量暗影只从发梢裙尾散去。此镜留2.5秒音乐与风声，不重复呼唤、不提前投刃；玻璃、后殿拱顶仍完整。',
'CY024K0':'承接窗外全身显形，仍从窗外同侧切到Kimi半身近景，中央彩窗的完整玻璃与石框留在画面右缘。她清晰可见地望向窗内，左手将小尺寸明刃抬到肩旁，右暗刃仍低持；长发向同一方向飘动，不再隔着玻璃显示模糊影子。她说出完整请求句，末尾留半拍，左臂随后朝右前方甩出明刃，接下一镜从殿内看明刃破窗。Kimi本人仍在窗外，双刃左右手不交换；此刻不出现护罩、阵纹或额外月环。',
'CY024A9':'教主仍在下段中央缓台，视线锁定高处GPT。低机位贴近他的右臂和侧脸，右肩带动手臂向左上方猛然推出，左臂后收稳住重心，黑金袍摆被发力带起。一枚暗金术矛从掌前迸出，掌根近处有厚实的短促压光，矛体越远越收细，朝高处GPT疾射。攻击只有这一枚离手的实体化术光，不是不断供能的巨炮，也不增加多弹；后镜千问用单枚扇叶偏转它的侧面轨迹。他未变身、未开罩，屋顶此时完整。',
'CY024B3':'切祭坛左侧的斜侧高机位，暗月罩位于上层平台中后景，表面平静且完全不透明。水龙已经化散；罩边只剩湿石面上的浅水、细涟漪和低缓退浪，可以流到罩脚附近，不再刻意留干燥隔离带。少量余水沿两侧外阶向低处排走，在台阶落差处翻起小水花，没有围罩的高水墙，也不做左右完全对称的浪槽。普通灯火已灭，中央后窗保留破口，侧窗和后殿完整。护罩主要防教徒法术，GPT的主龙和高压冲击只指向敌方；此镜罩面不受冲撞、罩内仍平静。',
'CY024B1':'镜头切到更低的外侧台阶，贴近水面斜拍汇向下方的余浪。前景一名黑金袍教徒身体被水推向下游，扭身伸手抓湿石沿，指尖刚刚滑脱；腰胸被厚水遮住，袍摆顺水拉开。中景另一人侧向失足，后景第三人转身抬手却来不及，前后位置和姿态错开，不再整齐排成一行。一根法杖脱手顺流打转，近前景浪头越过一级石阶，以深蓝水腹和局部白沫体现重量，人物不飞天。远处上层暗月罩边只有低缓浅水，近处较大的浪来自下层台阶汇流；不把上层罩边重新画成水墙。',
'CY027F':'战斗结束，雨渐停。ChatGPT已恢复人形，稳稳站在湿地，膜翼自然收拢，双臂松松交抱在身前。她略侧头、垂眼看向前景倒下的教主，眉梢轻抬，嘴角带一点冷淡的讥讽；视线落在敌人的脸上，不看镜头，也不提前弯腰取钥匙。教主与教徒倒地，八位同伴在下层收势，千问仍抱着小鱼；Kimi继续在最高祭坛守护Claude。停住这一眼后，GPT才松开双臂、转看腰间钥匙，接下一镜取钥匙。'
}
new=copy.deepcopy(by['CY024K0']);new.update(id='CY024K00',title='窗外月光，全身显形',seconds=2.5,dialogue='无对白',dialogue_cues=[],subtitle_cues=[],asset_ids=['MULKZI2WMFNJE','ENV-CHURCH'],entry_state='教主与教徒仍被正门牵住注意，Kimi呼唤已在画外完成。',exit_state='Kimi全身显形，仍悬于完整中央彩窗外，双刃低持。',framing='窗外斜侧全身，月亮在远处、外墙与完整彩窗在近处',purpose='先明确Kimi真实存在于窗外，再切近景举刃投射。',sound='短暂保留月影渡呼唤尾韵、夜风与Kimi专属BGM，不追加台词。',refs=[])
for key in list(new):
 if key.startswith('previous_'):del new[key]
at=p['shots'].index(by['CY024K0']);p['shots'].insert(at,new);by[new['id']]=new
framing={
'CY020B':('静止对视，高低之间','平视小鱼高度的侧面双人中景，固定50mm，建立相互视线'),
'CY024K0':('窗外近景，举刃请门','窗外同侧半身近景，右缘保留完整玻璃，面容与握刃清楚'),
'CY024A9':('掌前爆发，暗金术矛','低机位近中景，右臂强透视指向左上，脸和发射口同框'),
'CY024B3':('罩边浅水，余浪下行','左侧斜俯中远景，不对称构图，罩小于原正面全景占比'),
'CY024B1':('汇流冲人，指尖抓空','外侧下层台阶贴水低机位，前中后景错落，顺水斜向构图'),
'CY027F':('垂眼讥笑，胜负已分','保留原群像，GPT直立抱臂，目光向前景倒下的教主')}
for sid,a in actions.items():
 s=by[sid];s['action']=a;s['presentation']['visible']=a
 if sid in framing:s['title'],s['framing']=framing[sid]
 if sid in old:
  q=old[sid]['source_quote'];tail=''
  if sid in ['CY021A','CY024K0']:tail=q[q.index('\n\n'):]
  if sid=='CY024A9':tail=q[q.index('\n\n'):]
  s['source_quote']=a+tail;assert q in script,sid;script=script.replace(q,s['source_quote'],1)
 else:s['source_quote']=a
script=script.replace(by['CY024K0']['source_quote'],new['source_quote']+'\n\n'+by['CY024K0']['source_quote'],1)
by['CY020B'].update(entry_state='Claude喊完别碰她，小鱼仍张臂挡住教主。',exit_state='两人对视僵持，尚未发生推搡；下一镜开头教主才出手。',sound='脚步短停、轻微衣料与火把黑焰低鸣；对视停留不加撞击声。',cinematic_beats=[dict(offset=0,intent='小鱼抬眼，教主垂眼'),dict(offset=1.2,intent='固定相互凝视，轻蔑表情停住')])
by['CY020A'].update(entry_state='承020B对视，教主在本镜开头左手推开；原图为落地后的终态。',sound='画边衣袖带动和一次推搡接落地衣料声，随后虚弱呼吸；不重放Claude喊话。',cinematic_beats=[dict(offset=0,intent='画边左手推开，身体失衡'),dict(offset=.7,intent='落地，手肘撑起又软下')])
by['CY024K0'].update(entry_state='K00全身显形已经完成，Kimi在窗外，双刃未投。',sound='夜风承前，0.1—5.5秒说出原请求句，末尾留半拍；下一镜玻璃爆裂。',cinematic_beats=[dict(offset=0,intent='同侧切近，面容与左明刃清楚'),dict(offset=2.2,intent='请求门扉，持刃抬至肩侧'),dict(offset=5.5,intent='收句半拍，朝右前投刃')])
by['CY024K00']['cinematic_beats']=[dict(offset=0,intent='月光中的全身从暗影凝实'),dict(offset=1.5,intent='悬空望向完整中央彩窗，双刃低持')]
by['CY024R']['exit_state']='教主仍盯正门，Kimi呼唤收尾；切窗外全身显形。'
by['CY024A9'].update(sound='短促掌前压光爆发接术矛上行破风，咏唱不断；攻击离手后不保留连续炮声。',cinematic_beats=[dict(offset=0,intent='视线锁定高处，右肩猛推'),dict(offset=.35,intent='单枚术矛离手，近粗远细')])
by['CY024B3'].update(entry_state='水龙命中敌方后已化散，上层平台只留浅水与低缓退浪。',exit_state='暗月罩边浅水缓行，罩内平静；切罩内安抚，再接下层外阶汇流。',sound='近处浅水细响、台阶小落水，远处低沉余浪；不加罩体受压声。',cinematic_beats=[dict(offset=0,intent='斜侧交代罩边浅水尺度'),dict(offset=1.5,intent='低缓退浪沿外阶向下排走')])
by['CY024B1'].update(entry_state='下层外阶承接上方退浪汇流，教徒刚被打断施法。',exit_state='教徒失衡沿侧阶下滑，浪头减弱，接GPT落地。',sound='近处厚浪拍阶，抓石手掌滑脱和一声惊呼，法杖擦水；高处罩边仍是轻水声。',cinematic_beats=[dict(offset=0,intent='近景浪推腰胸，手指滑离石沿'),dict(offset=1,intent='中后景错落失衡，法杖顺流'),dict(offset=2.4,intent='余水带人下阶，接落地')])
by['CY027F'].update(entry_state='战后恢复人形，教主已倒地，GPT站稳收翼。',exit_state='GPT结束垂眼讥笑，松臂转看腰间钥匙，接027F0。',sound='低处滴水、湿衣轻响与风声；没有新增嘲讽台词。',cinematic_beats=[dict(offset=0,intent='直立松抱双臂，目光落向倒地教主'),dict(offset=1.5,intent='嘴角冷淡一挑，停住轻蔑'),dict(offset=3.2,intent='松臂移目腰间，下一镜取钥匙')])

# Apply continuity decisions only to live descriptive fields, never frozen prompts/history.
replacements=[
('CY020B教主左手推开她、右手持火','CY020B静态对视，CY020A开头教主左手推开她、右手持黑焰火把'),
('全段只有一支手持火把：','全段只有一支黑芯暗紫细边的手持仪式火把，固定火盆蜡烛仍是普通暖火：'),
('CY024R先闻呼唤，K0窗外举刃说请求','CY024R先闻呼唤，K00窗外全身显形留白2.5秒，K0窗外近景举刃说请求'),
('在十字架正后中央高窗外的月光中显现剪影','在十字架正后中央高窗外的月光中显现全身'),
('K0窗外剪影','K00窗外全身显形、K0窗外近景举刃'),
('月下剪影举明刃','月光中全身显形后近景举明刃'),
('GPT主动控制水流避开祭坛中央，水在接触暗罩前分成两路，留出罩外净空间隔；暗罩不抵抗友方水流。','GPT的主龙与高压冲击只打敌方；罩边允许湿石面、浅水和低缓退浪，不刻意留干燥隔离带。罩内平静，暗罩不与友方水流对抗。'),
('水流从始至终远离最高祭坛和同伴','主龙与高压冲击远离同伴，最高祭坛罩边允许浅水与低缓退浪'),
('最高祭坛净空','最高祭坛罩边仅浅水低浪'),
('最高祭坛不透明暗月罩与中央上层石阶保持干燥净空','最高祭坛不透明暗月罩安稳，中央上层石阶允许湿润与浅水'),
('友方暗月罩与中央上层石阶仍保持干燥净空','友方暗月罩安稳，中央上层石阶允许浅水和低缓退浪'),
('水从两侧经过，罩与水保持间隔','水在外阶下行，罩边仅浅水低浪'),
('GPT的银蓝水流在碰罩之前主动转向侧道，不撞罩、不压凹、不触发应力纹。','GPT的主龙与高压水势只打敌方，罩边允许浅水低浪，不受冲撞、不压凹、不触发应力纹。'),
('B3安全区','B3罩边浅水'),
('罩内人物不可见；千问','罩内人物不可见；千问')]
def words(t):
 for a,b in replacements:t=t.replace(a,b)
 return t
skip={'path','refs','visual_prompt','generation_request','page_layouts','source_manifest','origin_manifest'}
def rewrite(x):
 if isinstance(x,str):return words(x)
 if isinstance(x,list):return [rewrite(v) for v in x]
 if isinstance(x,dict):return {k:(v if k in skip or k.startswith('previous_') else rewrite(v)) for k,v in x.items()}
 return x
p=rewrite(p);script=words(script);by={s['id']:s for s in p['shots']}
p['continuity']['ritual_fire']='CY021A接起的手持仪式火把已经是黑芯暗紫细边；CY022以同一黑焰点燃乌烬木，不再由橙火转黑。固定火盆蜡烛保持普通暖火直到水流扑灭。Kimi震柴后中央没有燃木，暗罩边后来可有浅水低浪。最后空刑架星火仍为橙金色。'

rows=load(REC+'/实际请求.json');image_ids={r['id'] for r in rows}
assert image_ids=={'CY018','CY021A','CY020B','CY022A','CY022A1','CY022','CY024K00','CY024K0','CY024A9','CY024B3','CY024B1','CY027F'}
for row in rows:
 sid=row['id'];s=by[sid];dest=R/f'镜头设计/图像/细节与显形-v052/{sid}-v052-r{row.get("rev",1)}.png';dest.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(row['source'],dest)
 with Image.open(dest) as im:w,h=im.size;im.verify()
 rel=dest.relative_to(R).as_posix();req=REC+'/'+sid+'.json'
 save(req,dict(row,output=rel,sha256=sha(dest),dimensions=[w,h],engine='built-in image_gen',status='pending_author_visual_review'))
 if sid in old:s['previous_presentation_v051']=old[sid]['presentation'];s['previous_generation_request_v051']=old[sid]['generation_request']
 s['presentation'].update(path=rel,visible=s['action'],status='v0.52细节与显形修订候选，待作者审阅',missing='静帧已检查；显形、投刃、推搡、洪流受力和视线移动待动态制作。')
 s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0,y=0,w=1,h=1),panel_index=0,visual_prompt=row['input']['prompt'],generation_request=req,editorial_review=dict(version='v052',status='pending_author_review'),final_static_review=dict(version='v052',status='pending_author_visual_review'))
 s['refs'].append(dict(path=rel,role='v0.52修订候选；历史原图保留'))
elapsed=0
for i,s in enumerate(p['shots']):
 s.update(start_second=elapsed,end_second=elapsed+s['seconds']);elapsed+=s['seconds']
 if i+1<len(p['shots']):s['next_link']='接 '+p['shots'][i+1]['id']+'：'+p['shots'][i+1]['entry_state']
for sc in p['scenes']:
 group=[s for s in p['shots'] if s['scene']==sc['id']]
 sc.update(shot_ids=[s['id'] for s in group],seconds=sum(s['seconds'] for s in group),pages=list(dict.fromkeys(s['presentation']['path'] for s in group)))
p['page_layouts']=[dict(path=path,rows=1,cols=1) for path in dict.fromkeys(s['presentation']['path'] for s in p['shots'])]
out='镜头设计/shot-plan-v0.52.json';music_path='后期/细节与显形-v052/作者确认选曲-v052.json'
p.update(version='v0.52',picture_revision='v052',report_revision='v052',title='《穿云》带图分镜 v0.52 · 月光显形、目光与水势修订',total_seconds=elapsed,subtitle='132镜 · 434秒 · 新图待作者审阅',story_script='剧本/穿云-场景剧本-v0.52.md',source_manifest='镜头设计/shot-plan-v0.51.json',audio_arrangement='后期/细节与显形-v052/预演编排.json',music_adoption=music_path)
p['review_intro']='小鱼蓝眼、黑焰仪式火把、静止对视；新增窗外Kimi全身月光显形并改近景举刃。教主攻击、下层洪流和GPT战后俯视重构；罩边仅浅水低浪。'
p['review_focus']='比较人物视线与手位、黑焰连续性、窗外显形到投刃的衔接，以及上层浅水和下层汇流的尺度。'
p['revision_notes']=dict(previous_manifest=p['source_manifest'],modified_image_ids=[s['id'] for s in p['shots'] if s['id'] in image_ids],added_ids=['CY024K00'],moved_ids=[],boundary='增加2.5秒月光显形镜；旧131镜时长、对白与既有语音保持。Kimi新增镜沿用已确认专曲，其余选曲不改。')
script=script.replace('版本：v0.51','版本：v0.52',1)
(R/p['story_script']).write_text(script,encoding='utf-8');save(out,p)
adopt=load(base['music_adoption']);adopt['version']='v052';adopt['previous']=base['music_adoption'];adopt['marks']['CY024K00']=adopt['marks']['CY024K0'];adopt['overrides']['CY024K00']=adopt['marks']['CY024K0']
adopt['source_plan']=out;adopt['source_plan_sha256']=sha(R/out)
adopt['confirmation']+=' v0.52新增Kimi窗外显形CY024K00，沿用作者已确认的Kimi出场专曲。'
prev_shots={r['shot']:r for r in adopt['shots']}
adopt['shots']=[dict(copy.deepcopy(prev_shots.get(s['id'],prev_shots['CY024K0'])),shot=s['id'],title=s['title'],start=s['start_second'],end=s['end_second'],scene=s['scene'],music_id=adopt['marks'][s['id']]) for s in p['shots']]
save(music_path,adopt)
audio=load(base['audio_arrangement']);audio= rewrite(audio)
for section in audio['sections']:
 if section['id']=='M13':section['note']='Claude选择与离殿；CY029父亲打断及CY029E反应期间的停乐待精剪，以稳定镜号对齐当前画面。'
audio['shot_overrides']['CY024K00']=copy.deepcopy(audio['shot_overrides']['CY024K0']);audio['shot_overrides']['CY024K00']['note']='新增窗外月光全身显形，沿用Kimi已确认专曲与候选。'
for s in p['shots']:
 if s['id'] in actions or s['id']=='CY024R':audio['effects'][s['id']]=s['sound']
audio.update(version='v052-detail-moon-seven-tracks',shot_plan=out,shot_plan_sha256=sha(R/out),previous=base['audio_arrangement'],adopted_music=music_path)
save(p['audio_arrangement'],audio)
assert len(p['shots'])==132 and elapsed==434
for s in p['shots']:
 assert s['source_quote'] in script,s['id']
 if s['id'] in old:
  assert s['seconds']==old[s['id']]['seconds']
  assert s['dialogue']==old[s['id']]['dialogue']
  assert s['dialogue_cues']==old[s['id']]['dialogue_cues']
  assert s.get('subtitle_cues')==old[s['id']].get('subtitle_cues')
  assert adopt['marks'][s['id']]==load(base['music_adoption'])['marks'][s['id']]
snapshot=R/'镜头设计/带图分镜-冲击机位-v051.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
save(REC+'/变更核验.json',dict(shots=132,seconds=434,new_id='CY024K00',new_seconds=2.5,changed_images=sorted(image_ids),existing_shot_durations='unchanged',existing_dialogue_and_audio='unchanged',existing_music_marks='unchanged',new_music=adopt['marks']['CY024K00'],source_passages='132 matched',dynamic_validation='pending'))
print(out)
