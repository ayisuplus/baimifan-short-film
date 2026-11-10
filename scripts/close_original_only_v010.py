from pathlib import Path
import json, subprocess, hashlib, html

R = Path(__file__).resolve().parents[1]
D = R / '后期/参考一致性复核-v006'
G = R / '视频制作/Metaso-H3-v010'
def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
q = json.loads((G/'执行队列.json').read_text(encoding='utf8'))
x = q['items'][0]
assert x['status'] == 'downloaded_candidate'
video = R / x['local_path']
assert hashlib.sha256(video.read_bytes()).hexdigest() == x['sha256']
probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],encoding='utf8'))
decode = subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],capture_output=True,text=True)
assert decode.returncode == 0 and not decode.stderr.strip(), decode.stderr
v = next(s for s in probe['streams'] if s['codec_type']=='video')
record = dict(status='单镜试验回片，场景改善；画风与动作未最终通过，待作者比较',
    author_rejected_timeline='v005_2D_Anime_Fixes', timeline_modified=False,
    attempt_id=x['attempt_id'], task_id=x['task_id'], visual_references=1, turnarounds=0,
    reference=x['references'][0]['path'], sha256=x['sha256'],
    technical=dict(full_decode=True,width=v['width'],height=v['height'],fps=v['r_frame_rate'],video_duration=v.get('duration'),container_duration=probe['format']['duration']),
    observations=['九人、满月、冷蓝夜景、湿地反射与原入口轴线恢复','比v009忠实原分镜，细腻分层画法恢复'],
    remaining=['人物体积光和材质仍偏重；没有宣告二维画风通过','队伍后段趋于定势，指令到千问实际保护的交接仍需后续镜头承担','未验收逐音素口型及全片连续视听'],
    cause='上一轮v009已不传四视图，但引用了漂移回片的重绘稿；本次同时还原原分镜与修改提示，不能证明四视图是原因。实看GPT与千问卡是二维描线插画。',
    estimated_credits=51,billing_verified=False,new_final_export=False)
save(D/'作者纠偏与试验.json',record)
x['review_decision']='待作者比较，不装入时间线'
x['review_report']='后期/参考一致性复核-v006/作者纠偏与试验.json'
save(G/'执行队列.json',q)
old = R/'后期/二维动漫纠偏-v005/验证结果.json'
data=json.loads(old.read_text(encoding='utf8'))
data['historical_status_before_author_review']=data['status']
data['status']='作者已否定场景/画风一致性；原工程结构核验仅作技术记录，不代表视觉通过'
data['latest_review']='后期/参考一致性复核-v006/作者纠偏与试验.json'
save(old,data)
page=R/'后期/二维动漫纠偏-v005/工程内审阅.html'
s=page.read_text(encoding='utf8')
warning='<aside style="border:2px solid #ef9a68;padding:18px"><b>2026-10-28 作者纠偏：此版场景与画风未通过。</b> 以下为历史技术与修订记录，不代表视觉验收。<a href="../参考一致性复核-v006/对照审阅.html">查看原图、旧版与不传四视图试验</a>。新试片尚未替换达芬奇。</aside>'
s=s.replace('</style>','</style>'+warning,1)
page.write_text(s,encoding='utf8')
original=x['references'][0]['path']
oldref='视频制作/Metaso-H3-v009/参考/group-2d-keyframe.png'
content=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>白米饭 · 原图与无四视图试验</title>
<style>body{{margin:30px auto;max-width:1500px;padding:20px;background:#111722;color:#eee;font:18px/1.7 system-ui}}a{{color:#9bcaff}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(370px,1fr));gap:20px}}img,video{{width:100%}}article{{background:#202b3a;padding:16px;border-radius:10px}}.note{{color:#ffd19a}}video{{max-height:78vh}}summary{{cursor:pointer}}pre{{white-space:pre-wrap}}</style>
<h1>第17批 · 原分镜单图试验</h1><p class="note">只传当前分镜原图＋原选配音。无人物四视图、无重绘图、无回片参考。Metaso H3 单次5秒，预计51积分，账单未核验。尚未采用，未改达芬奇。</p>
<div class="grid"><article><h2>原分镜：本次唯一视觉输入</h2><img src="../../{original}"><p>九人、满月、蓝色夜景、湿地反光；精细线条与分层上色。</p></article>
<article><h2>上一版重绘输入：已拒用</h2><img src="../../{oldref}"><p>误改成白昼、八人、干地；画法也被压平。输入已偏离原图，不能继续用它修复。</p></article>
<article><h2>本次回片：2秒实帧</h2><img src="证据/B17-v010-2s.png"><p>人数与夜景恢复。人物体积光、材质仍偏重，不能直接判为画风通过。</p></article></div>
<h2>播放实际回片</h2><video controls preload="metadata" playsinline src="../../{x['local_path']}"></video><p>这是生成器实际返回的试片，附带声音不代表最终混音。画面约5秒，容器约5.175秒；完整解码和哈希已核验。</p>
<h2>本次结论</h2><p>原图匹配明显改善，可以比较；未通过最终采用。队伍动作后段仍偏定势，口型与连续动作尚未验收。原片音轨和工程均保留。</p>
<p>不能据此认定四视图是3D污染源：上一版补拍已没传四视图，本次还换回原图并调整了提示。实看GPT与千问四视图有明确二维描线。已经证实的问题是沿用漂移回片重绘，导致场景和画风错误延续。</p>
<p><a href="试验复核.json">独立试验复核</a> · <a href="后段独立复核.json">第17、25、37批原图比对</a> · <a href="作者纠偏与试验.json">状态与技术记录</a></p>
<details><summary>查看实际提示词</summary><pre>{html.escape(x['prompt'])}</pre></details></html>'''
(D/'对照审阅.html').write_text(content,encoding='utf8')
prefix='''## 2026-10-28：作者否定 v005 场景与画风；原图单参考试验待比较

v005 的场景/画风一致性已被作者否定，历史结构核验不代表视觉通过。第17批已按作者要求试一次不传人物四视图：仅当前 CY024 原分镜与原选声，Metaso H3 5秒（预计51积分、账单未核验），九人/月夜/湿地恢复，但画风与动作未最终通过。试片尚未装入达芬奇，也未导出成片。

当前入口：[原图/旧版/试片对照](后期/参考一致性复核-v006/对照审阅.html)。实看 GPT 与千问四视图有二维描线，不能断言其为3D污染源；上一轮已无四视图却沿用漂移回片重绘。本试验同时还原原图与改提示，不能作单变量因果结论。此单镜依作者指令豁免四视图；其他历史生成规则不据此批量改写。原镜头、声音、时间线和历史候选保留；待作者比较后再扩展修正。以下均为历史记录。

'''
for name in ['AGENTS.md','制作进度.md']:
    p=R/name
    p.write_text(prefix+p.read_text(encoding='utf8'),encoding='utf8')
    # Index only this turn's prefix, retaining unrelated worktree edits.
    base=subprocess.check_output(['git','show','HEAD:'+name],cwd=R).decode('utf8')
    oid=subprocess.check_output(['git','hash-object','-w','--stdin'],input=(prefix+base).encode('utf8'),cwd=R).decode().strip()
    subprocess.run(['git','update-index','--add','--cacheinfo','100644',oid,name],cwd=R,check=True)
print(json.dumps(record,ensure_ascii=False))
