"""Read-only creative review; never modifies the production board or shot source."""
import json, hashlib, html
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '后期/全片张力审查-v016'
index = json.loads((OUT / '审查索引.json').read_text(encoding='utf-8'))
shots = index['shots']
byid = {s['id']: s for s in shots}
reports = [json.loads((OUT / f'分段复核-{i:02}.json').read_text(encoding='utf-8-sig')) for i in range(1,4)]
coverage = sorted(i for r in reports for i in r['coverage_indices'])
assert coverage == list(range(1,134))
source = ROOT / '镜头设计/shot-plan-v0.61.json'
sha = hashlib.sha256(source.read_bytes()).hexdigest()
assert sha == '64211b935fc38d7bb7cdcf1edeaec1a970d730bf2ffdbb868875fa6615e1367a'
for s in shots:
    assert hashlib.sha256((ROOT / s['path']).read_bytes()).hexdigest() == s['sha256'], s['id']

priority = [
 dict(ids=['CY022A'], title='衣摆滑脱：最后的抵抗没有成为画面中心', problem='小鱼的指尖失去袍角，本该是这一刻最痛的变化；现在眼睛却容易先看金色台阶、教主背影和整座祭坛。紧接攥袍特写又退远，下一镜还要再次交代登阶，尺度重复。', recommendation='贴地斜侧近拍手、袍尾与孩子半张脸。布料从绷紧到滑过指尖，手最后一次试合却落空；教主身体只留边缘，下一镜才放开距离。收住地面亮点，保留左鱼右教主。', treatment='重设机位与动作关键状态。单纯裁大当前已经松开的手，补不出失去接触的一瞬。', reason='主审与前段独立复核一致。'),
 dict(ids=['CY021A'], title='接火把：处刑的选择拍得像礼仪交接', problem='两人完整摆开、火把垂直居中、蓝窗整齐发亮。道具递得很清楚，但父亲接过工具去伤害女儿的关系很弱。', recommendation='从递火教徒肩侧贴近：前景是接牢火把的右手和黑紫火焰，父亲眼神朝高处受缚的Claude转去，深处只留可辨的白色轮廓。短拉焦连接工具、执行者和目标。', treatment='改拍纵深关系，保留父亲冷静，不演成犹豫，也不用怒吼补张力。', reason='主审与前段独立复核一致。'),
 dict(ids=['CY023'], title='踹门：破门的冲击让位给完整人物亮相', problem='原图已有脚与门的撞击点，也有木屑；弱的是直立的腰肩和铺开的礼服占据视觉中心，动作更像抬腿展示。下一镜本来还要完整揭示援军，两次亮相的功能偏近。', recommendation='改成贴近门内侧的斜向低机位，让鞋底撞击、门板向镜头掠过和冷光裂口成为主体；人脸可暂被门框遮住。2秒内完成撞开与落脚，下一镜再看清全队。', treatment='主审的风格优先建议，非动作错误。可以保留GPT轻松踹开的态度，让门与碎屑承担冲击，不必把她演得吃力。', reason='主审追加；独立中段复核没有将此镜列为必改。'),
 dict(ids=['CY027B1'], title='GPT化龙：画面华丽，但升级关系没有拍清', problem='完整人形和身后独立完整龙首同时展示，第一眼更像再次召龙。前面已经有水龙大招，这一镜需要让观众明确感到“她本人变了”。', recommendation='补一个人身向龙身连续转换的阶段关键帧：白角、紫鬃与旋转水光保持方向连续，身体轮廓顺势转为长身龙，只保留一个变形主体；不要用完整人形与完整龙并列做主要阶段。', treatment='不是再加特效或拉近龙眼；是改清主体变化。保留2秒节拍及之后穿顶方向。', reason='主审与中段独立复核一致；属于叙事清晰度带来的张力提升。'),
 dict(ids=['CY028A'], title='解锁后站稳：她惦记小鱼的那句话太远', problem='三个人、长裙、蓝窗和地面都完整呈现。迈下脚托能看懂，但6.2秒里“那个孩子……”的牵挂仍被全身展示稀释，当前摄影又向后退。', recommendation='开头保留脚托到地面的一步，随后顺着Claude视线收至胸上双人近景，让GPT扶上臂的手与Claude寻找阶下孩子的眼睛同框；Kimi退入虚焦。', treatment='优先修改镜内摄影和补近景结束参考，不必整张废弃。镜长、原对白不变。', reason='主审与后段独立复核一致。'),
 dict(ids=['CY029C','CY029D'], title='脱力到接抱：需要接住重量，而不只是接成姿势', problem='连续画面都是左侧高亮火架、右侧蓝窗、两位漂亮人物。Claude倾斜但承重变化不鲜明，下一张已经贴头接近抱稳；接着还有稳定抱持与主动搭肩，容易成为一串相近合影。', recommendation='先改脱力这一张：同侧30–45度、腰高侧中景，清楚给出肩胯失衡、手垂落与GPT跨入接重的空间。下一镜连贯托背、探膝、起抱，再到后两镜稳定贴近。火架退到边缘虚焦，暖光只勾轮廓。', treatment='先改一个动作节点，再核查接抱衔接。不要四张全部重做，也不追加摔地或反复踉跄。', reason='主审与后段独立复核一致。'),
]
secondary = [
 dict(ids=['CY024A'], title='展翼起咏：优先收光，不急着缩景', problem='白裙、白翼、水珠、吊灯、蓝窗几乎都亮，脸与抬升方向没有足够主次。', recommendation='降低窗灯和地板高光，保住脸与翼缘；用下扇扬尘、水珠上浮、摄影跟升落实起飞。全身仍要留，才能交代离地与翼展。'),
 dict(ids=['CY024A5'], title='12秒结印：保持仪式中心，落实慢推与蓄势', problem='单张很容易像完整宣传海报，但现脚本已有慢推，不能把12秒直接当静止展示来判。', recommendation='保留中心构图和水龙尺度，推进后让脸与手印读得更清楚；用前后水流视差与蓄势变化支撑时长。不要提前攻击，不破坏祈愿到报术名的节拍。'),
 dict(ids=['CY024','CY027D','CY027F'], title='援军与胜负群像：避免连续“大家站好”', problem='全员露脸有建立阵容的作用，但后续防线和胜者镜头重复完整展示，容易平。', recommendation='保留第一次全队亮相；防线用错开的目光、武器转向和重心变化；胜负已分时向GPT下视教主的关系收近，不再强调每个人的衣饰。'),
 dict(ids=['CY006','CY008','CY026C'], title='请求与回应：靠反应差异，而不是统一加暗', problem='请求与失望反打的表情近似；发射塔邀请里火箭与灯光抢走点头反应。', recommendation='让请求到失望有目光、手势的变化；发射塔收背景对比，把Grok的回应作为焦点。原来明亮轻松的段落仍可明亮。'),
]
keep = [
 dict(ids=['CY009A','CY012'], title='空间与距离', reason='目送小鱼和第一次进入空教堂，需要人物变小来交代情感距离、祭坛方位。拉近反而失去信息。'),
 dict(ids=['CY019','CY020B','CY024A0','CY024A10','CY024A11','CY024A12'], title='刚调整的对峙、保护与扇子', reason='遮挡、高度差、近距离法术接触已更明确；这轮不建议再次推翻。实际动态仍需验收。'),
 dict(ids=['CY024K4'], title='试镣后的收刀', reason='核对原动作后，当前图是收刀后的状态：腕扣紫纹、Claude痛感与Kimi关切已在画面里，不应误当缺少试镣动作而重画。'),
 dict(ids=['CY027E','CY027E1','CY029E1'], title='雨滴与选择前的停顿', reason='安静是前后强动作的节奏对照；Claude听父亲后仍继续的变化靠微表演，不需要更大特效。'),
 dict(ids=['CY031','CY034'], title='空座位与结尾长椅', reason='空位等待与7秒相处是“终于安全”的落点。保留暖日光和呼吸，不把它们改成紧绷近景。'),
]
root_full = ['CY021A','CY022A','CY023','CY024','CY024K4','CY024A','CY024A8','CY024A5','CY027B1','CY028A','CY029C','CY029D']
report = dict(status='审查建议，未采用；本轮未换图', source=str(source.relative_to(ROOT)), source_sha256=sha, coverage=133, independent_coverage=coverage, root_full=root_full, independent_original_views=sum(len(r['inspected_full']) for r in reports), priority=priority, secondary=secondary, keep=keep, limits='静帧与镜头动作设计的艺术审查，不等于动态成片、配音或混音验收。六处为优先创意修订，不是六项技术不可生成。')
(OUT/'综合审查.json').write_text(json.dumps(report, ensure_ascii=False, indent=2),encoding='utf-8')

def esc(x): return html.escape(str(x),quote=True)
def time(s): return f'{int(s//60):02}:{s%60:05.2f}'
def pic(s):
    url=quote('../../'+s['path'],safe='/')
    return f'<figure><a href="{url}" target="_blank"><img loading="lazy" src="{url}" alt="{esc(s["id"]+" "+s["title"])}"></a><figcaption>{esc(s["id"])} · {time(s["start"])} · {s["seconds"]}秒 · {esc(s["title"])}</figcaption></figure>'
def cards(items,kind):
    out=''
    for i,f in enumerate(items,1):
        out+=f'<article id="{f["ids"][0]}"><div class="tag">{kind} {i:02}</div><h2>{esc(f["title"])}</h2><div class="pics">'+''.join(pic(byid[x]) for x in f['ids'])+'</div>'
        for key,label in [('problem','现在的问题'),('recommendation','怎么拍更有效'),('treatment','修改范围'),('reason','判断依据')]:
            if key in f: out+=f'<p><b>{label}：</b>{esc(f[key])}</p>'
        out+='</article>'
    return out
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · 全片张力审查</title><style>
*{box-sizing:border-box}body{margin:0;background:#111820;color:#e9edf0;font:16px/1.75 system-ui,"Microsoft YaHei",sans-serif}main{max-width:1120px;margin:auto;padding:30px 26px 80px}h1{font-size:34px;line-height:1.3}h2{font-size:23px;line-height:1.4}a{color:#c4d9ff}nav{display:flex;gap:18px;flex-wrap:wrap;padding:12px 0}.lead{font-size:19px;max-width:860px}.note{color:#b4bfc8}.stats{display:flex;gap:12px;flex-wrap:wrap}.stats span,.tag{padding:5px 11px;background:#283543;border-radius:5px}.tag{display:inline-block;color:#ffd28b;font-size:13px}article{padding:24px;background:#1a242e;border:1px solid #34414e;border-radius:12px;margin:24px 0}figure{margin:0;min-width:0}img{display:block;width:100%;height:auto;border-radius:6px}figcaption{font-size:13px;color:#b6c7d5;margin:7px 0 12px}.pics{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,360px),1fr));gap:15px}p{margin:12px 0}summary{cursor:pointer;font-size:20px;padding:12px 0}section{scroll-margin-top:20px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:18px}.small{font-size:13px;color:#a5b3c2}b{color:#f3d6aa}footer{border-top:1px solid #34414e;margin-top:28px;padding-top:22px}</style><main>
<p class="note">白米饭 / 当前生成板 v016 / 2026-10-27 / 仅审查，未换图</p><h1>华丽已经够了，<br>关键时刻要更准确。</h1><p class="lead">全片仍有类似问题。建议先改下面6处：让失去接触、撞开门、身体变形、承担重量这些真正的变化成为画面中心。并非所有镜头都要拍近、拍暗或加特效。</p><div class="stats"><span>133 镜全覆盖</span><span>3 段独立复核</span><span>6 处优先建议</span><span>保留当前生成板</span></div><nav><a href="#priority">优先改拍</a><a href="#secondary">局部优化</a><a href="#keep">建议保留</a><a href="#all">133镜索引</a><a href="../../视频制作/生成板-v016/生成板.html">当前生成板</a><a href="../扇子法术-v016/全片声音预览.html">全片带声预览</a></nav><p class="note">以下时间为全片起点。点击图片看原图；图下标明镜号与镜长。审查针对静帧及动作设计，尚未验收实际动态成片。</p><section id="priority">'''
page+=cards(priority,'优先改拍')+'</section><section id="secondary"><h1>这些先局部优化</h1>'+cards(secondary,'局部优化')+'</section><section id="keep"><h1>这些值得保留</h1>'+cards(keep,'保留')+'</section>'
page+='<section id="all"><details><summary>展开全片 133 镜索引与原图</summary><div class="grid">'+''.join(pic(s) for s in shots)+'</div></details><details><summary>查看独立复核与覆盖证据</summary><ul>'
page+=''.join(f'<li><a href="分段复核-{i:02}.json">第{i}段独立报告</a></li>' for i in range(1,4))
page+='</ul><p>主审看完12张全片联系表，并放大12张候选原图；独立复核另有32次原图查看记录（含重复镜及内心戏状态，不等于32张互不相同的主画面）。133镜图像哈希与审查索引一致。</p><a href="综合审查.json">综合审查数据</a> · <a href="审查索引.json">原图路径与哈希</a></details></section><footer class="small">审查源：shot-plan-v0.61.json<br>SHA256：'+sha+'<br>本轮只新增审查资料，不改变生成输入、镜长、配音、BGM或采用状态。</footer></main></html>'
(OUT/'审查.html').write_text(page,encoding='utf-8')
md=['# 全片张力审查 v016','',report['limits'],'','133镜全覆盖；3段独立复核；主审12张候选原图放大；六处优先修订建议尚未采用。','']
for f in priority:
    md += ['## '+f['title'],'',' / '.join(f['ids']),'',f['problem'],'',f['recommendation'],'',f['treatment'],'']
md+=['详细原图、次级建议与保留意见见同目录审查.html及三份分段复核。','',f'源 SHA256：{sha}']
(OUT/'审查结论.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'coverage':len(coverage),'priority_groups':len(priority),'source_unchanged':True,'all_133_image_hashes_unchanged':True,'html':str(OUT/'审查.html')},ensure_ascii=False))
