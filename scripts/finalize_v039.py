"""Archive final static/dialogue review; no image, dialogue or timing edits."""
import copy,json,hashlib,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,s):(R/p).write_text(s,encoding='utf-8')
def save(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
assert not (R/'镜头设计/shot-plan-v0.39.json').exists()
old=json.loads(read('镜头设计/shot-plan-v0.38.json'));d=copy.deepcopy(old);by={s['id']:s for s in d['shots']};script=read(old['story_script'])
replacements={
 '中殿圣灯左右等高对称悬挂一对':'中殿高处悬挂一盏通透环形烛式吊灯',
 '三对火盆、对称圣灯与两支蜡烛仍然燃着':'三对火盆、中央环形烛式吊灯、两只后墙壁烛与两支石座蜡烛仍然燃着',
 'Kimi在右侧柱边站定，准备施法':'Kimi在右侧柱边站定，持续维持已抵达Claude的贴身月辉',
 '施法水纹将靠近的侧浪与雷支流向外引开':'施法水纹已蓄好，准备在落水后将靠近的侧浪与雷支流向外引开',
 'v0.23三张候选以CY012-v023-r8为局部空间参考，其他旧镜图片尚未完成新家具与灯具同步。':'后墙家具与中央单吊灯以CY012-v023-r8为局部空间参考；历史双吊灯说明不再作为制作指令。'
}
def replace_text(s):
 for a,b in replacements.items():s=s.replace(a,b)
 return s
script=replace_text(script)
for s in d['shots']:
 for k in ['source_quote','action','entry_state','exit_state','next_link']:
  if k in s:s[k]=replace_text(s[k])
 s['invariants']=[replace_text(x) for x in s['invariants']]
for id,line in [('CY024A2','循吾之声，自漫长的沉眠中苏醒。'),('CY024A4','令灼烧无辜的烈焰，在奔流中止息；')]:
 s=by[id];quote=s['source_quote'];new=quote+'\n\n**ChatGPT（画外）：**\n'+line
 assert script.count(quote)==1 and line not in script
 script=script.replace(quote,new,1);s['source_quote']=new
by['CY022B1']['invariants']=[x for x in by['CY022B1']['invariants'] if x!='空镜不安排人物；援军在下一镜揭示，非人物消失。']+['两列骑士先越前列队守门，随后接GPT腰腿局部入场；这不是无人空镜。']
by['CY029E']['exit_state']='呼唤尾音散去，Claude转向空刑架；接CY029E1续咒，初蓄微光持续，尚未释放火种。'
d['continuity']['end_match']='CY031空座→CY031A从右靠近、落座、邀请与回答好→CY032A交勺→CY033旁景→CY034A唯一第一口饭→CY034空勺降低、两人回望。只一只碗、一把勺，末镜最后四秒静留。'
d['continuity']['audio']='当前引用19段既有临时读稿；新增及改写台词以当前字幕为准，缺失正式配音未冒用旧句。文件与镜内时长已核对，未实听；完整角色配音、实际试读和配乐粗剪仍待声音阶段。'
d['continuity']['remaining_image_sync']='v0.23局部同步备注为历史记录；当前按v0.38的115个主图路径逐一冻结。旧双悬灯、旧低台及历史母版不覆盖当前画面；本轮不重画。最终静帧审查与未消除的手侧差异见收尾审查记录。'
d['continuity']['qwen_hand_review']='CY024A0现图呈人物自身右臂托抱、左手持扇，与既定文字左托右扇相反。作者认可静帧保留；视频执行必须统一左臂承托、右手持扇，禁止在A0→A10间无交代换抱。此差异未通过连续动作验收。'
by['CY024A0']['presentation']['missing']='已实际核对：本图抱人、持扇手侧与左托右扇文字相反；静帧保留，视频须统一为左臂承托、右手持扇，不在镜间换抱。口型、抓紧、抬眼尚待动态验证。'
by['CY024A0']['final_review_exception']='hand_side_mismatch_open_for_video'
md=d['music_direction'];md['estimated_spell_sequence_seconds']=sum(by[i]['seconds'] for i in md['sequence']);md['pre_release_sequence_seconds']=53
assert md['estimated_spell_sequence_seconds']==61 and md['estimated_gpt_incantation_seconds']==46.8
for m in d['masters']:
 if m['id'] in ['M-ALTAR-v014','M-ALTAR-POST-v014']:
  m['status']='历史参考，不作为当前灯具母版';m['limits']='只用于历史空间/战损关系对照；双灯等旧设定已被中央单吊灯取代。当前执行以v0.23局部空间与逐镜采用图为准。'
 if m['id']=='M-ALTAR-v023':
  m['status']='作者确认局部空间设计';m['role']=replace_text(m['role']);m['limits']='当前后墙长椅、壁烛和中央单吊灯参考；不覆盖人物动作及战后状态。'
for s in d['shots']:
 s['presentation']['status']='2026-10-23作者确认当前静帧；收尾审查已记录，动态与声音未验收'
 s['final_static_review']=dict(author_confirmation='好，那么现在我们的画面就应该是没有问题了，你再审一下最终的画面还有台词，保存记录，然后这个对话的使命就结束了',scope='current_static_image_and_approved_dialogue',review='115-shot contact review; selected original images inspected',exception=s.get('final_review_exception'),dynamic_and_audio='not_approved_by_this_review')
d.update(version='v0.39',revision='v039',title='《穿云》带图分镜 v0.39 · 收尾审定',subtitle='115镜 · 6分21秒 · 画面沿用v0.38',story_script='剧本/穿云-场景剧本-v0.39.md',source_manifest='镜头设计/生成记录/生成索引-v039.json',review_intro='作者确认画面后的最终审查版：主图、对白与时长完全沿用v0.38；补齐剧本漏同步的两句原咒语，清理旧说明。千问手侧差异已明确留作视频连续性必修项。',review_focus='静帧与台词创作阶段收尾；不再新增画面和对白。以最终审查记录交接视频与声音制作。',revision_notes=dict(previous_manifest='镜头设计/shot-plan-v0.38.json',previous_html='镜头设计/带图分镜-v0.38.html',image_edits=[],dialogue_edits=[],duration_edits=[],boundary='仅文档漏同步、旧元数据和最终审查状态；图片、台词、字幕时点、音频引用均未变。'))
script=script.replace('其他角色参考 Eagle 收藏，具体采用造型待定。','其他角色沿用当前项目资产与已确认静帧造型，历史Eagle来源仅用于追溯。').replace('以下动作与对白为本版创作候选。','以下为本次收尾审定的动作与对白；静帧认可不等同动态和声音验收。')
lines=script.splitlines();lines[2]='版本：v0.39｜2026-10-23｜收尾审查；画面沿用v0.38，补回两句已定咒语，清理旧说明。';script='\n'.join(lines)+'\n'
script=script.replace('## 制作交接备注','## 历史制作交接备注（按版本留存；当前正文及收尾记录优先）',1)
write(d['story_script'],script);save('镜头设计/shot-plan-v0.39.json',d)
save(d['source_manifest'],dict(version='v039',previous_index=old['source_manifest'],generated_images=0,image_source='All 115 main image references unchanged from v0.38',review_record='镜头设计/生成记录/最终审查-v038/收尾审查记录.md'))
shutil.copy2(R/'镜头设计/带图分镜.html',R/'镜头设计/带图分镜-v0.38.html')
p='scripts/build_storyboard.py';s=read(p).replace('shot-plan-v0.38.json','shot-plan-v0.39.json').replace('"v038")','"v038", "v039")').replace("'v038')","'v038','v039')");write(p,s)
p='00_打开项目.html';s=read(p).replace('v0.38','v0.39');s=s.replace('</body>','<p style="text-align:center"><a href="镜头设计/生成记录/最终审查-v038/收尾审查记录.md">最终画面与台词审查记录（本次对话收尾）</a></p></body>');write(p,s)
p='制作进度.md';s=read(p);pos=s.index('## 2026-10-23：');s=s[:pos]+'## 2026-10-23：画面与台词收尾审定（v0.39）\n\n作者确认当前画面，并要求最终审查、保存记录、结束本次对话。完成115镜静帧拼图审看、重点原图复核及全剧本/台词审查；修复剧本漏写两句既定咒语、旧双吊灯/骑士空镜/Kimi起护描述及接镜、时长统计残留。图片、台词文本、字幕时点和镜头时长全部保留，115镜381秒。\n\n当前入口：[带图分镜](镜头设计/带图分镜.html)、[剧本v0.39](剧本/穿云-场景剧本-v0.39.md)、[收尾审查记录](镜头设计/生成记录/最终审查-v038/收尾审查记录.md)。所有旧版本与生成输入保留。千问CY024A0现图手侧与左托右扇执行约定相反，已明确留档，视频必须统一；未把它标为连续性通过。\n\n本对话的静帧与台词创作阶段结束。不自动启动后续任务、生成、配音或视频。后续由作者另行发起时读取收尾记录；声音实听与动态连续性均未在本次验收。\n\n'+s[pos:];write(p,s)
print('v039 final editorial snapshot created; no picture/dialogue/timing changes')
