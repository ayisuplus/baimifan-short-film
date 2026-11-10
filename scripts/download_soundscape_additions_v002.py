"""Acquire exact audio links from the previously inspected official source catalogue."""
import json,hashlib,subprocess,requests
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'资产/声音/音效-v001'
catalog=json.loads((D/'来源/catalog.json').read_text(encoding='utf8'))
manifest=json.loads((D/'来源清单.json').read_text(encoding='utf8'));known={x['id'] for x in manifest}
for ident in ['stone-break1','waterfall-small1','water-flow1','cup-put1','stone-rolls1','water-evaporation1','water-throw-stone2']:
    if ident in known:continue
    x=next(x for x in catalog if x['url'].endswith('/'+ident+'.mp3'))
    p=D/'原始'/(ident+'.mp3')
    r=requests.get(x['url'],headers={'Referer':x['page']},timeout=90);r.raise_for_status();p.write_bytes(r.content)
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
    manifest.append({**x,'id':ident,'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'seconds':dur,'license':'効果音ラボ利用規約','license_url':'https://soundeffect-lab.info/agreement/','status':'downloaded_not_audition_verified','downloaded':'2026-10-28'})
    (D/'来源清单.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    print(ident,dur,flush=True)
