"""One-time author revision: replace cushion gripping with gentle hand rubbing."""
import copy,hashlib,json
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
SOURCE='镜头设计/shot-plan-v0.55.json';REC='镜头设计/生成记录/宫殿躺姿-v055'
OLD='镜头设计/图像/宫殿躺姿-v055/CY010.png';NEW='镜头设计/图像/宫殿躺姿-v055/CY010-r2-搓手.png'
def load(f):return json.loads((R/f).read_text('utf-8-sig'))
def save(f,d):(R/f).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def sha(f):return hashlib.sha256((R/f).read_bytes()).hexdigest()
def rep(v,a,b):
 if isinstance(v,str):return v.replace(a,b)
 if isinstance(v,list):return [rep(x,a,b) for x in v]
 if isinstance(v,dict):return {k:(x if k.startswith('previous') else rep(x,a,b)) for k,x in v.items()}
 return v
p=load(SOURCE);by={s['id']:s for s in p['shots']};s=by['CY010'];n=by['CY009A']
if s['presentation']['path']!=OLD:raise SystemExit('Later hand revision exists; will not overwrite.')
previous=copy.deepcopy(s);previous_next=copy.deepcopy(n);oldhash=sha(SOURCE)
p=rep(p,OLD,NEW);by={s['id']:s for s in p['shots']};s=by['CY010'];n=by['CY009A']
s['previous_shot_v055_grip']=previous;n['previous_shot_v055_before_hand_rub']=previous_next
s.update(title='轻轻搓手的迟疑',framing='双手与淡紫软垫近距离特写',purpose='用轻柔搓手表现想帮忙却仍犹豫，保留慵懒和可爱，不演成生气。',entry_state='远钟传来，小鱼脚步仍在远处；GPT侧躺，右手原在脸侧，左手松搭垫边。',action='镜内0–0.7秒，GPT将右手从脸侧放下，靠垫继续承托头肩，双手在软垫上方松松相合；0.7–2.5秒，手掌与指腹轻轻来回摩挲两下，手指自然微弯，动作小而慢；2.5–3秒停住，双手仍松合。她保持侧躺，不抓软垫、不攥拳、不用力绞手，起身留到下一镜。',exit_state='双手轻搓后已停住，松松合在软垫上方；托腮已解除，下一镜才分手撑起身体。',sound='一声远钟及连续尾韵，轻微袖料声；小鱼远去的脚步在画外延续。')
s['source_quote']='钟声传来，ChatGPT把托腮的右手放下，头肩仍倚着靠垫。她将双手松松合在软垫上方，轻轻搓了两下，又停住。那点犹豫显得温软，手指没有抓紧任何东西。'
s['invariants']=[x for x in s['invariants'] if '本镜只有自身左手' not in x and 'GPT自身右手托右腮' not in x]
s['invariants'].append('本镜从托腮过渡到双手轻搓；头肩由靠垫承托，不提前起身。双手松合，动作小而慢，不抓垫、不攥拳、不用力绞手。')
s['presentation'].update(path=NEW,visible='双手松松合在淡紫软垫上方，手掌与指腹轻轻摩挲的中间状态；软垫没有抓皱。',status='作者指定轻搓双手；新静帧待作者审阅',missing='静帧仅展示手部姿态，缓慢摩挲及前后衔接待视频验证。')
s['refs'][0]['role']='双手轻搓的中间状态参考，不是固定首帧';s['refs'].insert(1,{'path':OLD,'role':'历史抓垫稿；作者认为像生气，已替换为搓手'})
s['generation_request']=REC+'/搓手修订.json'
s['cinematic_beats']=[{'offset':0,'intent':'右手从脸侧放下，双手松合'},{'offset':0.7,'intent':'掌与指腹轻轻摩挲两下'},{'offset':2.5,'intent':'停止摩挲，双手保持松合'}]
w,h=Image.open(R/NEW).size;s['page_size']=[w,h];s['panel_rect_pixels']=[0,0,w,h]
n['entry_state']='双手轻搓后停住、托腮已经解除；GPT仍侧躺，小鱼在远处出口附近。切至肩后近景，随后双手分开，左掌撑垫起身。'
n['action']=n['action'].replace('承左手松开，镜内0–2秒GPT解除托腮并撑起上身','承双手轻搓后的停顿，镜内0–2秒GPT分开双手、左掌撑垫抬起上身')
n['source_quote']=n['source_quote'].replace('ChatGPT解除托腮，撑起上身','ChatGPT停下搓手，分开双手，以左掌撑垫抬起上身')
n['cinematic_beats'][0]['intent']='双手分开、左掌撑垫，近过肩头肩随上身轻抬'
by['CY009']['next_link']='接 CY010：'+s['entry_state'];s['next_link']='接 CY009A：'+n['entry_state']
p['continuity']['palace']=p['continuity']['palace'].replace('孩子离开后左指压垫再松开，接解除托腮、撑垫收腿落脚与起身目送。','孩子离开后放下托腮的右手、轻搓双手并停住，再分手撑垫、收腿落脚与起身目送。')
p['continuity']['insert_motif']=p['continuity']['insert_motif'].replace('左指压软垫','轻搓双手')
for k in ['subtitle','review_intro']:p[k]=p[k].replace('软垫迟疑','搓手迟疑')
sf=p['story_script'];script=(R/sf).read_text('utf-8-sig')
for a,b in [(previous['source_quote'],s['source_quote']),(previous_next['source_quote'],n['source_quote'])]:
 assert a in script;script=script.replace(a,b,1)
(R/sf).write_text(script,'utf-8');assert all(x['source_quote'] in script for x in p['shots']);save(SOURCE,p);newhash=sha(SOURCE)
for f in ['后期/宫殿躺姿-v055/预演编排.json','后期/宫殿躺姿-v055/作者确认选曲.json','视频制作/生成板-v005/人物核对.json','视频制作/生成板-v005/声音核对.json']:
 d=rep(rep(load(f),oldhash,newhash),'软垫边的迟疑',s['title']);save(f,d)
f='视频制作/生成板-v005/人物核对.json';d=load(f);d['shots']['CY010'].update(note='只见GPT双手与袖口；右手已经离开脸侧，与左手轻柔摩挲。小鱼画外，头肩由靠垫支撑。',basis='作者本轮指定搓手；主线程实看新手部静帧');save(f,d)
f='视频制作/生成板-v005/动态审查.json';d=load(f);b=d['batches']['GB005'];v=b['shots']['CY010'];a=b['shots']['CY009A']
b['arc_zh']='小鱼独自离去，GPT仍侧躺；钟声里放下托腮的右手，轻搓双手两下后停住，才分手撑起身体，目送远处背影。'
b['arc_en']='The child leaves while GPT reclines. At the bell she lowers her right hand from her cheek, gently rubs her hands together and pauses, then separates them to rise once and watch the departure.'
v.update(camera_zh='保持双手和软垫的近距离特写；右手入画后，双手轻搓并停住，机位稳定，保留自然微动。',camera_en='Hold a close detail of both hands and the cushion. Her right hand enters, the palms rub gently and pause. Keep the camera steady with natural micro-movement.',action_zh_override=s['action'],action_en='Times are relative to this shot: at 0-0.7 seconds GPT lowers her right hand from her cheek to loosely meet her left hand above the cushion; her head and shoulder remain supported by the pillow. At 0.7-2.5 seconds she gently rubs her palms and fingertips together in two small slow passes, relaxed fingers slightly bent. At 2.5-3 seconds she stops with hands loosely together. She remains reclining, without gripping fabric, clenching fists or forceful hand-wringing. Do not sit up yet.')
a['action_zh_override']=n['action'];a['transition_zh']=a['transition_zh'].replace('承左手松开','承搓手停住、双手分开')
a['transition_en']='Cut from the pause after gentle hand rubbing to the tight shoulder view. Her hands separate and she begins one rise; cheek support has already been released. The image is the standing END state, not the opening frame.'
a['action_en']=a['action_en'].replace('GPT releases her cheek support and pushes her upper body up','GPT separates her relaxed hands, places her left palm on the cushion and pushes her upper body up')
save(f,d)
f='视频制作/生成板-v005/批次计划.json';d=load(f)
for b in d['batches']:
 if b['id']=='GB005':b['title']='独自离去、搓手迟疑与起身目送'
d['shot_notes']['CY010']='双手轻搓中间状态参考；前0.7秒先放下托腮的右手，摩挲两下后停住。不抓布、不攥拳，身体仍侧躺。';save(f,d)
print(json.dumps({'source_sha256':newhash,'image':NEW,'seconds':s['seconds'],'source_quotes_verified':132},ensure_ascii=False))
