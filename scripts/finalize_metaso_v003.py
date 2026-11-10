"""Publish repair candidates; preserve author choices and all earlier versions."""
from pathlib import Path
import json, hashlib, shutil, subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'视频制作/Metaso-H3-v003'
def read(p): return json.loads(p.read_text(encoding='utf8'))
def save(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

q=read(OUT/'执行队列.json'); videos=read(OUT/'视频核验.json'); edits=read(OUT/'剪辑候选.json')
assert len(q['items'])==25 and len(edits)==6
assert len({x['task_id'] for x in q['items']})==25
for x in q['items']:
    assert x['status']=='downloaded_candidate'
    assert read(OUT/(x['attempt_id']+'-受理回执.json'))['response']['task_id']==x['task_id']
    assert videos[x['attempt_id']]['decode']=='passed'
    assert sha(ROOT/x['local_path'])==x['sha256']==videos[x['attempt_id']]['sha256']
for x in edits.values():
    assert sha(ROOT/x['local_path'])==x['sha256'] and x['decode']=='passed'
    assert not x['accepted']

notes={
 'GB005':{'status':'整批修订候选 · 待作者复看','notes':['孩子向远离软榻的方向走；手部从双手已在画内起拍；肩后镜省略起身，避免家具穿插。独立复核未见原整批阻断，离场仍采用切镜省略。']},
 'GB009':{'status':'整批修订候选 · 待作者复看','notes':['重排拨开接触、失衡撑地、抱靴、抬脚挣脱的因果；接触在帽沿/头侧，非肩部推搡；背景重复搬运者与下阶逆行已清理。']},
 'GB015-2':{'status':'整批修订候选 · 待作者复看','notes':['Kimi固定左前方、Claude保持受缚；先闭成不透明护罩，再承受外部攻击；接第21批罩内镜。独立合成复核未见剧情/空间阻断。']},
 'GB016-1':{'status':'整批修订候选 · 待作者复看','notes':['圆刃触腕锁后反馈撤离，避开颈部；护卫两翼展开并留中路；云上GPT左、千问右，扇归千问。千问回应后移0.45秒至合扇后，原声不变速。']},
 'GB029':{'status':'整批修订候选 · 视线待重点复看','notes':['回望空刑架、父亲悬手垂落、左手承托右腕的单火种、孩子仰望依次衔接；清除提前燃烧与多余火源。小鱼抬眼略近镜头轴，高处刑架的视线指向仍偏含蓄，待作者观感复看。']},
 'GB030-1':{'status':'接头修订候选 · 待作者复看','notes':['承接第39批同一枚火种与托腕方向，离指后接冷木纹主观推进。主观段采用本地二维摄影推进；随后硬切木架独立燃烧，省略触木瞬间，切掉旧片持续手部火流。收手与搀扶沿用既有素材，见接头专项复核。']},
}
save(OUT/'审查汇总.json',notes)
metadata=OUT/'参考来源';metadata.mkdir(exist_ok=True)
for p in (OUT/'修订参考').glob('*.json'):shutil.copy2(p,metadata/p.name)
report={'api_tasks':25,'unique_task_ids':25,'downloaded':25,'running':0,'unknown_submission_outcomes':0,'receipt_ids_match':True,'raw_hash_and_full_decode':True,'candidate_batches':list(edits),'candidate_hash_and_decode':True,'actual_spent_credits':q['actual_spent_credits'],'observed_final_balance':q['observed_final_balance'],'author_adopted':False,'audio_boundary':'原速原声；仅第21批千问回应后移0.45秒并重建BGM避让；未作完整听审/口型验收。','known_review_focus':'第39批小鱼仰望目标仍偏含蓄；40仅必要接头连带修订。','references':'参考来源目录保存生成与独立审查记录；实际图像在修订参考目录。'}
save(OUT/'交付核验.json',report)
entry=read(ROOT/'视频制作/当前执行入口.json')
old='Metaso-H3-v002/执行队列.json'
if old not in entry['historical_queues']:entry['historical_queues'].append(old)
entry.update(entry='Metaso-H3-v003/生成进度.html',current_queue='Metaso-H3-v003/执行队列.json',running=0,status='five_batches_repaired_candidates_pending_author_review',current_repair_batches=[6,11,20,21,39],connector_batch=40,note='五批整段修订及第40批必要接头已形成候选。作者对v002的否定记录保留；v003未代作者最终采用。25任务全部下载，无在途任务，不按旧队列重复提交。')
save(ROOT/'视频制作/当前执行入口.json',entry)
doc='''# 五批整段返修 v003

第6、11、20、21、39批已重新设计动作与空间关系并交付剪辑候选，第40批连带修必要接头。当前工作台默认显示这6批，可切回全部44批。旧图、旧片、失败尝试、冻结输入和作者选声均保留；不将候选发布等同最终采用。

## 这次的主要修复

- 第6批：离去方向、双手起态与肩后接镜；起身动作使用剪辑省略。
- 第11批：拨开后失衡、抱靴后受力脱手；接触点为帽沿/头侧，背景人流重新约束。
- 第20批：先闭合不透明护罩，再遭攻击；Kimi与受缚Claude的站位固定。
- 第21批：圆刃触腕锁、护卫两翼展开、云上人物和扇子的归属；合扇后才回应。
- 第39批：空刑架、父亲悬手垂落、同一枚火种和小鱼反应。小鱼视线指向仍偏含蓄，列为作者重点复看。
- 第40批：同一火种离指接冷木纹主观推进。主观段是本地二维摄影推进；第三镜改用旧片7.5–9.333333秒的独立燃烧窗口，去掉手部火流。以硬切省略触木瞬间，无额外生成费用。

## 声音与核验边界

配音文件、作者选择和全片时长保持；第21批千问回应只后移0.45秒，BGM重建局部对白避让。新候选保留原速声音；文件、波形时长和切点核对不代表完整听审或口型通过。

本轮25个Metaso H3任务全部下载，受理任务ID唯一、哈希与完整解码通过；6批合成通过时长与解码检查。用掉1111.8积分，账户页回读剩余4694.3积分，未充值或改账户设置。失败尝试均保留，未默认采用。

版本化的`镜头改拍.json`是本轮设计覆盖，v025冻结输入不回写。`剪辑执行计划.json`列实际素材窗口，`剪辑候选.json`列输出哈希，独立报告保留本轮发现与修复边界。
'''
(OUT/'交付说明.md').write_text(doc,encoding='utf8')
subprocess.run(['python',str(ROOT/'scripts/build_metaso_progress_v002.py'),'--revision','v003'],check=True)
print(json.dumps(report,ensure_ascii=False))
