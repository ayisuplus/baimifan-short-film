from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];G=R/'视频制作/Metaso-H3-v006';p=G/'执行队列.json';q=json.loads(p.read_text(encoding='utf8'));aid='GB011-1-v006-CY020A-force-r2'
assert not any(x['attempt_id']==aid for x in q['items'])
ref=G/'参考/CY020A-站立对峙参考.png'
q['items'].append(dict(attempt_id=aid,batch_number=13,batch_id='GB011-1',shot_ids=['CY020A'],duration=4,mode='reference_image',references=[dict(path=ref.relative_to(R).as_posix(),role='reference_image',sha256=hashlib.sha256(ref.read_bytes()).hexdigest())],prompt="""4秒日系动画动作镜。Image 1仅用于人物身份、蓝发鲸帽小女孩和黑金法衣棕发教主、紫色法杖、冷蓝教堂与暖烛光的连续性；重新设计摄影机与全身站姿，不复刻参考图的低机位截脚构图。机位在两人侧面略高俯视，能一直看清小女孩两只蓝靴与石地接触、成人右侧腿脚和空闲手，男左手握紫杖保持不动。孩子在画面左、男人在右，孩子身高到男人腰部。两人同一块水平石质缓台，严禁悬浮、提起、抱住或托住孩子。
0至0.65秒，女孩双脚牢牢踩地，身体前倾挡路，两手推抵男人黑金袍腹前。0.65至1秒，男人空闲手突然短促推开她的肩头，掌根接触即发力，0.25秒内松手收回，不摸头不抓手不扶抱；孩子上身被推后仰，先从近侧脚跟开始失去支点。1至1.6秒，孩子双脚慌乱后退一步，后脚踩滑，重心落到支撑面外。1.6至2.1秒，孩子一只手拍到地面，臀侧随之落地；没有受伤血迹。2.1至4秒，手掌受重、蓝帽垂下、身体蜷缩停一拍后抬眼，父亲袍角已经越过她向前半步。所有动作遵循接触→冲量→脚滑→落地顺序，重力方向一直朝石地；孩子双脚只在真正摔倒瞬间抬起，严禁像木偶吊起、坐空气或轻柔放下。落地附近摄影机轻微震动一次，其余固定。姿势有清楚变形与恢复，动作不是均匀慢动作；完整4秒，无切镜、无变脸、无对白、无字幕、无BGM。""",change_reason='r1悬浮和轻放落座拒用；单镜重构脚与地面的受力链，不重做整批',repair_of='GB011-1-v006-CY020A-force-r1',estimated_credits=40.8,status='prepared',acceptance=['起态两脚接地','手掌短促接触后收回','接触早于失衡','失衡到手掌落地连续','孩子不是被抱起或放下']))
p.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8');print(aid)
