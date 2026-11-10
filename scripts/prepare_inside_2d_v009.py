from pathlib import Path
import json,shutil,hashlib,copy
R=Path(__file__).resolve().parents[1];G=R/'视频制作/Metaso-H3-v009'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
q=read(G/'执行队列.json');assert not any(x['attempt_id'].startswith('GB006') for x in q['items'])
x=copy.deepcopy(next(x for x in read(R/'视频制作/Metaso-H3-v008/执行队列.json')['items'] if x['attempt_id'].startswith('GB006')))
for k in ['task_id','local_path','sha256','bytes','submit_started','provider_status','review_decision','review_reason','adopted_ranges']:x.pop(k,None)
target=G/'参考/inside-2d-keyframe.png';source=Path('C:/Users/36322/.codex/generated_images/01a17883-69dd-74f1-8f13-bbde7422c943/exec-10b5c09c-c367-4608-8f80-cfa973990d0b.png');shutil.copyfile(source,target)
x.update(attempt_id='GB006-v009-early-inside-2d-r1',status='prepared',prompt='标准二维手绘动漫电影动画，绝不是漫剧、静态插画推拉或3D动画。唯一Image1是已重绘的二维关键帧，严格保持人物、毛边、帽顶、发束、手脚的清楚线稿、平涂底色与硬边赛璐璐阴影，背景也是手绘绘景。4秒连续镜头。保持低机位从教堂侧洞内部看小鱼进入，只有这一个蓝鲸帽小女孩，不添加其他人或生物。0–1秒她手掌撑住洞内石地，肘部与肩膀实际受力，后膝跨过门槛；1–2秒重心前移，另一膝轻落地，耳朵侧听；2–3.3秒停下爬行，抬眼向高处教堂内部观察，担忧又坚定；3.3–4秒保留呼吸、发梢和毛球惯性，不反复爬动。不把背景水平移动当动作，四肢真实支撑身体，衣物延迟跟随。不说话、不张嘴，不加字幕、音乐，不做摄影机切镜或绕行，任何一帧都不能变成模型或塑料质感。',references=[dict(path=target.relative_to(R).as_posix(),role='reference_image',sha256=hashlib.sha256(target.read_bytes()).hexdigest(),purpose='入洞二维手绘重绘关键帧，毛边与帽顶建模感也完全排除')],change_reason='v008脸部二维改善但毛边/帽顶与发束仍偏体积；再用真正二维关键帧纠偏，不扩大镜头范围')
q['spending_ceiling_credits']=250;q['items'].append(x);save(G/'执行队列.json',q);print(x['attempt_id'])
