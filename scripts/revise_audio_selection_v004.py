"""Record the author's listening decisions and a recognizable epic shortlist."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();root=a.root.resolve()
target=root/'资产/生成记录/声音候选-v004.json'
if target.exists(): raise SystemExit('Preserve existing v004')
old=root/'资产/生成记录/声音候选-v003.json'
d=json.loads(old.read_text(encoding='utf-8'));d.update(version='v004',previous=old.relative_to(root).as_posix())
reviews={
 'DeepSeek':('作者否决 · 保留旧样本','像普通人类小孩，完全不像鲸鱼宝宝。','下一版先确定已有鲸鱼宝宝的声线参考；避免用“年幼小女孩”泛化提示直接代替身份。娃娃感、音色质地与说话方式都需匹配，不能只升高音调。'),
 'ChatGPT':('方向接近 · 尚未定稿','作者认为很接近，仍希望进一步调整；具体微调方向未说完整。','保留现有音色作为比较基线；具体加重威严、成熟度或冷感尚未确认，不擅自换声线。'),
 'Claude':('作者否决 · 保留旧样本','年龄感变成小女孩，情绪和语调也不对。','成熟的年轻女性声，柔和而压抑，降低幼态与甜腻。护住宝宝时由压住的情绪突然用力，短促、急切，不作幼童尖叫；这是下一版方向建议，未生成。')}
for c in d['casting']:
 if c['role'] in reviews:
  c['review_status'],c['author_feedback'],c['voice_direction']=reviews[c['role']]
for m in d['music']:
 m['status']='作者试听：曲调合适，节奏偏慢 · 旧备选'
 m['author_feedback']='不作为本轮快切段主选；原文件保留。'
oldmusic=d['music']
common=dict(license='未取得本片同步及录音使用授权',license_url='https://warnerchappell.com/faqs/',status='新候选 · 官方来源待试听',heard=False,source_in=None,source_out=None,attribution='当前仅记录试听来源，署名本身不等于获得使用许可。',audition_note='打开官方试听／发行页；未下载原声，未写入成片。')
def item(id,title,author,source,description,role,**extra):
 return {**common,'id':id,'title':title,'author':author,'source':source,'description':description,'role':role,**extra}
d['music']=[
 item('BGM-BEACONS-001','The Lighting of the Beacons','Howard Shore','https://www.youtube.com/watch?v=w_hnJNnKZz0','《指环王：王者归来》完整原声；官方艺人频道发行版本。','叙事贴合优先：试配 GPT 四地邀约、分屏回应和穿云信号。选已形成推进的乐段，不从长铺垫机械铺起。',recognition_evidence='搜索索引返回官方艺人频道约194万播放；2026-10-21检索快照，不代表中国平台受众覆盖。'),
 item('BGM-VICTORY-001','Victory','Two Steps From Hell / Thomas Bergersen','https://www.youtube.com/watch?v=hKRUPYrAQoE','经典史诗音乐；不是《霍比特人》或《指环王》的电影原声。','熟悉感优先：试配踹门、群像登场和力量反转。只挑高潮段，不用整首五分钟的铺垫；对白压低人声与合唱。',recognition_evidence='Two Steps From Hell官方视频搜索快照约1.83亿播放，2026-10-21检索；不能据此保证每位观众熟悉。',catalog_source='https://www.extrememusic.com/discover/labels/two-steps-from-hell'),
 item('BGM-COURAGE-001','Heart of Courage','Two Steps From Hell / Thomas Bergersen','https://www.youtube.com/watch?v=K2iC1aCPbKA','经典预告片／史诗曲，非特定战争电影原声。','短段备用：援军列阵、邀约回应的持续推进。节拍数字不等于剪辑速度，重点试听细分节奏和重音。',catalog_source='https://www.extrememusic.com/albums/3602',recognition_evidence='Spotify艺人热门曲目列首；Extreme Music官方目录列入Greatest Hits Remastered。目录标67 BPM，本轮不声称它是高BPM歌曲。'),
 item('BGM-PELENNOR-001','The Battle of the Pelennor Fields','Howard Shore','https://www.youtube.com/watch?v=8t9eL-5wMFc','《指环王：王者归来》完整原声，官方艺人频道发行版本。','冲突强度备用：起飞与天空强光之间的极短段。不能为了音乐扩写战斗，依然直接跳至敌人倒地。',recognition_evidence='官方频道搜索快照约897万播放，2026-10-21检索；受众熟悉程度待作者试听判断。'),
 item('BGM-OVERHILL-001','Over Hill','Howard Shore','https://www.watertower-music.com/release/the-hobbit-an-unexpected-journey-original-motion-picture-soundtrack/','WaterTower官方《霍比特人：意外之旅》原声曲目18。','奇幻冒险备用：优先核听管弦推进段。官方曲目已核实，独立试听链接及合适截段尚未核定；不冒称已确认热度。'),
]+oldmusic
d['conclusion']='按作者听审修订：DeepSeek与Claude首轮试音否决，GPT音色接近但待微调。前三首原配乐降为慢节奏备选；新一轮优先经典电影／史诗曲的熟悉度与短段推进。'
d['listening_status']='作者已试听旧三首配乐与三句试音，反馈已逐项记录。新五首为来源核实后的待试听候选；未完成实际听审，不提供猜测的秒级入出点。'
d['generation_status']='本轮不重复按失败声线方向抽取试音。旧FLAC及请求保留；GPT留作基线。先确定DeepSeek参考与Claude成熟度、表演方向，再制作下一版。'
d['rights_note']='未发现以上电影原声可无条件直接用于本片的证据。正式发布需核实发行平台曲库是否覆盖所选录音和使用场景，或取得相应授权；音乐可试听/购买不等于视频使用许可。本轮未购买、申请授权或联系他人。'
d['research_sources']=['https://warnerchappell.com/faqs/','https://www.extrememusic.com/albums/3602','https://www.extrememusic.com/discover/labels/two-steps-from-hell','https://embed.spotify.com/?uri=spotify%3Aartist%3A2qvP9yerCZCS0U1gZU8wYp','https://www.youtube.com/watch?v=s4LX9NX7hS4']
d['cue_design']=[dict(scenes=['S01','S06'],music_id=None,direction='首尾保留温柔主题与留白，不为全片快切强行加战鼓；旧曲仅保留为备选。'),dict(scenes=['S02','S03','S04'],music_id=None,direction='脚步、锁链、火把入水等信息优先；音乐要有脉冲但不提前用完史诗高潮。中段新曲未选定。'),dict(scenes=['S05'],music_id=None,direction='比较两套方案：烽火台主题服务跨地域召集；Victory或Heart of Courage服务破门与援军群像。不是五首全部拼接。条约对白压乐、聒噪留白；起飞强光后立即收束并进入救援。')]
target.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=root/'资产/assets.json';assets=json.loads(path.read_text(encoding='utf-8'));assets['sound_manifest']=target.relative_to(root).as_posix();path.write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded author reviews and five epic candidates; historical files preserved.')
