"""Version the palace reclining-throne sequence; preserve timing, speech and music."""
import copy, hashlib, json, shutil
from pathlib import Path
from PIL import Image

R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/宫殿躺姿-v055'
IMG='镜头设计/图像/宫殿躺姿-v055'
OUT='视频制作/生成板-v005'
SOURCE='镜头设计/shot-plan-v0.55.json'

if (R/SOURCE).exists():
 raise SystemExit('v0.55 already exists. This one-time migration will not overwrite the reviewed version. Use the build scripts to render it.')
def load(p):return json.loads((R/p).read_text('utf-8-sig'))
def save(p,d):
 f=R/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()

base=load('镜头设计/shot-plan-v0.54.json');p=copy.deepcopy(base)
old={s['id']:s for s in base['shots']};by={s['id']:s for s in p['shots']}
ids=['CY005','CY006','CY007','CY008','CY009','CY010','CY009A']
poses='宫殿正面头在画面左、脚在右；GPT自身右手托右腮，右肘由靠垫承托，自身左手搭在座垫前缘。小鱼在靠近她头肩一端的卧榻前、台阶下轻抬眼；GPT略垂眼。侧躺期间不镜像、不切回端坐。'
space='对称金色哥特卧榻固定殿尾短墙前，长边横跨大厅，与长殿纵轴垂直、与台阶横边平行；正面朝对端出口。反向目送镜从卧榻后方高位看出口，前景应是靠背外背面，不能同时展示正面大块座垫。'
light='白金淡紫配色与蓝色服装本色保持；窗光柔和，地面保留低对比长反射，金饰不自发光，避免碎白眩光。'
updates={
'CY004D':dict(action='GPT仍侧躺在殿内卧榻上，画外平静发声放行，骑士收枪竖直、让开通道；小鱼空手跨过门槛。'),
'CY005':dict(title='空殿中的慵懒龙',framing='大全景／入口沿中轴望向横向对称卧榻',entry_state='宫门守卫已依照GPT画外命令让路，小鱼空手跨过门槛；GPT在殿尾卧榻上侧躺。',action='跨门后的大段跑程在切点省略，小鱼入镜时已接近高台，只完成最后几步，在卧榻头肩一端的台阶下停住并抬头。GPT头在画面左、脚在右，自身右手托腮、左手搭座垫前缘，懒懒侧躺；双翼舒展有支撑，单尾沿腿边自然延伸。',exit_state='小鱼空手停在卧榻头肩一端的前下方，轻抬眼求助；GPT保持侧躺。'),
'CY006':dict(framing='小鱼单人近景／卧榻头端反打，轻俯而非陡俯',entry_state='小鱼停在卧榻头肩一端的台阶下，气息未平，视线轻抬向画外右上方。',action='小鱼请求救Claude，双手收在胸前；问完仍看向画外侧躺的GPT，等一个答案。画内只有小鱼和右下方虚化的水平软垫边，不出现旧坐姿的竖直肩膀。',exit_state='小鱼保持轻抬的目光等待，GPT仍在画外侧躺。'),
'CY007':dict(framing='GPT侧躺中近景／正面同侧轴线',entry_state='GPT侧躺听完求助，自身右手仍托腮、左手搭在座垫前缘。',action='GPT慵懒的身体不动，目光略向下落到小鱼身上，眼神短暂迟疑后收住，以平静语气说出拒绝。右手继续托腮，左手自然搭垫边，不先抓握、不起身，也不嘲笑。',exit_state='拒绝说完，她仍侧躺，没有进一步解释。'),
'CY008':dict(framing='小鱼单人面部近景／延续同一卧榻头端反打',entry_state='小鱼难以相信，仍轻抬眼望着画外侧躺的GPT。',action='小鱼轻声追问，蓝眼仍看向画外右上方；等待没有回应后才垂下视线。画内不出现GPT的竖直肩影，软垫前缘与上一反打保持同侧。',exit_state='小鱼目光落下；GPT在画外保持侧躺和沉默。'),
'CY009':dict(framing='中远景／面向卧榻，小鱼离开向镜头走近',entry_state='小鱼低头，GPT仍在对称卧榻上侧躺。',action='小鱼说出决定后转身，向入口方向走去，低头擦去泪水；镜头沿她离开的方向短距离后退，保持前景孩子与远处卧榻同框。GPT仍头左脚右地侧躺，右手托腮、左手搭垫边，只有目光跟随；她还不起身。',exit_state='小鱼仍在长殿内走向远处出口，钟声传来；GPT仍侧躺。'),
'CY010':dict(title='软垫边的迟疑',framing='GPT自身左手与座垫前缘接触特写',purpose='以自由手的无意识收紧暴露迟疑，起身留到下一镜。',entry_state='小鱼仍在远端长殿内，GPT侧躺不动，远处钟声传来；右手继续托腮。',action='钟声传来，ChatGPT仍侧躺。自身左手的指尖压紧座垫前缘的淡紫织物，压出浅褶，停一拍后慢慢松开；右手继续托腮，不换手去抓金属扶手。',exit_state='左手指尖已松开、掌根仍搭在软垫前缘；下一镜才解除托腮并撑起身体。',sound='一声远钟及连续尾韵，极轻的织物摩擦；小鱼远去的脚步在画外延续，不切黑。'),
'CY009A':dict(title='起身目送长殿尽头',framing='卧榻后方偏侧高位超级大远景／越过横向靠背背面望向出口',purpose='从慵懒侧躺到主动起身的第一步，保留后段亲自救援的反差。',entry_state='左手刚松开软垫前缘，GPT仍侧躺；小鱼在远处出口附近。',action='承左手松开，0–2秒GPT将右手从脸侧放下、双翼自然收拢，左掌撑住座垫，把上身抬起；2–4秒收腿转到座前、双脚落在高台后站起，单尾顺座面边缘滑落到身后，避开扶手与椅框；4–6秒站在卧榻与长殿之间，目送小鱼越过对端宫门。高位后方镜头越过横向靠背外背面，王座正面朝远处出口，只有一个连续起身，不从站立终态重复起身。',exit_state='小鱼越过宫门，GPT站在卧榻前目送；切夜晚教堂侧墙。')}
for sid,values in updates.items():by[sid].update(values)
script=(R/base['story_script']).read_text('utf-8')
def replace_quote(sid,text):
 before=old[sid]['source_quote'];assert before in script
 return before,text
q005='高大的立柱尽头，横向对称的金色卧榻背靠殿尾短墙，正面朝着对端入口。ChatGPT独自侧躺其上，头在正面画面左侧、脚向右伸；自身右手托腮，右肘倚着靠垫，自身左手松松搭在淡紫座垫前缘。她的双翼有支撑地舒展，长尾沿腿边自然延伸。窗光和地面反射柔和，殿内只留下小鱼的脚步与喘息。'
q009a='ChatGPT将托腮的右手放下、双翼自然收拢，左掌撑住座垫抬起上身；她收腿转到座前，双脚落地后站起，长尾顺座面边缘滑到身后。镜头从卧榻后方偏侧高位越过横向靠背的外背面，沿长殿望向对端出口：卧榻长边与殿轴垂直、与台阶横边平行，正面朝远处宫门；ChatGPT站在卧榻与长殿之间，目送小鱼小小的蓝色背影越过门口。门外圣骑士不再阻拦。'
for sid,new in [('CY005',q005),('CY010',by['CY010']['action']),('CY009A',q009a)]:
 before,_=replace_quote(sid,new);script=script.replace(before,new,1);by[sid]['source_quote']=new
script=script.replace('殿内传来 ChatGPT 的声音。','殿内传来仍侧躺在卧榻上的ChatGPT的声音。',1)
script=script.replace('ChatGPT 抬起眼睛。','ChatGPT保持托腮侧躺，目光略向下落到台阶前的小鱼身上。',1)
script=script.replace('她保持平静，没有立刻回答。','她的眼神短暂迟疑，又收住；身体仍懒懒倚着靠垫，没有立刻回答，也没有嘲笑。',1)
script=script.replace('版本：v0.54｜2026-10-25｜水龙俯冲破顶、居中结印盘身、一次前指出击；纯水咏唱保留救赎。','版本：v0.55｜2026-10-26｜宫殿对称卧榻、慵懒侧躺与起身目送；既定对白和后段救援保持。',1)
for sid in ids:
 s=by[sid];path=IMG+('/CY009A-r2.png' if sid=='CY009A' else '/'+sid+'.png')
 s['previous_presentation_v054']=copy.deepcopy(old[sid]['presentation'])
 s['previous_generation_request_v054']=old[sid].get('generation_request')
 s['previous_static_review_v054']=s.pop('final_static_review',None)
 s['presentation']=dict(path=path,role='ending' if sid=='CY009A' else 'action',visible=s['action'],status='v0.55躺姿衍生静帧待作者审阅；对称卧榻设计已获认可',missing='只证明静帧代表状态；起身、收翼、尾巴落下及口型需动态验证。',show_as_main=True)
 with Image.open(R/path) as im:w,h=im.size
 s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0,y=0,w=1,h=1),panel_index=0,generation_request=REC+'/实际请求.json',visual_prompt='见本轮实际请求中对应镜号；历史坐姿与摆向错误候选不作为当前生成输入。',editorial_review=dict(version='v055',status='pending_author_review',dynamic_execution='pending'),final_static_review=dict(version='v055',status='pending_author_review'))
 s['refs']=[dict(path=path,role='本轮当前躺姿构图参考'),*s.get('refs',[])]
 s['invariants']=[t for t in s.get('invariants',[]) if not any(x in t for x in ['不展示起身','GPT已站起','王座只在'])]
 s['invariants'] += [space,light]
 if sid!='CY009A':s['invariants'].append(poses)
by['CY004D']['presentation']['visible']=by['CY004D']['action']
by['CY010']['invariants'].append('本镜只有自身左手压紧、松开软垫，不展示起身；右手托腮在画外保持。')
by['CY009A']['invariants'].append('本镜入态侧躺、出态站立；展示图仅为站立终态。双翼先收拢，尾巴从座面滑落一次，不穿椅、不留第二条尾巴。')
by['CY009A']['cinematic_beats']=[dict(offset=0,intent='右手离腮、收翼，左掌撑垫'),dict(offset=2,intent='收腿落脚后站起，单尾滑落'),dict(offset=4,intent='站定，目送小鱼越过宫门')]
for i,s in enumerate(p['shots'][:-1]):
 if s['id'] in updates or p['shots'][i+1]['id'] in updates:s['next_link']='接 '+p['shots'][i+1]['id']+'：'+p['shots'][i+1]['entry_state']
p['continuity']['palace']='宫门守卫放行时GPT在殿内画外侧躺；求助期间右手托腮、左手搭垫边，孩子离开后左指压垫再松开，接解除托腮、撑垫收腿落脚与起身目送。'+space+poses+light
p['continuity']['insert_motif']=p['continuity']['insert_motif'].replace('握扶手','左指压软垫')
for sc in p['scenes']:sc['pages']=list(dict.fromkeys(s['presentation']['path'] for s in p['shots'] if s['scene']==sc['id']))
p['page_layouts']=[dict(path=x,rows=1,cols=1) for x in dict.fromkeys(s['presentation']['path'] for s in p['shots'])]
p.update(version='v0.55',picture_revision='v055',report_revision='v055',title='《白米饭》带图分镜 v0.55 · 宫殿卧榻与慵懒龙',subtitle='132镜 · 435.5秒 · 宫殿躺姿、软垫迟疑与起身目送',source_manifest='镜头设计/shot-plan-v0.54.json',story_script='剧本/白米饭-场景剧本-v0.55.md',audio_arrangement='后期/宫殿躺姿-v055/预演编排.json',music_adoption='后期/宫殿躺姿-v055/作者确认选曲.json',review_intro='宫殿七镜统一对称卧榻，慵懒侧躺承接软垫迟疑与起身目送。',review_focus='手位、头脚方向、卧榻横向朝宫门与侧躺到站立的连续性。',revision_notes=dict(previous_manifest='镜头设计/shot-plan-v0.54.json',modified_image_ids=ids,modified_description_ids=list(updates),boundary='132镜顺序、435.5秒时长、全部对白字幕、临时读稿与七首选曲不变。'))
save(SOURCE,p);(R/p['story_script']).write_text(script,'utf-8')
music=load(base['music_adoption']);music.update(version='v055',previous=base['music_adoption'],source_plan=SOURCE,source_plan_sha256=sha(SOURCE))
for row in music['shots']:row['title']=by[row['shot']]['title']
save(p['music_adoption'],music)
audio=load(base['audio_arrangement']);audio.update(version='v055-palace',previous=base['audio_arrangement'],shot_plan=SOURCE,shot_plan_sha256=sha(SOURCE),adopted_music=p['music_adoption'])
audio['effects']['CY010']=by['CY010']['sound'];save(p['audio_arrangement'],audio)

plan=load('视频制作/生成板-v004/批次计划.json');plan.update(version='v005',source=SOURCE,output=OUT)
cast=load(plan['cast_review']);cast.update(version='v005',source=SOURCE,source_sha256=sha(SOURCE))
cast['shots']['CY009'].update(visible=['DeepSeek','ChatGPT'],offscreen=[],note='小鱼前景向镜头走近，GPT在远处卧榻仍侧躺，不能写成画外。')
for sid in ids:cast['shots'][sid]['basis']='v0.55实际新图逐张检查及连续性独立复核'
cast['shots']['CY005']['note']='GPT在远处横向卧榻侧躺，头左脚右；跑程跨切省略，构图参考不是强制首帧。'
cast['shots']['CY006']['note']=cast['shots']['CY008']['note']='画内只有小鱼与虚化软垫前缘；GPT在画外侧躺，没有竖直肩影。'
cast['shots']['CY007']['note']='自身右手托腮，左手搭垫边；小鱼画外，表情克制不嘲笑。'
cast['shots']['CY010']['note']='仅自身左手压软垫；右手仍托腮在画外。'
cast['shots']['CY009A']['note']='后方越过横向靠背看出口；图为站立终态，不是首帧；先完整起身再目送。'
save(OUT+'/人物核对.json',cast);plan['cast_review']=OUT+'/人物核对.json'
sound=load(plan['sound_review']);sound['CY010']['effects']=by['CY010']['sound'];sound['CY010'].pop('action_override',None)
save(OUT+'/声音核对.json',sound);plan['sound_review']=OUT+'/声音核对.json'
d=load(plan['direction_reviews'][0]);batches=d['batches']
for bid in ['GB003','GB004','GB005']:
 for sid,rv in batches[bid]['shots'].items():
  if sid in updates:rv['action_zh_override']=by[sid]['action']
batches['GB003']['exit_bridge_zh']='小鱼停在卧榻头肩一端台阶下，下一批接轻抬眼的求助；GPT保持侧躺。'
batches['GB003']['shots']['CY004D']['action_en']='GPT speaks from offscreen while still reclining inside the hall. The guards lift their spears vertically and step aside; the empty-handed child crosses the threshold while they remain outside.'
batches['GB003']['shots']['CY005'].update(action_en='After a travel ellipsis, DeepSeek completes only the last few steps to the head end of the raised daybed and looks up. GPT reclines head screen left, feet right, own right hand supporting cheek, own left hand loose on the front cushion. The wide symmetrical daybed stands crosswise at the short end wall, facing the entrance, never along a long side wall. Keep the child small in the enormous hall.',camera_zh='入口中轴大全景缓推少许，保留前景小鱼与殿尾横向卧榻；跑程已跨切省略，不追成近景。')
batches['GB004']['entry_bridge_zh']='小鱼已经停在卧榻头肩一端台阶下；眼线轻抬，GPT略垂眼，同侧反打不越轴。'
rv=batches['GB004']['shots']
rv['CY006'].update(camera_zh='卧榻头端轻俯单人近景缓推少许，问句结束前停住；只见小鱼与虚化软垫边，不保留旧坐姿肩影。',camera_en='Near the head end of the daybed, gently look down toward a single close-up of the child; ease a small push to a stop before her question ends. Only a blurred horizontal cushion edge may enter foreground, no upright adult shoulder.',action_en='DeepSeek looks gently upward to screen right at the offscreen reclining GPT, asks for help with her empty hands held near her chest, then waits without lowering her eyes. Keep her blue eyes and pleading expression; no other person appears.')
rv['CY007'].update(camera_zh='同侧GPT侧躺中近景，起始随目光缓靠近一点后收停；右手托腮和左手垫边同框，保留拒绝后的静默。',camera_en='A same-side medium close-up of reclining GPT eases slightly closer with her gaze, then holds; include her own right hand under her cheek and left hand on cushion edge.',action_en='Still reclining head screen left and feet right, GPT lowers her eyes toward the child below the dais. A moment of hesitation passes across her eyes before she calmly refuses. Own right hand remains under cheek and own left hand rests loosely on cushion edge. She neither sits up nor grips yet, and does not mock or smile.')
rv['CY008'].update(action_en='In the matching single close-up, DeepSeek softly asks her follow-up while looking up to screen right toward offscreen reclining GPT. Only after silence does she lower her gaze. Keep the blurred horizontal cushion edge consistent; no upright adult shoulder appears.')
batches['GB005'].update(arc_zh='小鱼转身独自离去，GPT仍侧躺；钟声里左手指尖压紧软垫后松开，她才撑起身体、落脚站定，目送蓝色背影。',arc_en='The child leaves while GPT still reclines; the bell triggers a small left-hand squeeze of the cushion, followed by a single rise to stand and watch her departure.',exit_bridge_zh='小鱼越过对端宫门，GPT站在横向卧榻与长殿之间；钟尾接教堂夜风。')
rv=batches['GB005']['shots']
rv['CY009'].update(camera_zh='面向卧榻的中远景，随小鱼离开短距离后退，保留孩子前景和GPT躺姿背景；不反向拍成入殿。',camera_en='Face the daybed in a medium-wide shot and track backward briefly as the child approaches the camera; retain reclining GPT in the distant background.',action_en='After saying her decision, DeepSeek turns and walks toward the entrance and camera, wiping a tear with one empty hand. GPT remains visibly reclining on the distant daybed, right hand under cheek and left hand on cushion; only her eyes follow. She has not risen. The child remains inside the hall when the bell arrives.')
rv['CY010'].update(camera_zh='锁定自身左手和淡紫座垫前缘的接触特写，指尖压出浅褶、停顿、松开；不摇向面部或金属扶手。',camera_en='Lock the detail on GPT\'s own left fingertips against the lavender front cushion; show soft upholstery compress, hold and release. Do not tilt toward face or a metal armrest.',action_en='GPT still reclines, her right hand supporting her cheek offscreen. Her own left fingertips press into the front cushion edge, hold briefly, and slowly loosen while the palm heel remains supported. She does not switch hands or sit up in this insert.')
rv['CY009A'].update(camera_zh='卧榻后方偏侧高位超级大远景，横向靠背外背面留前景；先稳住机位呈现起身，再缓缓抬高少许看见对端宫门，不能绕到卧榻正面。',camera_en='Use a high rear three-quarter extreme wide shot over the crosswise throne BACK EXTERIOR. Hold through the rise, then lift slightly toward the far exit; never orbit to its front.',transition_zh='承左手松开接一次连续起身；镜内0–2秒解除托腮并撑垫，2–4秒收腿落脚站起，4–6秒站定目送；图片只作站立终态参考。',transition_en='Match the released left hand into one continuous rise. The reference depicts the standing END state, never the opening frame.',action_en='At 0-2 seconds, GPT removes her right hand from cheek, folds both wings and pushes her torso up with her left palm on the cushion. At 2-4 she draws both legs to the front, plants her feet on the dais and stands; her single tail slides from the seat to behind her without crossing the frame. At 4-6 she stands between daybed and aisle watching the tiny blue child pass through the far door. The throne long edge crosses the hall, perpendicular to the aisle and parallel to the stair nosings, its front facing away from camera toward exit. No repeated rise or teleport to standing.')
save(OUT+'/动态审查.json',d);plan['direction_reviews']=[OUT+'/动态审查.json']
for b in plan['batches']:
 if b['id']=='GB003':b['title']='宫门放行与慵懒卧榻'
 if b['id']=='GB005':b['title']='独自离去、软垫迟疑与起身目送'
plan['shot_notes']['CY009A']='当前图为站立终态；先收翼、撑垫、收腿落脚，尾巴沿座面滑落一次。卧榻长边横跨大厅，镜头看到外背面。'
plan['shot_notes']['CY005']='大殿图用于空间与卧榻姿态，非强制首帧；大段跑程已跨切省略，三秒只完成最后几步。'
plan['navigation']['review']=REC+'/审查与交付.md'
save(OUT+'/批次计划.json',plan)

# Update the one existing environment asset, preserving its historical source.
assets=load('资产/assets.json');a=next(a for a in assets['assets'] if a['id']=='ENV-PALACE')
a['previous_v001']=copy.deepcopy(a)
a['related'] += [dict(path=a['path'],role='历史窄王座环境候选，保留不作为当前家具'),dict(path=a['source'],role='历史环境生成记录'),dict(path='镜头设计/图像/宫殿柔光-v055/CY007-对称卧榻懒懒龙-候选.png',role='作者认可的对称卧榻及躺姿设计母版；非人物身份四视图'),dict(path=IMG+'/CY009A-r2.png',role='反向空间：靠背外背面横跨前景，正面朝对端宫门')]
a.update(name='宫殿 · 对称卧榻与长殿',version='v055',path=IMG+'/CY005.png',status='对称卧榻与躺姿设计作者认可；衍生静帧待审',role=space+light,limits='仅用于S02宫殿；含人物的画面是空间/构图参考，不替代身份四视图。尾巴、收翼与起身仍需动态验证。',source=REC+'/实际请求.json')
save('资产/assets.json',assets)
snapshot=R/'镜头设计/带图分镜-v054.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
for fn in ['scripts/build_storyboard.py','scripts/build_generation_board.py','scripts/verify_generation_board.py']:
 f=R/fn;t=f.read_text('utf-8');t=t.replace('shot-plan-v0.54.json','shot-plan-v0.55.json') if 'storyboard' in fn else t.replace('生成板-v004','生成板-v005');f.write_text(t,'utf-8')
f=R/'00_打开项目.html';t=f.read_text('utf-8').replace('v0.54','v0.55').replace('生成板-v004','生成板-v005').replace('#GB014A','#GB003').replace('Kimi四秒背影显形 · 起中终多参考','宫殿对称卧榻与躺姿 · 多参考').replace('既定台词保持 · 月光流入、背影凝形与切位接近景','既定台词保持 · 慵懒侧躺、软垫迟疑与起身目送');f.write_text(t,'utf-8')
f=R/'AGENTS.md';t=f.read_text('utf-8').replace('当前全片入口为`视频制作/生成板-v004/生成板.html`','当前全片入口为`视频制作/生成板-v005/生成板.html`').replace('与v003全片旧版保留历史','、v003与v004全片旧版保留历史').replace('v0.54正片435.5秒','v0.55正片435.5秒');f.write_text(t,'utf-8')
for s in p['shots']:
 assert s['source_quote'] in script,s['id']
 for k in ['seconds','start_second','end_second','dialogue','dialogue_cues','subtitle_cues']:assert s.get(k)==old[s['id']].get(k),(s['id'],k)
assert music['marks']==load(base['music_adoption'])['marks']
assert len(p['shots'])==132 and p['total_seconds']==435.5
save(REC+'/变更核验.json',dict(shots=132,seconds=435.5,new_images=ids,all_timing_dialogue_cues_unchanged=True,music_marks_unchanged=True,source_quotes_verified=132,rejected_orientation=IMG+'/CY009A.png',current_reverse=IMG+'/CY009A-r2.png',scope='静帧、文案、数据核验；不表示连续动作或声音听审完成'))
print(SOURCE)
