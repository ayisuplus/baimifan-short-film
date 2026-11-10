"""Register delivered v005 audio in the index shared by UI, saves and rebuilds."""
import hashlib
import json
import wave
from urllib.parse import quote


def merge_v005(manifest, root):
    folder = root/'后期/日语配音修正-v005'
    if not (folder/'生成提示词.json').is_file():
        return manifest
    delivery = json.loads((folder/'生成提示词.json').read_text('utf-8-sig'))
    revisions = {c['id']: c for c in json.loads((root/'剧本/对白修订-v0.64-候选.json').read_text('utf8'))['cues']}
    cues = {c['id']: c for c in manifest['cues']}
    for item in delivery:
        cid=item['cue_id'];cue=cues[cid]
        assert item['ja']==revisions.get(cid, cue)['ja'], f'Text mismatch: {cid}'
        for kind in ['干声', '原生']:
            files=list((folder/kind).glob(cid+'__*.wav'))
            assert len(files)==1, (cid,kind,files)
            file=files[0];path=file.relative_to(root).as_posix()
            with wave.open(str(file),'rb') as wav:
                seconds=wav.getnframes()/wav.getframerate()
            raw=kind=='原生'
            # Keep IDs already present in the delivered workbench stable.
            oid='opt-v005-'+('raw-' if raw else '')+hashlib.sha1(cid.encode()).hexdigest()[:16]
            flags=[]
            if cid=='VO-CY026D-01':
                flags=['需听审末句「守って」尾音：原生文件最后10ms仍有约-31.6dBFS信号，不能据此认定断词，但未确认自然收尾。']
            option=dict(id=oid,path=path,url='../../'+quote(path,safe='/'),
                        label='v005 重录原生' if raw else 'v005 重录干声',
                        note=f"交付文本：{item['ja']}；新录音待逐字及表演听审。"+(' 原生完整文件，音量与干声不同。' if raw else ''),
                        selectable=True,sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
                        seconds=round(seconds,6),raw=raw,text_ja=item['ja'],text_zh=item['zh'],
                        text_version='v0.64-proposal' if cid in revisions else 'v0.63',
                        delivery_version='v005',review_flags=flags)
            cue['options']=[o for o in cue['options'] if o['path']!=path and o['id']!=oid]+[option]
    return manifest
