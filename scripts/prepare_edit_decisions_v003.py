from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'后期/导演重构-v003';Q=json.loads((R/'视频制作/Metaso-H3-v006/执行队列.json').read_text(encoding='utf8'))
def generated(a):
 x=next(x for x in Q['items'] if x['attempt_id']==a);assert x['status']=='downloaded_candidate';return x['local_path']
def seg(src,a,b,frames=None,anchor=None,props=None):
 x=dict(source=src,**{'in':round(a*24),'out':round(b*24)},frames=frames or round((b-a)*24),props=props or {})
 if anchor:x['anchor']=anchor
 return x
edits=[]
def edit(id,batch,start,end,why,segments):edits.append(dict(id=id,batch=batch,start=start,end=end,reason=why,segments=segments))
edit('church_space',7,2126,2198,'初见教堂纵深延长1.5秒，先读清祭坛关系再靠近',[seg('视频制作/LibTV-H3-v001/产物/GB006-H3-v001.mp4',10,13,108,'church_space')])
edit('child_decision',10,3007,3007,'听见搬柴后先有决定，再接原有下阶',[seg(generated('GB008R2-v006-CY016C-decision-r1'),.25,2.75,anchor='child_decision')])
src=generated('GB009-v006-CY016D-force-r1')
edit('acolyte_force',11,3079,3199,'短拉扯后明确掌根推、失衡、落地，裁掉无效等待',[seg(src,.5,1.5,anchor='acolyte_force'),seg(src,2,5.75)])
edit('father_audio',12,3388,3526,'以作者当前两段原声剪辑驱动口型，替换快慢嘴分段',[seg(generated('GB010-v006-CY021A-audio-r1'),0,6,anchor='father_audio',props={})])
edits[-1]['segments'][0]['follow_face']=True
src=generated('GB011-1-v006-CY020A-force-r2')
edit('father_force',13,3722,3806,'拒用首轮悬浮轻放，二轮脚接地；剪掉托肩等待，落地后留恢复',[seg(src,0,.75,anchor='father_force'),seg(src,1.5,2.75),seg(src,2.75,4,48)])
src=generated('GB011-2-v006-CY021-audio-r1');props={'ZoomX':1.344,'ZoomY':1.344,'Pan':0,'Tilt':-132.384}
edit('claude_audio',14,3806,3908,'原选声驱动两次发话，停顿用受缚手部承接，保留句后等待',[seg(src,0,1.375,anchor='claude_audio',props=props),seg('视频制作/LibTV-H3-v001/产物/GB011-2-H3-v001.mp4',3.5,5.25),seg(src,3.125,6,props=props)])
edit('father_refusal',14,3908,3908,'女儿说完后父亲闭口拒绝并转向刑火；不加新台词',[seg(generated('GB011-2-v006-CY021-father-r1'),.5,3.5,anchor='father_refusal')])
src=generated('GB015-2-v006-CY024K3-defense-r1')
edit('kimi_defense',20,5244,5340,'先蓄力、Kimi落脚挥刃、立即命中，接不透明罩余波',[seg(src,0,2,anchor='kimi_defense'),seg(src,2.625,4.25,anchor='kimi_contact'),seg('视频制作/Metaso-H3-v003/剪辑候选/GB015-2-v003.mp4',3.25,4)])
src=generated('GB019-v006-CY024A9-caster-r1')
edit('gpt_chant',26,6419,6776,'咏唱恢复施术者主体，保留敌矛与扇盾因果，云天承接水息',[seg(src,0,2.25,anchor='gpt_chant'),seg('视频制作/Metaso-H3-v002/剪辑候选/GB019-v002.mp4',0,4.5,anchor='spear_fan'),seg(src,6.75,15)])
edit('retreating_water',33,8020,8020,'补回退水中段，让水击结果先被读清',[seg('视频制作/Metaso-H3-v001/产物/GB023-Metaso-H3-v001.mp4',1.5,3,anchor='retreating_water')])
edit('aftermath_space',33,8020,8080,'保护罩与退水全景延长一秒，给音乐落点与空间恢复',[seg('视频制作/Metaso-H3-v001/产物/GB023-Metaso-H3-v001.mp4',3,5.5,84,'aftermath_space')])
edit('claude_offscreen',37,9405,9442,'Claude半句改由闭口小鱼反应承接，保留扶下前后动作',[seg('视频制作/Metaso-H3-v002/剪辑候选/GB028-v002.mp4',.625,.625+37/24,anchor='claude_offscreen')])
sound=[]
def fx(id,src,kind,anchor,offset,dur,peak=-24,**kw):sound.append(dict(ident='V3-'+id,src=src,kind=kind,anchor=anchor,offset=offset,dur=dur,peak=peak,**kw))
fx('wood-trigger','wooden-board1','Foley','child_decision',.1,.6,-22)
fx('turn-cloth','rustling-of-clothes1','Foley','child_decision',1.65,.65,-25)
fx('push-palm','punch-light2','Action','acolyte_force',1.375,.55,-17)
fx('push-cloth','rustling-of-clothes2','Foley','acolyte_force',1.34,.65,-24)
fx('child-ground','real-down1','Action','acolyte_force',2.25,1,-16)
fx('child-hand','wall-hit1','Foley','acolyte_force',2.2,.45,-22)
fx('acolyte-leaves','walk-leather-shoes1','Foley','acolyte_force',3.6,1.1,-24)
fx('father-push','punch-light2','Action','father_force',.5,.5,-17)
fx('father-slip','walk-leather-shoes1','Foley','father_force',1,.55,-25)
fx('father-ground','real-down1','Action','father_force',1.75,.9,-16)
fx('father-hand','wall-hit1','Foley','father_force',1.7,.45,-22)
fx('priest-robe','rustling-of-clothes3','Foley','father_refusal',2.25,.65,-25)
fx('claude-binding','key1','Foley','claude_audio',1.45,.6,-28,purpose='既有金属小响作束缚轻响代理，不宣称新录链声')
fx('kimi-plant','walk-leather-shoes1','Foley','kimi_defense',1.2,.45,-20)
fx('kimi-draw','mixkit-2799','Action','kimi_defense',1.5,.6,-21)
fx('shield-arc','magic-wind1','Magic','kimi_defense',1.6,.65,-20)
fx('shield-strike','mixkit-1306','Action','kimi_contact',.2,2,-14)
fx('shield-pressure','magic-reflection1','Magic','kimi_contact',.24,1.5,-20)
fx('shield-settle','magic-wind1','Magic','kimi_contact',1.1,1.2,-27)
fx('spear-whoosh','sword-drawn1','Action','spear_fan',.6,.6,-21)
fx('fan-catch','mixkit-2794','Action','spear_fan',1.5,.8,-17)
fx('fan-shield','magic-reflection1','Magic','spear_fan',1.55,2,-23)
for t in [382,383.2,386]:sound.append(dict(ident='V3-lock-'+str(t),src='mixkit-2858',kind='Foley',baseline_time=t,dur=.8,peak=-22))
dec=dict(edits=edits,tempo_voice_ids=['VO-CY024A-01','VO-CY024A9-01','VO-CY024A2-01','VO-CY024A3-01'],voice_overrides={'VO-CY021A-01':dict(anchor='father_audio',offset=.35,retain_part_offsets=True),'VO-CY021-01':dict(anchor='claude_audio',offset=.4),'VO-CY024A9-01':dict(anchor='gpt_chant',offset=.25),'VO-CY024A2-01':dict(anchor='gpt_chant',offset=7.031458),'VO-CY027B-01':dict(shift_frames=13)},sound_events=sound,not_adopted=['GB011-1-v006-CY020A-force-r1'],export_policy='不导出，达芬奇工程内核验')
(O/'剪辑决定.json').write_text(json.dumps(dec,ensure_ascii=False,indent=2),encoding='utf8');print('Decision file prepared')
