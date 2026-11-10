"""Only the two approved, unresolved local windows; preserve source voices."""
from pathlib import Path
import json, shutil, hashlib, subprocess, wave
import numpy as np
R=Path(__file__).resolve().parents[1]; O=R/'视频制作/Metaso-H3-v012'; D=O/'参考'; D.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
P=json.loads((R/'后期/二维动漫纠偏-v005/后期执行计划.json').read_text(encoding='utf8'))
G=Path('C:/Users/36322/.codex/generated_images/01a17883-69dd-74f1-8f13-bbde7422c943')
assert not (O/'执行队列.json').exists(),'Already prepared; never overwrite a submitted queue'
items=[]
for key,gen,voice_id,start,frames,duration in [('support','exec-07bc8da9-c7a7-4277-8475-0956e977d2de.png','VO-CY028A-01',9632,67,5),('carry','exec-93a7ff7a-7879-40df-aa57-dac6af956ec7.png','VO-CY028-01',10641,192,10)]:
 img=D/(key+'-locked-design-2d.png');shutil.copy2(G/gen,img)
 v=next(v for v in P['voice'] if v['id']==voice_id)
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',v['path'],'-ac','2','-ar','48000','-f','f32le','pipe:1'])
 voice=np.frombuffer(raw,dtype='<f4').reshape(-1,2);buf=np.zeros((duration*48000,2),np.float32)
 offset=(v['record']-start+12)/24; at=round(offset*48000);buf[at:at+len(voice)]=voice
 audio=D/(key+'-selected-voice.wav')
 with wave.open(str(audio),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(48000);w.writeframes((np.clip(buf,-1,1)*32767).astype('<i2').tobytes())
 common='这是本片二维动漫电影的实际表演镜头，不是漫剧，不是三维模型。严格照Image1的同一个人物设计、脸型、发色、眼色、头饰、领口、袖口、裙长与烧损黑边，不能改服装或增加露肤。线稿、薄花纹与分层色块贯穿每一帧；拒绝塑料皮肤、厚重雕塑蕾丝、模型发束、材质突然写实。人物的承重、呼吸、衣袖和头发必须真实运动，不能静帧推拉。只有参考音频中右侧银紫发GPT说日语，其余人不说话；严格依音频真实起停口型，静音时闭嘴，不加台词、字幕、音乐或旁白。'
 if key=='support':
  prompt=common+'\n5秒单镜，保持Image1双人中近景和原教堂冷蓝窗、木横架及打开的空腕扣位置。Claude在左侧，GPT在右侧，一手稳托Claude左上臂，另一手在画外支撑腰背。此前最后腕扣刚打开，本镜承接一次很小的身体重心下降：0–0.5秒准备承重；0.5–1.5秒Claude小心迈下低脚托（脚在画外，不生成新脚托），身体下移约半个头高，GPT同步屈膝承接、双手不放开；GPT在音频约0.58秒开始温柔说“ゆっくりでいい。”，Claude闭口听。1.5–2.5秒两人稳定落在同一地面，衣裙和发丝延迟轻落；2.5–3.3秒Claude疲惫地看向左下画外寻找孩子，GPT仍关切看她。3.3–5秒保持闭口、呼吸和轻微衣发余势。不得后仰摔倒，不公主抱，不重新锁腕，不出现Kimi特写或第三人，不额外挂水珠/蒸汽。背景仍原冷蓝夜景，没有火、没有新石阶。摄影机稳定随身体小幅下跟，前后空间不变，不加切镜。'
 else:
  prompt=common+'\n10秒，保持Image1同一蓝窗湿地与左后方燃烧的空木架，火在安全背景距离，人物衣服不燃烧。Image1是抱稳后的造型与姿态参考，不强制首帧已完成抱起。镜头为同侧斜前方中景，人物方向不翻转。0–0.5秒承接Claude已经膝软，GPT立即托住腰背，不能凭空瞬移到怀中。0.5–2秒GPT屈膝降重心、另一只手从Claude膝后托入，两只手连续接触、稳稳承重；Claude橙发、头纱与金纹焦边衣裙保持完整，赤脚自然悬垂。2–3.2秒GPT抱稳后凭腿部伸展站起，不让Claude主动跳跃，不再重复下蹲；上升时衣裙拖曳后跟。3.2–4.3秒GPT按音频轻说“行こう。”，Claude闭口靠稳，不亲吻；GPT眉眼坚定温柔。4.3–6秒抱持稳定并转眼望向出口，6–8.5秒保持同一方向迈出很小的一步，衣摆尾巴跟随。8.5–10秒保留转身前余量。不能增删翅膀、尾巴、花饰、珠链，禁止手指融合、额外腿、抱姿穿模，保持2D线稿，不加新人物或出门远景。'
 refs=[dict(path=img.relative_to(R).as_posix(),role='reference_image',sha256=sha(img),purpose='经原图对照的同设计二维输入',visually_reviewed=True),dict(path=audio.relative_to(R).as_posix(),role='reference_audio',sha256=sha(audio),seconds=duration,purpose='原已选GPT工作声，仅加静音对位，音色/速度不变')]
 items.append(dict(attempt_id='GB027-v012-support-close-r1' if key=='support' else 'GB030-v012-carry-design-r1',batch_number=37 if key=='support' else 40,batch_id='GB027' if key=='support' else 'GB030-1',duration=duration,prompt=prompt,references=refs,estimated_credits=duration*10.2,status='prepared',timeline_window=[start,start+frames],proposed_source_window=[12,12+frames],voice_id=voice_id,voice_reference_offset=offset,accepted=False))
q=dict(model='MiniMax-H3',provider='metaso',resolution='768P',ratio='16:9',authorization='2026-10-29用户明确批准实施局部修复方案；只有无合格旧源的两处，保留Kimi与原造型，不导出',spending_ceiling_credits=153,items=items)
save(O/'执行队列.json',q)
html='<meta charset="utf-8"><title>两处局部补拍输入 v012</title><h1>扶稳 / 抱起：原造型局部补拍</h1><p>总计15秒生成候选，预计153积分；仅拟替换67+192帧，尚未采用。</p>'
import html as H
for b in items:html+='<h2>'+b['attempt_id']+'</h2><p>'+str(b['timeline_window'])+'</p><img style="max-width:900px" src="'+b['references'][0]['path'].replace('视频制作/Metaso-H3-v012/','')+'"><audio controls src="'+b['references'][1]['path'].replace('视频制作/Metaso-H3-v012/','')+'"></audio><pre style="white-space:pre-wrap">'+H.escape(b['prompt'])+'</pre>'
(O/'补拍输入.html').write_text(html,encoding='utf8')
print('Prepared two local candidates, estimated 153 credits; not submitted')
