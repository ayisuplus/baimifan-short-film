"""Record independently reviewed source windows and explicit editorial compromises."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'后期/教堂动画修订-v011';Q=R/'视频制作/Metaso-H3-v014/执行队列.json'
q=json.loads(Q.read_text(encoding='utf8'));edl=json.loads((R/'后期/局部收口-v008/后期执行计划.json').read_text(encoding='utf8'))['edl'];paths={Path(x['source']).name:x['source'] for x in edl}
def seg(file,a,b,batch,note,old=None,frames=None):
 path=paths.get(file,str(R/'视频制作/Metaso-H3-v014/产物'/file));assert Path(path).exists()
 n=frames or b-a
 return dict(source=path,**{'in':a,'out':b},frames=n,speed=(b-a)/n*100,props={},batch=batch,note=note,old_sound_start=old)
rescue=[seg('GB013-H3-v001.mp4',0,72,16,'Claude受火煎熬，省略重复列队慢走',4418),seg('CY022-v014-release-r1.mp4',0,18,15,'仅采用已独立复核的0–18聚术；拒绝换手后段'),seg('CY022-v014-hand-release-r2.mp4',18,34,15,'单手离掌特写，短转腕作为切位省略'),seg('GB013-v005-CY023-r1.mp4',31,55,16,'脚踹门接触一击'),seg('CY023-v014-water-close-r2.mp4',4,22,16,'单手握拳出水，向右截击'),seg('CY022-v014-air-intercept-r2.mp4',16,34,16,'无人净空对冲，在亮点切开'),seg('CY022-v014-grip-free-r2.mp4',28,88,16,'手明确离开上臂；细节切位连接',frames=40),seg('CY024A0-v014-rescue-carry-r2.mp4',0,123,17,'托臀后离地并退柱；右手保留折扇并短暂辅助承托')]
shield=[seg('CY024K3-v014-shield-close-r1.mp4',0,32,20,'持刃起身'),seg('GB014-v002.mp4',120,132,20,'敌方反应遮接快速拉远段',4886),seg('CY024K3-v014-shield-close-r1.mp4',42,96,20,'同一蓝紫月罩连续封顶、恢复暗膜')]
carry=[seg('GB030-1-v003.mp4',78,108,40,'星火术名后离指',10446),seg('GB030-1-v003.mp4',108,126,40,'空架',10476),seg('GB030-1-v003.mp4',153,228,40,'空架燃起',10521),seg('GB030-1-v003.mp4',228,252,40,'Claude闭眼脱力，切落坐后的GPT接近',10596),seg('CY030-v014-weight-transfer-r1.mp4',0,90,40,'坐地后下蹲托背托膝、承重离地；不再直接跳成横抱')]
edits=[dict(start=4418,end=4838,segments=rescue,reason='补齐聚术、离掌、破门、水击、空中截击、松手、抱离，删除静止列队',sound_events=[dict(id='V3-church-fire-return',offset=0,duration=sum(s['frames'] for s in rescue)/24,gain_db=-5),dict(id='V3-spear-whoosh',offset=96,duration=.4,gain_db=-6),dict(id='SFX-063',offset=105,duration=.5),dict(id='SFX-064',offset=106,duration=.6),dict(id='V3-water-collect',offset=130,duration=.7,gain_db=-5),dict(id='V3-fan-catch',offset=152,duration=.35,gain_db=-4),dict(id='SFX-097',offset=222,duration=.7),dict(id='SFX-162',offset=238,duration=1.2,gain_db=-4)]),dict(start=5466,end=5571,segments=shield,reason='月罩从无到完整闭合，消除圆盘硬切暗球；敌方反应遮接模糊段',sound_events=[dict(id='V3-fan-shield',offset=40,duration=2,gain_db=-3)]),dict(start=10368,end=10689,segments=carry,reason='星火释放与燃架紧接术名；接抱补真实承重动作，脱力落坐用切镜省略',sound_events=[dict(id='SFX-162',offset=156,duration=2.5,gain_db=0)])]
result=dict(edits=edits,voice_relative={'VO-CY024-01':dict(edit_start=4418,offset=296)},review_method='Three independent action reviews plus lead visual inspection; source windows above only',editorial_choices=['GPT改为握拳出水，单手方向一致','千问右手保留合扇并短暂辅助承托，人物设计和抱持因果优先','Claude脱力落坐用近景转中景省略，随后拍清下蹲与托抱；不宣称站立直接接重','护盾形成态蓝白、终态深紫，作为同一月罩的能量建立'],author_final_accepted=False)
(O/'补镜采用清单.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
used={Path(s['source']).stem:[] for e in edits for s in e['segments']}
for e in edits:
 for s in e['segments']:used[Path(s['source']).stem].append([s['in'],s['out']])
for x in q['items']:
 if x['attempt_id'] in used:x.update(review_status='selected_windows_for_v011_author_review',selected_source_windows=used[x['attempt_id']],accepted=False)
 elif x['status']=='downloaded_candidate':x.update(review_status='not_selected_preserved')
Q.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8');print('Recorded reviewed rescue, shield and carry edits')
