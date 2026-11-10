"""Freeze author-selected voices and inventory usable speech without synthesis."""
from pathlib import Path
import json, hashlib, shutil, re, html, datetime, subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '声音/正式配音准备-v006'
OUT.mkdir(exist_ok=True)
for name in ['已选原件', '可直接沿用', '补录正文']:
    (OUT/name).mkdir(exist_ok=True)

def read(p): return json.loads(p.read_text(encoding='utf8'))
def write(p, data): p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def freeze(src, dst):
    assert src.is_file(), src
    if dst.exists(): assert sha(src) == sha(dst), f'Immutable output differs: {dst}'
    else: shutil.copy2(src, dst)
    return {'file': dst.relative_to(ROOT).as_posix(), 'source': src.relative_to(ROOT).as_posix(), 'sha256': sha(dst)}

review = ROOT/'声音/声线返修试听-v004'
choices = read(review/'作者选择.json')
assert choices['GPT']['candidate'] == 1 and choices['Kimi']['candidate'] == 1 and choices['千问']['candidate'] == 3
assert all(v['status'] in ('author_selected', 'retain_existing_voice') for v in choices.values())
freeze(review/'作者选择.json', OUT/'作者选择快照.json')
data = read(ROOT/'声音/选声整理-v004/按角色台词与表演.json')
current = read(ROOT/'剧本/白米饭-日语对白-v0.69.json')
source_lines = {x['id']: x for x in current['lines'] if x.get('ja') and x.get('status') not in ['merged_not_spoken','removed_not_spoken','removed_from_draft']}
lines = data['lines']
assert len(lines) == len(source_lines) == 54
assert all(x['ja'] == source_lines[x['id']]['ja'] and x['zh_back_translation'] == source_lines[x['id']]['zh_back_translation'] for x in lines)
old_voice = {x['id']: x for x in read(ROOT/'后期/局部收口-v008/后期执行计划.json')['voice']}
entries = {x['role']: x for x in read(review/'试听数据.json')}
voices = {}
texts = {}
for role, entry in entries.items():
    if role == '小鱼':
        voices[role] = {'status':'approved_existing_voice', 'source':'v008逐句既有录音', 'note':'保留现有声音；改词句仍须补录'}
        continue
    n = choices[role].get('candidate', 1)
    chosen = next(x for x in entry['previews'] if x['candidate'] == n)
    src = (review/chosen['file']).resolve()
    voices[role] = freeze(src, OUT/'已选原件'/(role+src.suffix))
    voices[role].update(candidate=n, status='author_voice_approved', timeline_adopted=False)
    if role in ['GPT','Kimi']:
        texts[role] = read(review/(role+'-输入.json'))['text']
    elif role == 'Claude':
        texts[role] = (ROOT/'声音/ElevenLabs-正式台词试听-v002/Claude-实际送读.txt').read_text(encoding='utf8')
    elif role == '教主':
        texts[role] = read(ROOT/'声音/ElevenLabs-正式台词试听-v003/教主-输入.json')['text']
    elif role in ['Gemini','教徒']:
        r = read(ROOT/('声音/ElevenLabs-正式台词试听-v003/'+role+'-直配结果.json'))
        preview = next(p for p in r['previews'] if p['file'] == src.name)
        texts[role] = '\n'.join(x['text'] for x in preview['history']['dialogue'])
    elif role == '千问': texts[role] = '行きましょう。つかまって。'
    elif role == 'Grok': texts[role] = 'もちろん。'
voices['GPT']['applies_to_roles'] = ['GPT','天使GPT','恶魔GPT']
voices['Kimi']['selection_evidence'] = '作者本轮明确回复：Kimi 候选 1；助手按该指示保存页面。'
voices['千问']['note_resolution'] = '旧备注要求Eleven重设计保留为历史；后续明确改用Breeze→IndexTTS，并采用候选3。无需再设计。'
voices['千问']['identity_reference'] = freeze(ROOT/'声音/千问跨语言试音-v005/千问-Breeze-中文原声.flac',OUT/'已选原件/千问-中文设计参考.flac')

def norm(text, hints):
    text = re.sub(r'\[[^\]]+\]', '', text)
    for a,b in sorted(hints.items(), key=lambda kv:-len(kv[0])): text=text.replace(a,b)
    return re.sub(r'[\s。、！？!?…―—「」『』,\.]','', text)

counts = {}
for x in lines:
    role=x['voice_role']; hints=x.get('reading_hints',{})
    x.pop('voice_decision', None)
    x['voice_asset']=role
    x['timeline_adopted']=False
    x['performance_acceptance']='逐句表演与准确性待验收；作者已确认声线'
    src=None
    if role=='小鱼':
        old=old_voice.get(x['id'])
        if old and norm(old['ja'], hints)==norm(x['ja'],hints):
            src=Path(old['path']); x['audio_state']='exact_existing_line'
        else: x['audio_state']='needs_recording'
    elif norm(x['ja'],hints) in norm(texts[role],hints):
        x['audio_state']='selected_master_contains_text'
        x['master']=voices[role]['file']
        x['coverage_evidence']='匹配实际送读/服务回执文本；尚非逐字听审或精确切分'
        if role in ['Grok','Gemini']:
            src=ROOT/voices[role]['file']; x['audio_state']='exact_existing_line'
    else: x['audio_state']='needs_recording'
    if src:
        x['existing_audio']=freeze(src,OUT/'可直接沿用'/(x['id']+'__'+role+src.suffix))
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(src)]))
        x['audio_seconds']=float(probe['format']['duration'])
    counts[x['audio_state']]=counts.get(x['audio_state'],0)+1

for role in voices:
    todo=[x for x in lines if x['voice_role']==role and x['audio_state']=='needs_recording']
    if todo: (OUT/'补录正文'/(role+'.txt')).write_text('\n'.join(x['tts_reading_text'] for x in todo)+'\n',encoding='utf8')
    (OUT/(role+'-完整日语.txt')).write_text('\n'.join(x['tts_reading_text'] for x in lines if x['voice_role']==role)+'\n',encoding='utf8')

manifest={'created_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),
 'status':'voices_author_approved_production_inventory','script':'剧本/白米饭-日语对白-v0.69.json',
 'script_sha256':sha(ROOT/'剧本/白米饭-日语对白-v0.69.json'),'summary':counts,'voice_assets':voices,'lines':lines,
 'generation_submitted':False,'timeline_modified':False,'notes':['54个活动ID完整保留；旧稿与原录音不覆盖。','母版覆盖是送读文本核对，不等于精确口型和母语发音验收。','Kimi/教主母版有三轮重复，需选一轮再切分，不能三轮全用。','先复用已认可表演；只对缺词和逐句不合格处补录，不全片重配。']}
write(OUT/'正式配音清单.json',manifest)
write(ROOT/'声音/当前声线.json',{'manifest':'声音/正式配音准备-v006/正式配音清单.json','voice_status':'author_approved','roles':list(voices),'timeline_adopted':False})
md=['# 白米饭 · 已定声线与正式配音清单','', '声线已确认：GPT候选1、Kimi候选1、千问候选3；其他角色沿用此前确认结果。天使/恶魔GPT共用本体。','',f'共54句：{counts["exact_existing_line"]}句已有独立录音，{counts["selected_master_contains_text"]}句在已选母版中待切分，{counts["needs_recording"]}句待补录。本轮整理、冻结与复用，未提交新生成或修改正片。','', '## 需要补录','']
for x in lines:
    if x['audio_state']=='needs_recording':md += [f'- {x["id"]} · {x["role"]}：{x["ja"]}（{x["zh_back_translation"]}）']
md += ['', '## 完整台词','']
for x in lines: md += [f'### {x["id"]} · {x["role"]}', '',x['ja'],'',x['zh_back_translation'],'', '表演：'+x['performance_direction_v004'],'','状态：'+x['audio_state'],'']
(OUT/'台词与补录清单.md').write_text('\n'.join(md),encoding='utf8')
labels={'exact_existing_line':'已有逐句文件','selected_master_contains_text':'已选母版覆盖，待切分','needs_recording':'待补录'}
rows=''.join('<tr><td>'+html.escape(x['id'])+'</td><td>'+html.escape(x['role'])+'</td><td>'+html.escape(x['ja'])+'<br><small>'+html.escape(x['zh_back_translation'])+'</small></td><td>'+labels[x['audio_state']]+'</td></tr>' for x in lines)
cards=''.join('<article><h2>'+html.escape(role)+'</h2><p>声线已确认</p>'+('<audio controls preload="none" src="'+html.escape(Path(v['file']).relative_to(OUT.relative_to(ROOT)).as_posix(),quote=True)+'"></audio>' if 'file' in v else '<p>保留逐句既有声音</p>')+'</article>' for role,v in voices.items())
page='<!doctype html><html lang="zh"><meta charset="utf-8"><title>白米饭 · 正式配音准备</title><style>body{max-width:1200px;margin:32px auto;padding:20px;background:#121923;color:#edf4fa;font:16px/1.7 system-ui}a{color:#a9dcff}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}article{background:#243246;padding:18px;border-radius:10px}audio{width:100%}td,th{padding:12px;border-bottom:1px solid #405166;text-align:left}small{color:#aabbcc}</style><h1>白米饭 · 正式配音准备</h1><p>九个角色声线已确认，54句日语及中文回译保持v0.69。旧备注留档，不再覆盖最新选择。</p><p>'+html.escape('；'.join(labels[k]+' '+str(v)+'句' for k,v in counts.items()))+'</p><p>母版覆盖按送读文本核对，尚待切分和逐句听审。此次未新生成、未替换正片。</p><p><a href="台词与补录清单.md">完整台词与补录清单</a></p><div class="grid">'+cards+'</div><table><tr><th>对白ID</th><th>人物</th><th>日语／中文回译</th><th>制作状态</th></tr>'+rows+'</table></html>'
(OUT/'配音清单.html').write_text(page,encoding='utf8')
print(json.dumps({'voices':len(voices),'lines':len(lines),'summary':counts},ensure_ascii=False))
