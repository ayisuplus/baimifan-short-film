from pathlib import Path
import json,hashlib,copy,shutil,html
R=Path(__file__).resolve().parents[1];G=R/'视频制作/Metaso-H3-v010';G.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
assert not (G/'执行队列.json').exists()
old=next(x for x in read(R/'视频制作/Metaso-H3-v009/执行队列.json')['items'] if x['batch_id']=='GB014')
x=copy.deepcopy(old)
for k in ['task_id','local_path','sha256','bytes','submit_started','provider_status','review_decision','review_reason','adopted_ranges']:x.pop(k,None)
path='镜头设计/图像/目光与入场-v048/CY024-v048-r1.png';sha=hashlib.sha256((R/path).read_bytes()).hexdigest()
assert sha=='b8a6dd3356348c52dd4f426e3b8973a8adf20417878a5718a83621e84c17be74'
prompt='''5秒，16:9，二维动漫电影的连续动作镜头。唯一Image1是本片原始采用分镜；它同时决定人物外貌、完整人数、服装、场景、光线和画风。不附人物四视图，也没有其他视觉参考。保持Image1原本精细的二维人物线条、柔和分层上色、发束与衣裙细节，不另画成简化粗线平涂风格，更不能变成三维建模、手办、塑料皮肤或游戏CG。必须是有完整重心变化与动作余势的动漫动画，不是静态插画推拉、漫剧或皮影式摆动。
场景严格延续Image1：蓝色月夜，正后高处圆月与远处哥特尖塔、左右高耸石柱与蓝色彩窗、原来旗帜的位置、湿润深色地面反射冷蓝月光和局部暖色火光、已有破门碎木。没有太阳，没有白昼蓝天，没有干燥浅灰地坪，不增加坍塌、废墟、白色台阶或另建一座教堂。镜头在殿内低位朝入口，保持原图透视轴线和前中后景关系。
必须恰好保留Image1中的九位同伴，每位一人；不是八人。中心白发双角GPT向前半步；画面左侧从远到近原有黑发红白衣、浅色发兽耳浅蓝白衣、黑发黑衣、紫发持扇、橙发红帽剑士五人；右侧金发黑红衣持斧、紫发紫衣、蓝绿发持杖三人。各自身份、头饰、武器和站位保持，不合并、删掉或新增角色。GPT的白色长裙、龙角、花饰等沿图，不简化为另一个角色。
从图中姿势开始：0–1秒GPT先迈进半步并踩稳，队友略有先后跟入，衣发随步伐滞后。1–3.5秒她简洁抬手示意保护，侧转头少许确认两翼；同伴朝两侧让开半步并抬起原有武器警戒，移动幅度克制，九人持续可辨，不整排走秀、不重复开门。3.5–5秒停在戒备定势，保留呼吸、发梢衣摆余势。摄影机只小幅跟进，始终包含完整队伍和场景，不切镜。
Audio1从0秒播放，为作者已选GPT声音，前段静音后约1.333秒进入『二人を守って。』，以音频实际发声为准；只有中心GPT同步开口，其余八人不代说。念完闭口，不拖音、不新增台词，不生成BGM、字幕或参考编号。保留夜风与自然脚步，最终以原作者音轨后期装配。'''
x.update(attempt_id='GB014-v010-original-shot-only-r1',status='prepared',prompt=prompt,references=[dict(path=path,role='reference_image',sha256=sha,purpose='原生成板v025采用的CY024夜景分镜；本次唯一视觉输入，不重绘')]+[s for s in old['references'] if s['role']=='reference_audio'],change_reason='作者怀疑人物四视图风格干扰，明确要求试一次不传四视图；同时回到真正原分镜，禁止沿用漂移回片。',duration=5,estimated_credits=51)
q=dict(model='MiniMax-H3',resolution='768P',ratio='16:9',spending_ceiling_credits=51,authorization='作者2026-10-28明确：试着不传人物四视图试一下；单镜5秒测试，原分镜和原配音输入，不替换时间线',items=[x]);save(G/'执行队列.json',q);shutil.copyfile(R/'视频制作/Metaso-H3-v009/上传索引.json',G/'上传索引.json')
save(G/'试验约定.json',dict(hypothesis='省去人物四视图，并从原分镜直接驱动，能否改善对原画风/场景的保真',not_a_controlled_causal_ablation='本次同时移除后续重绘底图，且没有同seed的含四视图对照；不能据单次结果认定四视图是唯一原因',visual_inputs=1,turnarounds=0,video_refs=0,original_audio_preserved=True,timeline_mutation=False,acceptance=['原图蓝色月夜不变白天','九人完整、武器身份不乱','教堂入口轴线/彩窗/旗帜/湿地/既有破门状态一致','保留原图精细二维画法，不因动漫一词简化成另一种画风','有迈步受力和队友警戒动作，非静图推拉']))
(G/'输入与对照.html').write_text('<meta charset="utf-8"><title>原分镜单图试验</title><style>body{max-width:1100px;margin:30px auto;background:#111822;color:#eee;font:18px/1.6 system-ui}img,video{width:100%}pre{white-space:pre-wrap}</style><h1>第17批：不传人物四视图</h1><p>仅原分镜＋原选声；5秒H3，预计51积分。试验回片尚未采用，未改达芬奇。</p><img src="../../'+path+'"><pre>'+html.escape(prompt)+'</pre>',encoding='utf8')
print(dict(attempt=x['attempt_id'],images=1,turnarounds=0,estimate=51))
