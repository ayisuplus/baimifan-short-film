from pathlib import Path
import json,html,hashlib,subprocess,re
R=Path(__file__).resolve().parents[1];O=R/'后期/二维动漫纠偏-v005'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def tc(f):return f'{f//86400:02}:{f//1440%60:02}:{f//24%60:02}:{f%24:02}'
p=read(O/'后期执行计划.json');a=read(O/'实际装配回读.json')['result'];final=read(O/'最终实际核验.json')['result']
assert a['audio_unchanged'] and final['audio_unchanged'] and a['save'] and final['save']
assert len(p['edl'])==len(a['video'])==final['clips']==121 and a['frames']==p['frames']==11497
assert a['audio_count']==85 and len(a['audio_tracks'])==8 and all(t['enabled'] for t in a['audio_tracks'])
for s,v in zip(p['edl'],a['video']):
 assert s['name']==v['name'] and s['record']==v['start'] and s['frames']==v['end']-v['start'] and Path(s['source'])==Path(v['path'])
 assert v['enabled'] and abs(s['in']-v['source_in'])<=1 and abs(s['out']-v['source_out'])<=1
for v in final['replacements']:
 s=next(s for s in p['edl'] if s['name']==v['name']);assert [s['in'],s['out']]==[v['source_in'],v['source_out']]
 for k,val in s['props'].items():assert abs(val-v['props'][k])<.0001
used={Path(s['source']).stem for s in p['edl']};spend={}
for version in ['v007','v008','v009']:
 path=R/f'视频制作/Metaso-H3-{version}/执行队列.json';q=read(path);spend[version]=round(sum(x['estimated_credits'] for x in q['items']),1)
 for x in q['items']:
  assert x['status']=='downloaded_candidate'
  if x['attempt_id'] in used:
   x['review_decision']='selected_ranges_v005_pending_author';x['adopted_ranges']=[dict(timeline_frames=[s['record'],s['record']+s['frames']],source_frames=[s['in'],s['out']],speed=s['speed']) for s in p['edl'] if Path(s['source']).stem==x['attempt_id']]
  elif x.get('review_decision')!='rejected':
   x.update(review_decision='superseded_style_rework',review_reason='原候选保留作历史；当前v005使用真正二维重绘输入生成的v009局部。不得根据旧提示词再执行。')
 save(path,q)
verify=dict(status='截图范围二维纠偏及工程结构已核验，待作者核定',timeline=p['timeline'],frames=11497,video_clips=121,selected_voice_cues=63,voice_pieces=64,music_segments=17,audio_items=85,enabled_audio_tracks=8,audio_exactly_matches_v004=True,replaced_style_windows=4,replacement_segments=7,video_decode='4条v009完整解码及哈希通过',source_and_native_frames='四处7段原速，源区间/位置/裁切值回读一致；其他段沿用原计划',author_b12_cut_preserved=True,old_timelines_preserved=['v003_Dramatic_Reconstruction','v004_Screenshot_2D_Style_Rework'],new_video_or_project_exported=False,cost_estimates=spend,total_estimated_h3_credits=round(sum(spend.values()),1),billing_verified=False,image_generation='内置imagegen重绘4张关键帧；未纳入H3积分估算',remaining=['日语逐音素精度及全片连续听审未完成','展翼0.75秒翼膜插镜放大后略软；闭口尾有约10帧时间跳跃，待作者观感核验','只修作者截图范围及接点；其余同类问题待作者核定后再查'],preview_server='8968未运行；此前启动被自动审批策略阻止，未另起服务绕过')
save(O/'验证结果.json',verify)
rows=[('第5–6批：内心争执与决定',1282,'恶魔/天使分开表演；小鱼说完接原来正确离开方向，保留上一轮定点修法。'),('第7批：入洞过渡',2126,'新增二维重绘动画：手膝承重、前移、抬眼；48帧原速接回大厅。'),('第12–14批：教主与Claude',3478,'保留按作者选声重拍、闭口尾及说话者对应的修法；作者删20帧不回填。'),('第17批：群像入场',4778,'二维群像迈入、踩稳，伙伴抬武器警戒；删除建模候选。'),('第18批：Kimi窗外',4922,'保留凝形→请门→银刃近景→投刃→下一镜破窗；提前破窗候选不用。'),('第25批：GPT展翼',6476,'二维蓄力、振翼、离地。翼膜特写避开提前张嘴；原速有声段接闭口余势。'),('第37批：阶上阶下',9699,'二维肩后空间桥保留四人上下关系；Claude先看孩子，千问和小鱼反应。')]
notes=['# 《白米饭》截图修正与二维动漫纠偏 v005','',f'达芬奇当前：`{p["timeline"]}`。121段、11497帧（7分59秒01帧）。这是截图范围的复看候选，待作者核定。','','此前把“高细节二次元三维渲染”写入补拍提示词是错误方向。只增加二维文字仍让旧CG参考主导，因此v008不作当前采用。现用内置imagegen先重绘4张真正二维关键帧，再交给原Metaso H3生成动画，并检查实际连续帧中的画风和表演。','','|位置|达芬奇回看时码|本轮状态|','|---|---|---|']
notes += [f'|{title}|{tc(frame)}|{desc}|' for title,frame,desc in rows]
notes+=['','声音：85个音频片段与v004逐项完全一致，保留63句作者选声（64片段）、17段BGM和8条启用声音轨。相对v003仅沿用此前小鱼决定句后移7帧与局部拟音对位。没有换音色、重新生成对白或移动音乐。','','验证：4条v009全长解码、哈希、实际回片独立抽帧复核；7个替换片段源区间/位置/裁切值经达芬奇读回核对。翼膜近景实际预览的顶部细黑边已修正。抽帧与工程结构不等于日语逐音素和全片连续听审已通过。','','复看细项：翼膜和Kimi银刃特写放大后略软；展翼闭口尾有小幅时间跳跃；Kimi窗面月形光效仍需作者核定。先验收这些截图，再查其余同类问题。','',f'费用记录：v007截图补拍预计{spend["v007"]}积分；v008二维文字纠偏未采用预计{spend["v008"]}；v009真正二维关键帧驱动预计{spend["v009"]}。合计H3预计{round(sum(spend.values()),1)}积分，未核实际账单。全部20次H3任务已回片，无在途，失败/替代候选均保留。4张内置imagegen费用不包含在上述H3估算。','','没有新成片、DRP或DRT导出；本轮仅抓工程核验静帧。预览服务8968启动曾被自动审批策略阻止（返回blocked by policy），当前从达芬奇复看；没有绕过限制启动其他服务。']
(O/'修订说明.md').write_text('\n'.join(notes)+'\n',encoding='utf8')
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>白米饭 · 二维动漫纠偏v005</title><style>body{font:18px/1.7 system-ui;max-width:1100px;margin:40px auto;background:#111822;color:#e6ebf4;padding:0 20px}a{color:#9ccaff}td,th{padding:12px;text-align:left;border-bottom:1px solid #334155}code{color:#ffd69b}img{width:100%}article{margin:30px 0}button{background:#26384b;color:#eef;padding:8px;border:1px solid #6083a3;border-radius:5px}.note{color:#ffdaa5}</style><h1>《白米饭》二维动漫纠偏 v005</h1><p class="note">截图范围复看候选 · 尚未最终验收 · 未导出成片/工程</p><p>请在达芬奇复看 <code>v005_2D_Anime_Fixes</code>，当前停在群像入场。7分59秒01帧，原配音/BGM/音效位置保持。你核定这些后，再检查其他同类问题。</p><p>这次先重绘四张二维关键帧，再由H3生成实际角色表演。明确排除3D模型、塑料手办质感，以及静图推拉或皮影式漫剧动作。旧候选保留作对照，不是当前采用。</p><table><tr><th>镜头</th><th>回看时码</th><th>处理</th></tr>'
page+=''.join('<tr><td>'+html.escape(title)+'</td><td><button onclick="navigator.clipboard.writeText(\''+tc(frame)+'\')">'+tc(frame)+'</button></td><td>'+html.escape(desc)+'</td></tr>' for title,frame,desc in rows)+'</table>'
for title,filename in [('入洞：手膝承重后抬眼','native-inside'),('入场：迈入并警戒','native-group'),('展翼：二维翼膜与衣料','native-wing-face'),('阶梯：四人上下关系','native-stairs')]:page+='<article><h2>'+title+'</h2><img src="证据/'+filename+'.png"><p>当前达芬奇时间线核验静帧，动作请在工程内播放复看。</p></article>'
page+='<p class="note">仍需复看：翼膜与银刃近景略软；展翼闭口尾的接头；Kimi窗面的月形光效。逐音素口型和全片连续听感未冒称通过。</p><p><a href="修订说明.md">修订说明与完整费用记录</a> · <a href="验证结果.json">工程验证</a> · <a href="../../视频制作/Metaso-H3-v009/补拍输入.html">本轮二维输入</a></p></html>'
(O/'工程内审阅.html').write_text(page,encoding='utf8')
# Update the input view to include the fourth keyframe and exact frozen prompts.
q=read(R/'视频制作/Metaso-H3-v009/执行队列.json');gp='<meta charset="utf-8"><title>二维关键帧驱动输入v009</title><style>body{max-width:1000px;margin:40px auto;font:18px/1.7 system-ui;background:#111822;color:#eee}img{width:100%}pre{white-space:pre-wrap}</style><h1>四处二维动漫局部输入</h1><p>4张内置imagegen关键帧，4条Metaso H3回片；预计214.2 H3积分，未核账单。以下为实际执行提示词。</p>'
for x in q['items']:gp+='<h2>'+x['attempt_id']+'</h2><img src="参考/'+Path(x['references'][0]['path']).name+'"><pre>'+html.escape(x['prompt'])+'</pre>'
(R/'视频制作/Metaso-H3-v009/补拍输入.html').write_text(gp,encoding='utf8')
prefix='''## 2026-10-28：截图修正与二维动漫纠偏 v005（当前复看候选）

达芬奇《白米饭》当前时间线 `v005_2D_Anime_Fixes`：121段、11497帧（7分59秒01帧）、85个音频片段、8条启用声音轨。截图范围先修口型/过渡；作者指出3D残留后，入洞、群像、展翼、阶梯四处先重绘二维关键帧再补拍。原选声、BGM与作者B12删20帧保留。当前画面不等于作者最终核定。

作者画风明确为标准二维动漫：有线稿与赛璐璐色块、有蓄力/重心/受力/余势的实际角色表演；拒绝3D建模、手办质感及静图推拉的漫剧。旧v007三维措辞是已纠正的历史错误，不得复用为新的执行标准。入口：[工程内复看](后期/二维动漫纠偏-v005/工程内审阅.html)；[修订说明](后期/二维动漫纠偏-v005/修订说明.md)。只修截图与必要接头，作者核定后才扩展同类检查。未导出新视频/DRP/DRT，最终核验并明确要求后再导出。以下为历史记录。

'''
for name in ['AGENTS.md','制作进度.md']:
 path=R/name;working=path.read_text(encoding='utf8');assert not working.startswith(prefix.splitlines()[0]);path.write_text(prefix+working,encoding='utf8')
 base=subprocess.check_output(['git','show','HEAD:'+name],cwd=R);oid=subprocess.check_output(['git','hash-object','-w','--stdin'],cwd=R,input=prefix.encode()+base).decode().strip();subprocess.run(['git','update-index','--add','--cacheinfo','100644',oid,name],cwd=R,check=True)
name='00_打开项目.html';banner='<section id="anime-v005" style="margin:18px;padding:18px;border:2px solid #9ccaff;background:#172336;color:#fff"><h2>当前：二维动漫纠偏 v005 · 达芬奇复看</h2><p>v005_2D_Anime_Fixes · 7分59秒01帧 · 四处二维重绘动画已装配；原声音保留，待你核定，未导出。</p><a style="color:#a9d6ff" href="后期/二维动漫纠偏-v005/工程内审阅.html">查看修正画面与复看时码</a></section>'
def insert(s):
 assert 'id="anime-v005"' not in s
 if re.search(r'<body[^>]*>',s,re.I):return re.sub(r'(<body[^>]*>)',lambda m:m.group(1)+banner,s,count=1,flags=re.I)
 assert '</style>' in s;return s.replace('</style>','</style>'+banner,1)
path=R/name;path.write_text(insert(path.read_text(encoding='utf8')),encoding='utf8');base=subprocess.check_output(['git','show','HEAD:'+name],cwd=R).decode('utf8');oid=subprocess.check_output(['git','hash-object','-w','--stdin'],cwd=R,input=insert(base).encode()).decode().strip();subprocess.run(['git','update-index','--add','--cacheinfo','100644',oid,name],cwd=R,check=True)
print(dict(timeline=p['timeline'],windows=4,audio_unchanged=True,cost_estimates=spend))
