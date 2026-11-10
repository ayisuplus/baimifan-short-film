"""Unprompted offline ASR of newly completed dialogue; not perceptual approval."""
from transcribe_selected_masters_v007 import ROOT,asr
import json,subprocess
import numpy as np
out=ROOT/'声音/缺口补齐-v008'
result=[]
for p in sorted(out.glob('VO-*-结果.json')):
    c=json.loads(p.read_text(encoding='utf8'))
    if c['status']!='saved_pending_review':continue
    pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/c['file']),'-ar','16000','-ac','1','-f','f32le','-'])
    r=asr({'array':np.frombuffer(pcm,dtype=np.float32).copy(),'sampling_rate':16000},generate_kwargs={'language':'ja','task':'transcribe'},return_timestamps=False)
    result.append(dict(id=c['line_id'],file=c['file'],sha256=c['sha256'],expected=c['body']['text'],asr=r['text']))
    (out/'补录ASR复核.json').write_text(json.dumps({'method':'Whisper-small offline unprompted Japanese; not listening approval','lines':result},ensure_ascii=False,indent=2),encoding='utf8')
    print(c['line_id'],r['text'],flush=True)
