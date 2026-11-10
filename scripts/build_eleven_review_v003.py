from pathlib import Path
import json, html

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'声音/ElevenLabs-正式台词试听-v003'
entries=[]
old=ROOT/'声音/ElevenLabs-正式台词试听-v002'
claude=json.loads((old/'Claude-生成记录.json').read_text(encoding='utf8'))
entries.append({'role':'Claude','kind':'designed','note':'已确认候选 1；这是声线选择，逐句表演仍可再挑。','lines':[], 'previews':[{'candidate':x['index'],'file':'../ElevenLabs-正式台词试听-v002/'+x['file'],'seconds':float(x['media']['format']['duration'])} for x in claude['previews']]})
for role in ['GPT','Kimi','教主']:
    req=json.loads((OUT/f'{role}-输入.json').read_text(encoding='utf8'))
    result=json.loads((OUT/f'{role}-结果.json').read_text(encoding='utf8'))
    entries.append({'role':role,'kind':'designed','note':f'正式台词 {len(req["lines"])} 句。'+(f'为满足设计预览最低字数，原句重复 {req["repeats"]} 轮。' if req['repeats']>1 else '使用全部实际台词。'),'lines':req['lines'],'previews':[{'candidate':x['candidate'],'file':x['file'],'seconds':float(x['media']['format']['duration'])} for x in result['previews']]})
for role in ['千问','Gemini','Grok','天使GPT','恶魔GPT','教徒']:
    result=json.loads((OUT/f'{role}-直配结果.json').read_text(encoding='utf8'))
    entries.append({'role':role,'kind':'direct','note':'现成日语声线，一次提交；主结果直接审核，网页附送版本折叠保留。','voice':result['previews'][0]['history']['dialogue'][0]['voice_name'],'lines':result['lines'],'previews':[{'candidate':x['candidate'],'file':x['file'],'seconds':float(x['media']['format']['duration']),'model':x['history']['model_id']} for x in result['previews']]})
entries.append({'role':'小鱼','kind':'retained','note':'按作者决定暂时保留现有声音，本轮未重新生成。','lines':[],'previews':[]})
(OUT/'试听数据.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf8')
cards=[]
for e in entries:
    role=e['role']; previews=[]
    for p in e['previews']:
        f=html.escape(p['file'],quote=True);i=p['candidate']; label=f'候选 {i}' if e['kind']=='designed' else ('主结果' if i==1 else '网页附送备用')
        a=f'<article><h3>{label} <small>{p["seconds"]:.1f} 秒</small></h3><audio controls preload="metadata" src="{f}"></audio><p><a href="{f}" download>下载原音频</a></p><button data-role="{role}" data-candidate="{i}" onclick="saveChoice(this.dataset.role,Number(this.dataset.candidate))">'+('选这版声线' if e['kind']=='designed' else '这版可用')+'</button></article>'
        if e['kind']=='direct' and i>1:a='<details><summary>附送备用 · 不必额外挑选</summary>'+a+'</details>'
        previews.append(a)
    rows=''.join('<tr><td>'+html.escape(x['ja'])+'</td><td>'+html.escape(x['zh_back_translation'])+'</td></tr>' for x in e['lines'])
    controls='' if e['kind']=='retained' else f'<label>备注<input id="note-{role}" placeholder="例如：声音可以，咏唱需更干脆"></label><button class="secondary" onclick="saveChoice(\'{role}\',0)">需要调整</button>'
    cards.append(f'<section id="{role}"><h2>{role}</h2><p>{html.escape(e["note"])}</p><p class="status" id="status-{role}"></p>'+('<p>声库：'+html.escape(e['voice'])+'</p>' if e.get('voice') else '')+'<div class="grid">'+''.join(previews)+'</div>'+controls+('<details><summary>日语台词与中文回译</summary><table>'+rows+'</table></details>' if rows else '')+'</section>')
data=json.dumps(entries,ensure_ascii=False).replace('</','<\\/')
choices=(OUT/'作者选择.json').read_text(encoding='utf8').replace('</','<\\/')
page='''<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>白米饭 · 全角色声线与短句试听</title><style>body{max-width:1180px;margin:32px auto;padding:0 24px;background:#121923;color:#eef4ff;font:16px/1.7 system-ui}h1{font-size:28px}h2{margin-top:0}h3{font-size:17px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}section{background:#1c2737;border-radius:15px;padding:24px;margin:24px 0}article{padding:16px;background:#27364c;border-radius:10px}audio{width:100%}button{cursor:pointer;background:#b8d8ff;color:#122136;border:0;border-radius:8px;padding:10px 16px;font:inherit}.secondary{background:#354660;color:#eef4ff;margin:12px}a{color:#abd5ff}small{font-weight:400;color:#c1ccdd}input{padding:9px;width:min(440px,70%);margin:15px;border:1px solid #566984;border-radius:8px;background:#121923;color:white;font:inherit}td{padding:8px;border-bottom:1px solid #3c4b62}details{margin:16px 0}.status{color:#9ee6c4;font-weight:600}.bar{position:sticky;top:0;background:#121923ee;padding:12px 0;z-index:5}.bar a{margin-right:15px}#notice{color:#ffe1a2}</style><h1>白米饭 · 全角色声线与短句试听</h1><p>Claude 已选候选 1；小鱼保留现有声音。GPT、Kimi、教主挑声线，其余短句直接审核。所有音频均为原速原文件，尚未替换正片。</p><div class="bar"><button onclick="exportChoices()">导出全部选择</button> <span id="notice">正在连接本地保存…</span></div><nav>'''+''.join(f'<a href="#{e["role"]}">{e["role"]}</a>　' for e in entries)+'</nav>'+''.join(cards)+'''<p>结构与解码核验不等于读音、情绪或最终听审通过。你可选声线、标记需要调整并写备注。</p><script>const entries='''+data+';let choices='+choices+''';let online=false;const endpoint='/api/voice-choice-v003';function render(){for(const e of entries){const c=choices[e.role];document.getElementById('status-'+e.role).textContent=!c?'待审核':c.status==='retain_existing_voice'?'已确认：保留现有声音':c.candidate===0?'已标记：需要调整':'已选：候选 '+c.candidate;const n=document.getElementById('note-'+e.role);if(n&&c?.note)n.value=c.note}}async function saveChoice(role,candidate){const note=document.getElementById('note-'+role)?.value||'';const payload={role,candidate,note};try{if(!online)throw new Error('未连接保存服务');const r=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});if(!r.ok)throw new Error('保存失败');choices=await r.json();document.getElementById('notice').textContent='已保存到项目：'+role;render()}catch(e){choices[role]={candidate,note,status:'local_unsaved'};localStorage.setItem('baimifan-voices-v003-unsaved',JSON.stringify(choices));document.getElementById('notice').textContent='仅保存在浏览器，请点“导出全部选择”交回';render()}}function exportChoices(){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(choices,null,2)],{type:'application/json'}));a.download='白米饭-全角色声线选择-v003.json';a.click()}async function init(){render();if(location.protocol==='file:'){document.getElementById('notice').textContent='本地文件模式：选后请导出选择';return}try{const r=await fetch(endpoint);if(!r.ok)throw 0;choices=await r.json();online=true;render();document.getElementById('notice').textContent='点击选择后自动写入项目'}catch(e){document.getElementById('notice').textContent='保存服务未连接：可导出选择'}}document.querySelectorAll('audio').forEach(a=>a.addEventListener('play',()=>document.querySelectorAll('audio').forEach(b=>{if(a!==b)b.pause()})));init();</script></html>'''
page=page[:page.index('<script>')]+'<script>const entries='+data+';let choices='+choices+';</script><script src="备注保存.js"></script></html>'
for e in entries:
    if e['kind']!='retained':
        role=e['role']
        page=page.replace(f'id="note-{role}"',f'aria-label="{role}备注" id="note-{role}"')
        marker=f'<button class="secondary" onclick="saveChoice(\'{role}\',0)">'
        page=page.replace(marker,f'<button onclick="saveChoice(\'{role}\')">保存备注</button>'+marker)
(OUT/'试听.html').write_text(page,encoding='utf8')
print(json.dumps({'roles':len(entries),'audio_files':sum(len(x['previews']) for x in entries)},ensure_ascii=False))
