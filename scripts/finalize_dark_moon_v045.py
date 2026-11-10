"""Synchronize residual continuity summaries after the v045 shot migration."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
changes={
'苍龙雷渊前干燥；苍龙雷渊后湿贴发丝肩背':'入罩前保留汗湿发丝；暗月罩隔绝天瀑直冲，撤罩后仅殿内水雾轻沾衣发',
'天瀑前干燥；天瀑后湿贴发丝肩背':'入罩前保留汗湿发丝；暗月罩隔绝天瀑直冲，撤罩后仅殿内水雾轻沾衣发',
'Kimi在CY024K2先撑盾、K3才劈拨；之后中央净空、火只留两侧低散柴':'Kimi在CY024K2循刃瞬移、回收明刃并向外震柴，K3以暗刃闭合不透明月罩；之后中央净空、燃木全留在罩外两侧',
'点燃后Kimi先保护两人，再以实体暗刃劈开并向两侧外下方拨散木头；残柴仍燃，水雷才灭火':'点燃后Kimi用明刃钉住柴堆外缘，循刃瞬移时回收明刃并以地面气浪向两侧外下方震散重柴，再以暗刃闭合不透明月罩；残柴留在罩外继续燃烧，水雷才灭火',
'月辉阻止后续伤害':'暗月罩隔绝后续火焰、水雷伤害',
'Kimi维持月辉':'Kimi维持暗月罩',
'在Claude月辉之外断开':'在祭坛暗月罩之外断开',
'Claude月辉与侧柱护光已就位':'祭坛暗月罩与侧柱护光已就位',
'Kimi由后窗进入':'Kimi在中央后窗外投刃、循刃瞬移进入',
'Kimi已从后窗进入，在最高祭坛维持两人的结界':'Kimi已从中央后窗外循刃瞬移至最高祭坛，维持覆盖两人与刑架的不透明暗月罩',
'Kimi的后窗突入与正门行动配合':'Kimi从后窗投刃瞬移的行动与正门行动配合',
'Claude衣料轮廓旁的月辉平时近乎透明，只有受冲时局部亮起，束具仍未解除':'祭坛暗月罩始终不透明，罩外不见人物和刑架；罩内Claude的束具仍未解除',
'## 乌烬木、月刃与星火 · v0.41':'## 乌烬木、月刃与星火 · v0.45',
'火祭与暗月救援 · v0.45 · 119镜394秒；16张修订候选待审':'暗月瞬临与罩内抱护 · v0.45 · 127镜420.5秒；17张修订候选待审',
'6 场 · 119 镜 · 6 分 34 秒 · 抱柴、逐次阻拦、Kimi暗月破柴与护盾':'6 场 · 127 镜 · 7 分 00.5 秒 · 明刃破窗、瞬移震柴、罩内抱护',
'本轮：Kimi月光与救赎<small>Kimi指尖月牙→贴身月辉→受击偏水→撤辉后解锁':'本轮：Kimi罩内抱护<small>收刃抱托→贴头拭汗→查看踝链→巨浪中抱护撑罩→撤罩接钥匙',
'本轮：Kimi暗月破柴<small>暗面裂柴→贴身月辉':'本轮：Kimi明刃破窗与瞬移救援<small>月下剪影→力量破窗→明刃钉柴→瞬移爆气震柴→暗刃闭合不透明月罩'
}
for rel in ['镜头设计/shot-plan-v0.45.json','剧本/穿云-场景剧本-v0.45.md','资产/assets.json','00_打开项目.html']:
 p=R/rel;text=p.read_text('utf-8')
 for a,b in changes.items():text=text.replace(a,b)
 p.write_text(text,'utf-8')
p=R/'后期/暗月瞬临-v045/预演编排.json';a=json.loads(p.read_text('utf-8'));a['shot_plan_sha256']=hashlib.sha256((R/'镜头设计/shot-plan-v0.45.json').read_bytes()).hexdigest();p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n','utf-8')
print('Synchronized v045 continuity summaries and audio plan hash.')
