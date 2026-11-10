"""Record this task's provenance and stage only its own delivery additions."""
from pathlib import Path
import json,hashlib,subprocess,re
R=Path(__file__).resolve().parents[1];O=R/'后期/声画重构-v002';G=R/'视频制作/Metaso-H3-v005'
def git(*args,input=None):return subprocess.check_output(['git',*args],cwd=R,input=input)
staged={x for x in git('diff','--cached','--name-only','-z').decode('utf8').split('\0') if x}
assert staged<={'AGENTS.md','制作进度.md'},'Do not mix existing staged work into this commit'
records=[]
for name,original in [('CY012-上阶首帧-v003.png','exec-c6697402-de24-4430-91e7-7492c34b6d76.png'),('CY016D-下阶首帧-v003.png','exec-864de577-0845-4055-967f-40ad387beb0f.png')]:
    p=G/'参考'/name
    src=Path('C:/Users/36322/.codex/generated_images/01a17883-69dd-74f1-8f13-bbde7422c943')/original
    sha=hashlib.sha256(p.read_bytes()).hexdigest()
    assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
    records.append({'path':str(p.relative_to(R)),'original_output':str(src),'sha256':sha,'tool':'built-in imagegen','role':'corrected first frame for H3 r3 stair pickup','design_summary':'以小鱼现有角色外观和教堂场景约束短腿、蓝色毛边鞋及实际台阶接触；此处是设计摘要，不伪称原始逐字提示词。'})
(G/'首帧来源.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
prefix='''## 2026-10-28：声画重构 v002（当前工程内核验入口）

达芬奇工程《白米饭》的 `v002_Church_Sound_Reconstruction` 已保存：44批、103段、11223帧，7分47.625秒；63句完整原速选定配音、13段原速BGM、186处声音事件分6轨装配。重点修复第7–20批的过渡、说话人对应与动作节奏，并处理水滴、水面、锁具和父亲反应接头。原44批哈希未变，v001与历史候选保留。

16次局部H3调用，11条采用、5条弃用；预计805.8积分，未核实际账单。没有整批重做。入口：[工程内审阅](后期/声画重构-v002/工程内审阅.html)；[修订说明](后期/声画重构-v002/修订说明.md)。当前直接在达芬奇从第7批00:01:19:14核验；作者明确要求最终核验通过并明确要求后再导出，不自动渲染成片或导出工程。该要求前完成的第19批无声短测试仅供取证。

实际时间线、完整原速配音、媒体完整性及PCM无削波检查通过；没有冒称连续听审、音素口型或最终观感已经验收。以下为历史入口与状态，不覆盖本节。

'''
for name in ['AGENTS.md','制作进度.md']:
    p=R/name;working=p.read_text(encoding='utf8');base=git('show','HEAD:'+name).decode('utf8')
    if not working.startswith(prefix):p.write_text(prefix+working,encoding='utf8')
    blob=git('hash-object','-w','--stdin',input=(prefix+base).encode('utf8')).decode().strip()
    git('update-index','--add','--cacheinfo','100644',blob,name)
name='00_打开项目.html';p=R/name;working=p.read_text(encoding='utf8');base=git('show','HEAD:'+name).decode('utf8')
notice='<aside style="margin:20px;padding:18px;border:2px solid #c39e63;background:#182631;color:#fff">当前：<a style="color:#a7dfff" href="后期/声画重构-v002/工程内审阅.html">声画重构 v002 · 达芬奇工程内核验</a>。63句配音、13段BGM、186处声音事件已接回；作者最终确认后再导出。</aside>'
def inject(s):
    out,n=re.subn(r'(<body\b[^>]*>)',lambda m:m[1]+notice,s,count=1,flags=re.I)
    if not n:out,n=re.subn(r'(<h1\b)',lambda m:notice+m[1],s,count=1,flags=re.I)
    assert n==1;return out
p.write_text(inject(working),encoding='utf8')
blob=git('hash-object','-w','--stdin',input=inject(base).encode('utf8')).decode().strip()
git('update-index','--add','--cacheinfo','100644',blob,name)
scripts=['prepare_church_retake_v005.py','review_pickups_v005.py','download_soundscape_additions_v002.py','measure_selected_speech_v002.py','compose_reconstruction_choices_v002.py','prepare_reconstruction_v002.py','reconform_music_v002.py','prepare_soundscape_v002.py','check_soundscape_mix_v002.py','write_resolve_reconstruction_v002.py','validate_reconstruction_v002.py','document_reconstruction_v002.py','record_reconstruction_delivery_v002.py']
paths=[R/'scripts'/s for s in scripts]
for folder in [O,G]:
    paths += [p for p in folder.rglob('*') if p.is_file() and p.suffix.lower() in {'.json','.md','.html','.py','.comp'}]
relative=[str(p.relative_to(R)).replace('\\','/') for p in paths]
git('add','--',*relative)
print('Staged this task only:',len(relative)+3,'files. Prior working changes kept outside index.')
