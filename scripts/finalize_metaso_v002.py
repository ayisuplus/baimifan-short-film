"""Publish scoped production records after all approved tasks return."""
from pathlib import Path
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'视频制作/Metaso-H3-v002'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
q=read(OUT/'执行队列.json');v=read(OUT/'视频核验.json');edited=read(OUT/'剪辑候选.json')
assert len(q['items'])==44 and len(edited)==20
assert all(x['status']=='downloaded_candidate' for x in q['items'])
assert len({x['task_id'] for x in q['items']})==44
for x in q['items']:
 assert len(x['references'])<=9 and len(x['prompt'])<=10000
 assert v[x['attempt_id']]['decode']=='passed' and sha(ROOT/x['local_path'])==x['sha256']
 for r in x['references']:assert sha(ROOT/r['path'])==r['sha256']
for b in edited.values():assert b['decode']=='passed' and sha(ROOT/b['local_path'])==b['sha256']
q.update(observed_final_balance=5806.1,actual_balance_decrease=3709.5,balance_source='2026-10-28 Metaso官方控制台账户页，IAB完整可见额度回读',running=0)
assert round(q['observed_initial_balance']-q['observed_final_balance'],1)==q['actual_balance_decrease']==q['estimated_total_credits']
save(OUT/'执行队列.json',q)
notes={
'GB005':['仅替换后6秒肩后镜，裁掉椅边与腿；以剪辑省略起身起始。'],
'GB007':['原失败批已补齐；四镜按3/2/5/5秒重排。'],
'GB011-1':['成人Claude恢复；左手挥推后切落地，未见踢踩。'],
'GB014':['12→9张参考；反应镜裁掉后窗多余人物。'],
'GB014A':['投刃明确离手；裁去提前裂窗帧，前4秒显形保留。'],
'GB015-1':['破窗、落木、瞬临、逼近四段按原时码重排。'],
'GB016-1':['扇归千问；单镜补拍合扇，闭合后不再展开。'],
'GB018':['11→9张参考；三段切点重新对齐。'],
'GB019':['扇轴/飞叶/碰撞/罩内六段重排，法术边缘保留。'],
'GB020-2':['固定首帧补拍纯水下冲，移除实体鳞片和固定亮眼。'],
'GB021':['删掉多余全殿插镜，近景和画外祈愿按原时码重排。'],
'GB022-1':['12秒蓄势保留，发令用固定首帧补拍后压至1.5秒；水龙无固定亮眼。'],
'GB022-2':['纯水撞盾回片通过本轮材质与散水目标。'],
'GB024':['化龙衣物消散、两者穿出同一屋顶破口分别补拍。'],
'GB026':['16→9张参考；首镜固定首帧，唯一小鱼由千问抱着，暗罩不透明。'],
'GB027':['交钥匙改双手特写；踝扣/腕扣/迈下分别补拍，清除重生火焰、束具和服装串位。'],
'GB028':['无火冷月小鱼反应重拍；眼部近静态段延至4秒，画面时长倍率2.133。'],
'GB029':['小鱼反应独立补拍并裁去开头火景；火种只留Claude段。'],
'GB030-1':['用近景与离地起抱拼接，去掉坐地帧；探膝过程以动作切省略。'],
'GB031':['17→9张参考；离殿重拍为朝正门行进。']}
assert set(notes)==set(edited)
save(OUT/'审查汇总.json',{k:{'status':'本轮目标已修 · 待完整视听','notes':n+['原配音/BGM保持原速；口型与最终跨切仍需完整播放验收。'],'accepted':False} for k,n in notes.items()})
save(OUT/'交付核验.json',{'unique_batches_with_media':44,'new_tasks':44,'all_new_tasks_downloaded':True,'active_tasks':0,'decoded_originals':44,'decoded_edited_batches':20,'reference_images_remaining_13_batches_before':121,'after':101,'maximum_per_request':max(len(x['references']) for x in q['items']),'actual_metaso_credit_decrease':3709.5,'balance':5806.1,'audio_source':'后期/生成收口-v025/全片声音预览.mp3','audio_sha256':sha(ROOT/'后期/生成收口-v025/全片声音预览.mp3'),'full_audiovisual_acceptance':False})
save(ROOT/'视频制作/当前执行入口.json',{'current_provider':'Metaso','entry':'Metaso-H3-v002/生成进度.html','current_queue':'Metaso-H3-v002/执行队列.json','historical_queues':['LibTV-H3-v001/H3节约余量执行队列.json','Metaso-H3-v001/执行队列.json'],'completed_unique_batches':44,'revised_edited_batches':20,'running':0,'note':'44批均已有回片；本轮任务均终态，不可按历史未提交标记重复提交。修订剪辑叠加v025原速配音/BGM供试听，未作最终口型和全片视听验收。'})
readme='''# 白米饭 · 精简参考与返修 v002

当前入口：[44批回片工作台](生成进度.html)。原44批已全部有回片，所有本轮已知画面缺陷均已通过局部复核或可见缺陷消除的剪辑抽核。20批修订剪辑已叠加v025原速日语配音/BGM，供对位试听；没有修改作者选音数据、原声音速度或全片时码。

13批待生成输入121张参考缩至101张，真正超过9图的是第17、25、36、42批（12→9、11→9、16→9、17→9），删的是群像已覆盖的次要身份卡。全部动作和构图图保留，其余9批未删图；Metaso的10000字符容量容纳完整提示词，不再误称这9批也图片超限。

本轮44个独立任务全部回片并解码通过，含剩余13批、原第8批补生成及多轮定点返修。前一轮保留的30批加本轮14个原空缺，形成44批完整候选覆盖。不存在在途任务。Metaso实际余额9515.6→5806.1，消耗3709.5积分，与冻结请求估算总额一致；没有充值或更改账户设置。两次明确并发拒绝保留单独回执，没有重复提交已受理任务。

普通参考模式在水龙、救人和群像上反复重构错误元素，因此改用同一官方H3接口的first_frame模式。7张imagegen内置工具局部修图位于修订参考，旧图与失败回片完整保留。人物/背景不采用新项目或网上替代素材。执行脚本支持参考图和固定首帧两种已文档化输入。

本轮解决的重点包括：水龙亮眼与鳞片、Claude身份、推倒因果、扇子归属与合拢、投刃离手、化龙衣物、救人段火焰/束具/服装连续性、重复孩子、离殿方向和坐地起抱。具体证据见审查汇总与各独立复核JSON。

有意采用的剪辑省略：第6批省略起身最初动作；第13批推手接触用动作切省略；第37批撤罩跨切省略、钥匙改双手特写；第40批探膝瞬间省略以避开坐地。原片均可对比。第38批眼部近静态镜画面拉长2.133倍，其余按EDL记录；原音不拉伸。没有以冻结帧、倒放或重复循环填镜长。

范围边界：采样、关键帧、局部连续抽核与技术解码不等于最终全片视听验收。对白口型、表演、镜间动作连续性、音乐乐句、环境拟音与最终美术采用仍待整片播放审核。这里不把候选标为作者已采用。

媒体沿项目既有规则留本地；Git记录脚本、请求、索引、路径、SHA和审查结果。镜号、原始媒体、历史输入以及既有未提交修改均保留。
'''
(OUT/'交付说明.md').write_text(readme,encoding='utf8')
print('44 tasks verified; 20 edited batches; no active tasks')
