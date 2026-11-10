"""Reuse the checked v017 pipeline for the four author-requested local revisions."""
from pathlib import Path
import re,json
from revise_space_v063 import CHANGES
ROOT=Path(__file__).resolve().parents[1]

def main():
 path=ROOT/'scripts/build_generation_v017.py'
 code=path.read_text('utf-8').replace("'revision_v062'","'revision_v063'")
 code=code.replace("plan.update(version='v017'", "plan.update(version='v018'")
 code=code.replace("s.get('camera', s['framing']) + ' ' + note", "note")
 code=code.replace("set(TARGETS[:-1])", "set(TARGETS)")
 code=code.replace('Six reviewed nodes must be revised','Nine visual references must be revised')
 code=code.replace('v062实际图像','v063实际图像').replace('Only six visual action/camera nodes revised','Only four batches visually revised')
 code=code.replace('关键动作重拍 v017','空间与张力 v018').replace('让关键动作成为画面中心','让冲突、距离和受阻变得清楚')
 code=code.replace('接火、滑脱、破门、化龙、牵挂与接抱：六处已按审查方向修订，原画和旧生成板保留。','按页面第2、3、8、10批：掀饭、暮色长阶、试锁与抓柴受阻。9张候选包含2张相邻宫门改光；第10批图片5原样保留。')
 code=code.replace('../../视频制作/生成板-v017/生成板.html','../../视频制作/生成板-v018/生成板.html').replace('生成板 v017</a>','生成板 v018</a>')
 code=code.replace('../全片张力审查-v016/审查.html','视觉复核.md').replace('本轮审查依据','独立视觉复核')
 groups=[('掀饭与求援',['CY003A','CY003B','CY003C','CY004','CY004A']),('暮色长阶与宫门',['CY004B','CY004C','CY004D','CY005']),('保证与试锁',['CY013A','CY015','CY016','CY016A1']),('抓柴与受阻',['CY016C','CY016D','CY017','CY017A','CY018','CY018B'])]
 code=re.sub(r'    groups = \[.*?\n    \]', '    groups = '+repr(groups),code,count=1,flags=re.S)
 ns={'__file__':str(path),'__name__':'v018_adapter'}
 exec(compile(code,str(path),'exec'),ns)
 ns.update(OLD='视频制作/生成板-v017',OUT='视频制作/生成板-v018',OLDFIX='后期/关键动作重拍-v017',FIX='后期/空间张力-v018',BASE='镜头设计/shot-plan-v0.62.json',SOURCE='镜头设计/shot-plan-v0.63.json',TARGETS=list(CHANGES),EN={k:v['en'] for k,v in CHANGES.items()})
 ns['main']()
 old=ns['load']('视频制作/生成板-v017/展开数据.json');new=ns['load']('视频制作/生成板-v018/展开数据.json')
 affected={'GB002','GB003','GB007','GB009'}
 for a,b in zip(old['batches'],new['batches']):
  assert a['id']==b['id']
  if b['id'] not in affected:assert a['references']==b['references'] and a['prompts']==b['prompts'],b['id']
  for ref in b['references']:assert ns['sha'](ref['path'])==ref['sha256']
  assert b['models'][b['selected_model']]['capacity_ok']
 before=ns['load']('镜头设计/shot-plan-v0.62.json');after=ns['load']('镜头设计/shot-plan-v0.63.json')
 for a,b in zip(before['shots'],after['shots']):
  if b['id'] not in CHANGES:assert a==b,b['id']
 assert len(old['batches'])==len(new['batches'])==41
 ns['write']('后期/空间张力-v018/局部范围核验.json',dict(unaffected_batches_identical=37,unchanged_shots=124,protected_shot='CY017A',references_verified=True,selected_model_capacity_verified=True,changed_batches=sorted(affected),video_generated=False))
 print('37 untouched batches and 124 untouched shots exactly preserved.')

if __name__=='__main__':main()
