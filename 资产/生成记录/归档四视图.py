"""保存四视图原件、调用依据与图册引用；不改动图像像素。"""
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
RECORDS = ROOT / '资产/生成记录'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    calls = read(RECORDS/'四视图结果收集-v001.json') + [
        read(RECORDS/'DeepSeek四视图结果-v001.json'),
        read(RECORDS/'DeepSeek局部修订结果-v002.json'),
        read(RECORDS/'DeepSeek局部修订结果-v003.json')]
    if len(calls) != 5 or len({x['id'] for x in calls}) != 5:
        raise ValueError('应有三位主角与 DeepSeek 两次局部修订，共五个独立结果')
    manifest_path = ROOT/'资产/assets.json'
    manifest = read(manifest_path)
    if manifest['title'] not in ('《穿云》资产图册 · v0.1', '《穿云》资产图册 · v0.2'):
        raise ValueError('当前图册版本已变化，不用历史归档脚本覆盖')
    snapshot = ROOT/'资产/历史/assets-v001.json'
    if not snapshot.exists():
        if manifest['title'] != '《穿云》资产图册 · v0.1':
            raise ValueError('缺少首版快照，请先核对历史')
        save(snapshot, manifest)

    output_records = []
    for call in calls:
        key = call['id']
        target = ROOT/'资产/图像/四视图'/f'{key}.png'
        target.parent.mkdir(parents=True, exist_ok=True)
        source = Path(call['output_path'])
        if not target.exists():
            shutil.copy2(source, target)
        if digest(source) != digest(target):
            raise ValueError('生成原件与本地副本不一致: '+key)
        with Image.open(target) as image:
            image.load()
            shape = dict(width=image.width, height=image.height, mode=image.mode)
        record = dict(id=key, asset_id=key.split('-TURN-')[0], date='2026-10-20',
            engine='built-in image_gen', original_output=str(source),
            path=target.relative_to(ROOT).as_posix(), sha256=digest(target), image=shape,
            actual_request=dict(prompt=call['prompt'], referenced_image_paths=call['refs'], transparent_background=False),
            references=[dict(path=p, project_path=Path(p).relative_to(ROOT).as_posix(), sha256=digest(Path(p))) for p in call['refs']],
            view_order=['正面全身','朝画面左侧面全身','背面全身','朝画面右侧面全身'],
            status={'CHAR-DEEPSEEK-TURN-v001':'历史候选：帽尾重复，后续局部修订', 'CHAR-DEEPSEEK-TURN-v002':'历史候选：后帽尾侧面缺失、背面扁平，后续修订'}.get(key, '候选待作者审阅'),
            review='视觉复核-v002.md；属于影视四向参考，非工程测量或作者采用验收。')
        save(RECORDS/f'{key}.json', record)
        output_records.append(record)

    selected = {'CHAR-CLAUDE':'CHAR-CLAUDE-TURN-v001', 'CHAR-GPT':'CHAR-GPT-TURN-v001', 'CHAR-DEEPSEEK':'CHAR-DEEPSEEK-TURN-v003'}
    details = {
        'CHAR-CLAUDE': ('Claude · 四向全身参考', '橙发圣女的正面、两侧与背面全身；母版负责身份与服装，前版设定板辅助下裙和鞋的连续性。', '侧背、下裙与鞋含补全；同一自然站姿的四向参考，不作为精确工程正交图。'),
        'CHAR-GPT': ('ChatGPT · 白龙娘四向全身', '以作者白龙娘原截图为身份依据，呈现正面、两侧和背面全身；原净版辅助遮挡部分。', '两侧躯干略带斜角。开衩与腿饰以原图/正面图的角色右腿为准，不按对称读取；尾巴弯曲是姿态参考，侧背含补全。'),
        'CHAR-DEEPSEEK': ('DeepSeek · 母本宝宝四向全身', '原始捧饭母本优先：保留脸、头身比例、蓝发蓝眼、鲸帽和宝宝感；穿搭卡只辅助衣服细节。', '中立站姿不持饭盆以显示衣装。背面帽尾体积表达较简化，镜头以母本及两侧视为准；鲸帽尾和身体尾是不同结构，母本优先于旧穿搭卡。')}
    reused = read(ROOT/'资产/四视图复用来源-v002.json')
    reuse_map = {x['asset_id']:x for x in reused}
    for asset in manifest['assets']:
        key = asset['id']
        if key not in selected and key not in reuse_map:
            continue
        previous_path, previous_source = asset['path'], asset['source']
        related = asset.setdefault('related', [])
        new_path = f'资产/图像/四视图/{selected[key]}.png' if key in selected else reuse_map[key]['path']
        if previous_path != new_path:
            for path, role in ((previous_path, '上一版形象参考：保留原件'), (previous_source, '上一版来源记录')):
                if path not in {r['path'] for r in related}:
                    related.append(dict(path=path, role=role))
        asset['path'] = new_path
        if key in selected:
            asset['name'],asset['role'],asset['limits'] = details[key]
            asset['version'] = selected[key].rsplit('-',1)[1]+' · 四视图'
            asset['status'] = '候选待作者审阅'
            asset['source'] = f'资产/生成记录/{selected[key]}.json'
            if 'AGENTS.md' not in {r['path'] for r in related}:
                related.append(dict(path='AGENTS.md', role='本项目角色四视图规范'))
        else:
            asset['name'] = asset['name'].replace('Eagle 原图', 'Eagle 四方向设定卡')
            asset['version'] = 'Eagle 原件'
            asset['source'] = '资产/四视图复用来源-v002.json'
            asset['role'] = '复用 Eagle 已有同造型角色设定卡，含四方向全身、表情及细节；对应原立绘保留在附属参考。'
            asset['limits'] = '旧卡正面有姿势、两侧略带斜角，作为四方向参考复用。合景保留人物服装本色；出场数量、站位和动态按分镜确定。'
        if key == 'CHAR-DEEPSEEK':
            for path,role in [('概念参考/02-DeepSeek-母版概念参考.webp','本轮作者指定最高优先母本'),
                              ('资产/图像/四视图/CHAR-DEEPSEEK-TURN-v001.png','历史 v001：帽尾重复，已局部修订'),
                              ('资产/生成记录/CHAR-DEEPSEEK-TURN-v001.json','四视图初版调用记录'),
                              ('资产/图像/四视图/CHAR-DEEPSEEK-TURN-v002.png','历史 v002：后帽尾侧面缺失'),
                              ('资产/生成记录/CHAR-DEEPSEEK-TURN-v002.json','第一次局部修订记录')]:
                if path not in {r['path'] for r in related}:related.append(dict(path=path,role=role))

    manifest['title'] = '《穿云》资产图册 · v0.2'
    manifest['scope'] = '重要角色优先四视图、已有设定卡优先复用。三位主角新增四向全身候选，七位援军复用 Eagle 同造型旧卡。DeepSeek 以原始捧饭母本为最高依据。点击图片查看原尺寸；来源记录保留完整请求，附属参考保留原立绘与历史版本。'
    save(manifest_path, manifest)
    save(RECORDS/'四视图文件核验-v002.json', dict(generated_calls=len(calls), selected_new_turnarounds=3, reused_sheets=len(reused), atlas_items=len(manifest['assets']), generated=[dict(id=x['id'], path=x['path'],sha256=x['sha256'],**x['image']) for x in output_records]))
    print(json.dumps(dict(atlas_items=len(manifest['assets']),new_turnarounds=3,reused_sheets=len(reused),retained_generated_history=2),ensure_ascii=False))


if __name__ == '__main__':
    main()
