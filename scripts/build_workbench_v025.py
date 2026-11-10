"""Join the frozen alignment and current author choices without changing either."""
import copy
import json
import re
from pathlib import Path
from urllib.parse import quote
from prepare_generation_v025 import ROOT, OUT as BOARD, FIX, SOURCE, load, write, sha

OUT='后期/制作工作台-v025'

def main():
    wb=copy.deepcopy(load('后期/制作工作台-v023/工作台数据.json'))
    source=load(SOURCE); sm={s['id']:s for s in source['shots']}
    board=load(BOARD+'/展开数据.json'); vp=load(FIX+'/配音对位方案.json')
    mix=load(FIX+'/实际BGM剪辑.json'); aligned=load(FIX+'/本轮对位采用.json')
    chosen={x['cue_id']:x for x in aligned['items']}; tc={c['id']:c for c in vp['cues']}
    shots={s['id']:s for s in wb['shots']}
    for sid,s in shots.items():
        src=sm[sid]
        s.update(start=src['start_second'],end=src['end_second'],
                 states=[dict(time=src['start_second']+x['offset'],image='../../'+quote(x['path'],safe='/'),label=x['label']) for x in src.get('review_state_sequence',[])])
    for c in wb['cues']:
        t=tc[c['id']]; a=chosen[c['id']]
        opt=next(x for x in c['options'] if x['path']==a['path'] and x['sha256']==a['sha256'])
        c.update(start=t['timeline_start'],end=t['timeline_end'],visual_shots=t['visual_shots'],
                 aligned_option=opt,alignment_only=a['alignment_only'],original_choice=a['original_choice'],
                 current_path=a['path'],audio_state='aligned_pending_review')
    for number,b in enumerate(board['batches'],1):
        b.update(number=number,submission_state='retimed_inputs_prepared_not_submitted')
        for j,sid in enumerate(b['shot_ids'],1):
            s=shots[sid]
            s.update(batch_number=number,batch_id=b['id'],batch_shot_number=j,display_name=f'第{number}批 · 第{j}镜',generation_row=next(r for r in b['rows'] if r['id']==sid))
            s['cue_ids']=[c['id'] for c in wb['cues'] if c['start']<s['end'] and c['end']>s['start']]
        b['revision_ids']=list(dict.fromkeys(cid for sid in b['shot_ids'] for cid in shots[sid]['cue_ids'] if next(c for c in wb['cues'] if c['id']==cid)['revision']))
    for c in wb['cues']:c['location']=shots[c['shot']]['display_name']
    wb.update(version='v025',duration=source['total_seconds'],timing_state='selected_voice_and_new_text_aligned',
              audio={k:'../../'+quote(FIX+'/'+name,safe='/') for k,name in [('bgm','BGM试听.mp3'),('mix','全片声音预览.mp3')]},
              batches=board['batches'],music=mix['cues'],silences=mix['silences'],
              sources={p:sha(p) for p in [SOURCE,BOARD+'/展开数据.json',FIX+'/实际BGM剪辑.json',FIX+'/本轮对位采用.json']})
    wb['summary'].update(shots=133,batches=len(board['batches']),selected=63,aligned=63,rejected_ids=[],valid_audio_hashes=63,revision_batches=sorted({shots[c['shot']]['batch_number'] for c in wb['cues'] if c['revision']}),alignment_only_ids=[x['cue_id'] for x in aligned['items'] if x['alignment_only']])
    write(OUT+'/工作台数据.json',wb)
    write(OUT+'/选择与返工核验.json',dict(state='63_cues_aligned',original_choices_preserved=True,choices_sha256=aligned['choices_source_sha256'],alignment_only=wb['summary']['alignment_only_ids'],timing_source=SOURCE,video_generated=False))
    (ROOT/OUT/'台词修订与配音交接.md').write_text('# v025声音与生成输入交接\n\n63句已按完整文件原速对位，7句新词已写入执行稿。Kimi月背回应和GPT祈愿使用现有v005：作者授权用于对位；原选旧版保留音色参考。原选择JSON没有被覆盖。\n\n本轮混音及全部提示词对应镜头源v0.65，133镜、44批、490.022729秒。后续改选不会自动修改已渲染混音，页面将提示需要重新对位。\n\n详细检查见[验证结果](../生成收口-v025/验证结果.json)，旧v023工作台保持历史基线。\n','utf8')
    print(json.dumps(wb['summary'],ensure_ascii=False))

if __name__=='__main__':main()
