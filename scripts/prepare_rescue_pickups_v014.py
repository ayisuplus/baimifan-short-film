from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'视频制作/Metaso-H3-v014/执行队列.json';q=json.loads(P.read_text(encoding='utf8'))
def ref(path,purpose):return dict(path=path,sha256=hashlib.sha256((R/path).read_bytes()).hexdigest(),role='reference_image',purpose=purpose,visually_reviewed=True)
charge=ref('视频制作/Metaso-H3-v013/参考/CY022-R1-聚术首帧-r1.png','教主小鱼身份、黑袍抓持者、局部教堂轴线、原冻结画风')
qwen=ref('镜头设计/图像/张力与机位-v060/CY024A0-v060-r2.png','千问和小鱼脸型服饰与教堂冷蓝光；构图重新取中景')
gpt=ref('镜头设计/图像/独立镜头-v009/CY026A-v009.png','只借画左白发龙娘GPT身份服装和精细二维画风；不借云宫背景，不出现画右千问')
style='精细日式二维动画电影，保持参考细线稿、赛璐璐阴影、人物比例和精致服装。不要3D建模、塑料皮肤、漫剧推拉。16:9，固定同侧镜头，无字幕、对白、音乐。'
rows=[
 ('CY023-v014-water-shot-r1',16,4,[gpt],'''教堂内看向破开的大木门，月夜在门后。镜头只拍参考画左的白发龙娘GPT一人，膝上三分之四中景，白发双角尖耳、白银纹长裙和膜翼折拢保持。门板刚被踹裂，木屑还在落，画面开头她已经伸出右手掌朝教堂内，也就是画面右前方，左臂自然靠身。0至0.5秒只从这只前伸掌前喷出一束窄而快的清水，沿画面左到右出画，穿过已破开的门洞；0.5至1.5秒她收回踢门后的膝部，落脚稳重心，水束持续向右出画；1.5至4秒水束停止，湿袖与头发顺势回落。动作果断，不先走进门再蓄力；水不变龙，不出大浪，不变护罩，不出现其他人物、云宫、中式建筑。''','破门脚部之后缺水击发出因果'),
 ('CY022-v014-intercept-release-r1',16,4,[charge],'''沿参考同侧轴线取略宽中景：鲸帽小女孩画左下，黑袍教徒在她左后，单手扣住上臂；棕橙发黑金袍教主在右。开头教主已前伸掌，琥珀细光从右往左，距离孩子至少一臂；一束窄水流立即从画外左前侧进入，在孩子身体前方的空隙和琥珀光迎面相撞，局部白水雾闪开，术光向无人的上方散掉。整个碰撞在孩子轮廓之外。黑袍抓持者因水花惊退半步，抓持手张开并明确离开孩子上臂；女孩脚仍着地，退半步但不倒下。1.5至4秒看清女孩上臂已自由、抓持者后撤，水花落下。教主始终右侧，不换位；火把仍仅后方教徒持有。没有大洪水，不能浇灭画外祭架火焰，没有千问，没有新抱起动作，没有伤口。''','需要看见水术截击和抓持手真正松开'),
 ('CY024A0-v014-rescue-carry-r1',17,5,[qwen,charge],'''教堂石阶旁同侧中全景，开头小鱼鲸帽宝宝双脚着地，黑袍人已缩手在右后远处，没有继续抓她。蓝紫编发、花形帽饰、白内裙深蓝外衣的千问从画面左侧快速进入，右手低持一把合拢折扇，右手不参加抱持。0至1秒千问左手带孩子向自己身前离开黑袍人；1至2.5秒她屈膝贴近，以左臂从孩子臀下承托，将孩子抱到自己左髋，孩子双腿此时才离地，孩子自然依住她肩头。2.5至4秒千问带孩子退到画面左边最近石柱后，折扇仍在右手低位；4至5秒停稳确认孩子安全。清楚表现左前臂托臀承重，孩子不漂浮、不自动升空、不长大、不变脸；不换抱，不多臂，不丢扇，不围绕人物转镜。干地只有少量新水花。''','从松手到安全抱持缺少承重动作')]
for aid,b,d,refs,prompt,reason in rows:
 assert not any(x['attempt_id']==aid for x in q['items'])
 q['items'].append(dict(attempt_id=aid,batch_number=b,batch_id=f'GB{b:03}',shot_id=aid,duration=d,prompt=style+prompt,references=refs,estimated_credits=round(d*10.2,1),status='prepared',accepted=False,change_reason=reason,repair_of='v0.69 rescue gap',quality_gate='single action, consistent identity and axis, visible contact and weight'))
assert sum(x['estimated_credits'] for x in q['items'])<=q['spending_ceiling_credits']
P.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8');print('Prepared 3 rescue pickups; estimate',sum(x['estimated_credits'] for x in q['items']))
