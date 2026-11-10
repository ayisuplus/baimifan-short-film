import json, pathlib, argparse
p=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser(); ap.add_argument('name');ap.add_argument('--prompt',required=True);ap.add_argument('--reference',required=True);ap.add_argument('--seconds',type=float,required=True);ap.add_argument('--seed',type=int,required=True);a=ap.parse_args()
w=json.loads((p/'035-r2.api.json').read_text('utf8'))
s=pathlib.Path(a.prompt).read_text('utf8')
w['7']['inputs']['image']=a.reference
w['8']['inputs'].update(prompt=s,duration_sec=a.seconds)
w['12']['inputs'].update(global_prompt=s,total_frames=round(a.seconds*24),seed=a.seed)
w['14']['inputs']['filename_prefix']='Baimifan/v028/'+a.name+'-no-upscale'
f=p/(a.name+'.api.json')
if f.exists(): raise SystemExit('Refusing to overwrite existing candidate')
f.write_text(json.dumps(w,ensure_ascii=False,indent=2),encoding='utf8')
print(f)
