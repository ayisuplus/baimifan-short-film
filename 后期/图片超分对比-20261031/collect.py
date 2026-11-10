import json,pathlib,subprocess,shutil,urllib.parse
p=pathlib.Path(r'E:\projects\内容创作\故事短片\白米饭\后期\图片超分对比-20261031'); cli=r'C:\Users\36322\.codex\runtimes\comfy-mcp\Scripts\comfy.exe'; out=p/'outputs';out.mkdir(exist_ok=True)
for receipt in sorted((p/'receipts').glob('*-run.json')):
 n=receipt.stem[:-4]; run=json.loads(receipt.read_text(encoding='utf-8-sig'));pid=run['data']['prompt_id']
 r=subprocess.run([cli,'--json','--where','local','jobs','status',pid,'--host','127.0.0.1','--port','8188'],capture_output=True,encoding='utf-8');(p/'receipts'/f'{n}-status.json').write_text(r.stdout,encoding='utf-8');d=json.loads(r.stdout)
 print(n,d['data']['status'],flush=True)
 if d['data']['status']!='completed':continue
 r=subprocess.run([cli,'--json','--where','local','download',pid,'--url-only'],capture_output=True,encoding='utf-8');(p/'receipts'/f'{n}-download.json').write_text(r.stdout,encoding='utf-8'); assert json.loads(r.stdout)['ok']
 for url in d['data']['outputs']:
  q=urllib.parse.parse_qs(urllib.parse.urlparse(url).query);src=pathlib.Path(r'G:\comfyui\ComfyUI\ComfyUI\output')/q['subfolder'][0]/q['filename'][0];shutil.copy2(src,out/f'{n}.png')
