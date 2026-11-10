from pathlib import Path
import json,subprocess,hashlib,shutil,html
import numpy as np
R=Path(__file__).resolve().parents[1];G=R/'视频制作/Metaso-H3-v007';O=R/'后期/截图定点修正-v004'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
P=read(R/'后期/导演重构-v003/后期执行计划.json');voices={v['id']:v for v in P['voice']}
def audio(id,parts,dur):
 x=np.zeros(round(dur*48000),np.float32)
 for vid,t in parts:
  v=voices[vid];raw=subprocess.check_output(['ffmpeg','-v','error','-i',v['path'],'-ac','1','-ar','48000','-f','f32le','pipe:1']);a=np.frombuffer(raw,dtype='<f4');i=round(t*48000);assert i+len(a)<=len(x);x[i:i+len(a)]+=a
 p=G/'参考'/(id+'.wav');subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar','48000','-ac','1','-i','pipe:0','-c:a','pcm_s24le',str(p)],input=x.astype('<f4').tobytes(),check=True);return p
cl=audio('Claude-两种表演原声',[('VO-CY020-01',1),('VO-CY021-01',5.15)],11)
father=G/'参考/教主-当前剪辑原声.wav';shutil.copyfile(R/'视频制作/Metaso-H3-v006/参考/教主-作者当前剪辑-口型基准.wav',father)
style='严格延续Image 1原片的高细节二次元三维渲染与精细插画融合质感：细密发丝、柔和皮肤体积、蕾丝与刺绣、木纹和真实空间景深、冷蓝窗光与暖烛边光。不要重画成平涂赛璐璐、粗线漫画或廉价2D动画，不换脸型、五官年龄、服装和饰物位置。即使嘴动也要保持原片的面部立体光影。'
items=[]
def add(id,batch,shot,dur,img,aud,prompt):
 refs=[dict(path=str(img.relative_to(R)).replace('\\','/'),role='reference_image',sha256=sha(img),purpose='当前相邻原片的身份、服装、渲染和光影唯一视觉基准'),dict(path=str(aud.relative_to(R)).replace('\\','/'),role='reference_audio',sha256=sha(aud),seconds=dur,purpose='作者已选实际声音，包含真实停顿及对位静音')]
 items.append(dict(attempt_id=id,batch_number=batch,batch_id=shot,duration=dur,mode='reference_with_selected_audio',references=refs,prompt=prompt,estimated_credits=round(dur*10.2,1),status='prepared',acceptance=['原片画风/面部/服装不跳变','音频发声时嘴动、静音时闭口','眼神和受缚或站立状态符合剧情','存在完整可用的目标时长'],change_reason='作者截图明确否定上一轮画风与口型；只修定点区间'))
add('GB011-v007-Claude-style-audio-r1',13,'GB011-1+GB011-2',11,G/'参考/Claude-原片风格.png',cl,style+'\n11秒连续近景，Claude仍双腕受缚在高坛横木，脚下柴未点燃，不出现释放、松链、流血、火烧或其他人。保持Image1的花饰、头纱、露肩白金蕾丝衣裙与黑胸结；镜头完整看见头顶到胸前，双腕边缘保留，禁止极端裁脸和持续推近。摄影机位于台阶下略仰拍，Claude视线落在右下方父亲与更低处的小鱼。\nAudio 1从0秒原样播放，是唯一台词与口型逐时刻基准。第一句その子に触らないで！在约1秒开始，喊声坚决愤怒，眉眼用力，不能带笑；真实起止以音频为准。之后闭口，眼神追随孩子在阶下失衡，身体仍被束缚，只有肩膀挣动。源片4.75秒进入第二种表演，目光转向父亲，约5.15秒后的音频说お父様……その子を逃がして。称呼后的长停顿必须闭唇，眼神由愤怒变为忍住恐惧的恳求，第二半句再开口，不能从头到尾循环张嘴。说完闭口等待至11秒；无新增词、气词或第二人声。\n全程只有同一Claude近景；没有切镜、换景、字幕、BGM；发丝轻微摆动，面部清晰，不摇头遮嘴。前0–4.75秒和后4.75–10.75秒分别需要成为可独立剪用的连续表演，4.75秒处嘴闭可安全切点。')
add('GB010-v007-father-style-audio-r1',12,'GB010',6,G/'参考/教主-原片风格.png',father,style+'\n6秒教主说话近景。只留Image1棕发教主的胸像与原有深蓝高窗背景，不出现前景递杖教徒，也不出现新增火盆、人群或孩子。教主已接过紫焰权杖，左手稳握，紫焰为已有法术，不是柴火。摄影机在他侧面稍低、三分之二侧脸，脸与嘴清晰，仍有完整额头下巴和肩膀。男人从阶下转头抬眼望向画外上方受缚女儿，说我が娘よ、神がお待ちだ。不要看向地上的孩子说此句；眼神傲慢冷硬、没有笑，头部转动很小。\nAudio1是作者实际剪过的唯一原声口型时间基准，从0秒播放，包含前0.35秒静音、句中停顿与末尾等待。嘴形必须按Audio1真实发声与停顿开闭，不改字、另读或重排音频，不增加第二句。末尾闭口停住。光照和材质延续参考原片，不变成平涂漫画脸。固定中近景，无快速推镜、极端大头、切镜、字幕、BGM。')
q=dict(model='MiniMax-H3',resolution='768P',ratio='16:9',spending_ceiling_credits=1000,authorization='用户要求修正九张截图并明确继续；延续已授权Metaso H3局部补拍范围，修完待作者核定后再查全片',items=items)
assert not (G/'执行队列.json').exists()
(G/'执行队列.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8')
shutil.copyfile(R/'视频制作/Metaso-H3-v006/上传索引.json',G/'上传索引.json')
page='<meta charset="utf-8"><title>截图定点补拍 v007</title><style>body{font:18px/1.7 system-ui;max-width:1000px;margin:40px auto;background:#171c25;color:#eee}pre{white-space:pre-wrap}img{max-width:600px}article{margin-bottom:50px}a{color:#acf}</style><h1>仅修作者截图的镜头</h1><p>Metaso MiniMax H3，768P普通通道，原选声音频参考；补拍候选待作者核定。旧版保留、不导出。</p>'
for i in items:page+='<article><h2>'+i['attempt_id']+'</h2><p>'+str(i['duration'])+'秒 · 预计'+str(i['estimated_credits'])+'积分</p><ul>'+''.join('<li>'+html.escape(r['role']+'：'+r['path']+'；'+r['purpose'])+'</li>' for r in i['references'])+'</ul><pre>'+html.escape(i['prompt'])+'</pre></article>'
(G/'补拍输入.html').write_text(page,encoding='utf8')
print(json.dumps([dict(id=i['attempt_id'],seconds=i['duration'],estimate=i['estimated_credits']) for i in items],ensure_ascii=False))
