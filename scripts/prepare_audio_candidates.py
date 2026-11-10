"""Freeze the first researched soundtrack and casting candidates, never adopt them."""
import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
args = p.parse_args()
root = args.root.resolve()
record = root / '资产/生成记录/声音候选-v001.json'
if record.exists():
    raise SystemExit('Preserve existing v001; create a new revision.')
music = [
    dict(id='BGM-HOPE-001', title='A Kind Of Hope', slug='a-kind-of-hope', url='https://www.scottbuckley.com.au/library/wp-content/uploads/2022/10/AKindOfHope.mp3', role='初遇与结尾的情感主题；第一遍保留忧伤，尾声回归温暖。', description='作者描述：钢琴、弦乐与氛围合成器，苦甜交织、略有迟疑的希望。', scenes=['S01','S06']),
    dict(id='BGM-DESCENT-001', title='Descent', slug='descent', url='https://www.scottbuckley.com.au/library/wp-content/uploads/2018/04/descent.mp3', role='宫殿犹豫、潜入与火祭的压迫底色；脚步发现与第二支火把前留白。', description='作者描述：阴暗氛围、人声纹理、合成器及处理过的管乐。需试听确认人声纹理不遮对白。', scenes=['S02','S03','S04']),
    dict(id='BGM-TITAN-001', title='Titan', slug='titan', url='https://www.scottbuckley.com.au/library/wp-content/uploads/2018/06/sb_titan.mp3', role='援军入场、邀约回闪与破局；对白处压低，战后迅速收束。', description='作者描述：沉郁大提琴起始，逐步展开至完整管弦乐。不是持续战斗鼓点，优先服务获救的释放感。', scenes=['S05']),
]
def acquire(m):
    m.update(author='Scott Buckley', source='https://www.scottbuckley.com.au/library/'+m.pop('slug')+'/', license='CC BY 4.0', license_url='https://creativecommons.org/licenses/by/4.0/', status='候选 · 待试听', heard=False, source_in=None, source_out=None)
    m['attribution'] = f"'{m['title']}' by Scott Buckley — released under CC BY 4.0. www.scottbuckley.com.au. 本片使用时注明剪辑及淡入淡出。"
    path = root / '资产/声音/BGM' / (m['id']+'.mp3')
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        if path.exists():
            raise RuntimeError('Existing candidate file; refusing overwrite')
        req = urllib.request.Request(m['url'], headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=45) as response:
            blob = response.read()
        tmp = path.with_suffix('.part.mp3')
        tmp.write_bytes(blob)
        probe = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,sample_rate,channels','-of','json',str(tmp)], capture_output=True, text=True, check=True)
        decode = subprocess.run(['ffmpeg','-v','error','-i',str(tmp),'-f','null','-'], capture_output=True, check=True)
        m.update(probe=json.loads(probe.stdout),sha256=hashlib.sha256(blob).hexdigest(),bytes=len(blob),decode_ok=True)
        tmp.rename(path)
        m['path'] = path.relative_to(root).as_posix()
    except Exception as ex:
        m['acquisition_error'] = str(ex)
    return m
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    music=list(pool.map(acquire,music))
refs=[
    dict(id='VOICE-REF-DS-01',title='一发入魂！ssr大肥鱼音色！',creator='星落落_oi',url='https://www.bilibili.com/video/BV1PPYM6EEUR/',role='DeepSeek',finding='歌唱音色参考。后续《人是猫》简介明确指向本视频；未取得独立对白包或公开合成音色 ID。页面标注未经作者授权禁止转载。',evidence='搜索索引正文；浏览器原页待核对',reusable=False),
    dict(id='VOICE-REF-DS-02',title='deepseek 翻唱《人是猫》真完整版',creator='星落落_oi / 蒙德砍壬',url='https://www.bilibili.com/video/BV1fYpn6SEk9/',role='DeepSeek',finding='简介明确写音色参考 BV1PPYM6EEUR；证明该系列的声线关系，不证明对白可复用。',evidence='搜索索引正文',reusable=False),
    dict(id='VOICE-REF-GPT-01',title='GPT小龙娘开始融入DeepSeek大家庭了',creator='这个刀子真甜',url='https://www.bilibili.com/video/BV1EvKK6NEoi/',role='GPT / DeepSeek',finding='相关角色成片与壁纸；形象注明 ZipZipPipe。未找到配音音色编号或独立人声下载。',evidence='搜索索引正文；直接抓取412',reusable=False),
    dict(id='VOICE-REF-CL-01',title='DS娘部署了Q娘帮自己干活',creator='奶糕兽',url='https://www.bilibili.com/video/BV1D4MS6jE36/',role='Claude / 千问 / DeepSeek',finding='系列列表出现《当我把散文中的珍珠鸟改成 Claude》《Claude和鱼尾草》，是作者线索；本视频并非已核实的 Claude 声音样本。',evidence='搜索索引正文；直接抓取412',reusable=False),
    dict(id='VOICE-REF-ENSEMBLE-01',title='模型洄游：AI之间的模术回战先行预告',creator='盐水哈基米',url='https://www.bilibili.com/video/BV1UmY56GEEa/',role='GPT / Gemini / Claude / Grok / DeepSeek',finding='简介说明配音音频为后期替换，剧情参考咒术回战；不能当作五个角色的公开原创音源。',evidence='搜索索引正文',reusable=False),
    dict(id='VOICE-REF-FISH-01',title='10月7日AI圈7件事',creator='AI鼓励师_悠一',url='https://www.bilibili.com/video/BV1arpN6FEHv/',role='DeepSeek',finding='简介标注 Fish Audio「苏晓晓」。这是现成音色名称线索；音色 ID、当前可用性及是否符合宝宝造型未核实。',evidence='搜索索引正文',reusable=False),
]
casting=[
    ('DeepSeek','奶软、圆润的幼小女孩声，清楚但不尖锐；不要成熟女仆声。','CY003','自然递饭，像分享自己最喜欢的食物。','CY006','着急求助，气息短但字句完整；不要全程哭腔。'),
    ('ChatGPT','偏中低的年轻女性声，清冷、克制，有分量。','CY007','拒绝时有停顿与压住的犹豫，不冷笑。','CY027B','轻而短、干脆截断；不喊成战斗口号。'),
    ('Claude','柔软偏细的年轻女性声，虚弱、带气息，避免甜腻。','CY020','先短吸气，护住宝宝的瞬间突然用力；尾音体力不支。',None,None),
    ('教主','低沉成年男声，庄严表面下带控制欲。','CY017','近乎温柔地宣判，平静更可怕。','CY027A','被挑战权威，咬住条约二字；不持续咆哮。'),
    ('教徒','偏干、直接的成年男声，与教主音色区分。','CY004','冷漠通告，勿解说腔。',None,None),
    ('千问','温润、沉稳的年轻女性声，落字清晰。','CY026A1','毫不迟疑的同意，短而稳。',None,None),
    ('Gemini','清亮、灵动的年轻女性声，与宝宝年龄感分开。','CY026B','轻快主动，有行动感。',None,None),
    ('Grok','略低、带一点沙感的年轻女性声。','CY026C','自信、轻微笑意，不夸张嘲讽。',None,None),
    ('Kimi','轻、柔、偏冷的年轻女性声。','CY026D','从困倦转为认真；短应声，不拖成长呻吟。',None,None),
]
cast=[dict(role=r,voice_direction=v,first_shot=s,first_acting=a,contrast_shot=s2,contrast_acting=a2,status='待合成试音',adopted_voice=None) for r,v,s,a,s2,a2 in casting]
data=dict(version='v001',date='2026-10-21',dialogue_source='镜头设计/shot-plan-v0.5.json',music=music,voice_references=refs,casting=cast,
    conclusion='本轮找到相关成片、歌唱声线和一个具名音色线索，未核实任何可直接用于本片的现成独立对白素材。优先为本片设计一致声线，先三位主角单句试音再扩展。',
    listening_status='尚未完成实际听审；音乐配器与情绪依据作者介绍，不能当作已试听结论。',
    generation_status='未生成正式试音：ComfyUI MCP server_info 失败；127.0.0.1:8188 返回502；历史 VoxCPM2 两个工作流路径不存在。没有改用其他服务或安装新工作流。',
    search_status='DeepSeek Search 两次401。作者同意改普通网页搜索及内置浏览器；B站直接抓取412。未下载、克隆或转载博主配音。',
    cue_design=[
        dict(scenes=['S01','S06'],music_id='BGM-HOPE-001',direction='首尾同一主题；递饭和眼神留空间，结尾最后4秒让音乐尾音与街市底声自然散去。'),
        dict(scenes=['S02','S03','S04'],music_id='BGM-DESCENT-001',direction='由极轻到压迫，不一路顶满。锁链、归来脚步、火把入水要能听清；踹门前短暂停乐。'),
        dict(scenes=['S05'],music_id='BGM-TITAN-001',direction='踹门撞击先出现，再进入希望主题。邀约段保持连贯推动；条约对白压低，聒噪前留白；强光之后收束。实际乐句入出点听审后填写。')])
record.parent.mkdir(parents=True,exist_ok=True)
record.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assets=root/'资产/assets.json'
atlas=json.loads(assets.read_text(encoding='utf-8'))
atlas['sound_manifest']=record.relative_to(root).as_posix()
assets.write_text(json.dumps(atlas,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'music':[{'id':m['id'],'file':m.get('path'),'error':m.get('acquisition_error')} for m in music],'voice_sources':len(refs),'casting':len(cast)},ensure_ascii=False))
