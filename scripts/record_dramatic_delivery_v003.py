from pathlib import Path
import json,html,subprocess,re
R=Path(__file__).resolve().parents[1];O=R/'后期/导演重构-v003'
P=json.loads((O/'后期执行计划.json').read_text(encoding='utf8'));V=json.loads((O/'验证结果.json').read_text(encoding='utf8'))
def tc(f):return f'{f//86400:02d}:{f//1440%60:02d}:{f//24%60:02d}:{f%24:02d}'
points=[('入殿空间','church_space'),('听见搬柴、决定行动','child_decision'),('教徒推开小鱼','acolyte_force'),('教主说话口型','father_audio'),('教主推开小鱼','father_force'),('Claude恳求与父亲拒绝','claude_audio'),('Kimi主动防御','kimi_defense'),('GPT咏唱主体与水息','gpt_chant'),('战后退水过渡','retreating_water'),('Claude画外半句','claude_offscreen')]
times=[(label,tc(next(x['record'] for x in P['edl'] if x.get('anchor')==a))) for label,a in points]
notes="""# 导演重构 v003 · 工程内复看候选

已保存至达芬奇工程《白米饭》，时间线 **v003_Dramatic_Reconstruction**。44批、113剪辑段、7分59秒01帧，比作者当前v002长12.25秒。旧时间线、原始媒体、所有候选以及作者在第12批删掉的20帧均保留。

## 本轮处理

| 作者问题 | 本轮实施 | 验收边界 |
|---|---|---|
| 对口型 | Claude恳求、教主长句、GPT两句咏唱按实际选声作为H3音频参考重拍；第34批回应后移13帧；第37批半句用闭口听者反应承接 | 参考音频驱动不保证逐音素通过，全片口型仍待连续复看 |
| 缺音效 | 补身体落地、掌根接触、撑地、脚底、刀刃、锁具和护罩撞击；按景别重排电平 | 126处可追踪事件，数字不是听感验收 |
| 缺过渡 | 小鱼听声决定、父亲闭口拒绝、教堂纵深、退水过程与罩外全景、咏唱后的云天 | 有因果或空间用途才插入；不是每换一个人都加空镜 |
| 时长偏短 | 空间、反应和受力恢复增加停留；冲量与命中压紧 | 不统一慢放全片 |
| 争执无力量 | 教徒短促推开、孩子离地落地；父亲推开二轮脚接地，剪掉托肩等待、保落地恢复 | 父亲第一轮悬浮轻放拒用；二轮仍是作者待验候选 |
| Kimi因果与皮影感 | 保留敌方先蓄力，再接Kimi落脚挥刃；去掉成盾等待，命中后接旧不透明罩余波 | 新片透明罩后段不用；显形旧段仍需整体观感复看 |
| GPT咏唱 | 头四句保调1.12倍速；恢复施术者眼神/嘴/手/水息，插入原有敌矛与扇盾因果 | 未改词，其他对白及术名原速；保调音质与韵律待听审 |
| BGM空缺与声音一致性 | 13段重切加4处过桥底，共17段；连续环境底、水声跨祈愿停乐，近景受力声抬出 | 4首新下载BGM已入素材池候选箱，未冒称试听采用；角色跨句音色/响度留最后精修 |

## 复看位置

"""
notes+='\n'.join(f'- {t}：{label}' for label,t in times)
notes+="""

## 声音与来源

8条启用音轨：Dialogue_Selected、Music_A/B/C、Ambience、Foley、Action、Magic。63条作者选声以64个片段保留（教主长句沿用作者切开的两段），只有头四句GPT咏唱用获授权速度候选。工作WAV是可编辑媒体，不是交付成片。四处长音乐空白改为试排过桥底；开场、破门前、祈愿0.8秒与结尾4秒仍保留设计停乐。

新增音效源为効果音ラボ与Mixkit。新增音乐4首在素材池 **08_BGM_New_Audition_Candidates**，来源与具体许可见JSON；Mixkit音乐许可用于网络/社交视频，不能据此泛称电视、广播、游戏均获授权。没有从未安装的Fairlight库虚构素材。链条轻响使用已有小金属声作代理，未称新录真实链声。

## 验证与剩余工作

逐项读回达芬奇113段画面与85段音频素材、8轨启用；对白/同轨音乐无重叠或越界。实际工作PCM有限且无削波，保护停乐期间环境水底连续。第12批两段声音实测保留原源0–4.416667秒及5.25–6.3秒，未回填作者删帧。Claude及父亲裁切另抓工程预览静帧，修正了纵向偏移和背景火盆露边；没有输出新视频、DRP或DRT。

9次局部H3任务全部回片，8条作为本轮剪辑候选，1条拒用保留。预计591.6积分，未核实际账单。没有整批重做。

仍待：全片连续听审、逐音素口型核验、表演张力及构图最终作者核验、最后的跨句音色/响度精修。结构及PCM通过不等于这些项目已通过。作者最终核验并明确要求后再导出。
"""
(O/'修订说明.md').write_text(notes,encoding='utf8')
cards=''.join(f'<tr><td><button onclick="navigator.clipboard.writeText(\'{t}\')">{t}</button></td><td>{html.escape(label)}</td></tr>' for label,t in times)
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>白米饭 · 导演重构 v003</title><style>body{background:#10141c;color:#e8edf4;font:17px/1.75 system-ui;max-width:1050px;margin:40px auto;padding:0 24px}h1{font-size:30px}p{max-width:950px}table{border-collapse:collapse;width:100%}td{padding:10px;border-bottom:1px solid #303a48}button{background:#26384b;color:#e9f3ff;border:1px solid #506b8d;border-radius:6px;padding:7px;cursor:pointer}a{color:#9bcaff}.badge{color:#ffd78d}</style><h1>白米饭 · 导演重构 v003</h1><p class="badge">工程内复看候选 · 尚未最终验收 · 未导出视频或工程</p><p>打开达芬奇工程《白米饭》的 <b>v003_Dramatic_Reconstruction</b>。7分59秒01帧；旧版与作者20帧删改保留。先看下列接头；按钮复制达芬奇时码。</p><table>'+cards+'</table><p>8条启用声音轨；63句选声，头四句GPT咏唱保调1.12倍。音乐长空缺、受力与护罩音效已重新试排。逐音素口型、连续听感与张力仍待复看。</p><p>9次局部补拍，8采用候选、1拒用；预估591.6积分，未核账单。</p><p><a href="修订说明.md">完整修订说明</a> · <a href="验证结果.json">工程验证</a> · <a href="../../视频制作/Metaso-H3-v006/补拍输入.html">本轮补拍输入和回片</a> · <a href="新增BGM来源.json">4首新增BGM来源</a></p></html>'
(O/'工程内审阅.html').write_text(page,encoding='utf8')
# Stage only a new navigation prefix against HEAD; preserve unrelated dirty root contents.
prefix="""## 2026-10-28：导演重构 v003（当前工程内复看候选）

达芬奇工程《白米饭》当前时间线为 `v003_Dramatic_Reconstruction`：44批、113段、11497帧（7分59秒01帧），63句选声以64片段保留、17音乐段、126音效事件、8条启用声音轨。作者第12批删20帧保留；头四句GPT咏唱保调1.12，其余对白/术名原速。局部补拍9次、8条候选采用、1条拒用，预计591.6积分未核账单，没有整批重做。

入口：[工程内审阅](后期/导演重构-v003/工程内审阅.html)；[修订说明](后期/导演重构-v003/修订说明.md)。结构/PCM核验通过不等于连续听审、音素口型或最终张力验收。旧版、原素材、作者选择与候选保留。没有新视频/DRP/DRT导出；仅抓裁切核验静帧。作者最终核验并明确要求后再导出。以下是历史状态。

"""
for name in ['AGENTS.md','制作进度.md']:
 path=R/name;working=path.read_text(encoding='utf8');assert not working.startswith(prefix.splitlines()[0]);path.write_text(prefix+working,encoding='utf8')
 base=subprocess.check_output(['git','show','HEAD:'+name],cwd=R)
 staged=prefix.encode()+base
 oid=subprocess.check_output(['git','hash-object','-w','--stdin'],cwd=R,input=staged).decode().strip()
 subprocess.run(['git','update-index','--add','--cacheinfo','100644',oid,name],cwd=R,check=True)
name='00_打开项目.html';path=R/name
banner='<section id="director-v003" style="margin:18px;padding:18px;border:2px solid #b69460;background:#172336;color:#fff"><h2>当前：导演重构 v003 · 达芬奇工程内复看</h2><p>时间线 v003_Dramatic_Reconstruction · 7分59秒01帧 · 画面与8轨声音已装配，未最终验收、未导出。</p><a style="color:#a9d6ff" href="后期/导演重构-v003/工程内审阅.html">查看复看时码和本轮修订</a></section>'
def insert(s):
 assert 'id="director-v003"' not in s
 if re.search(r'<body[^>]*>',s,re.I):return re.sub(r'(<body[^>]*>)',lambda m:m.group(1)+banner,s,count=1,flags=re.I)
 assert '</style>' in s
 return s.replace('</style>','</style>'+banner,1)
working=path.read_text(encoding='utf8');path.write_text(insert(working),encoding='utf8')
base=subprocess.check_output(['git','show','HEAD:'+name],cwd=R).decode('utf8');staged=insert(base).encode()
oid=subprocess.check_output(['git','hash-object','-w','--stdin'],cwd=R,input=staged).decode().strip();subprocess.run(['git','update-index','--add','--cacheinfo','100644',oid,name],cwd=R,check=True)
print(json.dumps(dict(timeline=P['timeline'],review_points=times),ensure_ascii=False))
