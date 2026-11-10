"""Versioned local ComfyUI preparation/validation/queue receipts; no editor internals."""
import argparse,copy,json,shutil,subprocess,sys,urllib.request
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
sys.path.insert(0,str(ROOT/'scripts'))
from gen_gate import assert_generation_allowed
COMFY=Path('G:/comfyui/ComfyUI/ComfyUI')
CLI='C:/Users/36322/.codex/runtimes/comfy-mcp/Scripts/comfy.exe'
INDEX={r['shot']:r for r in json.loads((ROOT/'后期/后半程逐镜审查-v031/镜头索引.json').read_text('utf8'))}
STYLE='Redraw the editable source image1 as traditional hand-drawn Japanese gothic fantasy anime, matching ONLY the drawing style of image2: confident clean dark ink contours, flat matte skin colors, hard-edged two-tone cel shadows, broad connected anime hair locks with simple highlight bands, graphic fabric folds and hand-drawn embroidery. Painted gouache background, consistent line weight and selective detail. Preserve source character identity, costume and story unless the specific correction says otherwise. No glossy 3D, plastic skin, realistic single hair strands, photorealistic cloth, PBR metal, CGI, excessive bloom, depth-of-field blur, text or captions. Preserve the source location and its time of day; style transfer must not import background objects. '
ANIM='Animate this exact hand-drawn 2D Japanese anime frame. Preserve ink outlines, hard-edged cel shading, flat matte skin, broad hair locks and painted gothic backgrounds throughout. Preserve identities, clothing, number of characters and established scenery. Intentional animation with anticipation, force, follow-through and settle; no loop, CGI, extra limbs, character morphing, unrelated cut, orbit or unmotivated zoom. '

def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def cli(args):
    p=subprocess.run([CLI,'--json','--where','local',*args],capture_output=True,text=True,encoding='utf8')
    envelopes=[json.loads(s) for s in p.stdout.splitlines() if s.startswith('{')]
    assert envelopes,(p.returncode,p.stderr[-600:])
    x=envelopes[-1];assert x.get('ok'),x
    return x
def plan():
    rows=json.loads((OUT/'shots.json').read_text('utf8'))
    for p in sorted(OUT.glob('group-*.json')):rows.extend(json.loads(p.read_text('utf8')))
    return rows
def prepare_keys(ids):
    template=json.loads((ROOT/'后期/小鱼脱手与二维统一-v030/041a-key-r1.api.json').read_text('utf8'))
    shutil.copy2(ROOT/'后期/Claude二维画风去重-v029/Claude-二维关键帧.png',COMFY/'input/Baimifan_v032_style.png')
    for s in plan():
        if s['id'] not in ids:continue
        src=OUT/'source'/f"{s['id']}.png";src.parent.mkdir(exist_ok=True)
        if s.get('source_override'):src=Path(s['source_override'])
        if not src.exists():
            subprocess.run(['ffmpeg','-v','error','-i',INDEX[s['source_shot']]['source'],'-vf',f"select=eq(n\\,{s.get('source_frame',0)})",'-frames:v','1','-pix_fmt','rgb24','-y',str(src)],check=True)
        name=f"Baimifan_v032_{s['id']}_source.png";shutil.copy2(src,COMFY/'input'/name)
        w=copy.deepcopy(template);w['1']['inputs']['image']=name;w['2']['inputs']['image']='Baimifan_v032_style.png'
        w['9']['inputs']['prompt']=STYLE+s['key_prompt'];w['10']['inputs']['seed']=202610303200+list(x['id'] for x in plan()).index(s['id'])
        if s.get('single_reference'):
            w['9']['inputs'].pop('images.image_2',None);w.pop('2',None)
            w['9']['inputs']['prompt']=w['9']['inputs']['prompt'].replace('matching ONLY the drawing style of image2:','using this exact visual language:')
        rev=s.get('key_revision',1)
        w['10']['inputs']['seed']+=1000*(rev-1)
        w['18']['inputs']['filename_prefix']=f"Baimifan/v032/{s['id']}-key-r{rev}"
        save(OUT/'workflows'/f"{s['id']}-key-r{rev}.api.json",w)
def prepare_videos(ids):
    template=json.loads((ROOT/'后期/小鱼脱手与二维统一-v030/037-video-r1.api.json').read_text('utf8'))
    approvals=json.loads((OUT/'key-approvals.json').read_text('utf8'))
    for s in plan():
        if s['id'] not in ids:continue
        assert approvals.get(s['id'])=='pass',s['id']
        src=COMFY/'output/Baimifan/v032'/f"{s['id']}-key-r{s.get('key_revision',1)}_00001_.png";assert src.exists(),src
        name=f"Baimifan_v032_{s['id']}_key.png";shutil.copy2(src,COMFY/'input'/name)
        (OUT/'keys').mkdir(exist_ok=True);shutil.copy2(src,OUT/'keys'/f"{s['id']}.png")
        w=copy.deepcopy(template);w['7']['inputs']['image']=name
        prompt=ANIM+s['motion_prompt'];frames=s['generate_frames']
        w['8']['inputs'].update(prompt=prompt,duration_sec=frames/24)
        w['12']['inputs'].update(global_prompt=prompt,total_frames=frames,seed=202610303500+list(x['id'] for x in plan()).index(s['id']))
        w['14']['inputs']['filename_prefix']=f"Baimifan/v032/{s['id']}-video-r1-no-upscale"
        save(OUT/'workflows'/f"{s['id']}-video-r1.api.json",w)
def submit(names):
    assert_generation_allowed()
    for name in names:
        receipt=OUT/'receipts'/f'{name}-submit.json'
        if receipt.exists():print(name,'already submitted',flush=True);continue
        wf=OUT/'workflows'/f'{name}.api.json';assert wf.exists(),wf
        v=cli(['workflow','validate','--workflow',str(wf),'--host','127.0.0.1','--port','8188'])
        save(OUT/'receipts'/f'{name}-validate.json',v);assert v['data']['valid'],v
        r=cli(['run','--workflow',str(wf),'--host','127.0.0.1','--port','8188','--no-watch']);save(receipt,r)
        print(name,r['data']['prompt_id'],flush=True)
def status():
    q=json.load(urllib.request.urlopen('http://127.0.0.1:8188/queue'))
    print('queue',len(q['queue_running']),len(q['queue_pending']))
    for p in sorted((OUT/'receipts').glob('*-submit.json')):
        r=json.loads(p.read_text('utf8'));pid=r['data']['prompt_id']
        hist=json.load(urllib.request.urlopen('http://127.0.0.1:8188/history/'+pid)).get(pid)
        if hist:
            save(OUT/'receipts'/p.name.replace('-submit','-history'),hist)
            print(p.stem,hist['status']['status_str'],[(v.get('filename'),v.get('subfolder')) for o in hist.get('outputs',{}).values() for vs in o.values() if isinstance(vs,list) for v in vs if isinstance(v,dict) and 'filename' in v])
        else:print(p.stem,'pending')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['keys','videos','submit','status']);p.add_argument('names',nargs='*');a=p.parse_args()
    {'keys':prepare_keys,'videos':prepare_videos,'submit':submit}.get(a.mode,lambda _:status())(a.names)
