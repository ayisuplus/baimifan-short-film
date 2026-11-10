"""Four authorized Claude/GPT voice designs; no realistic reference voices."""
import copy, html, importlib.util, json, shutil, time
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('breeze_io',ROOT/'scripts/generate_breeze_voice_candidates_v001.py')
io=importlib.util.module_from_spec(spec);spec.loader.exec_module(io)
api,save,sha=io.api,io.save,io.sha
REC=ROOT/'资产/生成记录/Claude-GPT英语声线-v003'
MEDIA=ROOT/'资产/声音/Claude-GPT英语声线-v003'
COMFY=io.COMFY
def load(p):return json.loads(p.read_text('utf-8'))

DIRECTIONS=[
 ('claude-A','Claude','CHAR-CLAUDE','A · 清透、温柔的少女角色',
  'Create the distinctive feminine voice of a young adult heroine in a Japanese fantasy anime, speaking clear English. A delicate, bell-clear tone with warmth underneath, musical phrasing and expressive little changes at phrase endings. The voice belongs to an animated heroine, not a live-action child. Thank you is gently reserved; What are you doing here reveals sudden concern; The little girl trails into a worried thought. Keep one recognizable voice throughout. Brief pauses between sentences; speak only the supplied words.'),
 ('claude-B','Claude','CHAR-CLAUDE','B · 温润、内藏锋芒',
  'Create the distinctive feminine voice of a young adult heroine in a Japanese fantasy anime, speaking clear English. A warm, velvety tone with a clear ringing center; soft phrases have expressive shape, and concern brings a crisp, focused edge. The voice belongs to an animated heroine, not a live-action child. Thank you is gently reserved; What are you doing here reveals sudden concern; The little girl trails into a worried thought. Keep one recognizable voice throughout. Brief pauses between sentences; speak only the supplied words.'),
 ('gpt-A','ChatGPT','CHAR-GPT','A · 慵懒、带宠溺的龙娘女王',
  'Create a distinctive adult female dragon-queen voice for a Japanese fantasy anime, speaking clear English. Full, rounded and soft, with a velvety lower register and richly shaped vowels. A languid queen: a slight knowing smile, playfully drawn phrase endings, effortless royal authority. Let her in is an unhurried command; the Church line has composed reluctance; Easy now and the reassurance turn warmly protective. Stylized anime character acting, never a child voice or flat narration. Brief pauses between sentences; speak only the supplied words.'),
 ('gpt-B','ChatGPT','CHAR-GPT','B · 从容、威严更鲜明的龙娘女王',
  'Create a distinctive adult female dragon-queen voice for a Japanese fantasy anime, speaking clear English. Full, rounded and soft, with a resonant lower register and a clear, ringing center. A poised queen: measured melodic phrasing, firm elegant endings, quiet royal authority that carries without shouting. Let her in is an unhurried command; the Church line has composed reluctance; Easy now and the reassurance turn warmly protective. Stylized anime character acting, never a child voice or flat narration. Brief pauses between sentences; speak only the supplied words.'),
]

def prepare():
 REC.mkdir(parents=True,exist_ok=True);MEDIA.mkdir(parents=True,exist_ok=True)
 old=load(ROOT/'资产/生成记录/英语声线候选-v001/manifest.json')
 texts={c['role']:c['text'] for c in old['candidates']}
 template=load(Path('G:/comfyui/ComfyUI/workflow/BreezeTTS2-deploy/voice-design-api.json'))
 catalog=api('/object_info')
 d=dict(version='v003',date='2026-10-26',engine='Breeze TTS 2',mode='VoiceDesign',status='prepared',
  authorization='作者要求Claude和GPT各两个二次元角色音色候选，明确避免欧美真人儿童演员感；小鱼B2只保留方向，未定稿。',
  rationale='原偏写实参考音可能把写实质感一并保留，这是待验证推断；本轮不克隆原样音，直接设计成年女性动漫角色声线。',
  source='视频制作/生成板-v010/英语译配.json',source_sha256=sha(ROOT/'视频制作/生成板-v010/英语译配.json'),
  comparison='同角色A/B台词、seed、参数一致，仅改变音色与表演描述。沿用v001试听台词供跨版比较；没有新增剧情。',
  xiaoyu_status='B2表演方向更接近，但真人儿童质感仍待解决；本轮不新增小鱼任务，也不指定固定声线。',
  scope='仅四次本地音频合成；无参考音、变调、变速、配乐或混响。文字描述是目标，实际角色感待作者试听。',candidates=[])
 for ident,role,asset_id,label,instruction in DIRECTIONS:
  g=copy.deepcopy(template);seed=20261028 if role=='Claude' else 20261029
  g['2']['inputs'].update(text=texts[role],instruction=instruction,seed=seed,max_new_tokens=256)
  g['3']['inputs']['filename_prefix']='audio/BreezeTTS2/WhiteRice-Anime-v003/'+ident
  for node in g.values():
   schema=catalog[node['class_type']]['input'];req=schema.get('required',{});assert not set(req)-set(node['inputs'])
   for k,v in node['inputs'].items():
    field=req.get(k,schema.get('optional',{}).get(k));assert field is not None
    if isinstance(v,list):assert catalog[g[v[0]]['class_type']]['output'][v[1]]==field[0]
    elif isinstance(field[0],list):assert v in field[0]
  request=f'资产/生成记录/Claude-GPT英语声线-v003/{ident}-request.json';save(ROOT/request,dict(prompt=g,client_id='white-rice-heroines-anime-v003'))
  d['candidates'].append(dict(id=ident,role=role,asset_id=asset_id,label=label,text=texts[role],instruction=instruction,seed=seed,request=request,status='prepared',schema_validated=True))
 save(REC/'manifest.json',d);return d

def render(d):
 body='<h1>Claude / GPT · 二次元角色声线</h1><p>四个新候选，不克隆上一轮偏写实的声音。两位都以成年女性动漫角色的声音设计，避免真人儿童演员感。卡片描述为设计目标，是否做到请按实际听感判断；全部未定稿。</p>'
 for role in ['Claude','ChatGPT']:
  group=[c for c in d['candidates'] if c['role']==role];body+=f'<h2>{role}</h2><p>{html.escape(group[0]["text"])}</p><div class="pair">'
  for c in group:
   if c['status']=='generated':body+=f'<section><h3>{html.escape(c["label"])}</h3><audio controls preload="metadata" src="../../声音/Claude-GPT英语声线-v003/{c["id"]}-preview.flac"></audio><p>{c["seconds"]:.2f}秒 · 待试听</p></section>'
  body+='</div>'
 body+='<p>同角色A/B使用相同台词及参数。试听副本仅作常量音量调整；未变调、变速或添加效果，原件保留。</p><p>小鱼B2暂定表演方向，真人儿童质感仍待解决，本轮没有重生小鱼。</p>'
 (REC/'试听.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Claude与GPT · 二次元声线试听</title><style>body{max-width:1100px;margin:35px auto;padding:0 24px;background:#141c25;color:#eee;font:17px/1.8 system-ui}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}section{padding:20px;background:#253343;border-radius:12px}audio{width:100%}h1,h2,h3{color:#f2d5ad}p{color:#c6d2df}@media(max-width:720px){.pair{grid-template-columns:1fr}}</style>'+body+'</html>',encoding='utf-8')

def run():
 q=api('/queue');assert not q['queue_running'] and not q['queue_pending'],'Local queue busy'
 d=load(REC/'manifest.json') if (REC/'manifest.json').exists() else prepare()
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
 print('DONE: four candidates, no voices adopted.',flush=True)
if __name__=='__main__':run()
