"""Synchronize the v0.9 editorial decisions and archive immutable render inputs."""
import hashlib,json,shutil,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
rec=R/'镜头设计/生成记录/逐镜独立-v009'
mf=R/'镜头设计/shot-plan-v0.9.json'
d=json.loads(mf.read_text(encoding='utf-8'))
ss=d['shots']; by={s['id']:s for s in ss}
s=by['CY020A']
s['exit_state']='宝宝伏在阶下，无力起身，仍想阻止教主。'
s=by['CY016D']
s.update(title='黑袍逼近，回头惊觉',framing='近景／黑袍前景与宝宝反应',purpose='把教徒逼近与宝宝阶下落地接起来；抓扯留在画外。',action='黑袍逼近，DeepSeek回头惊觉；画面切走，衣料拉扯与跌落声接下一镜。',exit_state='黑袍遮向镜头，画外跌落接阶下撑地。',sound='逼近脚步、衣料拉扯与画外落地；拟音待制作。',source_quote='黑袍的阴影罩住小鱼，她突然回头，惊慌地看向逼近的教徒。')
by['CY013']['framing']='面部与肩胸特写／察觉与担忧'
by['CY021']['sound']='急促喘息、衣料擦地。'
for i,s in enumerate(ss):
 s['next_link']=('接 '+ss[i+1]['id']+'：'+s['exit_state']+' → '+ss[i+1]['entry_state']) if i+1<len(ss) else '片尾停留后结束。'
 s['visual_prompt']=f"《穿云》{s['id']}。{s['action']} 开始：{s['entry_state']} 结束：{s['exit_state']} 人物设计延续原图，画面无字。"
 s['presentation']['visible']=s['action']
mf.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
script=R/d['story_script'];t=script.read_text(encoding='utf-8')
old='最后一名教徒在队尾掩上正门，门闩落下。随着这声闷响，一只手抓住 DeepSeek，将她从祭坛上拽下来。'
new='最后一名教徒在队尾掩上正门，门闩落下。黑袍的阴影罩住小鱼，她突然回头，惊慌地看向逼近的教徒。画面切走，一只手抓住 DeepSeek，将她从祭坛上拽下来；只听见衣料与落地声。'
t=t.replace(old,new).replace('- v0.8 当前采用顺序：','- v0.8 历史顺序（v0.9在其基础上调整）：')
script.write_text(t,encoding='utf-8')
entry=R/'00_打开项目.html';t=entry.read_text(encoding='utf-8')
t=t.replace('v0.8','v0.9').replace('4 分 36 秒','4 分 28 秒').replace('天瀑破顶、雷雨与爆闪、公主抱离殿','鲸帽卡住、仰视腾空、远俯教堂；逐镜独立原画')
entry.write_text(t,encoding='utf-8')
# Reconstruct submitted images from retained original outputs when an early edit used a mutable display path.
outputs=json.loads((rec/'输出归档.json').read_text(encoding='utf-8'))
ledger=json.loads((rec/'执行状态.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
archive=rec/'输入原件';archive.mkdir(exist_ok=True)
for r in ledger['requests']:
 doc=json.loads((rec/r['file']).read_text(encoding='utf-8'))
 request=doc.get('request',doc)
 r['request_sha256']=sha(rec/r['file']);r['inputs']=[]
 for raw in request.get('referenced_image_paths',[]):
  p=Path(raw);reconstructed=False
  if '独立镜头-v009' in raw:
   id=p.stem.replace('-v009','')
   p=Path(ledger['initial_outputs'][id]);reconstructed=True
  assert p.is_file(),p
  h=sha(p);dst=archive/(h[:16]+p.suffix)
  if not dst.exists():shutil.copy2(p,dst)
  r['inputs'].append(dict(submitted_path=raw,immutable_copy=dst.relative_to(R).as_posix(),source_original=str(p),sha256=h,reconstructed_from_retained_original=reconstructed))
for o in outputs.values():
 for h in o.get('history',[]):
  p=Path(h['original']);h['sha256']=sha(p)
ledger['input_note']='实际请求原文未改。早期局修曾引用展示副本，已按提交时对应的保留生成原件重建输入快照；新局修直接引用不可变原件。生成索引中的 archive hash 仅表示归档时路径内容，以本执行记录的输入原件为重放依据。'
(rec/'执行状态.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(rec/'输出归档.json').write_text(json.dumps(outputs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(shots=len(ss),seconds=d['total_seconds'],independent_renders=len(outputs),requests=len(ledger['requests'])),ensure_ascii=False))
