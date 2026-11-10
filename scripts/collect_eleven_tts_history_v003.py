"""Collect only exact project texts from official history; no synthesis."""
from pathlib import Path
import os,json,subprocess,urllib.request,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'声音/ElevenLabs-正式台词试听-v003'
env=os.environ.copy()
for line in (Path.home() / '.codex/local/content-tools/elevenlabs/.env.local').read_text(encoding='utf-8-sig').splitlines():
    if line.strip().startswith('ELEVENLABS_API_KEY='):env['ELEVENLABS_API_KEY']=line.split('=',1)[1].strip().strip('"').strip("'")
p=subprocess.run(['npx.cmd','--offline','@elevenlabs/cli@1.7.1','history','list','--page-size','40','--format','json','--no-retry'],env=env,capture_output=True,timeout=50)
p.check_returncode();history=json.loads(p.stdout)
source=json.loads((ROOT/'剧本/白米饭-日语对白-v0.69.json').read_text(encoding='utf8'))
records=[]
for role in ['千问','Gemini','Grok','天使GPT','恶魔GPT','教徒']:
    lines=[x for x in source['lines'] if x['role']==role and x.get('ja') and x['status'] not in ['merged_not_spoken','removed_not_spoken','removed_from_draft']]
    text='\n'.join(x['ja'] for x in lines)
    # The priest's assistant has an explicit reading expansion in the web input.
    variants=[text,text.replace('生贄','いけにえ')]
    matches=[h for h in history['history'] if h.get('dialogue') and len(h['dialogue'])==1 and h['dialogue'][0]['text'] in variants]
    matches.sort(key=lambda h: (h['model_id']!='eleven_v4',h['date_unix']))
    previews=[]
    for i,h in enumerate(matches,1):
        hid=h['history_item_id'];assert hid.isalnum()
        path=OUT/f'{role}-直配-{hid}.mp3'
        if not path.exists():
            req=urllib.request.Request(f'https://api.elevenlabs.io/v1/history/{hid}/audio',headers={'xi-api-key':env['ELEVENLABS_API_KEY']})
            with urllib.request.urlopen(req,timeout=40) as response:data=response.read()
            assert len(data)>1000
            path.write_bytes(data)
        data=path.read_bytes()
        probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(path)],capture_output=True,check=True)
        decoded=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],capture_output=True).returncode==0
        previews.append({'file':path.name,'candidate':i,'history':h,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'media':json.loads(probe.stdout),'decode_ok':decoded,'adopted':False})
    if previews:
        receipt={'role':role,'status':'web_direct_tts_saved_pending_review','lines':lines,'previews':previews,'generation_count':1,'note':'One web submission can produce main and experimental variants; history records actual charge.'}
        (OUT/f'{role}-直配结果.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
        records.append({'role':role,'files':len(previews),'durations':[round(float(p['media']['format']['duration']),3) for p in previews]})
print(json.dumps(records,ensure_ascii=False))
