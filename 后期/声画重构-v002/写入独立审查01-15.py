import json
from pathlib import Path
R=Path(__file__).resolve().parent
E='后期/声画重构-v002/证据/独立01-15/'
def issue(b,s,e,ids,problem,repair,origin,ev,category='regenerate',seconds=None):
    return dict(batch_number=b,final_start=s,final_end=e,shot_ids=ids,problem=problem,minimum_repair=repair,origin=origin,evidence=[E+x for x in ev],classification=category,reshoot_seconds=seconds,confidence='high' if b in [11,12] else 'medium-high')
issues=[
issue(7,89,96.666667,['CY012','CY013','CY014'],'入殿末仍在最下层，接Claude俯视与脚镣后已经抵达最高坛。原空间省略未给攀阶启动/到达，潜入的谨慎和距离感被削弱。','在7→8间补小鱼上阶2–3秒有效动作，生成4秒；表现方向与脚步，不要求4秒跑完整长阶。','源素材缺桥接，非后期单独引入；B7删卡帽静止1秒与此无关。',['B07-end.png','B08-start.png'],seconds=4),
issue(8,98.583333,100.083333,['CY015'],'小鱼‘我带你出去’期间主要是后帽/背头，Claude脸持续占据明显位置。看得到孩子伸手却看不到她坚定答话；8fps可见Claude略张嘴，存在归属含混，不能据此断言逐字代说。','先保留Claude问句，孩子承诺可后期在既有转头/手部镜头标明声源；若无法取得清楚发话起点，再补2–2.2秒小鱼3/4回答近景。当前最小强制补拍队列不加入。','源分镜执行未给要求的双方嘴可见；后期加速发生于9秒后，不是这句期间。',['B08-dialogue-8fps.jpg'],category='post_or_conditional_reshoot',seconds=2.2),
issue(9,110.791667,114.151625,['CY016A'],'小鱼‘再试一下’声音计划先开始，面部大约到112.5秒才明显开口，前约1.7秒闭嘴/喘息。前一句Claude劝走压孩子低头是合理画外反应，不应误判。','把小鱼发话起点移到明确开口处，后半可接手部再试锁，保持3.36秒原声。优先重排/延长反应，不加速配音；若可用开口不足，再补3.8秒近景。','当前B9原速，错位为源表演与配音排布不同步。',['B09-reply-8fps.jpg'],category='post_or_conditional_reshoot',seconds=3.8),
issue(10,118.291667,124.291667,['CY016C','CY016D'],'先从高坛小鱼旁看搬柴队伍，接队伍特写后小鱼突然已在最低阶抓木；缺‘放弃试锁，决定阻拦柴队’的转身和下阶启动。','10→11之间补2–3秒有效下阶动作，生成4秒；后方Claude留原位，孩子从左前向中央下方远离镜头，保持门在远端。','原素材缺动作桥，前版剪辑没有补足。',['B10-high-start.png','B10-end.png','B11-start.png'],seconds=4),
issue(11,124.291667,127.791667,['CY016D','CY017'],'抓木受推变成双脚同时离地的小跳，然后自己蹲稳、抬手碰帽，缺推动接触和侧向重心失衡。原源2–5秒也存在，不是仅由加速造成。','补5秒同机位抓木→空手触肩→一脚滑移→半跪单手撑地；后面的堆柴可留。','源动作错误，后期把源2–3.75秒150%且删3.75–4.7917秒恢复段进一步放大跳跃感。',['B11-action-8fps.jpg','B11-source-action-8fps.jpg'],seconds=5),
issue(12,137.166667,143.466667,['CY021A'],'6.3秒教主宣判期间前约4秒仍在接火/看交接处，约141.5秒后才清楚开口；‘我的女儿’时视线可能读成面向递火者，非高坛Claude。','7秒主镜，交接最多0.4秒，其后0.4–6.7完整发话；摄影机从高坛方向看教主，让他抬眼望画外Claude且嘴可见；如带交接图仍复制错误机位，去掉此图只留身份。','B12整段100%原速，源表演时序和机位问题，非后期加速。',['B12-dialogue-8fps.jpg'],seconds=7),
issue(13,153.833333,156.333333,['CY020B','CY020A'],'对视后教主胳膊刚扫动就切孩子已离地，触碰肩侧和受力起点没交代。跌落本身存在，但推动因果缺关键一拍。','只补3–4秒同轴一镜，先左手实际触肩，再向画左失衡落地，右手始终持火把；保留此前Claude喊停和短对视。','源未清楚建立接触；后期删源8–8.25秒进一步缩窄动作入口，不能把全部缺陷归于此0.25秒。',['B13-push-8fps.jpg'],seconds=4),
issue(14,156.333333,160.463333,['CY021','CY021B'],'Claude整句‘父亲…放她走’落在小鱼抬头张嘴/喘息脸上，且无Claude发话锚点；容易把父亲称呼误认给孩子。密帧只证实持续开嘴，不证明孩子逐字口型。','补5秒Claude恳求近景，0.25–4.38完整发话，保留句中停顿；旧小鱼仅做短无声反应或用抓袍手部接续，避免再次让张嘴脸覆盖全句。','原设计允许画外但执行产生歧义；当前B14未加速，非新剪法独有。',['B14-dialogue-8fps.jpg'],seconds=5)
]
batches=[]
for b in range(1,16):
    if b<7:
        batches.append(dict(batch_number=b,status='not_expanded_this_priority_pass',summary='已读取voice时间表；按用户后续聚焦7–15，本轮未重新逐帧声画验收，不沿用上一轮通过结论。'))
    else:
        ii=[i for i in issues if i['batch_number']==b]
        batches.append(dict(batch_number=b,status='reviewed_2fps_and_targeted_8fps',evidence=E+f'B{b}-r3-full-2fps.jpg',issues=ii,summary=('需局部重构，见问题。' if ii else 'B15袍角滑脱→教主登阶→触柴→黑焰→Claude反应因果可读，当前不需再生；补拟音和保留选择前停顿。')))
out=dict(scope='v001-r3第1–15批任务；本轮按用户追问优先完整实际复核7–15，1–6仅voice元数据，不宣称通过',source='后期/导演后期修正-v001/导出/白米饭-导演修订-v001-r3.mp4',design='镜头设计/shot-plan-v0.65.json',timing_basis='后期/导演后期修正-v001/后期执行计划.json；24fps最终记录时码',method='B7–15全长2fps实看；B8/9/12/14对白与B11/13动作8fps实看；B11原源2–5秒8fps对照；桥接当前成片原尺寸帧。网格切点近似，精确剪口需回片试剪。',limits=['未实际听审，不评价演员发音/音色/配乐音量或逐音口型','开合嘴与voice窗口比较属于可见发话归属/时序审查','独立拟音/环境声未完成不等于证实当前混音里完全无这些声音','不把所有画外音认定错误；B7教徒指令、B9Claude劝走和快走、B12让开均有合理反应镜动机'],root_cause='原片按画面段落安排动作，未把发话窗口与接触/决定等关键节拍一起拍出；上一轮局部提速又把受推恢复压短。首要恢复说话主体、空间转移和受力，再重排快慢，不整批重做。',batches=batches,minimum_chain=['7→8上阶桥4秒生成/2–3秒有效','10→11下阶桥4秒生成/2–3秒有效','B11受推5秒','B12宣判7秒','B13明确接触推倒4秒','B14Claude恳求5秒'],sound_completion=[{'phase':'潜入/偷救','needs':'远去提灯脚步与教徒命令的距离感；卡帽衣料；空堂脚步；金属锁试失败两次分别有力度与间隔；孩子短促呼吸。'},{'phase':'取柴/阻拦','needs':'脚步节奏持续逼近；木头受拉摩擦；推肩衣料、膝掌触地；堆柴重声；避免把过渡填满BGM。'},{'phase':'宣判/跌落/恳求','needs':'宣判时音乐让位；推倒接触、落地的同步声；Claude称呼父亲后留停顿；抓袍、布料拉紧与滑脱后脚步离去；火触木的一次明确起燃点。'}])
(R/'审查01-15.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')

p=R/'补拍输入01-15.json'
d=json.loads(p.read_text(encoding='utf-8'))
d['scope']='六条最小补拍候选：B11/B12/B13/B14及7→8、10→11桥接。B8/B9先后期尝试，不在本队列。'
new=[
dict(batch_number=13,batch_id='GB011-1',shot_ids=['CY020A'],duration=4,effective_duration=3,mode='reference',prompt='16:9电影级日系动画，4秒单一连续动作镜头。参考1和2分别只决定小鱼与教主身份，参考3提供本场人物左右、视线、黑紫火把与光照状态。用同侧略低机位中近景，稍宽于参考3，必须同时看见教主左手、小鱼肩和双脚到石地，不沿用终态落地图。小鱼画左，教主画右，两人近距离相对。0–0.6秒小鱼张臂挡路，教主右手持唯一黑芯暗紫细边火把，左手尚未触人。0.6–1.2秒教主左掌接触小鱼上臂肩侧，实在接触清楚可见后向画左推开一次。1.2–2.3秒孩子脚短滑、身体朝左侧倾，先手肘或手掌接石地后侧臀落地，不飞出去、不连续翻滚、不主动跳。教主停在右侧，火把全程右手，不靠近孩子头发。2.3–4秒小鱼在地面清醒喘气望右上，教主袍靴仍在右边近处，不踩她、不另推一次。摄影机可微俯跟随下降但不跨轴、不切镜、不用闪光遮挡接触。正常速度，孩子无流血，尚未起身抓袍。保持现行场景服装，不因四视图改披风或增加角色。没有对白、没有字幕、没有配乐。',references=[dict(path='资产/图像/四视图/CHAR-DEEPSEEK-TURN-v003.png',role='identity',visually_checked=True),dict(path='资产/图像/四视图/CHAR-PRIEST-TURN-v001.png',role='identity',visually_checked=True),dict(path='镜头设计/图像/张力与机位-v060/CY020B-v060-r1.png',role='staging_and_prop_state',visually_checked=True)],change_reason='补足左手接触→孩子失衡→落地的一次明确因果，现成片有落地无清楚触碰。',拟替换v001时间段=dict(start=153.833333,end=156.333333,note='只替换对视末至落地；保留先前Claude制止。接触动作必须保留，不能为保持旧总长再删掉。')),
dict(batch_number=7,batch_id='GB006',shot_ids=['CY012','CY013-transition'],duration=4,effective_duration=2.5,mode='first_frame',prompt='16:9日系动画，4秒单镜续接首帧，不重置场景。小鱼在画面左前方最低层地面，唯一Claude仍在正中最上层刑架，双腕受缚。小鱼凝神望高坛一瞬，沿画面左前向中央后上方奔上最近几级台阶，身体远离摄影机、体积逐渐变小，帽尾和发梢落后于急促小步。镜头轻微向前跟随，清楚看脚先踏上一阶再上下一阶，不能穿阶或滑行，不必4秒跑到最高刑架，更不能瞬移到顶端。该镜只交代她开始攀阶；下一镜Claude俯视允许时间省略。保持三段长阶、中央刑架、两侧火盆和单一高烛环，Claude不下台，小鱼不分身。潜入状态低声谨慎，后半略加快但正常动作速度。没有对白、字幕、配乐；轻脚步可供后期参考。',references=[dict(path=E+'B07-end.png',role='first_frame',visually_checked=True)],change_reason='低层入殿直接切高坛偷救缺攀阶动作。只增加攀登启动，不拍全程。',拟替换v001时间段=dict(start=91.583333,end=91.583333,note='在B7/B8边界插入约2.5秒，旧B7末可略收短避免重复前冲；不覆盖Claude问句。')),
dict(batch_number=10,batch_id='GB008R2',shot_ids=['CY016D-transition'],duration=4,effective_duration=2.5,mode='first_frame',prompt='16:9日系动画4秒连续镜头，固定从首帧现有高坛位置继续。左前景仍是受缚Claude部分衣裙与锁链，小鱼在她旁边，远处是门和正在向祭坛走来的搬柴队伍。小鱼看见木头后立刻放开近旁锁链，转身从画面左前沿中央台阶向画面中央偏右的下方远处跑下几级，离摄影机越来越远，朝队伍前端去；这与上一镜低处向高处的上阶方向相反。摄影机位于高坛朝门，跟随轻俯，不绕到教堂外，不镜像场景。必须看见脚一阶一阶下降与身体前倾的决定，不能像漂浮滑行。4秒只拍下阶起步到中段，允许下一镜已到低阶抓木，不必跑完整长阶。搬柴队伍继续向高坛走，与她相向，但本镜不发生接触、不把木头交给她；Claude仍在原刑架不移动，小鱼只有一个。参考帧只一个，保持其人物和服装；无对白、字幕、配乐。',references=[dict(path=E+'B10-high-start.png',role='first_frame',visually_checked=True)],change_reason='高坛偷救转为下阶拦柴缺决定与位置变化。此桥应插在队伍近景后，以新动机重返孩子启动动作，不重复原静态观察。',拟替换v001时间段=dict(start=122.291667,end=122.291667,note='B10/B11边界插入约2.5秒。若回片转身与脚步最清楚段在中段，取完整动作段，不固定只取前2.5秒。'))
]
old_ids={(x['batch_id'],tuple(x['shot_ids'])) for x in d['items']}
for x in new:
    if (x['batch_id'],tuple(x['shot_ids'])) not in old_ids:d['items'].append(x)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('written review and six-item input')
