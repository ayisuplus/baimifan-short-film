"""A different, documented first-frame mode for persistent reference reconstruction defects."""
from pathlib import Path
import json,copy,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'视频制作/Metaso-H3-v002';REF=OUT/'修订参考'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
q=read(OUT/'执行队列.json');gen=Path.home()/'.codex/generated_images/01a17883-69dd-74f1-8f13-bbde7422c943'
images={'water-start':'exec-5e823bff-25e9-40d3-8bf0-43886692a6d5.png','rescue-key':'exec-2d53e5fa-f81d-46f6-8a0c-a239d68dd8f4.png','rescue-wrist':'exec-849145d6-a6fe-4afd-8b8f-04e0136e8f89.png','rescue-step':'exec-c9279479-48d5-4ac7-a3f6-ce6a9e65d795.png'}
for name,file in images.items():
 dest=REF/(name+'-固定首帧-r004.png')
 if not dest.exists():shutil.copy2(gen/file,dest)
common='从给定第一帧原样开始，只让已有画面动起来，不重新设计角色或背景。单一连续镜头，无切镜，无字幕水印、无音乐、无新增人物。'
jobs=[
 ('GB020-2-r003','GB020-2-r004',REF/'water-start-固定首帧-r004.png',common+'6秒，陡俯视相机缓缓沿画中纯水巨浪下降。保持首帧透明无眼球的水流形状，表面只有一直流动的泡沫与折射，任何时刻都没有实体动物、鳞片、眼睛亮点。0–4.8秒水流向完整屋顶迫近，4.8–5.59秒水流吻端只在中央中殿同一位置接触屋顶并压开第一处缺口，最后停留在撞点，后殿与左右窗完整。5.59–6秒延续水花，不产生第二次撞击。全程没有人体。GPT画外0–5.35秒自然说一次：<d>[Japanese] 今こそ天を開き、大海を翻せ。</d>。'),
 ('GB022-1-r003-part2','GB022-1-r004-part2',OUT/'审查/GB022-1-r002-part1-11.5.png',common+'4秒。白衣女子从首帧胸前手印开始，0–0.3秒迅速解开双手，0.3–0.8秒右臂向前伸出，0.8–1.2秒食指明确向前发令，左手自然收回胸前；1.2–1.5秒保持指向，身后纯水浪头沿指向前移响应。1.5–4秒只是持续这一末态，没有第二次手势。水流材质与首帧完全一致，流动透明水和泡沫，不新增眼睛、发光眼点、鳞甲或动物皮肤。脸、白银衣服和龙角翼尾保持，无对白。'),
 ('GB027-r002-CY027F2','GB027-r003-CY027F2',REF/'rescue-key-固定首帧-r004.png',common+'4秒，冷月光，所有烛芯与木柴始终熄灭无暖光。先延续暗罩正在散去，0–0.5秒背景暗膜散尽显出受缚的橙发Claude。右侧白银衣GPT伸出唯一黑铁钥匙，0.5–2秒将钥匙交进左侧黑紫衣Kimi掌心，Kimi接稳。2–3秒Kimi持钥匙稍俯身朝画外踝扣，3–4秒保持。只交一次钥匙，不解锁，不改变任一人的服装，不新增火、衣物燃烧或烛火。无对白。'),
 ('GB027-r002-CY027G','GB027-r003-CY027G',REF/'rescue-wrist-固定首帧-r004.png',common+'4秒，全程冷月照明，蜡烛、柴堆和衣裙始终熄灭。Claude双脚自由稳踩脚托，没有踝扣，只有画面左侧抬起的最后腕扣待打开。右侧白衣GPT先扶稳她的背和上臂；左侧Kimi在0–0.8秒用黑铁钥匙转动唯一剩余腕扣，0.8–1.5秒腕扣清楚张开离开手腕，1.5–2.5秒Claude把自由手臂落下，GPT继续承重，2.5–4秒保持。露出两个自由手腕与两个自由脚踝，锁扣只留木架，不能又长回人物身上。没有跌落、迈下或抱走。无对白。'),
 ('GB027-r002-CY028A','GB027-r003-CY028A',REF/'rescue-step-固定首帧-r004.png',common+'7秒，保持首帧无腕扣无踝扣、普通烛火柴火全熄灭的状态。白衣GPT持续扶住橙发Claude上臂与背。0–2.2秒Claude从小脚托谨慎迈下，赤足逐一落到湿石地面、承重站稳；GPT一直支撑，Kimi在左后方拿着已打开的空扣，不把扣放回Claude身上。2.2–2.7秒摄影机在同一侧平稳靠近到两人胸上近景。2.7–6.2秒Claude疲倦望向阶下画外寻找小鱼，GPT继续扶稳，6.2–7秒延续末态。不要公主抱，不重复迈下，不出现火焰和暖光。GPT在0.1–1.68秒自然说一次<d>[Japanese] ゆっくりでいい。</d>；Claude在2.8–4.31秒说一次<d>[Japanese] あの子は……</d>。其它时段闭口。'),
 ('GB026-r002-part1','GB026-r003-part1',ROOT/'镜头设计/图像/目光与入场-v048/CY027D-v048-r1.png',common+'4秒。严格固定首帧每人的位置、人数与抱持关系。只让前排人物微抬眼，衣发轻摆，摄影机轻推近，不走步不变队形。唯一戴鲸帽孩子只在画面左后方千问怀里，前排紫发猫耳女子的两手保持首帧姿势，没有孩子、娃娃、人物或新增物件。两翼银白骑士原地守卫。最高祭坛暗紫罩保持完全不透明，罩内没有任何可见人物或木架。不新增第二个孩子、不新增白发龙角GPT、不展示武器攻击。所有人面向镜头所在正门来敌，保持冷月夜景，前3秒用于剪辑。无对白。')]
for oldid,newid,path,prompt in jobs:
 if any(x['attempt_id']==newid for x in q['items']):continue
 old=next(x for x in q['items'] if x['attempt_id']==oldid);b=copy.deepcopy(old)
 for k in ['task_id','local_path','sha256','bytes','submit_started','provider_status']:b.pop(k,None)
 b.update(attempt_id=newid,prompt=prompt,status='prepared',accepted=False,repair_of={k:old[k] for k in ['attempt_id','task_id','local_path']},change_reason='参考模式重复重构出错误元素；改用官方固定首帧模式，锁住已修正的画面元素。',references=[dict(slot=1,path=path.relative_to(ROOT).as_posix(),sha256=sha(path),kind='first_frame',role='first_frame')],estimated_credits=round(old['duration']*10.2,2),mode='first_frame')
 q['items'].append(b)
q['estimated_total_credits']=round(sum(x['estimated_credits'] for x in q['items']),2)
assert q['estimated_total_credits']<=q['spending_ceiling_credits']
(OUT/'执行队列.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8')
print(len(q['items']),q['estimated_total_credits'])
