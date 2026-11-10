"""Create the English/Breeze execution edition; preserve source film and Japanese history."""
import copy, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '视频制作/生成板-v010'
OLD = ROOT / '视频制作/生成板-v009'
def load(p): return json.loads(p.read_text('utf-8-sig'))
def write(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

TRANSLATIONS = {
 '你要吃一点吗？': 'Would you like some?',
 '谢谢你。': 'Thank you.',
 '今夜，为 Claude 行火祭。': 'Tonight, Claude goes to the pyre.',
 '让她进来。': 'Let her in.',
 '他们今晚要烧死 Claude。你能救救她吗？': "They'll burn Claude tonight. Can you save her?",
 '教会的事，我不该插手。': "I shouldn't interfere in Church affairs.",
 '可是……她会死的。': "But... she'll die.",
 '那我自己去。': "Then I'll go myself.",
 '取乌烬木，一人一根。': 'Fetch the blackash wood. One log each.',
 '你怎么来了？': 'What are you doing here?',
 '我带你出去。': "I'll get you out of here.",
 '别试了。你快走吧。': 'Stop trying. You need to go.',
 '再试一下。': 'One more try.',
 '快走！': 'Run!',
 '我的女儿，神明在等你。': 'My daughter. The divine awaits you.',
 '让开。': 'Move aside.',
 '别碰她！': "Don't touch her!",
 '父亲……放她走。': 'Father... let her go.',
 '护住她们。': 'Protect them.',
 '隐于月背的暗影啊，': 'O shadows behind the moon,',
 '请循此刃的银辉，': "follow this blade's silver light,",
 '为我开启通往彼端的门扉——': 'and open a passage to the other side—',
 '月影渡！': 'Moonshadow Crossing!',
 '千问，陪我救个人。': 'Qwen. Help me save someone.',
 '走吧。': "Let's go.",
 'Gemini。': 'Gemini.',
 '我去。': "I'm in.",
 'Grok。': 'Grok.',
 '当然。': 'Of course.',
 'Kimi。': 'Kimi.',
 '我走正门。她背后的彩窗，交给你。': "I'll take the front door. You take the stained-glass window behind her.",
 '嗯。': 'Mm.',
 '混元，Llama……都来。': 'Hunyuan, Llama... everyone, come.',
 '抱紧我。': 'Hold on tight.',
 '盘踞于苍穹尽头，': "At the heavens' farthest edge,",
 '统御万千深流的水之灵啊，': 'O spirit of water, ruler of a thousand deep currents,',
 '请将散落尘世的万千水息，': 'gather the scattered waters of this world',
 '汇作悬于群星之下的无岸之海。': 'into a shoreless sea suspended beneath the stars.',
 '以重云为岸，以长风为引，': 'Clouds your shore, winds your guide,',
 '令沉睡的潮汐翻卷，奔涌而来。': 'let sleeping tides rise and surge forth.',
 '此刻，洞开天穹，倒悬沧海；': 'Now, split the sky; upend the sea.',
 '令灼烧无辜的烈焰，在奔流中止息；': 'Quench the flames that burn the innocent;',
 '将阻挡吾行的高墙，淹没于万顷狂澜！': 'drown the walls before me in raging waves!',
 '请降下你的救赎——': 'Let your salvation descend—',
 '沧海天倾！': 'Heavenfall Deluge!',
 '你违反了互不干涉条约。': 'You broke our non-interference pact.',
 '聒噪。': 'Enough.',
 '慢慢来。': 'Easy now.',
 '那个孩子……': 'The little girl...',
 '她没事，在下面等你。': "She's safe. Waiting for you down below.",
 '沉睡于灰烬中': 'Slumbering in the ashes,',
 '的微光啊，': 'O faintest light,',
 'Claude……过来。': 'Claude... come here.',
 '回应我的呼唤。': 'answer my call.',
 '循着尚未散去的余温，': 'Follow the warmth that lingers,',
 '在我掌心，': 'here in my palm,',
 '再燃一次——': 'burn once more—',
 '星火。': 'Ember.',
 '我们走。': "Let's go.",
 '好。': 'Yes.',
}

def main():
 OUT.mkdir(exist_ok=True)
 board=load(OLD/'展开数据.json'); plan=load(OLD/'批次计划.json'); prev=load(OLD/'对白复核.json')
 source={c['source_text'] for b in board['batches'] for c in b['dialogue']}
 assert set(TRANSLATIONS)==source
 timing={
  'GB007':['Claude问句约1.6秒、小鱼承诺句约1.9秒；需试配自然接话，要清楚表达主动带她离开，不吞掉 out of here。'],
  'GB014A':['4秒月光显形留白保持；两段咏唱使用原2秒及3.3秒窗口，需实测长元音与停顿。'],
  'GB015':['术名 Moonshadow Crossing! 原窗口约1.2秒，通常五音节并含复辅音；须试配，不能为赶速破坏落点。'],
  'GB020':['云岸/长风与开天/倒海两句用紧凑英文；仍需实测，避免密集辅音让咏唱变成报幕。'],
  'GB024':['non-interference 含多音节，整句约2.52秒；需实测教主的指控语气，不能吞掉条约含义。'],
  'GB028':['前两段合成一个呼唤微光的句子，父亲插话后停声；下一批继续 answer my call，不把它当成回答父亲。'],
  'GB032':['末尾 Yes. 原窗口0.7秒；轻声明确答应，不延长成新的感谢台词。'],
 }
 loc=dict(source_sha256=board['source_sha256'],language='English',status='draft_pending_author_review',
  note='作者已确认英语与Breeze TTS 2；以下为英文执行译稿，保留中文原意。台词窗口沿用预演预算，未做英文声音或口型实测。术名、专名读法为候选，不能当作作者已选声线。',
  translations=TRANSLATIONS,continuous_line_parts={
   'CY024A9':'O spirit ', 'CY024A10':'of water, ', 'CY024A11':'ruler of ',
   'CY024A12':'a thousand ', 'CY024A1':'deep currents,'},
  quoted_fragments={'一人一根':'One log each.','过来':'Come here.'},timing_reviews=timing,
  pronunciation_drafts={'Claude':'klawd /klɔːd/；单音节', 'Qwen':'千问保留品牌英文名Qwen；候选读法kwen /kwɛn/，需试听确认',
   'Hunyuan':'混元保留Hunyuan，不改成日语汉字音；两个汉语音节，需试听确认',
   'Gemini':'JEM-in-eye /ˈdʒemɪnaɪ/', 'Grok':'grok /ɡrɒk/', 'Kimi':'KEE-mee /ˈkiːmi/',
   'Llama':'LAH-muh /ˈlɑːmə/', '乌烬木':'blackash wood，虚构材料英译候选',
   '月影渡':'Moonshadow Crossing，术名英译候选', '沧海天倾':'Heavenfall Deluge，术名英译候选',
   '星火':'Ember，采用余烬复燃的意象；术名英译候选'})
 write(OUT/'英语译配.json',loc)
 audit={k:copy.deepcopy(prev[k]) for k in ('source','source_sha256','counts','batches','batch_notes')}
 audit.update(version='v010',date='2026-10-26',reviewer='/root/review_english_v010',status='text_reviewed_voice_pending',
  board_source='视频制作/生成板-v009/展开数据.json',board_sha256=sha(OLD/'展开数据.json'),
  parent_review='视频制作/生成板-v009/对白复核.json',localization_sha256=sha(OUT/'英语译配.json'),
  review_scope='英语译义、角色意图、跨镜咏唱及时间预算；不代表已合成或听审。',
  summary='61条对白已独立完成英文文字审查：保留主动保证、自我约束、三段咏唱接续与首尾呼应。语种和Breeze TTS 2已确认；译稿措辞待作者审阅，专名、声音和口型未实测。',
  review_fixes=['神明译为the divine，避免擅加多神设定。','Moonshadow Crossing的预算说明修正为通常五音节。','召集同伴补回come，恢复召来动作。','聚水咏唱补回suspended，恢复悬空之海意象。'],
  migration='full_language_change',cues=[],issues=[])
 for old in prev['cues']:
  c={k:copy.deepcopy(v) for k,v in old.items() if k not in ('current_ja','notes','issue_ids')}
  c.update(current_text=TRANSLATIONS[c['source_text']],language='English',notes=[],issue_ids=[])
  if c['offscreen']:c['notes'].append('画外/嘴部未入画只说明声画方式；说话者仍是所列角色，画内角色不要代说。')
  timing_applies=not ((c['batch_id']=='GB024' and c['speaker']!='教主') or (c['batch_id']=='GB028' and c['speaker']!='Claude') or (c['batch_id']=='GB032' and c['source_text']!='好。'))
  if c['batch_id'] in timing and timing_applies:c['notes'].extend(timing[c['batch_id']])
  if c['source_text']=='教会的事，我不该插手。':c['notes'].append("shouldn't 表达自我约束，不写成没有能力或绝对无法救人。")
  if c['source_text']=='我带你出去。':c['notes'].append("I'll get you out 是小鱼的主动保证，不改成请求对方跟随。")
  if c['batch_id']=='GB019':c['notes'].append('一整句跨五镜连续咏唱，切镜不重起声线；H3分段拼合必须与整句一致。')
  if c['batch_id']=='GB029':c['notes'].append('继续对微光咏唱，不回答父亲；停顿保留，不新增台词填满时段。')
  audit['cues'].append(c)
 write(OUT/'对白复核.json',audit)
 plan.update(version='v010',output='视频制作/生成板-v010',dialogue_review='视频制作/生成板-v010/对白复核.json')
 plan['navigation']['review']='视频制作/生成板-v010/英语配音执行说明.md'
 plan['sound_policy']='英语台词按指定窗口只说一次，画外声不得由在画人物代说；跨镜咏唱保持连续。不上传配音参考。视频模型生成对白与口型，后期用Breeze TTS 2按实际表演制作替换声音。BGM只用于规划动作时间，最终后期铺设。'
 ex=plan['audio_execution']
 ex.update(dialogue_language='English',localization='视频制作/生成板-v010/英语译配.json',post_voice_engine='Breeze TTS 2',
  display_note='全片讲英语，后期角色配音使用Breeze TTS 2。本轮生成仅上传图片：不上传配音、不上传BGM。视频模型按英文台词生成声音与口型；BGM按已规划动作点在后期铺设。',
  prompt_zh='所有可辨台词只说上述英语，不读中文原意。自行生成自然对白及对应口型，无配音参考；不新增台词。只生成对白和环境动作音，不生成BGM。',
  prompt_en='English speech with lip sync; no audio reference, extra speech or music.',
  replacement_note='后期用Breeze TTS 2合成相同英文台词，按视频实际句长、重音和停顿指导并检查口型；它不是自动换声或自动口型对齐器。角色声线先试配确认，实际参考音频及逐字稿届时确定。保留原片；删除混合音轨时需分离或补回环境与动作声。')
 plan['global_gaps']=[v.replace('日语译配为执行草案','英语译配为执行草案') for v in plan['global_gaps']]
 write(OUT/'批次计划.json',plan)
 print('Created English edition: 60 translations, 61 cues, 34 batches. No media generated.')

if __name__=='__main__':main()
