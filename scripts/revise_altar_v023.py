"""Archive the author-requested local altar revisions; never modify source images."""
import copy, hashlib, json, shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REC = '镜头设计/生成记录/祭坛长椅连续性-v023'
IMG = '镜头设计/图像/祭坛长椅连续性-v023'
def read(p): return (ROOT/p).read_text(encoding='utf-8-sig')
def write(p,s): (ROOT/p).write_text(s,encoding='utf-8')
def save(p,x): write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

old=json.loads(read('镜头设计/shot-plan-v0.22.json'))
d=copy.deepcopy(old)
updates={'CY012':('CY012-v023-r8.png','CY012-请求-v008.json'), 'CY022B2':('CY022B2-v023-r2.png','CY022B2-请求-v004.json'), 'CY024B1':('CY024B1-v023-r2.png','CY024B1-请求-v002.json')}
space='祭坛中央彩窗、十字架与多段宽长阶共用中轴。最高石台向十字架后方延伸至实体后墙，两把同款深木长椅分列后墙左右，椅脚落在连续石地，中央登阶通道留空。各椅上方稍偏外有一只单根壁挂烛台；原双悬灯改为中殿高处一盏通透环形烛式吊灯。长阶下、中、上各一对铜火盆共六只，下段两石座各一支蜡烛。v0.23三张候选以CY012-v023-r8为局部空间参考，其他旧镜图片尚未完成新家具与灯具同步。'
light='天瀑前六火盆、一盏中央环形烛式吊灯、两后墙壁烛及两石座单烛提供暖光。顶部刑架低柴到CY022才点燃。CY024B后所有普通灯火与低柴熄灭，含新增壁烛和中央吊灯，冷月光照明；后殿拱顶保持完整。后续掌火及空刑架剧情火焰按原稿，不重新点亮普通灯具。'
replacements={old['continuity']['church']:space}
for s in old['shots']:
 for v in s['invariants']:
  if v.startswith('天瀑前六火盆、两圣灯'): replacements[v]=light
def replace_text(s):
 for a,b in replacements.items(): s=s.replace(a,b)
 return s.replace('六只铜火盆、两盏悬灯及两支石座蜡烛仍亮','六只铜火盆、中央环形烛式吊灯、两只后墙壁烛及两支石座蜡烛仍亮')
script=replace_text(read(old['story_script']))
script=script.replace('版本：v0.22｜','版本：v0.23｜',1)
script=script.replace('## 教堂空间与光源 · v0.14','## 教堂空间与光源 · v0.23')
script=script.replace('版本：v0.23｜2026-10-22｜','版本：v0.23｜2026-10-22｜更新CY012、CY022B2与CY024B1局部空间候选：后墙长椅、壁烛及中央吊灯；其余旧镜图片同步待办。',1)
script=script.replace('她落在教堂内侧的地上，忍住声音，抬起头。','她落在教堂内侧的地上，忍住声音，抬起头。\n\n十字架后方，两把深色木长椅靠着左右后墙，稳稳落在最高石台上；椅背上方各有一只单根壁挂烛台。中殿高处悬着一盏通透的环形烛式吊灯，中央通道敞开。')
impact='贴近最高祭坛后墙左侧的石台，水浪沿平台扑来，撞上此前靠墙摆放的深色木长椅。椅脚先滑过湿石，一端被掀离原位，椅身转向平台前缘；画面露出石台边缘与下行台阶。后墙上的单根壁烛已经熄灭。旁侧黑袍教徒失衡伸手，抓向椅背却落了空，被水带向同一方向。镜头停在长椅刚被掀起的瞬间，不展示人体撞击或受伤细节。'
oldimpact=next(s for s in old['shots'] if s['id']=='CY024B1')['source_quote']
script=script.replace(oldimpact,impact)
write('剧本/穿云-场景剧本-v0.23.md',script)
d.update(version='v0.23',revision='v023',title='《穿云》带图分镜 v0.23 · 祭坛长椅与中央吊灯',subtitle='三处局部空间候选；台词、镜序和时长保持',story_script='剧本/穿云-场景剧本-v0.23.md',source_manifest='镜头设计/生成记录/生成索引-v023.json',origin_manifest='镜头设计/shot-plan-v0.22.json')
d['continuity']['church']=space
d['continuity']['altar_lighting_v023']=light
d['continuity']['remaining_image_sync']='本轮仅更新CY012、CY022B2、CY024B1三图；其他旧图仍可能包含旧双悬灯、无长椅和旧后墙，尚未逐镜同步。v0.16原封版文件不改写。'
d['review_intro']='按作者确认更新三张候选：后墙两把落地长椅、两只单根壁烛、中央高位环形烛式吊灯；冲击镜改为左后方长椅被水掀离石台原位。93镜299秒不变。其他旧镜图尚未同步本次场景改变。'
d['review_focus']='检查空堂→吟唱的家具/灯具对应，以及天瀑后平台长椅受力和壁烛熄灭。新图待作者审阅，动态未制作。'
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.22.json',previous_html='镜头设计/带图分镜-v0.22.html',added_ids=[],modified_ids=list(updates),boundary='仅三图更新，其余90图、全部对白、镜序和时长保持；旧封版原件保留，整片新场景同步未完成。')
d['masters'].append({'id':'M-ALTAR-v023','title':'后墙长椅与中央吊灯局部候选','path':IMG+'/CY012-v023-r8.png','role':space,'status':'作者确认设计方向，生成画面待审','limits':'取代这三图的空间指引；其余历史图未批改。'})
for s in d['shots']:
 s['invariants']=[replace_text(v) for v in s['invariants']]
 s['source_quote']=replace_text(s['source_quote'])
 if s['id'] not in updates: continue
 filename,request=updates[s['id']]
 oldpath=s['presentation']['path']; newpath=IMG+'/'+filename
 s['refs']=[{'path':newpath,'role':'本轮当前候选'},{'path':oldpath,'role':'保留的上一版'},{'path':REC+'/'+request,'role':'实际冻结输入'},{'path':IMG+'/CY012-v023-r8.png','role':'后墙家具与灯具空间参考'}]
 s['presentation'].update(path=newpath,status='v0.23局部修订候选，待作者审阅；不改写v0.16封版')
 s['generation_request']=REC+'/'+request
 s['visual_prompt']=json.loads(read(s['generation_request']))['prompt']
 s['editorial_review']={'version':'v023','status':'candidate_pending_author_review','independent_review':'spatial_and_lighting_passed_with_limits','dynamic_execution':'pending'}
 with Image.open(ROOT/newpath) as im: w,h=im.size
 s['page_size']=[w,h];s['panel_rect_pixels']=[0,0,w,h]
 if s['id']=='CY012':
  s['action']+=' 十字架后墙两侧长椅落地，壁烛与高位中央吊灯点亮。'
  s['presentation']['missing']='静帧不能验证连续登阶；裙边暖轮廓仍偏强，视频中须明确低柴未点燃。'
 elif s['id']=='CY022B2':
  s['framing']='中殿后部低机位／大远景／静帧候选'
  s['action']+=' 后墙长椅、壁烛和中央环形吊灯延续CY012。'
 else:
  s.update(source_quote=impact,framing='最高祭坛后墙左侧／平台贴地局部近景',entry_state='天瀑已落下，水浪冲上最高石台后墙左侧；所有普通灯火已灭。',action='水浪将左后墙长椅一端掀离原位，椅身转向石台前缘；黑袍教徒失衡抓空，壁烛熄灭。',exit_state='长椅刚被掀起、人物被水带偏；切退水后教主原地撑住。')
  s['invariants'][0]='最高祭坛后墙左侧局部，长椅沿用此前建立的同款，石台边缘与下行阶梯交代高度，不新增塌墙或破地。'
  s['next_link']='接CY027：由局部水浪切退水大景，教主仍在护罩内原地。'
  s['presentation']['missing']='从墙边冲离、抬升、横转和落地的连续轨迹与音效待动态验证。'
 s['presentation']['visible']=s['action']
for sc in d['scenes']:
 sc['pages']=list(dict.fromkeys(s['presentation']['path'] for s in d['shots'] if s['scene']==sc['id']))
 sc['path']=sc['pages'][0]
d['page_layouts']=[{'path':s['presentation']['path'],'rows':1,'cols':1} for s in d['shots']]
save('镜头设计/shot-plan-v0.23.json',d)
snap=ROOT/'镜头设计/带图分镜-v0.22.html'
if not snap.exists():shutil.copy2(ROOT/'镜头设计/带图分镜.html',snap)
p='scripts/build_storyboard.py'; code=read(p).replace('shot-plan-v0.22.json','shot-plan-v0.23.json').replace('"v022")','"v022", "v023")').replace("'v022')","'v022','v023')")
write(p,code)
entry=read('00_打开项目.html').replace('v0.22','v0.23')
entry=entry.replace('新增吟唱与天瀑冲击候选','祭坛长椅与中央吊灯候选')
entry=entry.replace('镜头设计/图像/天瀑冲击补镜-v022/CY024B1-v022-r1.png',IMG+'/CY024B1-v023-r2.png').replace('镜头设计/图像/吟唱补镜-v021/CY022B2-v021-r2.png',IMG+'/CY022B2-v023-r2.png')
entry=entry.replace('<a href="归档/',f'<a href="{IMG}/CY012-v023-r8.png">空堂：后墙长椅与中央吊灯<small>两只壁烛 · 新空间候选</small></a>\n<a href="归档/',1)
entry=entry.replace('v0.23含新增候选；原91镜封版保持','v0.23三图修订；其他旧镜场景同步待办')
write('00_打开项目.html',entry)
progress='''## 2026-10-22：后墙长椅、壁烛与中央吊灯（v0.23，候选待审）

作者纠正长椅悬空并明确放到十字架后方靠墙；随后确认两只单根壁挂烛台，并将原双悬灯改为一盏挂高、通透的中央环形烛式吊灯。更新CY012、CY022B2、CY024B1三张候选：前两镜家具在后墙石面落地，后墙与彩窗下半部作相应重建，原多段长阶保持；冲击近景展示左后方长椅刚被掀起、平台边缘和熄灭的壁烛。此前悬空、承托不明及未采用中间稿全部保留。

[当前分镜v0.23](镜头设计/带图分镜.html)与[剧本v0.23](剧本/穿云-场景剧本-v0.23.md)已同步；93镜299秒，台词、镜序和单镜时长保持。独立视觉复核及原件/请求哈希见[记录](镜头设计/生成记录/祭坛长椅连续性-v023/复核记录.md)。图像仍待作者审阅。旧v0.16封版原件不改写。

本轮只更新三张图，其他旧镜仍存在双悬灯、无长椅、旧后墙等整片同步缺口，不能视为新空间已全片封版。静帧不能证明水流轨迹、抬升/落地、吟唱运动；未制作视频或声音。CY012裙边暖轮廓仍偏强，制作时须明确干柴未燃。

'''
text=read('制作进度.md'); marker='## 2026-10-22：天瀑冲击局部补镜'
write('制作进度.md',text.replace(marker,progress+marker,1))
print('v0.23 text and manifest prepared')
