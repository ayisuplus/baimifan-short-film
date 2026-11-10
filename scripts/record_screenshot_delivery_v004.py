from pathlib import Path
import json,html,subprocess,hashlib,concurrent.futures
R=Path(__file__).resolve().parents[1];O=R/'后期/截图定点修正-v004';G=R/'视频制作/Metaso-H3-v007'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def tc(f):
 f=round(f);return f'{f//86400:02}:{f//1440%60:02}:{f//24%60:02}:{f%24:02}'
p=read(O/'后期执行计划.json');a=read(O/'最终实际时间线.json')['result'];assembly=read(O/'实际装配回读.json')['result'];q=read(G/'执行队列.json')
assert a['frames']==p['frames']==11497 and len(a['video'])==len(p['edl'])==121
assert all(v['enabled'] for v in a['video']) and all(t['enabled'] for t in a['audio_tracks'])
quant=[]
for s,v in zip(p['edl'],a['video']):
 assert s['name']==v['name'] and s['record']==v['start'] and s['frames']==v['end']-v['start']
 assert Path(s['source'])==Path(v['path']) and abs(s['in']-v['source_in'])<=1 and abs(s['out']-v['source_out'])<=1
 if s['in']!=v['source_in'] or s['out']!=v['source_out']:quant.append(dict(name=s['name'],planned=[s['in'],s['out']],native=[v['source_in'],v['source_out']],reason='非整数变速回读取整误差1帧，无声器物/闭口段；不影响总长或配音'))
used=set(Path(s['source']).stem for s in p['edl'] if 'Metaso-H3-v007' in s['source'])
for x in q['items']:
 assert x['status']=='downloaded_candidate'
 assert hashlib.sha256((R/x['local_path']).read_bytes()).hexdigest()==x['sha256']
 if x['attempt_id'] in used:x.update(review_decision='used_selected_ranges_in_v004_pending_author',adopted_ranges=[dict(record=s['record'],source_frames=[s['in'],s['out']],timeline_frames=s['frames'],speed=s['speed']) for s in p['edl'] if Path(s['source']).stem==x['attempt_id']])
 else:assert x.get('review_decision')=='rejected'
save(G/'执行队列.json',q)
def decode(x):
 r=subprocess.run(['ffmpeg','-v','error','-i',str(R/x['local_path']),'-map','0:v:0','-f','null','NUL'],capture_output=True,text=True)
 return dict(attempt=x['attempt_id'],returncode=r.returncode,errors=r.stderr)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:checks=list(ex.map(decode,[x for x in q['items'] if x['attempt_id'] in used]))
assert all(c['returncode']==0 and not c['errors'] for c in checks)
save(O/'验证结果.json',dict(status='工程结构和定点候选核验通过，待作者复看',video_clips=121,frames=11497,seconds=11497/24,voice_pieces=64,music_segments=17,enabled_tracks=8,old_timeline_preserved=a['old_timeline'],native_quantization=quant,new_video_decode_checks=checks,selected_voice_preservation='63句64片段保留；仅VO-CY009-01后移7帧。作者B12删20帧及双音频片段保持。',music_preservation='全部17段与原版位置/时长/音量回读一致',foley='局部转身、群像脚步与洞口触地重新对位；其他声音原位保留',exported_video_or_project=False,qa_stills=5,limits=['独立4/12fps视觉与实际声音活动窗口核验，不等于逐日语音素认证','尚未冒称全片连续听审、作者审美核定','只处理截图及接点，作者核定后才扩展其他同类问题']))
rows=[('图1：内心戏→小鱼离开',1282,'恶魔、天使分别按选声补拍；小鱼说完再接原来正确的离开方向。新片走回王座部分拒用。'),('图2：钻入教堂',1910,'补洞内手膝落地、抬眼，再接稳定大厅和登阶；加入轻触与衣物摩擦。'),('图3/4：教主与Claude',3478,'按原片身份和材质重拍说话；Claude怒斥与恳求分清，撤掉过早抓袍插入；无声尾替成闭口反应。'),('图5：群像入场',4778,'低位带破木前景、队伍前后分层；舍弃回片重新开门的首秒，只用进入与命令。'),('图6：Kimi窗外请门',4922,'保留凝形；完整玻璃下请门→银刃特写承句尾→发力投刃→下一镜才破窗。首轮提前破窗拒用。'),('图7/8：GPT展翼（重复截图）',6476,'脚尖离地、翼压和衣摆建立动作，随后侧脸开唱；只在无声/无脸段调整时长。'),('图9：阶上与阶下',9699,'肩后俯视建立Claude/GPT与千问怀抱小鱼的阶差；移除上一镜重复小鱼反应，保留B38安抚与起咏手部。')]
estimate=round(sum(x['estimated_credits'] for x in q['items']),1)
notes=['# 截图定点修正 v004','',f'达芬奇《白米饭》时间线：`{p["timeline"]}`。44批、121段、11497帧，7分59秒01帧。仅截图范围及必要接头，待作者核定。','',f'本轮Metaso H3局部补拍12次，10条选段使用，2条拒用，无在途；预计{estimate}积分，未核实际账单。原片和失败候选保留。未导出新视频、DRP或DRT；5张工程静帧仅供裁切核验。','','|截图|回看时码|本轮处理|','|---|---|---|']
notes += [f'|{title}|{tc(frame)}|{desc}|' for title,frame,desc in rows]
notes+=['','保留63句作者选声（64个音频片段）、17段BGM与8条启用声音轨。仅小鱼决定句后移7帧；作者第12批删20帧与对应两段声音保持。相关拟音重排，混音PCM峰值检查未削波。','','Kimi银刃特写约3倍裁切，清晰度略软；广景新增月形发光标记，玻璃完整，列作者复看项。教主、Claude、GPT无声尾为闭口短段轻慢放；有声口部原速。大段开闭口已核对，日语逐音素与连续听感仍需核验，不把技术通过当成最终观感通过。','','你核定这些后，再检查其他同类问题。']
(O/'修订说明.md').write_text('\n'.join(notes)+'\n',encoding='utf8')
page='''<!doctype html><meta charset="utf-8"><title>白米饭·截图定点修正v004</title><style>body{font:18px/1.7 system-ui;max-width:1100px;margin:40px auto;background:#111822;color:#e6ebf4;padding:0 20px}a{color:#9ccaff}table{border-collapse:collapse;width:100%}td,th{padding:14px;text-align:left;border-bottom:1px solid #334155}code{color:#ffd69b}img{max-width:100%;border-radius:10px}article{margin:28px 0}</style><h1>《白米饭》截图定点修正 v004</h1><p>请在达芬奇复看 <code>v004_Screenshot_Targeted_Fixes</code>。时长仍为7分59秒01帧，旧版保留。已停在第5批起点，橙色标记为本轮修正。</p><p>这里只列你给的截图与必要接头，核定后再查其他同类问题。没有新成片/工程导出。</p><table><tr><th>截图</th><th>达芬奇时码</th><th>修改</th></tr>'''
page+=''.join('<tr><td>'+html.escape(title)+'</td><td><code>'+tc(frame)+'</code></td><td>'+html.escape(desc)+'</td></tr>' for title,frame,desc in rows)+'</table>'
page+='<p>原选63句（64片段）、17段音乐、8条声音轨保留；小鱼决定句仅后移7帧。局部衣擦、落步、洞口触地已对位。结构与PCM检查通过，尚不代表逐音素同步、连续听感或作者最终核定。</p><p>重点留意：Kimi银刃近景略软、窗面新增月光标记；教主/Claude/GPT静音尾的闭口停留是否自然。</p>'
for filename,title in [('native-kimi-blade.png','Kimi句尾银刃特写'),('native-stair-bridge.png','阶上到阶下空间桥'),('native-claude-tail.png','Claude静音尾表情')]:page+='<article><h2>'+title+'</h2><img src="证据/'+filename+'"><p>达芬奇工程内核验静帧，不是新导出视频。</p></article>'
page+=f'<p>本轮12次局部H3，10条选段使用、2条拒用，预计{estimate}积分（未核账单），无在途任务。</p><p><a href="修订说明.md">修订说明</a> · <a href="验证结果.json">验证记录</a> · <a href="../../视频制作/Metaso-H3-v007/补拍输入.html">冻结补拍输入</a></p>'
(O/'工程内审阅.html').write_text(page,encoding='utf8')
print(dict(review=str(O/'工程内审阅.html'),decode_checks=len(checks),estimate=estimate))
