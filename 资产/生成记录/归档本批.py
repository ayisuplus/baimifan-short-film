"""归档已完成的图像调用与原图复用；图册由公共渲染器生成。"""
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
RECORDS = ROOT / '资产/生成记录'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def metadata(path):
    with Image.open(path) as image:
        image.load()
        info = {'width': image.width, 'height': image.height, 'mode': image.mode}
        if 'A' in image.getbands():
            info['alpha_extrema'] = list(image.getchannel('A').getextrema())
        return info


def main():
    manifest_path = ROOT / '资产/assets.json'
    if manifest_path.exists() and json.loads(manifest_path.read_text(encoding='utf-8-sig'))['title'] != '《穿云》资产图册 · v0.1':
        raise ValueError('本脚本只归档首批资产，不覆盖后续图册；历史见资产/历史。')
    calls = json.loads((RECORDS / '生成调用-v001.json').read_text(encoding='utf-8'))
    if len(calls) != 9:
        raise ValueError('本批应保留九次调用，包含 GPT 首版与两次修订')
    paths = {}
    for call in calls:
        key = call['id']
        versioned = key if key.endswith(('-v002', '-v003')) else key + '-v001'
        source = Path(call['output_path'])
        target = ROOT / '资产/图像' / (versioned + '.png')
        if not target.exists():
            shutil.copy2(source, target)
        if digest(source) != digest(target):
            raise ValueError('生成原件与项目副本不一致: ' + key)
        paths[str(source)] = target.relative_to(ROOT).as_posix()
    for call in calls:
        key = call['id']
        versioned = key if key.endswith(('-v002', '-v003')) else key + '-v001'
        path = ROOT / paths[call['output_path']]
        references = []
        for ref in call['refs']:
            reference = Path(ref)
            project_path = paths.get(ref)
            if project_path is None and reference.is_relative_to(ROOT):
                project_path = reference.relative_to(ROOT).as_posix()
            references.append({'actual_input_path': ref, 'project_path': project_path,
                               'sha256': digest(reference)})
        record = {
            'asset_id': key.replace('-v002', '').replace('-v003', ''), 'version': versioned.rsplit('-', 1)[1],
            'date': '2026-10-20', 'engine': 'built-in image_gen',
            'actual_request': {'prompt': call['prompt'], 'referenced_image_paths': call['refs'],
                               'transparent_background': call['transparent']},
            'references': references, 'output': paths[call['output_path']],
            'original_output': call['output_path'], 'sha256': digest(path),
            'image': metadata(path),
            'status': '历史候选：透明边缘有杂色，保留不覆盖' if key in ('CHAR-GPT', 'CHAR-GPT-v002') else '候选待作者审阅',
            'evidence': '已实际查看生成图片；文件可解码、项目副本哈希与生成原件一致。不是动态或作者采用验收。',
        }
        save(RECORDS / (versioned + '.json'), record)

    def card(asset_id, name, category, path, role, limits, source, status='候选待作者审阅', version='v001', related=None):
        return dict(id=asset_id, name=name, category=category, version=version, status=status,
                    path=path, role=role, limits=limits, source=source, related=related or [])

    assets = []
    assets.append(card('REF-CLAUDE', '母版概念 · Claude 与黑袍人群', '概念参考',
        '概念参考/01-Claude-母版概念参考.webp', '作者指定：Claude 身份、服装色彩及哥特式画面氛围。',
        '原图只展示局部人物；裙身、背面及完整教堂结构需要补全候选。', '制作进度.md', '作者指定母版', '原件'))
    assets.append(card('REF-STREET', '母版概念 · 阳光街市与小鱼', '概念参考',
        '概念参考/02-DeepSeek-母版概念参考.webp', '作者指定：街市光影、DeepSeek 身份、体态与捧饭道具关系。',
        '黑袍遮挡区域不可见；饭盆与小鱼的接触仅是静态参考，未完成动作验证。', '制作进度.md', '作者指定母版', '原件'))

    assets.append(card('CHAR-CLAUDE', 'Claude · 白礼服与头纱', '主角', '资产/图像/CHAR-CLAUDE-v001.png',
        '主全身、背面及肖像，延续橙发、琥珀眼、橙花与白色刺绣礼服；用于 S01、S03—S06。',
        '裙身下部、背部、鞋和长发长度含合理补全，待作者确认；不是精确建模正交图，表情和受损状态按分镜补。',
        '资产/生成记录/CHAR-CLAUDE-v001.json', related=[{'path':'概念参考/01-Claude-母版概念参考.webp','role':'身份与服装原始依据'}]))

    reuse = json.loads((ROOT / '资产/复用来源.json').read_text(encoding='utf-8-sig'))
    for item in reuse:
        path = ROOT / item['path']
        if digest(path).upper() != item['sha256'].upper():
            raise ValueError('复用哈希异常: ' + item['id'])
        is_fish = item['id'] == 'MVFEDTJWNFEL8'
        assets.append(card('CHAR-DEEPSEEK' if is_fish else item['id'],
            'DeepSeek · 蓝鲸绒边斗篷' if is_fish else item['name'].split('_',1)[-1] + ' · Eagle 原图',
            '主角' if is_fish else '援军参考', item['path'],
            '沿用作者已有完整人物与穿搭拆解。鲸帽、蓝白色块、绒边、短靴作为一致性依据。' if is_fish else '作者指定沿用的援军角色参考；原字节复制，保留人物、服装和配色。',
            '这是服装参考总图，未另行重绘；伤后灰尘、破损和绷带按实际镜头补。' if is_fish else '最终出场数量、站位与动态能力待分镜；合景时统一渲染和光照，不改本色。',
            '资产/复用来源.json', '作者指定复用', '原件'))

    assets.append(card('CHAR-GPT', 'ChatGPT · 白龙娘净版', '主角', '资产/图像/CHAR-GPT-v003.png',
        '按用户指定截图保留龙角、翼、尾、银白长发与礼服，去除解说文字、播放器覆盖和悬浮小云。',
        '浅灰色不透明背景的再生成候选，底部遮挡部分有补全；不是透明合成素材，也不是逐像素原图裁切。',
        '资产/生成记录/CHAR-GPT-v003.json', version='v003', related=[
            {'path':'概念参考/04-ChatGPT-用户指定龙娘.png','role':'作者本轮指定的主要形象参考'},
            {'path':'资产/图像/CHAR-GPT-v001.png','role':'历史 v001：轮廓有杂色，保留追溯'},
            {'path':'资产/生成记录/CHAR-GPT-v001.json','role':'首版调用记录'},
            {'path':'资产/图像/CHAR-GPT-v002.png','role':'历史 v002：透明边缘仍有杂色'},
            {'path':'资产/生成记录/CHAR-GPT-v002.json','role':'第二版调用记录'}]))

    for asset_id, name, role, limits in [
        ('CHAR-PRIEST', '教主 · 黑金礼服', '虚构父亲角色的全身与肖像，持未点燃火把；属于同一黑袍教会。', '新创作候选，无现实人物相貌依据；服饰、年龄与面容尚待作者采用。'),
        ('CHAR-CULTIST', '教徒 · 黑袍正背参考', '依据母版黑袍群体补全的一套通用正背造型，可供不同教徒复用。', '背面与下身含补全；不是已验证的角色群体动态或战斗动作。'),
        ('ENV-STREET', '街市 · 阳光与长椅', 'S01 相遇与 S06 分饭的环境母版；暖阳、蓝白棚布、开放通道、长椅与远处教堂。', '原图被遮挡的空间、长椅和教堂外观为本版提案；非原图无损净版，人物尺度及教堂内外衔接待分镜验证。'),
        ('ENV-PALACE', '宫殿 · 独座与高台', 'S02 求助与 S05 信号回闪的环境母版；一个座位、空旷大厅、侧边露台。', '完整宫殿为新候选；椅子供龙翼与尾巴的实际坐姿、入口反向及露台角度尚待验证。'),
        ('ENV-CHURCH', '教堂 · 祭坛与侧墙洞口', 'S03—S05 场景母版：侧墙低洞、长椅、中央通道、祭坛、十字架、未燃柴薪和水盆。', '当前单视点；大门位于镜头后方，反向视角未制作。狗洞与鲸帽、十字架与 Claude 的尺度及火焰状态待分镜确认。'),
    ]:
        assets.append(card(asset_id, name, '场景' if asset_id.startswith('ENV-') else '配角',
            f'资产/图像/{asset_id}-v001.png', role, limits, f'资产/生成记录/{asset_id}-v001.json'))

    category_order = {'主角': 0, '场景': 1, '配角': 2, '援军参考': 3, '概念参考': 4}
    assets.sort(key=lambda asset: category_order[asset['category']])
    save(ROOT/'资产/assets.json', {'title':'《穿云》资产图册 · v0.1',
         'scope':'首批 15 项核心资产与 2 幅母版概念参考：8 项复用、7 项新制作候选。新候选待作者审阅；动态图、配音、分镜、背面补图和伤后状态未自动视为完成。点击主图查看原尺寸，展开来源可查看完整制作提示词。',
         'assets':assets})
    report = {'date':'2026-10-20','atlas_items':len(assets),'reused_assets':len(reuse),'generation_calls':len(calls),
              'new_active_candidates':7,'retained_history':['CHAR-GPT-v001','CHAR-GPT-v002'], 'files':[]}
    for asset in assets:
        path = ROOT / asset['path']
        report['files'].append({'id':asset['id'],'path':asset['path'],'sha256':digest(path),**metadata(path)})
    save(RECORDS/'文件核验-v001.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='files'},ensure_ascii=False))


if __name__ == '__main__':
    main()
