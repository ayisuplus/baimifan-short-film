"""Publish navigation for the verified subtitle synchronization."""
from pathlib import Path
import json,html,os
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'后期/对白字幕同步-v010'
p=json.loads((OUT/'同步计划.json').read_text(encoding='utf8'))
v=json.loads((OUT/'核验结果.json').read_text(encoding='utf8'))
assert v['saved'] and v['subtitle_text_and_frames_exact']
e=html.escape
def tc(f):
    f=int(f);return f'{f//86400:02}:{f//1440%60:02}:{f//24%60:02}:{f%24:02}'
cards=[]
for x,c in zip(p['lines'],p['subtitle_cues']):
    rel=Path(os.path.relpath(x['file'],OUT)).as_posix()
    cards.append(f'<article><small>{e(x["id"])} · {e(x["role"])} · {tc(c["start_frame"])}–{tc(c["end_frame_exclusive"])}</small><p>{e(c["ja"])}</p><p><b>{e(c["zh"])}</b></p><audio controls preload="none" src="{quote(rel)}"></audio></article>')
body='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · v010对白字幕同步</title><style>body{max-width:1080px;margin:32px auto;padding:0 24px;background:#111923;color:#e9edf3;font:16px/1.7 system-ui}a{color:#9bd4ff}section,article{background:#1b2734;padding:20px;border-radius:12px;margin:16px 0}small{color:#afc1d3}audio{width:100%;max-width:600px}</style><h1>《白米饭》对白与字幕同步 · v010</h1><section><p><b>v010_Dialogue_Subtitle_Sync</b> 已保存。54句原速配音，1条真实中文字幕轨，54条字幕逐字及逐帧读回一致。</p><p>开场“ありがとう…… / 谢谢你……”后移45帧至00:00:18:09，录音结束于19.655秒，字幕在19.667秒拍碗段切入时消失。短稿保留，不恢复已删“但我……”。这是对接拍碗段剪点，具体手掌接触帧和表演仍在后续画面审查中。</p><p>其他53句对白、123段画面、音乐音效以及旧v009保持不变。中文为显示字幕；日语SRT保留作校对。已在达芬奇界面抽查短句与中英文混排显示；不代表全片口型与最终表演通过。未导出成片或工程。</p><p>下方为逐句原声试听，不含工程混音；在达芬奇复看真实字幕和画面。</p><p><a href="修订说明.md">修订说明</a> · <a href="核验结果.json">实际核验</a> · <a href="白米饭-v010-中文.srt">中文字幕源</a> · <a href="白米饭-v010-日语校对.srt">日语校对源</a> · <a href="../../00_打开项目.html">项目首页</a></p></section>'''
body+=''.join(cards)+'''<script>document.addEventListener('play',e=>{if(e.target.tagName==='AUDIO')document.querySelectorAll('audio').forEach(a=>{if(a!==e.target)a.pause()})},true)</script></html>'''
(OUT/'工程内审阅.html').write_text(body,encoding='utf8')
print('v010 review: 54 cues')
