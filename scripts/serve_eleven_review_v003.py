"""Loopback-only review and explicit author-choice persistence."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import json,datetime,os,threading
LOCK=threading.Lock()
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'声音/ElevenLabs-正式台词试听-v003'
CHOICE=OUT/'作者选择.json'
ENDPOINT='/api/voice-choice-v003'
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
    def reply(self,status,obj):
        b=json.dumps(obj,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(b)
    def do_GET(self):
        if self.path==ENDPOINT:return self.reply(200,json.loads(CHOICE.read_text(encoding='utf8')))
        return super().do_GET()
    def do_POST(self):
        if self.path!=ENDPOINT:return self.reply(404,{'error':'not found'})
        if self.headers.get('Origin') not in (None,f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'):return self.reply(403,{'error':'origin'})
        if not self.headers.get('Content-Type','').startswith('application/json'):return self.reply(415,{'error':'json required'})
        try:
            size=int(self.headers.get('Content-Length','0'));assert 0<size<10000
            request=json.loads(self.rfile.read(size));role=request['role'];candidate=request.get('candidate');note=request.get('note','');assert isinstance(note,str) and len(note)<=2000
            entries=json.loads((OUT/'试听数据.json').read_text(encoding='utf8'));entry=next(x for x in entries if x['role']==role)
            assert 'candidate' not in request or (type(candidate) is int and candidate in [0]+[x['candidate'] for x in entry['previews']])
            assert entry['kind']!='retained'
        except (AssertionError,ValueError,KeyError,StopIteration):return self.reply(400,{'error':'invalid choice'})
        with LOCK:self.persist(request,entry,role,candidate,note)
    def persist(self,request,entry,role,candidate,note):
        current=json.loads(CHOICE.read_text(encoding='utf8'))
        stamp=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
        record={'candidate':candidate,'note':note,'status':'needs_revision' if candidate==0 else 'author_selected','time':stamp,'evidence':'author clicked review page','timeline_adopted':False}
        if 'candidate' not in request:
            record={**current.get(role,{'status':'pending','timeline_adopted':False}),'note':note,'note_saved_at':stamp,'note_evidence':'review page note edit'}
        if candidate:record['audio']=next(x['file'] for x in entry['previews'] if x['candidate']==candidate)
        with (OUT/'选择历史.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps({'role':role,'previous':current.get(role),'new':record},ensure_ascii=False)+'\n')
        current[role]=record;temp=CHOICE.with_suffix('.tmp');temp.write_text(json.dumps(current,ensure_ascii=False,indent=2),encoding='utf8');os.replace(temp,CHOICE)
        self.reply(200,current)
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',8971),Handler).serve_forever()
