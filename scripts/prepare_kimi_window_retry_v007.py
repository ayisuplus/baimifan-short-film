from pathlib import Path
import json,copy,html
R=Path(__file__).resolve().parents[1];G=R/'视频制作/Metaso-H3-v007';p=G/'执行队列.json';q=json.loads(p.read_text(encoding='utf8'))
old=next(x for x in q['items'] if x['attempt_id']=='GB014A-v007-kimi-window-style-audio-r1');old.update(review_decision='rejected',review_reason='发力前窗已出现大洞，动作因果错误；不能入剪')
x=copy.deepcopy(old)
for k in ['task_id','local_path','sha256','bytes','submit_started','provider_status','review_decision','review_reason']:x.pop(k,None)
x.update(attempt_id='GB014A-v007-kimi-window-style-audio-r2',status='prepared',change_reason='首轮误生破窗。固定机位、玻璃必须完整，出手后在撞击前结束。')
x['prompt']='Image1为Kimi身份与已举起的银色圆环刃、右手暗刃、服装和原片细密三维二次元插画质感。Image2明确她悬浮在教堂外，面对完好无损的彩色玻璃高窗。严格保持二图完整玻璃，玻璃为封闭实体表面，窗上全是连续蓝色菱形彩片和完整黑色窗棂，没有门、孔洞、圆洞、三角裂口、缺片、透明通道或裂纹。整段禁止玻璃发生任何改变或显露室内。\n9秒连续单镜，固定在Kimi左侧略后，清晰三分之二侧脸和银刃近景，窗玻璃固定在画面右半边。前7.7秒人物面向玻璃，只念咒与凝聚刃的银辉；Audio1从0秒播放原有日语この刃の銀の光をたどり、彼方へと通じる扉を、我に開け——，是真实配音和口型唯一基准，禁止另念或无声乱动嘴，停顿闭口。头发受夜风同向缓摆，身体有克制呼吸，不对镜头摆拍、不转身、不换摄影机侧别、不运镜穿窗。光只聚在左手圆环刃，不能在玻璃上画几何轮廓或魔法入口。\n7.7秒台词说完，闭口。8.0秒左肩稍后收，肘与腕带动明刃向画面右侧玻璃方向掷出，8.5秒左右明刃离手飞出画面右边；最后0.5秒保持随势，玻璃仍完整，影片结束在飞刃接触玻璃之前。下一剪辑镜头才破窗。右手暗刃始终低持不投掷。人物不穿窗，不施放护罩，不出现室内人物、不提前发生撞击。衣服、脸型、发饰、材质、光线沿原片，禁止平涂赛璐璐。无字幕、BGM、新台词。'
assert not any(i['attempt_id']==x['attempt_id'] for i in q['items']);q['items'].append(x);assert sum(i['estimated_credits'] for i in q['items'])<=q['spending_ceiling_credits']
p.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf8')
with (G/'补拍输入.html').open('a',encoding='utf8') as f:f.write('<article><h2>'+x['attempt_id']+'</h2><pre>'+html.escape(x['prompt'])+'</pre></article>')
print(x['attempt_id'])
