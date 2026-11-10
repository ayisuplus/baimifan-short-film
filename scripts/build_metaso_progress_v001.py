"""Verify downloaded candidates and render the cross-provider review page."""
from pathlib import Path
import html, json, os, subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '视频制作/Metaso-H3-v001'
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def save(path, value): path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
q = read(OUT/'执行队列.json')
for b in q['items']:
    if b['status'] != 'downloaded_candidate': continue
    path = ROOT / b['local_path']
    probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],encoding='utf-8'))
    result = subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(path),'-f','null','-'],capture_output=True,text=True)
    assert result.returncode == 0 and not result.stderr, result.stderr
    sheet = OUT/'审查'/(b['batch_id']+'-半秒采样.jpg')
    sheet.parent.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg','-hide_banner','-v','error','-y','-i',str(path),'-vf','fps=2,scale=320:-1,tile=5x6','-frames:v','1',str(sheet)],check=True)
    b.update(status='generated_candidate',actual_duration=float(probe['format']['duration']),decode='passed',probe=probe,review='文件完整解码通过，视听与口型待审；未替换最终日语配音与BGM。')
save(OUT/'执行队列.json',q)
prior=read(ROOT/'视频制作/LibTV-H3-v001/H3节约余量执行队列.json')['items']
allitems=[dict(b,provider='LibTV') for b in prior if b['status']=='generated_candidate'] + [dict(b,provider='Metaso') for b in q['items']]
cards=[]
for b in sorted(allitems,key=lambda x:x['batch_number']):
    title=html.escape(f"第{b['batch_number']}批 · {b['title']}")
    if b.get('local_path'):
        src=Path(os.path.relpath(ROOT/b['local_path'],OUT)).as_posix()
        player=f'<video controls playsinline muted preload="metadata" src="{html.escape(src)}"></video>'
        detail=html.escape(b.get('review','待审片'))
    else:
        player=''
        detail='生成中' if b['status']=='running' else html.escape(b['status'])
    badge='需返修' if b.get('quality_status')=='needs_rework' else '候选待审'
    cards.append(f'<article id="{b["batch_id"]}"><small>{b["provider"]} · {badge}</small><h2>{title}</h2>{player}<p>{detail}</p></article>')
done=sum(b['status']=='generated_candidate' for b in q['items'])
running=sum(b['status']=='running' for b in q['items'])
balance=q.get('observed_final_balance',q['observed_initial_balance'])
balance_label='回读余额' if 'observed_final_balance' in q else '提交前余额'
page=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · H3回片工作台</title>
<style>body{{background:#10141d;color:#e7ebf4;font:16px/1.6 system-ui;margin:0}}main{{max-width:1160px;margin:auto;padding:30px 24px}}h1{{margin:0}}h2{{font-size:20px}}p,small{{color:#b8c3d9}}a{{color:#8fcaff}}header,article{{background:#1b2535;padding:22px;border-radius:14px}}header{{margin-bottom:24px}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}}video{{width:100%;background:#000}}@media(max-width:760px){{.grid{{grid-template-columns:1fr}}}}</style>
<main><header><small>白米饭 / 当前执行服务：Metaso MiniMax H3</small><h1>{23+done} 批候选已回片</h1><p>LibTV 23批保留；Metaso新增 {done} 批，运行中 {running} 批。{balance_label} {balance} 积分，本轮7批余额减少755.1积分。</p><p>768P普通通道；Context IR关闭。原声尚未替换为已选日语配音和最终BGM。第13、21、31批需返修；第8批平台失败、另13批参考超限尚未提交。</p><a href="#GB022-1">查看本轮新增7批</a> · <a href="../../后期/制作工作台-v025/工作台.html">制作工作台</a> · <a href="../LibTV-H3-v001/生成进度.html">LibTV历史回片</a> · <a href="接入说明.md">API接入记录</a></header><div class="grid">{''.join(cards)}</div></main><script>document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(x=>{{if(x!==v)x.pause()}})));</script></html>'''
(OUT/'生成进度.html').write_text(page,encoding='utf-8')
print(json.dumps({'metaso_completed':done,'running':running,'total_completed':23+done}))
