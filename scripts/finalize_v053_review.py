"""Publish final description-only corrections while preserving images, dialogue and music."""
import copy,hashlib,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];OUT='后期/最终审查-v053'
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def save(p,v):
 f=R/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
base=read('镜头设计/shot-plan-v0.53.json');edits=[]
replacements=[
 ('05:12–05:18父亲打断','CY029/CY029E父亲打断'),
 ('战后撤罩，潮湿殿内的水雾轻沾衣边，再接后续蒸干','战后撤罩，衣物没有被水龙浇湿，不安排烘干；焦边与束缚压痕仍在'),
 ('解锁后确认小鱼安全，衣料仍湿且焦损。','解锁后确认小鱼安全，衣料没有挂水，固定焦损仍在。'),
 ('初蓄不熄灭，开句跨切裙边水汽。','初蓄不熄灭，开句跨切同一右手腕部的锁痕与微光。'),
 ('Claude已解缚并蒸干衣料，虚弱状态延续。','Claude已解缚，衣物没有被水龙浇湿，虚弱与焦损状态延续。'),
 ('人物头纱/衣料已经蒸干','人物头纱与衣料没有挂水，原有焦损保留'),
 ('B3两侧退水，B3A罩内安抚，B1教徒失足。','B1洪流冲散教徒，冲击结束后B3浅水环境余波，再接B3A罩内安抚。'),
 ('GPT已在主水幕侧前方高空悬停并开始咏唱；教主抬眼。','GPT已在完整中殿穹顶下悬停并开始咏唱，水龙尚未形成；教主抬眼。'),
 ('Kimi破柴后两侧与脚下散柴仍燃紫黑火','Kimi破柴后中央脚托周边已清空，燃烧的散柴均在暗罩外两侧'),
]
skip={'visual_prompt','refs','generation_request','page_layouts','source_manifest','origin_manifest'}
def words(s):
 for a,b in replacements:s=s.replace(a,b)
 return s
def walk(x,path=''):
 if isinstance(x,str):
  n=words(x)
  if n!=x:edits.append(dict(field=path,before=x,after=n))
  return n
 if isinstance(x,list):return [walk(v,path+f'[{i}]') for i,v in enumerate(x)]
 if isinstance(x,dict):return {k:(v if k in skip or k.startswith('previous_') else walk(v,path+'.'+k)) for k,v in x.items()}
 return x
p=walk(copy.deepcopy(base));by={s['id']:s for s in p['shots']}
for i,s in enumerate(p['shots'][:-1]):s['next_link']='接 '+p['shots'][i+1]['id']+'：'+p['shots'][i+1]['entry_state']
script=words((R/base['story_script']).read_text(encoding='utf-8')).replace('版本：v0.53','版本：v0.53r1',1)
p.update(version='v0.53r1',report_revision='v053r1',title='《穿云》带图分镜 v0.53r1 · 最终审查说明同步',source_manifest='镜头设计/shot-plan-v0.53.json',story_script='剧本/穿云-场景剧本-v0.53r1.md',audio_arrangement=OUT+'/预演编排-v053r1.json',music_adoption=OUT+'/作者确认选曲-v053r1.json')
p['revision_notes']=dict(previous_manifest=p['source_manifest'],modified_image_ids=[],added_ids=[],moved_ids=[],boundary='最终审查只清理现行说明冲突，图片、镜序、时长、对白字幕、既有语音和七首BGM均保持。')
p['review_intro']='最终审查已清理湿衣蒸干、旧余波顺序、提前出现水幕及燃柴位置说明；当前图片与全部采用用曲保持。'
p['review_focus']='当前静帧与选曲用于下一阶段制作，正式配音、乐句剪辑、混音及连续动作另行验证。'
(R/p['story_script']).write_text(script,encoding='utf-8');out='镜头设计/shot-plan-v0.53r1.json';save(out,p)
adopt=read(base['music_adoption']);adopt.update(version='v053r1',previous=base['music_adoption'],source_plan=out,source_plan_sha256=sha(R/out));save(p['music_adoption'],adopt)
audio=walk(read(base['audio_arrangement']),'audio');audio.update(version='v053r1-final-reviewed',shot_plan=out,shot_plan_sha256=sha(R/out),adopted_music=p['music_adoption'],previous=base['audio_arrangement']);save(p['audio_arrangement'],audio)
for a,b in zip(base['shots'],p['shots']):
 for k in ['id','seconds','start_second','end_second','dialogue','dialogue_cues','subtitle_cues','presentation']:assert a.get(k)==b.get(k),(a['id'],k)
 assert b['source_quote'] in script,b['id']
assert adopt['marks']==read(base['music_adoption'])['marks']
save(OUT+'/说明修复记录.json',dict(changes=edits,count=len(edits),images='unchanged',dialogue='unchanged',timing='unchanged',music='unchanged'))
snapshot=R/'镜头设计/带图分镜-余波与锁痕-v053.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
print(json.dumps(dict(version=p['version'],changes=len(edits)),ensure_ascii=False))
