"""One authorized Breeze audition using an English Japanese-anime-actress direction."""
import importlib.util, json, shutil, sys, time
from pathlib import Path
import numpy as np
import soundfile as sf
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('breeze_io', ROOT/'scripts/generate_breeze_voice_candidates_v001.py')
io = importlib.util.module_from_spec(spec); spec.loader.exec_module(io)
REC = ROOT/'资产/生成记录/小鱼英语声线-v006'
MEDIA = ROOT/'资产/声音/小鱼英语声线-v006'
INSTRUCTION = ('Japanese anime voice actress. A soft, rounded voice, lively and cute, with expressive anime character acting. '
 'Light, springy intonation and clean phrase endings. A small, hopeful smile in the invitation, '
 'a touch of stubbornness in the second line, and sincere conviction in the promise. Speak the given lines in clear English.')
def load(p): return json.loads(p.read_text('utf-8'))
def prepare():
 REC.mkdir(parents=True, exist_ok=True); MEDIA.mkdir(parents=True, exist_ok=True)
 if (REC/'manifest.json').exists(): return load(REC/'manifest.json')
 source = ROOT/'资产/生成记录/小鱼英语声线-v004/request.json'
 request = load(source); g = request['prompt']
 g['2']['inputs']['instruction'] = INSTRUCTION
 g['3']['inputs']['filename_prefix'] = 'audio/BreezeTTS2/WhiteRice-Xiaoyu-v006/seiyuu'
 request['client_id'] = 'xiaoyu-seiyuu-v006'
 catalog = io.api('/object_info')
 for n in g.values():
  required = catalog[n['class_type']]['input']['required']
  assert not set(required)-set(n['inputs'])
  for k,v in n['inputs'].items():
   s = required[k]
   if isinstance(v,list): assert catalog[g[v[0]]['class_type']]['output'][v[1]] == s[0]
   elif isinstance(s[0],list): assert v in s[0]
   elif len(s)>1 and isinstance(s[1],dict) and isinstance(v,(int,float)):
    assert s[1].get('min',v)<=v<=s[1].get('max',v)
 io.save(REC/'request.json', request); io.save(REC/'workflow.json', g)
 d = dict(version='v006', date='2026-10-26', role='小鱼', asset_id='CHAR-DEEPSEEK', engine='Breeze TTS 2', mode='VoiceDesign', language='English', status='prepared',
  text=g['2']['inputs']['text'], instruction=INSTRUCTION, authorization='作者要求最低成本试验：Breeze英文提示词写日本动漫女声优；一条小鱼英语候选。',
  comparison_source=source.relative_to(ROOT).as_posix(), comparison_source_sha256=io.sha(source),
  comparison='v004声音描述改写为英语，开头使用Japanese anime voice actress；保留柔软圆润和原表演目标。台词、seed和采样参数不变，无参考音。不是仅增加一个词的单变量测试。',
  request=(REC/'request.json').relative_to(ROOT).as_posix(), schema_validated=True, reference_audio=None, listening_status='pending_author_review')
 io.save(REC/'manifest.json',d); return d
def run():
 d = prepare()
 if d['status']=='generated': print('Already generated; no duplicate.'); return
 if not d.get('prompt_id'):
  q = io.api('/queue'); assert not q['queue_running'] and not q['queue_pending'], 'Queue busy'
  r = io.api('/prompt',load(REC/'request.json')); assert r.get('prompt_id') and not r.get('node_errors'),r
  d.update(status='submitted',prompt_id=r['prompt_id']); io.save(REC/'manifest.json',d)
 print('SUBMITTED',d['prompt_id'],flush=True)
 deadline=time.monotonic()+600
 while time.monotonic()<deadline:
  h=io.api('/history/'+d['prompt_id']).get(d['prompt_id'])
  if h:
   io.save(REC/'history.json',h); assert h['status']['status_str']=='success',h['status']
   item=h['outputs']['3']['audio'][0]; native=io.COMFY/'output'/item['subfolder']/item['filename']
   a,sr=sf.read(native,dtype='float32'); assert sr==24000 and a.ndim==1 and np.isfinite(a).all() and 1<len(a)/sr<20.4
   rms=float(np.sqrt(np.mean(a*a))); peak=float(np.max(np.abs(a))); assert rms>0.001
   raw=MEDIA/'xiaoyu-en-v006.flac'; assert not raw.exists(); shutil.copy2(native,raw); assert io.sha(raw)==io.sha(native)
   gain=min(0.055/rms,0.98/peak); preview=MEDIA/'xiaoyu-en-v006-preview.flac'; sf.write(preview,a*gain,sr,subtype='PCM_24')
   d.update(status='generated',path=raw.relative_to(ROOT).as_posix(),sha256=io.sha(raw),preview_path=preview.relative_to(ROOT).as_posix(),preview_sha256=io.sha(preview),seconds=len(a)/sr,sample_rate=sr,peak=peak,rms=rms,preview_gain_db=float(20*np.log10(gain)),native_output=str(native),processing='试听副本仅作常量音量调整；不变调、不变速，无配乐和混响，原件保留。')
   io.save(REC/'manifest.json',d); print('DONE',d['seconds'],'seconds',flush=True); return
  time.sleep(4)
 raise TimeoutError(d['prompt_id'])
if __name__=='__main__':
 if '--prepare' in sys.argv: prepare(); print('PREPARED')
 else: run()
