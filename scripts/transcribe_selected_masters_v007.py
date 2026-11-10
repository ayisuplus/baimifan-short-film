"""Offline ASR evidence for selected masters; no synthesis or adoption."""
import os
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
from pathlib import Path
import json, hashlib, subprocess
import numpy as np
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor, pipeline

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'声音/逐句切分审阅-v007'
OUT.mkdir(exist_ok=True)
MODEL = Path.home()/'.cache/huggingface/hub/models--openai--whisper-small/snapshots/973afd24965f72e36ca33b3055d56a652f456b4d'
inventory = json.loads((ROOT/'声音/正式配音准备-v006/正式配音清单.json').read_text(encoding='utf8'))
torch.set_num_threads(4)
model = WhisperForConditionalGeneration.from_pretrained(str(MODEL), local_files_only=True, torch_dtype=torch.float16, attn_implementation='eager').to('cuda')
processor = WhisperProcessor.from_pretrained(str(MODEL), local_files_only=True)
asr = pipeline('automatic-speech-recognition', model=model, tokenizer=processor.tokenizer, feature_extractor=processor.feature_extractor, device=0)
for role in ['Claude','GPT','Kimi','教主','千问','教徒']:
    src = ROOT/inventory['voice_assets'][role]['file']
    sha = hashlib.sha256(src.read_bytes()).hexdigest()
    assert sha == inventory['voice_assets'][role]['sha256']
    dest = OUT/(role+'-ASR.json')
    if dest.exists():
        assert json.loads(dest.read_text(encoding='utf8'))['source_sha256'] == sha
        print('existing',role,flush=True)
        continue
    pcm = subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-ar','16000','-ac','1','-f','f32le','-'])
    arr = np.frombuffer(pcm,dtype=np.float32).copy()
    print('transcribing',role,len(arr)/16000,flush=True)
    result = asr({'array':arr,'sampling_rate':16000}, chunk_length_s=25, stride_length_s=3, return_timestamps='word',generate_kwargs={'language':'ja','task':'transcribe'})
    record = dict(source=src.relative_to(ROOT).as_posix(),source_sha256=sha,seconds=len(arr)/16000,model=str(MODEL),method='offline Whisper-small; unprompted Japanese word timestamps; not human listening or performance approval',result=result)
    dest.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
    print('saved',role,flush=True)
