"""Review/navigation for the saved Resolve assembly, without exporting the film."""
from pathlib import Path
import json,html
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'后期/对白补齐-v009'
p=json.loads((OUT/'对白装配计划.json').read_text(encoding='utf8'))
v=json.loads((OUT/'核验结果.json').read_text(encoding='utf8'))
assert len(p['lines'])==54 and not p['missing'] and v['timeline_saved']
e=html.escape
def tc(f):
 f=int(f);return f'{f//86400:02}:{f//1440%60:02}:{f//24%60:02}:{f%24:02}'
cards=[]
for x in p['lines']:
 rel=Path(x['file']).relative_to(OUT).as_posix()
 label={'selected_master_split':'已选母版切片','existing_selected':'沿用已选独立录音','new_selected_voice_completion':'本轮补录','selected_voice_reading_repair':'本轮读音修正'}[x['source_kind']]
 take=f' · 母版第{x["repeat_take"]}轮' if x['repeat_take'] else ''
 cards.append(f'<article data-kind="{e(x["source_kind"])}"><header><b>{e(x["role"])}</b> · {tc(x["record"])} · {x["duration_seconds"]:.2f}秒</header><small>{e(x["id"])} · {label}{take}</small><p class="ja">{e(x["ja"])}</p><p>{e(x["zh"])}</p><audio controls preload="none" src="{quote(rel)}"></audio><details><summary>来源与装配</summary><p>{e(x["direction"])}</p><p>原速 · 工程增益 {x["gain_db"]:+.2f}dB · {x["sample_rate"]}Hz</p><p>{e(str(Path(x["source"]).relative_to(ROOT)))}</p><code>{x["sha256"]}</code></details></article>')
body='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · v009对白装配</title><style>body{max-width:1080px;margin:32px auto;padding:0 24px;background:#111923;color:#e9edf3;font:16px/1.7 system-ui}a{color:#9bd4ff}h1{font-size:30px}section,article{background:#1b2734;padding:20px;border-radius:12px;margin:16px 0}small,.muted{color:#afc1d3}.ja{font-size:22px}audio{width:100%;max-width:600px}button{background:#304a65;color:white;border:0;border-radius:6px;margin:6px;padding:10px;cursor:pointer}code{word-break:break-all;font-size:12px}header{color:#bbdefa}article[hidden]{display:none}</style><h1>《白米饭》对白已装入达芬奇</h1><section><p><b>v009_Selected_Voices_Assembly</b><br>54句 · 9角色分轨 · 本轮12句缺口已补齐 · v0.69文字</p><p>当前工程已保存。GPT沿用已选v004声线补九句；小鱼经作者授权，以本机IndexTTS参考原声补三句。三句GPT送读和一句Claude咏唱另外修正；旧录音与旧时间线均保留。</p><p>已核对完整路径、SHA、时长、入点、增益和轨道开关；对白无重叠、无重复旧词。v008画面123段、音乐和音效保持原样。</p><p class="muted">本页试听是分句素材，不含达芬奇混音。Kimi/教主第2轮为技术施工选择；未代作者确认逐句表演。精确口型、新救场动作、咏唱画面节奏与最终连续混音仍属于后续声画工作；没有导出视频、DRP或DRT。</p><p><a href="修订说明.md">修订与复看说明</a> · <a href="对白装配计划.json">完整装配计划</a> · <a href="核验结果.json">达芬奇读回</a> · <a href="../../00_打开项目.html">项目首页</a></p></section><nav><button onclick="filter('all')">全部54句</button><button onclick="filter('new')">本轮补录与修正</button></nav>'''
notice='<section><b>配音、文案与字幕核对提示</b><p>当前达芬奇字幕轨为0；下方文字是日语台词和中文回译，尚不是已安装的时间线字幕。开场Claude旧稿“谢谢你，但我……”在v0.68改为“谢谢你……”，配音沿用了短稿；当前声音结束至拍碗段仍约1.89秒，动作接点待处理。</p><a href="../对白字幕核对-v010/核对结论.md">查看删改来源与全54句核对结论</a></section>'
body+='<section><b>这是历史v009快照。</b><p>两处同步已在v010完成：开场接点调整、54条真实中文字幕已安装。<a href="../对白字幕同步-v010/工程内审阅.html">前往当前v010</a></p></section>'+notice+''.join(cards)+'''<script>function filter(k){document.querySelectorAll('article').forEach(a=>a.hidden=k==='new'&&!['new_selected_voice_completion','selected_voice_reading_repair'].includes(a.dataset.kind))}document.addEventListener('play',e=>{if(e.target.tagName==='AUDIO')document.querySelectorAll('audio').forEach(a=>{if(a!==e.target)a.pause()})},true)</script></html>'''
(OUT/'工程内审阅.html').write_text(body,encoding='utf8')
print('54 review cards generated')
