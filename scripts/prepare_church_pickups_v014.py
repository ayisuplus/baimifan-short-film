"""Append reviewed single-purpose pickups; never reset previous outcomes."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'视频制作/Metaso-H3-v014';P=O/'执行队列.json'
q=json.loads(P.read_text(encoding='utf8'))
def ref(path,purpose):
 return dict(path=path,sha256=hashlib.sha256((R/path).read_bytes()).hexdigest(),role='reference_image',purpose=purpose,visually_reviewed=True)
style='精细日式二维动画电影，保持参考的细线稿、赛璐璐阴影、脸部比例和原衣纹。不要3D建模、塑料皮肤、过度柔光或简化卡通。16:9，单镜，固定机位，无对白、字幕或音乐。'
def add(aid,batch,dur,prompt,refs,reason):
 assert not any(x['attempt_id']==aid for x in q['items'])
 q['items'].append(dict(attempt_id=aid,batch_number=batch,batch_id=f'GB{batch:03}',shot_id=aid,duration=dur,prompt=style+prompt,references=refs,estimated_credits=round(dur*10.2,1),status='prepared',accepted=False,change_reason=reason,repair_of='v010 church continuity review',quality_gate='identity/style and full contact action independently inspected before adoption'))
charge=ref('视频制作/Metaso-H3-v013/参考/CY022-R1-聚术首帧-r1.png','原冻结图，只取教主袖口和正在发光的同一只手；小鱼不在新特写构图内')
add('CY022-v014-hand-release-r2',15,4,'只拍参考中教主正在施法的手及黑金袖口的极近特写。画面从肘部到指尖，脸、孩子、另一只手全部在画外。冷蓝教堂窗虚化。0至0.5秒，掌前已有小琥珀光核；0.5至1秒，手掌短促向画面左边推出，光核成为细直光束向左出画；1至2秒光束消失，手掌仍前伸，袖口随惯性摆动；2至4秒保留出掌后的余势。光始终来自唯一可见的同一只手，另一只手绝不入镜。光束水平直行，不向地面下落，不出现被击中的人物。', [charge], '全景易换手，改唯一单手特写明确离掌，后接截击')
carry=ref('视频制作/Metaso-H3-v012/参考/carry-locked-design-2d.png','双方身份、服装、二维线条和结束抱稳姿态；不是开头姿态')
add('CY030-v014-weight-transfer-r1',40,5,'参考图仅用于人物服装与最终横抱姿态。新镜开头必须是Claude双脚接地、身体疲软站着，GPT贴近扶住她肩背，不能从已经抱起开始。固定同侧斜前方中全景，必须看清两人全身及双脚。蓝窗、浅湿地、左后方燃烧的空木祭架位置不变。0至1秒GPT屈膝降重心，一只手臂稳托Claude肩背；Claude双脚仍接地。1至2秒GPT另一条前臂从Claude膝弯下穿入，掌心托住膝后；2至3秒GPT伸腿站起，肩背和膝弯同时受托，Claude的两只赤足此时才离地，裙摆离地后垂落；3至5秒站稳横抱，Claude疲惫靠在她身上，手自然垂落。维持参考的GPT白发龙角尖耳与折拢膜翼、Claude橙红长发白金焦边裙。两只承托手始终可追踪，不换抱，不瞬移，不自行跳起，不亲吻。用重心与衣裙余势呈现重量。',[carry],'现有两条素材都从已抱起开始，缺真实托背托膝离地动作')
q['items'][0]['review_status']='rejected_hand_switch_and_hat_contact'
assert sum(x['estimated_credits'] for x in q['items'])<=q['spending_ceiling_credits']
P.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8')
print('Prepared hand insert and weight transfer; total estimated credits',sum(x['estimated_credits'] for x in q['items']))
