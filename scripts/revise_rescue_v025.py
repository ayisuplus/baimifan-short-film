"""Apply approved post-battle dialogue and two local frame changes, preserving history."""
import copy, hashlib, json, shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/战后对白与补镜-v025'
IMG='镜头设计/图像/战后对白与补镜-v025'
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,s):(R/p).write_text(s,encoding='utf-8')
def save(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
old=json.loads(read('镜头设计/shot-plan-v0.24.json'));d=copy.deepcopy(old)
shots={s['id']:s for s in d['shots']}
script=read(old['story_script'])
lines=script.splitlines();lines[2]='版本：v0.25｜2026-10-22｜战后解锁与接抱对白采用；新增CY028A2千问怀里的小鱼特写，强化CY029B空刑架火势。新生成两图为候选待审，其他已采用画面和历史稿保留。';script='\n'.join(lines)+'\n'
stand=shots['CY028A']['source_quote']
standnew='ChatGPT 扶住 Claude，等她从固定脚托上迈下。\n\n**ChatGPT：**\n慢慢来。\n\nClaude的赤足站稳同一祭坛平台，目光越过GPT，寻找阶下那个蓝色身影。\n\n**Claude：**\n那个孩子……'
child='切到阶下千问怀里的小鱼特写：蓝鲸帽下的小脸还留着泪痕，蓝色眼睛疲倦却清醒地抬向高处祭坛；她轻轻攥着千问的衣襟，后背与身体被稳稳承托。千问低头照看她。此刻只有冷月光，刑架尚未重新点燃。'
answer='**ChatGPT（画外）：**\n她没事，在下面等你。'
assert stand in script;script=script.replace(stand,standnew+'\n\n'+child+'\n\n'+answer+'\n\n确认小鱼有人照顾，Claude紧绷的肩膀慢慢松下来。',1)
script=script.replace('Claude！回来！','Claude……过来。',1)
script=script.replace('Claude 的肩膀下意识一缩。','教主叫她的名字时带着虚弱，后半句仍保留惯于命令她的口气。\n\nClaude 的肩膀下意识一缩。',1)
oldreact=shots['CY029E']['source_quote'];newreact=oldreact.replace('喊声尾音','呼唤的尾音');script=script.replace(oldreact,newreact,1);shots['CY029E']['source_quote']=newreact;shots['CY029E']['action']=newreact
fire='Claude回望空十字架，抬起一只手。橙金火焰跃向空木架，随即沿立柱与横木猛然翻卷上冲；厚实火舌裹住木料、越过横梁，空架轮廓与锁链仍从火隙中显露。镜头从低位略向刑架推进，焰浪向上掠出画面，短促的腾燃声接替教主呼唤的尾音。ChatGPT守在Claude身侧，同伴已经退开；火势止于刑架，没有扑向人物、蔓延地面或点燃建筑，普通灯具仍熄灭。随后收手、接抱及离殿时，旺盛燃烧转为刑架上的持续火光。'
script=script.replace(shots['CY029B']['source_quote'],fire,1)
held=shots['CY028']['source_quote'];script=script.replace(held,held+'\n\n**ChatGPT：**\n我们走。',1)
write('剧本/穿云-场景剧本-v0.25.md',script)
d.update(version='v0.25',revision='v025',title='《穿云》带图分镜 v0.25 · 战后对白与小鱼回应',subtitle='补小鱼被抱护的确认镜；空刑架火势增强',story_script='剧本/穿云-场景剧本-v0.25.md',source_manifest='镜头设计/生成记录/生成索引-v025.json',origin_manifest='镜头设计/shot-plan-v0.24.json')
d['review_intro']='战后对白已由作者确认。新增小鱼被千问抱护的视线回应特写，GPT画外说明她已安全；空刑架改为厚实火势上冲。两张新图待作者审阅，动态及新声音未制作。'
d['review_focus']='扶稳与询问→小鱼被抱护特写及GPT画外回答→力量回归→父亲命令→无言焚架→脱力接住→我们走。'
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.24.json',previous_html='镜头设计/带图分镜-v0.24.html',added_ids=['CY028A2'],modified_ids=['CY028A','CY029','CY029E','CY029B','CY028'],boundary='新增3秒小鱼特写；CY028A由3秒暂放宽至5秒以承载搀扶、两句对白及寻找视线。其余旧镜时长不变。共94镜304秒，旧93镜仅CY029B换图，旧图全保留。')
def dialogue(s,dialogue,quote,cues,sound):
 s.update(dialogue=dialogue,source_quote=quote,subtitle_cues=cues,dialogue_cues=[],dialogue_timing_status='provisional_subtitles_pending_voice_readthrough')
 s['sound']=sound+' 新配音未制作；字幕仅为阅读暂排，实际说话与动作节奏待声音预演。'
def cue(who,text,offset,duration):return dict(speaker=who,text=text,offset=offset,duration=duration)
s=shots['CY028A'];s['seconds']=5
dialogue(s,'ChatGPT：慢慢来。\nClaude：那个孩子……',standnew,[cue('ChatGPT','慢慢来。',0.2,1.5),cue('Claude','那个孩子……',2.6,2.0)],'锁链余响与滴水声。GPT贴着搀扶动作轻声安抚；Claude站稳后带牵挂寻找小鱼。')
s['action']='GPT轻声说“慢慢来”，扶Claude从脚托迈下站稳；Claude望向阶下，问“那个孩子……”。'
s['exit_state']='Claude的视线落向阶下千问抱着小鱼的位置。';s['next_link']='接CY028A2：顺Claude向下寻找的视线，切小鱼被千问抱护的特写，GPT回答跨切画外。'
s['presentation']['missing']+=' 新增寻找视线及口型尚未制作，旧静帧保留。'
new=copy.deepcopy(shots['CY028A']);new.update(id='CY028A2',title='她在下面等你',seconds=3,framing='轻俯视近景／小鱼面部与千问承托手臂同框',purpose='用可见的抱护状态回应Claude的牵挂，补齐寻找视线与确认安全的因果。',entry_state='Claude已站稳并寻找小鱼，GPT在她身侧回答。',action=child,exit_state='小鱼清醒地抬眼且有人抱护，Claude确认后转回自身状态。',next_link='接CY028B：确认小鱼安全后，回到Claude，力量在指尖恢复。',asset_ids=['CHAR-DEEPSEEK','ENV-CHURCH'],invariants=['时间为战后解锁之后、Claude焚刑架之前；只有冷月光，不出现火焰或龙影。','小鱼仍由千问抱护，不凭空独自站起；两人的接触与承托明确。','GPT的回答在画外，她仍在最高祭坛Claude身边，不移动到小鱼身边。','镜头是高处视线引出的近景，不是通过望远魔法观察；背景不重建整座教堂。'])
dialogue(new,'ChatGPT（画外）：她没事，在下面等你。',child+'\n\n'+answer,[cue('ChatGPT（画外）','她没事，在下面等你。',0.0,2.9)],'GPT答句跨切至小鱼特写，保持祭坛方向与距离感；滴水与安静呼吸，不添加小鱼新台词。')
new['presentation']=dict(path=IMG+'/CY028A2-v025-r1.png',role='action',visible=child,status='v0.25新增候选，待作者审阅',missing='静帧能显示抱护与抬眼；呼吸、抓衣襟、眼神接续及配音未动态制作。',show_as_main=True)
new['generation_request']=REC+'/CY028A2-请求-v001.json';new['visual_prompt']=json.loads(read(new['generation_request']))['prompt'];new['refs']=[dict(path=new['presentation']['path'],role='当前候选'),dict(path=new['generation_request'],role='冻结实际输入'),dict(path='资产/图像/C04_Qwen.png',role='千问身份与衣装参考')]
new.pop('claude_accessory_state',None)
new['editorial_review']=dict(version='v025',status='candidate_pending_author_review',dynamic_execution='pending')
d['shots'].insert(d['shots'].index(shots['CY028A'])+1,new)
s=shots['CY029'];s['retired_dialogue_cues']=copy.deepcopy(s['dialogue_cues'])
dialogue(s,'教主：Claude……过来。','**教主：**\nClaude……过来。',[cue('教主','Claude……过来。',0.3,3.4)],'教主虚弱地叫她的名字，后半句仍有命令意味；Claude肩膀下意识缩起。旧“回来”读稿停用并保留历史。')
s=shots['CY029B'];s.update(source_quote=fire,action='Claude抬手点燃空刑架；有厚度的火势沿立柱和横木猛然上冲，锁链与空架从火隙中显露，火止于刑架。',framing='低位中远景／短促向空刑架推近／起火高峰关键帧',sound='短促腾燃声接教主呼唤余音，继而是强烈木料燃烧与锁链热颤。无新对白、无爆炸声；音效尚未制作。')
s['cinematic_beats']=[{'offset':0,'intent':'指尖引火，保留Claude决断手势'}, {'offset':0.6,'intent':'短促向刑架推进，火势沿木架上冲并越出画面上缘'}, {'offset':2.3,'intent':'火势进入持续燃烧，切收手脱力，避免前后忽然跳成小火'}]
oldfire=s['presentation']['path'];s['presentation'].update(path=IMG+'/CY029B-v025-r1.png',visible=s['action'],status='v0.25火势强化候选，待作者审阅',missing='此图为腾燃高峰代表帧；推近、起火到持续燃烧的过渡、后续镜火光强度及声音待动态验证。')
s['generation_request']=REC+'/CY029B-请求-v001.json';s['visual_prompt']=json.loads(read(s['generation_request']))['prompt'];s['refs']=[dict(path=s['presentation']['path'],role='本轮强化候选'),dict(path=oldfire,role='保留上一版'),dict(path=s['generation_request'],role='冻结实际输入')];s['editorial_review']=dict(version='v025',status='candidate_pending_author_review',dynamic_execution='pending')
s=shots['CY028'];dialogue(s,'ChatGPT：我们走。',held+'\n\n**ChatGPT：**\n我们走。',[cue('ChatGPT','我们走。',0.8,1.8)],'抱稳后GPT轻声说“我们走”；Claude抬眼，下一镜主动搭肩，保留衣料与呼吸声。')
elapsed=0
for s in d['shots']:
 s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
 if s['id'] in ['CY028A2','CY029B']:
  with Image.open(R/s['presentation']['path']) as im:w,h=im.size
  s['page_size']=[w,h];s['panel_rect_pixels']=[0,0,w,h];s['panel_region']=dict(x=0.0,y=0.0,w=1.0,h=1.0);s['panel_index']=0
d['total_seconds']=elapsed
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']];sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
d['continuity']['postbattle_eyeline']='CY028A寻找阶下小鱼→CY028A2千问抱护小鱼且GPT画外回答→CY028B力量回归。小鱼眼中不再有战斗时的龙影。'
d['continuity']['cross_fire']='CY029B为空刑架起火高峰，向上翻卷而非横向爆炸；随后在刑架上持续燃烧。后续画面保留，动态衔接须控制火势回落及反光，不令普通灯具复燃。'
save('镜头设计/shot-plan-v0.25.json',d)
history=R/'镜头设计/带图分镜-v0.24.html'
if not history.exists():shutil.copy2(R/'镜头设计/带图分镜.html',history)
p='scripts/build_storyboard.py';code=read(p).replace('shot-plan-v0.24.json','shot-plan-v0.25.json').replace('"v024")','"v024", "v025")').replace("'v024')","'v024','v025')")
write(p,code)
cache=Path('C:/Users/36322/.codex/generated_images/01a162c1-6e38-7a10-aee7-5c8371c4830c')
records=[]
for sid,uid in [('CY028A2','2d58f3ad-a6b6-42ee-8126-7c34d0645f39'),('CY029B','a212f1e4-51b3-4bc2-9a68-38dd26f67037')]:
 path=R/IMG/(sid+'-v025-r1.png');original=cache/('exec-'+uid+'.png');req=R/REC/(sid+'-请求-v001.json');q=json.loads(req.read_text(encoding='utf-8'))
 assert sha(path)==sha(original)
 records.append(dict(shot_id=sid,original=str(original),destination=path.relative_to(R).as_posix(),sha256=sha(path),request=req.relative_to(R).as_posix(),request_sha256=sha(req),inputs=[dict(path=p,sha256=sha(Path(p))) for p in q['referenced_image_paths']],status='candidate_pending_author_review'))
index=dict(version='v025',previous_index=old['source_manifest'],records=records,review=REC+'/复核记录.md')
save('镜头设计/生成记录/生成索引-v025.json',index);save(REC+'/结果映射.json',index)
entry=read('00_打开项目.html').replace('v0.24','v0.25').replace('93 镜 · 4 分 59 秒','94 镜 · 5 分 04 秒').replace('救援对白更新；画面保持','战后对白与小鱼补镜；刑架火势增强').replace('护住她们 · 抱紧我 · 聒噪保留','慢慢来 · 那个孩子 · Claude过来 · 我们走')
entry=entry.replace('<a href="镜头设计/图像/',f'<a href="{IMG}/CY028A2-v025-r1.png">新增：千问怀里的小鱼特写<small>Claude寻找视线的回应 · 新图待审</small></a>\n<a href="{IMG}/CY029B-v025-r1.png">修订：空刑架火势上冲<small>腾燃高峰代表帧 · 新图待审</small></a>\n<a href="镜头设计/图像/',1)
write('00_打开项目.html',entry)
p='制作进度.md';text=read(p);idx=text.index('## ')
note='''## 2026-10-22：战后对白、小鱼回应与刑架火势（v0.25）

作者确认本段建议，并要求补千问怀里的小鱼特写、强化空刑架火势。已采用GPT“慢慢来。”、Claude“那个孩子……”、GPT“她没事，在下面等你。”、教主“Claude……过来。”及GPT“我们走。”。教主旧“回来”临时读稿停用，原音频和旧稿保留。焚架与接住瞬间不另加台词。

[当前分镜](镜头设计/带图分镜.html)与[剧本v0.25](剧本/穿云-场景剧本-v0.25.md)同步。新增CY028A2三秒特写接Claude向下寻找视线，GPT回答跨切画外；CY028A由三秒暂放宽至五秒，供扶稳、安抚与询问。当前94镜304秒（5分04秒）；其余旧镜时长保持。字幕仅阅读暂排，实际配音/动作节奏待制作。

两张内置imagegen新图均为候选待作者审阅：小鱼在千问怀里清醒抬眼，CY029B火势沿空架翻卷上冲。短促推近、腾燃声和火势转持续燃烧写入分镜，尚未制作视频/声音。后续镜头火光过渡留动态核对，原画未批量重绘。原93镜只替换一张火势候选，其他92图保持；原v0.16锁定文件不改写。见[复核记录](镜头设计/生成记录/战后对白与补镜-v025/复核记录.md)。

'''
write(p,text[:idx]+note+text[idx:]);print('v0.25 prepared:',len(d['shots']),elapsed)
