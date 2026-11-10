"""Expose an adopted story insertion without inventing audio or final timing."""
import hashlib,html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    path=ROOT/'镜头设计/王宫内心戏-已采用增补-v001.json'
    d=json.loads(path.read_text(encoding='utf-8'))
    story=(ROOT/d['story_source']).read_text(encoding='utf-8')
    assert hashlib.sha256((ROOT/d['story_source']).read_bytes()).hexdigest()==d['story_source_sha256']
    for c in d['cues']:assert story.count(c['source_text'])==1 and c['audio_path'] is None
    assert story.count('那我自己去。')==1
    esc=html.escape
    cards=''.join(f'<article><h2>{esc(c["speaker"])}</h2><p class="line">{esc(c["source_text"])}</p><p>{esc(c["delivery"])}</p><p class="tag">日语译配草案 · 未录音</p><p lang="ja">{esc(c["ja_draft"])}</p></article>' for c in d['cues'])
    page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>白米饭 · 王宫内心戏已采用增补</title><style>body{max-width:1000px;margin:32px auto;padding:24px;background:#151b26;color:#eee8dc;font:17px/1.8 system-ui}a{color:#b1dbea}h1{font-size:30px}h2{font-size:21px}article{padding:20px 26px;margin:20px 0;background:#202a38;border-left:4px solid #d8c49c;border-radius:10px}.line{font-size:24px}.note{padding:16px;background:#353027;border-radius:8px}.tag{color:#ddc09e;font-size:14px}li{margin:8px 0}nav{display:flex;gap:24px;flex-wrap:wrap}</style>
<nav><a href="../../00_打开项目.html">项目首页</a><a href="../生成板-v012/生成板.html#GB004">完整生成板基线 · 修订前</a><a href="../../后期/收尾修复-v001/全片声音预览.html#t=49">原声音预览 · 尚无新内心戏</a></nav>
<h1>王宫内心戏 · 已采用</h1><p>小鱼「可是……她会死的」 → GPT内心争执 → 小鱼「那我自己去」打断 → 转身离开 → 搓手迟疑、起身目送。</p>
<p class="note">中文剧情与两句台词已确认，两套大头娃娃四视图已采用；三张表演状态图已生成待审阅。新增两句尚无音频，全片计划63句，已有61句配音。原450.9秒／40批基线暂不包含本段。以下为局部静帧设计，尚未生成视频；待新日语配音实测后重排15秒批次与音乐。</p>'''
    page+=cards
    states=d.get('state_sequence',[])
    cues={c['id']:c for c in d['cues']}
    if states:
        page+='<h2>内心戏 · 连续状态试看</h2><p>同一个镜头的三个表演状态，并非必须切成三镜。轮看每图停留3秒，仅方便看图，不是配音时长或正式剪辑节奏。</p><div id="state-buttons" style="display:flex;gap:8px;flex-wrap:wrap">'
        for i,s in enumerate(states):
            assert (ROOT/s['path']).is_file() and s['offset_seconds'] is None
            page+=f'<button type="button" onclick="showState({i})">{i+1} · {esc(s["label"])}</button>'
        page+='<button type="button" id="cycle" onclick="toggleCycle()">自动轮看</button></div><figure style="margin:16px 0"><img id="state-image" style="width:100%;border-radius:12px" alt="内心戏状态图"><figcaption id="state-caption" aria-live="polite"></figcaption></figure>'
        previews=[]
        for s in states:
            c=cues.get(s['cue_id'])
            previews.append({'src':'../../'+s['path'],'caption':s['label']+' · '+s['action']+'\n'+(c['speaker']+'：'+c['ja_draft']+'（译配草案）' if c else '两只分身闭口，等待本体回答。')})
        payload=json.dumps(previews,ensure_ascii=False).replace('<','\\u003c')
        page+='<style>button{background:#34445a;color:#fff;border:1px solid #69809c;border-radius:7px;padding:9px 14px;cursor:pointer}button[aria-pressed="true"]{background:#6b4357}figcaption{white-space:pre-line;padding:12px;background:#202a38}pre{white-space:pre-wrap}</style><script>const states='+payload+';let index=0,timer=null;function showState(i){index=i;document.getElementById("state-image").src=states[i].src;document.getElementById("state-caption").textContent=states[i].caption;document.querySelectorAll("#state-buttons button:not(#cycle)").forEach((b,j)=>b.setAttribute("aria-pressed",String(i===j)));}function toggleCycle(){if(timer){clearInterval(timer);timer=null;}else{timer=setInterval(()=>showState((index+1)%states.length),3000);}document.getElementById("cycle").textContent=timer?"停止轮看":"自动轮看";}showState(0);</script>'
        page+='<h2>动作与衔接</h2>'
        for label,key in [('这段要表达什么','purpose'),('机位与运动','camera'),('进入内心戏','entry'),('回到现实','exit'),('时间范围','timing'),('背景定格实施','background_execution')]:
            page+='<p><strong>'+label+'：</strong>'+esc(d['shot_design'][key])+'</p>'
        for s in states:
            page+='<article><h2>图片'+str(s['picture_number'])+' · '+esc(s['label'])+'</h2><p class="tag">'+esc(s['role'])+' · '+esc(s['status'])+'</p><p><strong>时间锚点：</strong>'+esc(s['event_anchor'])+'；秒数待新配音实测。</p><p>'+esc(s['action'])+'</p><p><strong>接下一状态：</strong>'+esc(s['transition'])+'</p></article>'
        page+='<h2>本段参考图片顺序</h2><p>以下编号供本段审阅与后续编排。尚未上传或绑定模型；正式合批时按入口容量核实，不把六张图片默认都塞进同一任务。</p>'
        for ref in d['reference_images']:
            assert (ROOT/ref['path']).is_file()
            page+='<details><summary>图片'+str(ref['number'])+' · '+esc(ref['label'])+' — '+esc(ref['role'])+'</summary><a href="../../'+esc(ref['path'])+'"><img loading="lazy" style="width:100%" src="../../'+esc(ref['path'])+'" alt="'+esc(ref['label'])+'"></a></details>'
        page+='<h2>角色采用记录</h2>'
    for a in d.get('candidate_assets',[]):
        assert (ROOT/a['path']).is_file()
        page+='<h2>'+esc(a['label'])+'</h2><a href="../../'+esc(a['path'])+'"><img style="width:100%;border-radius:10px" src="../../'+esc(a['path'])+'" alt="'+esc(a['label'])+'"></a><p>'+esc(a['status'])+'</p>'
    page+='<h2>画面与衔接</h2><p>'+esc(d['visual'])+'</p><p>'+esc(d['transition'])+'</p><p>两只分身都不获胜，GPT未表态；不新增“好闺蜜”关系。小鱼打断句复用现有完整原声，只说一次。</p>'
    page+='<h2>素材进度与声音安排</h2><ul>'+''.join('<li>'+esc(x)+'</li>' for x in d['asset_requirements'])+'</ul><p>'+esc(d['timing_policy'])+'</p><p>'+esc(d['music_policy'])+'</p><p>不上传配音或BGM。模型口播使用复核后的日语，后期替换声音并检查口型；此页中文仅为原意与制作说明。</p>'
    page+='<p><a href="../../'+d['story_source']+'">采用后的完整场景剧本</a> · <a href="../../镜头设计/王宫内心戏-已采用增补-v001.json">增补来源与配音需求</a></p></html>'
    out=ROOT/'视频制作/生成板-v013';out.mkdir(exist_ok=True)
    (out/'生成板.html').write_text(page,encoding='utf-8')
    record={'status':d['status'],'story_source':d['story_source'],'story_sha256':d['story_source_sha256'],'insertion_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'new_lines':2,'existing_returned_lines':61,'planned_lines':63,'duration_locked':False,'baseline_unchanged':True,'state_images':len(states),'video_generated':False}
    (out/'增补核验.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(record,ensure_ascii=False))
if __name__=='__main__':main()
