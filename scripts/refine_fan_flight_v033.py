"""Separate isolated leaf flight from the impact beat, per final author steering."""
import json,copy,shutil,hashlib
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];REC='镜头设计/生成记录/展翼与扇面-v033';IMG='镜头设计/图像/展翼与扇叶-v033'
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,t):(R/p).write_text(t,encoding='utf-8')
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p='镜头设计/shot-plan-v0.33.json';d=json.loads(read(p));by={s['id']:s for s in d['shots']};assert 'CY024A12' not in by
s=by['CY024A11'];old=s['source_quote']
fly='''切单枚扇叶独立飞行的极特写。摄影机在刃尖侧前方朝后拍，近处尖端和薄刃清晰，叶身朝后延伸，细金边随缓慢轴向翻转掠过一道反光，远处教堂只剩虚化的色块。镜头只跟这一枚细长实体扇叶，不放入敌人术光、人脸、目标或碰撞火花。短暂子弹时间只用于欣赏刃形、花纹和飞行姿态，咏唱保持自然速度。'''
hit='''随后切单独的短促撞击镜头，扇叶斜切进入教主术光与空中ChatGPT之间的拦截点。暗金术光保持从教主朝GPT的世界方向，不能让攻击倒飞。刃缘接触时恢复正常速度，一声清脆裂响，术光被劈散成两股，偏向无人空处并消失；扇叶随之斜落空侧廊。千问在画外把余扇合拢收回胸侧，左臂始终未松开小鱼。

教主收回被震偏的手，发现两侧骑士已经封住接近路线。掩护仍在画外持续，Kimi继续施法；教主转向判断头顶雷声，逐步改为自保，而不是原地等待。'''
t=read(d['story_script']);assert old in t;t=t.replace(old,fly+'\n\n'+hit,1);write(d['story_script'],t)
s.update(title='单枚扇叶，侧前方极特写',framing='刃尖侧前方朝后拍／仅单枚扇叶／极近浅景深伴飞',purpose='单独欣赏暗器的刃形、花纹和飞行姿态，飞行画面不混入敌方招式。',action='只跟单枚扇叶飞行；刃尖近、叶身向后延伸，微旋时金边反光，背景高度虚化。',exit_state='扇叶即将抵达画外拦截点，切独立撞击。',source_quote=fly,sound='环境声短暂压低，只有细薄破空声；GPT画外咏唱自然连续，不变调。碰撞声留下一镜。')
impact=copy.deepcopy(s);impact.update(id='CY024A12',title='截断术光，恢复常速',seconds=1,framing='单独撞击近景／小接触亮点与术光分流',purpose='交代阻击结果，作为孤立飞行特写后的短促收尾。',entry_state='扇叶飞行特写结束，抵达教主至GPT的术光路径。',action='单叶击中暗金术光，短促亮点后两股残光偏离无人空处，叶片开始斜落；恢复正常速度。',exit_state='阻击成功；教主转防御，千问继续画外护人，接Kimi起护。',source_quote=hit,sound='画面恢复常速时一声短促清脆撞击，残光迅速散去；GPT咏唱连续，随后接Kimi微光声。',subtitle_cues=[dict(speaker='ChatGPT',text='统御深流与雷鸣的',offset=0,duration=1)])
by['CY024A12']=impact;i=d['shots'].index(s)+1;d['shots'].insert(i,impact)
out={'CY024A11':(3,'exec-1d64b8a6-769f-498d-bd00-e7c79f466d0b.png'),'CY024A12':(1,'exec-ec41be73-5d27-4120-96c0-15f8d64073f6.png')}
idxp='镜头设计/生成记录/生成索引-v033.json';idx=json.loads(read(idxp));rows=json.loads(read(REC+'/输出映射.json'))
for r in idx['records']:
 if r['shot_id']=='CY024A11' and r['attempt']==2:r['status']='rejected_author_requests_isolated_flight'
for r in rows:
 if r['id']=='CY024A11' and r['attempt']==2:r['status']='rejected_author_requests_isolated_flight'
for sid,(n,fn) in out.items():
 source=Path('C:/Users/36322/.codex/generated_images/01a162c1-6e38-7a10-aee7-5c8371c4830c')/fn;dest=f'{IMG}/{sid}-v033-r{n}.png';req=f'{REC}/{sid}-请求-v{n:03}.json';shutil.copy2(source,R/dest);args=json.loads(read(req));w,h=Image.open(R/dest).size
 q=by[sid];q.update(presentation=dict(path=dest,role='action',visible='单枚狭长实体扇叶在虚化背景前独立飞行，刃尖侧前方视角，无敌方术光。' if sid=='CY024A11' else '单叶刃缘接触术光的短促亮点；只表达接触瞬间。',status='v0.33新静帧候选，待作者审阅',missing='飞行、旋转、速度变化、撞击分流及声音尚未制作。',show_as_main=True),page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0.,y=0.,w=1.,h=1.),generation_request=req,visual_prompt=args['prompt'],refs=[dict(path=dest,role='本轮新候选'),dict(path=req,role='冻结实际输入')])
 idx['records'].append(dict(shot_id=sid,attempt=n,original=str(source),destination=dest,sha256=sha(R/dest),request=req,request_sha256=sha(R/req),inputs=[dict(path=x,sha256=sha(x)) for x in args['referenced_image_paths']],status='candidate_pending_author_review'))
 rows.append(dict(id=sid,attempt=n,original=str(source),status='candidate_pending_author_review'))
s['next_link']='接CY024A12：孤立飞行特写结束，单独交代撞击。';impact['next_link']='接CY024A1：术光被截断，GPT咏唱持续，Kimi起护。'
d['music_direction']['sequence'].insert(d['music_direction']['sequence'].index('CY024A11')+1,'CY024A12')
d['music_direction'].update(estimated_spell_sequence_seconds=51,estimated_gpt_incantation_seconds=46.8)
d['music_direction']['incantation_bridge']=dict(ids=['CY024A9','CY024A10','CY024A11','CY024A12','CY024A1'],text='统御深流与雷鸣的古老意志啊。',seconds=9,rule='前半句6秒跨教主1秒/开扇2秒/孤立飞行2秒/撞击1秒，后半句3秒在Kimi镜收尾，只念一次。')
d['continuity']['bullet_time']='CY024A11仅单枚实体扇叶独立飞行，刃尖侧前方向后拍；不得含敌方术光或碰撞。CY024A12独立1秒撞击、恢复常速。术光世界方向教主→空中GPT不变；咏唱自然连续，不因慢镜变调。'
d['review_intro']+=' 作者最后将飞行与撞击拆开：开扇2秒→仅暗器的侧前方极特写2秒→撞击1秒。'
d['revision_notes']['added_ids'].append('CY024A12');d['revision_notes']['modified_ids'].append('CY024A12');d['revision_notes']['boundary']=d['revision_notes']['boundary'].replace('17张','18张').replace('6张中间稿','7张中间稿')+' 最后将A11纯飞行与A12撞击分开，全片增加1秒至359秒。'
elapsed=0
for q in d['shots']:q['start_second']=elapsed;elapsed+=q['seconds'];q['end_second']=elapsed
d['total_seconds']=elapsed;assert len(d['shots'])==109 and elapsed==359
for sc in d['scenes']:
 ss=[q for q in d['shots'] if q['scene']==sc['id']];sc.update(shot_ids=[q['id'] for q in ss],seconds=sum(q['seconds'] for q in ss),pages=list(dict.fromkeys(q['presentation']['path'] for q in ss)));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=q['presentation']['path'],rows=1,cols=1) for q in d['shots']]
save(p,d);save(idxp,idx);save(REC+'/输出映射.json',rows)
p='制作进度.md';x=read(p).replace('CY024A11单叶子弹时间截击，共5秒','CY024A11仅单叶的侧前方子弹时间极特写、CY024A12独立撞击，共6秒').replace('当前17张新候选，6张中间稿','当前18张新候选，7张中间稿').replace('108镜358秒（5分58秒）','109镜359秒（5分59秒）').replace('升空和咏唱50秒','升空和咏唱51秒').replace('咏唱预算约45.8秒','咏唱预算约46.8秒');write(p,x)
p='00_打开项目.html';write(p,read(p).replace('108 镜','109 镜').replace('5 分 58 秒','5 分 59 秒').replace('护人、升空及咏唱50秒','护人、升空及咏唱51秒').replace('单片实体扇叶 · 子弹时间','单片扇叶独立飞行极特写 · 单独撞击'))
print('109 shots359seconds;18 current frames25 attempts;isolated flight then separate impact.')
