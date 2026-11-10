"""Apply author v0.8 continuity changes, preserving prior manifests and media."""
import copy,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1]
target=R/'镜头设计/shot-plan-v0.8.json'
assert not target.exists(),'v0.8 exists; inspect before editing'
d=json.loads((R/'镜头设计/shot-plan-v0.7.json').read_text(encoding='utf-8'))
old=copy.deepcopy(d)
script=(R/d['story_script']).read_text(encoding='utf-8')
script=script.replace('版本：v0.7｜','版本：v0.8｜')
q={}
q['hesitate']='钟声传来，ChatGPT 留在座位上，手指压紧金色扶手的雕纹，停了一拍，又慢慢松开。'
q['bowl']='DeepSeek 把饭碗留在街边矮桌上，眉头紧皱，担忧地抬头望向远处的宫殿。'
q['hole']='DeepSeek 躲在教堂本体侧墙的阴影里，身边就是低矮破洞。她等到最后一盏灯转入侧院，再从同一洞口钻入。'
q['basins']='两个相同的铜水盆对称放在祭坛最下一级台阶外的左右地面，中央通道留空；右盆用于接住第一支火把。'
q['block']='从小鱼身后贴地仰拍，她张开双臂，挡在高大的教主面前。教主轻蔑地俯视她，向前逼近，将她推开。'
q['grip']='小鱼伏在地上，沾灰的小手攥紧教主黑金长袍的拖尾，衣料被拉出绷紧的褶皱。'
q['door']='火光掠过空旷的中央通道，尽头正门已经关紧。冷光从门缝漏入，门板忽然一震。'
q['ward']='ChatGPT 抬起手。千问将小鱼护进怀里；Perplexity 护住祭坛。银白水光越过中殿穹顶，向中央聚拢。'
q['water']='天瀑从夜空轰穿中央中殿的穹顶，碎石随水向两侧飞散。巨瀑落地，水浪扑灭低柴火，将黑袍教徒冲向两侧；教主以暗金力量挡开水流，仍稳站原地。后殿拱顶完整，Claude 仍受缚，发梢和裙边被溅湿。'
q['approach']='天瀑停下，湿黑柴堆冒着水汽，浅水向两侧退去。教主没有挪动，暗金光仍分开脚边水流；ChatGPT 沿留空的通道走近，与他对视。千问抱着小鱼，Claude 尚未解锁。'
q['gptform']='白紫水光裹住 ChatGPT，她腾起，身体化为白紫长身水龙；白角与紫鬃在水光中展开。'
q['priestform']='教主离地升起，黑金羽翼在背后展开，进入人形鸦翼战斗态，面容仍然可辨。'
q['ascend']='白紫水龙和黑金鸦翼教主穿过中殿穹顶的破口，升到教堂上空，两道力量遥遥相对。'
q['eye']='小鱼靠在千问怀里，疲倦地抬眼。蓝色眼睛中倒映着腾空而起的白紫水龙，泪光微微一颤。'
q['sky']='保留钟楼上方的天空特写。夜云被闪电照亮，雨逐渐落下，几声沉闷的雷响带过空中的激战。'
q['rain']='雨滴穿过中殿穹顶破口，打在湿石地板上，涟漪里晃过白紫和暗金闪光。雷声由远及近，又渐渐退去。'
q['outside']='切到雨中的教堂外全景。窗内与门口交替闪出橙金、紫白魔法火光，几次短促爆闪和闷响带过殿内交战；建筑没有持续起火。'
q['return']='战斗结束，雨渐停。ChatGPT 已恢复人形，从中殿破口下落到湿地，身旁水光散去。教主与教徒已经倒地，九位援军都在，千问仍抱着小鱼。众人确认阻碍解除，才走向后殿祭坛。'
q['claudeye']='父亲的声音传来，Claude 的金色眼睛里映出他趴在湿地上、抬头伸手的身影。她的目光颤了一下。'
q['plead']='反打看清倒影中的教主：他趴在湿地上，肘撑着身体，已经抬起头，伸手挽留 Claude。喊声尾音在殿中回荡，他再没有力气站起来。'
replacements={
'DeepSeek 把饭碗留在街边矮桌上，松开手，抬头望向远处的宫殿。':q['bowl'],
'她缓缓站起。金色座位仍在她身后的高台上，她没有走下台阶。':q['hesitate'],
'她转过身，小小的脚步声穿过整座大殿。大侧远景里，她走向画面右侧远处的出口，只剩一个蓝色小点。':'她转过身，小小的脚步声穿过整座大殿，最后消失在门外。',
'DeepSeek 躲在侧墙的阴影里，等了一会儿，确认再没有人经过。':q['hole'],
'水盆固定在祭坛最下一级台阶外的右侧地面；':q['basins'],
'冲撞、摔落、衣料拖过石面的声音。':'教主一步步逼近小鱼。衣袍摩擦声压过她的喘息。',
'她猛然挣扎，木架与锁链一同震响。':'她猛然挣扎，木架与锁链一同震响。\n\n'+q['block'],
'另一名教徒递来第二支燃着的火把，教主伸手接过。':q['grip']+'\n\n另一名教徒递来第二支燃着的火把，教主伸手接过。',
'教主走向柴薪。沾灰的小手攥住他的黑金衣摆，他继续迈步；':'教主接过火把后走向柴薪，继续迈步；',
'吟唱逐渐增强，盖过木柴的爆裂声。':'吟唱逐渐增强，盖过木柴的爆裂声。\n\n'+q['door'],
'她们没有停步。Perplexity 边进门边举杖，屏障声立即压入，冷光越过同伴照向祭坛。':'她们没有停步，Perplexity 举杖护住祭坛，千问奔向小鱼。',
'ChatGPT 抬起手。千问将小鱼护进怀里；Perplexity 给 Claude 留下一层几乎透明的护光。穹顶下方，银白水光开始聚集。':q['ward'],
'天瀑从完整穹顶下方轰然落下，银白水幕扑灭柴火，水浪沿地面向两侧卷开，将黑袍教徒冲散。Claude 仍受缚，溅起的水打湿她的发梢与裙边。':q['water'],
'天瀑停下。湿黑柴堆冒着水汽，地面浅水向两侧退去；教徒们狼狈撑地，教主仍站着。千问抱着小鱼留在阶下，ChatGPT 收手，Claude 仍被锁在木架上。其他人挡住靠近的黑袍。':q['approach'],
'小鱼靠在千问怀里，艰难地抬眼。她疲倦的蓝眼睛里倒映着 ChatGPT 的白色龙角和身影，门外冷光勾出轮廓。她认出了来人，呼吸轻轻一顿，身体仍无力。':'',
'以小鱼的认出接入稍早的召集回闪。':'由援军群像接入稍早的召集回闪。',
'信号短鸣收尾，硬切回教堂并恢复空旷的殿内回声。画面短暂标注“此刻”。水雾渐散，柴火已灭；Claude 仍被锁住，小鱼一直由千问抱护。':'信号短鸣收尾，硬切回教堂并恢复空旷的殿内回声。画面短暂标注“此刻”。此刻柴火仍燃，ChatGPT 准备施展天瀑。',
'教主的黑金长袍卷起气流。ChatGPT 展开龙翼，两道身影掠出敞开的正门，升上钟楼上空。':q['gptform']+'\n\n'+q['priestform']+'\n\n'+q['ascend']+'\n\n'+q['eye'],
'不展开战斗招式。只切到钟楼与夜空，一阵强光在云层中亮起，轰鸣压住其他声音。':q['sky'],
'直接切到战斗之后。':'不展开双方的战斗招式。',
'细尘落在石板缝里，画面边缘一角黑金长袍一动不动。轰鸣的尾音散尽。':q['rain'],
'尘埃缓缓落下。':'雨渐停，水雾缓缓散去。',
'ChatGPT 从敞开的正门落回教堂，收拢龙翼。众人确认阻碍已经解除，才向祭坛走去。':q['return'],
'她的目光颤了一下，慢慢从父亲声音的方向移开，回望曾禁锢自己的空十字架。身侧的 ChatGPT 安静守着她。':q['claudeye']+'\n\n'+q['plead']+'\n\n她慢慢移开目光，回望空十字架。身侧的 ChatGPT 安静守着她。'
}
# Keep quotes updated by replacement where a full phrase overlaps; shot-specific passages below.
for a,b in replacements.items():
 assert a in script,a
 script=script.replace(a,b)
# Remove duplicate early hand emphasis, keeping the hesitation once after the departure.
script=script.replace('ChatGPT 的手指压紧扶手上的雕纹，停了一拍。\n\n她将这点迟疑藏回平静的表情；手仍留在扶手上。','她保持平静，没有立刻回答。')
# Move the existing recruitment block directly after the entrance reveal, before the spell.
start=script.index('由援军群像接入稍早的召集回闪。')
end=script.index('教主拦住通往祭坛的路。',start)
flash=script[start:end]
script=script[:start]+script[end:]
at=script.index('从敞开的门内望向祭坛，ChatGPT 沿中央通道前行；')
script=script[:at]+flash+script[at:]
# Ground fight follows the sky/rain bridge, then the exterior ellipsis.
start=script.index('教堂内，各路 AI 娘迎向涌来的教徒。')
end=script.index(q['sky'],start)
ground=script[start:end].strip()
script=script[:start]+script[end:]
at=script.index(q['rain'])+len(q['rain'])
script=script[:at]+'\n\n'+ground+'\n\n'+q['outside']+script[at:]
script+='\n\n- v0.8 当前采用顺序：入场群像→稍早邀约回闪→天瀑破中殿穹顶、灭火冲散→抗水教主与GPT对话→白紫水龙/黑金鸦翼升空→宝宝龙影→原天空特写雷雨→雨滴→殿内同伴迎敌→教堂外爆闪省略→战后恢复人形、解锁与施法力竭接抱。后殿拱顶和出口保留，雨在战后渐停；双盆对称，右盆承接第一支火把。历史备注不覆盖本段。\n'
shots={s['id']:s for s in d['shots']}
layouts={}
added=[]
def pic(id,name,cell=0,cols=1,rows=1,visible=''):
 s=shots[id];path='镜头设计/图像/'+name
 s['panel_index']=cell
 s['presentation']=dict(path=path,role='action',visible=visible,status='v0.8修订候选，待作者审阅',missing='静帧表达状态，连续变身、雨雷与动作仍待视频阶段验证。',show_as_main=True)
 s['refs']=[dict(path=path,role='本镜修订源图')]+[r for r in s['refs'] if not r['path'].startswith('镜头设计/图像/')]
 for k in ['page_size','panel_rect_pixels','panel_region','display_crop_normalized','generation_request']:s.pop(k,None)
 layouts[path]=dict(path=path,cols=cols,rows=rows)
def update(id,key,**kw):
 s=shots[id];s.update(action=q[key],source_quote=q[key],**kw)
def add(id,anchor,seconds,key,title,framing):
 s=copy.deepcopy(shots[anchor]);shots[id]=s
 for k in ['time_caption','split_screen_reveal']:s.pop(k,None)
 s.update(id=id,seconds=seconds,title=title,action=q[key],source_quote=q[key],purpose=title,framing=framing,entry_state=q[key],exit_state=q[key],dialogue='无对白',dialogue_cues=[],invariants=[])
 added.append(id);return s
update('CY004A','bowl',entry_state='听见今夜火祭消息，抱着饭碗。',exit_state='把碗留在桌上，焦急赶去求助。')
pic('CY004A','CY004A-放碗担忧-v008.png',visible='担忧皱眉，饭碗已经留桌。')
hand=copy.deepcopy(shots['CY007A'])
for k in ['presentation','panel_index','refs','page_size','panel_rect_pixels','panel_region']:
 if k in hand:shots['CY010'][k]=copy.deepcopy(hand[k])
update('CY010','hesitate',title='扶手上的迟疑',framing='手部特写',entry_state='宝宝已离开，GPT仍坐着，远处钟声传来。',exit_state='手指压紧后松开；决定与行动留到召集回闪。',invariants=['只以手部动作表达迟疑，不展示起身。'])
shots['CY009'].update(source_quote='她转过身，小小的脚步声穿过整座大殿，最后消失在门外。',exit_state='宝宝离开，钟声传来。')
pic('CY010A','潜入同一侧墙-四格-v008.png',0,2,2,'教堂本体侧墙洞口紧邻宝宝，教徒从侧门离开。')
update('CY010A','hole',entry_state='宝宝藏在教堂本体侧墙，洞口就在身边。',exit_state='教徒离开，准备由此洞钻入。')
pic('CY011','潜入同一侧墙-四格-v008.png',1,2,2,'机位在堂内，宝宝从画左月光洞口向右钻入暖光内殿。')
shots['CY011'].update(framing='内侧贴地侧近景',action='帽沿脱开石边，头肩从左侧洞口钻入，双手撑上堂内地面。',entry_state='她已从外侧探入同一墙洞。',exit_state='身体穿过洞口，落在同一左侧墙内。')
pic('CY012','潜入同一侧墙-四格-v008.png',2,2,2,'同一洞口在左前景，深处三级祭坛与双盆。')
pic('CY013','CY013-祭坛双盆远景-v008.png',visible='拉远建立全祭坛：三级低宽阶、单平台、固定脚托、两侧低柴与阶下对称双盆。')
shots['CY013']['framing']='祭坛大远景'
shots['CY020']['action']='Claude看见教主逼近宝宝，喊出制止并挣扎；此时尚未发生下一次摔落。'
add('CY020B','CY020',3,'block','小鱼挡住教主','宝宝后方低角度仰视')
pic('CY020B','阻拦抓袍与破门前-四格-v008.png',0,2,2,'宝宝背向镜头张臂，教主高大、轻蔑地俯视。')
shots['CY020B'].update(entry_state='Claude制止，宝宝仍挡在教主面前。',exit_state='教主逼近推开她，接失守倒地。')
add('CY021B','CY021',2,'grip','攥住袍尾','手部与拖尾局部特写')
pic('CY021B','阻拦抓袍与破门前-四格-v008.png',1,2,2,'白绒袖口小手抓紧黑金拖尾。')
shots['CY021B'].update(entry_state='宝宝无力站起，教主就在她旁边。',exit_state='衣摆被拉住，教主伸手接第二支火把。')
pic('CY021A','阻拦抓袍与破门前-四格-v008.png',2,2,2,'教主与教徒上半身火把交接，宝宝在画外，受缚Claude在后。')
shots['CY021A'].update(framing='上半身中近景',entry_state='宝宝在画外攥住袍尾，第一支火把仍在右盆。',exit_state='教主接牢第二支火把，迈步扯开宝宝的手。')
shots['CY022A']['entry_state']='宝宝刚抓住的袍尾随教主前行，从指尖滑脱。'
add('CY022C','CY022B',2,'door','破门前的静默','正门环境远景')
pic('CY022C','阻拦抓袍与破门前-四格-v008.png',3,2,2,'正门紧闭，门缝冷光与殿内火光。')
shots['CY022C'].update(entry_state='低柴正燃，吟唱响起。',exit_state='门板震动，接GPT踹门。',sound='吟唱压低，门板闷响，短暂吸气式停顿。')
update('CY024A','ward',exit_state='银白水光从屋顶外聚集，千问护住宝宝。',invariants=['还未破顶；下镜天瀑冲破中央穹顶。'])
shots['CY024A']['time_caption']={'text':'此刻 · 天瀑。','offset':.1,'duration':1.7}
update('CY024B','water',entry_state='屋顶外水光聚集。',exit_state='中殿破顶，柴火熄灭，教徒冲散，教主不动。')
pic('CY024B','CY024B-天瀑破顶三阶-v009.png',visible='巨瀑冲开中央穹顶、扑灭低柴；教主抗住水流，后殿仍受保护。')
update('CY027','approach',title='抗水而立',framing='低机位双人中远景',entry_state='瀑流刚停，教主仍在原位。',exit_state='GPT走近，面对教主。')
pic('CY027','CY027-教主抗水三阶-v009.png',visible='GPT走近抗住水流的教主，背后祭坛三阶，头顶中殿破口。')
shots['CY026'].update(action='GPT在稍早的宫殿发出集合信号，对应CY021同一次鸣响；回闪结束接当前GPT施法。',exit_state='切回现在的教堂，柴堆仍燃，天瀑即将发动。')
shots['CY027A']['entry_state']='GPT已经走近抗水而立的教主，双方在湿地对峙。'
add('CY027B1','CY027B',2,'gptform','白紫水龙显形','仰视近景／变身')
pic('CY027B1','变身升空与雨滴-四格-v008.png',0,2,2,'GPT被水光包围，龙躯显形；动态需衔接为同一人变身。')
add('CY027B2','CY027B',2,'priestform','黑金鸦翼展开','仰视中景／战斗态')
pic('CY027B2','变身升空与雨滴-四格-v008.png',1,2,2,'教主保留人脸人身，展开黑金羽翼。')
update('CY027C','ascend',title='破口之上',entry_state='白紫水龙和鸦翼教主已完成变身。',exit_state='双方升入夜空，宝宝从下方看见。',invariants=['通过中央屋顶破口升空；不是穿正门，不再是人形GPT。'])
pic('CY027C','变身升空与雨滴-四格-v008.png',2,2,2,'白紫巨龙与黑金鸦翼教主在破顶教堂上空对峙。')
update('CY025','eye',entry_state='GPT已经化龙腾空，宝宝在千问怀里。',exit_state='眼中龙影上升，接天空雷雨。',sound='水流升空的尾音，远雷渐起。')
pic('CY025','CY025-眼中升空水龙-v008.png',visible='疲倦蓝眼睛倒映上升的白紫水龙。')
update('CY027E','sky',seconds=4,entry_state='两人在教堂上空交战，画面离开人物。',exit_state='雨开始落下，雷声延续到地板镜。',sound='雨渐密；三声间隔闷雷，咚、咚、咚，闪光相应。',invariants=['保留原天空特写源图；雨雷与光闪在视频/后期阶段实现。'])
update('CY027E1','rain',title='雨滴落入大殿',entry_state='天空雷雨，战斗仍在画外。',exit_state='雨声接入殿内，同伴迎向残余教徒。',sound='贴近的雨滴、湿地涟漪，远雷尾音。')
pic('CY027E1','变身升空与雨滴-四格-v008.png',3,2,2,'雨滴打在湿地，涟漪反射天空光闪。')
shots['CY027D'].update(entry_state='雨滴落地；留在殿内的同伴迎向重新聚来的教徒。',exit_state='八人迎敌，千问护住宝宝，下一镜从教堂外省略交战。')
shots['CY027D']['action']=shots['CY027D']['action'].replace('屏障内','后殿拱顶下')
add('CY027E2','CY027D',3,'outside','窗内的战斗','教堂外大远景')
pic('CY027E2','CY027E2-教堂外战斗爆闪-v008.png',visible='雨中教堂窗内火光爆闪，建筑未持续燃烧，省略殿内交战。')
shots['CY027E2'].update(entry_state='同伴已经迎敌，切到建筑外。',exit_state='爆闪停下，雨渐停，接战后全景。',sound='数次短促魔法爆鸣，玻璃共振；尾声沉下。')
update('CY027F','return',entry_state='空中与殿内战斗均已结束，雨渐停。',exit_state='GPT恢复人形落地，所有敌人倒地，众人走向祭坛。')
pic('CY027F','CY027F-破顶战后归来-v008.png',visible='GPT在中殿恢复人形落地，九位援军与怀中宝宝、倒地敌方同框。')
update('CY029','claudeye',framing='金色眼睛极近特写',exit_state='眼中父亲抬头伸手；接他的反打。')
pic('CY029','Claude倒影与教主挽留-双格-v008.png',0,1,2,'Claude金眼中倒映倒地抬头的父亲。')
add('CY029E','CY029',2,'plead','无力挽留','贴地反打近景')
pic('CY029E','Claude倒影与教主挽留-双格-v008.png',1,1,2,'教主趴在湿地伸手挽留，头已经抬起，不能重新站立。')
shots['CY029E'].update(entry_state='上镜倒影和画外喊声已经发生。',exit_state='尾音散去，Claude转向空刑架，接焚架。',sound='“回来”的殿内回声渐弱，不重复播放第二遍台词。')
# Preserve footage reuse and temporal order while making stable-ID additions.
ids=[s['id'] for s in old['shots'] if s['id']!='CY007A']
for anchor,new in [('CY020','CY020B'),('CY021','CY021B'),('CY022B','CY022C'),('CY027B','CY027B1'),('CY027B1','CY027B2'),('CY029','CY029E')]:
 ids.insert(ids.index(anchor)+1,new)
flashids=[i for i in ids if i.startswith('CY026')]
ids=[i for i in ids if i not in flashids]
pos=ids.index('CY024')+1;ids[pos:pos]=flashids
ids.remove('CY025');ids.insert(ids.index('CY027C')+1,'CY025')
ids.remove('CY027D');ids.insert(ids.index('CY027E1')+1,'CY027D')
ids.insert(ids.index('CY027D')+1,'CY027E2')
geometry='祭坛只有三级低宽石阶接一个平平台；无侧阶。Claude受缚时赤足踩固定木脚托；低柴分两侧，阶下左右对称双铜盆，第一支湿火把只在右盆。'
for s in shots.values():
 # Replace old quoted substrings only when present in new script; exact overrides handle changed shots.
 if s['source_quote'] not in script:
  for a,b in replacements.items():
   if s['source_quote'] in a and b in script:
    s['source_quote']=b;break
 # Remove stale rules inherited from prior versions, then add the current geometry.
 s['invariants']=[v for v in s.get('invariants',[]) if not any(t in v for t in ['祭坛只有','完整穹顶','屋顶完整','屋顶与出口完好','回闪后','门外升空','从正门升空','先护罩'])]
 if s['scene'] in ['S03','S04','S05'] and not s['id'].startswith('CY026'):s['invariants'].append(geometry)
 if s['scene']=='S05' and not s['id'].startswith('CY026'):
  s['invariants'].append('天瀑只破中央中殿屋顶；后殿拱顶和正门留存。战后雨渐停，Claude蒸干后不再淋湿。')
 for field in ['action','entry_state','exit_state','purpose','framing']:
  s[field]=s[field].replace('完整穹顶下','中央穹顶破口下').replace('Claude仍在屏障内','Claude仍在后殿拱顶下')
sequence=[shots[i] for i in ids];t=0
for i,s in enumerate(sequence):
 assert s['source_quote'] in script,(s['id'],s['source_quote'])
 s.update(start_second=t,end_second=t+s['seconds']);t+=s['seconds']
 nxt=sequence[i+1] if i+1<len(sequence) else None
 s['next_link']=f"接 {nxt['id']}：{s['exit_state']} → {nxt['entry_state']}" if nxt else '结束。'
 s['editorial_review']=dict(version='v008',status='candidate_static_review',dynamic_execution='pending')
 s['visual_prompt']=f"《穿云》{s['id']}。{s['action']} 开始：{s['entry_state']} 结束：{s['exit_state']}。角色母本不变，无图内文字。"
d['shots']=sequence
for sc in d['scenes']:
 ss=[s for s in sequence if s['scene']==sc['id']]
 sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)))
used={s['presentation']['path'] for s in sequence}
d['page_layouts']=[p for p in d['page_layouts'] if p['path'] in used and p['path'] not in layouts]+[p for p in layouts.values() if p['path'] in used]
d.update(version='v0.8',revision='v008',title='《穿云》带图分镜 v0.8',total_seconds=t,story_script='剧本/穿云-场景剧本-v0.8.md',subtitle=f'六场 · {len(sequence)} 镜 · {t//60} 分 {t%60} 秒。天瀑破顶、雷雨省略双线战斗、力竭接抱。',origin_manifest='镜头设计/生成记录/镜头重排-v008/输出归档.json',roughcut_preview_label='旧版配乐粗剪 v002（未包含当前v0.8新画面与重排）')
for m in d['masters']:
 if 'ALTAR' in m['id']:m['status']='历史参考，当前以M-ALTAR-v008为准'
d['masters'].append(dict(id='M-ALTAR-v008',title='三级双盆祭坛',role=geometry,status='v0.8候选',limits='近景允许盆被角色遮挡，不另造台阶。',path='镜头设计/图像/CY013-祭坛双盆远景-v008.png'))
d['continuity'].update(church=geometry,signal='CY021/CY026为同一次信号。入场群像接稍早回闪，再回当前施法；宝宝龙影出现在真正变身升空后。',magic='天瀑破中殿穹顶、灭火冲散，教主抗住；双方对话后变身升空。天空雷雨→雨滴→同伴迎敌→教堂外魔法爆闪→战后才解锁。',wet_state='中央中殿露天，后殿拱顶完整。天瀑溅湿Claude；战后雨渐停，在后殿蒸干后不再淋湿。',battle='保留原CY027E天空特写，视频阶段加雨与数声闷雷。CY027E2窗内爆闪表现殿内交战，不让全教堂持续失火。')
d['review_intro']='修订潜入、三阶双盆祭坛与阻拦因果；天瀑破顶后抗水对话、变身升空，天空雷雨和教堂外爆闪分别省略两条战斗线。公主抱离殿保留。'
d['review_focus']='看洞口方向、双盆三阶、破顶后殿保留、龙影时序及雨滴后同伴迎敌。新增变身为候选；连续变身、雨雷和爆闪待视频阶段实现。'
d['revision_notes']=dict(previous_manifest='镜头设计/shot-plan-v0.7.json',previous_html='镜头设计/带图分镜-v0.7.html',added_ids=added,retired_ids=old['revision_notes']['retired_ids']+['CY007A'],retirement_reason='CY007A的手部源图移至CY010，避免重复迟疑。',moved_ids=flashids+['CY025','CY027D'],boundary='新图与静帧重排；沿用21段临时读稿，配乐MP4未重导；作者尚未审阅本轮候选。')
for s in sequence:assert (R/s['presentation']['path']).is_file(),s['presentation']['path']
(R/d['story_script']).write_text(script,encoding='utf-8')
snapshot=R/'镜头设计/带图分镜-v0.7.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
target.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(shots=len(sequence),seconds=t,added=added),ensure_ascii=False))
