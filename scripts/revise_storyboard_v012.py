"""Apply the post-Tianpu candle-extinction revision, preserving v0.11."""
import json, shutil, hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def read(p): return json.loads((root/p).read_text(encoding='utf-8'))
def write(p,d): (root/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
archive=root/'镜头设计/带图分镜-v0.11.html'
if not archive.exists(): shutil.copy2(root/'镜头设计/带图分镜.html',archive)
d=read('镜头设计/shot-plan-v0.11.json')
script=(root/'剧本/穿云-场景剧本-v0.11.md').read_text(encoding='utf-8')
changes=[
 ('版本：v0.11','版本：v0.12'),
 ('洪水扑灭十字架下的低柴和两只火盆，把黑袍教徒与散乱长椅冲向两侧。','洪水扑灭十字架下的低柴、两只火盆及殿内全部蜡烛与火把，把黑袍教徒与散乱长椅冲向两侧。'),
 ('湿黑柴堆和火盆冒着水汽。','湿黑柴堆和火盆冒着水汽。所有烛芯湿黑，烛焰及暖色倒影消失；破碎中殿穹顶与彩窗透入银蓝月光，照亮人物和湿地。后殿仍由彩窗透光，不增加新的破顶。'),
 ('一小簇橙金火光亮起。','一小簇橙金火光亮起，成为月光环境里新的局部暖光；周围蜡烛仍然熄灭。'),
 ('火没有蔓延到教堂。','火没有蔓延到教堂，蜡烛和火盆也没有复燃。随后接抱及离殿时，冷月光与空刑架的局部暖光共同照明。')
]
for a,b in changes:
 assert a in script,a
 script=script.replace(a,b)
script+='\n- v0.12：天瀑后殿内所有蜡烛、火把、双火盆和低柴熄灭；月光经中殿破顶、彩窗与门口照明。护罩、变身、雷光及战斗爆闪按来源保留；Claude指尖恢复力量后才出现自身暖光，再点燃空刑架，烛火始终不复燃。旧备注不覆盖本条。\n'
(root/'剧本/穿云-场景剧本-v0.12.md').write_text(script,encoding='utf-8')
rule='CY024B天瀑后殿内全部蜡烛、火把、双火盆与低柴熄灭，烛芯不发光；月光经中殿破顶、彩窗及门口照明，后殿穹顶保持完整。护罩/变身/雷电/战斗闪光仅按现场来源局部照明。CY028B起允许Claude火魔法暖光，CY029B起允许空刑架火光；烛台与火盆直到离殿都不复燃。'
d.update(title='《穿云》带图分镜 v0.12',version='v0.12',revision='v012',created='2026-10-22',story_script='剧本/穿云-场景剧本-v0.12.md',origin_manifest='镜头设计/shot-plan-v0.11.json',subtitle='天瀑灭烛、月光接续与Claude火光回归')
d['continuity']['lighting']=rule
d['continuity']['church']=d['continuity']['church'].replace('天瀑后两盆与柴火全部熄灭。','天瀑后两盆、柴火以及殿内全部蜡烛和火把熄灭。')
d['continuity']['magic']+=' '+rule
d['review_intro']='天瀑之后殿内烛火全部熄灭，湿地与人物改由银蓝月光照明。眼中倒影和教堂窗内暖光同步修正；护罩、战斗魔法与Claude后来重新燃起的火光保留。'
d['review_focus']='从CY024B连续查看到CY030：烛芯不再亮起，解锁段保持月光，CY028B指尖暖光回归，CY029B只点燃空刑架。'
d['roughcut_preview_label']='旧版静帧配乐 v002（69镜239秒，未包含v0.12改图；Victory决定保留）'
records=read('镜头设计/生成记录/熄烛月光-v012/结果映射.json')
selected={r['id']:r for r in records}
active=False
for s in d['shots']:
 for key in ['action','entry_state','exit_state','source_quote','visual_prompt','sound']:
  if key in s:
   for a,b in changes:s[key]=s[key].replace(a,b)
 if s['id']=='CY024B':active=True
 if active:
  s['invariants'].append(rule)
  s['lighting']=rule
 if s['id']=='CY030':active=False
 if s['id'] not in selected:continue
 r=selected[s['id']];old=s['presentation']['path'];job=read(r['request'])
 s['presentation']={'path':r['destination'],'role':'action','visible':s['action'],'status':'v0.12熄烛月光候选，待作者审阅','missing':'连续动态与正式声音待制作；本轮只修静帧光源。','show_as_main':True}
 s['visual_prompt']=job['input']['prompt'];s['generation_request']=r['request']
 s['refs']=[{'path':r['destination'],'role':'本轮独立改图候选'},{'path':r['request'],'role':'冻结的实际提示词与输入'},{'path':old,'role':'保留的上一版'}]
 s['editorial_review']={'version':'v012','status':'candidate_static_review','dynamic_execution':'pending'}
 s['panel_index']=0;s.pop('display_crop_normalized',None)
for i,s in enumerate(d['shots']):
 s['presentation']['visible']=s['action']
 s['next_link']='接 '+d['shots'][i+1]['id']+'：'+s['exit_state']+' → '+d['shots'][i+1]['entry_state'] if i+1<len(d['shots']) else '结束。'
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.11.json',previous_html='镜头设计/带图分镜-v0.11.html',added_ids=[],repurposed_ids=[],boundary='22镜独立照明修订；89镜286秒不变。旧配乐粗剪未重导。全部原件与冻结输入保留。')
d['page_layouts']=[{'path':s['presentation']['path'],'rows':1,'cols':1} for s in d['shots']]
for sc in d['scenes']:
 group=[s for s in d['shots'] if s['scene']==sc['id']]
 sc['pages']=list(dict.fromkeys(s['presentation']['path'] for s in group));sc['path']=sc['pages'][0]
assert all(s['source_quote'] in script for s in d['shots'])
assert len(d['shots'])==89 and sum(s['seconds'] for s in d['shots'])==286
write('镜头设计/shot-plan-v0.12.json',d)
for r in records:
 p=root/r['destination'];r['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
 assert r['sha256']==hashlib.sha256(Path(r['original']).read_bytes()).hexdigest()
 r['status']='candidate' if r['take']==selected[r['id']]['take'] else 'superseded-preserved'
write('镜头设计/生成记录/熄烛月光-v012/归档校验.json',records)
print('v0.12: 89 shots, 286 seconds, 22 lighting edits; quotes and original hashes passed')

