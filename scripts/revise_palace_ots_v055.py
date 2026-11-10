"""Apply the author's close over-shoulder revision to the v055 palace draft once."""
import copy, hashlib, json
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/宫殿躺姿-v055'
SOURCE='镜头设计/shot-plan-v0.55.json'
OLD='镜头设计/图像/宫殿躺姿-v055/CY009A-r2.png'
NEW='镜头设计/图像/宫殿躺姿-v055/CY009A-r3-过肩.png'
def load(f):return json.loads((R/f).read_text('utf-8-sig'))
def save(f,v):(R/f).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf-8')
def sha(f):return hashlib.sha256((R/f).read_bytes()).hexdigest()
def replace(v,a,b):
 if isinstance(v,str):return v.replace(a,b)
 if isinstance(v,list):return [replace(x,a,b) for x in v]
 if isinstance(v,dict):return {k:(x if k.startswith('previous') else replace(x,a,b)) for k,x in v.items()}
 return v
p=load(SOURCE);s=next(x for x in p['shots'] if x['id']=='CY009A')
if s['presentation']['path']!=OLD:raise SystemExit('Expected the wide r2 draft; will not overwrite a later revision.')
assert (R/NEW).is_file()
oldhash=sha(SOURCE);previous=copy.deepcopy(s)
oldspace='反向目送镜从卧榻后方高位看出口，前景应是靠背外背面，不能同时展示正面大块座垫。'
newspace='目送镜为紧过肩，摄影机在卧榻前沿靠过道一侧、GPT肩后，朝对端宫门；王座处在摄影机后方画外，不再从椅背后拍大全景。'
p=replace(p,oldspace,newspace);p=replace(p,OLD,NEW)
s=next(x for x in p['shots'] if x['id']=='CY009A')
s['previous_shot_v055_wide']=previous
s['framing']='GPT肩后紧过肩／左边缘裁切半个后脑与一侧肩膀，远处小鱼清晰'
s['action']='承左手松开，镜内0–2秒GPT解除托腮并撑起上身，近景只见左边缘半个后脑与肩膀轻轻抬起；2–4秒接同一次起身，摄影机随头肩平稳升高少许并收停，收腿落脚、收翼和尾巴避开椅框在画外连续完成；4–6秒头肩站定，只留呼吸与少量发丝微动，目送远处小鱼背对镜头走向并越过宫门。全程不拉远露全身，不换到脸部，不重复起身。'
s['entry_state']='左手刚松开软垫前缘，GPT仍侧躺，开始解除托腮；切至近距离肩后，前景只截半个后脑和肩，小鱼已在远处出口附近。'
s['exit_state']='GPT已站定，裁切的后脑与肩保持前景；小鱼背对她越过远处宫门，接夜晚教堂侧墙。'
s['invariants'][-1]='前景始终只露半个后脑和一个肩膀，无完整脸、全身、腿、尾巴或王座；图为起身后的目送终态。起身承重与收翼、单尾避开椅框在画外发生一次，不为展示动作改变紧过肩构图。'
q='ChatGPT解除托腮，撑起上身，收腿落脚后站起。镜头贴近她肩后，左侧画框只截取半个后脑和一侧肩膀，随头肩轻轻升起后停住；收翼、腿脚承重与尾巴离开座垫在画外连续完成。前景的她略虚，焦点落在长殿尽头清晰的小鱼背影上。小鱼继续走向并越过宫门，ChatGPT站定目送；王座在摄影机后方画外，门外圣骑士不再阻拦。'
scriptfile=p['story_script'];script=(R/scriptfile).read_text('utf-8-sig')
assert previous['source_quote'] in script
script=script.replace(previous['source_quote'],q,1).replace('殿内只留下小鱼的脚步与喘息。殿内安静，只有小鱼急促的脚步与喘息。','殿内只留下小鱼的脚步与喘息。')
(R/scriptfile).write_text(script,'utf-8');s['source_quote']=q
s['presentation'].update(visible='左前景裁切ChatGPT半个后脑和一侧肩膀，远处小鱼背对她走向宫门；王座画外。',status='作者指定紧过肩新机位；新静帧待作者审阅',missing='终态构图参考，头肩连续起身与画外承重仍待视频验证。')
s['refs'][0]['role']='本轮紧过肩终态构图参考'
s['refs'].insert(1,{'path':OLD,'role':'历史广角反打；结构已修正，作者因张力不足改用紧过肩'})
s['cinematic_beats']=[{'offset':0,'intent':'近过肩，头肩随撑起上身轻抬'},{'offset':2,'intent':'摄影机随同一次起身平稳升高后收停，腿尾画外'},{'offset':4,'intent':'站定目送，远处小鱼背对镜头越过宫门'}]
w,h=Image.open(R/NEW).size;s['page_size']=[w,h];s['panel_rect_pixels']=[0,0,w,h]
save(SOURCE,p);newhash=sha(SOURCE)
for f in ['后期/宫殿躺姿-v055/预演编排.json','后期/宫殿躺姿-v055/作者确认选曲.json','视频制作/生成板-v005/人物核对.json','视频制作/生成板-v005/声音核对.json']:
 save(f,replace(load(f),oldhash,newhash))
f='视频制作/生成板-v005/人物核对.json'
save(f,replace(load(f),'后方越过横向靠背看出口；图为站立终态，不是首帧；先完整起身再目送。','紧过肩仅露半个后脑和一侧肩膀，远处小鱼背对镜头离去；王座、腿和尾巴在画外。图为站立目送终态，不是首帧；随同一次起身轻升收停。'))
f='视频制作/生成板-v005/动态审查.json';d=load(f);v=d['batches']['GB005']['shots']['CY009A']
v.update(camera_zh='摄影机贴近GPT肩后，左边缘只截半个后脑和一个肩膀，焦点保持远处小鱼；随同一次起身平稳升高少许后收停，不拉远、不绕到正脸，王座在机后画外。',camera_en='Use a tight over-the-shoulder framing: crop half the back of GPT head and one shoulder at the left edge, softly foregrounded, and keep the distant child in focus. Rise gently with her head and shoulder, then settle. Never widen, orbit to her face or reveal the throne behind camera.',transition_zh='承左手松开切近过肩，头肩接同一次起身；镜内0–2秒抬起上身，2–4秒随站起升高并收停，4–6秒站定目送。图片只作目送终态参考。',transition_en='Cut from the released left fingers to a tight view from behind her shoulder, continuing one rise. The reference depicts the standing END state, not the opening frame.',action_zh_override=s['action'],action_en='Within this shot, all following times are relative to its start: at 0-2 seconds, GPT releases her cheek support and pushes her upper body up; only the cropped half back of her head and one shoulder lift in the near left foreground. At 2-4 seconds she completes the same rise as the camera gently rises with her shoulder and settles. Her legs plant, wings fold and single tail clears the chair frame OFFSCREEN; do not reveal these actions or widen the shot. At 4-6 seconds she stands still watching the distant child continue away, back to camera, through the far door. Keep the child clear and the foreground softly out of focus. The throne remains behind camera, outside the image. No full face, full body or repeated rise.')
save(f,d)
f='视频制作/生成板-v005/批次计划.json';d=load(f);d['shot_notes']['CY009A']='当前图为紧过肩目送终态；只露半个后脑与一个肩膀，远处小鱼背影清晰。镜内0–4秒随同一次起身轻升并收停，4–6秒目送；腿、尾巴与王座均在画外。';save(f,d)
f='资产/assets.json';d=replace(load(f),oldspace,newspace)
for a in d['assets']:
 for ref in a.get('related',[]):
  if ref.get('path')==OLD:ref.update(path=NEW,role='肩后紧过肩：半个后脑与肩压前景，远处小鱼离去，王座在机后画外')
save(f,d)
f=REC+'/变更核验.json';d=load(f);d['previous_reverse']=OLD;d['current_reverse']=NEW;d['author_revision']='作者认为广角张力不足，改为半后脑与单肩前景、远处小鱼的紧过肩镜头';save(f,d)
assert all(s['source_quote'] in script for s in p['shots'])
print(json.dumps({'source_sha256':newhash,'current_reverse':NEW,'source_quotes':len(p['shots'])},ensure_ascii=False))
