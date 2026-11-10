# Claude 少女声线与 VoxCPM2 工作流核对

2026-10-21。角色目标：清柔、年轻、略忧郁的少女；保留保护朋友时的坚定。作者已否决v001幼童感、v002过于年长。不能用整体升调掩盖错误声线。

## 问题定位

v002实际请求同时包含“成熟成年”“中低音区”“有厚度的胸腔共鸣”“略沙哑”。这些是本次年龄感偏大的直接设计风险。Claude此前没有参考音频，两次均为文字声音设计；换描述会重新影响身份，固定随机种子并不等于固定同一个说话者。此判断基于实际请求与作者听审，不虚构自动年龄测量。

## 已核对的能力与限制

- 官方区分文字设计、可控克隆、续接克隆。可控克隆接受音色参考并支持表演指令；续接模式要求精确原声转录，同时继承参考的节奏和情绪。官方同时承认可控生成会波动，未提供“所有角色最稳定”的万能配置。[官方README](https://github.com/OpenBMB/VoxCPM#readme)
- 本机节点版本提交为`2d1e32ec7d69cf2d002b0480c6113c0b68e0baef`。`nodes/tts_node.py`实际会在prompt_audio续接模式忽略voice_design；仅reference_audio时保留指令。本轮无需转录的可控模式更适合比较“同音色、不同场景表演”，但跨句一致性尚未验收。
- 本机`modules/generation.py`把voice_design包成括号前缀交给模型，不是独立的年龄、情绪旋钮。缩短描述、删除互相牵制的要求是本轮设计修正，不能宣称仅靠短提示词即可保证稳定。
- `core.py`实际走`_generate_with_prompt_cache`，temperature、sway、CFG-Zero*均传到底层。未修改这些参数；没有把“降低temperature一定更好”当作结论，也没有加步数或CFG来解决年龄感。
- `retry_badcase`依赖生成长度与文本token数的比例，不能检测错字、年龄、音色相似度或表演合适与否。指令前缀参与此路径的目标文本token计数；自动重试不是语音质检。
- 固定seed、参考文件哈希、模型/节点版本、设备精度和参数有利于追踪与复现；本轮没有做强制重新计算的重复运行实验，不能把ComfyUI缓存命中或一次成功当作确定性证明。

本机证据目录：`G:/comfyui/ComfyUI/ComfyUI/custom_nodes/ComfyUI-VoxCPM`，已查看`nodes/tts_node.py`、`nodes/advanced_params_node.py`、`modules/generation.py`、`modules/utils.py`、`src/voxcpm/core.py`、`src/voxcpm/model/voxcpm2.py`。官方示例基线见[README](https://github.com/OpenBMB/VoxCPM#-quick-start)；模型说明见[OpenBMB模型页](https://huggingface.co/openbmb/VoxCPM2)。未采用模型页上方旧式16000Hz保存示例；本机原生输出核实为48000Hz。

## 本轮有界对照

保持CFG 2、10步、seed 20261021、BF16、temperature 1、sway 1、CFG-Zero*开启；把原先隐式高级默认值写进请求，不代表更改或提升了参数。最多三次任务，不扩展全片。

1. A：文字设计少女声，台词仍为“别碰她！”。
2. ANCHOR：同一身份描述生成一段安静的临时少女参考。只是音色测试句，不是新增剧情，不自动升为采用。
3. B：与A同台词、同指令、同seed、同全部采样参数，只增加ANCHOR作为reference_audio。

A/B仅比较本次参考条件的影响。单次A/B不能证明长期稳定，也不能在参考未获认可前宣布角色声线已锁定。两句均保留原始音频、请求、prompt_id；旧版与其他角色、Victory不改。

## 建议后续流程

先听准身份，再冻结经过认可的干净单人参考；逐句只调整短表演指令。优先从同一身份参考产生温柔、急切等表演；仅当表演确实需要继承参考节奏，且有准确转录时再使用续接模式。发现音色漂移时，保留基线、一次只改一项，不同时换参考、种子与参数。

声线获认可后才做跨句试验：安静说话与护人喊话都保留少女身份，核对字词、口音、尾音、杂声及连续播放感。此阶段未完成，不能标记“最稳定已验证”。

## 实际执行边界

MCP server_info及validate_workflow仍返回泛化错误。已核实同一127.0.0.1:8188服务在线、队列空闲、RTX5090约30GiB可用；沿用已有直连接口。逐类读取实时schema检查必填项，提交时由/prompt校验节点，记录node_errors。未安装/更新组件，未替换服务。文件解码、播放与参数对照可核验；本轮未完成实际听审。
