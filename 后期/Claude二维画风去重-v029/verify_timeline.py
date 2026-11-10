import json, pathlib
p=pathlib.Path(__file__).resolve().parent
a=json.loads((p/'修改前DOM.json').read_text('utf8'));b=json.loads((p/'修改后DOM.json').read_text('utf8'));c=json.loads((p/'重新加载DOM.json').read_text('utf8'))
key=lambda x:float(x['left'][:-2]);a.sort(key=key);b.sort(key=key);c.sort(key=key)
assert b==c,'Reload changed timeline'
k=float(a[0]['width'][:-2])/234
spec=[];pos=0
for x in a:
 name=x['name'];frames=round(float(x['width'][:-2])/k)
 if name.startswith('039_'):continue
 if name.startswith('035_'):name='035_Claude二维制止_v029.mp4'
 if name.startswith('038_'):name='038_Claude二维恳求_v029.mp4';frames-=18
 spec.append({'name':name,'frames':frames,'start':pos});pos+=frames
assert len(b)==117 and pos==9142
for x,y in zip(spec,b):
 assert x['name']==y['name'],(x,y)
 assert x['frames']==round(float(y['width'][:-2])/k),(x,y)
 assert abs(x['start']-float(y['left'][:-2])/k)<0.5,(x,y)
r={'passed':True,'clips':len(b),'total_frames':pos,'fps':24,'duration':'00:06:20:22','reload_verified':True,'replacement_shots':['035','038'],'removed_shot':'039','removed_frames':48,'remaining_content_and_lengths_preserved':True,'only_downstream_shift_frames':-48}
(p/'时间线核对.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(r,ensure_ascii=False))
