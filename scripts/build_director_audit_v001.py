"""Publish a read-only director audit linked to the frozen, actual video candidates."""
from pathlib import Path
import json,html,os,collections
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'后期/导演全片审查-v001'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def esc(v):return html.escape(str(v))
def href(p):return esc(Path(os.path.relpath(ROOT/p,OUT)).as_posix())
def shot_names(batch,issue):
 names={s['id']:s.get('display_name',s['id']) for s in batch['shots']}
 return '、'.join(names.get(s,s) for s in issue.get('shot_ids',[]))
a=read(OUT/'当前44批审查清单.json');g=read(OUT/'全片导演意见.json')
rows=[]
for name in ['分段审查-01-15.json','分段审查-16-30.json','分段审查-31-44.json']:
 data=read(OUT/name)
 if isinstance(data,dict): data=data.get('batches') or data.get('reviews') or data.get('results')
 assert isinstance(data,list),name
 rows+=data
by={r['batch_number']:r for r in rows}
assert len(rows)==len(by)==44 and set(by)==set(range(1,45))
calibrations=read(OUT/'主审校准.json')
for c in calibrations:
 issue=by[c['batch_number']]['issues'][c['issue_index']]
 issue['priority']=c['priority'];issue['director_calibration']=c['reason']
labels={'regenerate':'必须局部重生','post':'后期可修','keep':'可保留','optional':'可选提升'}
count=collections.Counter(r['verdict'] for r in rows)
post_required=[r['batch_number'] for r in rows if r['verdict']=='post' and any(x['category']=='post' and x.get('priority') in ('P0','P1') for x in r.get('issues',[]))]
post_polish=[r['batch_number'] for r in rows if r['verdict']=='post' and r['batch_number'] not in post_required]
report={'coverage':{'batches':44,'planned_shots':133,'visual_method':'全时长2fps基础抽帧，疑点另加密/大图核查；不是实时连续带声观看','audio_listened':False},'picture_primary_counts':dict(count),'classification_limit':'后期可修表示已有可用素材与具体修法，不代表试剪或合成已经验证。若保留必要动作与台词后仍无法成立，升级为该局部镜头补拍。可保留不等于整片声音、口型或最终观感验收。','global':g,'batches':[by[i] for i in range(1,45)]}
report['post_priority']={'required_first_batches':sorted(post_required),'polish_only_batches':sorted(post_polish)}
(OUT/'导演审查结论.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
cards=[];md=['# 《白米饭》全片导演审查','',g['creative_thesis'],'','本轮审查当前工作台44批/133镜对应候选，保留源文件哈希。全时长2fps视觉覆盖与重点密采样，未完成实时连续听审；以下重生判断针对画面。未提交生成、未修改原片和作者选声。','',f'画面主分类：必须局部重生 {count["regenerate"]} 批；后期可修 {count["post"]} 批；可保留 {count["keep"]} 批。全片声音统一装配另列，不把每批因此重复归为问题。','','## 全片组织与后期','']
md += [f'后期类中，{len(post_required)}批列有P0/P1优先处理项，{len(post_polish)}批只有P2优化建议；不要把所有节奏偏好都当成硬伤。','分类边界：后期可修表示已有可用素材与具体修法，不代表试剪或合成已经验证。若保留必要动作与台词后仍无法成立，再升级该局部镜头补拍。可保留不等于全片验收。','']
for issue in g['issues']:
 md += [f'### {issue["id"]} · {issue["batches"]} · {labels[issue["category"]]}',issue['problem'],'',issue['repair'],'',issue['why_post'],'']
md+=['## 后期失败时才升级局部补拍','']
for x in g.get('conditional_pickups',[]):
 md += [f'- **第{x["batch_number"]}批**：{x["condition"]} {x["status"]}']
md+=['','## 44批逐项结论','','|批次|画面主结论|主要判断|','|---|---|---|']
for b in a:
 r=by[b['batch_number']];issues=r.get('issues',[]);kind=r['verdict'];parts=[]
 md.append(f'|第{b["batch_number"]}批 {b["id"]}|{labels[kind]}|{r["summary"].replace("|","/")}|')
 for j,x in enumerate(issues):
  start=x.get('local_start',0);end=x.get('local_end',start);start=0 if start is None else start
  parts.append(f'<p class="muted">{esc(shot_names(b,x))}</p>')
  evidence=[]
  for p in x.get('evidence',[]):
   path=ROOT/p
   if not path.exists():path=OUT/p
   if path.exists():evidence.append(f'<a href="{href(path.relative_to(ROOT))}">{esc(path.name)}</a>')
  parts.append(f'<section class="issue {esc(x["category"])}"><b>{esc(x.get("priority","P1"))} · {labels[x["category"]]}</b> <button data-jump="{start}">{start}–{end}秒</button><p>{esc(x["problem"])}</p><p class="muted">观感：{esc(x.get("viewer_impact",""))}</p><p>处理：{esc(x["repair"])}</p><p class="muted">依据：{esc(x.get("why_post_insufficient_or_feasible",""))}</p><small>{" · ".join(evidence)}</small></section>')
 poster=b['sheets'][0]
 folder=Path(poster).parent
 frame=folder/'frame-0001.jpg'
 cards.append(f'<article id="B{b["batch_number"]}" data-kind="{kind}"><small>{labels[kind]} · {b["id"]}</small><h2>第{b["batch_number"]}批 · {esc(b["title"])}</h2><p>{esc(r["summary"])}</p><video controls playsinline preload="none" poster="{href(frame)}" src="{href(b["path"])}"></video><p class="muted">本批实际 {b["video_duration"]:.3f}秒 / 规划 {b["planned_duration"]:.3f}秒；{esc(b["audio_state"])}</p>{"".join(parts)}<details><summary>全时长抽帧与审查边界</summary><p>{esc(r.get("review_method",""))}</p><p>{esc(r.get("limits","未作完整听审。"))}</p>{" · ".join(f"<a href=\"{href(p)}\">图表{k+1}</a>" for k,p in enumerate(b["sheets"]))}</details></article>')
md+=['','## 定位与处理明细','']
for b in a:
 r=by[b['batch_number']]
 md += [f'### 第{b["batch_number"]}批 · {b["title"]}',r['summary'],'']
 for x in r.get('issues',[]):
  md += [f'镜头：{shot_names(b,x)}','']
  md += [f'- **{labels[x["category"]]} / {x.get("priority","P1")} / 本批{x.get("local_start")}–{x.get("local_end")}秒**：{x["problem"]}',f'  - 影响：{x.get("viewer_impact","")}',f'  - 修法：{x["repair"]}',f'  - 判断依据：{x.get("why_post_insufficient_or_feasible","")}',f'  - 证据：{"、".join(x.get("evidence",[]))}']
 md+=['']
(OUT/'导演审查报告.md').write_text('\n'.join(md),encoding='utf8')
globalhtml=''.join(f'<section class="issue post"><b>{esc(x["id"])} · {esc(x["batches"])}</b><p>{esc(x["problem"])}</p><p>{esc(x["repair"])}</p></section>' for x in g['issues'])
globalhtml+='<h3>后期失败时才升级局部补拍</h3>'+''.join(f'<section class="issue optional"><b>第{x["batch_number"]}批</b><p>{esc(x["condition"])}</p><small>{esc(x["status"])}</small></section>' for x in g.get('conditional_pickups',[]))
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · 全片导演审查</title><style>body{margin:0;background:#10151e;color:#e4e9f1;font:16px/1.65 system-ui}main{max-width:1200px;padding:28px;margin:auto}header,article{padding:24px;background:#1b2534;border-radius:14px;margin-bottom:24px}h1{font-size:32px}h2{font-size:23px}a{color:#9bcbff}video{width:100%;max-height:560px;background:#000}.muted,small{color:#adbed3}button{background:#354861;border:0;color:white;padding:8px 12px;border-radius:5px;cursor:pointer;margin:4px}.issue{border-left:4px solid #719dcc;padding:12px 18px;margin:14px 0;background:#17202e}.regenerate{border-color:#ee8d7b}.optional{border-color:#bcb388}nav{display:flex;flex-wrap:wrap;gap:10px}.stats{font-size:21px}.issue p{margin:8px 0}[hidden]{display:none!important}</style><main><header><small>导演审查 / 当前44批候选 / 不启动生成</small><h1>先修叙事与动作，再修画面包装</h1>'''
page+=f'<p>{esc(g["creative_thesis"])}</p><p class="stats">必须局部重生 {count["regenerate"]} 批 · 后期可修 {count["post"]} 批 · 可保留 {count["keep"]} 批</p><p class="muted">覆盖全部44批与133镜对应候选。全时长2fps视觉覆盖，疑点另密采样；未作实时连续带声观看。声音统一装配另列。时间按钮均为本批实际视频秒数，稳定镜号仅表示镜头意图，不伪装自动检测边界。</p><p><a href="导演审查报告.md">完整文字报告</a> · <a href="导演审查结论.json">结构化结论</a> · <a href="../../视频制作/Metaso-H3-v003/生成进度.html">返回生成工作台与历史候选</a></p><details><summary>全片层面的6项后期意见</summary>{globalhtml}</details><p><button data-filter="all">全部44批</button><button data-filter="regenerate">必须局部重生</button><button data-filter="post">后期可修</button><button data-filter="keep">可保留</button></p><nav>{" ".join(f"<a href=\"#B{i}\">{i}</a>" for i in range(1,45))}</nav></header>{"".join(cards)}</main>'
page+='''<script>function filter(k){document.querySelectorAll('article').forEach(a=>a.hidden=k!=='all'&&a.dataset.kind!==k)}document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>filter(b.dataset.filter));document.querySelectorAll('[data-jump]').forEach(b=>b.onclick=()=>{let v=b.closest('article').querySelector('video');let go=()=>{v.currentTime=Number(b.dataset.jump);v.play().catch(()=>{})};if(v.readyState)go();else{v.addEventListener('loadedmetadata',go,{once:true});v.load()}});document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(x=>{if(x!==v)x.pause()})));document.querySelectorAll('nav a').forEach(a=>a.onclick=()=>filter('all'));</script></html>'''
page=page.replace('<p class="muted">覆盖全部44批', '<p><strong>必须先修：</strong>第30批腕扣未解却双手垂下；第16–17批破门方向与门洞昼夜；第21–25批回闪时态。第16批若试剪仍不能明确从外入内，则升级为踹门单镜补拍。后期方案尚未试剪，未列必须重生不等于可以直接定片。</p><p class="muted">覆盖全部44批')
page=page.replace('<p><strong>必须先修：</strong>',f'<p>后期类中：{len(post_required)}批有P0/P1优先处理项，{len(post_polish)}批仅有P2优化建议。</p><p><strong>必须先修：</strong>')
(OUT/'导演审查.html').write_text(page,encoding='utf8')
print(json.dumps({'batches':44,'counts':dict(count)},ensure_ascii=False))
