"""Small Japanese voice-clone validation in the isolated official IndexTTS 2.5 environment."""
from pathlib import Path
import os,sys,json,hashlib,time,urllib.request
ROOT=Path(__file__).resolve().parents[1]
ENGINE=Path('G:/IndexTTS-2.5')
OUT=ROOT/'声音/声线返修试听-v004'
os.chdir(ENGINE);sys.path.insert(0,str(ENGINE))
os.environ['USE_MODELSCOPE']='false'
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
os.environ['GRADIO_ANALYTICS_ENABLED']='False'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
try:
    with opener.open('http://127.0.0.1:8188/queue',timeout=10) as r:q=json.load(r)
    assert not q['queue_running'] and not q['queue_pending'],'ComfyUI busy: postpone GPU inference'
except ConnectionRefusedError:pass
import numpy as np
import soundfile as sf
import torch
from indextts.infer_v2_5 import IndexTTS2
assert torch.cuda.is_available()
ref=ROOT/'后期/日语配音修正-v004/切分输入/VO-CY026A1-01__Qwen__ja__v004.wav'
jobs=[('千问-IndexTTS25-旧声线验证','行きましょう。つかまって。',None),('千问-IndexTTS25-从容表演','行きましょう。つかまって。',[0,0,0,0,0,0,0,0.7])]
pending=[x for x in jobs if not (OUT/(x[0]+'.json')).exists()]
if not pending:print('Already completed; no duplicate generation');sys.exit(0)
tts=IndexTTS2(cfg_path='checkpoints/config.yaml',model_dir='checkpoints',use_bf16=True,use_cuda_kernel=False,use_qwen_emo=False)
for name,text,emotion in pending:
    target=OUT/(name+'.wav')
    if target.exists():raise RuntimeError('Unrecorded output exists; inspect before retry: '+str(target))
    torch.manual_seed(20261029)
    started=time.time()
    kwargs={'emo_vector':emotion} if emotion else {}
    tts.infer(spk_audio_prompt=str(ref),text=text,lang='JA',output_path=str(target),verbose=False,use_random=False,**kwargs)
    y,sr=sf.read(target)
    assert len(y)>sr*0.5 and np.isfinite(y).all()
    record={'engine':'IndexTTS-2.5','role':'千问','purpose':'日语链路验证；旧声线参考不是新设计采用','reference':str(ref),'reference_sha256':hashlib.sha256(ref.read_bytes()).hexdigest(),'text':text,'language':'JA','emotion_vector':emotion,'seed':20261029,'seconds':len(y)/sr,'sample_rate':sr,'elapsed_seconds':time.time()-started,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'listening_approved':False,'file':target.name}
    (OUT/(name+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(record,ensure_ascii=False),flush=True)
