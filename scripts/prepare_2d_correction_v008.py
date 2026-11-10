from pathlib import Path
import json,hashlib,shutil,copy,html
R=Path(__file__).resolve().parents[1];O=R/'后期/截图定点修正-v004';G=R/'视频制作/Metaso-H3-v008';G.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf8'))
def ref(path,purpose):return dict(path=path.relative_to(R).as_posix(),role='reference_image',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),purpose=purpose)
style=ref(O/'证据/二维基准/adjacent-B24-3s.png','唯一画风标准：原片GPT与Kimi手绘二维线条、离散明暗色块；不引用月球场景与坐姿')
q7=read(R/'视频制作/Metaso-H3-v007/执行队列.json');old={x['attempt_id']:x for x in q7['items']}
early=read(O/'二维纠偏-前段补拍草案.json');items=early['items']
standard='制作标准的二维手绘日本动漫电影动画，与Image1原片的二维人物画法一致。线条刻画脸、发束、衣褶和手指；皮肤使用干净底色及边界清楚的两到三层手绘阴影，高光为设计色块。背景为绘制的动画背景。必须排除3D建模、三维CG渲染、PBR塑料或蜡皮肤、连续光滑球面渐变、游戏过场感。不能做成漫剧、静态插画推拉、单图骨骼拉扯或只动嘴的纸片人。角色由关键姿势与自然中间动作连续表演，重心转移、预备、发力、惯性余势和头发衣摆跟随清楚；嘴型仍严格跟随已选Audio1真实发声与停顿。Image1只决定二维画法，不出现月球、岩石或坐姿；Image2只决定本镜人物、服装、道具和空间，彻底重绘成Image1那种二维动画，禁止继承Image2的建模表面。'
def add(oldid,newid,body,visual=None):
 x=copy.deepcopy(old[oldid])
 for k in ['task_id','local_path','sha256','bytes','submit_started','provider_status','review_decision','review_reason','adopted_ranges']:x.pop(k,None)
 images=[r for r in x['references'] if r['role']=='reference_image'];aud=[r for r in x['references'] if r['role']=='reference_audio']
 x.update(attempt_id=newid,status='prepared',prompt=standard+'\n'+body,references=[style,visual or images[0]]+aud,change_reason='作者明确排除3D建模感，按片中多数标准2D动漫纠偏；保留已修好的声音时码和因果')
 items.append(x)
add('GB014-v007-group-entry-style-audio-r1','GB014-v008-group-2d-r1','5秒门口入场。Image2的人物和武器都保留，门已被上一镜打碎，0秒起就敞开，不能重演开门。镜头低位稍偏侧，破木为前景，白发双角GPT在前，伙伴前中后三层错开。0–1秒GPT迈入；1–3.5秒是完整可剪用的命令与警戒：她踩稳脚，侧转头确认同伴并作一个简洁护卫手势；伙伴向两翼移动半步并抬起原有武器，姿态各有差别，不整排同步走秀。Audio1从0秒播放，只有GPT在约1.333秒说二人を守って。口部与眼神随短促坚决的表演变化，其他人闭嘴。3.5–5秒停在警戒姿态并保持呼吸、发梢和衣摆余势。面部和衣料必须是清楚手绘线稿与色块，不是游戏模型。无切镜、字幕、BGM或新增台词。')
add('GB018-v007-gpt-rise-style-audio-r1','GB018-v008-gpt-rise-2d-r1','8秒GPT展翼并咏唱。Image2锁定白色衣裙、双角和两片薄膜龙翼；必须手绘重绘翼骨、膜面与全身，画出来的翼膜阴影不是3D透光材质。0秒从地面脚尖承重开始，0–1.5秒屈膝一点、翼根下压、双翼有力扇下、重心向上、脚尖离地，衣摆和发束延迟跟上，地面空气波用二维速度线和少量尘点表现。1.5–3.7秒同侧机位随人轻抬至三分之四中景，避免对称正面全身摆拍和吊灯穿身。她抬眼看向穹顶，3.791667秒起只按Audio1说蒼穹の果てに座し、，实际起止随原声，不在静音提前开口。说完闭口直到8秒，只有头发/衣摆继续运动，嘴不循环。前7.25秒须完整可用。不要像3D角色展示、不要摄影机环绕模型、不要动态漫画静图平移。保持原服装/身份，教堂场景不变，不增加其他人、字幕、音乐。')
bridge=ref(O/'证据/native-stair-bridge.png','只用已建立的四人身份、扶持关系、上下台阶站位；建模质感必须改为二维手绘')
add('GB027-v007-stair-eyeline-r1','GB027-v008-stair-eyeline-2d-r1','4秒连续二维动漫过肩空间镜。Image2的构图关系保持：阶上近前景橙发Claude已经解锁，白发有翼GPT在她侧后扶住上臂；四级以上台阶下，紫发千问抱着蓝鲸帽小鱼。四个人各一，不增人物，衣裙原样，Claude焦边保留。角色的脸、头发、布料都像Image1一样由线条与色块绘制，不能用光滑三维模型。Claude先由撑住身体到轻轻转头低望孩子，GPT的手随其重心小幅调整支撑；千问抬眼，小鱼攥衣襟后把目光抬向阶上，表演先后有因果，不让四个人机械同时动。Audio1从0秒是Claude原有あの子は……，只有她发声；约1.51秒后闭口停住，GPT与另外两人全程不串嘴。摄影机固定过肩，不能只推拉一张插画当动画。前3.4167秒完整可用，最后保留动作余势。背景台阶是二维绘景，外形与高低不变；不发明光效、人物瞬移、字幕或BGM。',bridge)
for x in items:
 x['status']='prepared'
 for r in x['references']:assert hashlib.sha256((R/r['path']).read_bytes()).hexdigest()==r['sha256']
q=dict(model='MiniMax-H3',resolution='768P',ratio='16:9',spending_ceiling_credits=300,authorization='作者继续要求定点修正并明确必须标准二维动漫、不得3D建模或漫剧；沿用授权Metaso H3，只有4个风格失败局部',items=items)
assert not (G/'执行队列.json').exists();(G/'执行队列.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8');shutil.copyfile(R/'视频制作/Metaso-H3-v007/上传索引.json',G/'上传索引.json')
page='<meta charset="utf-8"><title>二维动漫纠偏输入v008</title><style>body{max-width:1000px;margin:35px auto;background:#111822;color:#eee;font:18px/1.7 system-ui}pre{white-space:pre-wrap}a{color:#adf}</style><h1>四处二维动漫纠偏</h1><p>以片中多数二维镜头为基准，保留现有声音与剪辑时码；必须是有角色表演的动画，不是静图推拉漫剧。每镜2张视觉参考。预计214.2积分，候选回片再审。</p>'
for x in items:page+='<h2>'+x['attempt_id']+'</h2><ul>'+''.join('<li>'+html.escape(r['purpose']+'：'+r['path'])+'</li>' for r in x['references'])+'</ul><pre>'+html.escape(x['prompt'])+'</pre>'
(G/'补拍输入.html').write_text(page,encoding='utf8');print([(x['attempt_id'],x['duration']) for x in items])
