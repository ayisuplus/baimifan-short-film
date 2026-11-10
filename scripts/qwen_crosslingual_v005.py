"""Reuse the running local IndexTTS service; one Chinese-reference Japanese trial."""
from pathlib import Path
import json,shutil,hashlib,urllib.request,subprocess,time
from gradio_client import Client, handle_file
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'声音/千问跨语言试音-v005'
def write(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
native=Path('G:/comfyui/ComfyUI/ComfyUI/output/audio/BreezeTTS2/WhiteRice-Qwen-v005/Chinese-Design_00001.flac')
ref=OUT/'千问-Breeze-中文原声.flac'
if not ref.exists():shutil.copy2(native,ref)
assert sha(native)==sha(ref)
hist=json.load(urllib.request.urlopen('http://127.0.0.1:8188/history/869d8ff1-c6f3-47c3-a9d0-73111b75d9e9'))
write('Breeze-完成回执.json',hist)
assert hist['869d8ff1-c6f3-47c3-a9d0-73111b75d9e9']['status']['status_str']=='success'
q=json.load(urllib.request.urlopen('http://127.0.0.1:8188/queue'))
assert not q['queue_running'] and not q['queue_pending'],'ComfyUI busy'
for p in [ref]:subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
record=OUT/'IndexTTS-日语结果.json'
if record.exists():print('Existing result preserved; no repeat request');raise SystemExit(0)
request={'engine':'IndexTTS-2.5','api':'http://127.0.0.1:7860','endpoint':'/gen_single','reference':ref.name,'reference_sha256':sha(ref),'text':'行きましょう。つかまって。','lang_choice':'JA','emo_control_method':'与音色参考音频相同','duration_factor':1.0,'emo_random':False,'voice_approved':False}
request_path=OUT/'IndexTTS-日语请求.json'
if request_path.exists() and json.loads(request_path.read_text(encoding='utf8')).get('status')!='client_validation_failed':raise RuntimeError('An uncompleted submission record exists; inspect server before retry')
write(request_path.name,request)
client=Client('http://127.0.0.1:7860',verbose=False)
start=time.time()
result=client.predict(prompt=handle_file(str(ref)),text=request['text'],lang_choice='JA',emo_ref_path=None,emo_control_method=request['emo_control_method'],duration_factor=1.0,emo_random=False,api_name='/gen_single')
write('IndexTTS-服务回执.json',{'result':result,'elapsed_seconds':time.time()-start})
path=result.get('value') if isinstance(result,dict) else result
if isinstance(path,dict):path=path['path']
assert isinstance(path,str) and Path(path).is_file(),result
target=OUT/'千问-IndexTTS-日语克隆.wav'
assert not target.exists()
shutil.copy2(path,target)
subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
audios=[]
for p in [ref,target]:
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=sample_rate,channels','-of','json',str(p)]))
 audios.append({'file':p.name,'sha256':sha(p),'probe':probe,'decode_ok':True})
write(record.name,{'request':request_path.name,'status':'generated_pending_listening','native_result':path,'audios':audios})
print(json.dumps(audios,ensure_ascii=False))
