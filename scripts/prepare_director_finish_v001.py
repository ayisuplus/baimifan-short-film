"""Build a versioned, source-preserving edit plan for the current 44 candidates."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'后期/导演后期修正-v001';OUT.mkdir(exist_ok=True)
A=json.loads((ROOT/'后期/导演全片审查-v001/当前44批审查清单.json').read_text(encoding='utf8'))
FPS=24
def fr(t):return round(t*FPS)
def seg(b,ins,outs,dur=None,props=None,note='',source=None):
    sb=A[(source or b)-1]
    st=fr(ins);en=min(fr(outs),fr(sb['video_duration']))
    return {'batch':b,'source_batch':source or b,'source':sb['path'],'in':st,'out':en,'frames':fr(dur) if dur is not None else en-st,'props':props or {},'note':note}

E={b['batch_number']:[seg(b['batch_number'],0,min(b['planned_duration'],b['video_duration']))] for b in A}
E[2]=[seg(2,0,4.667),seg(2,4.667,6.5,1.25,note='拍碗局部提速'),seg(2,6.5,14.0)]
E[3]=[seg(3,0,11)]
E[4]=[seg(4,0,5.167),seg(4,3,3.75,1.125,note='求救后闭口等待，减少笑脸停顿'),seg(4,6.292,9.75),seg(4,10.5,11.25,.75,note='拒绝尾音切孩子反应'),seg(4,11.25,14,3.5)]
E[5]=[seg(5,0,4,props={'ZoomX':1.8,'ZoomY':1.8,'Pan':450,'Tilt':80},note='恶魔发言聚焦'),seg(5,4,14.92,props={'ZoomX':1.8,'ZoomY':1.8,'Pan':-450,'Tilt':80},note='天使回应聚焦')]
E[6]=[seg(6,0,8),seg(6,8,11.25,note='收紧送别尾停')]
E[7]=[seg(7,0,5.25),seg(7,6.25,13,note='去掉卡帽重复保持')]
E[8]=[seg(8,0,9),seg(8,9,13.8,3.7,note='对白后试锁恢复动作压力')]
E[10]=[seg(10,0,4)]
E[11]=[seg(11,0,2),seg(11,2,3.75,1.17,note='拨帽接触后加快失衡'),seg(11,4.8,9),seg(11,9,10),seg(11,11,13,note='压缩抱靴等待')]
E[13]=[seg(13,0,8),seg(13,8.25,10,note='删除切后正立平台')]
E[14]=[seg(14,0,5.8)]
E[15]=[seg(15,0,12)]
E[16]=[seg(16,0,12),seg(16,12.333,12.917,props={'ZoomX':1.7,'ZoomY':1.7,'Pan':-218,'Tilt':78},note='只保踹门接触，不暴露反向门洞')]
E[17]=[seg(17,0,3,note='night_sky'),seg(17,3,6.5)]
E[19]=[seg(19,0,4.65),seg(19,6,12,note='保留术名，缩瞬移前等待')]
E[21]=[seg(21,0,6),seg(21,6,11.292,note='flashback_entry')]
E[22]=[seg(22,0,3.5,note='答应后及时离开，不回书')]
E[24]=[seg(24,1.417,10.125,9.167,note='去掉重复唤醒，画面轻慢放，原声原速')]
E[25]=[seg(25,2.25,4,4,note='完整五列铺满，不出现空版'),seg(25,4,14.458,note='flashback_return')]
E[27]=[seg(27,0,1.75,2.5,note='保留完整水滴，避开分裂'),seg(27,5,7.292,4.042,props={'ZoomX':3.0,'ZoomY':3.0,'Tilt':-450},note='聚水省略：稳定水滴接云海，保留全句')]
E[28]=[seg(28,4,12.25,10.0,note='取云海后段，弃提前地面水浪')]
E[30]=[seg(30,0,1.5),seg(30,1.5,6.375,props={'ZoomX':2.0,'ZoomY':2.0,'Pan':-580,'Tilt':352},note='踝锁特写排除已自由的双手'),seg(30,6.375,11.583)]
E[31]=[seg(31,0,9.5),seg(31,12,13.5,note='保留祈愿与0.8秒留白，术名后直接解印')]
E[33]=[seg(33,0,1.5),seg(33,3,12,note='余波接空殿，省略未实现的抓空')]
E[35]=[seg(35,0,2),seg(35,11.0,13.0,source=39,note='用现有小鱼仰望反应替换异能眼特写'),seg(35,166/24,255/24,135/24,note='完整剔除异常虹膜残帧，仅雨空温和慢放'),seg(35,255/24,14)]
E[36]=[seg(36,0,2),seg(36,3,12,note='收紧守门阵列展示')]
E[37]=[seg(37,0,8),seg(37,0,149/24,note='CY028A单镜H3补拍；只替换扶下6.208秒')];E[37][1]['source']=str(ROOT/'视频制作/Metaso-H3-v004/产物/GB027-v004-CY028A-r1.mp4')
E[38]=[seg(38,0,6.5),seg(38,2.75,4.5,1.75,source=39,note='用父亲反应替换图标式眼内倒影'),seg(38,8.25,14.208,6.0)]
E[39]=[seg(39,0,11.6,note='保留完整台词，缩小鱼望镜头尾停')]
E[40]=[seg(40,0,13.36)]
E[41]=[seg(41,.5,3.5,note='连续承重到站稳')]
E[42]=[seg(42,0,3),seg(42,9,14,note='days_later')]
E[43]=[seg(43,0,4.5),seg(43,4.5,6.4),seg(43,7.4,10.125,note='交勺后去重复停顿')]
E[44]=[seg(44,0,4.3,2.75,note='保留入口合唇空勺退出'),seg(44,4.3,9.417,6.25,note='把余量留给相望，末4秒无BGM')]

cursor=0;edl=[];batches=[]
for b in A:
    n=b['batch_number'];start=cursor
    for j,s in enumerate(E[n],1):
        assert s['out']>s['in'] and s['frames']>0
        s.update(record=cursor,ordinal=j,name=f'B{n:02d}_{b["id"]}_{j:02d}',speed=100*(s['out']-s['in'])/s['frames'])
        edl.append(s);cursor+=s['frames']
    batches.append({'batch':n,'id':b['id'],'start':start,'frames':cursor-start,'old_start':b['film_start'],'old_duration':b['planned_duration']})

voice=[]
for b in A:
    n=b['batch_number'];dest=batches[n-1]
    for c in b['cues']:
        local=c['start']-b['film_start']
        # Cues remain original speed. Only explicit editorial relocation changes their starts.
        if n==2 and local>6.5:local-=.583333
        if n==3:local-=.5
        if n==12 and c['id']=='VO-CY019-01':local=11.5
        if n==19 and local>6:local-=1.35
        event={'id':c['id'],'batch':n,'role':c['role'],'path':c['current_path'],'record':dest['start']+fr(local),'duration':c['end']-c['start'],'ja':c['ja'],'zh':c['zh']}
        assert event['record']+fr(event['duration'])<=dest['start']+dest['frames']+1,(n,event)
        voice.append(event)

plan={'fps':24,'width':1344,'height':768,'timeline':'v001_Director_Post_Repair_Final','edl':edl,'batches':batches,'voice':voice,'frames':cursor,'seconds':cursor/24,'status':'editable_candidate_requires_render_review'}
(OUT/'后期执行计划.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
print({'segments':len(edl),'voices':len(voice),'seconds':cursor/24})
