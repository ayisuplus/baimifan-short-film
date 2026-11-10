"""Publish reviewed descriptions without changing approved dialogue or source images."""
import copy, hashlib, json, shutil
from pathlib import Path

root=Path(__file__).resolve().parents[1]
out=root/'后期/终极审查-v001'
def read(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def save(p,v):(root/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
base=read('镜头设计/shot-plan-v0.48-bgm-v006.json');plan=copy.deepcopy(base)
script=(root/base['story_script']).read_text(encoding='utf-8-sig')
script=script.replace('版本：v0.48｜2026-10-24｜敌方反应、完整月影渡咏唱及局部眼肤色修正。','版本：v0.48r1｜2026-10-25｜终极审查说明同步；对白与画面保持。')
shots={s['id']:s for s in plan['shots']}
edits=[]
def transform(sid,field,fn):
    s=shots[sid];before=copy.deepcopy(s[field]);after=fn(before)
    if after!=before:s[field]=after;edits.append(dict(shot=sid,field=field,before=before,after=after))
def replace(sid,field,a,b):transform(sid,field,lambda v:v.replace(a,b))
single='只设一根宽于暗金护罩的连续水柱；罩顶接触前不分成两柱，接触后才环状炸开并向侧面分流。水向下、紫电沿柱内涡旋盘绕向上，二者同处一水体。'
three='水雷由同一云层降下一主两辅三股独立水柱：主柱打教主暗金罩，两辅柱打两翼教徒；不从手指喷水，不在途中分叉。三处落点主动避开Kimi暗月罩及中央祭坛安全区。CY024B末先收雷再停水；CY024B3只有落点余水沿两侧下行，CY024B3A罩内安抚，不以身体撑罩抗水。'
for sid in ['CY024B','CY024B3','CY024B3A']:
    transform(sid,'invariants',lambda v:[x.replace(single,three) for x in v])
old='中殿与后殿屋顶直到CY024B前都完整；最终只破中殿，保留后殿和正门。'
new='中殿与后殿屋顶在CY024A5首点落柱前保持完整；首柱于A5末贯穿中央中殿穹顶，A5A开始时首处破口已经形成。后续辅柱也只破中殿，保留后殿、正门和祭坛安全区。'
for sid in ['CY024A3','CY024A6','CY024A7']:transform(sid,'invariants',lambda v:[x.replace(old,new) for x in v])
replace('CY024A5','action','中央主水柱应声从云层落下；','中央主水柱应声从云层落下，贯穿中央中殿穹顶；')
replace('CY024A5A','entry_state','第一股主柱已压住教主','中殿首处落水破口已经形成，第一股主柱已压住教主')
q='她目光沿指向锁定下方教主，第一股主水柱应声落向暗金罩。'
r='她目光沿指向锁定下方教主，第一股主水柱应声贯穿中央中殿穹顶，落向暗金罩。'
assert q in script;script=script.replace(q,r)
for s in plan['shots']:replace(s['id'],'source_quote',q,r)
transform('CY024B1','invariants',lambda v:[x.replace('木椅是主主体，教徒失衡是次要反应；','教徒阵形被余浪冲散是主主体，长椅留在原位作尺度与位置参照；') for x in v])
old='Kimi 听到呼名，先睁眼，再撑着月石坐起；视野放宽，才看见俯身等她的 ChatGPT。'
new='Kimi已经睁眼并坐起；视野放宽，看见俯身等她的ChatGPT，直接承接分路交代。'
assert old in script;script=script.replace(old,new)
for field in ['action','source_quote']:replace('CY026D',field,old,new)
replace('CY026D','sound','月背微风','月面安静，无风声')
replace('CY026D','visual_prompt','Kimi坐起并答应同行','Kimi已经坐起并确认从Claude背后彩窗分路突入')
script=script.replace('脚凳','固定脚托')
for s in plan['shots']:
    for f in ['action','entry_state','exit_state','next_link','source_quote','visual_prompt']:
        replace(s['id'],f,'脚凳','固定脚托')
    transform(s['id'],'presentation',lambda v:{**v,**{k:v[k].replace('脚凳','固定脚托') for k in ['visible','missing']}})
transform('CY020A','entry_state',lambda _: '承接CY020B同一次推搡：小鱼已经失去平衡，身体向后跌落；Claude的呼喊不重放。')
transform('CY020B','next_link',lambda _: '接CY020A：'+shots['CY020A']['entry_state'])
transform('CY024A5','presentation',lambda v:{**v,'visible':v['visible'].replace('中央主水柱应声从云层落下；','中央主水柱应声从云层落下，贯穿中央中殿穹顶；')})
transform('CY024A5','next_link',lambda _: '接CY024A5A：'+shots['CY024A5A']['entry_state'])
replace('CY009A','action','修正近端王座透视与支撑；','')
transform('CY009A','presentation',lambda v:{**v,'visible':v['visible'].replace('修正近端王座透视与支撑；','')})
replace('CY024K2A','visual_prompt','Do not put people inside a transparent shield: the dark-moon shell is completely opaque deep indigo, no silhouettes.','No shield has formed in this shot; the opaque dark-moon ward will close in the next shot.')
replace('CY024B3','visual_prompt','In FOREGROUND giant thick heavy silver-blue water flow visibly forks LEFT and RIGHT well BEFORE reaching the dome, forming two distinct sweeping outward streams along side steps. The split point and dry central route must be readable together.','The three water columns and all lightning have stopped. Heavy clear runoff from their three separate impact zones merges into the LEFT and RIGHT side routes, sweeping down the side steps. The central route around the dome has remained dry and clear throughout; no incoming stream collides with or splits against the dome.')
plan.update(version='v0.48r1',report_revision='final-v001',story_script='剧本/穿云-场景剧本-v0.48r1.md',audio_arrangement='后期/终极审查-v001/预演编排.json',music_adoption='后期/终极审查-v001/作者确认选曲-v001.json')
plan['review_focus']='终极审查：六段主题加Kimi独立用曲已确认；旧执行说明已同步。图像疑点、动态与正式声音待验见终极审查报告。'
plan['title']='《穿云》带图分镜 v0.48r1 · 七首用曲确认与终极审查'
for a,b in zip(base['shots'],plan['shots']):
    for field in ['dialogue','dialogue_cues','subtitle_cues','generation_request','seconds','start_second','end_second','panel_region']:
        assert a.get(field)==b.get(field),(a['id'],field)
    assert a['presentation']['path']==b['presentation']['path']
    assert b['source_quote'] in script,b['id']
(root/plan['story_script']).write_text(script,encoding='utf-8')
newplan='镜头设计/shot-plan-v0.48r1.json';save(newplan,plan)
config=read(base['audio_arrangement']);config.update(version='final-review-v001',shot_plan=newplan,shot_plan_sha256=hashlib.sha256((root/newplan).read_bytes()).hexdigest())
adopted=read(plan['music_adoption'])
ids=[s['id'] for s in plan['shots']]
for sid,mid in adopted['marks'].items():
    if sid not in config['shot_overrides']:
        section=next(x for x in config['sections'] if ids.index(x['first_shot'])<=ids.index(sid)<=ids.index(x['last_shot']))
        config['shot_overrides'][sid]={'candidates':list(section['candidates']),'note':section['note']}
    c=config['shot_overrides'][sid]
    if mid not in c['candidates']:c['candidates'].insert(0,mid)
    c['status']='作者已确认本镜用曲；其他候选保留对照'
config['adopted_music']=plan['music_adoption']
config['effects']['CY026D']=config['effects']['CY026D'].replace('月背微风','月面安静，无风声')
save(plan['audio_arrangement'],config)
save('后期/终极审查-v001/说明修复记录.json',{'baseline':'镜头设计/shot-plan-v0.48-bgm-v006.json','reviewed':newplan,'preserved':'对白、字幕、时长、镜号、图片路径、冻结生成输入全部不变','changes':edits})
snapshot=root/'镜头设计/带图分镜-第六轮-v048.html'
if not snapshot.exists():shutil.copy2(root/'镜头设计/带图分镜.html',snapshot)
print(f'Reviewed {len(plan["shots"])} shots; {len(edits)} field corrections; 131 adopted music assignments.')
