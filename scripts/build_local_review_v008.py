"""One current entrypoint; historical versions remain reachable and immutable."""
from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[1];O=R/'后期/局部收口-v008'
L=json.loads((O/'采用与问题台账.json').read_text(encoding='utf8'))
def esc(x):return html.escape(str(x))
style='body{max-width:1100px;margin:40px auto;padding:0 24px;background:#111923;color:#e9edf3;font:16px/1.7 system-ui}a{color:#9bd4ff}table{border-collapse:collapse;width:100%}th,td{padding:12px;text-align:left;border-bottom:1px solid #344454}h1{font-size:30px}section{margin:24px 0;padding:22px;background:#1b2734;border-radius:12px}.muted{color:#b5c3d2}button{padding:8px;cursor:pointer}code{color:#e8d49d}'
def tc(f):return f'{f//1440:02}:{f//24%60:02}:{f%24:02}'
timeline=L.get('working_timeline') or L['current_timeline']
body='<h1>白米饭 · 局部修复复看</h1><p>'+esc(L['status'])+'</p><section><strong>当前达芬奇时间线</strong><p><code>'+esc(timeline)+'</code> · 7分59秒01帧</p><p>Kimi现有段落保留；只修明确错误。正在使用不等于最终核定。未经作者最终核验并明确要求，不导出。</p></section>'
body+='<section><h2>本轮处理与待核验</h2><table><tr><th>位置</th><th>问题</th><th>状态</th></tr>'
for row in L['required']:
 body+='<tr><td>'+esc(row['id'])+'<br>'+tc(row['frames'][0])+'–'+tc(row['frames'][1])+'</td><td>'+esc(row['issue'])+'</td><td>'+esc(row['status'])+'</td></tr>'
body+='</table></section><section><h2>候选采用记录</h2><table><tr><th>候选</th><th>处置</th></tr>'
for c in L['candidates']:body+='<tr><td>'+esc(c['id'])+'</td><td>'+esc(c['status'])+'</td></tr>'
body+='</table></section><section><h2>验收边界</h2><ul>'
for k,v in L['acceptance'].items():body+='<li>'+esc(k)+'：'+('已核验' if v else '未最终通过')+'</li>'
body+='</ul><p>逐帧与声音电平检查不能替代连续听审。原选声保留；跨句音色及最终口型由工程内复看确认。</p><p><a href="采用与问题台账.json">采用与问题台账</a> · <a href="修订说明.md">修订说明</a> · <a href="../../00_打开项目.html">返回项目首页</a></p></section>'
doc='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>白米饭局部修复复看</title><style>'+style+'</style>'+body+'</html>'
(O/'工程内审阅.html').write_text(doc,encoding='utf8')
home='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>白米饭</title><style>'+style+'</style><h1>白米饭</h1><p>从一碗饭开始，回到一碗饭。</p><section><h2>当前作品</h2><p><code>'+esc(timeline)+'</code> · 7分59秒01帧</p><p>'+esc(L['status'])+'</p><p><a href="后期/局部收口-v008/工程内审阅.html">打开本轮修复与采用记录</a></p><p class="muted">在达芬奇中复看；这不是最终导出或作者验收通过版。</p></section><section><h2>制作资料</h2><p><a href="后期/制作工作台-v025/工作台.html">原制作工作台：镜头、台词与作者选声</a>（生成前基线，时码不代表当前剪辑）</p><p><a href="制作进度.md">制作进度</a></p></section><details><summary>历史版本与对照</summary>'
for url,name in [('后期/二维动漫纠偏-v005/工程内审阅.html','v005 原时间线与历史审查'),('后期/参考一致性复核-v006/对照审阅.html','原图一致性试验'),('后期/导演重构-v003/工程内审阅.html','v003 导演重构'),('后期/声画重构-v002/工程内审阅.html','v002 声画重构'),('后期/导演后期修正-v001/修订审阅.html','v001 早期修订'),('视频制作/Metaso-H3-v003/生成进度.html','早期回片工作台')]:home+='<p><a href="'+url+'">'+name+'</a></p>'
home+='</details></html>';(R/'00_打开项目.html').write_text(home,encoding='utf8')
print('One current entrypoint, history preserved')
