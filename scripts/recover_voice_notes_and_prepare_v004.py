"""Recover author-entered DOM notes and prepare dialogue; no synthesis."""
from pathlib import Path
import json, datetime, copy
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'声音/ElevenLabs-正式台词试听-v003'
OUT=ROOT/'声音/选声整理-v004'
OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
choices=read(OLD/'作者选择.json')
snapshot=read(OLD/'页面备注恢复-20261029.json')
for item in snapshot['notes']:
    role=item['id'].removeprefix('note-');note=item['value']
    if choices[role].get('note','')==note:continue
    if choices[role].get('note',''):
        raise RuntimeError('Refusing to overwrite a newer saved note: '+role)
    previous=copy.deepcopy(choices[role])
    choices[role].update(note=note,note_evidence='recovered from live review input before reload',note_captured_at=snapshot['captured_at'])
    with (OLD/'选择历史.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps({'role':role,'previous':previous,'new':choices[role],'action':'recover_unsaved_author_note'},ensure_ascii=False)+'\n')
write(OLD/'作者选择.json',choices)
write(OUT/'作者选择与备注快照.json',choices)
directions={
'Claude':'沿用候选1的声线。感谢自然受阻；护小鱼时真正急喊；恳求转为克制；星火咏唱疲惫但意志清楚，不套用GPT的热血爆发。',
'GPT':'声线待重新确认。普通对白保留保护感；咏唱用动漫中的真实行动意图推进，呼唤→聚水→攀升→救人→发令。每级增加力量，避免全程轻柔朗诵，也不从第一句一直吼。',
'Kimi':'重选空灵清冷的少女声。轻而有明确音芯，日语咬字清楚；不是低沉成熟叙述，也不是拖长气声。呼唤古老意志时沉静集中，术名短促利落。',
'教主':'采用候选1声线。以理所当然的仪式权威压迫，命令短硬；不要怪笑或逗小孩；称女儿的表面温和与行动冷酷相冲突。',
'千问':'按作者指定，用本地Breeze设计古风美人声线；端雅从容而有行动力。日语支持与实测待核，不把未验证的本地能力当作可直接交付。',
'Gemini':'采用主结果声线；私も行く。清楚主动地接话，短句不再设计音色。',
'教徒':'采用主结果声线。押送与准备献祭的命令清楚直接，带有制度性的冷漠；不要故作滑稽或向观众解释教义。',
'Grok':'弃用本轮少女化直配，回到此前作者认可的v003原声音；本句日语未改，优先直接沿用原录音。',
'天使GPT':'与GPT本体使用同一最终声线；仅把情绪改为轻而尖锐的自我质问。不可使用独立Shizuka声线，不变幼、不变另一个角色。',
'恶魔GPT':'与GPT本体使用同一最终声线；仅把情绪改为克制、冷静地提醒代价。不可使用独立Konoha声线，不压成另一个人的音色。',
'小鱼':'暂时保留现有声音。新稿与旧录音逐句核词；保留音色不等于旧词可直接沿用。'
}
source=read(ROOT/'剧本/白米饭-日语对白-v0.69.json')
lines=[copy.deepcopy(x) for x in source['lines'] if x.get('ja') and x.get('status') not in ['merged_not_spoken','removed_not_spoken','removed_from_draft']]
assert len(lines)==54 and len({x['id'] for x in lines})==54
overrides={
'VO-CY024A-01':'清き水の主よ。直接向主呼唤，庄重但已有战斗决心；主读ぬし。句尾落稳，随后水开始响应，不拖成长吟。',
'VO-CY024A2-01':'水よ、集え。重心落在集え，短停后催动聚水；力量较呼唤提升一层。',
'VO-CY024A3-01':'雲の上に、海を成せ。前半随水升高，后半推进而非平读，成せ明确有力；不要每个词都额外停顿。',
'VO-CY024A4-01':'炎を鎮め、与下句连成一个救人意图，只留必要换气，不重新归零开始念诗。',
'VO-CY024A5-01':'罪なき者に、救いを――把救人的迫切压进救いを，留一个短蓄力点，立刻接术名；不拖尾消散气势。',
'VO-CY024A5-02':'蒼龍天傾！そうりゅうてんけい。把力量集中到这一声，清晰、短而决绝；发令接解印，释放随后发生。',
'VO-CY024R-01':'空灵清冷的声线，向古老意志作沉静而坚定的呼唤；古き意志よ集中而非软弱。举刃起势同步。',
'VO-CY024K0-01':'同一清冷声线，この刃を標に连贯，短停后道を開け果断；蓄力随句推进，标读しるべ。',
'VO-CY024K1A-01':'明刃钉稳后短促发令つきかげわたり；情绪提升而不改变声音身份，随后瞬移回收。',
'VO-CY026D-02':'醒来、撑起并看向GPT之后，清冷而可靠地答任せて；干净收口，不撒娇、不补说明。',
'VO-CY008M-01':'使用GPT同一声线，克制地提醒自己遵守协定；不额外压低音高、不换声。',
'VO-CY008M-02':'使用GPT同一声线；それで承接提醒，見殺し轻而尖锐地质问自己，不用独立少女声。'
}
records=[]
md=['# 白米饭 · 作者选声整理 v004','', '依据现场输入框补回全部备注。日语正文、中文回译及54个活动ID沿用v0.69；本轮只调整声线归属和表演要求，未生成音频、未替换正片。','', 'GPT、Kimi、千问仍待新声线试听；天使/恶魔GPT随GPT最终声线一起确定。Claude、教主、Gemini、教徒采用声线决定不等于每句表演通过。','']
for role,base in directions.items():
    selected=choices[role]
    group=[x for x in lines if ('教主' if x['role'].startswith('教主') else x['role'])==role]
    md += ['## '+role,'','作者备注：'+(selected.get('note') or '无新增文字备注；按已选结果处理。'),'','执行要求：'+base,'']
    texts=[]
    for line in group:
        line['voice_role']='GPT' if role in ['天使GPT','恶魔GPT'] else role
        line['voice_decision']=copy.deepcopy(selected)
        line['performance_direction_v004']=overrides.get(line['id'],line.get('direction',''))
        if role=='Grok':line['preferred_existing_audio']='后期/日语配音修正-v003/干声/VO-CY026C-02__Grok__ja__v003.wav'
        records.append(line)
        t=line['ja']
        for a,b in line.get('reading_hints',{}).items():t=t.replace(a,b)
        line['tts_reading_text']=t;texts.append(t)
        md += [f'### {line["id"]} · 原第{line.get("previous_batch","?")}批','',line['ja'],'','中文回译：'+line['zh_back_translation'],'','表演：'+line['performance_direction_v004'],'']
    (OUT/(role+'-日语录音正文.txt')).write_text('\n'.join(texts)+'\n',encoding='utf8')
write(OUT/'按角色台词与表演.json',{'source':'剧本/白米饭-日语对白-v0.69.json','status':'prepared_not_generated','voice_directions':directions,'lines':records})
(OUT/'选声与完整台词.md').write_text('\n'.join(md),encoding='utf8')
assert {x['id'] for x in records}=={x['id'] for x in lines}
assert all((ROOT/x['preferred_existing_audio']).is_file() for x in records if 'preferred_existing_audio' in x)
print(json.dumps({'recovered_notes':{x:choices[x]['note'] for x in ['Kimi','天使GPT','恶魔GPT']},'active_lines':len(records),'roles':len(directions),'generated_audio':False},ensure_ascii=False))
