from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'后期/截图定点修正-v004';G=R/'视频制作/Metaso-H3-v007/产物'
def seg(a,batch,lo,hi,n=None,props=None):return dict(source=str(G/(a+'.mp4')),batch=batch,**{'in':lo,'out':hi},frames=n or hi-lo,props=props or {},new_pickup=True)
def e(a,b,ss,why):
 assert sum(s['frames'] for s in ss)==b-a
 return dict(start=a,end=b,segments=ss,reason=why)
claude='GB011-v007-Claude-style-audio-r2';father='GB010-v007-father-style-audio-r1';wing='GB018-v007-gpt-rise-style-audio-r1';kimi='GB014A-v007-kimi-window-style-audio-r2'
old=dict(source=str(R/'视频制作/Metaso-H3-v003/剪辑候选/GB005-v003.mp4'),batch=6,**{'in':54,'out':120},frames=66,props={})
edits=[e(3478,3622,[seg(father,12,0,116),seg(father,12,60,74,28)],'原声发声区原速；去掉末尾无声乱说话，闭口反应0.583秒放1.167秒'),e(3914,4058,[seg(claude,14,114,228),seg(claude,14,260,275,30)],'恳求原声和表演原速；静音尾替换为实际闭口源10.833–11.458秒轻慢放'),e(1640,1760,[seg('GB005-v007-early-decision-audio-r1',6,0,54),old],'只用新说话0–2.25秒，接原片朝宫门离开；拒用新片走回王座的反向行动'),e(6476,6650,[seg(wing,25,0,60),seg(wing,25,60,72,24),seg(wing,25,72,144),seg(wing,25,180,192,18)],'仅延长无脸起飞末段0.5秒，使开口接实际起声；发声脸段保持原速，6.5秒后采用闭口尾'),e(5018,5229,[seg(kimi,18,0,144),seg(kimi,18,96,144,49,props=dict(ZoomX=3.0,ZoomY=3.0,Pan=-636.0,Tilt=-486.0)),seg(kimi,18,150,168)],'请门原声完整；最后两秒以银刃特写承接咒语，8秒后才接发力投刃，再接B19玻璃撞击；玻璃全程完整')]
(O/'剪辑修正增量.json').write_text(json.dumps(dict(replace_edits=edits,approval_boundary='候选经独立大段开闭口与因果核验，逐音素与连续听审仍由作者核定'),ensure_ascii=False,indent=2),encoding='utf8')
print('Five same-duration refinements written')
