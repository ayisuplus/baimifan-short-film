from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'后期/二维动漫纠偏-v005';G=R/'视频制作/Metaso-H3-v009/产物'
def seg(aid,lo,hi,record,batch,props=None):return dict(source=str(G/(aid+'.mp4')),**{'in':lo,'out':hi},record=record,frames=hi-lo,speed=100,batch=batch,props=props or {},name=f'B{batch:02d}_v005_2D_{record}',note='二维动漫纠偏；翼面细节避开无声提前张嘴，有声段及闭口尾均原速；原声音位置不变')
aid='GB018-v009-gpt-rise-2d-r1';z=1344/544
edits=[dict(start=6476,end=6650,segments=[seg(aid,0,84,6476,25),seg(aid,84,102,6560,25,dict(ZoomX=z,ZoomY=z,Pan=400*z,Tilt=-231*z+12)),seg(aid,102,152,6578,25),seg(aid,162,184,6628,25)]),dict(start=2126,end=2174,segments=[seg('GB006-v009-early-inside-2d-r1',36,84,2126,7)])]
edits[1]['segments'][0]['note']='二维动漫入洞过渡；手膝承重末段到抬眼定势，原速48帧，不加对白'
(O/'剪辑修正增量.json').write_text(json.dumps(dict(replace_edits=edits),ensure_ascii=False,indent=2),encoding='utf8')
print('Four-segment wing plan and redrawn inside source; validate candidate before applying')
