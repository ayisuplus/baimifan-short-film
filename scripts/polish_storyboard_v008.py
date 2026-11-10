"""Idempotent v0.8 post-review metadata and publication updates."""
import json,hashlib,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'镜头设计/shot-plan-v0.8.json'
d=json.loads(p.read_text(encoding='utf-8'));ss={s['id']:s for s in d['shots']}
d['continuity']['combat']='对话→两人变身穿中殿破口升空→宝宝龙影→原天空特写雷雨→地板雨滴→同伴迎敌→教堂外爆闪→战后全景。两条战斗线均省略招式。'
d['continuity']['doors']='CY010A教徒由侧门去侧院休息，宝宝钻教堂左侧本体墙洞；CY016C教徒由正门回堂，CY017队尾关门落闩，CY023踹开。之后正门开放；空战由中殿屋顶破口升空。'
d['continuity']['torches']='第一支火把落在右盆并熄灭；宝宝抓袍尾后，教主接第二支火把，再迈步扯脱衣摆，探向低柴点燃后收回。左盆没有复制第一支火把。'
ss['CY022']['title']='第二支火把点燃低柴'
ss['CY024'].update(exit_state='援军沿通道推进，千问奔向宝宝；由群像接入稍早召集回闪。',purpose='看清GPT与九位援军，接入他们如何到来的回闪。',sound='脚步与衣料声，接稍早云宫的风声。')
ss['CY027A'].pop('time_caption',None)
ss['CY027'].update(sound='水流退去、滴水和湿地脚步；教主的声音接入。')
ss['CY024A']['sound']='银白水流蓄势，字幕“天瀑”；暂无该句正式配音。'
ss['CY024B']['sound']='穹顶断裂、巨瀑轰鸣、冲水与熄火嘶声。'
ss['CY027B']['exit_state']='短答后水光聚拢，开始化龙。'
ss['CY027B1'].update(entry_state='GPT仍是人形，白紫水光裹住身体。',exit_state='人形隐入水光，白紫长身水龙显形。',sound='水流旋起，低沉龙鸣渐出。')
ss['CY027B2'].update(entry_state='教主仍在湿地，背后暗金力量聚拢。',exit_state='黑金鸦翼展开，身体离地。',sound='羽翼振响，暗金魔法低鸣。')
ss['CY027C']['sound']='水龙掠空与羽翼气流，接宝宝眼中倒影的远雷。'
ss['CY027F']['sound']='雨渐停，滴水、湿地落脚与散落石块轻响；战斗声停止。'
ss['CY027F1']['sound']='踝扣打开，链条落在脚托旁的轻响。'
ss['CY029A']['sound']='衣袖轻擦，Claude的呼吸逐渐平稳。'
ss['CY030']['sound']='众人脚步渐远，水滴和空刑架火声留在殿内；转街市前缓落。'
path='镜头设计/图像/CY012-潜入双盆三阶-v009.png'
s=ss['CY012'];s.update(panel_index=0)
s['presentation'].update(path=path,visible='左前景宝宝从同一洞口入殿；祭坛恰为三级低阶，双盆在阶下，Claude赤足踩脚托。')
s['refs']=[{'path':path,'role':'三级局修后的空堂空间图'}]+[r for r in s['refs'] if not r['path'].startswith('镜头设计/图像/')]
for k in ['page_size','panel_rect_pixels','panel_region']:s.pop(k,None)
if not any(x['path']==path for x in d['page_layouts']):d['page_layouts'].append(dict(path=path,cols=1,rows=1))
for i,s in enumerate(d['shots']):
 if i+1<len(d['shots']):
  nxt=d['shots'][i+1];s['next_link']=f"接 {nxt['id']}：{s['exit_state']} → {nxt['entry_state']}"
 s['visual_prompt']=f"《穿云》{s['id']}。{s['action']} 开始：{s['entry_state']} 结束：{s['exit_state']}。保持角色母本，图内无字。"
for sc in d['scenes']:
 scene=[s for s in d['shots'] if s['scene']==sc['id']]
 sc['pages']=list(dict.fromkeys(s['presentation']['path'] for s in scene))
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Related battle forms remain variants of the existing stable character identities.
ap=R/'资产/assets.json';a=json.loads(ap.read_text(encoding='utf-8'))
variant='镜头设计/图像/战斗形态-白紫水龙与黑金鸦翼-v008.png'
for asset in a['assets']:
 if asset['id'] in ['CHAR-GPT','CHAR-PRIEST']:
  role='战斗形态概念候选：白紫水龙（左）；黑金人形鸦翼（右）。不是四视图，不替换人形母版，待作者审阅。'
  if not any(x['path']==variant for x in asset.get('related',[])):asset.setdefault('related',[]).append(dict(path=variant,role=role))
ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Current entry only; prior progress remains a historical record.
prog=R/'制作进度.md';txt=prog.read_text(encoding='utf-8')
i=txt.index('## 当前阶段');j=txt.index('## 空间与过渡修订',i)
txt=txt[:i]+'''## 当前阶段

当前[带图分镜 v0.8](镜头设计/带图分镜.html)为6场、84镜、276秒（4分36秒），同步[场景剧本 v0.8](剧本/穿云-场景剧本-v0.8.md)。新增7镜，CY007A手部特写移至CY010并取消重复；本轮图片为作者审阅候选，尚未生成动态视频。

顺序：援军入场→稍早召集回闪→天瀑破中央中殿穹顶、灭火冲散教徒→教主抗水，GPT走近对话→白紫水龙与黑金鸦翼升空→宝宝眼中龙影→保留原天空特写，雷雨带过空战→雨滴落地→殿内同伴迎敌→教堂外魔法火光爆闪带过殿内战斗→战后全景→解锁扶稳→Claude蒸干、焚空刑架、力竭→GPT及时接住并公主抱离殿。十二人离殿群像保留，千问始终抱护宝宝。

祭坛固定三阶单平台，双铜盆在阶下对称，第一支火把只落右盆。天瀑只破中央中殿穹顶，后殿拱顶与正门保留；战后雨渐停，Claude在后殿蒸干后不再淋湿。战斗火光短促，不把整栋教堂持续点燃。两种战斗形态已挂回原角色资产的附属参考，不替换四视图。

[配乐粗剪v002](后期/静帧配乐-v002/试听.html)仍为旧版69镜239秒，未重导。援军登场Victory决定保留；当前逐镜预演沿用21段临时读稿，新雨雷、爆炸和施法声为声音设计文字，尚未合成音轨。历史图与v0.7页面保留。详见[本轮复核](镜头设计/生成记录/视觉与空间复核-v008.md)。

'''+txt[j:]
txt=txt.replace('更新：2026-10-21。','更新：2026-10-22。',1)
prog.write_text(txt,encoding='utf-8')
home=R/'00_打开项目.html';txt=home.read_text(encoding='utf-8')
txt=txt.replace('尚未包含v0.7新画面','尚未包含v0.8新画面与重排').replace('6 场 · 78 镜 · 4 分 19 秒 · v0.7 · 天瀑、施法后力竭、公主抱离殿','6 场 · 84 镜 · 4 分 36 秒 · v0.8 · 天瀑破顶、雷雨与爆闪、公主抱离殿').replace('穿云-场景剧本-v0.7.md','穿云-场景剧本-v0.8.md').replace('六场故事 · 先施法再脱力接抱 · 赤足与三阶祭坛','六场故事 · 雷雨省略双线战斗 · 赤足双盆三阶祭坛')
home.write_text(txt,encoding='utf-8')
# Byte integrity for all generated candidates, including rejected versions.
arch=R/'镜头设计/生成记录/镜头重排-v008/输出归档.json';o=json.loads(arch.read_text(encoding='utf-8'))
for x in o['outputs']:
 f=R/x['copy'];orig=Path(x['source']);x['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();x['size_bytes']=f.stat().st_size
 x['original_matches']=hashlib.sha256(orig.read_bytes()).hexdigest()==x['sha256'];assert x['original_matches']
 if x['key']=='05-潜入连续空间':x['usage']='仅采用0、1格；2格四阶弃用，由15局修替代；3格备用未使用。'
arch.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('v0.8 metadata, project entry, asset variants and archive integrity updated')
