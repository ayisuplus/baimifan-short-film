from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[3];D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
voice='后期/导演重构-v003/声音/VO-CY024-01-工作源.wav'
probe=subprocess.run(['ffmpeg','-hide_banner','-i',str(R/voice),'-af','silencedetect=noise=-35dB:d=0.04','-f','null','-'],capture_output=True,text=True,encoding='utf8',errors='replace')
(D/'B17-选声静音检测.txt').write_text(probe.stderr,encoding='utf8')
video='视频制作/Metaso-H3-v010/产物/GB014-v010-original-shot-only-r1.mp4'
new='视频制作/Metaso-H3-v011/产物/GB014-v011-original-2d-group-r1.mp4'
plan={
 'scope':'B17–32 最小剪辑建议；子代理仅本目录产出，不修改Resolve/队列',
 'fps':24,'range_convention':'start inclusive, end exclusive',
 'baseline':'v005_2D_Anime_Fixes; 后期/全片画风统一-v007/修前时间线.json',
 'evidence_method':'B17 v010/v011全5秒按24fps提取；逐帧面部页实看，v010候选24–83全部全景帧实看；B26源24–107全部逐帧实看；B25等沿既有精确源区间证据并读回裁切属性。原声silencedetect量测，不冒称连续听审或逐音素验收。',
 'edits':[
  {'id':'B17-replace-only-60f','action':'replace_video_only','status':'recommended_for_root_review',
   'timeline_start':4778,'timeline_end':4838,'timecode':['03:19:02','03:21:14'],
   'source':video,'source_sha256':sha(video),'source_in':24,'source_out':84,'duration_frames':60,'speed_percent':100,
   'transform':{'ZoomX':1,'ZoomY':1,'Pan':0,'Tilt':0},'preserve_existing_audio':True,
   'reason':'v010候选恢复原九人、月夜和湿地，千问仍持扇；红帽角色持剑，金发角色持斧，绿发持杖，候选范围未见互换。GPT短手势比整队长期走秀更适合2.5秒窗口。',
   'voice':{'path':voice,'sha256':sha(voice),'timeline_start':4786,'duration_seconds':1.41,'file_leading_silence_seconds':0.233979,
    'expected_source_first_audible_frame':37.615496,'expected_source_last_audible_frame':59.839496,
    'alignment':'原声文件起点映射候选源32帧；肉眼小嘴形变化约落在38–60帧，窗口大体接近，脸在全景内像素很少，不能验证每个日语音素。保持现有音轨，不把新回片原生声混入。'},
   'review_risks':['v010动作克制，只作局部收口，不能称张力最终批准','细密衣发与原图接近，但作者审美仍需最终看实际2.5秒','保留后续4838–4922教主反应与原声，不用v011末段换武器画面'],
   'evidence':['证据/B17-v010-full-02.jpg','证据/B17-v010-full-03.jpg','证据/B17-v010-full-04.jpg','证据/B17-v010-full-05.jpg','证据/B17-v010-full-06.jpg','证据/B17-v010-face-00.jpg','证据/B17-v010-face-01.jpg','B17-选声静音检测.txt']},
  {'id':'flashback-return-music-bridge','action':'audio_only_trial','status':'optional_AB_trial_not_auditioned',
   'cut_frame':6303,'cut_timecode':'04:22:15','window':[6285,6321],
   'incoming':{'id':'M09','source':'资产/声音/BGM/重选-v001/BGM-CY-FEAR-001.m4a','source_sha256':sha('资产/声音/BGM/重选-v001/BGM-CY-FEAR-001.m4a'),
    'original_timeline_start':6389,'new_timeline_start':6285,'keep_timeline_end':8007,
    'original_source_in_seconds':24.999932212885128,'new_source_in_seconds':20.666598879551795,
    'gain_db':-16.935598806937218,'fade_in_frames':36,'fade_in_window':[6285,6321],'fade_out_seconds':0.8,
    'constraint':'从原曲重建同一工作段，保持6389之后源位置映射和原结尾，不能把旧完整音乐整体前挪104帧。'},
   'outgoing':{'id':'N01_flashback','keep_timeline_start':5696,'old_timeline_end':6418,'new_timeline_end':6321,'fade_out_window':[6285,6321]},
   'do_not_change':['任何角色配音位置/速度/选择','回忆各场画面','M09既有后续动作卡点与祈愿停乐'],
   'reason':'现有N01已提前19帧进入首回忆，进入端无需重复加桥；回现实6303后N01仍持续4.79秒才结束。本试排用原曲前手柄让战斗音乐在返回现实前0.75秒出现并交接，不新增曲目。',
   'acceptance':'需要原速听A/B，确认原曲前手柄音色/乐句自然且不盖Kimi最后回应；若不自然保持现状，不冒称原来存在断乐。'}],
 'keep':[
  {'batch':25,'timeline':[6303,6650],'decision':'不换人物、不额外软裁、不补拍',
   'reason':'既有idx74(6560–6578)已Zoom2.470588、Pan988.235294、Tilt-558.705882，是局部切镜/口型规避，不是整个镜头的默认构图；另加统一裁切会破坏该策略及双翼/手势。原图与现片差异不足以证明场地被替换。'},
  {'batches':[18,19,20,21,23,24,30],'decision':'全部Kimi现片按作者选择保留，不以精细材质为由替换'},
  {'batch':26,'timeline':[6728,6812],'decision':'扇叶疑点排除，不补拍',
   'source_frame_findings':[
    {'frames':[24,29],'finding':'右手握扇轴，余扇留在手中'},
    {'frames':[29,61],'finding':'轴部青紫亮起，一条外缘叶根解开向右上离开；母扇/握柄持续留在手中，不是整扇离手'},
    {'frames':[61,97],'finding':'只有一枚有方尾、尖端和蓝底花纹的单叶伴飞，薄青紫光贴边'},
    {'frames':[97,99],'finding':'切碰撞镜，术矛与叶尚未接触'},
    {'frames':[99,108],'finding':'先发生接触强光，随后碎光及术光偏折；未看到碰前落叶'}],
   'evidence':['证据/B26-full-02.jpg','证据/B26-full-03.jpg','证据/B26-full-04.jpg','证据/B26-full-05.jpg','证据/B26-full-06.jpg','证据/B26-full-07.jpg','证据/B26-full-08.jpg'],
   'limit':'切出点没有完整展示飞叶落地，但镜头省略不等于剧情错误。单叶在另一机位显得厚一些，不构成整把合扇证据。'},
  {'batches':[26,27,28,29,30,31,32],'decision':'水珠/云涡/水龙现片保留，不扩大补拍',
   'reason':'既有实帧未发现需按人物建模问题重拍的证据。水龙目位有水体高光和眉骨，但未证实有固定发光眼球；水滴玻璃式折射不能单独触发角色返修。',
   'limit':'水龙目前为精确源区间头中尾及长镜加样检查，未作整段每帧眼部跟踪，不称所有帧零问题。'}],
 'rejected_alternative':{'source':new,'source_sha256':sha(new),'reason':'3.5秒后千问推进时出现持长剑漂移，不能整条采用；前半与v010相比无明确优势，采用v010窗口更保守。'},
 'do_not_execute':['没有新生成授权调用','不更换Kimi','不下载/采用尚未审过的新候选','不输出成片','不以本清单覆盖作者选择或根队列']}
(D/'最小剪辑清单.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
print('written',D/'最小剪辑清单.json')
