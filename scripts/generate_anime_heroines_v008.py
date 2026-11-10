"""Four authorized seiyuu-style Claude/GPT voice designs; Xiaoyu v006 remains adopted."""
import copy, html, importlib.util, json, shutil, time, sys
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('breeze_io',ROOT/'scripts/generate_breeze_voice_candidates_v001.py')
io=importlib.util.module_from_spec(spec);spec.loader.exec_module(io)
api,save,sha=io.api,io.save,io.sha
REC=ROOT/'资产/生成记录/Claude-GPT英语声线-v008'
MEDIA=ROOT/'资产/声音/Claude-GPT英语声线-v008'
COMFY=io.COMFY
def load(p):return json.loads(p.read_text('utf-8'))

DIRECTIONS=[('claude-A', 'Claude', 'CHAR-CLAUDE', 'A · 清透温柔，坚定藏在里面', 'Japanese anime voice actress. A gentle, clear and delicate heroine voice, warm and sensitive, with quiet inner strength. Light, expressive phrasing. Thank you is softly grateful; What are you doing here reveals sudden concern; The little girl trails into a worried thought. Speak the given lines in clear English, with brief pauses between sentences.'), ('claude-B', 'Claude', 'CHAR-CLAUDE', 'B · 温润柔和，护人时有锋芒', 'Japanese anime voice actress. A warm, velvety heroine voice, gentle and thoughtful, with a focused edge when someone she cares for is in danger. Expressive, flowing phrasing. Thank you is softly grateful; What are you doing here reveals sudden concern; The little girl trails into a worried thought. Speak the given lines in clear English, with brief pauses between sentences.'), ('gpt-A', 'ChatGPT', 'CHAR-GPT', 'A · 慵懒宠溺，自带王者气息', 'Japanese anime voice actress. A full, rounded and soft adult dragon-queen voice. Languid and warmly amused, with effortless royal authority and an affectionate smile. Let her in is an unhurried command; the Church line carries composed reluctance; Easy now and the reassurance become warmly protective. Speak the given lines in clear English, with brief pauses between sentences.'), ('gpt-B', 'ChatGPT', 'CHAR-GPT', 'B · 从容威严，仍然柔和慵懒', 'Japanese anime voice actress. A full, resonant and soft adult dragon-queen voice. Relaxed and dignified, with measured phrasing and unmistakable quiet authority. Let her in is an unhurried command; the Church line carries composed reluctance; Easy now and the reassurance become warmly protective. Speak the given lines in clear English, with brief pauses between sentences.')]

def prepare():
 REC.mkdir(parents=True,exist_ok=True);MEDIA.mkdir(parents=True,exist_ok=True)
 old=load(ROOT/'资产/生成记录/英语声线候选-v001/manifest.json')
 texts={c['role']:c['text'] for c in old['candidates']}
 template=load(Path('G:/comfyui/ComfyUI/workflow/BreezeTTS2-deploy/voice-design-api.json'))
 catalog=api('/object_info')
 d=dict(version='v008',date='2026-10-26',engine='Breeze TTS 2',mode='VoiceDesign',status='prepared',
  authorization='作者确认小鱼v006音色，要求Claude与GPT各两个候选，均使用Japanese anime voice actress方向并保留角色性格。',
  rationale='沿用小鱼成功的英文描述方向，但不克隆小鱼声音；使用VoiceDesign分别设计Claude与GPT的角色身份，无参考音。',
  source='视频制作/生成板-v010/英语译配.json',source_sha256=sha(ROOT/'视频制作/生成板-v010/英语译配.json'),
  comparison='同角色A/B台词、seed、参数一致，仅改变音色与表演描述。沿用v001试听台词供跨版比较；没有新增剧情。',
  xiaoyu_status='作者已暂定v006为小鱼固定参考；v007四种情绪已听审认可；本轮不生成小鱼。',
  validation_route='本会话MCP校验接口反复无诊断报错，沿用同一本地8188实时节点校验及提交时node_errors检查。',
  scope='仅四次本地音频合成；无参考音、变调、变速、配乐或混响。文字描述是目标，实际角色感待作者试听。',candidates=[])
 for ident,role,asset_id,label,instruction in DIRECTIONS:
  g=copy.deepcopy(template);seed=20261028 if role=='Claude' else 20261029
  g['2']['inputs'].update(text=texts[role],instruction=instruction,seed=seed,max_new_tokens=256)
  g['3']['inputs']['filename_prefix']='audio/BreezeTTS2/WhiteRice-Anime-v008/'+ident
  for node in g.values():
   schema=catalog[node['class_type']]['input'];req=schema.get('required',{});assert not set(req)-set(node['inputs'])
   for k,v in node['inputs'].items():
    field=req.get(k,schema.get('optional',{}).get(k));assert field is not None
    if isinstance(v,list):assert catalog[g[v[0]]['class_type']]['output'][v[1]]==field[0]
    elif isinstance(field[0],list):assert v in field[0]
  request=f'资产/生成记录/Claude-GPT英语声线-v008/{ident}-request.json';save(ROOT/request,dict(prompt=g,client_id='white-rice-heroines-anime-v008'))
  d['candidates'].append(dict(id=ident,role=role,asset_id=asset_id,label=label,text=texts[role],instruction=instruction,seed=seed,request=request,status='prepared',schema_validated=True))
 save(REC/'manifest.json',d);return d

def render(d):
 body='<h1>Claude / GPT · 二次元角色声线</h1><p>四个新候选，声音描述均以 Japanese anime voice actress 开头。Claude保留温柔细腻与内在坚定；GPT保留饱满柔和、慵懒与王者气息。两位分别设计声音，不克隆小鱼音色。卡片描述为目标，四条均待你听后选择。</p>'
 for role in ['Claude','ChatGPT']:
  group=[c for c in d['candidates'] if c['role']==role];body+=f'<h2>{role}</h2><p>{html.escape(group[0]["text"])}</p><div class="pair">'
  for c in group:
   if c['status']=='generated':body+=f'<section><h3>{html.escape(c["label"])}</h3><audio controls preload="metadata" src="../../声音/Claude-GPT英语声线-v008/{c["id"]}-preview.flac"></audio><p>{c["seconds"]:.2f}秒 · 待试听</p></section>'
  body+='</div>'
 body+='<p>同角色A/B使用相同台词及参数。试听副本仅作常量音量调整；未变调、变速或添加效果，原件保留。</p><p>小鱼已暂定v006音色，四种情绪测试获认可；本轮未重生成。</p>'
 (REC/'试听.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Claude与GPT · 二次元声线试听</title><style>body{max-width:1100px;margin:35px auto;padding:0 24px;background:#141c25;color:#eee;font:17px/1.8 system-ui}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}section{padding:20px;background:#253343;border-radius:12px}audio{width:100%}h1,h2,h3{color:#f2d5ad}p{color:#c6d2df}@media(max-width:720px){.pair{grid-template-columns:1fr}}</style>'+body+'</html>',encoding='utf-8')

def run():
 q=api('/queue');assert not q['queue_running'] and not q['queue_pending'],'Local queue busy'
 d=load(REC/'manifest.json') if (REC/'manifest.json').exists() else prepare()
 assert d['status']!='stopped_before_submission', 'Author stopped this run; do not submit'
 for c in d['candidates']:
  if c['status']=='generated':continue
  if not c.get('prompt_id'):
   q=api('/queue');assert not q['queue_running'] and not q['queue_pending'],'Other task appeared'
   r=api('/prompt',load(ROOT/c['request']));assert r.get('prompt_id') and not r.get('node_errors'),r
   c.update(prompt_id=r['prompt_id'],status='submitted');save(REC/'manifest.json',d)
  print('SUBMITTED',c['id'],c['prompt_id'],flush=True);deadline=time.monotonic()+600
  while time.monotonic()<deadline:
   h=api('/history/'+c['prompt_id']).get(c['prompt_id'])
   if h:
    save(REC/f'{c["id"]}-history.json',h);assert h['status']['status_str']=='success',h['status']
    a=h['outputs']['3']['audio'][0];native=COMFY/'output'/a['subfolder']/a['filename'];audio,sr=sf.read(native,dtype='float32')
    assert sr==24000 and audio.ndim==1 and np.isfinite(audio).all() and 1<len(audio)/sr<20.4
    rms=float(np.sqrt(np.mean(audio**2)));peak=float(np.max(np.abs(audio)));assert rms>0.001
    raw=MEDIA/f'{c["id"]}.flac';assert not raw.exists();shutil.copy2(native,raw);assert sha(raw)==sha(native)
    gain=min(0.055/rms,0.98/peak);preview=MEDIA/f'{c["id"]}-preview.flac';sf.write(preview,audio*gain,sr,subtype='PCM_24')
    c.update(status='generated',path=raw.relative_to(ROOT).as_posix(),sha256=sha(raw),native_output=str(native),seconds=len(audio)/sr,sample_rate=sr,rms=rms,peak=peak,preview_path=preview.relative_to(ROOT).as_posix(),preview_sha256=sha(preview),preview_gain_db=float(20*np.log10(gain)),listening_status='pending_author_review')
    save(REC/'manifest.json',d);render(d);print('COMPLETED',c['id'],round(c['seconds'],2),'seconds',flush=True);break
   time.sleep(4)
  else:raise TimeoutError(c['prompt_id'])
 d['status']='four_candidates_generated_pending_author_listening';save(REC/'manifest.json',d);render(d)
 print('DONE: four Claude/GPT candidates pending listening; Xiaoyu v006 remains adopted.',flush=True)
if __name__=='__main__':
 if '--prepare' in sys.argv:
  assert not (REC/'manifest.json').exists(), 'Preserve existing record'
  prepare(); print('PREPARED')
 else: run()
