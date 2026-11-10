from pathlib import Path
import json,hashlib,subprocess
import numpy as np,soundfile as sf
R=Path(__file__).resolve().parents[1];P=R/'视频制作/Metaso-H3-v014/执行队列.json';q=json.loads(P.read_text(encoding='utf8'));aid='CY024A-v014-caster-2d-sync-r1';assert not any(x['attempt_id']==aid for x in q['items'])
v=json.loads((R/'后期/对白字幕同步-v010/同步计划.json').read_text(encoding='utf8'))['lines'];out=np.zeros(7*48000,dtype=np.float32)
for id,start in [('VO-CY024A-01',4/24),('VO-CY024A2-01',58/24),('VO-CY024A5-02',128/24)]:
 x=next(x for x in v if x['id']==id);a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',x['file'],'-ar','48000','-ac','1','-f','f32le','pipe:1']),np.float32);i=round(start*48000);out[i:i+len(a)]=a
f='视频制作/Metaso-H3-v014/参考/caster-7s-selected-voices.wav';sf.write(R/f,out,48000,subtype='PCM_24');img='概念参考/04-ChatGPT-用户指定龙娘.png'
refs=[dict(path=img,sha256=hashlib.sha256((R/img).read_bytes()).hexdigest(),role='reference_image',visually_reviewed=True,purpose='作者GPT本体二维身份母本，禁止文字水印进入画面'),dict(path=f,sha256=hashlib.sha256((R/f).read_bytes()).hexdigest(),role='reference_audio',seconds=7,purpose='当前已选原速日语三句，按精确剪辑窗口拼接；生成声最终不入混音')]
q['items'].append(dict(attempt_id=aid,batch_number=26,batch_id='GB019',duration=7,estimated_credits=71.4,status='prepared',accepted=False,repair_of='B26 shiny-to-flat style discontinuity',change_reason='统一GPT起咏、聚水、术名三处近景为母本二维画风，原声原速口型参考',references=refs,prompt='''7秒精细日本二维动画，严格保持参考白发龙角女孩的脸、紫瞳、尖耳、白银纹胸衣与膜翼。可见细线稿与平涂阴影，不要3D、塑料皮肤、手办。只出现这一个GPT，她悬浮于冷蓝窗哥特教堂内，屋顶始终完好，没有水龙，没有破洞，没有教徒，嘴型同步音频，无字幕文字水印。全片同侧机位。
0至2.25秒：腰上中景，人物已经悬空稳定，缓慢抬起右掌到胸前，保持另一手安定；按音频说「清き水の主よ。」。一遍抬掌即可，不反复挥手。
2.25至5.25秒：同侧更近中景，右掌保持向上，身旁细小水珠缓缓上浮，按音频说「水よ、集え。」。水珠只有小量，不形成水龙或大浪，嘴在停顿中闭合。
5.25至7秒：同侧脸与肩近景，目光坚定朝向殿内右前方，按音频清楚说术名「蒼龍天傾！」，直到尾音结束，屋顶仍完整且身旁没有龙。不要提前前指发射，不要切到别场景。只用音频控制口型表演，不添加对白、旁白或背景音乐。'''))
assert sum(x['estimated_credits'] for x in q['items'])<q['spending_ceiling_credits'];P.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8');print('Prepared 7s caster; queue estimate',sum(x['estimated_credits'] for x in q['items']))
