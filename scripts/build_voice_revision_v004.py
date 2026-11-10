from pathlib import Path
import json,html,shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'声音/声线返修试听-v004'
OLD=ROOT/'声音/ElevenLabs-正式台词试听-v003'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
entries=[]
notes=read(OLD/'作者选择.json')
for role in ['GPT','Kimi']:
 r=read(OUT/(role+'-结果.json'))
 entries.append({'role':role,'kind':'designed','note':notes[role]['note'],'description':'新候选；'+('包含本体咏唱、安抚、恶魔提醒、天使质问。最后两句必须仍像GPT本人。' if role=='GPT' else '同一组四句正式台词重复三轮，只调整声线目标。'),'previews':[{'candidate':x['candidate'],'file':x['file'],'seconds':float(x['media']['format']['duration'])} for x in r['previews']]})
q=[]
for i,p in enumerate(sorted(OUT.glob('千问-IndexTTS25-*.json')),1):
 r=read(p);q.append({'candidate':i,'file':r['file'],'seconds':r['seconds'],'label':p.stem})
cross=ROOT/'声音/千问跨语言试音-v005/IndexTTS-日语结果.json'
if cross.exists():
 r=read(cross);a=r['audios'][1]
 q.append({'candidate':3,'file':'../千问跨语言试音-v005/'+a['file'],'seconds':float(a['probe']['format']['duration']),'label':'新方案：Breeze中文设计 → IndexTTS日语'})
entries.append({'role':'千问','kind':'direct','note':notes['千问']['note'],'description':'最新决定：先用Breeze设计中文古风美人，再由IndexTTS克隆成日语。候选3是本轮新方案，候选1/2保留作旧参考对照。' if cross.exists() else '作者追加改用IndexTTS。这里先验证旧参考声线说日语；未声称已完成古风声线设计。','previews':q})
grok=ROOT/'后期/日语配音修正-v003/干声/VO-CY026C-02__Grok__ja__v003.wav'
shutil.copy2(grok,OUT/'Grok-恢复旧版.wav')
entries.append({'role':'Grok','kind':'retained','note':notes['Grok']['note'],'description':'依作者意见恢复旧版；正片本轮未动。','previews':[{'candidate':1,'file':'Grok-恢复旧版.wav','label':'原选声音'}]})
for role in ['Claude','教主','Gemini','教徒']:
 path='../ElevenLabs-正式台词试听-v003/'+notes[role]['audio']
 entries.append({'role':role,'kind':'retained','note':'已确认声线，保留。','description':'此次不重复生成。','previews':[{'candidate':1,'file':path,'label':'已选声音'}]})
entries.append({'role':'小鱼','kind':'retained','note':'暂时保留现有声音。','description':'未重新生成。','previews':[]})
write(OUT/'试听数据.json',entries)
if not (OUT/'作者选择.json').exists():write(OUT/'作者选择.json',{e['role']:{'status':'retain_existing_voice' if e['kind']=='retained' else 'pending','note':'','prior_author_note':e['note']} for e in entries})
cards=[]
for e in entries:
 role=e['role'];items=[]
 for p in e['previews']:
  f=html.escape(p['file'],quote=True);idx=p['candidate']
  items.append(f'<article><h3>{html.escape(p.get("label","候选 "+str(idx)))}</h3><audio controls preload="metadata" src="{f}"></audio><p><a href="{f}" download>下载原件</a></p>'+('' if e['kind']=='retained' else f'<button onclick="saveChoice(\'{role}\',{idx})">选这版</button>')+'</article>')
 baseline=''
 if role=='千问' and cross.exists():baseline='<h3>新方案的中文声线原件</h3><audio controls preload="metadata" src="../千问跨语言试音-v005/千问-Breeze-中文原声.flac"></audio><p>中文试音附加语句只用于建立参考，不进入剧情。日语正式文本：行きましょう。つかまって。／走吧。抱紧我。</p>'
 if role in ['GPT','Kimi']:baseline=f'<details><summary>对照上一轮候选1</summary><audio controls preload="none" src="../ElevenLabs-正式台词试听-v003/{role}-1.mp3"></audio></details>'
 controls='' if e['kind']=='retained' else f'<label>本轮备注<input id="note-{role}" aria-label="{role}备注"></label><button onclick="saveChoice(\'{role}\')">保存备注</button> <button onclick="saveChoice(\'{role}\',0)">仍需调整</button>'
 cards.append(f'<section id="{role}"><h2>{role}</h2><p>你的备注：{html.escape(e["note"])}</p><p>{html.escape(e["description"])}</p><p class="status" id="status-{role}"></p><div class="grid">'+''.join(items)+'</div>'+baseline+controls+'</section>')
js=(OLD/'备注保存.js').read_text(encoding='utf8').replace('/api/voice-choice-v003','/api/voice-choice-v004').replace('声线选择-v003','声线选择-v004')
(OUT/'备注保存.js').write_text(js,encoding='utf8')
data=json.dumps(entries,ensure_ascii=False).replace('</','<\\/')
choices=(OUT/'作者选择.json').read_text(encoding='utf8').replace('</','<\\/')
page='''<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>白米饭 · 按备注返修试听 v004</title><style>body{max-width:1150px;margin:30px auto;padding:0 22px;background:#121923;color:#eef4ff;font:16px/1.7 system-ui}section{background:#1c2737;border-radius:14px;padding:22px;margin:22px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}article{padding:15px;background:#27364c;border-radius:10px}audio{width:100%}button{padding:9px 14px;border:0;border-radius:7px;background:#b8d8ff;color:#122136;cursor:pointer}input{display:block;width:95%;margin:12px 0;padding:10px;background:#121923;color:white;border:1px solid #789;border-radius:6px}a{color:#abd5ff}.status{color:#9ee6c4}.bar{position:sticky;top:0;background:#121923;padding:12px;z-index:2}</style><h1>白米饭 · 按备注返修试听</h1><p>先听新GPT和Kimi；天使、恶魔GPT已经合并到本体候选中。旧版与作者意见保留，本轮候选均未替换正片。技术检查不等于发音、情绪或音色通过。</p><div class="bar"><button onclick="exportChoices()">导出全部选择</button> <span id="notice">正在读取保存记录…</span></div><nav>'''+''.join(f'<a href="#{e["role"]}">{e["role"]}</a>　' for e in entries)+'</nav>'+''.join(cards)+'<script>const entries='+data+';let choices='+choices+';</script><script src="备注保存.js"></script></html>'
(OUT/'试听.html').write_text(page,encoding='utf8')
print(json.dumps({'roles':len(entries),'audio_files':sum(len(e['previews']) for e in entries)},ensure_ascii=False))
