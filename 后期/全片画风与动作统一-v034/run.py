"""Versioned local-only Qwen/H3 production, explicit inputs and approval records."""
import argparse,json,copy,subprocess,shutil,sys
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parent.parent
sys.path.insert(0,str(ROOT/'scripts'))
from gen_gate import assert_generation_allowed
C=Path('G:/comfyui/ComfyUI/ComfyUI')
CLI='C:/Users/36322/.codex/runtimes/comfy-mcp/Scripts/comfy.exe'
def save(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),'utf8')
def cli(args):
 p=subprocess.run([CLI,'--json','--where','local',*args],capture_output=True,text=True,encoding='utf8')
 lines=[json.loads(x) for x in p.stdout.splitlines() if x.startswith('{')]
 assert lines,(p.returncode,p.stderr[-600:])
 v=lines[-1];assert v.get('ok'),v
 return v
def prepare(job):
 name=job['name'];dest=P/'workflows'/f'{name}.api.json'
 assert not dest.exists(),'Immutable workflow exists: '+name
 if job['type']=='key':
  w=json.loads((ROOT/'后期/后半程逐段修订-v032/workflows/066-key-r2.api.json').read_text('utf8'))
  image=job['source'];input_name=f'Baimifan_v034_{name}.png';shutil.copy2(image,C/'input'/input_name)
  w['1']['inputs']['image']=input_name
  w['9']['inputs']['prompt']=job['prompt']
  if job.get('style_source'):
   style_name=f'Baimifan_v034_{name}_style.png';shutil.copy2(job['style_source'],C/'input'/style_name)
   w['2']={'class_type':'LoadImage','inputs':{'image':style_name}}
   w['9']['inputs']['images.image_2']=['2',0]
  w['10']['inputs']['seed']=job['seed'];w['18']['inputs']['filename_prefix']='Baimifan/v034/'+name
 else:
  assert job.get('key_review')=='pass','Key must be viewed before video'
  w=json.loads((ROOT/'后期/小鱼脱手与二维统一-v030/037-video-r1.api.json').read_text('utf8'))
  image=job['source'];input_name=f'Baimifan_v034_{name}.png';shutil.copy2(image,C/'input'/input_name)
  w['7']['inputs']['image']=input_name
  w['8']['inputs'].update(prompt=job['prompt'],duration_sec=job['frames']/24)
  w['12']['inputs'].update(global_prompt=job['prompt'],total_frames=job['frames'],seed=job['seed'])
  w['14']['inputs']['filename_prefix']='Baimifan/v034/'+name
 assert all(not any(x in n['class_type'].lower() for x in ['upscale','supir','flashvsr']) for n in w.values())
 save(dest,w);save(P/'jobs'/f'{name}.json',job)
 return dest
def submit(name):
 assert_generation_allowed()
 receipt=P/'receipts'/f'{name}-submit.json';assert not receipt.exists(),'Existing receipt; inspect before resubmitting'
 w=P/'workflows'/f'{name}.api.json'
 v=cli(['workflow','validate','--workflow',str(w),'--host','127.0.0.1','--port','8188']);save(P/'receipts'/f'{name}-validate.json',v);assert v['data']['valid']
 r=cli(['run','--workflow',str(w),'--host','127.0.0.1','--port','8188','--no-watch']);save(receipt,r)
 print(name,r['data']['prompt_id'],flush=True)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('mode',choices=['prepare','submit']);a.add_argument('items',nargs='+');args=a.parse_args()
 if args.mode=='prepare':
  for f in args.items:
   for job in json.loads(Path(f).read_text('utf8')):prepare(job)
 else:
  for name in args.items:submit(name)
