"""Render the Japanese-first screenplay dialogue draft; never submits media."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];P=R/'剧本/白米饭-日语对白-v0.65.json';D=json.loads(P.read_text(encoding='utf8'))
rows=D['lines'];byid={v['id']:v for v in rows};active=[v for v in rows if v['ja']]
assert len(byid)==63 and len(active)==54
for v in rows:
 if not v['ja']:assert byid[v['merged_into']]['ja']
def esc(s):return str(s).replace('|','\\|').replace('\n',' ')
out=['# 《白米饭》日语对白主稿 v0.65','', '**待审稿；尚未配音、未替换当前v008。日语是创作主稿，中文为回译。**','',
'这次重点压缩咏唱，并修五处对白的表达。原63个对白ID保留，9个合并后不再单独朗读，共54句活动台词；原始台词、声音和时间线都保留。已自然的短句不为变化而硬改。','',
'主数据为同目录 `白米饭-日语对白-v0.65.json`。本文件从主数据生成，表演说明和读音提示不混入TTS朗读正文。','', '## 三段咏唱','']
for role,g in D['groups'].items():
 out += ['### '+role,'']
 for k in g['new_ids']:
  v=byid[k];out += ['> '+v['ja'],'>','> '+v['zh_back_translation'],'']
 lo,hi=g['spoken_budget_seconds']
 out += [f"原配音片段合计约{g['previous_audio_seconds']:.1f}秒；新稿口播目标约{lo}–{hi}秒，仅为表演预算，未经配音实测。",'',g['scene_budget_note'],'']
 if role=='Kimi':out+=['动作顺序：呼唤与举刃起势→银光蓄起→投刃破窗→明刃钉稳→报“月影渡り”→循刃瞬移、回收。护罩是之后的独立防御动作。标读しるべ、刃读やいば。','']
 if role=='GPT':out+=['呼唤→水聚→天海成形→止火与救赎的连续祈愿→术名。第四、五句不能各自拉成长停顿。术名后才释放主龙；水龙攻击敌方金罩的动作仍保留，不因为删掉“高墙”一句就删除这段剧情。日文沿用原「蒼龍天傾」，读そうりゅうてんけい；中文术名仍为「沧龙天倾」。','']
 if role=='Claude':out+=['第一句后仍有父亲的「クロード……来なさい。」及Claude的反应。她选择继续，才说「この手に、宿れ。」；不是从头再起咏。束具此时已解，掌心光屑→火种→空刑架起火→脱力的顺序保留。星火读せいか。','']
out+=['## 五处对白修订','', '| 位置／人物 | 日语主稿 | 中文回译 | 表演意图 |','|---|---|---|---|']
for k in ['VO-CY006-01','VO-CY007-01','VO-CY008M-02','VO-CY021-01','VO-CY026D-01']:
 v=byid[k];out.append('| '+ ' | '.join(map(esc,[f"B{v['previous_batch']} {v['role']}",v['ja'],v['zh_back_translation'],v['direction']]))+' |')
out+=['','B13「その子に触らないで！」本身自然，保留怒喊；B14改为向父亲低声求准许孩子离开。开头Claude的「ありがとう。でも、私……」保留；开头与结尾「少し食べる？」保持完全相同，结尾只答「うん。」。','',
'## 按角色批量组织配音','',
'同一个角色统一声线和批次管理。实际配音按场景／表演段组织，保留逐句ID、原始输出和可替换的片段。一次生成整段台词，并不保证从低语到怒喊再到咏唱都自然；若成段生成，连续对话或同一段咏唱可一起表演，不能把全片相隔很远的场景不加区分地拼成一段。','',
'顺序：日语台词审定→代表句选声与表演试听→定该段实录节奏→画面预演→必要局部补拍。ElevenLabs与本地克隆尚未调用；是否本地克隆应看试听结果，不先锁流程。','',
'## 全片活动对白（叙事顺序）','', '| ID／旧批次定位 | 人物 | 日语主稿 | 中文回译 | 状态 |','|---|---|---|---|---|']
for v in active:out.append('| '+' | '.join(map(esc,[v['id']+f" / B{v['previous_batch']}",v['role'],v['ja'],v['zh_back_translation'],'修订' if v['status']=='revised_draft' else '保留']))+' |')
out+=['','旧批次和帧号只用于找到原片，不作为新录音剪点。','', '## 合并追踪（不再单独朗读）','', '| 原ID | 合并／承接ID | 原因 |','|---|---|---|']
for v in rows:
 if not v['ja']:out.append('| '+' | '.join(map(esc,[v['id'],v['merged_into'],v['direction']]))+' |')
out+=['','## 核验边界','', '已对照v0.64设定、v008对白与动作先后，三段咏唱和重点对白做独立文字复核。没有声称日语母语者或配音演员已经验收；真正的口腔节奏、读音与情绪仍需试听。当前稿含称谓、术名和停顿的表演取舍，等待作者审阅。','']
(R/'剧本/白米饭-日语对白-v0.65.md').write_text('\n'.join(out),encoding='utf8')
print('Rendered 54 active cues, 9 merged IDs, no generation or timeline change')
