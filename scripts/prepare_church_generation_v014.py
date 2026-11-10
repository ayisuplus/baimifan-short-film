"""Prepare one reviewed, bounded action test. Does not submit or overwrite."""
from pathlib import Path
import json,copy
R=Path(__file__).resolve().parents[1];O=R/'视频制作/Metaso-H3-v014';O.mkdir(exist_ok=True)
qpath=O/'执行队列.json';assert not qpath.exists(),'Preserve existing queue'
old=json.loads((R/'视频制作/Metaso-H3-v013/执行队列.json').read_text(encoding='utf8'))
ref=copy.deepcopy(old['items'][0]['references'][0])
ref['purpose']='原冻结静帧独立复核：人物、握持、冷蓝窗与暖光一致；不是拒用视频的抽帧。只证明可见局部空间。'
prompt='''4秒单镜，精细日式二维动画电影。严格保持首帧全部人物、脸型、服饰、线条与赛璐璐阴影，保持同侧低位斜仰机位，人物大小和站位不变。画面左下的蓝发鲸帽小女孩被左侧黑袍人的手扣住上臂；右侧棕橙发教主面向她；唯一黑紫火把由右后方黑袍人持有。无对白，所有人嘴闭合。
只完成一次短促施法：开头已有光核，0至0.6秒教主把首帧中已经伸向画面左侧、掌前带光的那一条手臂微微回收，肩肘蓄力；0.6至1.2秒同一条手臂沿原方向快速伸直，琥珀光核从这只掌心离开，成为一条向画面左下净空运动的细光迹。不要把光核传给另一只手，不另举第二只手。1.2至4秒在光迹尚未触及女孩前，保持出掌后的肩臂姿势与衣袖短暂余势，光迹出画，小女孩没有被击中、没有伤口、没有被抛飞。她被扣住的上臂、手掌和抓持者接触点始终不变。
摄影机固定、不绕行、不切镜、不拉远，不再花几秒重新生成大光球。不要发射向地面下坠的光球；只向左下的画外净空发出短直光迹。石阶仍干燥，本镜没有水、护盾、水龙、雨、刀具或新人物。不要3D建模、塑料皮肤、手办质感、字幕、音乐。'''
q=dict(model='MiniMax-H3',provider='metaso',resolution='768P',ratio='16:9',authorization='作者要求直接修复教堂段，密塔剩余额度优先，不足转本地ComfyUI；现余额971.3，经控制台实时核实。保留历史，不充值，不导出。',spending_ceiling_credits=900,balance_observed_credits=971.3,balance_source='https://metaso.cn/minimax-h3-console',balance_observed_date='2026-10-29',items=[dict(attempt_id='CY022-v014-release-r1',batch_number=15,batch_id='GB012',shot_id='CY022-R1',duration=4,prompt=prompt,references=[ref],estimated_credits=40.8,status='prepared',accepted=False,change_reason='上一回片换手且光核下坠；只补同一手短促离掌',repair_of='CY022-v013-charge-release-r1 rejected video; original still independently reviewed',quality_gate='same emitting arm; no contact with child; style and grip stable')])
qpath.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8')
print('Prepared one 4-second action test; estimate 40.8 credits')
