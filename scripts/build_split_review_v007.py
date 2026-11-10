"""Build a local audition page from the immutable split manifest."""
from pathlib import Path
import json,html,os
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'声音/逐句切分审阅-v007'
manifest=json.loads((OUT/'切分清单.json').read_text(encoding='utf8'))
asr=json.loads((OUT/'逐句ASR复核.json').read_text(encoding='utf8'))
inventory=json.loads((ROOT/manifest['source_inventory']).read_text(encoding='utf8'))
coverage=json.loads((OUT/'生成覆盖口径更正.json').read_text(encoding='utf8'))
prior_generated=set(coverage['gpt_current_voice_uncovered_but_prior_generated_ids'])
transcripts={(r['id'],r['take']):r['asr_text'] for r in asr['lines']}
assert len(transcripts)==51
notes={
 'VO-CY028B-01':'重点听「灰に眠る」的起音；两次转写均出现偏差，尚不能确定是否错读。',
 'VO-CY031A-02':'重点听结尾是否清楚说了「うん」；短句转写成「ふぅ」，可能是气声或识别错误。',
 'VO-CY024A-01':'重点核对「きよき水のぬしよ」，尤其开头和句末。',
 'VO-CY024A2-01':'重点核对「集え／つどえ」的读音。',
 'VO-CY024A3-01':'重点核对结尾「なせ」，不要只依据转写文字判断。',
 'VO-CY024A4-01':'重点核对「鎮め／しずめ」的收口。',
 'VO-CY024A5-02':'术名按「そうりゅうてんけい」逐音听核；转写无法验证术名。',
 'VO-CY024R-01':'三轮并听「ふるきいしよ」的句尾；「意志／石」是转写同音字问题，不据此判错。',
 'VO-CY024K1A-01':'三轮术名均有识别疑点，按「つきかげわたり」逐音核对。',
 'VO-CY021A-01':'对比三轮「我が娘よ」「神がお待ちだ」的助词、读音和压迫感。',
 'VO-CY019-01':'三轮「どけ」均被转写为不同词，短促喝令需直接听辨。',
 'VO-CY029-01':'核对「クロード……来なさい」的停顿与名字尾音；不应多出助词。',
 'VO-CY027A-01':'转写将「不干渉」识别成近音词；听核「ふかんしょう」，不把识别用字当实录。',
 'VO-CY010A-01':'片中木材名称按送读稿读「こくじん」；转写同音字不能当作真实台词内容。',
}
def esc(x):return html.escape(str(x),quote=True)
def link(p):return esc(os.path.relpath(ROOT/p,OUT).replace('\\','/'))
rows=[]
script=json.loads((ROOT/inventory['script']).read_text(encoding='utf8'))
script_order={r['id']:i for i,r in enumerate(script['lines'])}
for row in sorted(inventory['lines'],key=lambda r:script_order[r['id']]):
    cid=row['id']; candidates=[x for x in manifest['candidates'] if x['id']==cid]
    status='已有旧版母版·待衔接' if cid in prior_generated else ('新词录音未匹配' if row['audio_state']=='needs_recording' else ('已选母版切片' if candidates else '原独立录音保留'))
    body=f'<article data-role="{esc(row["voice_role"])}" data-focus="{str(cid in notes).lower()}" data-missing="{str(row["audio_state"]=="needs_recording").lower()}"><div class="meta">{esc(row["role"])} · {esc(cid)} <span>{status}</span></div><h2 lang="ja">{esc(row["ja"])}</h2><p>{esc(row["zh_back_translation"])}</p>'
    if cid in notes:body+=f'<p class="notice">{esc(notes[cid])}</p>'
    body+=f'<details><summary>表演提示与读音</summary><p>{esc(row["performance_direction_v004"])}</p><p lang="ja">送读：{esc(row["tts_reading_text"])}</p></details>'
    if candidates:
        body+='<div class="takes">'
        for c in candidates:
            body+=f'<section><b>第{c["take"]}轮</b> · {c["duration_seconds"]:.2f} 秒<audio controls preload="none" src="{link(c["file"])}"></audio><details><summary>转写与原件位置</summary><p lang="ja">{esc(transcripts[(cid,c["take"])])}</p><p>转写仅供定位，不能代替听审。</p><a href="{link(c["source"])}#t={c["start_seconds"]:.3f},{c["end_seconds"]:.3f}">母版 {c["start_seconds"]:.3f}–{c["end_seconds"]:.3f} 秒</a></details></section>'
        body+='</div>'
    elif cid in prior_generated:body+='<p class="notice">上一轮GPT完整18句母版已生成并保存；本句没有纳入后来的新声线11句母版。当前待核对声线衔接，不是从未生成，也不自动采用已被要求返修的旧候选。</p><a href="../ElevenLabs-正式台词试听-v003/试听.html#GPT">查看上一轮完整母版与原记录</a>'
    elif row['audio_state']!='needs_recording':body+=f'<audio controls preload="none" src="{link(row["existing_audio"]["file"])}"></audio>'
    else:body+='<p class="notice">已保留小鱼原声；当前清单尚未匹配这句新词的录音。先查既有产物，再补实际缺口。</p>'
    rows.append(body+'</article>')
roles=sorted({r['voice_role'] for r in inventory['lines']})
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · 逐句试听 v007</title><style>
*{box-sizing:border-box}body{margin:0;background:#111923;color:#e9edf3;font:16px/1.7 system-ui}main{max-width:1160px;margin:auto;padding:32px 24px}h1{font-size:32px;margin:0}h2{font-size:24px;margin:12px 0 3px}p{margin:8px 0}a{color:#9bd4ff}header,article{background:#1b2734;border:1px solid #344454;border-radius:12px;padding:22px;margin-bottom:18px}.muted,.meta{color:#b5c3d2}.meta span{float:right;color:#e8d49d}.notice{border-left:3px solid #d5ad62;padding:8px 12px;background:#302c24;color:#f3d9a7}.toolbar{position:sticky;top:0;background:#111923f5;padding:14px 0;z-index:2;display:flex;gap:12px;flex-wrap:wrap;align-items:center}select,button{font:inherit;padding:8px 14px;background:#26384b;color:#eef;border:1px solid #55718e;border-radius:6px}button,summary{cursor:pointer}audio{display:block;width:100%;margin:12px 0}.takes{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:16px}.takes section{padding:14px;background:#111923;border-radius:8px}details{color:#b5c3d2;font-size:14px}article[hidden]{display:none}@media(max-width:600px){main{padding:16px 10px}h1{font-size:26px}h2{font-size:21px}.meta span{float:none;display:block}}
</style><main><header><p class="muted">白米饭 / v0.69 台词 / v006 已定声线</p><h1>逐句试听</h1><p>35句已切分 · 51条表演候选 · 7句原独立录音 · 12句缺录</p><p>先听句首、句尾和表演；Kimi与教主每句提供三轮对照，目前尚未选轮。橙色提示是转写疑点，不是错读结论。其他句也仍需听审。</p><p class="muted">原速、原增益，保留句内停顿；本页未写入正片或替你确认采用。</p><a href="../../00_打开项目.html">返回项目</a> · <a href="../正式配音准备-v006/配音清单.html">声线与补录来源</a></header><div class="toolbar"><label>角色 <select id="role"><option value="">全部角色</option>'''
page+=''.join(f'<option>{esc(r)}</option>' for r in roles)
page+='''</select></label><label>范围 <select id="scope"><option value="all">全部54句</option><option value="focus">转写疑点</option><option value="missing">缺录12句</option></select></label><button id="stop">停止播放</button><span id="count"></span></div>'''+''.join(rows)+'''<script>
const audios=[...document.querySelectorAll('audio')];audios.forEach(a=>a.addEventListener('play',()=>audios.filter(b=>b!==a).forEach(b=>b.pause())));
document.querySelector('#stop').onclick=()=>audios.forEach(a=>a.pause());
function filter(){let n=0;const role=document.querySelector('#role').value,s=document.querySelector('#scope').value;document.querySelectorAll('article').forEach(a=>{a.hidden=(role&&a.dataset.role!==role)||(s==='focus'&&a.dataset.focus!=='true')||(s==='missing'&&a.dataset.missing!=='true');if(!a.hidden)n++;else a.querySelectorAll('audio').forEach(x=>x.pause())});document.querySelector('#count').textContent=`显示 ${n} 句`}
document.querySelector('#role').onchange=filter;document.querySelector('#scope').onchange=filter;filter();
</script></main></html>'''
page=page.replace('35句已切分 · 51条表演候选 · 7句原独立录音 · 12句缺录','35句已切分 · 7句原独立录音 · 9句旧版待衔接 · 3句新词未匹配')
page=page.replace('先听句首、句尾和表演；Kimi与教主每句提供三轮对照，目前尚未选轮。','角色声线已确认，无需重新选声。这里将已生成母版拆开供局部核对；Kimi与教主的三轮是同一已选声线里的重复表演。')
page=page.replace('缺录12句','声音待办12句')
page=page.replace('其他句也仍需听审。','无需重新进行全角色选声。')
(OUT/'逐句试听.html').write_text(page,encoding='utf8')
(OUT/'听审疑点.json').write_text(json.dumps(dict(status='ASR_flags_not_confirmed_mispronunciations',notes=notes),ensure_ascii=False,indent=2),encoding='utf8')
print('review page: 54 lines / 58 playable audio sources / prior GPT generation restored to view')
