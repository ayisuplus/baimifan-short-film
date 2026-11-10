"""One Chinese-language audition, holding the v004 voice description and settings fixed."""
import importlib.util,json,shutil,time
from pathlib import Path
import numpy as np
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('breeze_io',ROOT/'scripts/generate_breeze_voice_candidates_v001.py')
io=importlib.util.module_from_spec(spec);spec.loader.exec_module(io)
REC=ROOT/'资产/生成记录/小鱼中文声线-v005'
MEDIA=ROOT/'资产/声音/小鱼中文声线-v005'
def load(p):return json.loads(p.read_text('utf-8'))
def run():
 q=io.api('/queue');assert not q['queue_running'] and not q['queue_pending'],'Queue busy'
 REC.mkdir(parents=True,exist_ok=True);MEDIA.mkdir(parents=True,exist_ok=True)
 if (REC/'manifest.json').exists():d=load(REC/'manifest.json')
 else:
  previous=ROOT/'资产/生成记录/小鱼英语声线-v004/request.json';request=load(previous)
  g=request['prompt'];g['2']['inputs']['text']='你要吃一点吗？再试一下。我带你出去。'
  g['2']['inputs']['instruction']=g['2']['inputs']['instruction'].replace('英语','中文')
  g['3']['inputs']['filename_prefix']='audio/BreezeTTS2/WhiteRice-Xiaoyu-Chinese-v005/xiaoyu'
  request['client_id']='xiaoyu-chinese-v005';catalog=io.api('/object_info')
  for n in g.values():
   req=catalog[n['class_type']]['input']['required'];assert not set(req)-set(n['inputs'])
   for k,v in n['inputs'].items():
    if isinstance(v,list):assert catalog[g[v[0]]['class_type']]['output'][v[1]]==req[k][0]
    elif isinstance(req[k][0],list):assert v in req[k][0]
  io.save(REC/'request.json',request)
  d=dict(version='v005',date='2026-10-26',role='小鱼',asset_id='CHAR-DEEPSEEK',engine='Breeze TTS 2',mode='VoiceDesign',language='Chinese',status='prepared',text=g['2']['inputs']['text'],instruction=g['2']['inputs']['instruction'],
   authorization='作者要求改说中文试一试；本轮仅小鱼一条中文试听。',
   comparison_source='资产/生成记录/小鱼英语声线-v004/request.json',comparison_source_sha256=io.sha(previous),
   comparison='仅将朗读文本换为对应中文原句、语言指令英语换为中文，模型、seed、所有采样参数与其余声音描述保持；无参考音。语言改变仍可能改变生成音色，不声称声音身份已固定。',
   scope='未切换全片生成板执行语言；其他角色暂停；语种和固定声线均待作者试听决定。',
   request='资产/生成记录/小鱼中文声线-v005/request.json',schema_validated=True,listening_status='pending_author_review')
  io.save(REC/'manifest.json',d)
 if d['status']=='generated':print('Already generated; no duplicate.');return
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
   raw=MEDIA/'xiaoyu-zh-v005.flac';assert not raw.exists();shutil.copy2(native,raw);assert io.sha(raw)==io.sha(native)
   gain=min(0.055/rms,0.98/peak);preview=MEDIA/'xiaoyu-zh-v005-preview.flac';sf.write(preview,a*gain,sr,subtype='PCM_24')
   d.update(status='generated',path=raw.relative_to(ROOT).as_posix(),sha256=io.sha(raw),preview_path=preview.relative_to(ROOT).as_posix(),preview_sha256=io.sha(preview),seconds=len(a)/sr,sample_rate=sr,peak=peak,rms=rms,preview_gain_db=float(20*np.log10(gain)),native_output=str(native),processing='常量音量调整的试听副本；无变调、变速、配乐或混响，原件保留。')
   io.save(REC/'manifest.json',d);print('DONE',d['seconds'],'seconds',flush=True);return
  time.sleep(4)
 raise TimeoutError(d['prompt_id'])
if __name__=='__main__':run()
