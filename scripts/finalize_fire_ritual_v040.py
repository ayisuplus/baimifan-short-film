"""Finalize continuity wording after independent v040 review."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text('utf-8-sig'))
def save(p,d):(R/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p='镜头设计/shot-plan-v0.40.json';d=load(p);by={s['id']:s for s in d['shots']}
fire='CY022引燃高柴后，黑芯暗紫边火焰向中央连成火海，破柴前远景遮蔽Claude，近景从火隙见她和焦损衣边。CY024命令后，Kimi在CY024K1裂开高柴、CY024K2向两侧推散并形成贴身月辉；此后允许中央让空，残柴与黑焰仍在两侧和低处。水雷随后扑灭全部祭薪。最后星火点燃空木架为橙金色，脚边乌烬木不复燃。'
d['continuity']['ritual_fire']=fire
script=(R/d['story_script']).read_text('utf-8')
start=script.index('乌烬木引燃后，');end=script.index('\n\n',start)
script=script[:start]+fire+script[end:]
(R/d['story_script']).write_text(script,encoding='utf-8')
for s in d['shots']:
 s['invariants']=[fire if x.startswith('乌烬木引燃后，') else x for x in s['invariants']]
 if s['id'] in ['CY016D','CY017','CY017A','CY018','CY018B']:
  s['invariants']=[x for x in s['invariants'] if x not in ['Claude 仍被固定；冲突主要借她的反应与画外声音表现。','教主祷词移到被发现后；此前空堂里没有教主或吟唱。']]
 if s['id']=='CY021A':
  s['invariants']=[x.replace('此时柴薪仍未点，Claude仍受束，小鱼不能站起。','此时高柴未点燃，Claude仍受束；小鱼听见教主接火后会再次站起挡路。') for x in s['invariants']]
 if s['id'] in ['CY024K1','CY024K2']:
  s['invariants']=[x for x in s['invariants'] if x!='施法声始终为ChatGPT，教主反应不新增对白。']
  s['invariants'].insert(0,'Kimi暗月破柴与月辉护身连续完成；本镜无咏唱对白，GPT长咏唱尚未开始。')
by['CY016D']['framing']='长阶下端侧面中景，双手抓住搬柴教徒的同一根木头'
by['CY017']['framing']='阶下低机位近中景，撑地伸手与抱木离开者'
by['CY018']['framing']='阶下侧面近中景，拦腿失败与抱木教徒同框'
# The old accepted image on the moved shot remains accepted as an image only.
by['CY021A']['final_static_review']['scope']='reused_image_only; revised timing/dialogue and narrative are v040 pending author review'
save(p,d)
a=load(d['audio_arrangement']);a['shot_plan_sha256']=hashlib.sha256((R/p).read_bytes()).hexdigest();save(d['audio_arrangement'],a)
print('Independent review wording corrections applied.')

