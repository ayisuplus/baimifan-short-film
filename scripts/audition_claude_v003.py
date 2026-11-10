"""Bounded Claude A/B: only reference conditioning differs between A and B."""
import argparse, hashlib, json, shutil, subprocess, time, urllib.parse, urllib.request
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--prepare-only',action='store_true');a=p.parse_args();root=a.root.resolve()
base='http://127.0.0.1:8188';op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
def api(path,data=None):
    req=urllib.request.Request(base+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
    with op.open(req,timeout=30) as f:return json.loads(f.read())
def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
record_path=root/'资产/生成记录/Claude-少女声线对照-v003.json'
if record_path.exists():raise SystemExit('Existing run preserved; do not resubmit')
identity='十八岁少女声，清柔通透，轻盈自然的中高声区，清晰普通话。'
acting='为保护朋友，着急而坚定地短促喝止，收住尾音。'
jobs=[('A','别碰她！',identity+acting),('ANCHOR','别害怕，我会陪着你。等天亮了，我们一起离开这里。',identity+'安静克制，略带忧伤，自然说话。'),('B','别碰她！',identity+acting)]
prompts={}
for key,text,direction in jobs:
    inputs=dict(model_name='VoxCPM2',lora_name='None',text=text,voice_design=direction,cfg=2.0,steps=10,normalize_text=False,seed=20261021,force_offload=True,device='cuda',dtype='bf16',advanced_params=['30',0])
    graph={'24':{'class_type':'VoxCPM_TTS','inputs':inputs},'30':{'class_type':'VoxCPM_AdvancedParams','inputs':dict(min_tokens=2,max_tokens=2048,temperature=1.0,sway=1.0,use_cfg_zero_star=True,retry_max_attempts=3,retry_threshold=6.0)},'1':{'class_type':'SaveAudio','inputs':dict(audio=['24',0],filename_prefix=f'audio/chuanyun/VOICE-CLAUDE-v003-{key}')}}
    if key=='B':
        inputs['voice_config']=['22',0]
        graph['2']={'class_type':'LoadAudio','inputs':{'audio':'chuanyun_CLAUDE_anchor_v003.flac'}}
        graph['22']={'class_type':'VoxCPM_VoiceCloning','inputs':{'reference_audio':['2',0],'trim_silence':False,'prompt_text':''}}
    prompts[key]=graph
    path=root/f'资产/生成记录/VOICE-CLAUDE-v003-{key}-request.json'
    if path.exists():assert json.loads(path.read_text(encoding='utf-8'))==graph
    else:save(path,graph)
if a.prepare_only:raise SystemExit(0)
record=dict(engine='Local VoxCPM2',seed=20261021,comparison='A/B文字、种子和全部采样参数一致；B仅增加本轮合成的未采用少女参考。ANCHOR是声线测试文本，不改剧本。',status='running',listening_review='未实际听审；不声称B优于A或稳定性已经通过',results=[])
save(record_path,record)
for key,text,direction in jobs:
    q=api('/queue')
    if q['queue_running'] or q['queue_pending']:raise SystemExit('Queue busy; preserve partial results')
    if key=='B':
        source=root/'资产/声音/试音/VOICE-CLAUDE-v003-ANCHOR.flac'
        dest=Path(r'G:\comfyui\ComfyUI\ComfyUI\input\chuanyun_CLAUDE_anchor_v003.flac')
        if dest.exists():assert source.read_bytes()==dest.read_bytes()
        else:shutil.copy2(source,dest)
    graph=prompts[key]
    for node in graph.values():
        info=api('/object_info/'+node['class_type'])[node['class_type']]
        assert set(info['input']['required']).issubset(node['inputs'])
    result=dict(key=key,text=text,voice_design=direction,request=f'资产/生成记录/VOICE-CLAUDE-v003-{key}-request.json',status='prepared')
    record['results'].append(result);save(record_path,record)
    submitted=api('/prompt',{'prompt':graph,'client_id':'chuanyun-claude-v003'})
    result.update(prompt_id=submitted['prompt_id'],node_errors=submitted.get('node_errors',{}),status='queued');save(record_path,record)
    print(json.dumps({'key':key,'prompt_id':result['prompt_id']}),flush=True)
    end=time.monotonic()+360
    while time.monotonic()<end:
        h=api('/history/'+result['prompt_id'])
        if result['prompt_id'] in h:break
        time.sleep(3)
    else:raise SystemExit('Still running; prompt id saved, do not duplicate')
    h=h[result['prompt_id']];result['server_status']=h.get('status');save(record_path,record)
    media=h['outputs']['1']['audio'][0]
    with op.open(base+'/view?'+urllib.parse.urlencode(media)) as f:blob=f.read()
    dest=root/f'资产/声音/试音/VOICE-CLAUDE-v003-{key}.flac'
    if dest.exists():raise SystemExit('Preserve output')
    dest.write_bytes(blob)
    subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=sample_rate,channels','-of','json',str(dest)]))
    result.update(path=dest.relative_to(root).as_posix(),sha256=hashlib.sha256(blob).hexdigest(),native_output=media,probe=probe,status='generated_pending_listen')
    save(record_path,record);print(json.dumps({'key':key,'probe':probe}),flush=True)
record['status']='generated_pending_listen';save(record_path,record)
