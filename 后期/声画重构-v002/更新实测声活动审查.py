import json
from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'审查01-15.json'
d=json.loads(p.read_text(encoding='utf-8'))
v=json.loads((R/'选定配音实测停顿.json').read_text(encoding='utf-8'))
d['audio_activity_revision']='已追加选定配音实测停顿.json。文件总长不是持续说话时长；以下区间为幅度阈值信号活动，可能包括呼吸，不等同音素转写或听审。保留原速完整文件，但画面按有效发话与停顿分段。'
d['voice_activity_7_15']=[{k:x[k] for k in ['id','batch','file_duration','signal_intervals']} for x in v if 7<=x['batch']<=15]
for b in d['batches']:
    for i in b.get('issues',[]):
        if b['batch_number']==9:
            i['problem']='小鱼答话镜嘴约112.5秒才明显开口；选声第一活动窗111.0101–111.5330秒已在此前，故至少第一短句存在可见发话起点风险。文件中多处静音/呼吸，不应认定整个3.36秒持续讲话。前句Claude劝走仍是合理画外反应。'
            i['minimum_repair']='按选声各活动窗对齐小鱼的可见开合，停顿可留闭口或插手部。第一短句先找到明确发话锚点，再接试锁；保留文件3.36秒完整原速。若缺能对应第一短句的画面，再补3.8秒近景。'
        if b['batch_number']==12:
            i['problem']='选声实际两段活动为137.6172–139.0709及140.0035–141.6028秒，角色到约141.5秒才明显开始说话；因此第一句和第二句大部分时间确在接火闭口，非把静音尾误算发话。6.3秒文件末1.864秒静音应可切反应。'
            i['minimum_repair']='以新教主朝高坛的近景，分别对应选声0.45055–1.904275、2.83685–4.4361两段发话；0.9326秒句间停顿不强迫嘴动，末1.864秒静音可切孩子反应。完整6.3秒声文件原速，不要求新镜连续说足6.3秒。'
        if b['batch_number']==14:
            i['problem']='选声称呼活动156.5657–157.2227秒、后句159.0796–160.1631秒均缺明确Claude发话锚点，整镜主要是张嘴抬头的小鱼。中间约1.857秒是停顿，应利用留白反应，不应持续制作说话口型。'
            i['minimum_repair']='新Claude称呼近景→1.857秒无对白小鱼反应/手部→Claude后句近景，完整4.13秒文件原速，句间停顿保留。新回片需裁去错误提前燃火与新增后景人物，见v005首轮独立复核.json。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
review={
 'scope':'仅B11/B14首轮回片；未听审，口型仅可见开合及归属，不作逐音通过',
 'items':[
  {'id':'GB009-v005-CY016D-r1','verdict':'candidate_use','method':'全长2fps+0.5–3.2秒8fps','evidence':['视频制作/Metaso-H3-v005/审查/GB009-v005-CY016D-r1-2fps.jpg','后期/声画重构-v002/证据/独立01-15/B11-new-contact-8fps.jpg'],'findings':'空手约1.375–2.25秒真实接触肩/上臂，小鱼随后约2.375–2.75秒下降单手撑地，未出现旧片双脚同时离地弹跳；之后搬柴者离去，孩子伸手仍向木头。','use':[0,5],'required_edit':'保留接触和落地原速，不再150%。头几秒木头牵拉导致一脚抬起，但另一脚仍承重，可理解失衡前抵抗。','limits':'不是全片采用/听审结论。'},
  {'id':'GB011-2-v005-CY021-r1','verdict':'post_crop_and_phrase_edit_required','method':'全长2fps、1.3秒原尺寸及裁切全长4fps','evidence':['后期/声画重构-v002/证据/独立01-15/B14-new-full.png','后期/声画重构-v002/证据/独立01-15/B14-new-crop-4fps.jpg'],'findings':'Claude身份、受缚和前置发话明确，但全幅背景已出现底部木柴橙火与右后新人物，剧情尚未点火，必须排除。静态crop可去除，却在末段低头时下巴贴下沿。','required_edit':{'crop':'750:422:295:10，后段随头下沉建议y=10+12*t；动态crop还需成片确认','spoken_plan':'选声0.23235–0.889375称呼；0.889375–2.746275静音反应；2.746275–3.82975后句；尾部0.30025秒可留闭口等待','source_candidate':'源1.557–2.531为称呼可见发话，源3.361–4.653为后句，时间来自主代理原声活动测量，与2/4fps可见开合大致一致。分句调画面，不调原配音速度。','pause_insert':'优先旧小鱼手部撑地/抓袍前的无嘴反应，不能让另一张明显讲话脸接管停顿。'},'limits':'尚未审动态crop成片；无法从4fps确认逐音嘴型；新增人物/火必须整段排除。'}
 ]}
(R/'v005首轮独立复核.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
print('updated activity-based findings and first-return review')
