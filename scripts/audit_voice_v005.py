"""Bounded file/text/timing audit. Signal measurements are not listening approval."""
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'后期/日语配音修正-v005'


def main():
    data=json.loads((ROOT/'后期/制作工作台-v023/工作台数据.json').read_text('utf8'))
    specs=json.loads((OUT/'生成提示词.json').read_text('utf8'))
    rows=[]
    for spec in specs:
        cue=next(c for c in data['cues'] if c['id']==spec['cue_id'])
        target=(cue['revision'] or cue)['ja']
        assert spec['ja']==target
        files=[]
        for folder in ['干声','原生']:
            p=next((OUT/folder).glob(spec['cue_id']+'__*.wav'))
            probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
            stream=probe['streams'][0]
            pcm=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ac','1','-ar','40000','pipe:1']),dtype='<f4')
            active=np.flatnonzero(np.abs(pcm)>.01)
            rms=float(np.sqrt(np.mean(pcm[-400:]**2)))
            files.append(dict(kind=folder,path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                              seconds=len(pcm)/40000,sample_rate=int(stream['sample_rate']),channels=stream['channels'],
                              peak=float(np.abs(pcm).max()),tail_10ms_rms_dbfs=round(20*np.log10(max(rms,1e-10)),3),
                              tail_below_minus40_db_seconds=round((len(pcm)-1-active[-1])/40000,6) if len(active) else len(pcm)/40000,
                              complete_decode=True,nonfinite_samples=int(np.count_nonzero(~np.isfinite(pcm))),
                              samples_at_fullscale=int(np.count_nonzero(abs(pcm)>=1))))
        rows.append(dict(cue=cue['id'],location=cue['location'],role=cue['role'],text=target,
                         delivery_text_matches=True,baseline_window=round(cue['end']-cue['start'],6),
                         duration_change=round(files[0]['seconds']-(cue['end']-cue['start']),6),files=files,
                         flag='native_tail_needs_listening' if files[1]['tail_10ms_rms_dbfs']>-40 else None))
    report=dict(scope='v005 nine delivered cues',rows=rows,decode_pass=True,
                text_check='delivery specifications only; no ASR or listening claim',
                listening_completed=False,tail_attention=[x['cue'] for x in rows if x['flag']],
                voice_choices_changed=False,timing_remixed=False)
    (OUT/'复查-文件与时长.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    lines=['# v005 配音复查', '', '9句干声和9句原生文件均可完整解码；实际哈希与候选索引一致。交付提示词与本轮7句改词及2句原词一致。没有进行逐字ASR或实际听审，不能以文件/文字核验替代发音、声线或表演通过。', '',
           '| 位置 | 角色 / 台词 | 新干声秒数 | 旧窗口秒数 |', '|---|---|---:|---:|']
    for row in rows:
        lines.append(f"| {row['location']} | {row['role']}：{row['text']} | {row['files'][0]['seconds']:.3f} | {row['baseline_window']:.3f} |")
    lines+=['', '## 需要注意', '',
            '第23批第3镜 GPT分工长句：原生7.180秒，干声7.161秒；原生最后10毫秒仍约-31.6dBFS，干声约-30.1dBFS，结尾没有明确静默。需听原生末句「彼女を守って」判断是否收尾完整，不能根据波形断言缺字，也不能用补静音掩盖问题。', '',
            '9句不能直接套回旧时码。例如祈愿从旧3.80秒变为6.817秒，月背唤醒从旧0.98秒变为2.340秒。后续应先按原速完整声音重新分配镜头和音乐窗口，保留既定留白。', '',
            '## 接线修正', '',
            '原来只向工作台派生数据注入v005，保存API仍读取v022索引，造成9句都能显示但不能选择；重建也会丢失。本轮接入共享候选索引及两个构建入口，沿用原候选ID，以实际文件计算哈希与精确时长。9条干声和9条原生均可定位。', '',
            '每个候选携带实际交付文本，新文/旧文按文本匹配判断。新录直接显示“先听这一版”，选择后显示“新稿已选 · 待对位”，旧作者选择未自动覆盖。月背尾音听审标记保留在候选卡上。', '',
            '结论：9句文件已齐，接线修正后可逐句试听选择；当前尚不能宣称全片声音或最终生成时码已验收。']
    (OUT/'复查结论.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    print(json.dumps(dict(files=18,decoded=True,tail_attention=report['tail_attention'],text_specs_match=True,listening_completed=False),ensure_ascii=False))


if __name__=='__main__':main()
