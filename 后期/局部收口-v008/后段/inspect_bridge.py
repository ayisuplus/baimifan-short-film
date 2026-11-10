from pathlib import Path
import subprocess,io,json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
p=R/'视频制作/Metaso-H3-v003/产物/GB029-v003-CY029E4-r002.mp4'
nextp=R/'视频制作/Metaso-H3-v002/剪辑候选/GB028-v002.mp4'
cells=[(p,f) for f in [0,12,24,36,48,60,72,81]]+[(nextp,f) for f in [0,12,24,36]]
sheet=Image.new('RGB',(1440,320*4),'#18202b');d=ImageDraw.Draw(sheet)
for i,(q,f) in enumerate(cells):
    raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(f/24),'-i',str(q),'-frames:v','1','-vf','scale=480:-1','-f','image2pipe','-vcodec','png','pipe:1'])
    im=Image.open(io.BytesIO(raw));x=(i%3)*480;y=(i//3)*320;sheet.paste(im,(x,y+40));d.text((x+5,y+5),('bridge ' if q==p else 'next B38 ')+str(f)+'f',fill='white')
sheet.save(O/'bridge-join.jpg',quality=94)
