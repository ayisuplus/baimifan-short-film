"""Reconcile returned Japanese text with the execution board; never edit audio."""
import copy,csv,hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'视频制作/生成板-v011'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    OUT.mkdir(exist_ok=True)
    old=ROOT/'视频制作/生成板-v010'
    board=load(old/'展开数据.json');plan=load(old/'批次计划.json')
    csvpath=ROOT/'后期/日语配音交接-v001/台词与回交表.csv'
    with csvpath.open(encoding='utf-8-sig',newline='') as f:returned=list(csv.DictReader(f))
    cues=[(b,c,i) for b in board['batches'] for i,c in enumerate(b['dialogue'])]
    assert len(cues)==len(returned)==61
    loc=load(ROOT/'视频制作/生成板-v009/日语译配.json')
    loc.update(status='returned_audio_text_pending_listening_and_timing',note='日语对白逐句采用回交表的日语最终稿，保留中文原意。61条声音已交回；存在超窗及咏唱切分待核，不等于逐字听审或口型验收。',translations={},timing_reviews={},delivery_csv=csvpath.relative_to(ROOT).as_posix(),delivery_csv_sha256=sha(csvpath))
    audit=load(old/'对白复核.json')
    audit.update(version='v011',date='2026-10-26',status='japanese_return_reconciled_pending_audio_fixes',migration='japanese_audio_return',board_source='视频制作/生成板-v010/展开数据.json',board_sha256=sha(old/'展开数据.json'),review_scope='文本与画面对照、回交覆盖、实测发声与原预算对照；不代表61句已逐字听审。',summary='61条对白使用日语回交文本，原镜序与预算保持。语义基本衔接；配音时长、连续母版插空与原曲卡点存在待办，暂不可冻结。',review_fixes=['全61条由英语执行稿同步为日语回交稿。','旧Breeze英语路线从当前执行要求移除。','逐句显示实际音频与原预算，保留未通过时长项。'],issues=[])
    audio=[]
    for (batch,cue,ci),row,review in zip(cues,returned,audit['cues']):
        assert (row['批次'],row['镜号'],row['中文原意'])==(batch['id'],cue['shot_id'],cue['source_text'])
        assert (review['batch_id'],review['cue_index'])==(batch['id'],ci)
        zh=row['中文原意'];ja=row['日语最终稿'].strip();assert ja
        if zh in loc['translations']:assert loc['translations'][zh]==ja
        loc['translations'][zh]=ja
        duration=float(row['实际文件时长秒']);start=float(row['实际发声开始秒']);end=float(row['实际发声结束秒']);budget=cue['end']-cue['start'];span=end-start
        path='后期/日语配音交接-v001/成品-v001/干声/'+row['输出文件名'];assert (ROOT/path).is_file()
        state='speech_over_budget' if span>budget+0.2 else ('timing_margin_check' if span>budget+0.02 else 'file_padding_over_budget' if duration>budget+0.02 else 'within_budget_pending_listening')
        note=(f'回交能量估计发声区间约{span:.2f}秒 / 原预算{budget:.2f}秒；'+('发声本身超窗超过0.2秒，须重新对位、重录或另审改时，不得自动加速/截字。' if state=='speech_over_budget' else '与预算差不足0.2秒，属临界对齐项；须结合词尾与画面检查，不直接判为必须重录。' if state=='timing_margin_check' else '文件余白超过预算，需按词首词尾试听修剪，不可直接截到预算。' if state=='file_padding_over_budget' else '时长可放入预算；字词、情绪及口型仍待听审。'))
        review.update(current_text=ja,language='Japanese',notes=[note],issue_ids=[],delivery=row['表演语气'],listener=row['听话对象'],intention=row['意图'])
        if review['offscreen']:review['notes'].append('画外/嘴部未入画；说话者仍是所列角色，不让画内人物代说。')
        if state!='within_budget_pending_listening':loc['timing_reviews'].setdefault(batch['id'],[]).append(row['角色']+'「'+ja+'」：'+note)
        info=dict(cue_id=row['台词ID'],batch_id=batch['id'],cue_index=ci,shot_id=cue['shot_id'],speaker=row['角色'],text=ja,path=path,sha256=sha(ROOT/path),file_seconds=duration,speech_start=start,speech_end=end,speech_seconds=round(span,3),budget_seconds=round(budget,6),state=state,note=note,master=row['连续母版文件及区间'],delivery_status=row['交付状态'],transcript_verified=False)
        audio.append(info)
    assert len(loc['translations'])==60
    assert ''.join(loc['continuous_line_parts'].values())==loc['translations']['统御万千深流的水之灵啊，']
    write(OUT/'日语译配.json',loc)
    audit['localization_sha256']=sha(OUT/'日语译配.json')
    write(OUT/'对白复核.json',audit)
    write(OUT/'日语音频映射.json',dict(csv=csvpath.relative_to(ROOT).as_posix(),csv_sha256=sha(csvpath),scope='回交元数据对齐；独立技术复核见后期/收尾审查-v001',cues=audio))
    plan.update(version='v011',output='视频制作/生成板-v011',dialogue_review='视频制作/生成板-v011/对白复核.json')
    plan['navigation']['review']='后期/收尾审查-v001/收尾审查与交接.md'
    plan['sound_policy']='所有有词对白使用日语，逐字按本批台词，只说一次。画外声不得由在画人物代说，跨镜咏唱不重起。不上传配音或BGM；视频模型按日语生成对白与口型，后期使用已回交日语干声，但超窗及母版插空问题解决前不得冻结。BGM只在后期铺设。'
    plan['audio_execution'].update(dialogue_language='Japanese',localization='视频制作/生成板-v011/日语译配.json',post_voice_engine='已回交日语配音（seed-audio）',display_note='全片有词对白使用日语；61条干声已回交并可逐句试听。仅上传图片，不上传配音或BGM。存在配音超窗、母版插空与原曲卡点待办，当前是收尾审查版，不是可直接提交版。',prompt_zh='所有可辨台词只说上述日语，不朗读中文原意。按指定日语生成对白及口型，无配音参考，不新增台词。只生成对白和环境动作音，不生成BGM。',prompt_en='Japanese speech only, matching the specified Japanese dialogue and lip sync. No audio reference, extra speech or music.',replacement_note='后期使用已回交日语干声。先解决发声超窗与咏唱母版对位，再验字词、句长、重音、停顿和口型；不可承诺同词音频自动对口型。保留原片，分离或补回环境动作声。')
    plan['mix_notes']=[x for x in plan['mix_notes'] if 'Breeze' not in x]
    plan['mix_notes'].append('三段咏唱母版作为连续声线参考，不得整段贴入后假设所有停顿对齐；Claude父亲打断、Kimi显形及破窗留白按收尾审查重新对位。')
    plan['global_gaps']=[x for x in plan['global_gaps'] if '英语译配' not in x]
    plan['global_gaps']+=['日语回交稿与61条文件已绑定；发声超窗、咏唱切分/插空和逐字听审尚未通过。','无词吟唱、警戒声、喘息等按环境/表演声音另验，61条对白齐全不代表全片声音齐全。']
    plan['audio_execution']['prompt_en']='Japanese speech only, with lip sync. No audio reference, extra speech or music.'
    write(OUT/'批次计划.json',plan)
    print('Prepared Japanese v011: 61 cues; original shots, timing and audio files preserved.')

if __name__=='__main__':main()
