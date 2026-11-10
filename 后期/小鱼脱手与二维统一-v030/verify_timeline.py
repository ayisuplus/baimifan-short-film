import json
from pathlib import Path
p=Path(__file__).resolve().parent
a=json.loads((p/'修改前DOM.json').read_text('utf8'))
b=json.loads((p/'修改后DOM.json').read_text('utf8'))
c=json.loads((p/'重新加载DOM.json').read_text('utf8'))
key=lambda x:float(x['left'][:-2])
for rows in (a,b,c):rows.sort(key=key)
assert b==c,'Reload changed timeline'
assert len(a)==len(b)==117
k=float(a[0]['width'][:-2])/234
replacements={'037_B13_v008_3818.mp4':'037_小鱼推离撑地_二维_v030.mp4','041_B15_GB012_01.mp4':'041_小鱼脱手与点火_二维_v030.mp4'}
pos=0
for old,new in zip(a,b):
    assert new['name']==replacements.get(old['name'],old['name']),(old,new)
    assert abs(float(old['left'][:-2])-float(new['left'][:-2]))<0.05,(old,new)
    assert abs(float(old['width'][:-2])-float(new['width'][:-2]))<0.05,(old,new)
    frames=round(float(new['width'][:-2])/k)
    assert abs(pos-float(new['left'][:-2])/k)<0.5,(pos,new)
    pos+=frames
assert pos==9142
r={'passed':True,'clips':117,'total_frames':9142,'fps':24,'duration':'00:06:20:22','reload_verified':True,'replacements':replacements,'other_115_clips_preserved':True,'all_positions_and_lengths_preserved':True,'export_verified':False}
(p/'时间线核对.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(r,ensure_ascii=False))
