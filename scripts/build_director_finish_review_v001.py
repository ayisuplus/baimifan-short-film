from pathlib import Path
import json,html,os
from urllib.parse import quote

R=Path(__file__).resolve().parents[1];O=R/'后期/导演后期修正-v001'
P=json.loads((O/'后期执行计划.json').read_text(encoding='utf8'))
A=json.loads((R/'后期/导演全片审查-v001/导演审查结论.json').read_text(encoding='utf8'))
S=json.loads((R/'后期/导演全片审查-v001/当前44批审查清单.json').read_text(encoding='utf8'))
EX={4:'求救后换闭口等待；拒绝尾音提前落到孩子反应，保留垂眼。',17:'门洞天空局部压暗转冷；动态遮罩避开走近人物。',21:'回闪入口加一次“稍早”。',25:'完整五列做暗列逐显，消除空版；回现场的音乐入口随新切点重排。',35:'异常眼段全部移除，换普通小鱼反应；雨空单独慢放，雨地与骑士保持原切点。',37:'旧批前8秒解锁保留，仅CY028A换入新拍0–6.208秒。',38:'图标式眼内倒影换父亲实景反打，保留被打断后的停顿。',40:'触木切点前两帧加入局部暖光；独立点燃音效仍待声音制作。',42:'保留空刑架火光下的近景；删去新增火盆的离殿远景，接“数日后”长椅。'}
rows=[]
def tm(t):return f'{int(t)//60:02d}:{t%60:05.2f}'
for b,a,src in zip(P['batches'],A['batches'],S):
    n=b['batch'];ss=[s for s in P['edl'] if s['batch']==n]
    notes=[s['note'] for s in ss if s['note'] and s['note'] not in ['night_sky','flashback_entry','flashback_return','days_later']]
    action=EX.get(n,'；'.join(notes) or '保留现有画面，按选定配音与整片时间线对齐。')
    rows.append(dict(batch=n,id=b['id'],start=b['start']/24,end=(b['start']+b['frames'])/24,original=str(R/src['path']),original_sha256=src['sha256'],audit=a['summary'],action=action,status='单镜补拍并采用' if n==37 else ('后期修订' if a['verdict']=='post' else '保留'),segments=ss))
record={'timeline':P['timeline'],'seconds':P['seconds'],'frames':P['frames'],'video_segments':80,'voice_files':63,'music_segments':13,'original_files_preserved':44,'new_generation_calls':1,'new_generation_seconds':7,'adopted_generation_seconds':149/24,'estimated_generation_credits':71.4,'actual_debit_verified':False,'render':'导出/白米饭-导演修订-v001-r3.mp4','scope':'画面后期修订候选；选定配音与BGM已装配；非发行混音母版','remaining':['独立拟音、环境声尚未完成，本候选未混入生成片原声，以免叠出旧台词/音乐。','未完成连续声音听审、日语发音与逐句口型验收。','低风险表演残留：第4批发言时仍略带笑意，第39批尾部视线仍偏正前；已减少停顿，不宣称表演被完全改写。'],'batches':rows}
(O/'修订交付记录.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
cards=[]
for x in rows:
    orig=quote(os.path.relpath(x['original'],O).replace('\\','/'),safe='/')
    edits='；'.join(f"镜段{i+1}：源{s['source_batch']}批 {s['in']/24:.3f}–{s['out']/24:.3f}s → {s['frames']/24:.3f}s" for i,s in enumerate(x['segments']))
    cards.append(f'''<article id="B{x['batch']:02}"><header><b>第{x['batch']}批 · {html.escape(x['id'])}</b><span>{x['status']}</span></header><button onclick="seek({x['start']})">▶ 修订后 {tm(x['start'])}–{tm(x['end'])}</button><p>{html.escape(x['action'])}</p><details><summary>原问题与原片对照</summary><p>{html.escape(x['audit'])}</p><video controls muted preload="none" src="{orig}"></video><small>原片默认静音，保留历史声音；与新配音选择分开。</small><p class="meta">{html.escape(edits)}</p></details></article>''')
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · 导演修订 v001</title><style>body{margin:0;background:#10151d;color:#e9edf2;font:16px/1.65 system-ui,Microsoft YaHei}main{max-width:1180px;margin:auto;padding:28px}h1{font-size:30px}p{color:#cbd2dc}a{color:#9bcef6}#player{width:100%;max-height:70vh;background:#000}nav{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}button,nav a{background:#23364b;border:1px solid #38516a;border-radius:6px;color:#e4f1ff;padding:8px 12px;cursor:pointer;text-decoration:none}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:18px}article{background:#19222e;padding:20px;border:1px solid #2a394d;border-radius:10px}header{display:flex;justify-content:space-between;gap:12px;margin-bottom:12px}header span{color:#b2d8ac;font-size:13px}article video{width:100%}.meta,small{font-size:12px;color:#a2b0c2}.notice{border-left:3px solid #cba367;padding:12px 18px;background:#28281f}details{margin-top:12px}summary{cursor:pointer}.stats{color:#98c9ed;font-size:18px}</style><main><h1>《白米饭》导演修订 · v001</h1><p class="stats">44批 · 7分40.67秒 · 80个剪辑段 · 63句选定配音 · 13段BGM</p><p>先后期、后补拍。仅第37批“扶下”补拍7秒并取6.208秒，保留该批前8秒解锁。原44批全部保留，文件哈希复核一致。</p><video id="player" controls preload="metadata" src="导出/白米饭-导演修订-v001-r3.mp4"></video><p><a href="导出/白米饭-导演修订-v001-r3.mp4">打开修订整片</a> · <a href="修订说明.md">修订说明</a> · <a href="修订交付记录.json">逐批记录</a></p><p class="notice">这是画面修订候选，已装配选定配音和BGM；独立拟音、环境声与连续听审尚未完成，不能当发行混音母版。片尾4秒无音乐按计划保留，此版尚未补入街声和呼吸。</p><nav>'''+''.join(f'<a href="#B{n:02}">{n}</a>' for n in range(1,45))+'''</nav><div class="grid">'''+''.join(cards)+'''</div></main><script>function seek(t){const v=document.getElementById('player');v.currentTime=t;v.scrollIntoView({behavior:'smooth',block:'center'});v.play();}function hash(){const h=location.hash;if(h.startsWith('#t='))seek(Number(h.slice(3)));}window.addEventListener('hashchange',hash);</script></html>'''
(O/'修订审阅.html').write_text(page,encoding='utf8')
md='''# 《白米饭》导演后期修订 v001

当前可编辑时间线：`v001_Director_Post_Repair_Final`，Resolve工程《白米饭》。1344×768、24fps、11056帧（7分40.667秒）。原片参考线与试修线全部保留。

本轮以剪辑、局部变速、取景裁切、门洞色彩遮罩、回闪/时间省略标记、群像暗列逐显及反应镜替换处理。只有第37批扶下镜在裁切试修失败后使用Metaso MiniMax H3补拍：1次7秒，采用前149帧/6.208秒。该批原前8秒解锁不动。预估71.4积分；未读取实际扣款，不将预估当账单。

主要修正：第4批听话停顿、第5批内心分身发言取景、第11/13批受力剪点、第16/17批破门空间和昼夜、第21/25批回闪提示及完整五列、第27批分裂水滴、第28批提前地面浪、第30批未解锁先垂手、第35/38批异常眼睛、第37批服装连续性、第41/42批抱起到离开、第43/44批交勺与进食收束。第40批只增加触木前两帧局部暖光，点燃拟音仍在声音待办。

63句当前选择的原始录音保持原速，独立对话轨；13段BGM保持原速，重新映射动作瞬态、淡入淡出与对白压低。动作瞬态来自测量，不宣称已经人耳确认是音乐强拍。祈愿0.8秒留白、父亲段停乐、最后4秒音乐为零均保留。声音样本边界与时间线精度单独验证。

## 验证与边界

- 原44批源文件SHA-256全部与审查清单相同，未覆盖。
- 达芬奇最终画面80段起止逐项与EDL一致，无时间线空隙；63句声音原速且完整时长误差在一个采样点内；13段音乐与最终时钟一致。
- 已实际查看导出关键修正帧，独立复核了门洞、水滴、异常眼、补拍服饰/落地、五列与时间标记；技术检测及最终复核见同目录记录。
- 尚未做连续声音听审、逐句日语发音/口型验收。独立拟音和环境声尚未成品；当前新线没有把含旧台词与音乐的生成原声混进来。原始参考线保留原声，可继续取材。此交付是画面修订候选，不是声音制作已完成的发行母版。
- 第4批发言表情仍略带笑意、第39批尾部视线仍偏正前，已减少停顿；未为这类低风险表演余量继续花费重拍。

## 恢复与继续

工程备份 `白米饭-导演修订-v001.drp` 和时间线 `导演修订-v001.drt` 保存在本目录，本机源媒体仍引用项目内原路径。它们不是包含全部媒体的独立归档，迁移电脑时必须同时带齐源视频、63句录音、音乐分段及本次补拍媒体。

`后期执行计划.json` 是最终源片入出点与记录位置，`最终时间线结构.json` 是达芬奇最终读回。`B*.comp` 是采用的Fusion效果；`门洞夜景.comp`和r1/r2试片为历史候选。历史施工脚本只记录当时操作，不能在已装配最终线直接重跑有Ripple的脚本。先建空线再装画面，验证后再装声音。

## 逐批修订

'''
md+='\n'.join(f"- 第{x['batch']}批 [{tm(x['start'])}]：{x['action']}" for x in rows)+'\n'
(O/'修订说明.md').write_text(md,encoding='utf8')
print({'cards':len(cards),'page':str(O/'修订审阅.html')})
