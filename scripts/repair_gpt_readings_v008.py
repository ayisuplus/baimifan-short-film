"""Explicit kana repairs prompted by two independent unprompted ASR passes."""
from pathlib import Path
import json,hashlib,urllib.request,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'声音/缺口补齐-v008'
texts={'VO-CY007-01':'教会には手を出さない。そう約束したの。','VO-CY026A-01':'センモン、ひとだすけに、つきあって。','VO-CY026D1-01':'キミ、クロードがあぶない。'}
keypath=Path.home() / '.codex/local/content-tools/elevenlabs/.env.local'
key=next(x.split('=',1)[1].strip().strip('"').strip("'") for x in keypath.read_text(encoding='utf-8-sig').splitlines() if x.startswith('ELEVENLABS_API_KEY='))
for ident,text in texts.items():
 p=OUT/(ident+'-r2-结果.json');assert not p.exists()
 original=json.loads((OUT/(ident+'-结果.json')).read_text(encoding='utf8'))
 d={**original,'status':'outcome_unknown_do_not_repeat','generation_revision':2,'repair_reason':'Two unprompted recognizers found similar lexical deviation or inserted filler; use explicit reading and remove ambiguous ellipsis','previous_receipt':ident+'-结果.json','body':{'text':text,'model_id':'eleven_multilingual_v2','language_code':'ja'}}
 for k in ['file','sha256','bytes','media','decode_ok','request_id','character_cost_header']:d.pop(k,None)
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
 req=urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/'+d['voice_id'],data=json.dumps(d['body'],ensure_ascii=False).encode(),headers={'xi-api-key':key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=60) as res:
  audio=res.read();assert 'audio' in res.headers.get('Content-Type','')
  d.update(request_id=res.headers.get('request-id'),character_cost_header=res.headers.get('character-cost'))
 file=OUT/(ident+'__GPT-r2.mp3');file.write_bytes(audio)
 d.update(status='saved_pending_review',file=file.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(audio).hexdigest(),bytes=len(audio),decode_ok=subprocess.run(['ffmpeg','-v','error','-i',str(file),'-f','null','-'],capture_output=True).returncode==0)
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
 print(ident,'saved r2',flush=True)
