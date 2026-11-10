"""Build a local candidate review page from verified LibTV receipts; never submits tasks."""
from pathlib import Path
import json
import html

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '视频制作/LibTV-H3-v001'
def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))
def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

queue = read('H3节约余量执行队列.json')
nodes = {n['id']: n for n in read('最终画布回读.json')}
verified = read('已交付视频核验.json')
reviews = {
 'GB001': '半秒采样：四镜结构与角色外观基本保持，递饭动作可见。切点与计划存在偏移，未验收口型。',
 'GB002': '半秒采样：Claude特写、掀饭、告知与转身跑开均可见。掀饭力度与衔接需连续观看确认，未验收口型。',
 'GB003': '半秒采样：冷蓝紫暮色与长阶纵深保持，入门和内殿可见。守卫初始交叉枪动作、末镜是否及时停下需专项复核；切点略偏移。',
 'GB004': '半秒采样：求救、GPT卧榻回应、小鱼追问三段可见。尚未对照最终干声检查口型与表演节奏。',
}
cards = []
batch_order = {b['batch_id']: b['batch_number'] for b in queue['items']}
for media in sorted(verified, key=lambda m: batch_order[Path(m['file']).name.split('-H3-')[0]]):
    bid = Path(media['file']).name.split('-H3-')[0]
    batch = next(b for b in queue['items'] if b['batch_id'] == bid)
    node = nodes[batch['node_id']]
    assert node['data']['taskInfo']['status'] == 2
    stream = next(s for s in media['probe']['streams'] if s['codec_type'] == 'video')
    duration = float(media['probe']['format']['duration'])
    batch.update(status='generated_candidate', task_id=node['data']['taskInfo']['taskId'],
                 local_path=media['file'], sha256=media['sha256'], actual_duration=duration,
                 review=reviews.get(bid, batch.get('review','待视听审片。')), accepted=False)
    video = '产物/' + Path(media['file']).name
    title = f"第{batch['batch_number']}批 · {batch['title']}"
    cards.append(f'''<article id="{bid}"><header><span class="badge">{'需返修 · 内容问题' if batch.get('quality_status')=='needs_rework' else '候选 · 待审片'}</span><h2>{html.escape(title)}</h2>
      <p>MiniMax H3 · {stream['width']} × {stream['height']} · 实际 {duration:.3f} 秒 · 报价 {batch['estimated_credits']} 积分</p></header>
      <video controls playsinline preload="metadata" muted src="{video}"></video>
      <p>{html.escape(reviews.get(bid, batch.get('review','待视听审片。')))}</p>
      <div class="links"><a href="{video}" download>保存原视频</a><a href="审查/{bid}-半秒采样.jpg">查看采样图</a>
      <a href="../../后期/制作工作台-v025/工作台.html#t={batch['film_start']}">回到对应工作台画面</a></div>
      <details><summary>任务与文件核验</summary><p>任务 {batch['task_id']}<br>SHA256 {media['sha256']}<br>文件完整解码通过；半秒图片采样不等于完整视听、口型或采用验收。</p></details></article>''')

queue['execution_status'] = queue.get('execution_status', 'generating')
write('H3节约余量执行队列.json', queue)
old = read('H3执行队列.json')
for batch in (old if isinstance(old, list) else old.get('items', [])):
    latest = next((b for b in queue['items'] if b['batch_number'] == batch['batch_number']), None)
    if latest and latest['status'] == 'generated_candidate':
        batch.update({k:latest[k] for k in ('status','node_id','task_id','local_path','sha256','actual_duration')})
if isinstance(old, dict):
    old['execution_queue'] = 'H3节约余量执行队列.json'
write('H3执行队列.json', old)
incident = read('GB003-重复提交异常.json')
incident.update(final_node_task='20261028001103732479236', observed_balance_after_cancel=2769,
                refund='Cancellation dialog warned no refund; later observed balance recovered to2769. Final charge/refund not verified against transaction ledger. Do not claim154 confirmed net loss.')
write('GB003-重复提交异常.json', incident)

pending = ''.join(f"<tr><td>第{b['batch_number']}批</td><td>{html.escape(b['title'])}</td><td>{html.escape('生成中' if b['status']=='running' else ('平台失败，已记录' if b['status'].startswith('failed') else '未提交'))}</td><td>{b['duration']}秒 / 预计{b['estimated_credits']}积分</td></tr>" for b in queue['items'] if b['status'] != 'generated_candidate')
page = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · H3回片审阅</title>
<style>body{margin:0;background:#10141d;color:#e7ebf4;font:16px/1.6 system-ui,sans-serif}main{max-width:1160px;margin:auto;padding:36px 24px}h1{font-size:32px;margin:4px 0}h2{font-size:21px;margin:6px 0}p{color:#b8c3d9}a{color:#8fcaff}a:hover{color:white}.intro,.notice{padding:20px 24px;background:#1a2435;border-radius:14px;margin-bottom:22px}.notice{border-left:4px solid #e3ac5b}nav{display:flex;gap:20px;flex-wrap:wrap}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}article{background:#1b2230;padding:20px;border-radius:16px;overflow:hidden}video{width:100%;background:black;border-radius:8px}.badge{color:#f1ce8c;font-size:13px}.links{display:flex;gap:18px;flex-wrap:wrap;font-size:14px}details{margin-top:16px;font-size:13px;overflow-wrap:anywhere}table{width:100%;border-collapse:collapse;font-size:14px}td,th{text-align:left;padding:10px;border-bottom:1px solid #344056}@media(max-width:760px){.grid{grid-template-columns:1fr}main{padding:20px 12px}}button{cursor:pointer;background:#344b70;color:white;border:0;border-radius:8px;padding:10px 16px}</style>
<main><div class="intro"><small>白米饭 / 生成执行 v001 / 2026-10-28</small><h1>__COUNT__ 批 H3 候选已回片</h1><p>原文件已保存，完整解码通过。点击视频可播放；默认静音，打开声音听到的是模型原生声，尚未替换为已选日语配音与最终BGM。</p><nav><a href="../../后期/制作工作台-v025/工作台.html">返回制作工作台</a><a href="#pending">查看未提交批次</a><a href="执行记录.md">执行与异常记录</a></nav></div>
<div class="notice"><b>本轮额度已用至不足下一批</b><p>本轮已停止提交，原视频与任务记录均已保存；模型原声暂未替换。已完成 __COUNT__ 批，运行中 __RUNNING__ 批。当前状态：__STATE__。<a href="#GB011-1">第13批需返修</a> · <a href="#GB016-1">第21批需返修</a> · <a href="#GB005">第6批裁切评估</a>。历史第三批误提交已取消，原片保留，详情见执行记录。</p></div>
<div class="grid">''' + ''.join(cards) + '''</div><section id="pending"><h2>H3 待提交队列</h2><p>下表区分生成中、失败与未提交；金额为各批请求报价，失败返还以平台余额为准。另有13批原规划Seedance，未调用。</p><table><thead><tr><th>批次</th><th>内容</th><th>状态</th><th>请求量</th></tr></thead><tbody>''' + pending + '''</tbody></table></section></main><script>document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(x=>{if(x!==v)x.pause()})));</script></html>'''
page=page.replace('__COUNT__',str(len(cards))).replace('__RUNNING__',str(sum(b['status']=='running' for b in queue['items']))).replace('__STATE__',html.escape(queue.get('execution_status','generating')))
(OUT / '生成进度.html').write_text(page,encoding='utf-8')
print('Built',len(cards),'verified local video cards.')
