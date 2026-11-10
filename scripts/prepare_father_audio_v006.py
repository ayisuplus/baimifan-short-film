from pathlib import Path
import json,subprocess,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'后期/导演重构-v003';G=R/'视频制作/Metaso-H3-v006'
def read(p):return json.loads(p.read_text(encoding='utf8'))
a=read(O/'开始时达芬奇实际状态.json')['result'];v=[x for x in a['audio'] if x['track']==1 and x['name']=='VO-CY021A-01'];pieces=[]
for x in v:
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(x['source_start_time']),'-i',x['path'],'-t',str((x['end']-x['start'])/24),'-ac','1','-ar','48000','-f','f32le','pipe:1']);pieces.append(np.frombuffer(raw,dtype='<f4'))
y=np.concatenate([np.zeros(16800,np.float32),*pieces]);y=np.pad(y,(0,288000-len(y))).astype('<f4')
audio=G/'参考/教主-作者当前剪辑-口型基准.wav'
subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar','48000','-ac','1','-i','pipe:0','-c:a','pcm_s24le',str(audio)],input=y.tobytes(),check=True)
refs=[]
for p,role in [(G/'参考/教主-当前说话状态.png','reference_image'),(audio,'reference_audio')]:
 d=dict(path=p.relative_to(R).as_posix(),role=role,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 if role=='reference_audio':d['seconds']=6
 refs.append(d)
q=read(G/'执行队列.json');aid='GB010-v006-CY021A-audio-r1';assert not any(x['attempt_id']==aid for x in q['items'])
q['items'].append(dict(attempt_id=aid,batch_number=12,batch_id='GB010',shot_ids=['CY021A'],duration=6,mode='reference_with_selected_audio',references=refs,prompt='6秒16:9日系动画近景，严格保持Image 1人物教主的年龄、棕发、黑金法衣、胸前饰物、紫色法杖与教堂阶梯空间。以祭坛上女儿看向台阶下父亲的轻俯拍近景，只见父亲头肩和原背景，不引入女儿或孩子。保持冷蓝环境与克制暖烛光，木柴尚未点燃，天顶尚未破损。Audio 1是本镜唯一日语原声时间基准，必须照实际音频逐时刻驱动教主唇形和下颌；台词我が娘よ、神がお待ちだ。不能另读、改词、改变声线、吞停顿或重新提前音频。Audio 1前0.35秒静音保留，静音时双唇闭合，音频停顿时也停止说话，末尾闭口等待。父亲看着上方女儿，表情坚定而冷淡，不微笑，不夸张摇头；说神がお待ちだ时眼神变硬，靠眼神而不是全身晃动。全程单镜，脸部清晰，嘴无遮挡，只有极轻缓推近。无额外说话者、配乐、字幕或剪镜。',change_reason='用作者当前剪过20帧的原选声驱动口型，替换多段快慢嘴；保留原音剪辑决定',estimated_credits=61.2,status='prepared',acceptance=['口型依Audio1开合及停顿','人物服饰法杖一致','不新增台词或额外演员']))
(G/'执行队列.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8')
print(aid)
