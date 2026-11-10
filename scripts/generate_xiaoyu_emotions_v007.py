"""Four authorized emotion auditions anchored to author-approved Xiaoyu v006."""
import copy, html, importlib.util, json, shutil, sys, time
from pathlib import Path
import numpy as np
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('breeze_io', ROOT/'scripts/generate_breeze_voice_candidates_v001.py')
io=importlib.util.module_from_spec(spec); spec.loader.exec_module(io)
REC=ROOT/'资产/生成记录/小鱼英语情绪-v007'
MEDIA=ROOT/'资产/声音/小鱼英语情绪-v007'
COMMON="Speak English as a Japanese anime voice actress. Keep the reference speaker's identity and soft, rounded timbre. "
EMOTIONS=[
 ('happy','开心','Happy and delighted, with an audible warm smile and lively, springy phrasing.'),
 ('hurt','委屈','Feeling hurt and unfairly misunderstood, tenderly asking to be heard. Let the hurt show in the words, without sobbing.'),
 ('stubborn','倔强','Stubbornly determined, insisting with a little defiant spirit. She refuses to give up.'),
 ('serious','认真','Serious and sincere, calmly focused and quietly resolute. She means every word of her promise.')]
def load(p): return json.loads(p.read_text('utf-8'))
def prepare():
 REC.mkdir(parents=True,exist_ok=True); MEDIA.mkdir(parents=True,exist_ok=True)
 if (REC/'manifest.json').exists(): return load(REC/'manifest.json')
 ref=load(ROOT/'资产/生成记录/小鱼英语声线-v006/manifest.json')
 assert ref['listening_status']=='author_approved_direction'
 source=ROOT/ref['path']; assert io.sha(source)==ref['sha256']
 target=io.COMFY/'input/white-rice-xiaoyu-v006-approved.flac'
 if target.exists(): assert io.sha(target)==ref['sha256']
 else: shutil.copy2(source,target)
 graph=load(Path('G:/comfyui/ComfyUI/workflow/BreezeTTS2-deploy/voice-direction-api.json'))
 catalog=io.api('/object_info')
 d=dict(version='v007',date='2026-10-26',role='小鱼',asset_id='CHAR-DEEPSEEK',engine='Breeze TTS 2',mode='VoiceDirection',status='prepared',
  authorization='作者要求用已认可小鱼音色，分别试开心、委屈、倔强和认真，四条供听审。',
  reference_path=ref['path'],reference_sha256=ref['sha256'],reference_input=str(target),reference_text=ref['text'],
  reference_text_provenance='v006原生成请求文本；作者已听审认可声音方向，未另做逐字自动转写验证。',
  scope='四条用相同三句英语、v006干声参考、seed和采样参数，只更改情绪指令。非剧情连读，不按镜头卡时；其他角色暂停。',
  processing='原件保留；试听副本仅调整整体音量到相同RMS目标，无变调、变速、混响或配乐。',
  validation_route='MCP validate_workflow本会话多次无诊断报错；使用同一本地8188实时object_info校验与提交时node_errors检查。',
  candidates=[])
 for ident,label,emotion in EMOTIONS:
  g=copy.deepcopy(graph); g['4']['inputs']['audio']=target.name
  instruction=COMMON+emotion+' Say only the provided text, with a brief pause between sentences.'
  g['2']['inputs'].update(text=ref['text'],reference_text=ref['text'],instruction=instruction,seed=20261027,max_new_tokens=256)
  g['3']['inputs']['filename_prefix']=f'audio/BreezeTTS2/WhiteRice-Xiaoyu-v007/{ident}'
  for n in g.values():
   schema=catalog[n['class_type']]['input']; req=schema['required']; assert not set(req)-set(n['inputs'])
   for k,v in n['inputs'].items():
    field=req.get(k,schema.get('optional',{}).get(k)); assert field is not None
    if isinstance(v,list): assert catalog[g[v[0]]['class_type']]['output'][v[1]]==field[0]
    elif isinstance(field[0],list): assert v in field[0],(k,v)
    elif len(field)>1 and isinstance(field[1],dict) and isinstance(v,(int,float)):
     assert field[1].get('min',v)<=v<=field[1].get('max',v)
  request=REC/f'{ident}-request.json'; io.save(request,dict(prompt=g,client_id='xiaoyu-emotions-v007'))
  d['candidates'].append(dict(id=ident,label=label,text=ref['text'],instruction=instruction,request=request.relative_to(ROOT).as_posix(),status='prepared',schema_validated=True))
 io.save(REC/'manifest.json',d); return d
def render(d):
 body='<h1>小鱼 · 四种情绪试听</h1><p>用你认可的v006原声作参考，保留 Japanese anime voice actress 与柔软圆润的声音方向。四条台词和参数相同，仅改变情绪指令。先听像不像同一个小鱼，再听情绪是否到位。</p>'
 body+='<p>Would you like some? One more try. I\'ll get you out of here.<br>你要吃一点吗？再试一下。我带你出去。</p>'
 body+='<section><h2>v006 · 你认可的声音基准</h2><audio controls preload="metadata" src="../../声音/小鱼英语声线-v006/xiaoyu-en-v006-preview.flac"></audio></section>'
 for c in d['candidates']:
  if c['status']!='generated': continue
  body+=f'<section><h2>{html.escape(c["label"])}</h2><audio controls preload="metadata" src="../../声音/小鱼英语情绪-v007/{c["id"]}-preview.flac"></audio><p>{c["seconds"]:.2f}秒 · 新表演待听审</p><details><summary>实际表演指令</summary><p>{html.escape(c["instruction"])}</p></details></section>'
 body+='<p>试听副本只调整整体音量，未变调或变速，原件保留。相同RMS方便比较，但不代表主观响度完全相同。沿用同一参考不等于身份稳定性已通过；最终以你的听感为准。</p><p><a href="../../../00_打开项目.html">返回项目</a></p>'
 page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>小鱼 · 四种情绪试听</title><style>body{max-width:850px;margin:30px auto;padding:24px;background:#141c25;color:#eee;font:17px/1.8 system-ui}section{padding:20px;background:#253343;border-radius:12px;margin:20px 0}audio{width:100%}h1,h2{color:#f2d5ad}p{color:#c6d2df}a{color:#abd7ff}</style>'+body+'</html>'
 (REC/'试听.html').write_text(page,encoding='utf-8')
def run():
 d=prepare()
 for c in d['candidates']:
  if c['status']=='generated': continue
  if not c.get('prompt_id'):
   q=io.api('/queue'); assert not q['queue_running'] and not q['queue_pending'],'Queue busy; do not interrupt'
   r=io.api('/prompt',load(ROOT/c['request'])); assert r.get('prompt_id') and not r.get('node_errors'),r
   c.update(status='submitted',prompt_id=r['prompt_id']); io.save(REC/'manifest.json',d)
  print('SUBMITTED',c['id'],c['prompt_id'],flush=True); deadline=time.monotonic()+600
  while time.monotonic()<deadline:
   h=io.api('/history/'+c['prompt_id']).get(c['prompt_id'])
   if h:
    io.save(REC/f'{c["id"]}-history.json',h); assert h['status']['status_str']=='success',h['status']
    item=h['outputs']['3']['audio'][0]; native=io.COMFY/'output'/item['subfolder']/item['filename']
    a,sr=sf.read(native,dtype='float32'); assert sr==24000 and a.ndim==1 and np.isfinite(a).all() and 1<len(a)/sr<20.4
    rms=float(np.sqrt(np.mean(a*a))); peak=float(np.max(np.abs(a))); assert rms>0.001
    raw=MEDIA/f'{c["id"]}.flac'; assert not raw.exists(); shutil.copy2(native,raw); assert io.sha(raw)==io.sha(native)
    gain=min(0.055/rms,0.98/peak); preview=MEDIA/f'{c["id"]}-preview.flac'; sf.write(preview,a*gain,sr,subtype='PCM_24')
    c.update(status='generated',path=raw.relative_to(ROOT).as_posix(),sha256=io.sha(raw),preview_path=preview.relative_to(ROOT).as_posix(),preview_sha256=io.sha(preview),seconds=len(a)/sr,sample_rate=sr,peak=peak,rms=rms,preview_gain_db=float(20*np.log10(gain)),native_output=str(native),listening_status='pending_author_review')
    io.save(REC/'manifest.json',d); render(d); print('COMPLETED',c['id'],c['seconds'],'seconds',flush=True); break
   time.sleep(4)
  else: raise TimeoutError(c['prompt_id'])
 d['status']='four_candidates_generated_pending_author_listening'; io.save(REC/'manifest.json',d); render(d); print('DONE',flush=True)
if __name__=='__main__':
 if '--prepare' in sys.argv: prepare(); print('PREPARED')
 else: run()
