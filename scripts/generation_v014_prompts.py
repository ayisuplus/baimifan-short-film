"""Lossless structural reference remap and concise H3 rendering, without truncation."""
import copy,re

def n(v):return f'{v:.3f}'.rstrip('0').rstrip('.')
def compact_h3(batch,plan):
    refs=batch['references'];rows=batch['rows']
    defs=[]
    for r in refs:
        role=(r['person']+'四视图：同一人四角度，身份服饰保持') if r['kind']=='identity' else ('状态参考' if r['kind']=='state' else '构图状态，非强制首帧')
        defs.append(f"<Picture {r['slot']}>={role}")
    rules='哥特异世界动画，16:9，15秒。保持参考本色；四视图不增加人物，非当前镜中人物不入画。连续动作不重演。无字幕水印、无BGM、无额外台词。'
    people={r['person'] for r in refs if r['kind']=='identity'}
    rules+=''.join(v for name,v in plan.get('character_continuity_zh',{}).items() if name in people)
    detail=[]
    for idx,row in enumerate(rows,1):
        # These fields are source-authored, not auto-summarized or sliced to fit.
        text=f"[Shot {idx}] {n(row['start'])}–{n(row['end'])}s <Picture {row['slot']}>；画内:{'、'.join(row['visible']) or '环境'}。"
        if row['reflection']:text+='仅倒影:'+','.join(row['reflection'])+'。'
        text+=row['transition']+row['camera']+row['action']
        if row['execution']:text+=' 调度:'+row['execution']
        # Stable continuity notes carry constraints absent from brief action prose.
        if row['note']:text+=' 注意:'+row['note']
        if row['cast_note']:text+=' 人物:'+row['cast_note']
        text+=' 声音:'+row['effects']
        if row['states']:text+=' 同一镜连续状态:'+','.join(f"{n(row['start']+x['offset'])}s=<Picture {x['slot']}>({x['label']})" for x in row['states'])+'。'
        detail.append(text)
    for c in batch['dialogue']:
        mode=c['mode'] if c.get('entry_offscreen') else ('画外连续，不让在画者代说' if c['offscreen'] else '匹配口型')
        detail.append(f"{n(c['start'])}–{n(c['end'])}s {c['speaker']} {mode}:<d>[Japanese] {c['text']}</d>；仅一次。")
    if batch['used_seconds']<15:detail.append(f"{n(batch['used_seconds'])}–15s保持末态微动，无新动作台词，剪去余量。")
    text='subject_definitions:\n'+'\n'.join(defs)+'\nsummary:\n[reference generation] '+rules+'\nretention_analysis:\n身份服饰 fully_preserved；构图状态 weak_reference，按动作连续变化。\ndetailed_description:\n'+'\n'.join(detail)+'\noverall_soundscape:\n仅上列原文日语在窗口内说出；窗口含原声尾白，自然念完即闭口，不拖音填满。画外对白跨切不断；环境拟音连续。\nnon_diegetic_music:\nN/A'
    # Chinese prose uses review labels; exported H3 always uses its native notation.
    text=re.sub(r'图片(\d+)',r'<Picture \1>',text)
    return text

def repair_board(board,plan):
    for b in board['batches']:
        if b['id']=='GB019':
            removed=next(r for r in b['references'] if r.get('shot_id')=='CY024A2' and r['kind']=='composition')
            kept=next(r for r in b['references'] if r.get('shot_id')=='CY024A1' and r['kind']=='composition')
            oldslots={r['slot']:i+1 for i,r in enumerate(r for r in b['references'] if r is not removed)}
            oldslots[removed['slot']]=oldslots[kept['slot']]
            b['reference_reduction']=dict(removed=copy.deepcopy(removed),reused_path=kept['path'],reason='罩内擦汗沿用前镜双人构图；原图留在静帧预览，动作文字保留。')
            b['references'].remove(removed)
            for r in b['references']:r['slot']=oldslots[r['slot']]
            for row in b['rows']:
                row['slot']=oldslots[row['slot']]
                for st in row['states']:st['slot']=oldslots[st['slot']]
                for k,v in row.items():
                    if isinstance(v,str):row[k]=re.sub(r'图片(\d+)',lambda m:'图片'+str(oldslots[int(m[1])]),v)
            for name,p in b['prompts'].items():
                pattern=r'@图片(\d+)' if name=='seedance25' else r'<Picture (\d+)>'
                b['prompts'][name]=re.sub(pattern,lambda m:('@图片'+str(oldslots[int(m[1])])) if name=='seedance25' else f'<Picture {oldslots[int(m[1])]}>',p)
            # Remove the redundant definition after remapping, never its action row.
            p=b['prompts']['seedance25'];p='\n'.join(line for line in p.splitlines() if not ('构图、空间与代表状态：' in line and removed['purpose'] in line and line.startswith('@图片')))
            b['prompts']['seedance25']=p+'\n罩内安抚的最后一镜沿用前镜双人构图，近取Kimi伸手给Claude擦汗；不删除擦汗动作。'
        if b['id']=='GB004M':
            b['prompts']['seedance25']=b['prompts']['seedance25'].replace('不切成定格图，不用人物整体淡入代替物质变化。','背景与成人本体始终使用同一冻结底板；只动画两只分身，显现后不重复出现。')
        if b['id']=='GB005':
            c=next(c for c in b['dialogue'] if c['shot_id']=='CY009');old=c['mode']
            c.update(offscreen=False,entry_offscreen=True,mode='仅起声在画外打断，立即切回小鱼后由她本人对嘴说完；其他角色不代说')
            b['prompts']['seedance25']=b['prompts']['seedance25'].replace(old,c['mode'])
        b['prompts']['seedance25']+='\n对白窗口包含原声词尾与留白；自然念完即闭口，余下保持表演，不拖音填满窗口。'
        b['prompts']['minimax-h3']=compact_h3(b,plan)
        for name,p in b['prompts'].items():
            b['models'][name]['chars']=len(p)
            b['models'][name]['image_count']=len(b['references'])
            # Capacity issues are recomputed from the final exported text and input set.
            b['models'][name]['issues']=[x for x in b['models'][name]['issues'] if not ('字符' in x and '限制' in x) and not ('张参考超过' in x)]
            contract=plan['model_contracts'][name]
            if len(p)>contract.get('max_chars',10**9):b['models'][name]['issues'].append(f"提示词{len(p)}字符超过{contract['max_chars']}字符；此对照模板不可提交，采用本批Seedance模板。")
            if len(b['references'])>contract['max_images']:b['models'][name]['issues'].append(f"本批{len(b['references'])}张参考超过{contract['max_images']}图；此对照模板不可提交。")
            pattern=r'@图片(\d+)' if name=='seedance25' else r'<Picture (\d+)>'
            assert set(map(int,re.findall(pattern,p)))==set(range(1,len(b['references'])+1)),b['id']
