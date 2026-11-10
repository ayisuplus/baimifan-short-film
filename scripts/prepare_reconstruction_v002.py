"""Conform approved, local pickups into a new timeline while retaining original EDL."""
from pathlib import Path
import copy,json
R=Path(__file__).resolve().parents[1];O=R/'后期/声画重构-v002'
def read(p):return json.loads(p.read_text(encoding='utf8'))
P=read(R/'后期/导演后期修正-v001/后期执行计划.json');A=read(O/'采用剪辑.json'); FPS=24
def f(t):return round(t*FPS)
def part(s,a,b):
    z=copy.deepcopy(s);left=a-s['record'];right=b-s['record'];ratio=(s['out']-s['in'])/s['frames']
    if s['name'] in ['B17_GB014_01','B21_GB016-1_02','B25_GB018_01','B40_GB030-1_01','B42_GB031_02']:z['fusion_comp']=s['name']
    z.update(**{'in':s['in']+round(left*ratio),'out':s['in']+round(right*ratio),'frames':b-a})
    return z
edl=[];batches=[];maps={};cursor=0
for oldb in P['batches']:
    n=oldb['batch']; oldsegs=[s for s in P['edl'] if s['batch']==n]; edits=sorted([e for e in A['replacements'] if e['batch']==n],key=lambda e:e['start'])
    bstart=cursor;pos=0;local=[];knots=[[0,0]]
    def keep(a,b):
        for s in oldsegs:
            x=max(a+oldb['start'],s['record']);y=min(b+oldb['start'],s['record']+s['frames'])
            if y>x:local.append(part(s,x,y))
    for e in edits:
        a=f(e['start']);b=f(e['end']);assert pos<=a<=b<=oldb['frames'],(n,e,pos,oldb['frames'])
        keep(pos,a);knots.append([a/FPS,sum(s['frames'] for s in local)/FPS])
        for x in e['segments']:
            src=Path(x['source']);src=src if src.is_absolute() else R/src
            assert src.exists(),str(src)
            sf=f(x.get('in',0));ef=f(x['out']);frames=f(x.get('duration',x['out']-x.get('in',0)))
            local.append(dict(batch=n,source_batch=x.get('source_batch',n),source=str(src),**{'in':sf,'out':ef},frames=frames,props=x.get('props',{}),note=e['reason'],anchor=x.get('anchor'),new_pickup=x.get('new_pickup',False),fusion_comp=x.get('fusion_comp'),fx_flash=x.get('fx_flash',False)))
        knots.append([b/FPS,sum(s['frames'] for s in local)/FPS]);pos=b
    keep(pos,oldb['frames']);knots.append([oldb['frames']/FPS,sum(s['frames'] for s in local)/FPS])
    for j,s in enumerate(local,1):
        sp=Path(s['source']);s['source']=str(sp if sp.is_absolute() else R/sp)
        s.update(record=cursor,ordinal=j,name=f'B{n:02d}_{oldb["id"]}_{j:02d}',speed=100*(s['out']-s['in'])/s['frames']);cursor+=s['frames'];edl.append(s)
    batches.append({**oldb,'start':bstart,'frames':cursor-bstart,'v001_start':oldb['start'],'v001_frames':oldb['frames']})
    maps[str(n)]=knots
def maplocal(n,t):
    ks=maps[str(n)]
    for i in range(len(ks)-1):
        (a,x),(b,y)=ks[i:i+2]
        if a<=t<b:return x+(t-a)*(y-x)/(b-a)
    return ks[-1][1]
voices=copy.deepcopy(P['voice'])
for v in voices:
    vp=Path(v['path']);v['path']=str(vp if vp.is_absolute() else R/vp)
    n=v['batch'];local=(v['record']-P['batches'][n-1]['start'])/FPS
    v['record']=batches[n-1]['start']+f(maplocal(n,local))
    if v['id'] in A.get('voice_overrides',{}):
        ov=A['voice_overrides'][v['id']]
        if 'anchor' in ov:
            s=next(s for s in edl if s.get('anchor')==ov['anchor']);v['record']=s['record']+f(ov.get('offset',0))
        else:v['record']=batches[ov.get('batch',n)-1]['start']+f(ov['local'])
    assert v['record']+f(v['duration'])<=cursor,(v['id'],'end')
sortedv=sorted(voices,key=lambda v:v['record'])
for a,b in zip(sortedv,sortedv[1:]):assert a['record']/FPS+a['duration']<=b['record']/FPS+.001,(a['id'],b['id'])
result={**P,'timeline':'v002_Church_Sound_Reconstruction','edl':edl,'batches':batches,'voice':voices,'frames':cursor,'seconds':cursor/FPS,'batch_time_maps':maps,'status':'new_edit_candidate_pending_render_and_review'}
(O/'后期执行计划.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'seconds':cursor/FPS,'segments':len(edl),'voices':len(voices)},ensure_ascii=False))
