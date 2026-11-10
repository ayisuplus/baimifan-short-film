"""One authorized Xiaoyu candidate with literal Chinese anime wording."""
import importlib.util,json,shutil,time
from pathlib import Path
import numpy as np
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('breeze_io',ROOT/'scripts/generate_breeze_voice_candidates_v001.py')
io=importlib.util.module_from_spec(spec);spec.loader.exec_module(io)
REC=ROOT/'资产/生成记录/小鱼英语声线-v004'
MEDIA=ROOT/'资产/声音/小鱼英语声线-v004'
TEXT="Would you like some? One more try. I'll get you out of here."
INSTRUCTION='二次元动漫角色女声。音色柔软、圆润，灵动可爱，有鲜明的动漫配音感。说话有表情，语调轻巧、有弹性，句尾干净。邀请时带期待的小笑意，坚持时有一点小倔强，承诺时认真笃定。用清晰的英语说给定台词。'
def load(p):return json.loads(p.read_text('utf-8'))
def run():
 q=io.api('/queue');assert not q['queue_running'] and not q['queue_pending'],'Queue busy'
 REC.mkdir(parents=True,exist_ok=True);MEDIA.mkdir(parents=True,exist_ok=True)
 if (REC/'manifest.json').exists():d=load(REC/'manifest.json')
 else:
  g=load(Path('G:/comfyui/ComfyUI/workflow/BreezeTTS2-deploy/voice-design-api.json'))
  g['2']['inputs'].update(text=TEXT,instruction=INSTRUCTION,seed=20261027)
  g['3']['inputs']['filename_prefix']='audio/BreezeTTS2/WhiteRice-Xiaoyu-v004/literal-anime'
  catalog=io.api('/object_info')
  for n in g.values():
   req=catalog[n['class_type']]['input']['required'];assert not set(req)-set(n['inputs'])
   for k,v in n['inputs'].items():
    if isinstance(v,list):assert catalog[g[v[0]]['class_type']]['output'][v[1]]==req[k][0]
    elif isinstance(req[k][0],list):assert v in req[k][0]
  io.save(REC/'request.json',dict(prompt=g,client_id='xiaoyu-literal-anime-v004'))
  d=dict(version='v004',date='2026-10-26',role='小鱼',asset_id='CHAR-DEEPSEEK',engine='Breeze TTS 2',mode='VoiceDesign',status='prepared',text=TEXT,instruction=INSTRUCTION,
   authorization='作者要求先做好小鱼，暂停其他角色，并直接在提示词里写二次元。本次一条候选。',
   approach='直接使用中文声音描述并写明二次元动漫角色；朗读文本仍为英语。无参考音，保留柔软圆润的设计目标，不克隆旧真人儿童质感。指令语言采用中文是本次实验选择，不保证跨语言风格指令一定有效。',
   previous_feedback='B2表演方向更接近，但仍像欧美真人儿童演员；其他角色也仍有真人感，全部暂未定稿。',
   request='资产/生成记录/小鱼英语声线-v004/request.json',schema_validated=True,reference_audio=None,listening_status='pending_author_review')
  io.save(REC/'manifest.json',d)
 if d['status']=='generated':print('Already generated; no duplicate task.');return
 if not d.get('prompt_id'):
  r=io.api('/prompt',load(REC/'request.json'));assert r.get('prompt_id') and not r.get('node_errors'),r
  d.update(status='submitted',prompt_id=r['prompt_id']);io.save(REC/'manifest.json',d)
 print('SUBMITTED',d['prompt_id'],flush=True);deadline=time.monotonic()+600
 while time.monotonic()<deadline:
  h=io.api('/history/'+d['prompt_id']).get(d['prompt_id'])
  if h:
   io.save(REC/'history.json',h);assert h['status']['status_str']=='success',h['status']
   item=h['outputs']['3']['audio'][0];native=io.COMFY/'output'/item['subfolder']/item['filename'];a,sr=sf.read(native,dtype='float32')
   assert sr==24000 and a.ndim==1 and np.isfinite(a).all() and 1<len(a)/sr<20.4
   rms=float(np.sqrt(np.mean(a*a)));peak=float(np.max(np.abs(a)));assert rms>0.001
   raw=MEDIA/'xiaoyu-v004.flac';assert not raw.exists();shutil.copy2(native,raw);assert io.sha(raw)==io.sha(native)
   gain=min(0.055/rms,0.98/peak);preview=MEDIA/'xiaoyu-v004-preview.flac';sf.write(preview,a*gain,sr,subtype='PCM_24')
   d.update(status='generated',path=raw.relative_to(ROOT).as_posix(),sha256=io.sha(raw),preview_path=preview.relative_to(ROOT).as_posix(),preview_sha256=io.sha(preview),seconds=len(a)/sr,sample_rate=sr,peak=peak,rms=rms,preview_gain_db=float(20*np.log10(gain)),native_output=str(native),processing='试听副本只作常量音量调整；不变调、不变速，原件保留。')
   io.save(REC/'manifest.json',d);print('DONE',d['seconds'],'seconds',flush=True);return
  time.sleep(4)
 raise TimeoutError(d['prompt_id'])
if __name__=='__main__':run()
