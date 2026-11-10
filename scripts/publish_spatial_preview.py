"""Publish v002 review page and derived diagnostic frames from the rendered movie."""
import json,hashlib,subprocess,html,math
from pathlib import Path
from urllib.parse import quote
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1]
out=root/'后期/静帧配乐-v002'
plan_path=root/'镜头设计/shot-plan-v0.6.json'
plan=json.loads(plan_path.read_text(encoding='utf-8'));shots=plan['shots'];by={s['id']:s for s in shots}
movie=out/'穿云-全片静帧配乐-v002.mp4'
assert movie.exists()
record=json.loads((out/'粗剪记录.json').read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Metadata-only edits after render may update the plan hash only after verifying every render input.
assert record['duration']==plan['total_seconds']
assert len(record['shots'])==len(shots)
for a,s in zip(record['shots'],shots):
    assert (a['id'],a['start'],a['end'],a['image'],a['crop'])==(s['id'],s['start_second'],s['end_second'],s['presentation']['path'],s['panel_rect_pixels'])
    assert a['image_sha256']==sha(root/a['image'])
record['shot_plan_sha256']=sha(plan_path)
record['metadata_verified_against_render_inputs']=True
(out/'粗剪记录.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
chapters=[(by[id]['start_second'],label) for id,label in [('CY001','街市初见'),('CY004A','放碗与赶往宫殿'),('CY010A','空堂营救'),('CY016D','被发现与献祭'),('CY023','援军登场 · Victory'),('CY026A','邀约快闪'),('CY027A','条约对峙与交锋'),('CY027G','战后解锁与扶稳'),('CY031','数日后 · 再分一碗饭')]]
clock=lambda s:f'{int(s)//60:02d}:{int(s)%60:02d}'
buttons=''.join(f'<button data-time="{t}">{clock(t)}　{html.escape(name)}</button>' for t,name in chapters)
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>穿云 · 全片静帧配乐 v002</title><style>body{margin:0;background:#101319;color:#eee6dc;font:16px/1.7 system-ui,"Microsoft YaHei",sans-serif}main{max-width:1120px;margin:auto;padding:24px}h1{margin-bottom:5px}p{color:#bcb9b6}video{display:block;width:100%;max-height:76vh;background:#000}nav{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0}button,a{color:#f2e4ca}button{background:#252b36;border:1px solid #505561;border-radius:6px;padding:10px;cursor:pointer}a{margin-right:18px}#now{margin:10px 0;color:#ddc397}</style><main><h1>穿云 · 全片静帧配乐</h1><p>v002 · 3分59秒 · 69镜 · 空间与过渡修订 · BGM＋对白字幕</p><video id="film" controls playsinline preload="metadata" poster="预览.jpg" src="MOVIE"></video><div id="now">点击播放，或选择段落。</div><nav>BUTTONS</nav><p>本版补齐放碗赶路、被拽下、失守落地、沿通道入殿和最后腕扣；水盆、锁链、座位与救援站位重新核对。保留援军群像、战斗省略和结尾停顿。</p><p>仍为静帧试听，暂不含角色配音和动作音效。</p><a href="MOVIE" download>下载本版 MP4</a><a href="../../镜头设计/带图分镜.html">逐镜查看</a><a href="../静帧配乐-v001/试听.html">对照上一版</a><details><summary>音乐与修订记录</summary><p>首尾 Concerning Hobbits；宫殿至献祭 A Knife in the Dark；援军与对峙 Victory；召集与战后 Heart of Courage。换曲点随新镜头重新定位，破门仍对齐 Victory，回闪与结尾有短交叠。</p><a href="粗剪记录.json">剪辑记录</a><a href="../../镜头设计/生成记录/视觉与空间复核-v006.md">本轮空间复核</a></details></main><script>const v=document.getElementById('film');const chapters=CHAPTERS;document.querySelectorAll('[data-time]').forEach(b=>b.addEventListener('click',()=>{v.currentTime=Number(b.dataset.time);v.play().catch(()=>{})}));v.addEventListener('timeupdate',()=>{const c=chapters.filter(c=>c[0]<=v.currentTime).at(-1);document.getElementById('now').textContent=String(Math.floor(v.currentTime/60)).padStart(2,'0')+':'+String(Math.floor(v.currentTime%60)).padStart(2,'0')+' / 03:59　'+c[1]});</script></html>'''
page=page.replace('MOVIE',quote(movie.name)).replace('BUTTONS',buttons).replace('CHAPTERS',json.dumps(chapters,ensure_ascii=False))
(out/'试听.html').write_text(page,encoding='utf-8')
frames=out/'核验帧';frames.mkdir(exist_ok=True)
for s in shots:
    f=frames/(s['id']+'.jpg')
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(s['start_second']+s['seconds']/2),'-i',str(movie),'-frames:v','1','-vf','scale=480:270','-update','1',str(f)],check=True)
# Analysis contact sheets only; source illustrations and production frames remain unmodified.
for i in range(0,len(shots),36):
    group=shots[i:i+36];sheet=Image.new('RGB',(1920,300*math.ceil(len(group)/4)),(20,23,30));draw=ImageDraw.Draw(sheet)
    for j,s in enumerate(group):
        x=(j%4)*480;y=(j//4)*300
        sheet.paste(Image.open(frames/(s['id']+'.jpg')),(x,y))
        draw.text((x+8,y+277),f"{s['id']}  {clock(s['start_second'])} - {clock(s['end_second'])}",fill=(240,235,225))
    sheet.save(out/f'画面核验-{i//36+1}.jpg',quality=94)
subprocess.run(['ffmpeg','-v','error','-y','-ss',str(by['CY024']['start_second']+1),'-i',str(movie),'-frames:v','1','-update','1',str(out/'预览.jpg')],check=True)
print(json.dumps({'review_page':str(out/'试听.html'),'frames':len(shots),'chapters':chapters},ensure_ascii=False))
