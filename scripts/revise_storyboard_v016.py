"""Add the calm-before-storm cutaway and restore GLM's tail, preserving v015."""
import copy,json,shutil,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def read(p):return json.loads((root/p).read_text(encoding='utf8'))
def write(p,v):(root/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
records=read('镜头设计/生成记录/收工补镜-v016/结果映射.json')
audit=[]
for r in records:
 p=root/r['destination'];p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():shutil.copy2(r['original'],p)
 h=hashlib.sha256(p.read_bytes()).hexdigest()
 assert h==hashlib.sha256(Path(r['original']).read_bytes()).hexdigest()
 audit.append(dict(id=r['id'],path=r['destination'],sha256=h,original=r['original']))
write('镜头设计/生成记录/收工补镜-v016/归档校验.json',audit)
selected={r['id']:r for r in records}
d=read('镜头设计/shot-plan-v0.15.json');by={s['id']:s for s in d['shots']}
script=(root/d['story_script']).read_text(encoding='utf8')
quote='教堂外，乌云掠过明月，冷光忽明忽暗。风把蓝金旗帜猛然拉紧，枯叶卷过石阶；远方传来一声闷雷。大门仍闭，穹顶完整，雨还没有落下。'
script=script.replace('版本：v0.15','版本：v0.16',1).replace(by['CY026']['source_quote'],quote+'\n\n'+by['CY026']['source_quote'],1)
script+='\n- v0.16：CY026集结前新增3秒CY022B1风起空镜，云遮月、旗动、枯叶、远雷；不提前下雨或破坏屋顶。CY027D仅补回GLM黑色白尖的大尾巴，既有分层站位及修长比例保留。\n'
(root/'剧本/穿云-场景剧本-v0.16.md').write_text(script,encoding='utf8')
s=copy.deepcopy(by['CY026'])
s.update(id='CY022B1',title='风暴将至',seconds=3,framing='教堂外侧低机位远景／环境空镜',
purpose='从Claude眼底的火切到殿外风起，短暂蓄势后揭示援军集结。',
entry_state='教堂内低柴已燃；教堂外同一夜晚，门闭、建筑完好，尚未下雨。',
action='乌云掠过月亮，旗帜被风拉紧，枯叶卷离石阶；教堂静立，人物留在画外。',
exit_state='风声与远雷余音延续，切近门前集结队伍。',
sound='殿内吟唱跨切后渐低；风声、旗布猎猎、枯叶摩擦，一声远处闷雷；末尾接骑士脚步与甲片声。声音为设计提示，待制作。',
source_quote=quote,asset_ids=['ENV-CHURCH'],invariants=['同一座黑金教堂与蓝金旗帜；门闭、穹顶完整，无战损。','仅风起云动，未降雨；没有天瀑、水龙、洪水或战斗闪电。','空镜不安排人物；援军在下一镜揭示，非人物消失。'],dialogue='无对白',dialogue_cues=[])
s.pop('subtitle_cues',None)
d['shots'].insert(d['shots'].index(by['CY026']),s)
by['CY022B']['exit_state']='Claude仍望着小鱼；切殿外风起的环境空镜。'
by['CY022B']['sound']='火焰细响和压低吟唱；吟唱跨切入外景，逐渐被风声盖过。'
by['CY026']['entry_state']='风起、云层遮月，尚未下雨；援军已来到紧闭教堂门外。'
by['CY026']['sound']='承接风声与闷雷余音，脚步、长枪与甲片轻响进入；声音为制作提示，尚未制作音轨。'
by['CY027D']['invariants'].append('GLM保留一条蓬松黑色大尾巴、末端大片白毛；从身后腰臀伸出，在画面右侧空隙显露，不遮脸和宝宝。')
for s in d['shots']:
 if s['id'] in selected:
  r=selected[s['id']];previous=s['presentation']['path']
  s.update(visual_prompt=r['input']['prompt'],generation_request=r['request'],panel_index=0,editorial_review={'version':'v016','status':'candidate_static_review','dynamic_execution':'pending'})
  s['presentation']={'path':r['destination'],'role':'action','visible':s['action'],'status':'v0.16收尾候选，待作者审阅','missing':'连续风云、旗帜与尾巴运动及正式声音待视频制作。','show_as_main':True}
  s['refs']=[{'path':r['destination'],'role':'本轮独立原画'},{'path':r['request'],'role':'冻结实际输入'},{'path':previous,'role':'上一版或相邻镜头参考'}]
  s.pop('display_crop_normalized',None)
elapsed=0
for i,s in enumerate(d['shots']):
 s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
 s['next_link']='接 '+d['shots'][i+1]['id']+'：'+s['exit_state']+' → '+d['shots'][i+1]['entry_state'] if i+1<len(d['shots']) else '结束。'
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']]
 sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)))
 sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
d.update(title='《穿云》带图分镜 v0.16',version='v0.16',revision='v016',story_script='剧本/穿云-场景剧本-v0.16.md',origin_manifest='镜头设计/shot-plan-v0.15.json',total_seconds=elapsed,subtitle='风起空镜与GLM尾巴收尾',
review_intro='集结前补入风起、云遮月的教堂环境空镜；GLM补回黑色白尖大尾巴。现有角色、分层站位及多级祭坛不变。',
review_focus='连看CY022B—CY022B1—CY026蓄势与集结，再看CY027D尾巴与人物遮挡。',roughcut_preview_label='旧版静帧配乐v002（69镜239秒，未包含v0.16改图；Victory决定保留）')
d['continuity']['weather_before_arrival']='CY022B1风起、云遮月，尚未下雨；CY026同一夜晚、完整教堂门前集结。天瀑和后续雨战维持原顺序。'
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.15.json',previous_html='镜头设计/带图分镜-v0.15.html',added_ids=['CY022B1'],repurposed_ids=[],boundary='新增3秒空镜，仅修改CY027D尾巴，91镜292秒；旧90镜时长与顺序保留，89镜图片不变；旧配乐粗剪未重导。')
assert len(d['shots'])==91 and elapsed==292
assert all(s['source_quote'] in script for s in d['shots'])
p=root/'镜头设计/带图分镜-v0.15.html'
if not p.exists():shutil.copy2(root/'镜头设计/带图分镜.html',p)
write('镜头设计/shot-plan-v0.16.json',d)
print('v016: 91 shots, 292 seconds')
