from pathlib import Path
import json,hashlib,shutil,copy,html
R=Path(__file__).resolve().parents[1];G=R/'视频制作/Metaso-H3-v009';G.mkdir(exist_ok=True);(G/'参考').mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
assert not (G/'执行队列.json').exists()
q8=read(R/'视频制作/Metaso-H3-v008/执行队列.json')
files={'GB014':('group','exec-e73d47f4-aa9c-4879-8c22-90da232a7f69.png'),'GB018':('wing','exec-c9aae993-efd8-4d0b-86a5-0e301424da6d.png'),'GB027':('stairs','exec-9e993b1e-ad4c-4bfc-a7be-696b81288107.png')}
items=[]
for old in q8['items']:
 bid=old['attempt_id'].split('-')[0]
 if bid not in files:continue
 key,name=files[bid];source=Path('C:/Users/36322/.codex/generated_images/01a17883-69dd-74f1-8f13-bbde7422c943')/name;target=G/'参考'/f'{key}-2d-keyframe.png';shutil.copyfile(source,target)
 x=copy.deepcopy(old)
 for k in ['task_id','local_path','sha256','bytes','submit_started','provider_status','review_decision','review_reason','adopted_ranges']:x.pop(k,None)
 body=x['prompt'].split('\n',1)[1].replace('Image2','Image1')
 if bid=='GB018':body=body.replace('3.791667秒起只按Audio1说','保持闭口至4.058秒，4.058秒起只按Audio1实际发声说')
 standard='这是标准二维手绘动漫电影动画，绝不是漫剧或3D动画。唯一Image1是本镜已重绘的二维动画关键帧，严格继承其中黑色轮廓线、脸部平涂肤色、硬边赛璐璐阴影与手绘发束，整段不得转回3D模型/PBR/塑料手办/光滑渐变皮肤。人物从图中姿势进行完整手绘动画式表演，预备、发力、惯性跟随、动作之间自然衔接。禁止用静态插画推拉、皮影式摆动、循环张嘴代替动画。原有衣服、身份、人数和空间不变；Audio1是原作者选定配音，只有指定人物在实际发声时开口，禁止静音段提前开口。\n'
 x.update(attempt_id=x['attempt_id'].replace('v008','v009'),status='prepared',prompt=standard+body,change_reason='v008的建模风格残留拒用；先用内置imagegen真正重绘二维关键帧，再驱动H3动作。仅3个局部，原声音和时长保留。',references=[dict(path=target.relative_to(R).as_posix(),role='reference_image',sha256=hashlib.sha256(target.read_bytes()).hexdigest(),purpose='本镜二维重绘关键帧；构图/角色沿原镜，清楚线稿和硬边色块为唯一视觉输入')]+[r for r in x['references'] if r['role']=='reference_audio'])
 items.append(x)
q=dict(model='MiniMax-H3',resolution='768P',ratio='16:9',spending_ceiling_credits=200,authorization='作者授权继续修复截图范围，明确标准2D动漫、非漫剧；现有Metaso H3路由和选声不变',items=items)
save(G/'执行队列.json',q);shutil.copyfile(R/'视频制作/Metaso-H3-v008/上传索引.json',G/'上传索引.json')
page='<meta charset="utf-8"><title>二维关键帧驱动补拍v009</title><style>body{max-width:1000px;margin:40px auto;font:18px/1.7 system-ui;background:#111822;color:#eee}img{width:100%}pre{white-space:pre-wrap}</style><h1>二维动漫局部补拍</h1><p>三镜先重绘输入图，再由H3生成实际表演。不是以静图替代动画。预计173.4积分，未核账单。</p>'
for x in items:page+='<h2>'+x['attempt_id']+'</h2><img src="参考/'+Path(x['references'][0]['path']).name+'"><pre>'+html.escape(x['prompt'])+'</pre>'
(G/'补拍输入.html').write_text(page,encoding='utf8');print([(x['attempt_id'],x['duration']) for x in items])
