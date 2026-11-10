"""Project adapter for explicit cross-shot speech and decimal timing.

Shared v2 renderer remains unchanged. Only two timing guards are generalized,
after validation against the project's complete natural-rate voice plan.
"""
import copy, hashlib, html, json, math, os, re
from pathlib import Path
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
SHARED=ROOT.parent.parent/'OpenCut/toolkit/plugins/film-studio/skills/generation-board/scripts/build_multiref_board.py'
OUT=ROOT/'视频制作/生成板-v014'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def write(p,d):(ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    plan=load(OUT/'批次计划.json');source=load(plan['source']);sm={s['id']:s for s in source['shots']}
    timing=load('后期/生成前修正-v014/配音对位方案.json');tc={c['id']:c for c in timing['cues']}
    edit=load('后期/生成前修正-v014/实际BGM剪辑.json')
    rhythm=load(OUT/'配乐卡点方案.json')
    for b in plan['batches']:
        for p in rhythm['batches'][b['id']]['points']:
            candidates=[x for x in edit['action_points'] if x.get('action_zh')==p['action_zh']]
            if len(candidates)==1:
                p['time']=round(candidates[0]['timeline_time']-sm[b['shot_ids'][0]]['start_second'],6)
    write(OUT/'配乐卡点方案.json',rhythm)
    for s in source['shots']:
        for c in s.get('subtitle_cues',[]):
            t=tc[c['cue_id']]
            assert abs(s['start_second']+c['offset']-t['timeline_start'])<1e-5
            assert abs(c['duration']-(t['timeline_end']-t['timeline_start']))<1e-5
            if c['offset']<0 or c['offset']+c['duration']>s['seconds']+.002:
                assert c['cross_shot_offscreen'] and len(c['visual_shots'])>1
                assert all(i in sm for i in c['visual_shots'])
    text=SHARED.read_text(encoding='utf-8')
    replacements={
        "s['start_second']==elapsed":"abs(s['start_second']-elapsed)<1e-6",
        "s['end_second']==elapsed":"abs(s['end_second']-elapsed)<1e-6",
        "elapsed==data['total_seconds']":"abs(elapsed-data['total_seconds'])<1e-6",
        "used<=15 and":"used<=15.000001 and",
        "c['offset']>=0 and end<=used+0.002":"lo+c['offset']>=-0.002 and end<=used+0.002",
        "c['offset']+c['duration']<=s['seconds']+0.002":"c.get('cross_shot_offscreen',False) or c['offset']+c['duration']<=s['seconds']+0.002",
        "off='画外' in c['speaker']":"off=c.get('cross_shot_offscreen',False) or '画外' in c['speaker']",
    }
    for old,new in replacements.items():
        assert text.count(old)==1,('Shared renderer changed; review adapter',old)
        text=text.replace(old,new)
    ns={'__file__':str(SHARED),'__name__':'project_repaired_compiler'}
    exec(compile(text,str(SHARED),'exec'),ns)
    board=ns['compile_board'](ROOT,plan)
    from generation_v014_prompts import repair_board
    repair_board(board,plan)
    board['film_seconds']=source['total_seconds']
    audio=load(OUT/'日语音频映射.json');am={(a['batch_id'],a['cue_index']):a for a in audio['cues']}
    edit=load('后期/生成前修正-v014/实际BGM剪辑.json')
    for b in board['batches']:
        b['used_seconds']=round(b['used_seconds'],6);b['handle_seconds']=round(15-b['used_seconds'],6);b['film_end']=round(b['film_end'],6)
        for i,c in enumerate(b['dialogue']):
            a=am[b['id'],i];c['returned_audio']=a
            assert abs(b['film_start']+c['start']-a['timeline_start'])<1e-5
        for p in b['rhythm']['points']:
            # Use the BGM script's explicit action anchors, not proportional beat guesses.
            candidates=[x for x in edit['action_points'] if x.get('action_zh')==p['action_zh']]
            if len(candidates)==1:p['film_time']=candidates[0]['timeline_time'];p['time']=round(p['film_time']-b['film_start'],6)
            assert 0<=p['time']<b['used_seconds']+.001,(b['id'],p)
            cue=next((m for m in edit['cues'] if m['timeline_start']<=p['film_time']<m['timeline_end']),None)
            p['source_seconds']=round(cue['source_in']+p['film_time']-cue['timeline_start'],5) if cue else None
            p['music_id']=cue['music_id'] if cue else None
            if p['action_zh']=='结印镜中咏唱暂停':p['music_intent']='本镜5.74–6.54秒收声留白0.8秒，后期保留水流'
            if '10.2秒咏唱' in p['music_intent']:p['music_intent']=p['music_intent'].replace('10.2秒咏唱',f"{tc['VO-CY024A-01']['timeline_start']-b['film_start']:.2f}秒咏唱")
            if '7.3秒呼唤' in p['music_intent']:p['music_intent']=p['music_intent'].replace('7.3秒呼唤',f"{tc['VO-CY029-01']['timeline_start']-b['film_start']:.2f}秒呼唤")
            suffix='；'+('原曲已落入实际试听时间线，乐句待听审。' if cue else '此处明确停乐，用拟音承担动作。')
            if suffix not in p['music_intent']:p['music_intent']+=suffix
        for name,model in b['models'].items():
            model['issues']=[x for x in model['issues'] if '当前对白时间沿用预演预算' not in x and '原曲剪入/剪出和乐句重拍尚未' not in x]
            model['issues']+=['自然原声与镜头时间已对位；逐字听审和动态口型未验收。','BGM已制作实际剪辑试听；乐句与情绪落点待听审。']
            model['capacity_ok']=len(b['references'])<=model['max_images'] and model['chars']<=plan['model_contracts'][name].get('max_chars',10**9)
        b['selected_model']='minimax-h3' if b['models']['minimax-h3']['capacity_ok'] else 'seedance25'
        assert b['models'][b['selected_model']]['capacity_ok']
        b['selection_reason']='完整参考与提示词符合2026-10-26实时接口2000字符/9图限制；提交前重新确认接口。' if b['selected_model']=='minimax-h3' else 'H3图数或字符超限，采用已有Seedance模板，完整保留身份及构图参考。'
    board['actual_bgm_edit']='后期/生成前修正-v014/实际BGM剪辑.json'
    board['post_captions']=[{'shot_id':sid,'start':sm[sid]['start_second'],'end':sm[sid]['start_second']+2,'ja':ja} for sid,ja in [('CY026A','少し前'),('CY031','数日後')]]
    write(OUT/'展开数据.json',board)
    sound_items=[dict(shot_id=r['id'],film_start=r['film_start'],film_end=r['film_end'],required_sound=r['effects'],execution='按生成提示词制作环境、动作及非词声；替换对白时保留或后期补回。',status='specified_not_rendered') for b in board['batches'] for r in b['rows']]
    write('后期/生成前修正-v014/非语言声音执行.json',dict(scope='133镜同源声音要求，非新增对白清单；尚无音效成品。',items=sound_items))
    # The persisted rhythm data uses the same resolved clocks as the visible board.
    rhythm=load(OUT/'配乐卡点方案.json')
    for b in board['batches']:rhythm['batches'][b['id']]=b['rhythm']
    write(OUT/'配乐卡点方案.json',rhythm)
    board['review_hashes']['视频制作/生成板-v014/配乐卡点方案.json']=hashlib.sha256((OUT/'配乐卡点方案.json').read_bytes()).hexdigest()
    write(OUT/'展开数据.json',board)
    (OUT/'提示词').mkdir(exist_ok=True)
    for b in board['batches']:
        for name,prompt in b['prompts'].items():(OUT/'提示词'/f"{b['id']}-{name}.txt").write_text(prompt.rstrip()+'\n',encoding='utf-8')
    template=(SHARED.parent.parent/'assets/board-multiref.html').read_text(encoding='utf-8')
    prefix='../../'
    # Project copy: explicit model choice, real audio, actual music source ranges.
    template=template.replace("let b=D.batches[index];document.querySelector('#main')","let b=D.batches[index];model=b.selected_model;document.querySelector('#main')")
    template=template.replace('${D.request_seconds-D.film_seconds}','${n(D.request_seconds-D.film_seconds)}')
    template=template.replace('译配措辞仍是草案；时间为表演预算，未做声音或口型实测。','台词按回交日语原稿，时间按自然原声重新对位；发音、表演和动态口型仍待听审。')
    template=template.replace('动作时间目标已规划；原曲区间与音乐重拍待听审对齐。这里的秒数不是已检测或已锁定的音乐节拍。','原曲区间已实际剪入试听版；原曲秒数可追溯。瞬态测量只是候选，乐句与情绪卡点仍需试听。')
    template=template.replace("p.source_seconds==null?'待乐句对齐':n(p.source_seconds)","p.source_seconds==null?'停乐 · 拟音落点':esc(musicLabel(p.music_id))+' · '+n(p.source_seconds)+'秒'")
    template=template.replace('原曲剪入/剪出待精剪。','曲目归属参考；实际进出与停乐以配乐卡点表和声音预览为准。')
    template=template.replace('当前H3稿须重组参考输入后方可提交；Seedance稿保留这组完整参考。','本批已选Seedance模板保留完整参考；H3稿仅作对照，不用于本批提交。')
    template=template.replace('<h2>完整提示词</h2>','<h2>完整提示词</h2><p class="notice">本批安排：${b.selected_model===\'seedance25\'?\'Seedance 2.5\':\'MiniMax H3\'}。${esc(b.selection_reason)}</p>')
    template=template.replace("function update(){let m=b.models[model];", "function update(){let m=b.models[model];document.querySelector('#copy').disabled=!m.capacity_ok;document.querySelector('#download').hidden=!m.capacity_ok;")
    template=template.replace("document.querySelector('#copy').onclick=async()=>{try{", "document.querySelector('#copy').onclick=async()=>{if(!b.models[model].capacity_ok)return;try{")
    template=template.replace('复制提示词草案','复制本批可用提示词')
    page=template.replace('__DATA__',json.dumps(board,ensure_ascii=False).replace('<','\\u003c')).replace('__ROOT__',prefix)
    for key in ['home','previs','review']:page=page.replace('__'+key.upper()+'__',html.escape(prefix+quote(plan['navigation'][key],safe='/#')))
    extra='''<script>
const beforeAudioCard=dialogueCard;
dialogueCard=function(b,c,i){let card=beforeAudioCard(b,c,i),a=c.returned_audio;return card.slice(0,card.lastIndexOf('</article>'))+`<audio controls preload="none" style="width:100%" aria-label="${esc(roleName(c.speaker))}：${esc(c.text)}" src="${url(a.path)}"></audio><p class="muted">完整文件 ${dt(a.file_seconds)} 秒 · 原速对位 ${dt(a.budget_seconds)} 秒。${esc(a.note)}<a href="${url('后期/生成前修正-v014/全片声音预览.html')}#t=${b.film_start+c.start}">连同画面试听本句</a></p></article>`;};
document.querySelector('header').insertAdjacentHTML('beforeend',`<p class="notice">已按自然原声修复时间，共63句。<a href="${url('后期/生成前修正-v014/全片声音预览.html')}">打开全片声音与画面预览</a>。后期日语时间字幕：${D.post_captions.map(c=>dt(c.start)+'秒「'+c.ja+'」').join('、')}，各2秒。</p>`);render();
</script>'''
    page=page.replace('</body>',extra+'</body>')
    (OUT/'生成板.html').write_text(page,encoding='utf-8')
    stats=dict(shots=len(sm),batches=len(board['batches']),cues=len(audio['cues']),film_seconds=source['total_seconds'],all_selected_models_fit=True,seedance_batches=[b['id'] for b in board['batches'] if b['selected_model']=='seedance25'],h3_unsupported_batches=[b['id'] for b in board['batches'] if not b['models']['minimax-h3']['capacity_ok']],scope='结构与时间验证；修正候选视听审阅与动态口型仍为单独验收项')
    write(OUT/'结构核验.json',stats);print(json.dumps(stats,ensure_ascii=False))

if __name__=='__main__':main()
