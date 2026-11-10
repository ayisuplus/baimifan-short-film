"""Write the in-project review guide; never render or export Resolve media."""
from pathlib import Path
import json,html,hashlib
R=Path(__file__).resolve().parents[1];O=R/'后期/声画重构-v002'
def read(p):return json.loads(p.read_text(encoding='utf8'))
P=read(O/'后期执行计划.json'); S=read(O/'音效施工记录.json'); Q=read(R/'视频制作/Metaso-H3-v005/执行队列.json'); mix=read(O/'混音电平检查.json')
def tc(f):
    f=round(f);return f'{f//86400:02d}:{f//1440%60:02d}:{f//24%60:02d}:{f%24:02d}'
changes={7:'补上小鱼逐级上阶，明确殿门到刑架的空间过渡。',8:'提前Claude回应画面；小鱼说话期间用手部开锁承接，取消过快处理。',9:'把小鱼发话与画面对齐，给锁具操作留出时间。',10:'补小鱼逐级下阶，连接刑架与搬柴教徒。',11:'替换为明确肩部接触后失衡半跪，去掉双脚跳起。',12:'更换教主仰望高处Claude的机位，按录音实际发话段剪口，不把尾部静音当对白。',13:'保留前段站位，补掌部接触后摔倒的受力过程。',14:'Claude呼喊后切抓袍手部，留白后回到脸部恳求；裁掉不合剧情的背景。',16:'保留门外蓄势，补完整踹门、门扇内开、脚落地。',17:'延长进门停留，Kimi画外音仍在教主反应镜头下。',18:'保留4秒无对白显形，放慢局部动作承接。',19:'刀刃、银流、凝实分段；两帧亮闪遮住轻微姿态接缝。',27:'水滴合流镜头采用无声画面反放；配音保持正向完整原速。',28:'云层后接真正水面，补清空间变化。',30:'Kimi检查脚部束缚时保留未解除的腕部状态，消除提前自由垂手。',38:'恢复父亲伸手，再接两段迟疑表情，原四句完整录音保留。',39:'移除已前移的重复父亲反应，用实际手部段承接停顿。',42:'恢复3秒走向门外，门外火盆保留，殿内仍冷湿。',44:'吃饭动作恢复正常速度，结尾保留4秒无BGM。'}
count=len(S['events']); estimated=sum(x.get('estimated_credits',0) for x in Q['items'])
lines=[f'# 白米饭 · 声画重构 v002（待作者核验）','',f'当前达芬奇工程：《白米饭》；时间线：`{P["timeline"]}`。全长 **{tc(P["frames"])}，467.625秒**，44批、103个剪辑段。旧v001线和原媒体保留。','',
'## 当前播放方式','',
'直接在达芬奇剪辑页播放当前时间线。主代理已把播放头放在第7批起点 **00:01:19:14**，优先检查小鱼进入教堂至Kimi出现。不要根据历史成片判断本轮声音是否已装配。','',
'作者明确要求：**最终核验通过并明确要求后再导出**。本轮未导出完整成片或交付DRP/DRT；该指令到达前已完成一条第19批无声短测试，保留取证，不是当前审阅成片。','',
'## 已装配','',
f'- 63句作者选定配音，全部源文件不变、完整长度、100%速度，无相邻录音重叠。',
f'- 13段BGM按新画面重排，保留原速和对白避让，最后4秒无BGM。',
f'- {count}处声音事件分为环境、拟音、动作和魔法4条工作声轨；加上对白、音乐，共6轨。每处源文件、截取、音量、声像、回响和对位记录在`音效施工记录.json`，工作WAV位于`声音/`，这些是剪辑素材，不是成片导出。',
f'- {len(Q["items"])}次MiniMax H3局部补拍调用，11条采用、5条弃用，未整批重做；预计{estimated:.1f}积分，未核实账单扣费。冻结输入与失败候选均保留。','',
'## 重点核验位置','',
'|批次|当前起点|修改内容|','|---|---|---|']
for b in P['batches']:
    if b['batch'] in changes:lines.append(f'|第{b["batch"]}批|{tc(b["start"])}|{changes[b["batch"]]}|')
lines+=['','## 检查结果与边界','',
'文件与达芬奇实际时间线读回一致：103段画面连续、11223帧；63句配音时长及原速逐一吻合；原44批媒体SHA256未变。',
f'工作PCM混音检查为有限样本、无削波；统一输出增益{mix["shared_gain_db"]:.1f}dB，样本峰值{mix["peak_after_gain"]:.3f}。此结果不是实际AAC成片检测，也不等于主观响度已验收。',
'第19批显形接缝已有短测试独立复核；其余采用依据源片抽帧、声活动边界与剪辑计划。整条新线尚未完成连续听审、音素级口型及作者观感验收。工程内光流、裁切与镜间呼吸仍应实际播放复看，不能用技术检查代替。',
'音效使用已下载的[効果音ラボ](https://soundeffect-lab.info/)素材，来源及许可链接存`音效来源清单.json`。Fairlight本地常见目录未发现安装库，作者确认可能尚未安装，因此没有继续寻找或安装。',
'少数旧脚步点的补充判定见`音效对位增量.json`（若存在）；链条、扇骨、细餐具与角色非语言喘息没有冒称已经独立录制。已用锁具/衣料/木材等声层服务动作，具体材质和表演适配仍待实听。','',
'## 工作记录','',
'- `后期执行计划.json`：剪辑段、声音位置与旧新时码映射。',
'- `达芬奇时间线核对.json`、`文件与剪辑计划检查.json`：实际工程读回与媒体完整性。',
'- `音效设计-对位.json`、`音效施工记录.json`、`声音施工记录.json`：声音工作文件。',
'- `采用剪辑.json`、分段独立审查及补拍复核：采用理由和剩余限制。',
'- `../../视频制作/Metaso-H3-v005/补拍输入.html`：冻结局部补拍输入。','']
(O/'修订说明.md').write_text('\n'.join(lines),encoding='utf8')
table=''.join(f'<tr><td>第{b["batch"]}批</td><td>{tc(b["start"])}</td><td>{html.escape(changes[b["batch"]])}</td></tr>' for b in P['batches'] if b['batch'] in changes)
page=f'''<!doctype html><meta charset="utf-8"><title>白米饭 · 达芬奇声画重构 v002</title><style>body{{font:17px/1.65 system-ui;background:#151b24;color:#e9eef4;max-width:1050px;margin:40px auto;padding:20px}}a{{color:#8dd3ff}}td,th{{text-align:left;padding:12px;border-bottom:1px solid #445}}.notice{{padding:18px;background:#293d4d}}code{{color:#f6d69b}}</style><h1>白米饭 · 声画重构 v002</h1><p class="notice">在达芬奇直接核验；待作者明确要求后再导出。当前没有本轮完整成片。</p><p>时间线 <code>{P['timeline']}</code> · 7分47.625秒 · 44批 · 103剪辑段</p><p>63句完整原速对白、13段BGM、{count}处环境与动作音效已装配。优先从 <b>00:01:19:14</b> 第7批看至第20批。</p><p><a href="修订说明.md">修订说明及检查边界</a> · <a href="../../视频制作/Metaso-H3-v005/补拍输入.html">局部补拍输入与历史候选</a></p><table><thead><tr><th>批次</th><th>当前时间码</th><th>重点核验</th></tr></thead><tbody>{table}</tbody></table><p>已作文件、时长、实际时间线与样本电平检查；连续听审、音素口型和最终观感仍待核验。不要把旧视频或第19批无声短测试当成本轮带声音版本。</p>'''
(O/'工程内审阅.html').write_text(page,encoding='utf8')
print(json.dumps({'guide':str(O/'修订说明.md'),'sound_events':count,'estimated_credits':estimated},ensure_ascii=False))
