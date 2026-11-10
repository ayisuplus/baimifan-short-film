"""Build the repaired static-frame / actual mixed-audio preview (stdlib only)."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from urllib.parse import quote


def build(root: Path) -> dict:
    output = root / '后期/收尾修复-v001/全片声音预览.html'
    sources = {
        'shots': '镜头设计/shot-plan-v0.57.json',
        'voice': '后期/收尾修复-v001/配音对位方案.json',
        'music': '后期/收尾修复-v001/实际BGM剪辑.json',
        'mapping': '视频制作/生成板-v012/日语音频映射.json',
        'review': '视频制作/生成板-v012/对白复核.json',
    }
    data = {k: json.loads((root / p).read_text(encoding='utf-8-sig')) for k, p in sources.items()}
    audio = root / '后期/收尾修复-v001/全片声音预览.mp3'
    if not audio.is_file():
        raise ValueError(f'Missing audio: {audio}')
    import os
    def url(path: Path) -> str:
        return quote(os.path.relpath(path, output.parent).replace('\\', '/'), safe='/')
    timings = {s['shot_id']: s for s in data['voice']['shots']}
    shots = []
    previous = 0.0
    for s in data['shots']['shots']:
        start, end = float(s['start_second']), float(s['end_second'])
        if not math.isclose(start, previous, abs_tol=0.001) or end <= start:
            raise ValueError(f'Non-contiguous shot: {s["id"]}')
        timing = timings[s['id']]
        if abs(timing['new_start'] - start) > .001 or abs(timing['new_end'] - end) > .001:
            raise ValueError(f'Voice/shot timing mismatch: {s["id"]}')
        path = root / s['presentation']['path']
        if not path.is_file():
            raise ValueError(f'Missing presentation image: {path}')
        shots.append(dict(id=s['id'], title=s['title'], start=start, end=end, image=url(path),
                          action=s['action'], camera=s.get('camera', s.get('framing', '')),
                          sfx=s.get('sound', ''), source_path=s['presentation']['path']))
        previous = end
    duration = previous
    if abs(duration - data['music']['film_seconds']) > .001:
        raise ValueError('Music timeline length does not match shots')
    mapping = {c['cue_id']: c for c in data['mapping']['cues']}
    review = {(c['batch_id'], c['cue_index']): c for c in data['review']['cues']}
    cues = []
    for c in data['voice']['cues']:
        m = mapping[c['id']]
        r = review[(m['batch_id'], m['cue_index'])]
        if r['shot_id'] != c['shot_id'] or r['current_text'] != c['text_ja']:
            raise ValueError(f'Dialogue text mismatch: {c["id"]}')
        if not r['source_text'].strip():
            raise ValueError(f'Missing Chinese text: {c["id"]}')
        if not (0 <= c['timeline_start'] < c['timeline_end'] <= duration + .001):
            raise ValueError(f'Invalid dialogue time: {c["id"]}')
        cues.append(dict(id=c['id'], role=c['role'], ja=c['text_ja'], zh=r['source_text'],
                         start=c['timeline_start'], end=c['timeline_end'], shot=c['shot_id'],
                         estimated=bool(c.get('estimated_word_boundaries')),
                         offscreen=bool(c.get('cross_shot_offscreen'))))
    if len(cues) != len(mapping):
        raise ValueError('Voice cues do not cover the audio mapping')
    shot_map = {s['id']: s for s in shots}
    anchors = [('Kimi · 月光显形', 'CY024R'), ('GPT · 展翼起咏', 'CY024A'),
               ('父亲呼唤 · 沉默', 'CY029'), ('结尾 · 再次递饭', 'CY031')]
    payload = dict(title='白米饭 · 全片声音预览', duration=duration, audio=url(audio), shots=shots, cues=cues,
                   music=data['music']['cues'], silences=data['music']['silences'],
                   anchors=[dict(label=label, time=shot_map[sid]['start'], shot=sid) for label, sid in anchors],
                   sources={p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in sources.values()},
                   validation=dict(shots=len(shots), images=len(shots), cues=len(cues),
                                   japanese_and_chinese=len(cues), music_cues=len(data['music']['cues']),
                                   silences=len(data['music']['silences']), duration=duration))
    encoded = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    page = HTML.replace('__PAYLOAD__', encoded)
    output.write_text(page, encoding='utf-8')
    return dict(output=str(output), **payload['validation'])


HTML = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>白米饭 · 全片声音预览</title><style>
:root{color-scheme:dark;font-family:Inter,"Microsoft YaHei",sans-serif;background:#10151e;color:#e9edf3}*{box-sizing:border-box}body{margin:0}main{max-width:1380px;margin:auto;padding:20px}header{display:flex;align-items:baseline;gap:18px;flex-wrap:wrap}h1{font-size:25px;margin:0 0 6px}p{line-height:1.6}.muted{color:#aab6c5;font-size:13px}.pill{font-size:12px;border:1px solid #486074;border-radius:20px;padding:5px 12px;color:#9bd2d3}.layout{display:grid;grid-template-columns:minmax(0,1fr) 310px;gap:20px;margin-top:18px}.screen{background:#070a10;border:1px solid #283343;border-radius:12px;overflow:hidden}.frame{position:relative;aspect-ratio:16/9;display:flex;align-items:center;justify-content:center}.frame img{width:100%;height:100%;object-fit:contain}.static{position:absolute;top:12px;left:12px;background:#09121dd9;padding:5px 10px;border-radius:5px;color:#d3e0ec;font-size:12px}.subs{min-height:118px;padding:16px 22px;background:#161e2a;border-top:1px solid #283343}.jp{font-size:22px;line-height:1.55;margin:3px 0}.cn{font-size:15px;color:#aebfd2;line-height:1.6}.speaker{color:#eacb8b;font-size:12px}.subitem+.subitem{margin-top:12px}.controls{padding:14px 0}audio{display:none}.row{display:flex;gap:9px;align-items:center;flex-wrap:wrap}button,select{font:inherit;background:#222e3e;border:1px solid #405067;border-radius:7px;color:inherit;padding:8px 12px;cursor:pointer}button:hover{background:#33465c}button.primary{background:#426d6f;border-color:#5d9a9d}button:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid #f2d39c;outline-offset:3px}input[type=range]{width:100%;accent-color:#9bd2d3;margin:14px 0 5px}.time{font-variant-numeric:tabular-nums;color:#c6d3e3;font-size:13px;white-space:nowrap}.grow{flex:1}.box{background:#18212d;border:1px solid #2c394a;border-radius:10px;padding:16px;margin-bottom:12px}.label{color:#8fa7bd;font-size:12px;margin-bottom:8px}.shotname{font-size:18px;line-height:1.5}.detail{font-size:14px;line-height:1.75;white-space:pre-line}.music{color:#a7ded2}.warning{color:#f0c797}#chapter{width:100%;max-width:100%;font-size:13px}details{margin-top:14px;color:#aab6c5;font-size:12px}summary{cursor:pointer}#error{color:#ffadad;margin:8px 0}.footer{margin-top:12px;font-size:12px;color:#7e91a6;line-height:1.7}@media(max-width:900px){main{padding:14px}.layout{grid-template-columns:1fr}aside{display:grid;grid-template-columns:1fr 1fr;gap:12px}.box{margin:0}.jp{font-size:19px}}@media(max-width:560px){aside{display:block}.box{margin-bottom:12px}.jp{font-size:17px}.subs{padding:12px;min-height:105px}h1{font-size:21px}}
</style></head><body><main>
<header><h1>白米饭 · 全片声音预览</h1><span class="pill">静帧 + 日语配音 + BGM</span></header>
<div class="muted">跟随实际混音时间切换静帧，用于检查叙事、对白与音乐节奏。尚非动态成片；声音候选待试听。</div>
<div class="layout"><section><div class="screen"><div class="frame"><img id="picture" alt="当前镜头静帧"><span class="static">静帧预演 · 非动态视频</span></div><div id="subs" class="subs" aria-live="off"></div></div>
<div class="controls"><audio id="audio" preload="metadata"></audio><div class="row"><button id="play" class="primary">▶ 播放</button><button id="prev" title="上一镜（←）">← 上一镜</button><button id="next" title="下一镜（→）">下一镜 →</button><span class="grow"></span><span id="time" class="time"></span></div><input id="seek" type="range" min="0" step="0.01" value="0" aria-label="播放进度"><div id="anchors" class="row"></div><div id="error" role="status"></div></div>
<div class="footer">空格播放 / 暂停，左右键切镜。链接中的 #t=秒 可保存试听位置。字幕使用配音对位时间；连续咏唱的句界是估算定位，不代表逐词识别验收。</div>
</section><aside><div class="box"><div class="label" id="shotlabel">当前镜头</div><div id="shotname" class="shotname"></div><p id="action" class="detail"></p><div id="camera" class="muted"></div><p><select id="chapter" aria-label="选择镜头"></select></p></div>
<div class="box"><div class="label">当前声音安排</div><div id="music" class="detail music"></div><p id="musicnote" class="muted"></p><div class="warning detail">音效 / 环境声尚未制作</div><p id="sfx" class="muted"></p></div>
<div class="box"><div class="label">预览覆盖</div><div id="coverage" class="detail"></div><details><summary>数据来源与校验</summary><p id="sources" class="detail"></p></details></div></aside></div>
</main><script id="data" type="application/json">__PAYLOAD__</script><script>
'use strict';
const D=JSON.parse(document.getElementById('data').textContent), $=id=>document.getElementById(id), A=$('audio');
const fmt=t=>`${Math.floor(t/60).toString().padStart(2,'0')}:${(t%60).toFixed(1).padStart(4,'0')}`;
let index=-1,lastCue='',lastMusic='',raf=0;
A.src=D.audio;$('seek').max=D.duration;
$('coverage').textContent=`${D.validation.shots} 镜 · ${D.validation.cues} 句日语对白\n${D.validation.music_cues} 段 BGM · 总长 ${fmt(D.duration)}\n全部静帧、日中台词与配音时间已关联。`;
$('sources').textContent=Object.entries(D.sources).map(([p,h])=>`${p}\nSHA256 ${h}`).join('\n\n');
for(const s of D.shots){const o=document.createElement('option');o.value=s.start;o.textContent=`${fmt(s.start)} · ${s.id} ${s.title}`;$('chapter').append(o);}
for(const k of D.anchors){const b=document.createElement('button');b.textContent=k.label;b.onclick=()=>seek(k.time);$('anchors').append(b);}
function hashTime(){const m=location.hash.match(/^#t=(\d+(?:\.\d+)?)/);return m?Number(m[1]):0;}
function setHash(t){history.replaceState(null,'',`#t=${t.toFixed(2)}`);}
function seek(t){t=Math.max(0,Math.min(D.duration,t));A.currentTime=t;render(t);setHash(t);}
function node(tag,cls,text){const e=document.createElement(tag);e.className=cls;e.textContent=text;return e;}
function render(t=A.currentTime){
 let ni=D.shots.findIndex(s=>t>=s.start&&t<s.end);if(ni<0)ni=D.shots.length-1;
 if(ni!==index){index=ni;const s=D.shots[index];$('picture').src=s.image;$('picture').alt=`${s.id} ${s.title} · 静帧`;$('shotlabel').textContent=`当前镜头 ${index+1}/${D.shots.length} · ${s.id} · ${fmt(s.start)}—${fmt(s.end)}`;$('shotname').textContent=s.title;$('action').textContent=s.action;$('camera').textContent=s.camera;$('sfx').textContent=`待制作的设计：${s.sfx||'以镜头声音设计为准。'}`;$('chapter').value=String(s.start);if(D.shots[index+1]){const preload=new Image();preload.src=D.shots[index+1].image;}}
 $('seek').value=t;$('time').textContent=`${fmt(t)} / ${fmt(D.duration)}`;
 const active=D.cues.filter(c=>t>=c.start&&t<c.end), key=active.map(c=>c.id).join('|');
 if(key!==lastCue||!$('subs').childNodes.length){lastCue=key;$('subs').replaceChildren();if(!active.length){$('subs').append(node('div','muted','此刻无对白 · 留意画面与声音的呼吸'));}for(const c of active){const div=node('div','subitem','');div.append(node('div','speaker',`${c.role}${c.offscreen?' · 跨镜画外声':''}${c.estimated?' · 句界估算':''}`),node('div','jp',c.ja),node('div','cn',c.zh));$('subs').append(div);}}
 const music=D.music.filter(c=>t>=c.timeline_start&&t<c.timeline_end), silent=D.silences.find(c=>t>=c.timeline_start&&t<c.timeline_end), mk=music.map(c=>c.id).join('|')+'|'+(silent?.id||'');
 if(mk!==lastMusic||!$('music').textContent){lastMusic=mk;$('music').textContent=music.length?music.map(c=>`♫ ${c.music_id}\n${fmt(c.timeline_start)}—${fmt(c.timeline_end)}`).join('\n'):'停乐 · 无 BGM';$('musicnote').textContent=music.length?music.map(c=>c.editorial_note).join('；'):(silent?.reason||'此段未铺音乐。');}
}
function loop(){render();if(!A.paused)raf=requestAnimationFrame(loop);}
$('play').onclick=()=>A.paused?A.play().catch(e=>{$('error').textContent=`无法播放：${e.message}`;}):A.pause();
A.addEventListener('play',()=>{$('play').textContent='❚❚ 暂停';cancelAnimationFrame(raf);loop();});
A.addEventListener('pause',()=>{$('play').textContent='▶ 播放';cancelAnimationFrame(raf);render();setHash(A.currentTime);});
A.addEventListener('timeupdate',()=>render());A.addEventListener('ended',()=>setHash(A.currentTime));
A.addEventListener('error',()=>{$('error').textContent='音频未能加载，请从项目预览服务打开此页面，并确认全片声音预览.mp3存在。';});
$('picture').addEventListener('error',()=>{$('error').textContent='当前镜头图片无法加载，请检查预览服务路径。';});
A.addEventListener('loadedmetadata',()=>{if(Math.abs(A.duration-D.duration)>.2)$('error').textContent=`音频时长 ${A.duration.toFixed(2)} 秒与计划 ${D.duration} 秒不符。`;seek(hashTime());},{once:true});
$('seek').addEventListener('input',e=>seek(Number(e.target.value)));$('chapter').onchange=e=>seek(Number(e.target.value));
$('prev').onclick=()=>seek(D.shots[Math.max(0,index-1)].start);$('next').onclick=()=>seek(D.shots[Math.min(D.shots.length-1,index+1)].start);
window.addEventListener('hashchange',()=>seek(hashTime()));window.addEventListener('keydown',e=>{if(/INPUT|SELECT|TEXTAREA|BUTTON/.test(e.target.tagName))return;if(e.code==='Space'){e.preventDefault();$('play').click();}if(e.code==='ArrowLeft'){e.preventDefault();$('prev').click();}if(e.code==='ArrowRight'){e.preventDefault();$('next').click();}});
render(Math.max(0,Math.min(D.duration,hashTime())));
</script></body></html>'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(build(args.root.resolve()), ensure_ascii=False, indent=2))
