"""Build a readable review entry for the timing revision, without changing audio."""
from html import escape
from prepare_generation_v021 import ROOT,FIX,OUT,SOURCE,load,n
def main():
 src=load(SOURCE);sm={s['id']:s for s in src['shots']};changes=load(FIX+'/重排明细.json');edit=load(FIX+'/实际BGM剪辑.json');plan=load(OUT+'/展开数据.json')
 def at(sid,label):return f'<a href="全片声音预览.html#t={sm[sid]["start_second"]}">{label}</a>'
 links=''.join(at(sid,label) for sid,label in [('CY008M','内心戏完整两句'),('CY016A','试锁后的对话'),('CY024K00','Kimi显形 → 请求 → 瞬移'),('CY024A','GPT咏唱与水龙'),('CY028A','问孩子 → 回答 → Claude咏唱'),('CY029E1','继续选择 → 星火触木'),('CY031','收尾与四秒留白')])
 rows=''.join(f'<tr><td>{escape(c["title"])}</td><td>{n(c["old_seconds"])}秒</td><td>{n(c["new_seconds"])}秒</td><td>{at(c["shot_id"],"连同画面试听")}</td></tr>' for c in changes['changed_shots'])
 music=''.join(f'<tr><td>{c["id"]}</td><td>{n(c["timeline_start"])}–{n(c["timeline_end"])}</td><td>{n(c["source_in"])}–{n(c["source_out"])}</td></tr>' for c in edit['cues'])
 page=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · 语音与音乐对位 v021</title><style>body{{max-width:1040px;margin:auto;padding:30px;background:#101820;color:#e6edf3;font:16px/1.8 system-ui,'Microsoft YaHei'}}h1{{font-size:34px}}a{{color:#a6d9d4}}nav,.jump{{display:flex;flex-wrap:wrap;gap:12px}}nav a,.jump a{{padding:9px 14px;border:1px solid #3b5866;border-radius:8px;text-decoration:none}}.box{{background:#1b2836;padding:18px 22px;margin:20px 0;border-radius:12px}}.numbers{{font-size:22px;color:#f1d6a3}}table{{width:100%;border-collapse:collapse}}td,th{{text-align:left;padding:10px;border-bottom:1px solid #334454}}.muted{{color:#b3bec9;font-size:14px}}</style>
<h1>让画面跟上新的日语配音</h1><p class="numbers">v021 · 133镜 · 8分03.22秒 · 63句 · 43批</p>
<nav><a href="../../视频制作/生成板-v021/生成板.html">打开最终生成板</a><a href="全片声音预览.html">播放完整试听</a><a href="../../00_打开项目.html">项目首页</a></nav>
<div class="box"><b>这次调整</b><p>沿用你刚调整的全部日语配音及当前画面。9个长句镜头延长；Claude起咏两镜按新版分句收紧，使上一句真实结束后恰好进入6秒父亲插话窗口。总长比旧版增加18.82秒，两个超长批次在安全镜间拆开。</p><p>63条完整新版干声各播放一次，不变速、不截尾。13段音乐按动作锚点重剪，46个动作点保留；音乐仍用原七首。Kimi落地改对同曲后一个已测瞬态候选，避免旧入点越过原曲开头。</p><p>保留4秒月光显形、6秒父亲插话、祈愿到术名0.8秒空窗，以及结尾4秒无BGM。短句后的动作和反应留白继续保留。</p></div>
<h2>从重点段落试听</h2><div class="jump">{links}</div>
<h2>镜长怎么变了</h2><table><thead><tr><th>镜头</th><th>原镜长</th><th>新镜长</th><th></th></tr></thead><tbody>{rows}</tbody></table>
<div class="box"><b>核验与边界</b><p>已核验：全部图片保持、63条完整音频各一次、语音无重叠、字幕/生成窗口/混音同源、音乐源区间有效、实际输出可解码、停乐区没有BGM泄漏。</p><p class="muted">本页为静帧＋实际新混音，尚未生成视频。音乐瞬态候选不冒充已听审的乐句重拍，逐字发音、乐句感受与动态口型需分别验收。</p><a href="验证结果.json">完整文件核验</a> · <a href="独立语音复核.md">独立语音复核</a> · <a href="独立配乐复核.md">独立配乐复核</a></div>
<details><summary>音乐剪辑区间（原曲原速，无整曲循环）</summary><table><tr><th>乐段</th><th>成片秒</th><th>原曲秒</th></tr>{music}</table></details></html>'''
 (ROOT/FIX/'修正交接.html').write_text(page,'utf-8')
 print('Published v021 review entry')
if __name__=='__main__':main()
