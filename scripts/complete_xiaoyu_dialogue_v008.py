"""Authorized local IndexTTS completion, using the running server and original voice."""
from pathlib import Path
import json,hashlib,time,shutil,urllib.request
from gradio_client import Client,handle_file
import soundfile as sf
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'声音/缺口补齐-v008'
lines=[x for x in json.loads((ROOT/'声音/逐句切分审阅-v007/切分清单.json').read_text(encoding='utf8'))['missing_lines'] if x['role']=='小鱼']
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
with opener.open('http://127.0.0.1:8188/queue',timeout=5) as f:q=json.load(f)
assert not q['queue_running'] and not q['queue_pending'],'ComfyUI busy; do not contend with an executing task'
ref=ROOT/'后期/导演重构-v003/声音/VO-CY006-01-工作源.wav'
assert ref.exists()
client=Client('http://127.0.0.1:7860',verbose=False)
for line in lines:
    receipt=OUT/(line['id']+'-结果.json')
    assert not receipt.exists(),'Existing receipt: inspect before retry'
    params={'emo_control_method':'与音色参考音频相同','prompt':handle_file(str(ref)),'text':line['tts_reading_text'],'lang_choice':'JA','emo_ref_path':None,'emo_weight':0.65,'emo_random':False,'duration_factor':1.0,'param_18':False,'param_23':3}
    meta={'line_id':line['id'],'role':'小鱼','line':line,'engine':'IndexTTS-2.5 running local UI','endpoint':'http://127.0.0.1:7860','authorization':'2026-10-29 user explicitly approved local IndexTTS referencing original Xiaoyu voice for these three gaps','reference':str(ref),'reference_sha256':hashlib.sha256(ref.read_bytes()).hexdigest(),'body':{'text':line['tts_reading_text'],'language':'JA','emotion':'same as original reference','duration_factor':1.0,'do_sample':False,'num_beams':3},'status':'outcome_unknown_do_not_repeat','author_performance_accepted':False}
    receipt.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
    start=time.time();r=client.predict(**params,api_name='/gen_single')
    if isinstance(r,dict):r=r.get('value',r.get('path'))
    if isinstance(r,dict):r=r['path']
    p=Path(r);assert p.exists(),repr(r)
    target=OUT/(line['id']+'__小鱼.wav');shutil.copy2(p,target)
    y,sr=sf.read(target)
    assert len(y)>sr*.15 and np.isfinite(y).all()
    meta.update(status='saved_pending_review',file=target.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),sample_rate=sr,seconds=len(y)/sr,elapsed_seconds=time.time()-start,local_server_output=str(p),decode_ok=True)
    receipt.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'id':line['id'],'seconds':meta['seconds'],'elapsed':meta['elapsed_seconds']},ensure_ascii=False),flush=True)
