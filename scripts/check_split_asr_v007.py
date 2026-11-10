"""Independent short-clip ASR evidence; never interpret as listening approval."""
from transcribe_selected_masters_v007 import ROOT,OUT,asr
import json,subprocess
import numpy as np
manifest=json.loads((OUT/'切分清单.json').read_text(encoding='utf8'))
result=[]
for c in manifest['candidates']:
    pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/c['file']),'-ar','16000','-ac','1','-f','f32le','-'])
    r=asr({'array':np.frombuffer(pcm,dtype=np.float32).copy(),'sampling_rate':16000},generate_kwargs={'language':'ja','task':'transcribe'},return_timestamps=False)
    result.append(dict(id=c['id'],take=c['take'],file=c['file'],sha256=c['sha256'],expected_reading_text=c['reading_text'],asr_text=r['text']))
    (OUT/'逐句ASR复核.json').write_text(json.dumps(dict(method='offline Whisper-small, short-clip transcription without text prompting; not listening approval',lines=result),ensure_ascii=False,indent=2),encoding='utf8')
    print(c['id'],c['take'],r['text'],flush=True)
