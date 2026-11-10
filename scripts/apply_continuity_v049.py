"""Archive image edits and update only the authorized continuity images."""
import copy,hashlib,json,shutil
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
def read(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def save(p,v):
    path=root/p;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
record=read('镜头设计/生成记录/连续性修复-v049-输入.json')
base=read(record['base']);plan=copy.deepcopy(base);shots={s['id']:s for s in plan['shots']}
folder=root/'镜头设计/图像/连续性修复-v049';folder.mkdir(exist_ok=True)
changes=[];paths={}
for row in record['items']:
    source=Path(row['source']);target=folder/row['filename'];shutil.copy2(source,target)
    with Image.open(target) as im:im.verify()
    with Image.open(target) as im:w,h=im.size
    previous=row.get('previous')
    if previous:shutil.copy2(Path(previous['source']),folder/previous['filename'])
    s=shots[row['shot']];old=copy.deepcopy(s['presentation']);old_request=s['generation_request']
    request={'engine':'built-in image_gen','date':record['date'],'shot':s['id'],'request':row['input'],'output':target.relative_to(root).as_posix(),'sha256':sha(target),'previous_request':old_request,'previous_image':old['path'],'previous_candidate':previous,'review':'technical and root visual inspection complete; independent review and author visual approval tracked separately'}
    reqpath=f'镜头设计/生成记录/连续性修复-v049/{s["id"]}-请求.json';save(reqpath,request)
    s['previous_presentation_v048r1']=old;s['previous_generation_request_v048r1']=old_request
    newpath=target.relative_to(root).as_posix();paths[old['path']]=newpath
    s['presentation'].update(path=newpath,status='v0.49连续性局部修订，待作者视觉确认')
    note='底柴与腰锁统一' if s['id']=='CY015' else '腰锁统一' if s['id']=='CY016' else '单中轴高位烛环统一；近景按机位裁出上缘'
    s['invariants'].append(note+'；本轮不改人物动作、对白或BGM。')
    s['visual_prompt']=row['input']['prompt'];s['generation_request']=reqpath
    s['refs'].append({'path':newpath,'role':'v0.49连续性修订主图；原图作为历史参考保留'})
    s['previous_final_static_review_v048r1']=s.get('final_static_review')
    s['final_static_review']={'version':'v049','scope':'authorized_prop_and_fixture_continuity_edits','status':'pending_author_visual_confirmation','changes':note,'dynamic_and_audio':'unchanged_and_not_reviewed_by_image_edit'}
    s['page_size']=[w,h];s['panel_rect_pixels']=[0,0,w,h];s['panel_region']={'x':0,'y':0,'w':1,'h':1}
    changes.append({'shot':s['id'],'before':old['path'],'after':newpath,'sha256':sha(target),'request':reqpath,'correction':note})
for scene in plan['scenes']:scene['pages']=[paths.get(p,p) for p in scene['pages']]
plan.update(version='v0.49',picture_revision='v049',report_revision='v049',title='《穿云》带图分镜 v0.49 · 吊灯、底柴与腰锁连续性修复',source_manifest=record['base'],audio_arrangement='后期/连续性修复-v049/预演编排.json')
plan['review_intro']='吊灯、脚边底柴与腰锁三项局部连续性修复；10镜换图，既定动作、对白和七首用曲保持。GPT大招优化另作讨论提案。'
plan['review_focus']='核对单中轴高位烛环、低柴与矩形腰锁；新版静帧待作者视觉确认。GPT大招仍使用上一版，提案未实施。'
plan['revision_notes']={'previous_manifest':record['base'],'modified_image_ids':[r['shot'] for r in changes],'added_ids':[],'boundary':'仅10镜局部道具/背景编辑；结构revision沿用v048验证分支，展示版号v0.49。131镜431.5秒、全部台词字幕、7首用曲与其他121镜图片不变。'}
for a,b in zip(base['shots'],plan['shots']):
    for key in ['id','scene','seconds','start_second','end_second','action','entry_state','exit_state','dialogue','dialogue_cues','subtitle_cues','source_quote']:
        assert a.get(key)==b.get(key),(a['id'],key)
assert plan['music_adoption']==base['music_adoption']
out='镜头设计/shot-plan-v0.49.json';save(out,plan)
audio=read(base['audio_arrangement']);audio.update(version='v049-picture-with-adopted-seven-tracks',shot_plan=out,shot_plan_sha256=sha(root/out));save(plan['audio_arrangement'],audio)
save('镜头设计/生成记录/连续性修复-v049/变更清单.json',{'base':record['base'],'plan':out,'changes':changes,'images':10,'shots':131,'seconds':431.5,'unchanged':'全部动作、台词、字幕、时间、作者确认BGM映射、其余121镜图片'})
snapshot=root/'镜头设计/带图分镜-终极审查-v048r1.html'
if not snapshot.exists():shutil.copy2(root/'镜头设计/带图分镜.html',snapshot)
print(json.dumps({'images':len(changes),'plan':out,'seconds':plan['total_seconds']},ensure_ascii=False))
