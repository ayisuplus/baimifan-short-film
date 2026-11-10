from pathlib import Path
import json,html,os
R=Path(__file__).resolve().parents[1];O=R/'视频制作/Metaso-H3-v006';q=json.loads((O/'执行队列.json').read_text(encoding='utf8'))
parts=['<!doctype html><meta charset="utf-8"><title>v006局部补拍输入</title><style>body{max-width:1100px;margin:30px auto;font:18px/1.7 system-ui}pre{white-space:pre-wrap}img{max-width:32%}article{border-bottom:1px solid #bbb;padding:20px}</style><h1>导演重构 · 局部补拍输入 v006</h1><p>MiniMax H3，768P，普通通道，关闭Context IR；只补列明镜头，原素材保留，回片复核后再接入。</p>']
for b in q['items']:
 parts.append(f'<article><h2>第{b["batch_number"]}批 · {b["attempt_id"]}</h2><p>{b["duration"]}秒 · 预计{b["estimated_credits"]:.1f}积分 · {html.escape(b["status"])}</p>')
 for r in b['references']:
  rel=os.path.relpath(R/r['path'],O).replace('\\','/');parts.append(('<audio controls src="'+html.escape(rel)+'"></audio>') if r['role']=='reference_audio' else '<img src="'+html.escape(rel)+'">')
 parts.append('<pre>'+html.escape(b['prompt'])+'</pre><pre>'+html.escape(json.dumps(b['references'],ensure_ascii=False,indent=2))+'</pre></article>')
(O/'补拍输入.html').write_text(''.join(parts),encoding='utf8')
print('Input view updated:',len(q['items']))
