"""Make a versioned, shot-linked voice comparison from existing recordings."""
from pathlib import Path
from urllib.parse import quote
import ast
import hashlib
import json
import re
import shutil
import subprocess
from voice_candidates_v005 import merge_v005

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / '后期/配音挑选-v022'
BOARD = ROOT / '视频制作/生成板-v022'
OLD_PREVIEW = ROOT / '后期/语音节奏定版-v021/全片声音预览.html'
OLD_BOARD = ROOT / '视频制作/生成板-v021/生成板.html'

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def duration(path):
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(path)])
    return round(float(out), 3)

def make_option(path, label, note='', selectable=True):
    path = Path(path)
    path = path if path.is_absolute() else ROOT / path
    if not path.is_file():
        raise FileNotFoundError(path)
    relative = path.relative_to(ROOT).as_posix()
    return dict(id='opt-'+hashlib.sha256(relative.encode('utf-8')).hexdigest()[:16], path=relative,
                url='../../'+quote(relative, safe='/'), label=label, note=note, selectable=selectable,
                sha256=sha(path), seconds=duration(path))

def main():
    PREVIEW.mkdir(parents=True, exist_ok=True)
    BOARD.mkdir(parents=True, exist_ok=True)
    mapping = load(ROOT/'视频制作/生成板-v021/日语音频映射.json')['cues']
    voice = {x['id']: x for x in load(ROOT/'后期/语音节奏定版-v021/配音对位方案.json')['cues']}
    current = {x['cue_id']: x for x in mapping}
    options = {key: {} for key in current}
    def add(cue, path, label, note='', selectable=True, raw=False):
        if cue not in options:
            raise ValueError(f'Unknown cue: {cue}')
        opt=make_option(path, label, note, selectable)
        opt['raw']=raw
        options[cue][opt['path']] = opt
    dirs = [
        ('后期/日语配音交接-v001/成品-v001/干声', 'v001 旧版干声'),
        ('后期/日语配音修正-v002/干声', 'v002 干声'),
        ('后期/日语配音修正-v003/干声', 'v003 干声'),
        ('后期/日语配音修正-v004/干声', 'v004 干声'),
    ]
    for folder,label in dirs:
        for path in sorted((ROOT/folder).glob('*.wav')):
            cue=path.name.split('__', 1)[0]
            if cue not in current: continue
            name=label
            if '-0.9s' in path.stem: name += ' · 0.9秒版'
            if '-1.2s' in path.stem: name += ' · 1.2秒版'
            is_old_spell = cue=='VO-CY024A5-02' and 'v001' in folder
            note = '旧版术名为「そうかいてんけい！」，与现行词不符，仅供对照。' if is_old_spell else ('历史A2A版本；咏唱切分与发音请听审。' if 'v001' in folder else '逐句版本；发音和表演以试听为准。')
            add(cue, path, name, note, not is_old_spell)
    # Earlier board mappings include two inner-scene originals and a corrected spell absent from the dry folders.
    for cue,path,label in [
        ('VO-CY008M-01','资产/声音/王宫内心戏-v001/VO-CY008M-01__恶魔GPT__ja__v001.wav','v001 内心戏原版'),
        ('VO-CY008M-02','资产/声音/王宫内心戏-v001/VO-CY008M-02__天使GPT__ja__v001.wav','v001 内心戏原版'),
        ('VO-CY024A5-02','资产/声音/沧龙出海-v002/VO-CY024A5-02__GPT__ja__v002.wav','v002 沧龙出海修正版'),
        ('VO-CY024A5-01','后期/日语配音修正-v003/原生/GPT-A句10-汝の救済を.wav','v003 祈愿原生首版'),
        ('VO-CY024A0-01','后期/日语配音修正-v003/原生/千问-024A0-抱紧我.wav','v003 抱紧我原生首版'),
    ]: add(cue,path,label,'历史备选，逐字与表演需听审。')
    add('VO-CY024A5-02','后期/日语配音修正-v003/原生/GPT-术名そうかいてんけい.wav',
        'v003 旧术名原生版','旧版术名为「そうかいてんけい！」，与现行词不符，仅供对照。',False)
    # Preserve uncut and intermediate files as secondary alternatives, grouped in the UI.
    for folder,label in [
        ('后期/日语配音交接-v001/成品-v001/原生','v001 原生未剪'),
        ('后期/日语配音修正-v004/原生','v004 原生未剪'),
        ('后期/日语配音修正-v004/切分输入','v004 切分输入'),
    ]:
        for path in sorted((ROOT/folder).glob('VO-*.wav')):
            cue=path.name.split('__',1)[0]
            if cue in current:
                add(cue,path,label,'与同版干声为同次表演；首尾、声道或停顿可能不同。',raw=True)
    specs_tree=ast.parse((ROOT/'后期/日语配音修正-v003/build_dry.py').read_text('utf-8'))
    specs=next(ast.literal_eval(node.value) for node in specs_tree.body
               if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='specs' for t in node.targets))
    for output, native, *_ in specs:
        cue=output.split('__',1)[0]
        if native.startswith('Claude-星火'): continue  # continuous files are listed as groups
        if cue=='VO-CY024A5-02': native='GPT-术名そうりゅうしゅつかい.wav'  # rebuilt after the old spec
        add(cue,ROOT/'后期/日语配音修正-v003/原生'/native,'v003 原生未剪',
            '与v003干声为同次表演；首尾和停顿可能不同。',raw=True)
    for cue,file,label in [
        ('VO-CY024K1A-01','T2A-术名A-1.2s.wav','v002 术名A 原生未剪'),
        ('VO-CY024K1A-01','T2A-术名B-0.9s.wav','v002 术名B 原生未剪'),
        ('VO-CY026D-02','T2A-应答うん.wav','v002 应答原生未剪'),
    ]: add(cue,ROOT/'后期/日语配音修正-v002/原生'/file,label,'与v002干声为同次表演；首尾和声道可能不同。',raw=True)
    trial_dir=ROOT/'后期/日语配音交接-v001/试音候选-v001'
    trials=load(trial_dir/'试音记录-v001.json')
    known={x['file']: x for x in trials['trials']}
    for path in sorted(trial_dir.glob('*.wav')):
        cue=path.name.split('__',1)[0]
        if cue not in current: continue
        rec=known.get(path.name)
        if rec and rec['japanese'] != current[cue]['text']:
            raise ValueError(f'Trial text mismatch: {path}')
        name='v001 历史试音 · '+(rec['candidate'] if rec else path.stem.rsplit('-',1)[-1])
        note='历史试音，此前整体被否定；发音与表演请重新试听。' if rec else '历史记录标为待补但文件存在；原文和实际内容需听审确认。'
        add(cue,path,name,note)
    for c in mapping:
        if c['path'] not in options[c['cue_id']]:
            add(c['cue_id'],c['path'],'当前混音使用版本','现有整片混音使用此文件。')
    group_definitions = [
        ('kimi','Kimi 月影渡连续咏唱',['VO-CY024R-01','VO-CY024K0-01','VO-CY024K0-02','VO-CY024K1A-01'],[
            ('后期/日语配音交接-v001/成品-v001/原生/母版-Kimi月影渡-连续咏唱.wav','v001 原生整段','处理前原始连续表演。',True),
            ('后期/日语配音交接-v001/成品-v001/母版/母版-Kimi月影渡-连续咏唱.wav','v001 旧整段（含术名）','历史A2A母版。',True),
            ('后期/日语配音修正-v002/原生/T2A-母版A-平稳念咒.wav','v002 A 平稳念咒（前三句）','完整慢版，无可靠单句边界，不含术名。',True),
            ('后期/日语配音修正-v002/原生/T2A-母版B-念咒口语.wav','v002 B 念咒口语（前三句）','与v002对应单句同源，不含术名。',True),
            ('后期/日语配音修正-v002/母版/母版-Kimi月影渡-连续咏唱-v002.wav','v002 拼接母版（含术名）','与v002逐句切片同源。',True),
            ('后期/日语配音修正-v004/母版/母版-Kimi月影渡-连续咏唱-v004.wav','v004 拼接母版（含术名）','与v004逐句干声同源。',True)]),
        ('gpt','GPT 水龙咏唱',[f'VO-{x}-01' for x in ['CY024A','CY024A9','CY024A2','CY024A3','CY024A6','CY024A7','CY024A4','CY024A8','CY024A5']]+['VO-CY024A6-02','VO-CY024A5-02'],[
            ('后期/日语配音交接-v001/成品-v001/原生/母版-GPT沧海天倾-连续咏唱.wav','v001 原生整段（含旧术名）','旧术名不符，仅供对照。',False),
            ('后期/日语配音交接-v001/成品-v001/母版/母版-GPT沧海天倾-连续咏唱.wav','v001 旧整段（含旧术名）','术名为旧词，仅供对照。',False),
            ('后期/日语配音修正-v003/原生/GPT-沧海天倾母版-10句.wav','v003 快速连续版（十句）','不含术名；无可靠单句边界。',True),
            ('后期/日语配音修正-v003/原生/GPT-沧海天倾母版B-庄重10句.wav','v003 庄重连续版（十句）','不含术名；无可靠单句边界。',True),
            ('后期/日语配音修正-v003/母版/母版-GPT沧海天倾-连续咏唱-v003.wav','v003 逐句拼接母版','与v003逐句干声同源。',True)]),
        ('claude','Claude 星火完整咏唱',['VO-CY028B-01','VO-CY028C-01','VO-CY029E1-01','VO-CY029E2-01','VO-CY029E3-01','VO-CY029E4-01','VO-CY029B1-01'],[
            ('后期/日语配音交接-v001/成品-v001/原生/母版-Claude星火-连续咏唱.wav','v001 原生整段','处理前原始连续表演。',True),
            ('后期/日语配音交接-v001/成品-v001/母版/母版-Claude星火-含停顿-连续咏唱.wav','v001 旧整段（含停顿）','历史A2A母版。',True),
            ('后期/日语配音修正-v003/母版/母版-Claude星火-连续咏唱-v003.wav','v003 拼接母版（含停顿）','逐句文件与父亲停顿拼接。',True)]),
        ('claude-front','Claude 星火前两句',['VO-CY028B-01','VO-CY028C-01'],[
            ('后期/日语配音修正-v003/原生/Claude-星火前段-2句.wav','v003 连续原声前两句','只包含前两句。',True)]),
        ('claude-back','Claude 星火后五句',['VO-CY029E1-01','VO-CY029E2-01','VO-CY029E3-01','VO-CY029E4-01','VO-CY029B1-01'],[
            ('后期/日语配音修正-v003/原生/Claude-星火后段-5句.wav','v003 连续原声后五句','只包含后五句。',True)]),
    ]
    groups=[dict(id=gid,title=title,members=members,options=[make_option(*o) for o in opts]) for gid,title,members,opts in group_definitions]
    for g in groups:
        if any(c not in current for c in g['members']): raise ValueError(g['id'])
    cues=[]
    for c in mapping:
        v=voice[c['cue_id']]
        cues.append(dict(id=c['cue_id'],shot=c['shot_id'],visual_shots=c.get('visual_shots',[c['shot_id']]),
                         role=c['speaker'],ja=c['text'],start=c['timeline_start'],end=c['timeline_end'],
                         current_path=c['path'],options=list(options[c['cue_id']].values())))
    manifest=dict(version='v022', source='视频制作/生成板-v021/日语音频映射.json',
                  source_sha256=sha(ROOT/'视频制作/生成板-v021/日语音频映射.json'), cues=cues, groups=groups)
    manifest = merge_v005(manifest, ROOT)
    (PREVIEW/'候选索引.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    choices=PREVIEW/'作者选择.json'
    if not choices.exists(): choices.write_text('{"schema": 1, "cue_choices": {}, "group_choices": {}}\n',encoding='utf-8')
    # Keep the previous complete, fixed mix intact; the selector auditions source clips separately.
    page=OLD_PREVIEW.read_text('utf-8')
    data_start='<script id="data" type="application/json">'
    ps=page.index(data_start)+len(data_start);pe=page.index('</script>',ps)
    payload=json.loads(page[ps:pe])
    payload['audio']='../'+quote('语音节奏定版-v021/全片声音预览.mp3',safe='/')
    page=page[:ps]+json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+page[pe:]
    marker='<div class="footer">'
    assert page.count(marker)==1
    panel='<section class="voice-picker" aria-labelledby="voice-picker-title"><div class="picker-header"><div><h2 id="voice-picker-title">这个画面的配音版本</h2><p>逐句试听后点“选这版”；选择自动保存。跨镜对白共用同一个选择。</p></div><span id="choice-count" class="choice-count"></span></div><div class="voice-jumps"><button id="prev-voice" type="button">← 上一句</button><button id="next-voice" type="button">下一句 →</button><button id="next-unpicked" type="button">下一个未选</button></div><p class="picker-warning">整片播放仍是 v021 固定混音。挑选后要重新对齐语音、镜长和 BGM，才会进入新版混音。</p><div id="choice-status" role="status">正在读取已选版本…</div><div id="voice-options"></div></section>'
    page=page.replace(marker,panel+marker,1).replace('</head>','<link rel="stylesheet" href="配音挑选.css"></head>',1).replace('</body>','<script src="配音挑选.js"></script></body>',1)
    page=page.replace('白米饭 · 全片声音预览','白米饭 · 配音挑选预演').replace('静帧 + 日语配音 + BGM','静帧 + 配音对比 + BGM')
    (PREVIEW/'全片声音预演.html').write_text(page,encoding='utf-8')
    # Keep stable prompts and visual timing; remove audio players and their private file metadata from the new generation board.
    shutil.copytree(ROOT/'视频制作/生成板-v021/提示词',BOARD/'提示词',dirs_exist_ok=True)
    shutil.copy2(ROOT/'视频制作/生成板-v021/结构核验.json',BOARD/'结构核验.json')
    page=OLD_BOARD.read_text('utf-8')
    a='<script id="data" type="application/json">';b='</script>'
    start=page.index(a)+len(a);end=page.index(b,start);data=json.loads(page[start:end])
    data['version']='v022'
    for batch in data['batches']:
        for dialogue in batch['dialogue']:dialogue.pop('returned_audio',None)
    page=page[:start]+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+page[end:]
    injected=re.compile(r'<script>\s*const beforeAudioCard=dialogueCard;.*?</script>',re.S)
    assert len(injected.findall(page))==1
    extra='''<script>const beforeVoiceLink=dialogueCard;dialogueCard=function(b,c,i){let card=beforeVoiceLink(b,c,i);return card.slice(0,card.lastIndexOf('</article>'))+`<p><a href="../../后期/配音挑选-v022/全片声音预演.html#t=${b.film_start+c.start}">在预演版比较这句配音</a></p></article>`;};document.querySelector('header').insertAdjacentHTML('beforeend',`<p class="notice">配音版本请在<a href="../../后期/配音挑选-v022/全片声音预演.html">预演版逐句试听和挑选</a>；此处的镜长与对白窗口仍为 v021 基线，待选定后重新对位。</p>`);render();</script>'''
    page=injected.sub(lambda _:extra,page)
    old=quote('后期/语音节奏定版-v021/全片声音预览.html',safe='/')
    new=quote('后期/配音挑选-v022/全片声音预演.html',safe='/')
    page=page.replace(old,new)
    (BOARD/'生成板.html').write_text(page,encoding='utf-8')
    print(json.dumps(dict(cues=len(cues),options=sum(len(c['options']) for c in cues),groups=len(groups),group_options=sum(len(g['options']) for g in groups)),ensure_ascii=False))

if __name__=='__main__': main()
