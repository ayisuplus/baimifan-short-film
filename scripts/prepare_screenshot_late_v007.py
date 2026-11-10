"""Prepare only the three late screenshot pickup drafts; never submit or alter queue.

Default writes the JSON draft only. --materialize creates its frozen local image
and padded selected-audio references, hashes them and updates the same draft.
No API access, Resolve calls, video export, voice synthesis or queue mutation.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '后期/截图定点修正-v004/后段补拍草案.json'
REF = ROOT / '视频制作/Metaso-H3-v007/参考'
PLAN = json.loads((ROOT / '后期/导演重构-v003/后期执行计划.json').read_text(encoding='utf8'))
VOICES = {v['id']: v for v in PLAN['voice']}

def rel(path):
    return str(Path(path).relative_to(ROOT)).replace('\\', '/')

def source(batch):
    return next(s['source'] for s in PLAN['edl'] if s['batch'] == batch)

def image_spec(name, batch, second, purpose):
    return dict(path=rel(REF / (name + '.png')), role='reference_image',
                source=source(batch), source_second=second, purpose=purpose,
                reviewed_evidence=f'后期/截图定点修正-v004/证据/late-B{batch}-actualsource-2fps.jpg')

def audio_spec(name, duration, parts):
    return dict(path=rel(REF / (name + '.wav')), role='reference_audio', seconds=duration,
                purpose='作者原选工作声音；只添加静音，不变速、不换音色、不重新合成',
                parts=[dict(id=vid, offset_seconds=offset, source=VOICES[vid]['path'],
                            speaker=VOICES[vid]['role'], zh=VOICES[vid]['zh'], ja=VOICES[vid]['ja'])
                       for vid, offset in parts])

STYLE = ('严格继承Image1原片高细节二次元三维渲染与精细插画融合质感：细密发丝、柔和皮肤体积、'
         '原有蕾丝刺绣和衣料厚度、真实空间景深、冷蓝窗光与克制暖光。不改成平涂赛璐璐、粗线漫画，'
         '不改变脸型、年龄、衣服、饰品、武器或翅膀。优化构图和表演，不另换美术风格。')

def make_items():
    specs = [
        dict(attempt_id='GB014-v007-group-entry-style-audio-r1', batch_number=17, batch_id='GB014', duration=5,
             timeline_replace_frames=[4778,4838], use_candidate_frames=[24,84],
             references=[image_spec('late-B17-group-original',17,2.5,'群像身份、服装、持物、门口环境及原片渲染基准'),
                         audio_spec('late-B17-GPT-selected',5,[('VO-CY024-01',1+8/24)])],
             prompt=STYLE+'\n5秒连续门口入场，门已经破开，不再开门或踹门。保持Image1全部既定人物身份和武器，不增删换装。'
             '摄影机仍在殿内看门口、低位微偏侧，门边破木作前景，GPT在队伍前方，伙伴形成前中后三层而非横排摆拍。'
             '前1秒准备和视线确认；1至3.5秒必须是一段完整可独立剪用的入场和命令：GPT向殿内迈半步，目光看向受困者方向，'
             '伙伴向两翼警戒。只有中央白发双角GPT说Audio1中的二人を守って，声音从1.333333秒起、真实发声以音频为准；其他人嘴闭。'
             '说完闭唇，3.5至5秒保持同一受威胁方向的警戒供剪辑余量。命令要短促坚决、不微笑、不看摄影机。'
             '动作正常速度、腿脚受力真实，不慢动作、不整齐走秀、不新增台词或音乐，不切镜。'),
        dict(attempt_id='GB014A-v007-kimi-window-style-audio-r1', batch_number=18, batch_id='GB014A', duration=9,
             timeline_replace_frames=[5018,5229], use_candidate_frames=[0,211],
             references=[image_spec('late-B18-kimi-original',18,4.5,'Kimi原片身份、服装、明暗双刃左右手与侧面窗位置'),
                         image_spec('late-B18-window-space',18,3.5,'只用于窗外位置、窗框比例和面朝玻璃的空间关系，不重复凝形'),
                         audio_spec('late-B18-Kimi-selected',9,[('VO-CY024K0-01',0),('VO-CY024K0-02',89/24)])],
             prompt=STYLE+'\n9秒Kimi窗外请门和甩刃。承接她已经在教堂正后中央高窗外凝实，人物朝向同一玻璃，'
             '镜头在她窗外侧后方看三分之二侧脸，窗棂保留在画面右缘。左手明刃抬肩旁，右手暗刃低持，绝不左右互换。'
             'Audio1是Kimi唯一台词与口型基准，从0秒播放。0秒开始请循此刃的银辉，3.708333秒起为我开启通往彼端的门扉，'
             '完整日语原声及真实停顿以Audio1为准，不另读中文，不添加第一句或月影渡。嘴部只在实际发声时运动。'
             '0至4秒侧脸与明刃近景，轻收近但保留肩和手；4至7.7秒摄影机同侧滑向肩后，越刀锋清楚看到完整窗棂和内侧目标，'
             'Kimi不转身面对摄影机，仍坚定朝玻璃请求。约7.7秒音频结束后留短半拍，8.0至8.7秒肩带肘向右前方发力甩出左手明刃。'
             '明刃出画，人物留窗外；8.79秒前出手动作已经完成并留余量。下一镜从窗内看破窗，当前镜不提前破碎、不本人穿窗、'
             '不瞬移、不加护罩。头发同方向飘、动作有惯性，避免站姿悬停只动嘴。禁新增人声、BGM、字幕。'),
        dict(attempt_id='GB018-v007-gpt-rise-style-audio-r1', batch_number=25, batch_id='GB018', duration=8,
             timeline_replace_frames=[6476,6650], use_candidate_frames=[0,174],
             references=[image_spec('late-B25-GPT-wing-original',25,8.5,'GPT脸、原白色衣裙、双角、两片膜翼、原教堂和原片渲染基准'),
                         audio_spec('late-B25-GPT-selected',8,[('VO-CY024A-01',91/24)])],
             prompt=STYLE+'\n8秒GPT展翼离地并开始咏唱，只包含中央白发双角双膜翼的GPT。保持Image1白色原裙、双角、'
             '翼骨结构和薄膜质感，不换装、不变成羽翼、不增加手杖。她仍在原教堂大厅，避免吊灯穿模。'
             '0至1.5秒低侧机位看半身到双脚和一侧翼根，有力下扇、裙摆与地面浮尘受气流向下外扬，脚尖真实离地，不能开场已经悬空摆拍。'
             '1.5至3.7秒同侧缓升到三分之四中景，人物避开吊灯，水珠依次上浮，前中后层次清楚；灯只作远处暖色层次，冷蓝窗光勾边。'
             '3.791667秒起，GPT按Audio1原选日语完整说盘踞于苍穹尽头，真实发声与停顿以音频为准，'
             '此时侧脸嘴部清楚、目光抬向穹顶。说完闭唇，至7.25秒是完整可剪用动作和句子，7.25至8秒只延续悬停余量。'
             'Audio1只有GPT这一句。千问的抱紧我已经在前一个镜头说完，这个镜头绝对不说抱紧我，不出现千问、小鱼或其他人。'
             '不重读其他咏唱、不加叹词、BGM或字幕；不要全段正面全身对称摆姿势，不环绕转圈，不用快速推脸。')
    ]
    for x in specs:
        x.update(mode='reference_with_selected_audio', estimated_credits=round(x['duration']*10.2,1),
                 status='draft_unmaterialized', change_reason='作者截图定点返修，保持现时间线总帧数；候选需视觉和口型复核',
                 acceptance=['原片身份、服装、画风连续','原选声音与发声/闭口节奏匹配','动作因果和相邻镜头空间连续',
                             'use_candidate_frames可完整覆盖目标窗口，不借变速修嘴','保留既有音轨，不采用模型另造的人声'])
    return specs

def materialize(item):
    import numpy as np
    REF.mkdir(parents=True,exist_ok=True)
    for r in item['references']:
        path=ROOT/r['path']
        if r['role']=='reference_image':
            subprocess.run(['ffmpeg','-v','error','-y','-ss',str(r['source_second']),'-i',r['source'],'-frames:v','1',str(path)],check=True)
        else:
            a=np.zeros(round(r['seconds']*48000),dtype=np.float32)
            for part in r['parts']:
                raw=subprocess.check_output(['ffmpeg','-v','error','-i',part['source'],'-ac','1','-ar','48000','-f','f32le','pipe:1'])
                samples=np.frombuffer(raw,dtype='<f4');start=round(part['offset_seconds']*48000)
                assert start>=0 and start+len(samples)<=len(a),(part['id'],start,len(samples),len(a))
                a[start:start+len(samples)]+=samples
            subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar','48000','-ac','1','-i','pipe:0','-c:a','pcm_s24le',str(path)],input=a.astype('<f4').tobytes(),check=True)
        r['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    item['status']='prepared_draft_not_queued'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--materialize',action='store_true');args=ap.parse_args()
    items=make_items()
    if args.materialize:
        for item in items:materialize(item)
    draft=dict(model='MiniMax-H3',resolution='768P',ratio='16:9',fps=24,items=items,
               estimated_credits_total=round(sum(i['estimated_credits'] for i in items),1),
               constraints=['不修改执行队列','不提交API','不修改Resolve','不导出视频','替换窗口帧数不变'],
               b38_minimal_post=dict(
                   reason='先消除重复小鱼开眼动作和回到更早状态，不恢复B37原段里GPT代Claude动嘴问题',
                   retain_B37_child=dict(timeline_frames=[9699,9736],source=source(38),source_frames=[15,52]),
                   replace_B38_child=dict(timeline_frames=[9781,9881],source=source(38),source_frames=[52,100],
                                         speed_percent=48.0,method='只在不说话的小鱼反应上延长2秒至4.166667秒；禁嘴部变速、禁与前段重复0.625–2.167'),
                   preserve_B38_hand=dict(timeline_frames=[9881,9978],source=source(38),source_frames=[100,197]),
                   limitation='这可消除动作重置，不能凭空建立阶上阶下关系。若仍需明确空间桥，须另审参考后补一个2秒镜；当前不生成未确认参考。',
                   notes='实际源切点4.166667、6.5、8.208333由场景检测确认。B37相邻新补拍2.792–4.333秒GPT口动风险已存在，不回填。'))
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(draft,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'draft':str(OUT),'materialized':args.materialize,'count':len(items)},ensure_ascii=False))

if __name__=='__main__':main()
