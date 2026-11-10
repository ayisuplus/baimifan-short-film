"""Record explicit adopted ranges, after visual review; no whole-batch regeneration."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'后期/声画重构-v002'
P=json.loads((R/'后期/导演后期修正-v001/后期执行计划.json').read_text(encoding='utf8'))
S=json.loads((R/'后期/导演全片审查-v001/当前44批审查清单.json').read_text(encoding='utf8'))
reps=[]
def old(n):return S[n-1]['path']
def new(name):return '视频制作/Metaso-H3-v005/产物/'+name+'.mp4'
def s(path,a,b,d=None,anchor=None,props=None,**kw):
    return {'source':path,'in':a,'out':b,**({'duration':d} if d is not None else {}),**({'anchor':anchor} if anchor else {}),'props':props or {},**kw}
def edit(n,a,b,segments,reason):reps.append({'batch':n,'start':a,'end':b,'segments':segments,'reason':reason})
def end(n):return P['batches'][n-1]['frames']/24
edit(7,12,12,[s(new('GB006-v005-CY012-r3'),.5,3.5,anchor='stair_up',new_pickup=True)],'补小鱼踏阶上高坛的3秒空间过渡；保留短腿、毛边靴与室内光色')
edit(8,9,end(8),[s(old(8),9,13.8,anchor='try_lock')],'试锁恢复原速，失败后的指尖压力与停顿不再129%赶过')
edit(10,4,4,[s(new('GB008R2-v005-CY016D-transition-r3'),.5,3.5,anchor='stair_down',new_pickup=True)],'补从高坛跑下阶阻拦搬柴的3秒行动桥')
edit(11,0,5.5,[s(new('GB009-v005-CY016D-r1'),0,5,anchor='push_wood',new_pickup=True)],'真正推肩接触后失衡撑地，去掉原150%小跳')
priest=new('GB010-v005-CY021A-r2');crop={'ZoomX':1.3,'ZoomY':1.3,'Pan':-90,'Tilt':0}
edit(12,3,11.3,[s(priest,2.2,3.934,46/24,'priest_sentence',crop,new_pickup=True),s(priest,3.934,5.339,22/24,props=crop,new_pickup=True),s(priest,5.339,6.693,38/24,props=crop,new_pickup=True),s(priest,6.693,7,11/24,props=crop,new_pickup=True)],'从高坛方向看父亲，按所选录音两段真实发声和中间停顿分段对位；删初始无意义等待，裁去边缘道具漂移')
edit(13,7.25,end(13),[s(new('GB011-1-v005-CY020A-r1'),0,3.5,anchor='push_child',new_pickup=True)],'单次左掌推肩、落地、余势同镜；保留Claude前句制止')
plea='后期/声画重构-v002/处理片段/CY021-恳求-跟随裁切.mp4'
edit(14,0,end(14),[s(plea,1.3,2.531,22/24,'claude_plea',new_pickup=True),s(old(14),3.5,5.35,44/24,anchor='grip_robe'),s(plea,3.361,4.653,26/24,new_pickup=True),s(plea,4.653,5,10/24,new_pickup=True)],'Claude称呼父亲→抓袍手部承接长静默→Claude完整恳求→等回应；不让孩子代说，跟随裁切剔除过早点火与新增人物')
edit(16,12,end(16),[s(new('GB013-v005-CY023-r1'),.8,3.8,anchor='door_kick',new_pickup=True)],'补足门内破门、门扇内开与落脚，保留原火幕/列阵/裙摆/门前静默')
edit(17,0,3,[s(old(17),1,3,2.5,'gpt_entry',fusion_comp='B17_GB014_01')],'从门已开状态接入，去掉第二次慢开门，群像轻慢2.5秒承完整命令')
edit(18,10.5,11,[s(old(18),10.5,11,1)],'保持4秒无对白显形，只给末句仍发声的口部表演增加半秒，随后甩刃')
tele=new('GB015-1-v005-CY024K2-r1')
edit(19,0,end(19),[s(old(19),0,2,anchor='glass_break'),s(old(19),3,5.5,anchor='blade_coordinate'),s(tele,.5,2.75,anchor='kimi_materialize',new_pickup=True),s(tele,3.875,5,anchor='kimi_settle',new_pickup=True,fx_flash=True),s(old(19),10,12,anchor='cultist_attack')],'删掉飞刃击木前提前露出清空柴堆的宽镜；地面银流凝实后接低蹲，弃中间轻跳，以2帧凝实闪光连接，再接敌人举手')
# Optional reviewed water pickup is selected by the independent close-motion review.
decision=O/'水珠采用.json'
if decision.exists():
    d=json.loads(decision.read_text(encoding='utf8'))
    edit(27,0,end(27),d['segments'],d['reason'])
edit(28,5,end(28),[s(new('GB020-1R2-v005-CY024A6-r1'),0,5,anchor='sky_water',new_pickup=True)],'保留前5秒云层定位，后5秒明确悬天连续水面及下压蓄势，原声不缩不加速')
edit(30,1.5,6.375,[s(new('GB021-v005-CY024A4-r1'),0,5.5,anchor='inspect_lock',new_pickup=True)],'恢复Kimi脸、双手、踝扣和脚托同框的侧面中近景；双腕不入框避免提前解锁')
for name in ['后期修法31-44.json','后期修法07-15.json']:
    p=O/name
    if p.exists():
        obj=json.loads(p.read_text(encoding='utf8'));rows=obj if isinstance(obj,list) else obj['items']
        for x in rows:
            if 'batch_number' in x:
                n=x['batch_number'];reps[:]=[r for r in reps if r['batch']!=n];converted=[]
                for y in x['segments']:
                    props={}
                    if y.get('crop'):
                        props={'ZoomX':2.25,'ZoomY':2.25,'Pan':-513,'Tilt':461.25} if n==8 else {'ZoomX':1.12,'ZoomY':1.12,'Tilt':-30}
                    converted.append(s(x['source'],y['source_in_frame']/24,y['source_out_frame']/24,(y['record_out_frame']-y['record_in_frame'])/24,props=props))
                edit(n,0,end(n),converted,x['why']);continue
            edit(x['batch'],x['v001_local_start'],x['v001_local_end'],x['segments'],x['reason'])
edit(39,65/24,203/24,[s(old(39),131/24,203/24,138/24)],'按原源真实切点5.458333–8.458333取手部。父亲反应已前移到其呼唤处，这里不重复降手；连续掌心微光承咏唱，原声原速；不使用1fps联系表名义时间猜源切点')
if not any(x['batch']==44 for x in reps):edit(44,0,2.75,[s(old(44),0,4.3)],'入口合唇恢复原速，给吃饭与咀嚼呼吸，最后4秒停乐仍保留')
voice={'VO-CY021A-01':{'anchor':'priest_sentence','offset':0},'VO-CY019-01':{'local':9.6},'VO-CY021-01':{'anchor':'claude_plea','offset':0},'VO-CY024-01':{'anchor':'gpt_entry','offset':.35},'VO-CY024K0-01':{'local':4},'VO-CY024K0-02':{'local':7.708333333333},'VO-CY024K1A-01':{'anchor':'blade_coordinate','offset':1.0},'VO-CY024A4-01':{'anchor':'inspect_lock','offset':0},'VO-CY024A8-01':{'local':7.0}}
for v in P['voice']:
    if v['batch']==38:voice[v['id']]={'local':(v['record']-P['batches'][37]['start'])/24}
extra=O/'后期修法07-15.json'
if extra.exists():
    x=json.loads(extra.read_text(encoding='utf8'))
    if isinstance(x,dict):voice.update(x.get('voice_overrides',{}))
A={'status':'visually_reviewed_ranges_pending_context_render','replacements':reps,'voice_overrides':voice,'music_action_overrides':{'M06':{'anchor':'door_kick','offset':.45,'start_at_action':True},'M07':{'anchor':'kimi_settle','offset':0}},'limits':'分句非静音区对位，不等于逐音口型或完整连续听审。回片/旧片均保留。'}
(O/'采用剪辑.json').write_text(json.dumps(A,ensure_ascii=False,indent=2),encoding='utf8');print(len(reps),'edits')
