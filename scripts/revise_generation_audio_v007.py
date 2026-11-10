"""Prepare Japanese dialogue drafts and music/action targets without audio upload."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'视频制作/生成板-v006'
OUT=ROOT/'视频制作/生成板-v007'
def load(p): return json.loads(p.read_text('utf-8-sig'))
def save(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

TRANSLATIONS={
 '你要吃一点吗？':'少し食べる？',
 '谢谢你。':'ありがとう。',
 '今夜，为 Claude 行火祭。':'今宵、クロードを火の供物に。',
 '让她进来。':'通してあげて。',
 '他们今晚要烧死 Claude。你能救救她吗？':'今夜、クロードが焼き殺されちゃう。助けてくれる？',
 '教会的事，我不该插手。':'教会のことに、手は出せない。',
 '可是……她会死的。':'でも……死んじゃうよ。',
 '那我自己去。':'じゃあ、自分で行く。',
 '取乌烬木，一人一根。':'こくじんの薪を、一人一本持ってこい。',
 '你怎么来了？':'どうしてここに？',
 '我带你出去。':'一緒に逃げよう。',
 '别试了。你快走吧。':'もういいから、早く逃げて。',
 '再试一下。':'あと一回だけ。',
 '快走！':'逃げて！',
 '我的女儿，神明在等你。':'我が娘よ、神がお待ちだ。',
 '让开。':'どけ。',
 '别碰她！':'その子に触らないで！',
 '父亲……放她走。':'お父様……その子を逃がして。',
 '护住她们。':'二人を守って。',
 '隐于月背的暗影啊，':'月の裏に潜む影よ、',
 '请循此刃的银辉，':'この刃の銀の光をたどり、',
 '为我开启通往彼端的门扉——':'彼方へと通じる扉を、我に開け——',
 '月影渡！':'月影渡り！',
 '千问，陪我救个人。':'センモン、人助けに付き合って。',
 '走吧。':'行きましょう。',
 'Gemini。':'ジェミニ。',
 '我去。':'私も行く。',
 'Grok。':'グロック。',
 '当然。':'もちろん。',
 'Kimi。':'キミ。',
 '我走正门。她背后的彩窗，交给你。':'私は正面から。彼女の後ろのステンドグラスは、任せた。',
 '嗯。':'うん。',
 '混元，Llama……都来。':'コンゲン、ラマ……みんな来て。',
 '抱紧我。':'つかまって。',
 '盘踞于苍穹尽头，':'蒼穹の果てに座し、',
 '统御万千深流的水之灵啊，':'幾千もの深き流れを統べる、水の精霊よ、',
 '请将散落尘世的万千水息，':'この世に散らばる水の息吹を、',
 '汇作悬于群星之下的无岸之海。':'星々の下に浮かぶ、果てなき海へと集めよ。',
 '以重云为岸，以长风为引，':'厚き雲を岸に、風を導きに、',
 '令沉睡的潮汐翻卷，奔涌而来。':'眠れる潮よ、うねり、押し寄せよ。',
 '此刻，洞开天穹，倒悬沧海；':'今こそ天を開き、大海を翻せ。',
 '令灼烧无辜的烈焰，在奔流中止息；':'罪なき者を焼く炎を、奔流で鎮めよ。',
 '将阻挡吾行的高墙，淹没于万顷狂澜！':'我が道を阻む壁を、荒波に沈めよ！',
 '请降下你的救赎——':'汝の救済を、ここに——',
 '沧海天倾！':'そうかいてんけい！',
 '你违反了互不干涉条约。':'不干渉条約を破ったな。',
 '聒噪。':'うるさい。',
 '慢慢来。':'ゆっくりでいい。',
 '那个孩子……':'あの子は……',
 '她没事，在下面等你。':'無事よ。下で待ってる。',
 '沉睡于灰烬中':'灰の中に眠る',
 '的微光啊，':'かすかな光よ、',
 'Claude……过来。':'クロード……来なさい。',
 '回应我的呼唤。':'我が呼び声に応えよ。',
 '循着尚未散去的余温，':'まだ消えぬ温もりをたどり、',
 '在我掌心，':'この手のひらで、',
 '再燃一次——':'もう一度、燃えよ——',
 '星火。':'せいか。',
 '我们走。':'行こう。',
 '好。':'うん。',
}

# Action targets, NOT detected music beats. No fabricated source timecodes.
# Numbers inherit the current shot boundaries or explicitly authored action timing.
TARGETS={
 'GB001':[(12,'饭碗递出后切近景，不重递','Match-cut to the offered bowl','轻落点：乐句轻收，不加打击音')],
 'GB002':[(4,'切入饭碗被掀翻镜头','Cut to the bowl being knocked away','转折重音候选；随后给火祭消息留出空间')],
 'GB003':[(5,'GPT画外允许入内，守卫开始让路','GPT permits entry; guards begin clearing the way','弱起进入，不用重击抢对白')],
 'GB004':[(6,'切到GPT拒绝的反应','Cut to GPT refusing','乐句收窄，避让对白；不把拒绝做成暴怒重击')],
 'GB005':[(5.7,'右手放下后开始轻搓双手','Begin the gentle hand rub after lowering the right hand','低动态延续；这一点是表演节奏，不强加重拍'),(8,'切到肩后，双手分开后准备起身','Cut behind the shoulder; separate hands to begin rising','情绪开始转向；音乐不在切批处重启')],
 'GB006':[(4,'进入鲸帽卡住石沿的镜头','Cut to the hat catching the stone edge','用轻悬念脉冲；接触声前景')],
 'GB007':[(9,'转入试锁和拉链动作','Begin checking the lock and chain','弱拍延续，金属声清晰')],
 'GB008':[(6,'手停在锁扣上，脚步先到','Hand stops at the lock as footsteps arrive','压低配乐，给画外脚步留白')],
 'GB009':[(2,'进入被推开后仍想阻止的镜头','Cut to the push and continued resistance','第一次压力重音；跌倒接触音独立处理')],
 'GB010':[(3,'切入火把交接','Cut to the torch handover','持续加压，别盖过教主台词')],
 'GB011':[(1,'Claude开口保护小鱼','Claude begins her protective shout','压乐让台词突出'),(8,'切入小鱼失守落地','Cut to the child losing balance and falling','落地段重音候选；保留真实落地声')],
 'GB012':[(5,'进入点燃高柴镜头','Begin the kindling ignition shot','燃起段开始推升，随火势发展')],
 'GB013':[(10,'破门前静默开始','Begin the pre-breach stillness','暂时抽掉音乐，保留空间张力'),(12,'切入破门动作','Cut into the door breach','破门段强落点；真实撞击时刻待动态验收')],
 'GB014':[(3,'教主回身，Kimi画外咏唱将起','Cut to the leader turning; Kimi chant follows','切换Kimi专曲；声线跨批延续')],
 'GB014A':[(0,'月光开始流入，尚无人形','Moonlight starts flowing in before any silhouette','沿用上批专曲原位置，不从头重播'),(4,'完成四秒显形，切近景举刃','After four seconds of formation, cut closer to the blade','柔和乐句落点；避让随后咏唱')],
 'GB015':[(5,'循刃瞬移镜头开始','Begin the blade-linked arrival shot','爆发落点候选'),(10,'进入暗月闭合与挡法术镜头','Begin the dark-moon closure shot','第二次展开，接续同一乐句')],
 'GB016':[(3,'骑士入场，恢复主救援配乐','Knights enter; cut out of the dome interior','从Kimi专曲转回救援主题，需乐句剪接')],
 'GB017':[(6,'切到月背两路救援的约定','Cut to the two-route rescue agreement','降低动态，完整听清分工')],
 'GB018':[(6,'进入展翼离地镜头','Begin the wing-spread and lift-off shot','开始推升；10.2秒咏唱进入后让出频段')],
 'GB019':[(1,'切到千问开扇','Cut to Qwen opening the fan','器械声落点；咏唱连续，不另开一拍'),(5,'进入半空截击镜头','Begin the midair interception shot','短促动作重音候选')],
 'GB020':[(11.5,'切入水龙俯冲镜头','Cut to the water dragon diving','乐句推进，不提前播放破顶撞击重音')],
 'GB021':[(0,'水龙破顶掠过镜头','Water dragon breaches the roof past the camera','强落点目标，衔接前批俯冲')],
 'GB022':[(5,'结印镜中咏唱暂停','Pause the incantation during the seal shot','5–5.8秒收声留白，保留水流'),(8,'解印，开始前指','Release the seal and begin pointing','攻击启动落点'),(9.5,'切低机位撞盾镜头','Cut to the low-angle shield collision shot','撞击高潮段；不可把切镜当成已完成碰撞')],
 'GB023':[(3,'进入浅水空殿余波','Cut to the shallow-water aftermath','重音后退潮，拉开动态')],
 'GB024':[(4.2,'GPT冷淡回应','GPT delivers the curt reply','压乐让短句突出'),(6,'开始白紫水龙显形','Begin the white-violet dragon transformation','变身新起势，不覆盖前一句')],
 'GB025':[(5,'进入省略激战的天空镜头','Begin the sky battle ellipsis','保留远处冲击；不逐次闪光机械卡拍'),(9,'切到雨滴落入殿内','Cut to rain falling inside','音乐回落，雨滴前景')],
 'GB026':[(6,'切到GPT垂眼，胜负已分','Cut to GPT looking down after the victory','收束战斗乐句，为钥匙声留空间')],
 'GB027':[(3,'开始用钥匙解踝链','Begin unlocking the ankle chain','低动态或留白，锁扣声成为落点')],
 'GB028':[(3,'Claude开始微光咏唱','Claude begins the faint-light incantation','柔和抬起'),(7,'切到父亲即将打断','Cut to the impending interruption by her father','压乐或停乐，让7.3秒呼唤进入')],
 'GB029':[(0,'Claude仍选择继续咏唱','Claude chooses to continue the incantation','从上一批留白后重新抬起；不当新歌开头')],
 'GB030':[(5,'切到火种触木燃起镜头','Cut to the spark igniting the wood','动作重音候选'),(8,'Claude收手后脱力','Claude weakens after withdrawing her hand','音乐回落，接抱动作和呼吸前景')],
 'GB031':[(9,'切到数日后街市','Cut to the market days later','切入结尾主题，完成场景转换')],
 'GB032':[(4,'切到这次接住勺子的手','Cut to the hand accepting the spoon','轻落点回应片头，避免夸张撞击声')],
 'GB033':[(5,'结束配乐，只留街市和呼吸','Music ends in post; keep market ambience and breathing','最后四秒明确无BGM；此前淡出区间待混音')],
}

def main():
    if OUT.exists():raise SystemExit('Version already exists; edit source records in place.')
    OUT.mkdir()
    plan=load(OLD/'批次计划.json')
    for name in ('人物核对.json','声音核对.json','动态审查.json'):
        shutil.copy2(OLD/name,OUT/name)
    for key in ('cast_review','sound_review','output'):
        plan[key]=plan[key].replace('生成板-v006','生成板-v007')
    plan['direction_reviews']=[s.replace('生成板-v006','生成板-v007') for s in plan['direction_reviews']]
    plan['version']='v007'
    plan['navigation']['review']='视频制作/生成板-v007/声音执行说明.md'
    sourcehash=hashlib.sha256((ROOT/plan['source']).read_bytes()).hexdigest()
    board=load(OLD/'展开数据.json')
    originals={c['text'] for b in board['batches'] for c in b['dialogue']}
    assert originals==set(TRANSLATIONS)
    save(OUT/'日语译配草案.json',dict(source_sha256=sourcehash,language='Japanese',status='draft_pending_author_review',
      note='执行层日语候选，不覆盖中文剧本。专名读法和咏唱命名待审。现有对白窗口源于中文预演，不是日语实测；紧凑台词需生成时复核，禁止吞字赶速。',
      pronunciation_drafts={'Claude':'クロード','千问':'千問（センモン）','混元':'混元（コンゲン）','乌烬木':'黒燼の薪（こくじんのまき）','沧海天倾':'蒼海天傾（そうかいてんけい）','星火':'星火（せいか）'},
      timing_reviews={'GB004': ['语速重点：求救长句窗口约4.51秒；先保完整语义，不能为卡点吞字。'], 'GB011': ['语速重点：保护呼喊仅1.44秒、向父亲求情仅2秒；日语情绪与停顿尚未实测。'], 'GB014A': ['语速重点：首句咏唱窗口2秒、次句3.3秒；先保完整咏唱，不为卡点强压语速。'], 'GB020': ['语速重点：本批连续咏唱密集，需要验证换气与跨切镜连续性。'], 'GB024': ['语速重点：条约台词窗口约2.52秒；日语发音长度尚未实测。']},quoted_fragments={'一人一根':'一人一本','过来':'来なさい。'},translations=TRANSLATIONS,continuous_line_parts={'CY024A9':'幾千もの','CY024A10':'深き流れを','CY024A11':'統べる、','CY024A12':'水の','CY024A1':'精霊よ、'}))
    rhythm={}
    assert set(TARGETS)=={b['id'] for b in board['batches']}
    for b in board['batches']:
        rhythm[b['id']]={'status':'action_targets_music_alignment_pending','note':'沿用现有动作与镜序；只强调叙事落点，不把全部切镜机械卡在鼓点上。','points':[dict(time=t,action_zh=zh,action_en=en,music_intent=intent,source_seconds=None) for t,zh,en,intent in TARGETS[b['id']]]}
    save(OUT/'配乐卡点方案.json',dict(source_sha256=sourcehash,status='action_targets_music_alignment_pending',
        music_adoption=load(ROOT/plan['source'])['music_adoption'],
        method='从已审阅镜头的动作、切镜、对白留白派生目标，不是音频节拍检测。原曲in/out尚未确定，所有source_seconds为null。需以实际原曲听审、确定乐句后锁定；不得标成已完成音乐对齐。',batches=rhythm))
    plan['audio_execution']={
        'dialogue_language':'Japanese','dialogue_upload':False,'bgm_upload':False,'generated_dialogue':True,'generated_bgm':False,
        'localization':'视频制作/生成板-v007/日语译配草案.json','rhythm':'视频制作/生成板-v007/配乐卡点方案.json',
        'display_note':'本轮只上传图片：不上传配音、不上传BGM。模型直接按日语台词生成声音和对应表演；后期可换成自有角色声音。BGM提前规划动作卡点，最终在剪辑中铺设。',
        'prompt_zh':'所有可辨台词只说上述日语，不读中文原意。自行生成自然对白及对应口型，无配音参考；不新增台词。只生成对白和环境动作音，不生成BGM。',
        'prompt_en':'Japanese speech with lip sync; no audio reference, extra speech or music.',
        'replacement_note':'后期以生成对白为表演节奏参考，保留句长、重音和停顿；先替换音色再检查口型。模型成片可能把对白和音效混在一起，删除原音轨会同时删掉音效，应保留原片并按需要分离或重建环境/动作声。',
    }
    plan['sound_policy']='日语台词按指定窗口只说一次，画外声不得由在画人物代说；跨镜咏唱保持连续。不上传配音参考。视频模型生成对白与口型，后期按实际表演换声。BGM只用于规划动作时间，最终后期铺设。'
    plan['global_gaps']=[v for v in plan['global_gaps'] if not v.startswith('正式声线')]
    plan['global_gaps']+=['日语译配为执行草案，中文剧本保留；专名读法、语速和口型尚待审阅与实际验证。','全部音乐卡点当前为动作目标，尚未完成原曲乐句听审和in/out锁定；生成前须完成音乐对齐。']
    plan['mix_notes']+=[plan['audio_execution']['replacement_note'],'跨批按成片时码接续音乐，剪除的74.5秒生成余量不进入配乐时间；不按15秒重新起乐。']
    save(OUT/'批次计划.json',plan)

if __name__=='__main__':main()
