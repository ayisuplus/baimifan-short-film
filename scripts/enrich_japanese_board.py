"""Project-only returned-audio review UI; shared renderer remains unchanged."""
import json,re
from pathlib import Path

def enrich(root,out):
    mapping=out/'日语音频映射.json'
    if not mapping.exists():return
    data=json.loads((out/'展开数据.json').read_text(encoding='utf-8'))
    audio=json.loads(mapping.read_text(encoding='utf-8'))
    bykey={(x['batch_id'],x['cue_index']):x for x in audio['cues']}
    for batch in data['batches']:
        for i,cue in enumerate(batch['dialogue']):cue['returned_audio']=bykey[(batch['id'],i)]
        for model in batch['models'].values():
            model['issues']=[('日语回交文件已绑定；实际发声时长见对白卡，超窗/母版切分问题及逐字听审、口型仍待解决。' if '当前对白时间沿用预演预算' in s else s) for s in model['issues']]
    data['post_captions']=[dict(shot_id='CY026A',start=208.5,end=210.5,zh='稍早',ja='少し前',note='后期字幕，非对白，不让视频模型生成'),dict(shot_id='CY031',start=411.5,end=413.5,zh='数日后',ja='数日後',note='后期字幕，非对白，不让视频模型生成')]
    (out/'展开数据.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    p=out/'生成板.html';page=p.read_text(encoding='utf-8')
    payload=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    page=re.sub(r'(<script id="data" type="application/json">).*?(</script>)',lambda m:m[1]+payload+m[2],page,count=1,flags=re.S)
    page=page.replace('译配措辞仍是草案；时间为表演预算，未做声音或口型实测。','日语文本与交回音频逐句绑定；原画面预算保留，实际发声时长在下方对照。超窗、切分与逐字听审尚有待办。')
    page=page.replace('中文原意与日语候选并列','中文原意与日语回交稿并列')
    extra=r'''<style>.returned-audio{border-top:1px solid #536175;padding-top:12px;margin-top:14px}.returned-audio audio{width:min(100%,540px);display:block;margin:10px 0}.returned-audio .warn{color:#ffd0a2}.returned-audio .fit{color:#c2e1b8}.returned-audio img{max-width:550px;display:block}.audio-proof{font-size:13px;color:#b6c0cc}</style>
<script>
const originalDialogueCard=dialogueCard;
dialogueCard=function(b,c,i){let card=originalDialogueCard(b,c,i),a=c.returned_audio;if(!a)return card;let row=b.rows.find(r=>r.id===c.shot_id),ref=row&&b.references.find(r=>r.slot===row.slot);let status=a.state==='speech_over_budget'?'发声超窗 · 待解决':a.state==='timing_margin_check'?'临界窗口 · 需对齐':a.state==='file_padding_over_budget'?'文件余白超窗 · 待试听修剪':'发声可放入预算 · 待听审';let extra=`<div class="returned-audio"><strong class="${a.state==='within_budget_pending_listening'?'fit':'warn'}">${esc(status)}</strong><audio controls preload="none" src="${url(a.path)}" aria-label="${esc(roleName(c.speaker))}：${esc(c.text)}"></audio><p class="audio-proof">文件 ${dt(a.file_seconds)} 秒 · 回交能量估计 ${dt(a.speech_seconds)} 秒 · 原预算 ${dt(a.budget_seconds)} 秒<br>${esc(a.note)}</p><p class="audio-proof">${esc(a.master)} · 文件到齐不等于逐字听审通过</p>${ref?`<details><summary>对照本句画面</summary><img loading="lazy" src="${url(ref.path)}" alt="${esc(row.title)}"><p>${esc(row.action)}</p></details>`:''}</div>`;return card.replace(/<\/article>$/,extra+'</article>');};
document.querySelector('header').insertAdjacentHTML('beforeend',`<p class="notice issue">收尾审查：61条日语音频已到齐；配音超窗、连续咏唱插空和原曲卡点尚未验收。<a href="${url('后期/收尾审查-v001/收尾审查与交接.md')}">查看收尾结论与下一步</a>。两处时间字幕由后期叠加：208.5秒「少し前」、411.5秒「数日後」，各2秒。</p>`);
render();
</script>'''
    extra=extra.replace("return card.replace(/<\\/article>$/,extra+'</article>');", "return card.slice(0,card.lastIndexOf('</article>'))+extra+'</article>';")
    page=page.replace('</body>',extra+'</body>') if '</body>' in page else page+extra
    p.write_text(page,encoding='utf-8')

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    enrich(root,root/'视频制作/生成板-v011')
