import copy, hashlib, json, shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
def load(path):return json.loads((R/path).read_text(encoding='utf-8'))
def save(path,obj):
 p=R/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=load('镜头设计/shot-plan-v0.52.json');p=copy.deepcopy(base);old={s['id']:s for s in base['shots']};by={s['id']:s for s in p['shots']}
script=(R/base['story_script']).read_text(encoding='utf-8')
rec='镜头设计/生成记录/余波与锁痕-v053'
# Finish the impact before cutting to the quiet aftermath and interior embrace.
block='\n\n'.join(old[i]['source_quote'] for i in ['CY024B3','CY024B3A','CY024B1'])
assert block in script
script=script.replace(block,'\n\n'.join(old[i]['source_quote'] for i in ['CY024B1','CY024B3','CY024B3A']),1)
moving=by['CY024B1'];p['shots'].remove(moving);p['shots'].insert(p['shots'].index(by['CY024B3']),moving)
def action(sid,text):
 s=by[sid];q=s['source_quote'];s['action']=text;s['presentation']['visible']=text
 if sid=='CY028C':n=text+'\n\n**Claude（画外，接上句）：**\n的微光啊，'
 else:n=q.replace(old[sid]['action'],text) if old[sid]['action'] in q else q
 if sid=='CY024B3A':assert n!=q
 if n!=q:
  global script
  assert q in script;script=script.replace(q,n,1);s['source_quote']=n
action('CY024B3A',old['CY024B3A']['action'].replace('Claude听见外面轰鸣','外面的冲击已经结束，Claude听着渐远的余水声'))
by['CY024B3A']['title']='余声渐远，靠肩安抚'
by['CY024B3A']['entry_state']='大招冲击结束，上层只留浅水，暗月罩仍安稳。'
by['CY024B3A']['exit_state']='Claude在Kimi怀侧慢慢放松，GPT在外收势准备落地。'
by['CY024B3A']['sound']='隔着暗膜的余水声逐渐变轻，近处轻呼吸；不再传来新的撞击轰鸣。'
by['CY024B1']['exit_state']='洪流将教徒带离施法位置，浪势消退；接B3大招结束后的环境余波。'
by['CY024B1']['cinematic_beats'][-1]['intent']='余水带人下阶，冲击结束，接浅水环境'
by['CY024B3'].update(title='大招余波，浅水空殿',purpose='结束冲击段落，用静环境和渐轻的水声给观众一次呼吸。',entry_state='承B1教徒被冲散，主龙与冲击浪均已结束，只剩排水余波。',exit_state='安稳暗罩留在冷月空殿，接罩内靠肩安抚。')
by['CY024B3']['sound']='承上一镜厚浪声迅速衰减，留下浅水滴落与殿内空旷回响；音乐从冲击重音收为余韵。'
by['CY024B3']['cinematic_beats']=[dict(offset=0,intent='冲击结束，固定环境镜交代暗罩安稳'),dict(offset=1.5,intent='浅水下行，余声渐远')]
action('CY028C','咏唱尾半句跨切Claude已经解放的右手腕特写。浅淡束缚压痕仍在，焦边蕾丝袖口保留；手指起初微颤，随“的微光啊”慢慢稳住。极少橙金光屑轻映指节，仍是初蓄，未形成完整火种。手与衣料没有挂水、没有蒸汽，压痕不消退，衣物不修复；没有新增治疗法术。')
by['CY028C'].update(title='锁痕与微光',framing='同一右手的侧上方近特写，腕部压痕与指节为重心',purpose='以刚获自由的手腕和逐渐稳定的手指，表现Claude重新掌握自己的力量。',entry_state='承028B右手指尖初蓄，首句咏唱尚未念完，腕扣早已解除。',exit_state='手指稍稳、初蓄未熄；父亲呼唤即将令她短暂停声。',claude_accessory_state='原有焦边保留，衣料与头纱未被水龙浇湿，不需要烘干。',cinematic_beats=[dict(offset=0,intent='近切腕部压痕，手指轻颤'),dict(offset=1,intent='稳住右手，少量微光映亮指节')])
by['CY028B']['claude_accessory_state']='手和袖口没有挂水，蕾丝固定焦边保留，指尖仅少量初蓄光屑。'
# Clean live continuity descriptions; frozen requests and historical fields stay intact.
repls=[
 ('CY028C以裙边水汽承接整体烘干，下一镜可见恢复轻盈的头纱。','CY028C改为锁痕与微光特写，头纱没有浸湿与烘干过程。'),
 ('湿袖焦黑的边缘仍在滴水。','袖口干燥，原有焦黑边缘保留。'),
 ('战后雨渐停，Claude蒸干后不再淋湿。','战后雨渐停；Claude此前始终在罩内，衣物没有被水龙浇湿，撤罩后不再受雨淋。'),
 ('撤罩后仅殿内水雾轻沾衣发；CY028C随衣料蒸干；随后恢复轻盈','撤罩后衣发仍无挂水，不安排湿衣与烘干；头纱自然轻盈'),
 ('蒸干只去水，不修复焦损','衣物未被浇湿；微光不治疗伤痕，也不修复焦损'),
 ('C热息蒸干','C锁痕与微光、手指从轻颤到稍稳'),
 ('站立觉醒→蒸散水汽','站立觉醒→锁痕与微光'),
 ('裙边水汽代表衣料与头纱整体蒸干，后镜接轻盈干纱','手腕压痕与初蓄微光，衣物和头纱无挂水'),
]
def words(s):
 for a,b in repls:s=s.replace(a,b)
 return s
skip={'visual_prompt','refs','generation_request','source_manifest','origin_manifest','page_layouts'}
def rewrite(x):
 if isinstance(x,str):return words(x)
 if isinstance(x,list):return [rewrite(v) for v in x]
 if isinstance(x,dict):return {k:(v if k in skip or k.startswith('previous_') else rewrite(v)) for k,v in x.items()}
 return x
p=rewrite(p);script=words(script);by={s['id']:s for s in p['shots']}
rows=load(rec+'/实际请求.json')
for row in rows:
 sid=row['id'];s=by[sid];path=f'镜头设计/图像/余波与锁痕-v053/{sid}-v053-r1.png';dest=R/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(row['source'],dest)
 with Image.open(dest) as im:w,h=im.size;im.verify()
 req=rec+'/'+sid+'.json';save(req,dict(row,output=path,sha256=sha(dest),dimensions=[w,h],engine='built-in image_gen',review='静帧已查看，无挂水、蒸汽或成熟火种；待作者审阅，动态未制作'))
 s['previous_presentation_v052']=old[sid]['presentation'];s['previous_generation_request_v052']=old[sid]['generation_request']
 s['presentation'].update(path=path,status='v0.53修订候选，待作者审阅',missing='手指从轻颤到稳定及连续咏唱待动态验证。')
 s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0,y=0,w=1,h=1),panel_index=0,generation_request=req,visual_prompt=row['input']['prompt'],editorial_review=dict(version='v053',status='pending_author_review'),final_static_review=dict(version='v053',status='pending_author_review'))
 s['refs'].append(dict(path=path,role='v0.53修订候选；原图保留'))
elapsed=0
for i,s in enumerate(p['shots']):
 s.update(start_second=elapsed,end_second=elapsed+s['seconds']);elapsed+=s['seconds']
 if i+1<len(p['shots']):s['next_link']='接 '+p['shots'][i+1]['id']+'：'+p['shots'][i+1]['entry_state']
for sc in p['scenes']:
 group=[s for s in p['shots'] if s['scene']==sc['id']];sc.update(shot_ids=[s['id'] for s in group],seconds=sum(s['seconds'] for s in group),pages=list(dict.fromkeys(s['presentation']['path'] for s in group)))
p['page_layouts']=[dict(path=path,rows=1,cols=1) for path in dict.fromkeys(s['presentation']['path'] for s in p['shots'])]
out='镜头设计/shot-plan-v0.53.json';music='后期/余波与锁痕-v053/作者确认选曲-v053.json';audio_path='后期/余波与锁痕-v053/预演编排.json'
p.update(version='v0.53',picture_revision='v053',report_revision='v053',title='《穿云》带图分镜 v0.53 · 大招余波与锁痕微光',subtitle='132镜 · 434秒 · 余波重排与两张局部修订',source_manifest='镜头设计/shot-plan-v0.52.json',story_script='剧本/穿云-场景剧本-v0.53.md',audio_arrangement=audio_path,music_adoption=music)
p['review_intro']='撞盾与洪流冲人连续结束，接浅水空殿和罩内安抚；星火起咏改为锁痕与微光，取消湿衣蒸干。'
p['review_focus']='检查冲击结束到环境余波的节奏，及初蓄光屑、腕部压痕与后续成熟火种的区别。'
p['revision_notes']=dict(previous_manifest=p['source_manifest'],modified_image_ids=['CY028B','CY028C'],moved_ids=['CY024B1'],added_ids=[],boundary='132镜时长、对白字幕与七首选曲不变；B1移至B3前，C改手腕特写，B去挂水。')
script=script.replace('版本：v0.52','版本：v0.53',1);(R/p['story_script']).write_text(script,encoding='utf-8');save(out,p)
adopt=load(base['music_adoption']);adopt.update(version='v053',previous=base['music_adoption'],source_plan=out,source_plan_sha256=sha(R/out))
adopt_rows={s['shot']:s for s in adopt['shots']};adopt['shots']=[dict(adopt_rows[s['id']],title=s['title'],start=s['start_second'],end=s['end_second']) for s in p['shots']];save(music,adopt)
audio=rewrite(load(base['audio_arrangement']));audio.update(version='v053-aftermath-seven-tracks',shot_plan=out,shot_plan_sha256=sha(R/out),previous=base['audio_arrangement'],adopted_music=music)
for section in audio['sections']:
 if section['id']=='M09':
  section['last_shot']='CY024B3A'
  section['note']+=' B1冲人结束后接B3环境余波与B3A安抚，重音收为余韵；采用曲目不变。'
for sid in ['CY024B1','CY024B3','CY024B3A','CY028B','CY028C']:audio['effects'][sid]=by[sid]['sound']
save(audio_path,audio)
assert len(p['shots'])==132 and elapsed==434
for s in p['shots']:
 assert s['source_quote'] in script,s['id']
 for k in ['seconds','dialogue','dialogue_cues','subtitle_cues']:assert s.get(k)==old[s['id']].get(k),(s['id'],k)
assert adopt['marks']==load(base['music_adoption'])['marks']
snapshot=R/'镜头设计/带图分镜-细节与显形-v052.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
save(rec+'/变更核验.json',dict(shots=132,seconds=elapsed,sequence=['CY024B','CY024B1','CY024B3','CY024B3A','CY027'],images=['CY028B','CY028C'],dialogue_and_music='unchanged',source_passages='132 matched',dynamic='pending'))
print(out)
