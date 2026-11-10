"""Record the approved avatars and the three newly generated state references."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def write(p,d): (ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def evidence(p):
    f=ROOT/p
    return {'path':p,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'size':list(Image.open(f).size)}
def main():
    approval='2026-10-26 作者：可以了，接着做。采用恶魔v003酒红配色。'
    p='资产/assets.json';a=read(p)
    for group in a.values():
        if not isinstance(group,list):continue
        for item in group:
            if isinstance(item,dict) and item.get('id')=='CHAR-GPT-DEVIL-CHIBI':
                item['status']='作者已采用v003酒红配色'
                item['limits']='沿用已采用大头娃娃比例与酒红配色；侧背为一致性推演，不作工程尺寸。'
    write(p,a)
    p='资产/生成记录/王宫内心戏-v001/恶魔生成记录.json';a=read(p)
    a['records'][-1].update(status='author_adopted',approval=approval);write(p,a)
    angel='资产/图像/王宫内心戏-v001/CHAR-GPT-ANGEL-TURN-v003.png'
    devil='资产/图像/王宫内心戏-v001/CHAR-GPT-DEVIL-TURN-v003.png'
    plate='镜头设计/图像/数学宫殿-v056/CY007.png'
    names=['恶魔提醒','天使反驳','等待回答']
    files=[f'镜头设计/图像/王宫内心戏-v001/CY008M-S0{i+1}-{n}.png' for i,n in enumerate(names)]
    originals=['exec-296a6bb6-616e-42fc-ab0d-95eedbaf63b8.png','exec-baf21807-cce0-4a15-be99-77a6776150a6.png','exec-d3691d9c-1002-4d85-8cfa-6693ef0d43bd.png']
    inputs=[[plate,angel,devil],[files[0]],[files[1],angel,devil]]
    records=[]
    for i,p in enumerate(files):
        records.append(dict(id=f'CY008M-S0{i+1}',**evidence(p),status='generated_candidate_pending_author_review',engine='built-in image_gen',prompt=f'镜头设计/生成记录/王宫内心戏-v001/S0{i+1}-prompt.txt',actual_inputs=[evidence(x) for x in inputs[i]],original_output='C:/Users/36322/.codex/generated_images/01a172cc-398b-71b3-98dc-536dd1b4ac2c/'+originals[i]))
    write('镜头设计/生成记录/王宫内心戏-v001/生成记录.json',{'records':records,'limits':'三张为同一镜头的状态参考，不是三个必切镜头；生成图背景视觉延续但非像素锁定。动态口型、转头、饰物遮挡和背景定格需视频/合成验证。'})
    p='镜头设计/王宫内心戏-已采用增补-v001.json';d=read(p)
    d['status']='story_and_avatar_designs_adopted_state_images_pending_review_voice_and_retime'
    for x in d['candidate_assets']:
        if 'DEVIL' in x['path']:x.update(label='恶魔GPT · v003酒红配色已采用',status=approval)
    d['asset_requirements']=['天使GPT四视图v003已采用。','恶魔GPT四视图v003酒红配色已采用。','同一镜头的三张表演状态图已生成，待作者画面审阅；尚未生成视频。']
    d['shot_design']={'purpose':'让观众看到GPT在协议约束与怜悯之间犹豫；争执不判胜负，现实中的小鱼打断内心戏。','camera':'沿用王座反应近景构图，内心段锁定机位；本体与背景定格虚化。只让两只分身表演、轻微悬浮和转头，避免摄影机运动破坏定格感。','entry':'接小鱼担忧的反应，切回王座上的GPT；以现有反应图定格并逐渐虚化，前景两只分身显现后恶魔开始说话。图片4是分身已出现的表演状态，不作为凭空长出分身之前的起帧。','exit':'图片6两只分身闭口等待，本体不回答。小鱼现有完整日语原声从画外接入，消去分身、解除虚化，切回小鱼离开；这句只播放一次，随后接既有搓手迟疑与起身目送。','timing':'新增两句配音实测前，以下用对白事件定位，秒数暂空；不是已冻结的15秒提交稿。','background_execution':'三张生成图是构图/表演参考。正式合成定格背景应复用同一王座底图，避免生成图之间轻微差异造成背景游动。'}
    actions=[
        ('VO-CY008M-01','恶魔开口至完整句结束','左侧恶魔抱臂、半垂眼，向右侧天使慢悠悠提醒；天使闭口，双手收在胸前担忧地听。','恶魔说完自然闭口，天使接话；不切景、不重启出现动作。'),
        ('VO-CY008M-02','天使接话至完整句结束','右侧天使一手贴胸、一手向小鱼所在画外方向摊开；先心疼，后焦急地反驳。左侧恶魔闭口倾听，不同时说话。','天使收回伸出的手并闭口；两只分身顺着动作转头抬眼望向后方本体。'),
        (None,'天使说完后至小鱼画外打断','两只分身在原位置抬眼等待后方GPT表态，嘴均闭合；本体保持定格，不点头、不答应。','短暂停留后由小鱼现有完整原声打断，切回现实；不安排胜利表情或额外台词。')]
    d['state_sequence']=[]
    for i,(cue,anchor,action,transition) in enumerate(actions):
        d['state_sequence'].append(dict(id=f'CY008M-S0{i+1}',label=names[i],path=files[i],picture_number=i+4,role='同镜头表演状态参考',cue_id=cue,event_anchor=anchor,offset_seconds=None,action=action,transition=transition,status='已生成，待作者审阅'))
    d['reference_images']=[dict(number=i+1,path=p,label=label,role=role) for i,(p,label,role) in enumerate([(angel,'天使四视图','已采用身份与比例'),(devil,'恶魔四视图','已采用身份与配色'),(plate,'王座反应底图','本体姿态与空间；背景定格来源')]+[(p,n,'表演状态候选，不替代身份四视图') for p,n in zip(files,names)])]
    d['next_steps']=['审阅三张内心戏状态图','复核新增两句日语并录制，沿用GPT既有音色','按实测配音重排15秒批次与BGM事件时码','冻结实际模型输入后生成并验证口型、转头和背景定格']
    d['generation_record']='镜头设计/生成记录/王宫内心戏-v001/生成记录.json'
    write(p,d)
    print('Approved devil v003; recorded three state images and event-based shot design.')
if __name__=='__main__':main()
