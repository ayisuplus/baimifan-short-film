"""Author the seven visual references at six approved action nodes; preserve timing/audio."""
import copy, hashlib, json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
BASE='镜头设计/shot-plan-v0.61.json'
OUT='镜头设计/shot-plan-v0.62.json'
REQ='镜头设计/生成记录/关键动作-v062/请求.json'
FIX='后期/关键动作重拍-v017'
CHANGES={
'CY021A':dict(framing='递火教徒肩侧的紧近景，右手/火把在前、父亲侧脸在中、受缚女儿在远处',camera='85mm压缩纵深感；从递火教徒肩侧贴近，先看右手接牢，随父亲目光短拉焦到高处受缚白色轮廓；不绕轴，不退成仪式群像。',action='教主右手接牢唯一黑芯暗紫细边的仪式火把，目光从交接处转向高处受缚的Claude。教徒肩与递火手留在前景边缘；Claude直立在高处未燃柴堆后，双腕受缚。父亲冷静决断，不犹豫。固定火盆与蜡烛仍普通暖火。',note='接牢后的中间状态参考，非硬首帧。教主棕金眼，火把右持；远处Claude可辨但虚焦，不能当画外人物删掉。只一支火把，不改变杯口/黑金材质。',cast=dict(visible=['教主','教徒','Claude'],offscreen=['DeepSeek'],reflection=[],note='教徒仅肩与手，Claude是高处虚焦受缚轮廓；教主面部与右手为主体。')),
'CY022A':dict(framing='贴地斜侧紧近景，小手、将滑脱的黑金袍尾与左侧半张脸',camera='75mm近摄感；与攥袍前镜同侧，沿袖口到指尖定住，背景台阶与蓝窗散焦；不后退看教主全身。',action='延续上一镜同一次攥袍，教主朝画面右侧离去。绷紧的袍角逐渐滑过小鱼指尖，只剩最后一折接触；她试合一次却落空，小手慢慢落下，眼神追着袍尾。教主身体与右手火把在画外，高柴尚未燃。下一镜才看登阶距离。',note='新图是最后指尖接触，不是已经松手的终态；起镜延续绷紧，镜尾才完全滑脱。小鱼左、教主袍尾右，单次滑脱，不重新抓两次。',cast=dict(visible=['DeepSeek','教主'],offscreen=['Claude'],reflection=[],note='小鱼局部脸/袖/手，教主只见袍尾；教主脸与右手火把画外。')),
'CY023':dict(framing='门内侧斜向低位撞击特写，鞋底、门板与冷光裂口',camera='摄影机贴近门内侧，从右上踢来的鞋底与向镜头掠过的门板形成斜线；撞击轻震后定住，脸不必入画。',action='GPT从门外以右脚一次踹开门扇。鞋底撞击处木料破裂，门板向殿内掠过，冷月光从裂口涌入；木屑沿受力方向飞散。她收脚落地跨入，2秒内完成，不重复踹。下一镜才完整揭示GPT与八位援军。',note='本图是撞击瞬间，不是已完成破门的首帧。前景踢腿为右腿且保留腿饰；后景支撑左腿由长裙遮住，最多露鞋尖。脸在画外，力量由门板与碎屑体现。',cast=dict(visible=['ChatGPT'],offscreen=['八位正门援军','教徒'],reflection=[],note='GPT只见鞋、腿和衣摆，完整面容与队伍下一镜揭示。')),
'CY027B1':dict(framing='沿左下至右上变形轨迹仰视，单一白紫龙身占主体',camera='近低机位沿同一上升轨迹轻仰跟，主体前后连续；背景中殿已破顶，后殿不新增破口。',action='白紫水光裹住GPT，她腾起。人形轮廓在同一次上升中转为长身水龙，白角与紫鬃连续延展；下段衣褶与饰物在水光里消散并转为白鳞。阶段画面只有一个连贯主体，没有完整人形站在独立龙首旁。2秒镜尾服装残形全部消失，完整龙形向上，接教主变身与双方穿顶。',note='新图为中后段变形阶段：衣褶转鳞，不是龙最终穿衣，也不是召出另一条龙。起段由上一镜GPT人形延续，镜尾完成单体化龙。淡紫眼克制，不增加巨大亮眼、额外龙首或人形分身。'),
'CY028A':dict(framing='起段全景交代迈下脚托，随后同侧收至胸上双人近景',camera='先保留足部落地与GPT支撑；Claude站稳后顺视线缓慢靠近，2.7秒左右到胸上双人近景，问孩子时眼睛与扶上臂的手同框。Kimi退入左侧虚焦，不是新增切镜。',action='GPT轻声说“慢慢来”，折翼扶Claude从脚托迈下站稳。Kimi收好束具让开。摄影机沿同侧收近，Claude带着疲惫向阶下画外寻找小鱼，问“那个孩子……”，GPT手仍支撑上臂和背。Claude苍白、衣边焦损和头纱保持，普通灯火仍熄灭。',note='保留旧全景作起段空间/扶持参考，新图用于站稳后的近景状态；两图是同一个6.2秒镜头的阶段，不能插跳切或从终态直接省略迈下。0.1–2.6秒GPT、2.8–6.08秒Claude原速对白不变。',cast=dict(visible=['ChatGPT','Kimi','Claude'],offscreen=['Qwen','DeepSeek'],reflection=[],note='起段三人，近景阶段Kimi仅左缘虚焦衣肩；Claude与GPT脸及扶持手为主体。')),
'CY029C':dict(framing='同侧腰高斜侧中景，失衡躯干与下垂手形成方向反差',camera='水平机位，Claude髋在左下、肩头偏右，GPT从右向左跨入；不以歪镜代替受力，不为露脸把身体摆直。火架退画缘虚焦。',action='Claude放下施法手，膝盖微软，仍站立的髋向左下失去支撑，肩头向右侧GPT倾去；近侧手因脱力垂直下落。GPT立即跨入、弯膝，以一手开始接住她上背，另一手向膝部下降但尚未托膝。她仍有意识，没有跪地、坐地或摔地。',note='新图是失衡与上背开始承托的关键状态；下垂手不主动抱人。髋肩斜线与GPT反向跨入形成受力关系，镜尾才接下一镜探膝。C-r1跪地、r2近直立均拒用。'),
'CY029D':dict(framing='同侧低位接重中景，双承托点、弯膝和刚离地赤足可读',camera='沿上一镜同侧略放宽，留GPT弯膝接重与Claude脚刚离地的范围；不起镜就定成贴头合影，下一镜才收近抱稳。',action='延续同一次接重。GPT一臂托住Claude上背，另一臂探进膝弯并承住，弯膝跨入重心后开始起抱；Claude赤足刚离地，近侧手仍无力垂下。两人头部保持分开，Claude尚未主动搭肩。下一镜GPT才站直抱稳，之后Claude再主动靠近。',note='本图为低位承重起抱阶段；起镜沿C的背托继续探膝，不能把阶段图当已经站直抱稳首帧。Claude赤足，GPT自己的银白鞋保留；双臂承托、实际负重与跨切连续性另验。')
}

def main():
    old=json.loads((ROOT/BASE).read_text('utf-8-sig'));new=copy.deepcopy(old)
    jobs=json.loads((ROOT/REQ).read_text('utf-8'));chosen={j['id']:j for j in jobs if j.get('selected_for_v017')}
    assert set(chosen)==set(CHANGES)
    for s in new['shots']:
        sid=s['id']
        if sid not in CHANGES:continue
        c=CHANGES[sid];j=chosen[sid]
        s['previous_presentation_v061']=copy.deepcopy(s['presentation'])
        s['previous_final_static_review_v061']=copy.deepcopy(s.get('final_static_review'))
        s['presentation'].update(path=j['project_output'],visible=c['action'],status='v062关键动作新候选，作者已授权改拍，待成图审阅',missing='静帧候选；连续运动、负重、变形和口型尚待动态验收')
        s.update(framing=c['framing'],camera=c['camera'],action=c['action'],source_quote=c['action'],visual_prompt=j['prompt'],generation_request=REQ,revision_v062={k:v for k,v in c.items() if k not in ['action','camera','framing']})
        s['refs'].insert(0,dict(path=j['project_output'],role='v062当前关键动作候选'))
        s['invariants'].append(c['note'])
        s['final_static_review']=dict(version='v062',status='pending_author_review',review=FIX+'/视觉复核.md',dynamic_execution='pending')
        with Image.open(ROOT/j['project_output']) as im:w,h=im.size
        s['page_size']=[w,h];s['panel_rect_pixels']=[0,0,w,h];s['panel_region']=dict(x=0.0,y=0.0,w=1.0,h=1.0)
        if sid=='CY028A':
            states=[dict(path=s['previous_presentation_v061']['path'],offset=0,label='起段空间与迈下扶持参考，非固定首帧',label_en='Opening wide spatial and support reference, not a fixed first frame'),dict(path=j['project_output'],offset=2.7,label='站稳后寻找小鱼的近景状态',label_en='Close state after standing, looking for the child')]
            s['state_references']=states;s['review_state_sequence']=copy.deepcopy(states)
        if sid=='CY029C':s['exit_state']='上背已开始被GPT承接，尚未托膝，未触地；接同一次起抱。'
        if sid=='CY029D':
            s['entry_state']='Claude向GPT倾斜，上背刚被承接；GPT另一臂还未探入膝弯。'
            s['exit_state']='双臂托背与膝弯，Claude刚离地；GPT弯膝承重，下一镜才站直抱稳。'
    new.update(title='《白米饭》带图分镜 v0.62 · 关键动作重拍',version='v0.62',revision='v062',previous_source=BASE,story_script='剧本/白米饭-场景剧本-v0.61.md',subtitle='133镜 · 464.4秒 · 六处关键动作与情绪改拍候选',roughcut_preview=FIX+'/全片声音预览.html',audio_repair_plan=FIX+'/配音对位方案.json')
    new['revision_notes']=dict(scope='作者授权六处改拍，7张新静帧与摄影动作说明；站稳镜保留宽到近阶段。未改镜长、对白、BGM或视频生成状态。',previous_source_sha256=hashlib.sha256((ROOT/BASE).read_bytes()).hexdigest(),generation_requests=REQ)
    assert [(s['id'],s['seconds'],s.get('subtitle_cues')) for s in old['shots']]==[(s['id'],s['seconds'],s.get('subtitle_cues')) for s in new['shots']]
    (ROOT/OUT).write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    p=ROOT/'剧本/白米饭-场景剧本-v0.60.md';txt=p.read_text('utf-8')
    txt=txt.replace('版本：v0.60｜2026-10-27｜扇子近摄与青紫法术修订；其余剧情对白不变。','版本：v0.61｜2026-10-27｜六处关键动作与摄影修订；剧情对白不变。')
    txt=txt.replace('当前镜头源v0.61、生成板v016','当前镜头源v0.62、生成板v017').replace('本轮只改三张扇子机位与法术表现','本轮修订接火、滑脱、破门、本人化龙、站稳牵挂与脱力接抱六处')
    additions={
      'Claude的父亲穿着教主礼服走到长阶下端。':'机位贴在递火教徒肩侧：右手与火把在前景，父亲侧脸在中景，高处受缚Claude留成虚焦白色轮廓。接牢后一次短拉焦连接工具、父亲目光与女儿，不增加犹豫。\n\nClaude的父亲穿着教主礼服走到长阶下端。',
      '教主继续迈步。教主右手持同一支黑焰仪式火把':'贴地斜侧紧近景，延续小手攥住袍尾。最后一折布料从指尖滑过，小鱼试合一次却落空；半张脸与下垂小手留在画左，袍尾向画右离去。此镜不退成教堂全景，下一镜才交代登阶距离。\n\n教主继续迈步。教主右手持同一支黑焰仪式火把',
      '大门被一脚踹开。吟唱戛然而止。':'门内侧斜向低机位贴近鞋底撞击处：GPT右脚一次踹裂门板，木料向殿内掠过，冷光从裂口涌入。她收脚落地跨入，脸暂在画外，下一镜再揭示全队；吟唱戛然而止。',
      '白紫水光裹住 ChatGPT，她腾起，身体化为白紫长身水龙；白角与紫鬃在水光中展开。':'白紫水光裹住 ChatGPT，她沿同一轨迹腾起，人形轮廓连续转为白紫长身水龙。白角与紫鬃延展，衣褶与饰物在水光中消散转为鳞片；镜尾服装残形完全消失，画面只有她这一条完整龙，不并列完整人形与另一条召唤龙。',
      'Claude的赤足站稳同一祭坛平台，目光越过GPT，寻找阶下那个蓝色身影。':'Claude的赤足站稳同一祭坛平台。镜头由全景沿同侧收至胸上双人近景，GPT扶上臂的手与Claude寻找阶下孩子的眼睛同框，Kimi退入虚焦。收近在Claude起句前后到位，保持同一个6.2秒连续镜头。',
      '火焰已经攀上空木架。Claude的施法手已经放下，力量耗尽，膝盖一软，身体向右侧倾去。她仍有意识，没有摔到地上。':'火焰已经攀上空木架，退在画缘虚焦。水平腰高侧中景中，Claude放下施法手，膝盖微软，髋在左下、肩头向右侧GPT倾去；手垂直落下，与躯干形成方向反差。她仍站立而失衡，没有跪地或摔地。GPT跨入弯膝，一手开始接住上背，另一手向膝部下降。',
      'ChatGPT 立即靠近，一只手臂托住 Claude 的背，另一只手臂探入她的膝弯，顺势将她抱起。':'延续同一次接重：ChatGPT一臂托背、另一臂探进Claude膝弯，弯膝承担重量后开始起抱，Claude赤足刚离地、手仍垂落。此刻两人头部不贴近；下一镜才站直抱稳，之后Claude才主动搭肩。'
    }
    for a,b in additions.items():
        assert a in txt,a
        txt=txt.replace(a,b,1)
    (ROOT/'剧本/白米饭-场景剧本-v0.61.md').write_text(txt,encoding='utf-8')
    print('v0.62 authored: 7 visual references, all timing/dialogue unchanged')

if __name__=='__main__':main()
