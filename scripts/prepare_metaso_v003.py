"""Build individually reviewed single-shot repair jobs without changing v025."""
from pathlib import Path
import json, hashlib, argparse, math
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'视频制作/Metaso-H3-v003'
def read(p): return json.loads(p.read_text(encoding='utf8'))
def save(p,v): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
COMMON='严格从固定首帧开始，只让该画面发生指定动作；保持原有角色、服装、道具和空间。单一连续镜头，不切镜，不增加人物，无字幕水印，无背景音乐。'
def add(jobs):
    w=read(ROOT/'后期/制作工作台-v025/工作台数据.json');batches={b['number']:b for b in w['batches']}
    p=OUT/'执行队列.json'
    q=read(p) if p.exists() else dict(version='v003',model='MiniMax-H3',resolution='768P',ratio='16:9',spending_ceiling_credits=5806.1,observed_start_balance=5806.1,authorization='作者要求修复第6、11、20、21、39批剧情与空间错误，沿用已授权Metaso H3积分；40仅必要接头。无充值。',items=[])
    overrides=read(OUT/'镜头改拍.json') if (OUT/'镜头改拍.json').exists() else {}
    for j in jobs:
        b=batches[j['batch_number']]; sid=j['shot_id']; aid=j.get('attempt_id',b['id']+'-v003-'+sid)
        if any(x['attempt_id']==aid for x in q['items']):continue
        ref=ROOT/j['reference'];assert ref.is_file(),ref
        duration=j.get('duration',max(4,math.ceil(j['used_seconds'])))
        item=dict(batch_number=b['number'],batch_id=b['id'],attempt_id=aid,title=b['title'],shot_ids=[sid],film_start=b['film_start'],part_offset=j['offset'],used_seconds=j['used_seconds'],duration=duration,prompt=COMMON+j['prompt'],references=[dict(slot=1,path=ref.relative_to(ROOT).as_posix(),sha256=sha(ref),role='first_frame')],estimated_credits=round(duration*10.2,2),status='prepared',accepted=False,change_reason=j['reason'],repair_of=j.get('repair_of',{'author_rejected_version':'v002','batch_id':b['id']}),source='后期/制作工作台-v025/工作台数据.json',mode='first_frame')
        if j.get('last_reference'):
            last=ROOT/j['last_reference'];assert last.is_file()
            item['references'].append(dict(slot=2,path=last.relative_to(ROOT).as_posix(),sha256=sha(last),role='last_frame'))
        q['items'].append(item);overrides[aid]=j
    q['estimated_total_credits']=round(sum(x['estimated_credits'] for x in q['items']),2)
    assert q['estimated_total_credits']<=q['spending_ceiling_credits']
    save(p,q);save(OUT/'镜头改拍.json',overrides)
    print(json.dumps({'tasks':len(q['items']),'estimated_credits':q['estimated_total_credits']},ensure_ascii=False))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--fragment');args=a.parse_args()
    if args.fragment: add(read(ROOT/args.fragment))
    else: add([
        dict(batch_number=6,shot_id='CY009',offset=0,used_seconds=5,reference='镜头设计/图像/数学宫殿-v056/CY009.png',reason='原图已面向离开方向，取消额外转身；锁定背景GPT躺姿，孩子向近处退出。',prompt='5秒。鲸帽孩子已经背对远处软榻，朝镜头方向离开。她一边轻擦眼泪一边沿地面缓慢走近镜头，不回头、不转身、不走向软榻；相机缓缓后退保持孩子全身。远处白衣GPT始终横躺在同一榻上，头左脚右，只用眼睛跟随孩子，不起身。孩子0–1.7秒轻声说一次<d>[Japanese] じゃあ、自分で行く。</d>，随后嘴闭合，难过却坚持地走。宫殿台阶、软榻、窗格位置不变。'),
        dict(batch_number=6,shot_id='CY010',offset=5,used_seconds=3,reference='镜头设计/图像/宫殿躺姿-v055/CY010-r2-搓手.png',reason='起态已经有双手，不再让手从画外进入；只保留犹豫的手部反应。',prompt='4秒固定手部特写，前3秒用于剪辑。画面中已有且始终只有同一个人的两只手，白袖金镯与紫金软垫不变。0–1.6秒右拇指在左手背上缓慢揉动两下，幅度小；1.6–3秒双手停住，表现犹豫转为决心。3–4秒自然保持供剪辑余量。手不从画外进入，手不离开软垫，不增加第三只手，不出现脸或其他身体。不说话。'),
        dict(batch_number=6,shot_id='CY009A',offset=8,used_seconds=6,reference='镜头设计/图像/数学宫殿-v056/CY009A.png',reason='用明确省略剪辑从手部切到已起身肩后，不强行在背面镜头生成躺到站的不可见过程。',prompt='6秒肩后长轴镜头。白发GPT已停在近景左侧，摄影机紧贴她肩后，只有头后和肩膀局部，脸和下半身不进入画面。她安静注视远处鲸帽孩子。孩子背对镜头沿中轴一直走向已打开的远门，缓慢越过门槛进入云光，身形逐渐变小；不回头不突然跑回。GPT仅有轻微呼吸与发丝摆动，不再做起身、转身或追赶动作。相机固定，不展示榻前立起、不让王座或椅背长在门口，不新增人物。无对白。')
    ])
