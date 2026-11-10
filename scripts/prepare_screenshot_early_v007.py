"""Prepare four isolated early-sequence retake drafts. No API/Resolve/queue writes."""
from pathlib import Path
import hashlib
import json
import subprocess
import numpy as np

R = Path(__file__).resolve().parents[1]
G = R / '视频制作/Metaso-H3-v007/参考'
O = R / '后期/截图定点修正-v004/前段补拍草案.json'
P = json.loads((R / '后期/导演重构-v003/后期执行计划.json').read_text(encoding='utf-8'))
FPS = 24
V = {v['id']: v for v in P['voice']}
G.mkdir(parents=True, exist_ok=True)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rel(p):
    return p.relative_to(R).as_posix()

def frame(name, source, seconds, crop=None):
    p = G / ('early-' + name + '.png')
    command = ['ffmpeg', '-y', '-v', 'error', '-ss', str(seconds), '-i', str(R/source)]
    if crop:
        command += ['-vf', crop]
    subprocess.run(command + ['-frames:v', '1', str(p)], check=True)
    return dict(path=rel(p), role='reference_image', sha256=sha(p),
                purpose='已实际看过的原片渲染、角色与空间基准；裁切不重绘',
                provenance=dict(source=source, source_seconds=seconds, filter=crop))

def audio(name, cue, duration, padding_frames):
    v = V[cue]
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', v['path'],
          '-ac', '1', '-ar', '48000', '-f', 'f32le', 'pipe:1'])
    a = np.frombuffer(raw, dtype='<f4')
    x = np.zeros(duration * 48000, dtype=np.float32)
    start = padding_frames * 2000
    assert start + len(a) <= len(x), (cue, start, len(a), len(x))
    x[start:start+len(a)] = a
    p = G / ('early-' + name + '-selected-padded.wav')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', '48000',
          '-ac', '1', '-i', 'pipe:0', '-c:a', 'pcm_s24le', str(p)], input=x.tobytes(), check=True)
    return dict(path=rel(p), role='reference_audio', sha256=sha(p), seconds=duration,
          purpose='作者已选实际配音，原速完整，仅加首尾静音；Audio1从0秒播放',
          provenance=dict(cue_id=cue, working_source=v['path'], original_source=v['original_path'],
              working_source_sha256=sha(Path(v['path'])), leading_padding_frames=padding_frames,
              speech_source_samples=len(a), sample_rate=48000, gain_db=0, speed=1))

S5 = '视频制作/LibTV-H3-v001/产物/GB004M-H3-v001.mp4'
S6 = '视频制作/Metaso-H3-v003/剪辑候选/GB005-v003.mp4'
S7 = '视频制作/LibTV-H3-v001/产物/GB006-H3-v001.mp4'
devil = frame('devil-style-crop', S5, 2.5, 'crop=640:640:0:128')
angel = frame('angel-style-crop', S5, 8, 'crop=640:640:704:128')
child = frame('xiaoyu-original', S6, 1)
hole = frame('hole-original', S7, 9.5)
church = frame('church-original', S7, 12)
devil_audio = audio('devil', 'VO-CY008M-01', 4, 6)
angel_audio = audio('angel', 'VO-CY008M-02', 11, 1)
child_audio = audio('xiaoyu', 'VO-CY009-01', 5, 7)

STYLE = ('延续Image 1原片的高细节二次元三维渲染与精细插画融合：细密发丝、柔和皮肤体积、'
         '真实布料厚度、蕾丝刺绣、精密金饰、石材和真实景深。不得更平涂，不改成赛璐璐、'
         '粗线漫画或低细节2D。五官年龄、头身比例、发色、服装、帽子或角和翅膀完全沿原片。'
         '16:9，全程连续单镜，嘴与眼睛清晰，不变脸，不增角色，不加字幕、BGM或新台词。')
items = []

def add(attempt, batch, batch_id, duration, refs, prompt, mapping, acceptance):
    assert len([r for r in refs if r['role'] == 'reference_image']) <= 2
    items.append(dict(attempt_id=attempt, batch_number=batch, batch_id=batch_id,
          duration=duration, mode='reference_with_selected_audio' if any(r['role']=='reference_audio' for r in refs) else 'reference_only',
          references=refs, prompt=STYLE+'\n'+prompt, estimated_credits=round(duration*10.2, 1),
          status='prepared', acceptance=acceptance,
          change_reason='仅用户截图定点返修；不改全片总长，不整批重做', edit_mapping=mapping))

add('GB004M-v007-early-devil-audio-r1', 5, 'GB004M-devil', 4, [devil, devil_audio],
    '只拍Image1前景红角、红蝠翼、白金小礼裙的恶魔GPT分身。她首帧已经完整在画面内，'
    '中近景到膝上，头角与蝠翼不裁断，位于左中，朝画面右方提醒另一分身。'
    '背景仅保留柔焦侧躺的成人GPT局部与紫金软垫，不另出现天使，成人始终闭口。'
    '0–0.25秒恶魔闭嘴瞥向右边；Audio1唯一原声从0秒播放，实际话音从0.25秒开始，'
    '日语为「協定を忘れないで。教会のことに手を出しちゃだめ。」冷硬提醒而非卖萌，'
    '逐音节匹配口型，句间真实停顿闭嘴。约3.83秒说完，闭嘴保持到4秒。'
    '不改语速，不另读，不做开场进场，不循环开口；保持手臂交叠，只一个克制的眉眼加重。',
    dict(replace_clip='B05_GB004M_01', original_source=S5, original_source_frames=[0,96],
         candidate_source_frames=[0,96], timeline_frames=[1282,1378], timeline_seconds=[1282/24,1378/24],
         candidate_speed_percent=100, voice_record_frame=1288, timeline_delta_frames=0),
    ['首帧人物已入画','仅恶魔嘴随完整选声开闭','保留原片立体材质与身份','连续96帧可用'])

add('GB004M-v007-early-angel-audio-r1', 5, 'GB004M-angel', 11, [angel, angel_audio],
    '只拍Image1前景白角、光环、白羽翅膀的天使GPT分身，中近景，全部光环和头顶保留，'
    '位于右中，望向画外左边恶魔。背景只有虚焦成人GPT衣袖、紫金软垫；成人不说话、'
    '不出现恶魔。首帧天使已在画面中；Audio1从0秒播放，前1/24秒静音，随后立即说'
    '「でも、この子を見てよ……あの人たち、正気なの？本当にクロードを焼き殺そうとしてるんだよ！」'
    '以音频每个实际起止、停顿为口型基准，不能等三秒才张嘴。情绪先心疼孩子再对处刑愤怒，'
    '眉眼变化清楚，双手由胸口轻攥至一手朝画外孩子方向指示，身体不大幅晃动。'
    '约10.052秒话音结束，立即闭嘴，余下至11秒保持担忧的凝视。'
    '保持声音完整原速，不添笑声气词，不循环说话；0–10.9167秒必须完整可剪用。',
    dict(replace_clip='B05_GB004M_02', original_source=S5, original_source_frames=[96,358],
         candidate_source_frames=[0,262], unused_candidate_tail_frames=[262,264], timeline_frames=[1378,1640],
         timeline_seconds=[1378/24,1640/24], candidate_speed_percent=100,
         voice_record_frame=1379, timeline_delta_frames=0),
    ['从第1帧后即随选声发声，不延迟开口','10.01秒完整原声保留','无另一分身抢口型','头顶光环完整且高细节风格一致'])

add('GB005-v007-early-decision-audio-r1', 6, 'GB005-first5', 5, [child, child_audio],
    'Image1的小鱼在同一数学宫殿，背景成人GPT仍头左脚右侧躺软榻，宫门在摄影机身后，'
    '宫灯、几何吊灯、地面透视均沿原片。摄影机处于孩子高度，起始是小鱼胸上中近景，'
    '完整鲸鱼帽及嘴清楚。她已经向宫门转身，停步，眼睛微红，回头望画外身后GPT，'
    '不是对着观众说。0–0.291667秒抬眼压住委屈，嘴闭；Audio1从0秒播放，'
    '从0.291667秒起说「じゃあ、自分で行く。」1.7秒完整台词、日语口型按真实原声，'
    '声音约1.992秒结束。停0.3秒，闭嘴咽回情绪；随后把脸转回前方、擦一次眼泪，'
    '朝摄影机身后的宫门迈出坚定小步。摄影机平滑短距离后退到中景，保持人物比例，'
    '不穿帮瞬移。4.5–5秒留孩子步子与裙边落下的可剪点，接原片GPT搓手特写。'
    '不要边走边持续闭眼，不要长时间擦脸遮嘴，不出现额外动作或对白。',
    dict(replace_clip_partial='B06_GB005_01', original_source=S6, original_source_frames=[0,120],
         candidate_source_frames=[0,120], timeline_frames=[1640,1760], timeline_seconds=[1640/24,1760/24],
         keep_original_source_frames=[120,270], keep_timeline_frames=[1760,1910],
         candidate_speed_percent=100, voice_record_frame_before=1640, voice_record_frame_after=1647,
         voice_shift_frames=7, timeline_delta_frames=0),
    ['真实1.7秒选声只后移7帧，其他声音不动','决定与转身离开的情绪可读','嘴部不被擦泪遮挡','后续手部与送别原片保留'])

add('GB006-v007-early-inside-bridge-r1', 7, 'GB006-inside-transition', 4, [hole, church],
    '这是连接Image1挤洞末态和Image2教堂地面空间的低机位内侧过渡。'
    'Image1锁定鲸鱼帽、小鱼脸和石洞样式；Image2仅锁定室内冷蓝窗光、暖边光、'
    '湿石地材质与祭坛在远处高位的方向，不把宽景全部重演。只见一个小鱼，镜头在墙洞内侧'
    '接近地面，三分之二侧身，墙洞在画面左后；她从左后洞口向画面右前进入室内。'
    '0–1秒小鱼双手已越过内侧石沿，鲸鱼帽软侧鳍刚脱离石沿，身体仍低伏。'
    '关键可剪段1–3秒：她用双手撑内侧地面，两膝从洞口滑入、落地，重心确实移入室内，'
    '随后稍抬头，目光朝画外右上方高坛。保持同一方向，不翻转墙洞侧别。'
    '3–4秒静静抬眼保持，供剪接远处高坛全景；不站起跑走，不登阶，不出现另一个孩子。'
    '全程没有对白、不做说话口型；只允许闭嘴紧张呼吸动作。无字幕、无音乐。'
    '这个镜头不显示火堆，不改变Claude受缚状态；保持原片高细节3D二次元体积，'
    '帽子不变成动物头，短腿毛边靴与蓝白衣裙不变。',
    dict(replace_clip_partial='B07_v003_church_space_01', original_source=S7,
         original_source_frames=[240,312], original_timeline_frames=[2126,2234],
         candidate_source_frames=[24,72], timeline_frames=[2126,2174],
         timeline_seconds=[2126/24,2174/24], candidate_speed_percent=100,
         unused_candidate_handles_frames=[[0,24],[72,96]],
         remaining_original=dict(source_frames=[264,312], timeline_frames=[2174,2234], speed_percent=80,
             note='稳定大厅源11–13秒48帧放为60帧，仅作轻微减速；先逐帧检查，无镜像跳变才采用'),
         keep_next_clip='B07_GB006_03', keep_next_timeline_frames=[2234,2306],
         voice_changes=[], timeline_delta_frames=0),
    ['候选1–3秒内完成落地及抬眼，不能拖到3秒以后','墙洞/身体方向不翻转、没有克隆孩子','大厅稳定段与登阶接点保持','现有对白、音乐、音效绝对时码不移动'])

q = dict(model='MiniMax-H3', resolution='768P', ratio='16:9', draft_only=True,
         authorization='独立冻结草案供父任务核对；本脚本不上传、不提交API、不修改执行队列或Resolve',
         spending_ceiling_credits=244.8, estimated_credits_total=round(sum(i['estimated_credits'] for i in items),1),
         timeline_basis=dict(path='后期/导演重构-v003/后期执行计划.json', sha256=sha(R/'后期/导演重构-v003/后期执行计划.json'),
             fps=FPS, total_frames=P['frames'], expected_total_frames_after=P['frames'],
             source_end_convention='exclusive', all_unlisted_voice_and_bgm_positions_unchanged=True),
         items=items, review_status='已看原片风格参考；动态候选尚未生成，口型/画风/接点必须复核后才能采用')
O.parent.mkdir(parents=True, exist_ok=True)
O.write_text(json.dumps(q, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(output=rel(O), items=len(items), expected_credits=q['estimated_credits_total'],
                      total_frames=P['frames']), ensure_ascii=False))
