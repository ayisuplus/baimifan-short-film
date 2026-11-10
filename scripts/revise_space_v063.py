"""Version the author's four localized visual revisions; never change audio timing."""
import copy,json,hashlib
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
REQ='镜头设计/生成记录/空间张力-v063/完整请求.json'
FIX='后期/空间张力-v018'
# action is deliberately inherited unless the camera crop or time ellipsis needs clarification.
CHANGES={
 'CY003C':dict(framing='碗沿高度冲击近景，手、倾斜饭碗与小鱼半张脸',camera='贴近碗沿，沿一次拍击小幅随动后停住；后方Claude虚焦回望，背景摊位退暗。',note='拍击后倾饭状态，非硬首帧。手掌拍外碗沿，不伸进饭里；小鱼始终握住同一碗。白米饭单向落下，去掉混淆米粒的花瓣与金色飘粒。',en='Bowl-height close shot of one palm striking the outside rim, rice spilling downward and the child retaining the same bowl; Claude remains worried in soft depth.'),
 'CY004B':dict(framing='偏侧远景，多段长阶斜向通往远处宫门，小鱼在中远景',camera='低位偏左远景，石阶与栏杆斜向向右上收束；只轻跟小鱼跑上一小段，切宫门省略剩余路程。',action='日落后蓝紫暮色里，小鱼空手跑上宫殿外长阶的一小段；多段台阶伸向高门，两旁紫旗与局部暖灯保持。随后切到已抵宫门，省略剩余登阶路程。',exit='小鱼仍沿长阶向宫门奔跑；切下一镜省略余下路程，下一镜已到门前。',note='保持2秒，不能高速跑完整条长阶。太阳已落到地平线下，冷天光主导，暖色仅灯具和宫门内部；不是新造长街。',en='Oblique long view of deep palace stairs at blue-violet dusk after sunset. Show only a short section of the empty-handed child running for two seconds; cut elliptically to arrival at the gate.'),
 'CY004C':dict(framing='暮色宫门低机位，交叉长枪与急停的小鱼',camera='沿用原宫门机位与交叉枪构图，仅统一日落后的冷蓝紫天光；宫门内与灯具保留局部暖色。',transition='省略剩余登阶路程，切到小鱼已跑至宫门前急停；暮色与上镜一致。',note='仅光线连续性修订。无可见太阳与金色直射，门外冷、门内暖；两骑士封闭头盔，枪仍交叉。',en='Preserve crossed spears and closed gate composition. Match cool blue-violet dusk with no visible sun; only lamps and door interior remain locally warm. Cut elliptically from the stair run.'),
 'CY004D':dict(framing='暮色宫门低机位，开门与竖枪让路',camera='沿用原开门放行构图及运镜，门外冷蓝紫暮色，门内仍为暖烛光。',note='仅光线连续性修订。保持原开门、收枪、孩子进门动作；室内暖光是烛光，不回到夕阳直射。',en='Preserve the original open-door passage and upright spears. Maintain cool twilight outside and warm candlelit palace interior, without visible sun or direct sunset.'),
 'CY015':dict(framing='小鱼侧后肩侧双人近景，孩子侧脸、Claude俯视与腰锁同框',camera='同侧近机位沿孩子仰视联系Claude，双方说话嘴可见；手够向腰锁，背景退暗，避免退成全身合照。',note='小鱼站最高平整台面木架左侧；Claude直立双腕受缚，双踝与脚托在画外仍保持。保证对白顺序与口型不变；无钥匙工具。',en='Same-side close two-shot links child side profile and Claude looking down, both speaking mouths visible, hands reaching closed waist lock. Preserve standing/bound states outside crop.'),
 'CY016':dict(framing='沿腰链看手与闭合锁的紧近景，小鱼紧绷侧脸在左',camera='贴近腰锁与双手，窄景深沿绷紧链条短移；先看掰锁失败，再看手转抓链，局部侧脸保留受力表情。',note='掰锁转拉链中间状态，不是解锁成功。Claude只见躯干及局部受缚腕，脸/脚画外；锁和链均完整闭合，无钥匙工具。',en='Tight close-up on closed waist padlock, small hands, taut chain and strained child profile. First pry unsuccessfully, then pull chain; no key, broken link or release.',cast=dict(visible=['DeepSeek','Claude'],offscreen=[],reflection=[],note='Claude仅躯干及局部受缚腕，脸与脚画外；小鱼局部脸/双手。')),
 'CY016D':dict(framing='沿乌烬木斜线的低位中近景，小鱼前景、搬柴者右缘、高处祭坛左后景',camera='保留小鱼左、搬柴者右，偏侧看木头纵深；阶梯退向左后，远处Claude虚焦，不再正中对称。',note='这是抓牢木端的中间状态。开头仍接松锁下阶，未加推搡；同一教徒一根木，小鱼双手抓同一端。木未燃，火盆仍普通暖火。',en='Oblique low medium close shot along one log. Child left grips its end, cropped carrier right, stairs and bound Claude recede to far left. Start with original release-lock and descent, then grip; no push yet.'),
 'CY017':dict(framing='地面侧近景，撑地小手与伸出的另一只手，过路袍靴形成遮挡',camera='镜头落到地面，近看小鱼半跪撑手；搬柴者从右前景继续上阶，正中祭坛在画外，阶边与经过者形成纵深。',note='一次推开后的代表状态，不能跳过推开动作。撑地一手、伸手一手，半跪而非第三只手；搬柴不中断，高处Claude在画外。',en='Ground-level oblique close view after one push: child left half-kneels with one hand planted and the other reaching; carrier and log exit right/upstairs. Altar is outside crop.',cast=dict(visible=['DeepSeek','教徒'],offscreen=['Claude'],reflection=[],note='小鱼近景，搬柴教徒右缘与后景；Claude在高处画外。')),
 'CY018':dict(framing='贴地靴腿与落空小手的局部近景，斜向阶沿退到右后',camera='同侧贴地近摄，孩子局部脸/撑手在左下，另一只手伸向右侧离去靴子；上身、木头和祭坛裁出画面。',note='图为拨踢后滑倒、伸手落空状态，不是开头就趴地。先撑起拦另一人小腿，后被一次拨开；靴子与身体留间隙，不新增伤势。',en='Ground-level close detail of child left reaching after a departing boot right following one non-graphic shove aside. Begin with rising and catching a second carrier leg; upper torso/log and altar stay outside crop.',cast=dict(visible=['DeepSeek','教徒'],offscreen=['Claude'],reflection=[],note='小鱼局部脸与双手、教徒袍靴；主教徒上身和所抱木头画外，Claude高处画外。'))
}
CHANGES['CY016D'].update(
 cast=dict(visible=['DeepSeek','教徒','Claude'],offscreen=[],reflection=[],note='小鱼与搬柴者近景；Claude只在左后高处虚焦受缚，无对白。'),
 note='这是抓牢木端的中间状态。切镜省略松锁后下阶路程，从阶下抓木起；未加推搡。同一教徒一根木，小鱼双手抓同一端。木未燃，火盆仍普通暖火。',
 en='Oblique low medium close shot along one log. Child left grips its end, cropped carrier right, bound Claude visible out of focus far left upstairs. Elliptically omit the descent and start at the stair foot reaching for the log; no push yet.'
)

def main():
 old=json.loads((ROOT/'镜头设计/shot-plan-v0.62.json').read_text('utf-8'));new=copy.deepcopy(old)
 jobs=json.loads((ROOT/REQ).read_text('utf-8')); chosen={j['id']:j for j in jobs if j.get('selected_for_v018')}
 for s in new['shots']:
  sid=s['id']
  if sid not in CHANGES:continue
  c=CHANGES[sid];j=chosen[sid]
  s['previous_presentation_v062']=copy.deepcopy(s['presentation'])
  s['presentation'].update(path=j['project_output'],status='v063空间与张力修订候选，待作者审阅',missing='静帧候选；动作接触、口型和连续运动待动态核验')
  s.update(framing=c['framing'],camera=c['camera'],visual_prompt=j['prompt'],generation_request=REQ,revision_v063=dict(note=c['note'],camera_en=c['en'],action_en=c['en']))
  if 'action' in c:s['action']=c['action'];s['source_quote']=c['action']
  if 'exit' in c:s['exit_state']=c['exit']
  if 'transition' in c:s['revision_v063']['transition_zh']=c['transition'];s['revision_v063']['transition_en']=c['en']
  if 'cast' in c:s['revision_v063']['cast']=c['cast']
  s['presentation']['visible']=s['action']
  s['refs'].insert(0,dict(path=j['project_output'],role='v063当前空间张力候选'))
  s['invariants'].append(c['note'])
  s['final_static_review']=dict(version='v063',status='pending_author_review',review=FIX+'/视觉复核.md',dynamic_execution='pending')
  with Image.open(ROOT/j['project_output']) as im:w,h=im.size
  s['page_size']=[w,h];s['panel_rect_pixels']=[0,0,w,h];s['panel_region']=dict(x=0.,y=0.,w=1.,h=1.)
 new.update(title='《白米饭》带图分镜 v0.63 · 空间与张力修订',version='v0.63',revision='v063',previous_source='镜头设计/shot-plan-v0.62.json',story_script='剧本/白米饭-场景剧本-v0.62.md',subtitle='133镜 · 464.4秒 · 四批空间与张力修订',roughcut_preview=FIX+'/全片声音预览.html',audio_repair_plan=FIX+'/配音对位方案.json')
 new['revision_notes']=dict(scope='按页面顺序第2/3/8/10批；7张构图修订及2张相邻宫门改光；CY017A保留。时长对白声音不变。',generation_requests=REQ)
 assert [(s['id'],s['seconds'],s.get('subtitle_cues')) for s in old['shots']]==[(s['id'],s['seconds'],s.get('subtitle_cues')) for s in new['shots']]
 (ROOT/'镜头设计/shot-plan-v0.63.json').write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n','utf-8')
 original=(ROOT/'剧本/白米饭-场景剧本-v0.61.md').read_text('utf-8')
 notes='# v0.62 摄影修订（2026-10-27，优先于下方保留正文的摄影说明）\n\n当前镜头源 v0.63、生成板 v018。剧情、对白及原镜长不变。\n\n'+'\n\n'.join('**'+sid+'**：'+c['camera']+' '+c['note'] for sid,c in CHANGES.items())+'\n\n---\n\n'
 (ROOT/'剧本/白米饭-场景剧本-v0.62.md').write_text(notes+original,'utf-8')
 print('Authored nine v063 visual references.')

if __name__=='__main__':main()
