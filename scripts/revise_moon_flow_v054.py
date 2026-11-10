"""Version Kimi's four-second rear-view materialization and derived generation board."""
import copy, hashlib, json, shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
OUT='视频制作/生成板-v004'
REC='镜头设计/生成记录/月光流动-v054'
IMG='镜头设计/图像/月光流动-v054'
def load(p):return json.loads((R/p).read_text('utf-8-sig'))
def save(p,x):
 f=R/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
base=load('镜头设计/shot-plan-v0.53r3.json');p=copy.deepcopy(base)
old={s['id']:s for s in base['shots']};by={s['id']:s for s in p['shots']}
s=by['CY024K00'];close=by['CY024K0']
states=[dict(path=IMG+'/背影-月光流入.png',offset=0,label='起始：只有月光流入，无人形',label_en='start, flowing moonlight without a human silhouette'),dict(path=IMG+'/背影-月光凝形.png',offset=1.6,label='中间：光流构成背影，下摆与双腿尚未凝实',label_en='intermediate, light becomes the rear silhouette while hem and legs remain light'),dict(path=IMG+'/背影-显形完成.png',offset=3.5,label='终态：完整背影，双刃低持',label_en='end, fully solid rear view with both blades held low')]
for state in states:
 assert (R/state['path']).is_file(),state['path']
 state['status']='v0.54背影显形候选，待作者审阅'
 state['limits']='同一连续镜头的状态参考；预演按状态切换静帧，不代表已生成动画。'
 state['sha256']=sha(state['path'])
s.update(seconds=4,title='月光流动，背影渐显',framing='窗外正后方远景全身；Kimi背对镜头、正面朝向完整中央彩窗，人物约占画高一半',purpose='以巨大彩窗和小背影建立闯入前的压力，并清楚展示月光自身流动后凝成人形。',entry_state='画外呼唤已结束；窗外尚无人形，银白月光从镜头左后侧流向高窗前。',exit_state='Kimi在完整中央彩窗前凝为实体，背对镜头悬空；双刃低持，尚未抬刃或投出。',state_references=states)
action='切到教堂正后中央高窗外，摄影机退到Kimi将显形位置的正后方。完整蓝色尖拱彩窗正对镜头，高墙与扶壁压住画面两侧；人物最终仅占画高约一半，头饰至靴尖完整可见。0–0.8秒，窗前没有人形，银白月光从镜头左后侧沿弧线流入；0.8–1.6秒，光流在窗前放缓、折回汇聚，逐渐勾出背对镜头的人形轮廓；1.6–3.5秒，头发与肩背先凝实，裙摆、双腿和双刃由相连的光丝逐步形成，背景仍可从尚未凝实的间隙看见，不能以整个人透明度淡入代替；3.5–4秒，Kimi完整悬停，脸正朝玻璃，不回头，左手明刃与右手暗刃低持，长发裙摆轻向画面左侧飘动。月光来自镜头后方偏左，实月不入画；没有黑烟、月环或传送门。摄影机沿正后轴线缓慢前移少许，到身形凝实即收停，全程保持远景比例与完整窗框；玻璃和拱顶完好，不提前举刃或破窗。'
script=(R/base['story_script']).read_text('utf-8')
assert s['source_quote'] in script
script=script.replace(s['source_quote'],action,1)
s.update(action=action,source_quote=action,sound='前一镜呼唤尾韵在入镜后淡去，夜风持续；光流汇聚可配极轻的银色气流声，凝实不加爆炸、撞击或新台词。既有Kimi选曲由后期延续。',cinematic_beats=[dict(offset=0,intent='无人形，月光从镜头左后侧流入'),dict(offset=.8,intent='月光在窗前放缓汇聚为背影轮廓'),dict(offset=1.6,intent='肩背凝实，下摆双腿仍与光流相连'),dict(offset=3.5,intent='实体背影完整，双刃低持，摄影机收停')])
s['previous_presentation_v053r3']=old[s['id']]['presentation']
s['previous_generation_request_v053r3']=old[s['id']].get('generation_request')
s['presentation']=dict(path=states[1]['path'],role='action',visible='正后方远景，Kimi肩背已显，下摆与双腿仍为相连的月光；完整中央彩窗在她正前方。',status=states[1]['status'],missing='起中终图仅说明4秒内的连续物质变化，流动与凝形的动态效果待视频验证。',show_as_main=True)
with Image.open(R/states[1]['path']) as im:w,h=im.size
s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0,y=0,w=1,h=1),panel_index=0,generation_request=REC+'/实际请求.json',visual_prompt='见当前实际请求记录中的背影-月光凝形；原侧面候选保留。',editorial_review=dict(version='v054',status='pending_author_review'),final_static_review=dict(version='v054',status='pending_author_review'))
s['refs'].extend(dict(path=v['path'],role=v['label']+'；当前背影候选') for v in states)
# The next shot keeps its image, words and duration; make the new angle change explicit.
before=close['source_quote'];old_action=close['action']
new_action=old_action.replace('仍从窗外同侧切到Kimi半身近景','由正后远景切到既有窗外斜侧半身近景：摄影机切位，Kimi身体与目光始终朝向同一面玻璃，不为展示脸而转身')
assert new_action!=old_action
close['action']=new_action;close['presentation']['visible']=new_action
close['source_quote']=before.replace(old_action,new_action)
assert before in script;script=script.replace(before,close['source_quote'],1)
close['entry_state']='承正后远景显形完成，摄影机切到窗外斜侧近景；Kimi不转身，仍面对同一完整彩窗，双刃低持。'
close['framing']='窗外斜侧半身近景；由上一镜正后远景切位，Kimi朝向玻璃不变'
close['cinematic_beats'][0]['intent']='由正后背影切窗外斜侧近景，摄影机换位而Kimi不转身；脸与左明刃清楚'
# Absolute end-of-film silence and the older duration note follow the changed timeline.
by['CY034']['sound']=by['CY034']['sound'].replace('430–434','431.5–435.5').replace('430-434','431.5-435.5')
if isinstance(p.get('continuity'),dict) and 'kimi_chant' in p['continuity']:
 p['continuity']['kimi_chant']=p['continuity']['kimi_chant'].replace('显形留白2.5秒','正后方背影显形4秒')
elapsed=0
for i,x in enumerate(p['shots']):
 x.update(start_second=elapsed,end_second=elapsed+x['seconds']);elapsed+=x['seconds']
 if i+1<len(p['shots']):x['next_link']='接 '+p['shots'][i+1]['id']+'：'+p['shots'][i+1]['entry_state']
for sc in p['scenes']:
 group=[x for x in p['shots'] if x['scene']==sc['id']]
 sc.update(seconds=sum(x['seconds'] for x in group),pages=list(dict.fromkeys(x['presentation']['path'] for x in group)))
 for key in ['start','start_second']:
  if key in sc:sc[key]=group[0]['start_second']
 for key in ['end','end_second']:
  if key in sc:sc[key]=group[-1]['end_second']
p['page_layouts']=[dict(path=path,rows=1,cols=1) for path in dict.fromkeys(x['presentation']['path'] for x in p['shots'])]
source='镜头设计/shot-plan-v0.54.json';music='后期/月光流动-v054/作者确认选曲.json';audio_path='后期/月光流动-v054/预演编排.json'
p.update(version='v0.54',picture_revision='v054',report_revision='v054',title='《白米饭》带图分镜 v0.54 · 月光流动与背影显形',subtitle='132镜 · 435.5秒 · 4秒月光显形',total_seconds=elapsed,source_manifest='镜头设计/shot-plan-v0.53r3.json',story_script='剧本/白米饭-场景剧本-v0.54.md',audio_arrangement=audio_path,music_adoption=music,review_intro='月光显形扩至4秒，正后方远景背影面对高窗，光流连续构成人物；起中终静帧用于状态预演。',review_focus='检查月光成为人物、背影比例、双刃左右手与下一镜斜侧切位。')
p['revision_notes']=dict(previous_manifest=p['source_manifest'],modified_image_ids=['CY024K00'],modified_description_ids=['CY024K00','CY024K0'],duration_change=dict(shot='CY024K00',before=2.5,after=4),boundary='其他131镜时长、全部对白及七首选曲不变；后续绝对时码顺延1.5秒。')
script=script.replace('版本：v0.53r2','版本：v0.54',1).replace('显形留白2.5秒','正后方背影显形4秒')
(R/p['story_script']).write_text(script,'utf-8');save(source,p)
adopt=load(base['music_adoption']);adopt.update(version='v054',previous=base['music_adoption'],source_plan=source,source_plan_sha256=sha(source))
adopt_rows={x['shot']:x for x in adopt['shots']};adopt['shots']=[dict(adopt_rows[x['id']],title=x['title'],start=x['start_second'],end=x['end_second']) for x in p['shots']];save(music,adopt)
audio=load(base['audio_arrangement']);audio.update(version='v054-moon-flow',shot_plan=source,shot_plan_sha256=sha(source),previous=base['audio_arrangement'],adopted_music=music)
audio['effects'][s['id']]=s['sound'];audio['effects']['CY034']=by['CY034']['sound'];save(audio_path,audio)
plan=load('视频制作/生成板-v003/批次计划.json');plan.update(version='v004',output=OUT,source=source)
cast=load(plan['cast_review']);cast['source_sha256']=sha(source)
if 'source' in cast:cast['source']=source
cast['shots'][s['id']]['note']='开始没有人形；月光逐渐构成Kimi背影，完整实体仅在最后0.5秒出现；不露面、不转头。'
save(OUT+'/人物核对.json',cast);plan['cast_review']=OUT+'/人物核对.json'
sound=load(plan['sound_review']);sound[s['id']]={'effects':'短暂呼唤尾韵消退，夜风持续，光流汇聚的极轻气流声；无爆炸、撞击或台词。'}
sound['CY034']['effects']=sound['CY034']['effects'].replace('430–434','431.5–435.5').replace('430-434','431.5-435.5')
save(OUT+'/声音核对.json',sound);plan['sound_review']=OUT+'/声音核对.json'
directions={}
for path in plan['direction_reviews']:directions.update(load(path)['batches'])
b=next(x for x in plan['batches'] if x['id']=='GB014');at=plan['batches'].index(b)
original=copy.deepcopy(directions['GB014'])
b.update(title='正门吸引注意',shot_ids=['CY024','CY024R'],handle_reason='在注意力转向正门的反应后分批，保留下一批完整4秒显形和6秒咏唱。')
plan['batches'].insert(at+1,dict(id='GB014A',title='月光流入，背影显形与举刃',shot_ids=['CY024K00','CY024K0'],group_reason='4秒月光凝形接6秒完整请求与投刃，角色状态与声线连续。',handle_reason='10秒有效内容；后续破窗至护罩为14秒完整动作链，无法整体并入剩余5秒；不拆断后续动作链。',status='draft_not_submitted'))
directions['GB014']=dict(original,arc_zh='正门九人现身与指令→教主转头→画外呼唤牵出后窗。',arc_en='The entrance command draws the priest toward the main door, while an offscreen invocation introduces the rear-window action.',exit_bridge_zh='教主视线留在正门，画外呼唤已结束；下一批切窗外无人形的月光。',shots={i:original['shots'][i] for i in b['shot_ids']})
d=dict(original,arc_zh='月光流入空窗前→汇成小小背影→实体凝稳→斜侧切近→左手举明刃、完整请求后投出。',arc_en='Flowing moonlight gathers into a small rear-view figure before the towering window; once solid, a side close-up shows her request and single blade throw.',entry_bridge_zh='承上一批画外呼唤尾韵，正门仍牵住敌方注意；窗前起始没有人形。',shots={i:original['shots'][i] for i in ['CY024K00','CY024K0']})
d['shots']['CY024K00']=dict(camera_zh='镜头退到人物正后方远景，脸朝玻璃、只见背影；沿轴线缓推少许，身形凝实即收停，人物始终约占画高一半，完整高窗形成压迫感。',camera_en='Use a distant direct rear full-body view, with Kimi about half of frame height before the towering intact window. Dolly forward slightly on her rear axis and ease to a stop as she becomes solid; never orbit or reveal her face.',transition_zh='承画外呼唤尾韵切到窗前空处，月光流入并连续成形，4秒内不切镜。',transition_en='Cut from the completed invocation to empty air outside the rear window; keep all four seconds uncut.',action_en='At 0-0.8 seconds, silver-white moonlight enters from behind and left of the camera, with no human silhouette. At 0.8-1.6 it slows and gathers in front of the glass. At 1.6-3.5, hair and shoulders become solid first; the hem, legs and small blades form from connected light filaments, with background visible through unfinished gaps. At 3.5-4, one solid Kimi floats facing the glass, back to camera, both hands low: her left bright blade is screen left and her right dark blade screen right. She does not turn, raise a blade or land. The physical moon stays behind the camera, outside frame. No black smoke, portal or overall opacity fade.',effects_en='The previous invocation decays into continuous night wind and a faint airy gathering sound; no impact or new speech.')
d['shots']['CY024K0']['transition_zh']='完整背影凝稳后，摄影机切到既有窗外斜侧近景；Kimi不转身、仍朝同一玻璃。长发风向、双刃持手连续，请求结束才投刃。'
d['shots']['CY024K0']['transition_en']='After materialization completes, cut the CAMERA from behind to the established exterior side close-up; Kimi never turns away from the same glass. Preserve wind and blade hands; throw after the complete request.'
d['shots']['CY024K0']['camera_zh']='切至窗外斜侧半身近景后，小幅随左手明刃抬起调整，随即停住让完整请求与投刃发生；右缘完整玻璃持续可见。'
d['shots']['CY024K0']['camera_en']='Once in the exterior side medium close-up, reframe slightly with the raised left-hand blade, then hold for the full request and throw; keep intact glass at the right edge.'
directions['GB014A']=d
save(OUT+'/动态审查.json',dict(batches=directions));plan['direction_reviews']=[OUT+'/动态审查.json']
plan.get('action_overrides',{}).pop(s['id'],None)
plan.get('execution_notes',{}).pop(s['id'],None)
plan.setdefault('shot_notes',{})[s['id']]='正后方同机位起中终状态参考；预演为静帧切换，动态须连续凝形，不把三图切成三个镜头。'
plan['global_gaps']=[t.replace('434','435.5') for t in plan.get('global_gaps',[])]
plan['mix_notes']=[t.replace('430–434','431.5–435.5').replace('430-434','431.5-435.5').replace('204–410','205.5–411.5').replace('204-410','205.5-411.5') for t in plan.get('mix_notes',[])]
save(OUT+'/批次计划.json',plan)
assert len(p['shots'])==132 and elapsed==435.5
for x in p['shots']:
 assert x['source_quote'] in script,x['id']
 for key in ['dialogue','dialogue_cues','subtitle_cues']:assert x.get(key)==old[x['id']].get(key),(x['id'],key)
 if x['id']!='CY024K00':assert x['seconds']==old[x['id']]['seconds']
assert adopt['marks']==load(base['music_adoption'])['marks']
snapshot=R/'镜头设计/带图分镜-v053r3.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
save(REC+'/变更核验.json',dict(shots=132,film_seconds=435.5,old_film_seconds=434,changed_duration='CY024K00: 2.5 -> 4',other_131_durations_unchanged=True,dialogue_and_music_unchanged=True,source_passages_verified=132,new_board_batches=34,requested_seconds=510,handle_seconds=74.5,final_no_bgm=[431.5,435.5],status='静帧与文字设计；动态未生成'))
print(source)
