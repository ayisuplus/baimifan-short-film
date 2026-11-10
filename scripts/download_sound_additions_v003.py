"""Fetch identified official sound files and retain their exact provenance."""
from pathlib import Path
import requests,re,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];O=R/'资产/声音/音效-v003';O.mkdir(parents=True,exist_ok=True);D=R/'后期/导演重构-v003'
rows=[]
catalog=json.loads((R/'资产/声音/音效-v001/来源/catalog.json').read_text(encoding='utf8'))
targets=[]
for ident in ['real-down1','thunder2','punch-light2','wall-hit1']:
    x=next(x for x in catalog if x['url'].endswith('/'+ident+'.mp3'));targets.append({'id':ident,'title':x['title'],'url':x['url'],'page':x['page'],'license_url':'https://soundeffect-lab.info/agreement/'})
for num,title in [(2858,'Gear metallic lock sound'),(2799,'Metallic sword scrape'),(2794,'Heavy sword hit'),(1306,'Cinematic water metal hit')]:
    page=f'https://mixkit.co/free-sound-effects/download/{num}/?context=item+grid'
    r=requests.get(page,timeout=40);r.raise_for_status();(D/'来源'/f'mixkit-{num}-download.html').write_text(r.text,encoding='utf8')
    urls=re.findall(r'https[^\s"<>]+\.wav',r.text);assert urls
    targets.append({'id':f'mixkit-{num}','title':title,'url':urls[0],'page':'https://mixkit.co/free-sound-effects/metal/','license_url':'https://mixkit.co/license/modal/sfxFree/'})
for x in targets:
    p=O/(x['id']+('.wav' if x['url'].endswith('.wav') else '.mp3'))
    if not p.exists():
        try:
            r=requests.get(x['url'],headers={'Referer':x['page']},timeout=40);r.raise_for_status();p.write_bytes(r.content)
        except requests.RequestException as exc:
            print(x['id'],type(exc).__name__,flush=True);continue
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)]))
    rows.append({**x,'path':p.relative_to(R).as_posix(),'seconds':duration,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':'downloaded_not_auditioned'})
    (D/'新增音效来源.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
    print(x['id'],round(duration,3),flush=True)
