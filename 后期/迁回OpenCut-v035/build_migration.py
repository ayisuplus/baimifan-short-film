"""One-time v033 migration. Native Rust validates/publishes the portable backup.
No browser storage access, Resolve mutation, transcoding, or GPU calls.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import copy, hashlib, json, shutil, subprocess, uuid

OUT=Path(__file__).resolve().parent
FILM=OUT.parents[1]
APP=Path('E:/projects/媒体后期/OpenCut-classic')
BACKUPS=APP/'.local/project-backups'
REFERENCE=BACKUPS/'481c39e8-f496-413f-be47-df1b35f50cf7'
EXE=APP/'target/debug/opencut-creative.exe'
SOURCE=OUT/'migration-source'
PROJECT='baimifan-fullfilm-v035-source'
PACKAGE='baimifan-fullfilm-v035'
OLDPROJECT='79d4ad8a-fc76-49dc-9797-913ded176ff2'
OLDPACKAGE='baimifan-director-three-shots-v1'
BACKUP='baimifan-fullfilm-v035-20261101'
NAME='白米饭 · 全片画面 v035（达芬奇 v033 迁回）'

def read(p): return json.loads(p.read_text(encoding='utf8'))
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def sha(p):
 with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def native(root,command,value):
 r=subprocess.run([str(EXE),str(root),command],input=json.dumps(value,ensure_ascii=False),encoding='utf8',capture_output=True,check=True)
 v=json.loads(r.stdout); assert v.get('ok'),v
 return v['value']
def remap(v):
 if isinstance(v,list):
  for x in v: remap(x)
 if isinstance(v,dict):
  for k,x in v.items():
   if k in ('project_id','projectId','package_id','packageId','id'):
    if x==OLDPROJECT: v[k]=PROJECT
    elif x==OLDPACKAGE: v[k]=PACKAGE
   elif k=='editor_projects': v[k]=[PROJECT]
   if k not in ('provenance','source','sources'): remap(v[k])
def uid(kind,key): return str(uuid.uuid5(uuid.NAMESPACE_URL,PACKAGE+'/'+kind+'/'+key))

def probe(item):
 p=Path(item['source']); assert p.is_file(),p
 r=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],capture_output=True,encoding='utf8',check=True)
 d=json.loads(r.stdout); v=next(x for x in d['streams'] if x['codec_type']=='video')
 assert v['r_frame_rate']=='24/1' and v['avg_frame_rate']=='24/1',(p,v['r_frame_rate'])
 frames=int(v['nb_frames']); duration=frames/24
 assert item['source_in']+item['end']-item['start']<=frames
 return dict(source=str(p),size=p.stat().st_size,sha256=sha(p),frames=frames,duration=duration,width=v['width'],height=v['height'],hasAudio=any(x['codec_type']=='audio' for x in d['streams']),lastModified=round(p.stat().st_mtime*1000))

def main():
 assert not SOURCE.exists(),'Migration source already exists; do not overwrite'
 assert not (BACKUPS/BACKUP).exists(),'Completed backup already exists'
 native(BACKUPS,'backup',{'action':'verify','id':REFERENCE.name})
 live=read(OUT/'Resolve-current.json'); previous=read(FILM/'后期/迁回达芬奇-v033/Resolve迁回读回.json')
 assert live['name']=='v033_OpenCut_Picture_Return' and live['start']==0 and live['end']==9059
 assert all(live[k]==previous[k] for k in ['name','id','start','end','settings'])
 assert len(live['tracks'])==len(previous['tracks'])
 for a,b in zip(live['tracks'],previous['tracks']):
  assert len(a['items'])==len(b['items'])
  for x,y in zip(a['items'],b['items']): assert all(x[k]==y[k] for k in y)
 tracks=[t for t in live['tracks'] if t['kind']=='video']; assert len(tracks)==1 and tracks[0]['enabled']
 items=tracks[0]['items']; assert len(items)==118
 assert all(not t['items'] for t in live['tracks'] if t['kind']!='video')
 cursor=0
 for c in items:
  assert c['enabled'] and c['start']==cursor and c['end']>c['start']; cursor=c['end']
  assert c['speed']=={'Percentage':100.0}
  p=c['properties']
  for k,val in dict(Pan=0,Tilt=0,ZoomX=1,ZoomY=1,RotationAngle=0,AnchorPointX=0,AnchorPointY=0,Pitch=0,Yaw=0,FlipX=False,FlipY=False,CropLeft=0,CropRight=0,CropTop=0,CropBottom=0,Opacity=100,CompositeMode=0,DynamicZoomEnabled=False).items(): assert p[k]==val,(c['name'],k,p[k])
 with ThreadPoolExecutor(max_workers=4) as pool: media=list(pool.map(probe,items))
 assert len(set(x['source'] for x in media))==118
 print('Verified 118 source files,',sum(x['size'] for x in media),'bytes',flush=True)
 shutil.copytree(REFERENCE/'creative',SOURCE/'creative')
 shutil.copytree(REFERENCE/'package',SOURCE/'package')
 creative=SOURCE/'creative'; package=SOURCE/'package'
 (creative/'writing'/OLDPROJECT).rename(creative/'writing'/PROJECT)
 for p in [*(creative/'versions').glob('*.json'),*(creative/'writing'/PROJECT/'versions').glob('*.json'),*(creative/'asset-library/versions').glob('*.json'),*(creative/'upscale').rglob('*.json'),creative/'asset-library/import-report.json',package/'manifest.json']:
  v=read(p); remap(v); write(p,v)
 write(creative/'owner.json',{'owner':{'owner':'opencut-rust','root':'\\\\?\\'+str(creative.resolve()),'package_id':PACKAGE},'migration_source':str(REFERENCE)})
 # Package and writing history is copied as reference, never used as an inferred
 # mapping from 118 edit ordinals to CY story shots. The original prototype stays intact.
 manifest=read(package/'manifest.json');manifest['title']=NAME;write(package/'manifest.json',manifest)
 native(creative,'read',{}); native(creative,'writing',{'action':'read','project_id':PROJECT});native(package,'package',{})
 browser=read(REFERENCE/'browser.json');project=copy.deepcopy(browser['project']);now=datetime.now(timezone.utc).isoformat()
 project['id']=PROJECT; project['metadata']={'id':PROJECT,'name':NAME,'createdAt':now,'updatedAt':now,'duration':9059*5000}
 scene=project['scenes'][0];scene['id']=uid('scene','main');scene['name']='达芬奇 v033 · 完整画面';scene['createdAt']=now;scene['updatedAt']=now;scene['bookmarks']=[]
 project['currentSceneId']=scene['id'];project['scenes']=[scene];project['timelineViewState']={'playheadTime':0,'scrollLeft':0,'zoomLevel':0.12}
 template=scene['tracks']['main']['elements'][0]
 params=copy.deepcopy(template['params'])
 maintrack={'type':'video','id':uid('track','main'),'name':'完整画面 · v033 迁回','hidden':False,'muted':False,'elements':[]}
 scene['tracks']={'main':maintrack,'overlay':[],'audio':[]}
 metas=[];evidence=[]
 for c,m in zip(items,media):
  duration=c['end']-c['start'];mid=uid('media',m['source']);eid=uid('clip',c['name'])
  maintrack['elements'].append(dict(type='video',id=eid,name=c['name'],mediaId=mid,startTime=c['start']*5000,duration=duration*5000,trimStart=c['source_in']*5000,trimEnd=(m['frames']-c['source_in']-duration)*5000,sourceDuration=m['frames']*5000,hidden=False,isSourceAudioEnabled=False,params=copy.deepcopy(params)))
  metas.append(dict(id=mid,name=Path(c['source']).name,type='video',size=m['size'],lastModified=m['lastModified'],width=m['width'],height=m['height'],duration=m['duration'],fps=24,hasAudio=m['hasAudio'],mimeType='video/mp4',backupSha256=m['sha256']))
  evidence.append(dict(**m,name=c['name'],media_id=mid,element_id=eid,start_frame=c['start'],end_frame=c['end'],source_in=c['source_in'],source_out_exclusive=c['source_in']+duration,resolve_reported_source_out=c['source_out']))
 snapshot={'project':project,'media':metas,'drafts':{}}
 write(OUT/'migration-browser.json',snapshot)
 write(OUT/'source-media-evidence.json',evidence)
 native(BACKUPS,'backup',{'action':'begin','id':BACKUP,'snapshot':snapshot,'creative_root':str(creative),'package_root':str(package),'created_at':now})
 for meta,m in zip(metas,media):
  plan=native(BACKUPS,'backup',{'action':'upload','id':BACKUP,'media_id':meta['id']})
  shutil.copy2(m['source'],plan['path'])
 result=native(BACKUPS,'backup',{'action':'finish','id':BACKUP})
 verified=native(BACKUPS,'backup',{'action':'verify','id':BACKUP})
 destination=OUT/'完整工程备份'/BACKUP
 shutil.copytree(BACKUPS/BACKUP,destination)
 native(destination.parent,'backup',{'action':'verify','id':BACKUP})
 write(OUT/'migration-package-evidence.json',{'backup_id':BACKUP,'backup_directory':str(destination),'native_result':result,'verified':verified,'resolve_snapshot_sha256':sha(OUT/'Resolve-current.json'),'resolve_project_backup_sha256':sha(OUT/'migration-source.drp'),'clip_count':118,'frames':9059,'fps':24,'sources_bytes':sum(x['size'] for x in media),'native_reference_origin':str(REFERENCE),'timeline_bindings':'Not inferred: edit clips can contain multiple CY shots. Reference manuscript/library retained separately.','no_transcode':True,'no_generation':True})
 print(json.dumps({'backup':BACKUP,'files':len(verified['files']),'bytes':verified['bytes'],'copy':str(destination)},ensure_ascii=False),flush=True)

if __name__=='__main__': main()
