"""Three first-line auditions on the installed local VoxCPM2; preserve all inputs."""
import argparse, hashlib, json, shutil, subprocess, time, urllib.parse, urllib.request
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,required=True); a=p.parse_args(); root=a.root.resolve()
base='http://127.0.0.1:8188'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
def api(path,data=None):
    req=urllib.request.Request(base+path,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json'})
    with opener.open(req,timeout=20) as r: return json.loads(r.read())
out=root/'资产/生成记录/主角试音-v001.json'
if out.exists(): raise SystemExit('Preserve existing audition run')
queue=api('/queue')
if queue['queue_running'] or queue['queue_pending']: raise SystemExit('Local queue busy; no submission')
info=api('/object_info/VoxCPM_TTS')['VoxCPM_TTS']
saveinfo=api('/object_info/SaveAudio')['SaveAudio']
record=dict(engine='VoxCPM2 local ComfyUI',endpoint=base,model_path='G:/comfyui/ComfyUI/ComfyUI/models/tts/VoxCPM/VoxCPM2',hardware=api('/system_stats'),transport_note='MCP server_info/validate/launch returned generic errors. Used the same installed server through loopback HTTP; bypassed proxy for localhost only. Server /prompt validates inputs before enqueue.',reference_audio=None,listening_status='未进行实际听审，未采用；不得当成全片配音',results=[])
jobs=[('DS','DeepSeek','CY003','你要吃一点吗？','年幼小女孩的声音，音色圆润柔软，清晰的普通话，自然地分享食物，轻轻询问，温柔可爱，语速稍慢。'),('GPT','ChatGPT','CY007','我不能插手教会的仪式。','年轻成年女性的声音，中低音，清冷、沉稳、克制，普通话清晰，语速稍慢，心中有犹豫但不外露，平静地拒绝。'),('CLAUDE','Claude','CY020','别碰她！','年轻女性的声音，细腻柔软，略微虚弱带气息。看到朋友被伤害，突然着急地出声阻止，短促有力，尾音力竭，普通话。')]
def freeze(): out.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
freeze()
for code,role,shot,text,direction in jobs:
    inputs=dict(model_name='VoxCPM2',lora_name='None',text=text,voice_design=direction,cfg=2.0,steps=10,normalize_text=False,seed=20261021,force_offload=True,device='cuda',dtype='bf16')
    assert set(info['input']['required']).issubset(inputs)
    prompt={'24':{'class_type':'VoxCPM_TTS','inputs':inputs},'1':{'class_type':'SaveAudio','inputs':{'audio':['24',0],'filename_prefix':f'audio/chuanyun/VOICE-{code}-v001'}}}
    request=root/f'资产/生成记录/VOICE-{code}-v001-request.json'
    request.write_text(json.dumps(prompt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    result=dict(role=role,shot_id=shot,text=text,request=request.relative_to(root).as_posix(),status='prepared')
    record['results'].append(result); freeze()
    try:
        submitted=api('/prompt',{'prompt':prompt,'client_id':'chuanyun-voice-audition-v001'})
        result.update(prompt_id=submitted['prompt_id'],validation_errors=submitted.get('node_errors',{}),status='queued'); freeze()
        print(json.dumps({'role':role,'prompt_id':result['prompt_id']},ensure_ascii=False),flush=True)
        until=time.monotonic()+360
        while time.monotonic()<until:
            history=api('/history/'+result['prompt_id'])
            if result['prompt_id'] in history: break
            time.sleep(3)
        else: raise RuntimeError('Still running after six minutes; retained prompt id, do not duplicate')
        h=history[result['prompt_id']]; result['server_status']=h.get('status')
        audios=h.get('outputs',{}).get('1',{}).get('audio',[])
        if not audios: raise RuntimeError('No SaveAudio output; inspect server_status')
        media=audios[0]; query=urllib.parse.urlencode(media)
        with opener.open(base+'/view?'+query,timeout=20) as r: blob=r.read()
        dest=root/f'资产/声音/试音/VOICE-{code}-v001.flac'; dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists(): raise RuntimeError('Output already exists')
        dest.write_bytes(blob)
        probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=sample_rate,channels','-of','json',str(dest)],capture_output=True,text=True,check=True)
        subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],capture_output=True,check=True)
        result.update(path=dest.relative_to(root).as_posix(),sha256=hashlib.sha256(blob).hexdigest(),probe=json.loads(probe.stdout),status='generated_pending_listen',native_output=media)
    except Exception as ex:
        result.update(status='failed_or_pending',error=str(ex)); freeze(); print(json.dumps(result,ensure_ascii=False),flush=True); break
    freeze(); print(json.dumps({'role':role,'path':result['path'],'probe':result['probe']},ensure_ascii=False),flush=True)
