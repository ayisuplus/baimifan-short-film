"""Add Qwen's dialogue insert without altering existing image or voice files."""
import copy,json,hashlib,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,s):(R/p).write_text(s,encoding='utf-8')
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not (R/'镜头设计/shot-plan-v0.37.json').exists()
rec='镜头设计/生成记录/千问抱紧我-v037';dest='镜头设计/图像/千问抱紧我-v037/CY024A0-v037-r1.png'
source=Path('C:/Users/36322/.codex/generated_images/01a162c1-6e38-7a10-aee7-5c8371c4830c/exec-0c133691-d589-4c2b-8857-e45345697729.png')
(R/dest).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,R/dest)
o=json.loads(read('镜头设计/shot-plan-v0.36.json'));d=copy.deepcopy(o);by={s['id']:s for s in d['shots']};a=by['CY024A'];script=read(o['story_script'])
old=a['source_quote'];gpt=old[old.index('镜头转向ChatGPT'):]
quote='回闪结束，回到此刻的教堂。切千问与小鱼的双人近景，两人的脸和承托动作清楚可见。千问已退到右侧石柱内侧，用左臂将小鱼托稳、稍稍收紧抱持，右手在腰侧握着尚未打开的折扇。她低头看着孩子，轻声说：\n\n**千问：**\n抱紧我。\n\n小鱼攥紧千问的衣襟，向她靠过去。千问随后抬眼望向画外的GPT。近旁圣骑士护住柱外，Kimi已经在同侧后方持续护持Claude；水雷尚未释放，衣发和石面没有洪水打湿。'
assert script.count(old)==1;script=script.replace(old,quote+'\n\n'+gpt,1)
n=copy.deepcopy(by['CY028A2']);w,h=Image.open(R/dest).size;req=rec+'/CY024A0-请求-v002.json';spec=json.loads(read(req))
n.update(id='CY024A0',title='抱紧我',seconds=2,framing='千问与小鱼双人近景／说话者与受话者同框',purpose='落实抱紧我的说话者、对象和抱护动作，预告GPT即将升空施法。',entry_state='召集回闪结束；千问已把小鱼抱到右侧石柱内侧，Kimi的护持已起效。',action='千问左臂托稳小鱼、右手低持合扇，低头说抱紧我；小鱼抓紧衣襟靠近，她随后抬眼望向GPT。',exit_state='小鱼已经抓稳，合扇仍握在千问右手；切GPT展翼升空。',dialogue='千问：抱紧我。',sound='0.2—1.3秒千问说“抱紧我”；衣料收紧与短促呼吸。句末留小鱼抓紧的反应，末尾引入下一镜拍翼低频；新声音尚未制作。',next_link='接CY024A：千问抬眼引出GPT展翼，拍翼气流延续；此句不再放在GPT画面上。',invariants=['左臂持续承托小鱼，右手合扇，为CY024A10开扇留起点；小鱼不落地。','水雷尚未释放，无洪水、雨水湿发或破顶；普通灯火仍在，祭火在画外。','千问是本句说话者，小鱼无新增台词；Kimi已在画外维持保护。'],asset_ids=['MULKZI2WM2FEL','CHAR-DEEPSEEK','ENV-CHURCH'],source_quote=quote,presentation=dict(path=dest,role='action',visible='千问低头对怀中小鱼说话，小鱼攥住衣襟，合扇留在手边。',status='v0.37新静帧候选，待作者审阅',missing='静帧已查看；口型、抓紧、抬眼和气流衔接待动态制作。',show_as_main=True),refs=[dict(path=dest,role='新增双人近景候选'),dict(path=req,role='冻结实际输入')],generation_request=req,visual_prompt=spec['prompt'],dialogue_cues=[],subtitle_cues=[dict(speaker='千问',text='抱紧我。',offset=0.2,duration=1.1)],page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0.,y=0.,w=1.,h=1.),editorial_review=dict(version='v037',status='candidate_pending_author_review',dynamic_execution='pending'),lighting='完整教堂内冷蓝窗光与现有普通烛光，尚未落水。',time_caption=a.pop('time_caption'),cinematic_beats=[dict(offset=0,intent='千问抱稳并低头'),dict(offset=.2,intent='千问说抱紧我'),dict(offset=1.3,intent='小鱼抓紧，千问抬眼接GPT')])
n.pop('claude_accessory_state',None)
a.update(source_quote=gpt,purpose='建立GPT飞行能力、高低距离与咏唱位置。',entry_state='千问与小鱼已在前镜抱稳，GPT站在中央通道。',action='GPT展开两片膜翼，下扇扬尘、双脚离地，避开吊灯升至穹顶下方；水珠在前中后景上浮，悬停后起咏。',dialogue='ChatGPT：盘踞于苍穹尽头，',sound='0—4.2秒展翼准备、翼膜低沉振动与气流，低弦起；4.2秒GPT起句。千问对白已移入前镜，不在此镜重复。正式声音未制作。',subtitle_cues=[c for c in a['subtitle_cues'] if c['speaker']=='ChatGPT'],cinematic_beats=[dict(offset=0,intent='展翼蓄势，气流起'),dict(offset=1.2,intent='向下振翼，双脚离地'),dict(offset=4.2,intent='悬停后GPT起句')])
a['presentation']['visible']=a['action'];a['editorial_review']=dict(version='v037',status='dialogue_reallocated_existing_image_retained',dynamic_execution='pending')
d['shots'].insert(d['shots'].index(a),n);by['CY026E']['next_link']='接CY024A0：召集回闪结束，切回此刻千问抱护小鱼。';by['CY026E']['exit_state']='五格回应结束，切回此刻千问与小鱼的双人近景。'
d['music_direction']['sequence'].insert(0,'CY024A0');d['music_direction']['estimated_spell_sequence_seconds']+=2
d['music_direction']['rule']='CY024A0千问“抱紧我”独立近景2秒→CY024A展翼低鼓和风声，4.2秒GPT起咏；其余跨镜长咒语与音乐节奏不变。'+d['music_direction']['rule'].split('；',1)[1]
d['continuity']['qwen_dialogue']='CY026E回闪结束→CY024A0千问低头说抱紧我、小鱼抓紧→CY024A GPT展翼升空并起咏。千问左臂承托、右手合扇，接后续开扇。'
d.update(version='v0.37',revision='v037',title='《穿云》带图分镜 v0.37 · 千问抱护近景',subtitle='抱紧我独立近景 · 展翼起咏衔接',story_script='剧本/穿云-场景剧本-v0.37.md',source_manifest='镜头设计/生成记录/生成索引-v037.json',review_intro='新增CY024A0两秒千问与小鱼双人近景，抱紧我的对白字幕移入该镜；CY024A保留展翼与GPT起咏，原图片不变。115镜381秒，新静帧待审，尚未制作新声音视频。',review_focus='说话者和对象同框；左臂抱稳、右手合扇；句后抓紧与抬眼引出GPT展翼。',revision_notes=dict(previous_manifest='镜头设计/shot-plan-v0.36.json',previous_html='镜头设计/带图分镜-v0.36.html',added_ids=['CY024A0'],modified_ids=['CY024A','CY026E'],boundary='新增2秒独立对话镜；原114镜图片、时长及已有声音文件不改。'))
elapsed=0
for s in d['shots']:s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
assert elapsed==381 and len(d['shots'])==115;d['total_seconds']=elapsed
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']];sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
lines=script.splitlines();lines[2]='版本：v0.37｜2026-10-23｜千问“抱紧我”新增独立双人近景，接GPT展翼升空与起咏。';script='\n'.join(lines)+'\n'
write(d['story_script'],script);save('镜头设计/shot-plan-v0.37.json',d)
save(d['source_manifest'],dict(version='v037',previous_index=o['source_manifest'],records=[dict(shot_id='CY024A0',original=str(source),destination=dest,sha256=sha(R/dest),request=req,request_sha256=sha(R/req),inputs=[dict(path=p,sha256=sha(p)) for p in spec['referenced_image_paths']],status='candidate_pending_author_review')],failed_request=rec+'/第一次请求结果.json'))
shutil.copy2(R/'镜头设计/带图分镜.html',R/'镜头设计/带图分镜-v0.36.html')
p='scripts/build_storyboard.py';s=read(p).replace('shot-plan-v0.36.json','shot-plan-v0.37.json').replace('"v036")','"v036", "v037")').replace("'v036')","'v036','v037')").replace('["CY026E","CY024A"]','["CY026E",*(["CY024A0"] if data.get("revision")=="v037" else []),"CY024A"]');write(p,s)
p='00_打开项目.html';write(p,read(p).replace('v0.36','v0.37').replace('114 镜','115 镜').replace('6 分 19 秒','6 分 21 秒'))
p='制作进度.md';s=read(p);pos=s.index('## 2026-10-23：');s=s[:pos]+'## 2026-10-23：千问“抱紧我”独立近景（v0.37）\n\n作者确认新增该画面。新增CY024A0双人近景2秒，千问低头说话、小鱼抓紧衣襟，右手合扇准备后续开扇；接CY024A展翼升空。原CY024A中的千问对白字幕移入新镜，GPT起咏仍在原镜4.2秒，不重复对白。同步[剧本v0.37](剧本/穿云-场景剧本-v0.37.md)与[带图分镜](镜头设计/带图分镜.html)。115镜381秒（6分21秒）。\n\n内置imagegen首请求被输入安全检查拦截且无输出，简化为普通保护对话描述后生成一张候选；完整请求与结果记录保留。旧图和声音未改，未生成新配音或视频。\n\n'+s[pos:];write(p,s)
print('v0.37:115shots381seconds;Qwen cue moved to CY024A0')
