"""Rebuild and preflight API graphs only. Does not upload or submit GPU jobs."""
import json,pathlib,subprocess
p=pathlib.Path(r'E:\projects\内容创作\故事短片\白米饭\后期\图片超分对比-20261031')
cli=r'C:\Users\36322\.codex\runtimes\comfy-mcp\Scripts\comfy.exe'
def call(args,receipt):
 r=subprocess.run([cli,'--json','--where','local']+args,capture_output=True,encoding='utf-8'); (p/'receipts'/receipt).write_text(r.stdout,encoding='utf-8')
 d=json.loads(r.stdout); print(receipt, json.dumps(d,ensure_ascii=False)[:1300],flush=True)
 if not d.get('ok'): raise RuntimeError(d)
 return d
for s in json.loads((p/'samples.json').read_text(encoding='utf-8-sig')):
 for method in ['realesrgan','seedvr2','rtx']:
  w,h=s['target_size']; wf={'1':{'class_type':'LoadImage','inputs':{'image':pathlib.Path(s['input']).name}}}
  if method=='realesrgan':
   wf['2']={'class_type':'UpscaleModelLoader','inputs':{'model_name':'RealESRGAN_x4plus.safetensors'}}
   wf['3']={'class_type':'ImageUpscaleWithModel','inputs':{'upscale_model':['2',0],'image':['1',0]}}
  elif method=='seedvr2':
   wf['2']={'class_type':'SeedVR2LoadDiTModel','inputs':{'model':'seedvr2_ema_7b-Q8_K_M.gguf','device':'cuda:0','blocks_to_swap':32,'swap_io_components':False,'offload_device':'cpu','cache_model':False,'attention_mode':'sdpa'}}
   wf['4']={'class_type':'SeedVR2LoadVAEModel','inputs':{'model':'ema_vae_fp16.safetensors','device':'cuda:0','encode_tiled':True,'encode_tile_size':1024,'encode_tile_overlap':128,'decode_tiled':True,'decode_tile_size':1024,'decode_tile_overlap':128,'tile_debug':'false','offload_device':'cpu','cache_model':False}}
   wf['3']={'class_type':'SeedVR2VideoUpscaler','inputs':{'image':['1',0],'dit':['2',0],'vae':['4',0],'seed':20261031,'resolution':h,'max_resolution':3840,'batch_size':1,'uniform_batch_size':False,'color_correction':'lab','temporal_overlap':0,'prepend_frames':0,'input_noise_scale':0.0,'latent_noise_scale':0.0,'offload_device':'cpu','enable_debug':False}}
  else:
   wf['3']={'class_type':'RTXVideoSuperResolution','inputs':{'images':['1',0],'resize_type':'target dimensions','resize_type.width':3840,'resize_type.height':round(h/8)*8,'quality':'ULTRA'}}
  wf['5']={'class_type':'ImageScale','inputs':{'image':['3',0],'upscale_method':'lanczos','width':w,'height':h,'crop':'disabled'}}
  wf['6']={'class_type':'SaveImage','inputs':{'images':['5',0],'filename_prefix':f'Baimifan/Upscale_20261031/{s["id"]}_{method}'}}
  name=s['id']+'_'+method; f=p/'workflows'/(name+'.api.json'); f.write_text(json.dumps(wf,indent=2),encoding='utf-8')
  d=call(['workflow','validate','--workflow',str(f),'--host','127.0.0.1','--port','8188'],name+'-validate.json')
  if d['data'].get('valid') is not True:raise RuntimeError('invalid workflow')
