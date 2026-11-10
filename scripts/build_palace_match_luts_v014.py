"""Reproducible bounded display-referred corrections for the existing Rec.709 shots."""
from pathlib import Path
import json, math, shutil, hashlib
R=Path('E:/projects/内容创作/故事短片/白米饭');O=R/'后期/宫殿调色-v014'
L=O/'LUT';L.mkdir(parents=True,exist_ok=True)
D=Path('C:/ProgramData/Blackmagic Design/DaVinci Resolve/Support/LUT/MCP')
D.mkdir(parents=True,exist_ok=True)
PARAMS={
 'stair':dict(power=.98,shoulder=.005,balance=[1.003,1,1],gold_reduction=.02),
 'gate':dict(power=.88,shoulder=.018,balance=[1.012,1.003,1],gold_reduction=.02),
 'inner':dict(power=.84,shoulder=.025,balance=[1.008,1.002,1],gold_reduction=.06),
 'dialogue':dict(power=1.10,shoulder=.055,balance=[.975,.995,1.025],gold_reduction=.18),
}
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def transform(r,g,b,p):
 y=.2126*r+.7152*g+.0722*b
 if y<=1e-9:return 0,0,0
 target=y**p['power']-p['shoulder']*smooth(.5,1,y)
 vals=[v*target/y for v in [r,g,b]]
 # Select warm yellow highlights rather than blanket desaturation of blue costumes.
 gold=smooth(.015,.14,min(r,g)-b)*(1-smooth(.12,.28,r-g))*smooth(.25,.6,y)
 yy=.2126*vals[0]+.7152*vals[1]+.0722*vals[2]
 vals=[(yy+(v-yy)*(1-gold*p['gold_reduction']))*bal for v,bal in zip(vals,p['balance'])]
 return tuple(max(0,min(1,v)) for v in vals)
manifest={}
for name,p in PARAMS.items():
 filename=f'Baimifan_v014_{name}_r1.cube';path=L/filename
 lines=[f'TITLE "Baimifan v014 {name} r1"','LUT_3D_SIZE 33','DOMAIN_MIN 0 0 0','DOMAIN_MAX 1 1 1']
 for ib in range(33):
  for ig in range(33):
   for ir in range(33):
    vals=transform(ir/32,ig/32,ib/32,p);assert all(math.isfinite(v) for v in vals)
    lines.append(' '.join(f'{v:.7f}' for v in vals))
 data='\n'.join(lines)+'\n';path.write_text(data,encoding='ascii')
 target=D/filename
 if target.exists():assert target.read_bytes()==path.read_bytes(),'Do not overwrite an installed grade'
 else:shutil.copyfile(path,target)
 manifest[name]=dict(parameters=p,relative_lut='MCP/'+filename,project_lut=str(path.relative_to(R)),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
(O/'lut-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('Built and installed four versioned 33-point shot correction LUTs.')
