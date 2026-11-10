from pathlib import Path
import json,hashlib,subprocess,copy,html
R=Path(__file__).resolve().parents[1];G=R/'视频制作/Metaso-H3-v007'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def ref(p,role,purpose,seconds=None):
 d=dict(path=p.relative_to(R).as_posix(),role=role,purpose=purpose,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 if seconds:d['seconds']=seconds
 return d
q=read(G/'执行队列.json');assert not any(x['attempt_id'].endswith('style-audio-r2') for x in q['items'])
old=q['items'][0];old['review_decision']='rejected';old['review_reason']='开头凭空出现鱼形物体；原参考边缘小鱼帽子被误解，不能直接采用。'
x=copy.deepcopy(old)
for k in ['task_id','local_path','sha256','bytes','submit_started','provider_status','review_decision','review_reason']:x.pop(k,None)
x.update(attempt_id='GB011-v007-Claude-style-audio-r2',status='prepared',change_reason='只改失败条件：上一条4.5秒无杂物且材质一致的近景作唯一视觉参考，避免帽子误读')
x['references'][0]=ref(G/'参考/Claude-修净近景.png','reference_image','r1源4.5秒实际无杂物近景；维持原片细节、脸型、光影')
x['prompt']+='\nImage1已是干净的Claude近景，整条片始终维持此景别，不先拉到全身、不增加任何鱼、鱼形玩偶、动物、小鱼角色、其他人或前景道具。唯一画面是被缚Claude的面部、头纱、肩胸、双腕边缘及横木。不要在最后加笑容或说新台词。'
q['items'].append(x)
v=next(v for v in read(R/'后期/导演重构-v003/后期执行计划.json')['voice'] if v['id']=='VO-CY028A-02')
aud=G/'参考/bridge-Claude问孩子.wav'
subprocess.run(['ffmpeg','-y','-v','error','-i',v['path'],'-af','apad','-t','4','-ac','1','-ar','48000','-c:a','pcm_s24le',str(aud)],check=True)
q['items'].append(dict(attempt_id='GB027-v007-stair-eyeline-r1',batch_number=37,batch_id='GB027-to-GB028',duration=4,mode='reference_with_selected_audio',status='prepared',estimated_credits=40.8,references=[ref(G/'参考/bridge-阶上.png','reference_image','Claude已解锁与GPT搀扶状态、服装、台阶'),ref(G/'参考/bridge-阶下.png','reference_image','台阶下千问怀抱小鱼的身份服装与状态'),ref(aud,'reference_audio','已选Claude问孩子原声，约1.51秒后闭口',4)],prompt='4秒电影空间桥接镜头。严格延续Image1和Image2细密发丝、精细蕾丝金属、皮肤体积和冷蓝光的二次元三维插画融合质感，不改平涂漫画。Image1为阶上受救出的橙发Claude与扶她的白发有翼GPT；Image2为台阶下紫发千问抱着蓝帽小鱼。四个人各一个，不能融合、换服、缩小成玩具。Claude双手已经解锁，衣裙有原片焦黑边，GPT轻扶她右上臂。摄影机在Claude左后肩上方，以橙发头纱和自由垂手作近前景，向下方看见至少四级完整石阶，阶下三米处千问抱着小鱼抬头。台阶向画面右下延伸，明确高度差与安全距离。保持同一侧轴线，固定景别不切镜。Claude轻轻转头看向阶下孩子，Audio1从0秒播放她现有的あの子は……，仅Claude发声，语音1.51秒后停住；侧后机位不正面表演夸张口型，GPT和千问与孩子全部闭嘴。1.5秒后视线沿台阶停在孩子，克制呼吸，保持扶持关系至4秒，切下一镜小鱼反应。无水冲、落地瞬移、更多角色、脱衣、绑回锁链、超大法阵、字幕、BGM或额外声音。',acceptance=['上下台阶距离清楚','Claude已解锁且被GPT扶持','千问怀抱小鱼身份准确','可剪前82帧，不重复旧小鱼反应'],change_reason='替换B37末段重复的小鱼镜及回切，先交代阶上到阶下，再接B38原反应'))
(G/'执行队列.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8')
with (G/'补拍输入.html').open('a',encoding='utf8') as f:
 for i in q['items'][-2:]:f.write('<article><h2>'+i['attempt_id']+'</h2><pre>'+html.escape(i['prompt'])+'</pre></article>')
print([(i['attempt_id'],i['status']) for i in q['items']])
