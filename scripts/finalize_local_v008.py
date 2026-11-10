"""Publish the actual adopted working timeline and scoped review record."""
from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];O=R/'后期/局部收口-v008'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
A=read(O/'修后实际状态.json');L=read(O/'采用与问题台账.json');Qp=R/'视频制作/Metaso-H3-v012/执行队列.json';Q=read(Qp)
L.update(current_timeline=A['timeline'],working_timeline=None,previous_timeline='v005_2D_Anime_Fixes',status='局部修复已装入达芬奇并保存，待作者复看；尚未锁画或完成最终混音',frames=A['frames'],video_count=A['video_count'],audio_count=A['audio_count'])
statuses={'B13-push':'已采用v011源12–108帧；保留湿地祭坛，音效按接触/推出/落地分层对位','B17-entry':'已采用v010源24–84帧；九人、月夜、湿地和原武器；后续教主反应保留','B37-support':'局部补拍已装入；原声结束转Claude反应特写，遮蔽无声张嘴；Kimi前段保留','B37-bridge':'改用现有冷蓝湿地听者反应，源0–48帧按58.5366%播放；非新增干石阶','B40-42-carry':'仅8秒窗口采用连续托背托膝、抱起、站稳；行こう转托抱细节，保留原声与后续离场'}
for x in L['required']:x['status']=statuses[x['id']]
if not any(x['id']=='B10-tail' for x in L['required']):L['required'].insert(0,dict(id='B10-tail',frames=[3043,3175],issue='起身尾部漂移',status='剪去18帧漂移尾部，下阶提前并保留总长，三次落步同步提前'))
for c in L['candidates']:
 if c['id']=='GB011-1-v011-father-force-2d-r1':c.update(status='已用于v008，限源12–108帧；待作者最终核定',adopted=True)
for i in Q['items']:
 i.update(accepted=False,accepted_in_working_timeline=True,author_final=False,adopted_timeline=A['timeline'],adoption_note='仅采用后期执行计划指定窗口，原生口型未整条通过，已以听者/手部特写修剪')
 c=dict(id=i['attempt_id'],path=i['local_path'],status='已按指定窗口装入v008并局部裁切；待作者最终核定',adopted=True,source_window=i['proposed_source_window'])
 L['candidates']=[x for x in L['candidates'] if x['id']!=c['id']]+[c]
L['candidates']=[x for x in L['candidates'] if x['id']!='GB014-v010-original-shot-only-r1']+[dict(id='GB014-v010-original-shot-only-r1',path='视频制作/Metaso-H3-v010/产物/GB014-v010-original-shot-only-r1.mp4',status='已用于v008，限24–84帧',adopted=True)]
L['acceptance']=dict(structural=True,visual=False,lip_sync=False,continuous_listening=False,author_final=False)
L['verification_notes']=['已抽查真实达芬奇接头帧并独立复核前中后段；不等于全片逐帧/连续视听验收','110条未涉及视频的全部属性与源时间逐字段保持；B40未改前缀的原属性另行恢复','63句选声的64个音频片段来源与时点保持，13句仅改增益','48k PCM数学叠加峰值-5.164 dBFS，无削波；不含最终Fairlight总线/效果听审','B12让开为父亲前景与小鱼反应；未证明错说话者，保留','扇子母扇留手、单叶释放和撞击顺序经动态帧核查；不再列普遍缺法术','B25与水龙不凭材质体积感扩修，维持待作者观感核验']
L['preserve']=[x.replace('B26扇叶魔法已有，待逐帧确认','B26母扇留手/单叶释放/撞击顺序已核，保留原片') for x in L['preserve']]
L['cost']=dict(new_h3_tasks=2,generated_seconds=15,adopted_seconds=(67+192)/24,estimated_credits=153,actual_bill_verified=False,image_generation_cost_included=False)
save(O/'采用与问题台账.json',L);save(Qp,Q)
manifest=[]
paths=set(c['path'] for c in A['video'] if 'v008' in c['name'])|set(c['path'] for c in A['audio'] if '局部收口-v008' in c['path'])
for p in sorted(paths):
 f=Path(p);h=hashlib.sha256()
 with f.open('rb') as q:
  for b in iter(lambda:q.read(1024*1024),b''):h.update(b)
 manifest.append(dict(path=str(f.relative_to(R)),bytes=f.stat().st_size,sha256=h.hexdigest()))
save(O/'本轮采用媒体校验.json',manifest)
report='''# 《白米饭》局部收口 v008

当前达芬奇工程《白米饭》，时间线 `v008_Local_Continuity_Fixes` 已保存：44批、123个画面片段、11497帧（24fps，7分59秒01帧）、85个音频片段。v005原时间线仍在。当前版本是待作者复看的修订稿，尚未锁画或完成最终混音。

## 已落地

| 位置（分:秒:帧） | 本轮处理 |
|---|---|
| 第10批 02:06:19–02:12:07 | 剪短起身漂移尾部18帧，下阶提前，保持总长；三次落步声提前0.75秒 |
| 第13批 02:39:02–02:43:02 | 用已有v011的4秒同场景动作，接触/推出/手撑地/身体落地分别对音效 |
| 第17批 03:19:02–03:21:14 | 用已有v010的2.5秒夜景九人入场，保留原武器和教主反应 |
| 回忆返回 04:21:21–04:23:09 | 原M09以原曲前把手提前进入，和N01做36帧交接；后续音乐卡点保留 |
| 第37批 06:41:08–06:44:03 | 2.79秒二维原造型局部补拍；对白结束后切同一源的Claude反应，避开GPT无声张嘴 |
| 第37批 06:44:03–06:47:13 | 已有冷蓝湿地听者镜替换干石阶接头；源0–48按58.5366%帧采样，未启用光流 |
| 第40批末至42批 07:23:09–07:31:09 | 同一条动作保持托背托膝→抱起→站稳；07:26:04–07:27:04切托抱细节，保留“行こう”原声；原离场镜不动 |
| 对白 | 13句仅校正片段增益；不改台词、音色、源文件、时长；原咏唱1.12倍保调处理保留 |

本轮先取旧素材，再补两个确实缺失的局部镜头。MiniMax H3生成5秒+10秒，只采用约10.79秒；预计153积分，实际账单未核验，未包含修参考图的生图费用。没有整批重做。

## 采用与拒用

第13批只用v011父亲推出的12–108帧；第17批用v010的24–84帧，不用v011后段千问长剑漂移。v012的两条回片只采用指定窗口，并以剪辑解决所见嘴部矛盾；回片完成本身不代表整条通过。

此前改变人物设计的 late-collapse-2d、late-carry-2d、middle-ankle-2d 仍拒用、保留文件，不作为新输入。其余v011候选保留候选状态；Kimi、原Claude对白、展翼、水龙等未扩大替换。B12“让开”的现有前景父亲/听者反应未证明错说话者，保留。扇子单叶释放、母扇留手及撞击顺序已核，无需新增补拍。

## 已验证与边界

- 实际达芬奇读回：画面无空洞，8条音频轨均启用；63句选声仍为64片段，17段音乐、4条音效/环境工作轨保留。
- 110个完全未涉及的视频片段，其名称、源路径、源入出、速度及全部画面属性逐字段一致。第40批未改前缀另行逐项核验，保留原属性。B12作者删除20帧不回填。
- 本轮修复前后接头已从真实达芬奇抓静帧，前、中、后独立复核。证据在 `工程帧核验/` 和各段复核记录；抽帧不等于连续观看和听审。
- 对实际读回的85个声音片段进行48k立体声源片段+增益数学叠加，峰值约-5.164 dBFS，无超满刻度样本。结果不代表最终Fairlight总线效果、主观力度或音色验收。
- 重建音乐工作源保留原曲时间映射；24bit重编码存在极小量化差，不能称与旧文件字节相同。
- 没有导出新成片、DRP或DRT；只保存工程、工作音频及核验静帧。

## 仍待最终核验

必须在达芬奇连续复看本次修复及全片：近景口型是否自然，扶下与托抱裁切是否顺畅，回忆返回是否清楚，音效力量/距离/混响是否合适，BGM进退、跨句音色与咏唱保调质感是否可接受。保留这些待核项，未代作者宣布锁画或最终混音通过。

作者最终核验通过且明确要求后才导出。若局部仍不通过，先指出具体时码与缺失信息，再补最短必要镜头，不扩成整批返工。
'''
(O/'修订说明.md').write_text(report,encoding='utf8')
prefix='''## 2026-10-29：局部收口 v008（唯一当前工程入口）

达芬奇《白米饭》当前时间线 `v008_Local_Continuity_Fixes`：44批、123画面段、11497帧（7分59秒01帧）、85音频片段、8启用声音轨；v005保留。第10批剪短漂移尾部，第13/17批使用合格旧素材；第37扶下与第40末–42抱持共约10.79秒局部补拍，接头/嘴部用现有反应及托抱细节修剪。Kimi现有段落不动，不明显3D不重拍。13句仅改增益，作者选声、B12删20帧与原咏唱保调速度保留。

入口：[本轮工程内复看](后期/局部收口-v008/工程内审阅.html)；[修订说明](后期/局部收口-v008/修订说明.md)。两次H3预计153积分，账单未核。结构与PCM核验通过，仍待连续视听/精确口型/作者最终验收；没有新视频、DRP或DRT导出。作者最终核验并明确要求后才导出。所有实际生成参考须符合本片目标风格并守住原人物设计；拒用稿不再作参考。下方旧“当前”标题均为历史快照，不覆盖本节。

'''
(O/'本轮文档前缀.md').write_text(prefix.rstrip()+'\n',encoding='utf8')
for name in ['AGENTS.md','制作进度.md']:
 f=R/name;s=f.read_text(encoding='utf8')
 if not s.startswith('## 2026-10-29：局部收口 v008'):f.write_text(prefix+s,encoding='utf8')
subprocess.check_call(['python',str(R/'scripts/build_local_review_v008.py')],cwd=R)
print('Recorded adopted working timeline, unresolved acceptance, source hashes and scoped documentation')
