"""Two authorized expression variants anchored to the original Xiaoyu B voice."""
import copy, hashlib, html, json, shutil, time, urllib.request
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'资产/生成记录/小鱼英语声线-v002'
MEDIA=ROOT/'资产/声音/小鱼英语声线-v002'
COMFY=Path('G:/comfyui/ComfyUI/ComfyUI')
HTTP=urllib.request.build_opener(urllib.request.ProxyHandler({}))
def api(route,data=None):
 req=urllib.request.Request('http://127.0.0.1:8188'+route,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
 with HTTP.open(req,timeout=30) as r:return json.load(r)
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text('utf-8'))

def prepare():
 REC.mkdir(parents=True,exist_ok=True);MEDIA.mkdir(parents=True,exist_ok=True)
 old=load(ROOT/'资产/生成记录/英语声线候选-v001/manifest.json')
 ref=next(c for c in old['candidates'] if c['id']=='xiaoyu-B')
 source=ROOT/ref['path'];assert sha(source)==ref['sha256']
 target=COMFY/'input/white-rice-xiaoyu-B-v001.flac'
 if target.exists():assert sha(target)==ref['sha256']
 else:shutil.copy2(source,target)
 graph=load(Path('G:/comfyui/ComfyUI/workflow/BreezeTTS2-deploy/voice-direction-api.json'))
 directions=[
  ('B1','灵动、带笑的期待',"Keep the reference speaker's soft, rounded voice. Perform as a lively girl character in an English-dubbed anime. Let her facial expressions be audible: 'Would you like some?' has a bright, inviting smile and a gently bouncing question; 'One more try.' has a little spark of determination; 'I'll get you out of here.' is a tender, confident promise. Use light, expressive melodic intonation and clear words. Brief pauses between sentences. Say only the provided text."),
  ('B2','表情更鲜明、带小倔劲',"Keep the reference speaker's soft, rounded voice. Perform as an expressive girl character in an English-dubbed anime, with distinct emotional turns. 'Would you like some?' is eagerly hopeful, as she offers her bowl with shining eyes. 'One more try.' is a small, stubborn declaration. 'I'll get you out of here.' becomes warmly resolute: she really means this promise. Use animated changes in rhythm and emphasis, with crisp, expressive phrase endings. Brief pauses between sentences. Say only the provided text.")]
 manifest=dict(version='v002',date='2026-10-26',engine='Breeze TTS 2',mode='VoiceDirection',role='小鱼',asset_id='CHAR-DEEPSEEK',status='prepared',
  authorization='作者明确授权保留小鱼B柔软圆润，增加二次元角色灵动与表情感，生成两个版本。',
  source_candidate='资产/生成记录/英语声线候选-v001/manifest.json#xiaoyu-B',reference_path=ref['path'],reference_sha256=ref['sha256'],reference_input=str(target),reference_text=ref['text'],reference_text_provenance='原B生成请求逐字文本；未另做自动转写验收。',
  author_feedback='原B柔软圆润很好，但像真实人类小孩，缺少二次元角色神态。原六段未定稿；仅B作为本次音色参考。',
  scope='只改变小鱼表演指令；不重做Claude或GPT。相同原B音频、英文台词、seed和参数，比较两种表情方向。不进行变调、变速、混响或配乐处理。',candidates=[])
 catalog=api('/object_info')
 for variant,label,instruction in directions:
  g=copy.deepcopy(graph);g['4']['inputs']['audio']=target.name
  g['2']['inputs'].update(text=ref['text'],reference_text=ref['text'],instruction=instruction,seed=20261027,max_new_tokens=256)
  g['3']['inputs']['filename_prefix']=f'audio/BreezeTTS2/WhiteRice-Xiaoyu-v002/{variant}'
  for node in g.values():
   spec=catalog[node['class_type']]['input'];req=spec.get('required',{});assert not set(req)-set(node['inputs'])
   for k,v in node['inputs'].items():
    field=req.get(k,spec.get('optional',{}).get(k));assert field is not None
    if isinstance(v,list):assert catalog[g[v[0]]['class_type']]['output'][v[1]]==field[0]
    elif isinstance(field[0],list):assert v in field[0],(k,v)
  request=f'资产/生成记录/小鱼英语声线-v002/{variant}-request.json';save(ROOT/request,dict(prompt=g,client_id='white-rice-xiaoyu-anime-v002'))
  manifest['candidates'].append(dict(id=variant,label=label,text=ref['text'],instruction=instruction,request=request,status='prepared',schema_validated=True))
 save(REC/'manifest.json',manifest);return manifest

def render(d):
 body='<h1>小鱼 · 二次元表情候选</h1><p>保留原B的柔软圆润，以原B音频作参考，比较两种角色表演方向。三段台词相同；文字描述是设计目标，是否有角色神态请以实际听感判断。所有版本未定稿。</p>'
 body+='<p>Would you like some? One more try. I\'ll get you out of here.</p><section><h2>原B · 对照</h2><audio controls preload="metadata" src="../../声音/英语声线候选-v001/xiaoyu-B-preview.flac"></audio></section>'
 for c in d['candidates']:
  if c['status']=='generated':body+=f'<section><h2>{c["id"]} · {html.escape(c["label"])}</h2><audio controls preload="metadata" src="../../声音/小鱼英语声线-v002/{c["id"]}-preview.flac"></audio><p>{c["seconds"]:.2f}秒 · 待试听</p></section>'
 body+='<p>试听副本只做常量音量调整，与原B使用相同整体RMS目标；没有变调或变速。原件保留。</p>'
 page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>小鱼 · 二次元声线试听</title><style>body{max-width:850px;margin:35px auto;padding:0 24px;background:#141c25;color:#eee;font:17px/1.8 system-ui}section{padding:15px 25px;background:#253343;border-radius:12px;margin:20px 0}audio{width:100%}h1,h2{color:#f2d5ad}p{color:#c6d2df}</style>'+body+'</html>'
 (REC/'试听.html').write_text(page,encoding='utf-8')

def run():
 q=api('/queue');assert not q['queue_running'] and not q['queue_pending'],'Queue busy; no interruption'
 d=load(REC/'manifest.json') if (REC/'manifest.json').exists() else prepare()
 for c in d['candidates']:
  if c['status']=='generated':continue
  if not c.get('prompt_id'):
   q=api('/queue');assert not q['queue_running'] and not q['queue_pending'],'Other job present'
   r=api('/prompt',load(ROOT/c['request']));assert r.get('prompt_id') and not r.get('node_errors'),r
   c.update(prompt_id=r['prompt_id'],status='submitted');save(REC/'manifest.json',d)
  print('SUBMITTED',c['id'],c['prompt_id'],flush=True)
  deadline=time.monotonic()+600
  while time.monotonic()<deadline:
   h=api('/history/'+c['prompt_id']).get(c['prompt_id'])
   if h:
    save(REC/f'{c["id"]}-history.json',h);assert h['status']['status_str']=='success',h['status']
    a=h['outputs']['3']['audio'][0];native=COMFY/'output'/a['subfolder']/a['filename'];audio,sr=sf.read(native,dtype='float32')
    assert sr==24000 and audio.ndim==1 and np.isfinite(audio).all() and 1<len(audio)/sr<20.4
    rms=float(np.sqrt(np.mean(audio**2)));assert rms>0.001
    raw=MEDIA/f'{c["id"]}.flac';assert not raw.exists();shutil.copy2(native,raw);assert sha(raw)==sha(native)
    gain=min(0.055/rms,0.98/float(np.max(np.abs(audio))));preview=MEDIA/f'{c["id"]}-preview.flac';sf.write(preview,audio*gain,sr,subtype='PCM_24')
    c.update(status='generated',path=raw.relative_to(ROOT).as_posix(),sha256=sha(raw),native_output=str(native),seconds=len(audio)/sr,sample_rate=sr,rms=rms,peak=float(np.max(np.abs(audio))),preview_path=preview.relative_to(ROOT).as_posix(),preview_sha256=sha(preview),preview_gain_db=float(20*np.log10(gain)),listening_status='pending_author_review')
    save(REC/'manifest.json',d);render(d);print('COMPLETED',c['id'],round(c['seconds'],2),'seconds',flush=True);break
   time.sleep(4)
  else:raise TimeoutError(c['prompt_id'])
 d['status']='two_candidates_generated_pending_author_listening';save(REC/'manifest.json',d);render(d)
 print('DONE: two candidates; original B retained; no adopted voice.',flush=True)
if __name__=='__main__':run()
