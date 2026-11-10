"""Six authorized English voice designs. Uses the existing local ComfyUI only."""
import copy, hashlib, html, json, shutil, time, urllib.request
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/'资产/生成记录/英语声线候选-v001'
MEDIA=ROOT/'资产/声音/英语声线候选-v001'
COMFY=Path('G:/comfyui/ComfyUI/ComfyUI')
BASE='http://127.0.0.1:8188'
HTTP=urllib.request.build_opener(urllib.request.ProxyHandler({}))
def api(route,data=None):
 req=urllib.request.Request(BASE+route,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
 with HTTP.open(req,timeout=30) as r:return json.load(r)
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

ROLES=[
 ('xiaoyu','小鱼','CHAR-DEEPSEEK',"Would you like some? One more try. I'll get you out of here.",
  [('A','清亮、真诚','A little girl with a clear, bright, youthful voice and natural English pronunciation. She sounds sincere, friendly and quietly determined. Speak naturally, with a brief pause between sentences.'),
   ('B','柔软、圆润','A little girl with a soft, rounded, youthful voice and natural English pronunciation. She sounds sincere, friendly and quietly determined. Speak naturally, with a brief pause between sentences.')]),
 ('claude','Claude','CHAR-CLAUDE',"Thank you. What are you doing here? The little girl...",
  [('A','清澈、细腻','A young woman with a clear, delicate, warm voice and natural English pronunciation. She speaks gently and thoughtfully, with quiet inner strength. Speak naturally, with a brief pause between sentences.'),
   ('B','温润、有共鸣','A young woman with a warm, rounded, resonant voice and natural English pronunciation. She speaks gently and thoughtfully, with quiet inner strength. Speak naturally, with a brief pause between sentences.')]),
 ('gpt','ChatGPT','CHAR-GPT',"Let her in. I shouldn't interfere in Church affairs. Easy now. She's safe. Waiting for you down below.",
  [('A','柔和、慵懒的王者从容','A woman with a full, soft, warm voice and natural English pronunciation. A relaxed queen with effortless authority: unhurried, composed, slightly languid, accustomed to being listened to. Speak naturally, with a brief pause between sentences.'),
   ('B','饱满、端正的王者威严','A woman with a full, soft, warm voice and natural English pronunciation. A dignified queen with quiet authority: poised, assured, steady, accustomed to being listened to. Speak naturally, with a brief pause between sentences.')]),
]

def prepare():
 RECORD.mkdir(parents=True,exist_ok=True);MEDIA.mkdir(parents=True,exist_ok=True)
 base=json.loads(Path('G:/comfyui/ComfyUI/workflow/BreezeTTS2-deploy/voice-design-api.json').read_text('utf-8'))
 catalog=api('/object_info'); manifest=dict(version='v001',date='2026-10-26',title='白米饭 · 英语声线候选',engine='Breeze TTS 2',mode='voice_design',status='candidates_pending_author_listening',
  authorization='作者要求小鱼、Claude、GPT各两个候选，试听后决定；本轮仅六段本地试音。',
  source='视频制作/生成板-v010/英语译配.json',source_sha256=sha(ROOT/'视频制作/生成板-v010/英语译配.json'),
  scope='选声音身份；台词摘自现稿并拼成试听片段，不代表连续剧情或已按镜头卡时。无配乐、音效、混响或音高处理。',
  comparison='同角色A/B使用相同台词、种子与采样参数，仅改变声音描述。描述是生成目标，实际差异待听审。',
  voice_reference='尚未采用。选定候选后再建立准确逐字稿和固定参考；固定seed不等于已证明跨句音色稳定。',
  candidates=[])
 for ri,(slug,name,asset_id,text,variants) in enumerate(ROLES):
  for variant,label,instruction in variants:
   ident=f'{slug}-{variant}';graph=copy.deepcopy(base)
   graph['2']['inputs'].update(text=text,instruction=instruction,seed=20261026+ri,max_new_tokens=256)
   graph['3']['inputs']['filename_prefix']=f'audio/BreezeTTS2/WhiteRice-English-v001/{ident}'
   for node in graph.values():
    schema=catalog[node['class_type']]['input']; required=schema.get('required',{})
    assert not set(required)-set(node['inputs']),node['class_type']
    for key,value in node['inputs'].items():
     if isinstance(value,list):
      assert value[0] in graph
      source=catalog[graph[value[0]]['class_type']]
      assert source['output'][value[1]]==required[key][0]
     else:
      spec=required.get(key,schema.get('optional',{}).get(key))
      assert spec is not None
      if isinstance(spec[0],list):assert value in spec[0]
      if len(spec)>1 and isinstance(spec[1],dict) and isinstance(value,(int,float)):
       assert spec[1].get('min',value)<=value<=spec[1].get('max',value)
   save(RECORD/f'{ident}-request.json',{'prompt':graph,'client_id':'white-rice-english-voice-auditions-v001'})
   manifest['candidates'].append(dict(id=ident,role=name,asset_id=asset_id,variant=variant,label=label,text=text,instruction=instruction,seed=20261026+ri,request=f'资产/生成记录/英语声线候选-v001/{ident}-request.json',status='prepared',schema_validated=True))
 save(RECORD/'manifest.json',manifest)
 return manifest

def render(manifest):
 sections=[]
 for slug,name,_,text,_ in ROLES:
  cards=[]
  for c in manifest['candidates']:
   if c['role']!=name or c['status']!='generated':continue
   filename=Path(c.get('preview_path',c['path'])).name
   cards.append(f'<article><h3>{c["variant"]} · {html.escape(c["label"])}</h3><audio controls preload="metadata" src="../../声音/英语声线候选-v001/{filename}"></audio><p>{c["seconds"]:.2f}秒 · 候选，未采用</p></article>')
  sections.append(f'<section><h2>{name}</h2><p>{html.escape(text)}</p><div class="pair">'+''.join(cards)+'</div></section>')
 page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · 英语声线试听</title><style>body{margin:40px auto;padding:0 24px;max-width:1100px;background:#131a23;color:#edf0f6;font:17px/1.8 system-ui}h1,h2{color:#eedbb4}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}article{padding:22px;background:#223040;border-radius:12px}audio{width:100%}section{margin:32px 0}p{color:#c8d3e0}@media(max-width:700px){.pair{grid-template-columns:1fr}}</style><h1>白米饭 · 英语声线试听</h1><p>小鱼、Claude、GPT各两版。同角色两版使用相同台词与参数，仅更换声线描述。先听音色是否贴合角色；不要求卡住镜头时长。所有版本均为候选，等你选择。</p><p>试听副本只做统一整体RMS的音量调整，未改音色、速度或音高；原始音频保留。此处理便于对比，不代表主观响度完全相同。卡片描述为设计目标，实际听感由你判断。</p>'''+''.join(sections)+'</html>'
 (RECORD/'试听.html').write_text(page,encoding='utf-8')

def run():
 # Re-running after interruption never silently duplicates submitted generations.
 manifest=load_manifest() if (RECORD/'manifest.json').exists() else prepare()
 q=api('/queue');assert not q['queue_running'] and not q['queue_pending'],'ComfyUI is busy; do not interrupt other work.'
 for c in manifest['candidates']:
  if c['status']=='generated':continue
  began=time.monotonic()
  if not c.get('prompt_id'):
   q=api('/queue');assert not q['queue_running'] and not q['queue_pending'],'Another task entered queue; pause candidates.'
   result=api('/prompt',json.loads((ROOT/c['request']).read_text('utf-8')))
   assert result.get('prompt_id') and not result.get('node_errors'),result
   c.update(status='submitted',prompt_id=result['prompt_id']);save(RECORD/'manifest.json',manifest)
  print('SUBMITTED',c['id'],c['prompt_id'],flush=True)
  deadline=time.monotonic()+600
  while time.monotonic()<deadline:
   hist=api('/history/'+c['prompt_id']).get(c['prompt_id'])
   if hist:
    save(RECORD/f'{c["id"]}-history.json',hist)
    assert hist['status']['status_str']=='success',hist['status']
    item=hist['outputs']['3']['audio'][0];native=COMFY/'output'/item['subfolder']/item['filename']
    audio,sr=sf.read(native,dtype='float32');seconds=len(audio)/sr
    assert sr==24000 and audio.ndim==1 and np.isfinite(audio).all() and 1<seconds<20.4
    peak=float(np.max(np.abs(audio)));assert peak>0.001
    target=MEDIA/f'{c["id"]}.flac';assert not target.exists(),'Never overwrite candidate audio'
    shutil.copy2(native,target);assert sha(native)==sha(target)
    c.update(status='generated',path=target.relative_to(ROOT).as_posix(),native_output=str(native),sha256=sha(target),seconds=seconds,sample_rate=sr,peak=peak,rms=float(np.sqrt(np.mean(audio**2))),elapsed_seconds=round(time.monotonic()-began,2),listening_status='pending_author_review')
    save(RECORD/'manifest.json',manifest);render(manifest);print('COMPLETED',c['id'],round(seconds,2),'seconds',flush=True);break
   time.sleep(4)
  else:raise TimeoutError(c['prompt_id'])
 manifest['status']='six_candidates_generated_pending_author_listening';finalize_previews(manifest)
 print('DONE six candidates, no voice adopted.',flush=True)
def finalize_previews(manifest):
 for c in manifest['candidates']:
  if c['role']=='ChatGPT':c['asset_id']='CHAR-GPT'
  source=ROOT/c['path'];assert sha(source)==c['sha256']
  audio,sr=sf.read(source,dtype='float32');gain=0.055/float(np.sqrt(np.mean(audio**2)));adjusted=audio*gain
  assert float(np.max(np.abs(adjusted)))<0.99
  target=MEDIA/f'{c["id"]}-preview.flac';sf.write(target,adjusted,sr,subtype='PCM_24')
  c.update(preview_path=target.relative_to(ROOT).as_posix(),preview_sha256=sha(target),preview_gain_db=round(float(20*np.log10(gain)),3))
 manifest['preview_processing']='统一整体RMS=0.055的常量增益；保留原件，不改音高/速度/音色；不代表主观响度完全一致。'
 save(RECORD/'manifest.json',manifest);render(manifest)
def load_manifest():return json.loads((RECORD/'manifest.json').read_text('utf-8'))
if __name__=='__main__':run()
