"""Freeze a portable Japanese dubbing handoff from the current board, without inference."""
import collections, csv, hashlib, json, shutil, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'后期/日语配音交接-v001'
def load(p):return json.loads(p.read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def japanese_notes(notes,shot):
 result=[]
 for n in notes:
  if "shouldn't" in n:n='表达“不该插手”的自我约束，不写成没有能力或绝对无法救人。'
  elif 'out of here' in n:n='Claude问句约1.6秒、小鱼承诺句约1.9秒；日语需试配自然接话，要清楚表达小鱼主动带她离开。'
  elif "I'll get you out" in n:n='“我带你出去”是小鱼的主动保证，不改成请求对方跟随。'
  elif 'Moonshadow Crossing' in n:n='“月影渡”术名窗口约1.2秒；须试配日语读法，不能为赶速破坏落点。'
  elif 'H3分段' in n:n=('一整句跨五镜连续咏唱，切镜不重起声线。' if shot=='CY024A9' else '接上句连续咏唱，切镜不重起声线。')
  elif '紧凑英文' in n:n='云岸／长风与开天／倒海的意象保留；需日语实测，避免为卡时让咏唱变成报幕。'
  elif 'non-interference' in n:n='“互不干涉条约”指控整句约2.52秒；需日语试配，不能吞掉条约含义。'
  elif 'answer my call' in n:n='前两段合成一个呼唤微光的句子，父亲插话处停声；随后从“回应我的呼唤”续咏，不把它当成回答父亲。'
  elif 'Yes.' in n:n='末尾“好”原窗口0.7秒；轻声明确答应，不延长成新的感谢台词。'
  result.append(n)
 return result
def main():
 assert not OUT.exists(),'Preserve frozen handoff; use a new version'
 OUT.mkdir(parents=True); (OUT/'声音参考').mkdir()
 board=load(ROOT/'视频制作/生成板-v010/展开数据.json')
 ja=load(ROOT/'视频制作/生成板-v009/日语译配.json')
 shots=load(ROOT/board['source']); sm={s['id']:s for s in shots['shots']}
 assert sha(ROOT/board['source'])==board['source_sha256']==ja['source_sha256']
 roles={'DeepSeek':('小鱼','柔软圆润、灵动、有表情的日本动漫少女；善良，遇事有小倔劲。v006音色已由作者暂定，v007四种情绪得到“可以”的反馈；英语样本用于身份参考，日语迁移仍需听审。'),
 'Claude':('Claude','温柔、细腻、有疲惫感但不软弱；保护小鱼时有坚定锋芒。新声线未定，先各试清透温柔、温润坚定两个方向。'),
 'ChatGPT':('GPT','饱满柔和的龙娘女王；平日慵懒，看似不想理会，真正救人时可靠、有王者气息。先各试慵懒宠溺、从容威严两个方向；不要用发怒代替威严。'),
 'Kimi':('Kimi','清冷但有少女感；轻盈、专注，咏唱清晰；不要成熟得失去少女气质。'),
 '千问':('千问','中国古典美人的温婉、端雅和从容；日语自然表达，不要求模仿中文口音。'),
 'Gemini':('Gemini','活泼可爱的猫猫／电竞少女，反应快、有精神；不要给正式台词擅加喵声或口头禅。'),
 'Grok':('Grok','粗豪、强势、有点蛮横，爽快果断；保留本片AI娘身份。作者提到的马斯克仅为性格联想，不要求克隆真人声音。'),
 '教主':('教主／Claude的父亲','反派坏博士气质，带控制欲和仪式感；平静而残酷，失势后虚弱仍想发号施令。'),
 '教徒':('教徒','麻木、迷狂、空洞的追随者气质；本片两句具体仍按冷淡传令和简短命令表演。不要靠全程吼叫或含糊发音表现。')}
 slugs={'DeepSeek':'Xiaoyu','Claude':'Claude','ChatGPT':'GPT','Kimi':'Kimi','千问':'Qwen','Gemini':'Gemini','Grok':'Grok','教主':'CultLeader','教徒':'Cultist'}
 cues=[]; per_shot=collections.Counter()
 for b in board['batches']:
  for c in b['dialogue']:
   role=c['speaker'].split('（')[0]; assert role in roles
   v=c['review']; zh=c['source_text']; assert zh in ja['translations']
   per_shot[c['shot_id']]+=1; ident=f"VO-{c['shot_id']}-{per_shot[c['shot_id']]:02}"
   cues.append(dict(id=ident,role=role,display_name=roles[role][0],shot_id=c['shot_id'],batch_id=b['id'],scene=sm[c['shot_id']]['scene_title'],shot_title=sm[c['shot_id']]['title'],
    source_zh=zh,japanese_draft=ja['translations'][zh],japanese_status=('作者此前确认该句译意与措辞，仍需日语表演适配' if zh in ['教会的事，我不该插手。','我带你出去。'] else '历史日语草案，需语言与表演复核'),
    listener=v['listener'],intention=v['intention'],delivery=v['delivery'],film_start=v['film_start'],film_end=v['film_end'],duration=v['duration'],batch_start=c['start'],batch_end=c['end'],mode=c['mode'],notes=japanese_notes(v['notes'],c['shot_id']),
    filename=f'{ident}__{slugs[role]}__ja__v001.wav'))
 assert len(cues)==61 and len(set(c['source_zh'] for c in cues))==60
 refs=[]
 ref=load(ROOT/'资产/生成记录/小鱼英语声线-v006/manifest.json')
 emotions=load(ROOT/'资产/生成记录/小鱼英语情绪-v007/manifest.json')
 for name,c in [('Xiaoyu-v006-identity',ref)]+[(f'Xiaoyu-v007-{c["id"]}',c) for c in emotions['candidates']]:
  source=ROOT/c['path']; assert sha(source)==c['sha256']; dest=OUT/'声音参考'/f'{name}.flac';shutil.copy2(source,dest)
  refs.append(dict(file=dest.relative_to(OUT).as_posix(),sha256=sha(dest),source_project_path=c['path'],text=ref['text'],transcript_status='原生成请求文字；可据实际音频核对，不冒称ASR逐字验收',language='English',sample_rate=c['sample_rate'],seconds=c['seconds'],purpose='声音身份基准' if 'identity' in name else '情绪表现参考'))
 counts=collections.Counter(c['role'] for c in cues)
 text=['# 《白米饭》日语配音需求清单\n','版本：交接v001｜2026-10-26｜61条对白、60种中文原句、9个有词角色。全片预演435.5秒。\n',
 '## 给执行 agent 的任务\n',
 '请为哥特式异世界动画短片《白米饭》制作日语角色配音。中文是剧情与语义依据，下方日语是已有草案，需先复核为自然的动漫对白。保持每个角色独立、稳定的声音身份。不要改剧情、增删台词或另配旁白。此包只交接声音制作，不需要生成图片、视频、BGM或音效。\n',
 '故事梗概：小鱼向受押送的Claude递饭，得知她当晚要被火祭；向慵懒的龙娘女王GPT求救被拒后，独自去救。Claude反过来保护小鱼，GPT最终召集伙伴出手。救援后Claude用微弱星火回应父亲，随后离开，片尾再次递饭。请保留善意、保护与慵懒外表下的可靠之间的反差。\n',
 '## 执行顺序与范围\n',
 '- [ ] 先核对61条中文与日语，回交日语最终稿及改译理由；保留稳定台词ID。特别保留“不该插手”的自我约束、“我带你出去”的主动保证，不把神明擅改为多神设定。\n',
 '- [ ] 小鱼先用附带身份参考试日语，确认柔软圆润和动漫角色感能迁移。她的英语v006音色已暂定，但不能直接声称日语克隆同样稳定。模型不支持跨语言参考时，说明限制并按声音目标做候选。\n',
 '- [ ] Claude和GPT各先交两个日语声线候选，使用下方正式台词选句；其他角色先短试音。作者选定后固定音色ID／参考音，再完成全片。不把候选直接当采用。\n',
 '- [ ] 逐条录制／合成，三段咏唱按连续表演处理；交干声与可追溯记录。工具和模型由接收agent按实际能力核实，不要求使用Breeze，也不宣称本包提供了新模型调用权限。\n',
 '- [ ] 本地Claude/GPT英语v008仅准备了四请求，作者中止后未提交；不要继续运行它。现有生成板v010仍是英语历史执行版，本包是新的日语配音交接快照，不代表板内提示词已经切换日语。回收配音后由本项目统一同步。\n',
 '## 角色音色\n','共通方向：主要AI娘角色可用 “Japanese anime voice actress” 指导风格；本轮朗读日语。角色声音要有动漫表演的辨识度，避免回到欧美真人儿童演员感。角色之间保持区别，不用小鱼参考去克隆所有人。教主与教徒按各自反派角色处理。\n']
 for role,(name,desc) in roles.items():text.append(f'- **{name}：{counts[role]}条**。{desc}\n')
 text+=['\n混元、Llama只在GPT召集台词中被叫到，当前没有独立对白，不新增台词或试音任务。\n',
 '## 台词与时间规则\n',
 '- 清单时间单位均为秒。全片时间从正片起点算，批内时间只用于定位原生成板；15秒是视频生成批次，不是配音文件长度。窗口来自预演预算，尚未用日语实测。\n',
 '- 尽量自然落入窗口；若放不下，报告实际时长与建议，不吞字、机械加速、删语义，也不要拉长尾音凑时长。文件开头结尾保留少量剪辑余量并记录实际发声起止。\n',
 '- 一条台词只说一次。“画外／嘴部未入画”不改变说话者；其他角色不得代说。表演标注、角色名、ID、括号说明不能被读进音频。\n',
 '- 小鱼开头与片尾同一句分别交付，情境不同，不去重。短回应、呼名、术名也必须交付。群演不额外说清晰可辨的词。\n',
 '## 连续咏唱和关键停顿\n',
 '- Kimi：从“隐于月背的暗影啊”到“月影渡”是同一咏唱，跨镜保留同一声线与句势。月光慢慢显形的4秒视觉留白保留，不能用额外台词填满；术名落点按清单窗口。\n',
 '- GPT：从“盘踞于苍穹尽头”到“沧海天倾”是一段完整咏唱。“统御万千深流的水之灵啊”横跨CY024A9、CY024A10、CY024A11、CY024A12、CY024A1，清单只列一条9秒窗口；不能按五个画面各读一次。先交连续母版，再按台词ID给切分与对应母版区间。术名前有意停顿，最后完整清晰落名。\n',
 '- Claude：“沉睡于灰烬中”与“的微光啊”跨镜连成一句。366.5秒句尾后停声6秒，父亲“Claude……过来”与她反应发生其中；372.5秒从“回应我的呼唤”接着咏唱，不从开头重念。剩余全文连续至“星火”，虚弱但意志越来越坚定。交含停顿的连续母版和逐句区间，父亲单独一轨，不混进她的干声。\n',
 '- GPT说“不该插手”是自我约束；“聒噪”平静冷淡。Claude“别碰她”是保护小鱼的愤怒；“父亲……放她走”保留称呼后的痛苦停顿。\n',
 '## 名称与术名读法待复核\n',
 '以下来自历史日语草案，不是全部已锁定：'+ '；'.join(f'{k} → {v}' for k,v in ja['pronunciation_drafts'].items())+'。其他已有写法：Gemini＝ジェミニ，Grok＝グロック，Kimi＝キミ，Llama＝ラマ，月影渡＝月影渡り。请统一确认自然读法，并在回交表写假名；不得默默每条换读音。\n',
 '## 交回文件\n',
 '- 每条按清单指定文件名交独立干声WAV，优先PCM 24-bit、单声道；保留模型原生采样率，写明数值，不把升采样当新增质量。有必要做统一48kHz剪辑副本时，同时保留原生母版。\n',
 '- 不混BGM、环境音、音效或空间混响；不硬限幅，不变调掩盖音色差异。咏唱另附3个连续母版及每条在母版中的区间；不能逐句切断尾音或呼吸。\n',
 '- 填写同包《台词与回交表.csv》中的日语最终稿、假名读法、音色ID／参考、实际时长、发声起止、母版文件与区间、模型与参数、状态、异常说明。候选编号和采用状态分清；缺项明确写缺失，不补造。\n',
 '- 附简洁试听索引，按角色和剧情顺序可定位；技术可播放、字词核验、主观音色听审分别报告。不要把成功生成等同于作者验收。\n',
 '## 逐条配音清单\n']
 for i,c in enumerate(cues,1):
  text.append(f"\n### {i:02d} · {c['display_name']} · {c['id']}\n\n- [ ] 文件：`{c['filename']}`\n- 场景：{c['scene']}／{c['shot_title']}；对{c['listener']}说。镜号{c['shot_id']}，批次{c['batch_id']}。\n- 中文：{c['source_zh']}\n- 日语草案：{c['japanese_draft']}（{c['japanese_status']}）\n- 表演：{c['delivery']}；意图：{c['intention']}。\n- 全片窗口：{c['film_start']:.3f}–{c['film_end']:.3f}秒，预算{c['duration']:.3f}秒；批内{c['batch_start']:.3f}–{c['batch_end']:.3f}秒。\n- 声画方式：{c['mode']}。\n")
 text+=['\n## 声音参考与溯源\n','`声音参考/`内5个FLAC均为未处理原件：小鱼v006身份基准、v007开心／委屈／倔强／认真。英文逐字稿来自原请求：`Would you like some? One more try. I\'ll get you out of here.` 请据音频再次核对，不能把英文参考词混进日语输出。完整哈希与来源在《交接数据.json》。\n','中文与时间来自当前v010展开数据／v0.56镜头计划；日语来自v009历史译配。61条已逐一映射，未按60种原句去重。\n']
 (OUT/'日语配音需求清单.md').write_text(''.join(text),encoding='utf-8')
 fields=['台词ID','角色','镜号','批次','场景','中文原意','日语草案','草案状态','听话对象','表演语气','意图','全片开始秒','全片结束秒','预算秒','输出文件名','日语最终稿','假名读法','音色ID或参考','实际文件时长秒','实际发声开始秒','实际发声结束秒','连续母版文件及区间','模型与参数','交付状态','异常说明']
 with (OUT/'台词与回交表.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(fields)
  for c in cues:w.writerow([c['id'],c['display_name'],c['shot_id'],c['batch_id'],c['scene'],c['source_zh'],c['japanese_draft'],c['japanese_status'],c['listener'],c['delivery'],c['intention'],c['film_start'],c['film_end'],c['duration'],c['filename']]+['']*10)
 save(OUT/'交接数据.json',dict(version='v001',date='2026-10-26',purpose='日语配音交接快照，非已完成配音',source_files={p:sha(ROOT/p) for p in ['视频制作/生成板-v010/展开数据.json','视频制作/生成板-v009/日语译配.json',board['source']]},count=len(cues),role_counts=dict(counts),cues=cues,references=refs))
 pack=OUT.parent/'白米饭-日语配音交接-v001.zip'
 assert not pack.exists()
 with zipfile.ZipFile(pack,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(OUT.rglob('*')):
   if p.is_file():z.write(p,Path(OUT.name)/p.relative_to(OUT))
 print(json.dumps({'cues':len(cues),'roles':dict(counts),'files':len(list(OUT.rglob('*')))-1,'zip':str(pack),'bytes':pack.stat().st_size},ensure_ascii=False))
if __name__=='__main__':main()
