"""Read-only three-shot projection through the existing Director Desk adapter.

No generation, Resolve access or author-choice writes. Media is a local package.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TOOLKIT = ROOT.parents[1] / 'OpenCut/toolkit/compat/creative-workbench/app'
sys.path.insert(0, str(TOOLKIT))
from store import Store
from import_board import import_board
from studio import studio_view
from writing import initialize_writing

OUT = ROOT / '后期/OpenCut导演台原型-v001'
PACKAGE = OUT / 'package'
BOARD = '后期/制作工作台-v025/工作台数据.json'
SCRIPT = '剧本/白米饭-场景剧本-v0.69.md'
FROZEN = '视频制作/LibTV-H3-v001/GB004-冻结执行.json'
VIDEO = '后期/独立剪辑-v017/03_接小鱼与GPT对话.mp4'
SHOT_IDS = ['CY006', 'CY007', 'CY008']

def read(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8-sig'))

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

def main():
    PACKAGE.mkdir(parents=True, exist_ok=True)
    (PACKAGE/'media').mkdir(exist_ok=True)
    (OUT/'.gitignore').write_text('.local/\npackage/media/\n', encoding='utf-8')
    owned = [BOARD, SCRIPT, FROZEN, '剧本/白米饭-日语对白-v0.69.json',
             '后期/独立剪辑-v017/剪辑清单.json', '后期/宫殿调色-v014/after.json',
             '后期/迁回达芬奇-v033/迁移剪辑清单.json']
    before = {p:sha(ROOT/p) for p in owned}
    store = Store(OUT/'导演台')
    store.directory.mkdir(parents=True,exist_ok=True)
    (store.directory/'.gitignore').write_text('runtime.local.json\nserver.*.log\nwrite.lock\nhistory/\n',encoding='utf-8')
    if not store.path.exists():
        store.init('白米饭 · OpenCut 三镜资料试用', 'story')
    rust_owned = (store.directory / 'opencut-owner.json').exists()
    if not rust_owned:
        import_board(store, ROOT, BOARD, script_path=SCRIPT)
    view = studio_view(store.root, store.read())
    execution = read(FROZEN)
    frozen = execution['batch']
    script = (ROOT/SCRIPT).read_text(encoding='utf-8-sig')
    lines = {x['id']:x for x in read('剧本/白米饭-日语对白-v0.69.json')['lines']}
    media = {}
    def register(rel, label):
        path = (ROOT/rel).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError(f'Missing or outside project: {rel}')
        digest = sha(path)
        key = digest[:24]
        target = PACKAGE/'media'/(key+path.suffix.lower())
        if not target.exists() or sha(target)!=digest:
            shutil.copyfile(path, target)
        media[key] = dict(path=target.relative_to(PACKAGE).as_posix(), sha256=digest,
                          source=path.relative_to(ROOT).as_posix(), label=label)
        return key
    video = register(VIDEO, 'v033 保留的宫殿对白片段 · 含 v017 已有声音')
    after = read('后期/宫殿调色-v014/after.json')
    ambience = next(t for t in after['tracks'] if t['type']=='audio' and t['index']==5)['items'][0]
    # Extract a short reference from the existing stem; never synthesize audio.
    amb = OUT/'.local/宫殿环境声-14秒.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(946/24),'-i',ambience['path'],
                    '-t','14','-vn','-c:a','pcm_s16le',str(amb)],check=True)
    ambkey=register(amb.relative_to(ROOT).as_posix(),'历史宫殿环境声 · 14秒试听')
    music = next(m for m in view['music'] if m['music_id']=='BGM-CY-KH-05')
    music_key = register(music['path'], '历史配乐候选 · 本原型未铺入时间线')
    shots=[]
    bounds=[(0,151),(151,234),(234,336)]
    for sid,(start,end) in zip(SHOT_IDS,bounds):
        shot = next(s for s in view['shots'] if s['id']==sid)
        cue_id='VO-'+sid+'-01'
        line=lines[cue_id]
        cue=next(c for t in after['tracks'] if t['type']=='audio' for c in t['items'] if (c.get('name')or'').startswith(cue_id))
        audio=register(Path(cue['path']).relative_to(ROOT).as_posix(),cue_id+' · v009 装配录音')
        refs=[]
        for ref in frozen['references']:
            if ref.get('kind')=='identity' or ref.get('shot_id')==sid or Path(ref['path']).stem==sid:
                refs.append(dict(media=register(ref['path'], ref.get('purpose',sid)),
                                 label=ref.get('purpose',sid), status=ref.get('status',''),
                                 source=ref['path']))
        # Exact cue anchors in the current source, not a fabricated summary.
        starts = [script.index('**小鱼** · `VO-CY006-01`'),
                  script.index('她看了孩子一会儿，目光迟疑'),
                  script.index('**小鱼** · `VO-CY008-01`'),
                  script.index('### 王宫内心戏（作者已采用）')]
        index=SHOT_IDS.index(sid)
        left,right=starts[index:index+2]
        shots.append(dict(id=sid,title=shot['title'], writingGroup='GB004', action=shot['generation_row']['action'],
            camera=shot['generation_row']['camera'], story=script[max(left,0):right].strip(),
            storySource=SCRIPT, prompt=execution['request']['prompt'], promptSource=FROZEN,
            promptLabel='GB004 · LibTV H3 v001 · 实际提交的冻结输入（整批三镜）',
            warning='当前剧本 v0.69 已修改对白与动作；旧回片及冻结提示词未同步。资料查看不代表重新采用。',
            references=refs, dialogue=dict(id=cue_id,role=line['role'],ja=line['ja'],zh=line['zh_back_translation']),
            sounds=[dict(kind='配音',label='v009 装配录音 · 可独立试听',media=audio),
                    dict(kind='环境',label='历史宫殿环境声 · 参考试听',media=ambkey),
                    dict(kind='BGM',label='历史配乐候选 · 未铺入原型',media=music_key)],
            soundDesign=shot['generation_row'].get('effects',''),
            clip=dict(media=video,sourceIn=start/24,duration=(end-start)/24,sourceDuration=14,width=1344,height=768,fps=24),
            provenance=dict(board=BOARD,workbenchShotId=sid,workbenchRevision=view['project_revision'],
                            currentPicture='达芬奇 v033 所用 v017 宫殿对白成片源，按已保存剪点分成三段',
                            clipRangeFrames=[start,end])))
    manifest=dict(schemaVersion=1,id='baimifan-director-three-shots-v1',title='白米饭 · OpenCut 创作三镜原型',
                  fps=24,shots=shots,media=media,sources=before,
                  note='独立试用工程；画面与已有混音来自 v033 所用宫殿对白源。BGM仅作资料试听。')
    write(PACKAGE/'manifest.json',manifest)
    if not rust_owned:
        initialize_writing(store,manifest)
        from prepare_opencut_screenplay import prepare
        prepare()
    write(OUT/'.local/workbench.json',dict(cli=str(TOOLKIT/'cli.py'),root=str(store.root)))
    assert before=={p:sha(ROOT/p)for p in owned},'Source files changed'
    write(OUT/'构建核验.json',dict(shots=SHOT_IDS,frames=336,seconds=14,media=len(media),
                                source_files_unchanged=True,sources=before,adapter='creative-workbench.import_board + studio_view'))
    print(json.dumps(dict(package=str(PACKAGE),shots=SHOT_IDS,media=len(media)),ensure_ascii=False))

if __name__=='__main__': main()
