"""Publish versioned candidates and review evidence, without adopting or replacing source media."""
from pathlib import Path
import html,json,os,subprocess,hashlib,argparse
parser=argparse.ArgumentParser();parser.add_argument('--revision',choices=['v002','v003'],default='v002');args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/('视频制作/Metaso-H3-'+args.revision)
def read(p):return json.loads(p.read_text(encoding='utf8'))
def esc(s):return html.escape(str(s))
def url(p):return esc(Path(os.path.relpath(ROOT/p,OUT)).as_posix())
q=read(OUT/'执行队列.json');w=read(ROOT/'后期/制作工作台-v025/工作台数据.json')
history=[]
for name,provider in [('LibTV-H3-v001/H3节约余量执行队列.json','LibTV'),('Metaso-H3-v001/执行队列.json','Metaso v001')]:
 for x in read(ROOT/'视频制作'/name)['items']:
  if x.get('local_path'):history.append(dict(x,provider=provider))
current=[dict(x,provider='Metaso '+args.revision) for x in q['items']]
selection=read(OUT/'剪辑候选.json') if (OUT/'剪辑候选.json').exists() else {}
notes=read(OUT/'审查汇总.json') if (OUT/'审查汇总.json').exists() else {}
if args.revision=='v003':
 for x in read(ROOT/'视频制作/Metaso-H3-v002/执行队列.json')['items']:
  if x.get('local_path'):history.append(dict(x,provider='Metaso v002'))
 selection={**read(ROOT/'视频制作/Metaso-H3-v002/剪辑候选.json'),**selection}
 notes={**read(ROOT/'视频制作/Metaso-H3-v002/审查汇总.json'),**notes}
cards=[];complete=0
for i,b in enumerate(w['batches'],1):
 attempts=[x for x in history+current if x['batch_id']==b['id']]
 available=[x for x in attempts if x.get('local_path')]
 if available:complete+=1
 chosen=selection.get(b['id'])
 main=chosen or (available[-1] if available else {})
 note=notes.get(b['id'],{});state=note.get('status','待逐镜视听复核')
 if main.get('local_path'):
  posters=OUT/'页面缩略';posters.mkdir(exist_ok=True)
  poster=posters/(b['id']+'-'+hashlib.sha256(main['local_path'].encode()).hexdigest()[:8]+'.jpg')
  if not poster.exists():subprocess.run(['ffmpeg','-v','error','-y','-ss','0.3','-i',str(ROOT/main['local_path']),'-frames:v','1','-vf','scale=640:-1',str(poster)],check=True)
  media=f'<video controls playsinline muted preload="none" poster="{url(poster.relative_to(ROOT).as_posix())}" src="{url(main["local_path"])}"></video>'
  media+='<p class="meta">'+(esc(chosen.get('audio','修订剪辑试听：叠加v025原速配音/BGM，口型未验收。')) if chosen else '模型原生回片：未替换最终配音/BGM。')+'</p>'
 else:media='<p>尚未回片</p>'
 if not chosen and main.get('part_offset') is not None:media='<p class="warn">下方为局部补拍，完整批次剪辑尚未发布。</p>'+media
 rows=[]
 for x in attempts:
  label=x.get('attempt_id',x['provider']+' 原片')
  if x.get('local_path'):rows.append(f'<li><a href="{url(x["local_path"])}">{esc(label)}</a> · {esc(x.get("change_reason","历史候选保留"))}</li>')
  else:rows.append(f'<li>{esc(label)} · {esc(x["status"])}</li>')
 shotnames=' / '.join(f'第{i}批第{j}镜（{s}）' for j,s in enumerate(b['shot_ids'],1))
 issues=note.get('notes',[])
 cards.append(f'<article id="{b["id"]}" data-state="{esc(state)}"><small>{esc(state)}</small><h2>第{i}批 · {esc(b["title"])}</h2>{media}<p>{esc("；".join(issues))}</p><p class="meta">{esc(shotnames)}<br>原定剪辑长 {b["used_seconds"]:.3f} 秒</p><details><summary>原片、补拍与历史对比（{len(attempts)}）</summary><ul>{"".join(rows)}</ul></details></article>')
running=sum(x['status']=='running' for x in current);done=sum(bool(x.get('local_path')) for x in current)
balance=f'余额回读 {q["observed_final_balance"]} 积分' if 'observed_final_balance' in q else f'提交前余额 {q.get("observed_start_balance",9515.6)} 积分；实际余额待回读'
links=[]
for p in sorted(OUT.glob('*.json')):
 if any(s in p.name for s in ['复核','审查汇总','剪辑候选','参考精简','交付核验','接头剪辑修复']):links.append(f'<a href="{esc(p.name)}">{esc(p.stem)}</a>')
page=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · 精简与返修 v002</title>
<style>body{{background:#10141d;color:#e7ebf4;font:16px/1.6 system-ui;margin:0}}main{{max-width:1200px;margin:auto;padding:30px 24px}}h1{{margin:0}}h2{{font-size:20px}}p,small,.meta{{color:#b8c3d9}}a{{color:#8fcaff}}header,article{{background:#1b2535;padding:22px;border-radius:14px}}header{{margin-bottom:24px}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}}video{{width:100%;aspect-ratio:16/9;background:#000}}.warn{{color:#ffc58c}}details{{margin-top:12px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}button{{background:#30405b;color:white;border:0;border-radius:8px;padding:10px;cursor:pointer}}@media(max-width:760px){{.grid{{grid-template-columns:1fr}}}}</style>
<main><header><small>白米饭 / Metaso MiniMax H3 / 768P普通通道</small><h1>{complete} / 44 批已有回片</h1><p>13批待生成输入：121张参考精简至101张；每次≤9张。原片与旧版完整保留。</p><p>本轮已回 {done} 个任务，运行中 {running} 个。{balance}。</p><p class="warn">修订剪辑已叠加v025原速配音/BGM供试听，历史原片保留模型原声。下载或局部视觉修复不代表最终采用；口型、动作跨切和完整声音仍须验收。</p><nav><a href="../../后期/制作工作台-v025/工作台.html">台词、配音与BGM工作台</a><a href="../Metaso-H3-v001/生成进度.html">上轮回片</a><a href="执行队列.json">冻结任务与记录</a></nav><details><summary>审查证据</summary>{' · '.join(links)}</details><p><button onclick="filter(false)">全部44批</button> <button onclick="filter(true)">仅需处理</button></p><nav>{' '.join(f'<a href="#{b["id"]}">{i}</a>' for i,b in enumerate(w['batches'],1))}</nav></header><div class="grid">{''.join(cards)}</div></main><script>document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(x=>{{if(x!==v)x.pause()}})));function filter(on){{document.querySelectorAll('article').forEach(x=>x.hidden=on&&!/返修|阻断|待处理/.test(x.dataset.state))}}</script></html>'''
if args.revision=='v003':
 page=page.replace('精简与返修 v002','五批整段重拍 v003').replace('13批待生成输入：121张参考精简至101张；每次≤9张。原片与旧版完整保留。','第6、11、20、21、39批按完整动作链返修；第40批连带修接头。补拍使用1张起态参考，闭罩镜另补1张终态。默认显示本轮6批，旧候选保留。')
 page=page.replace('修订剪辑已叠加v025原速配音/BGM供试听','新候选沿用选定原速配音/BGM；第21批千问回应后移0.45秒，合扇后入声').replace('../Metaso-H3-v001/生成进度.html','../Metaso-H3-v002/生成进度.html')
 page=page.replace(' playsinline muted ', ' playsinline ')
 page=page.replace('<button onclick="filter(true)">仅需处理</button>', '<button onclick="repairs()">本轮6批返修</button>')
 page=page.replace('</script>', "function repairs(){document.querySelectorAll('article').forEach(x=>x.hidden=!['GB005','GB009','GB015-2','GB016-1','GB029','GB030-1'].includes(x.id))}repairs();document.querySelectorAll('nav a[href^=\"#\"]').forEach(a=>a.addEventListener('click',()=>filter(false)));</script>")
(OUT/'生成进度.html').write_text(page,encoding='utf8')
print(json.dumps(dict(unique_batches=complete,downloaded_tasks=done,running=running),ensure_ascii=False))
