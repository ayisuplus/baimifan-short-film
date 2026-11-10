# OpenCut CLI：给不擅长浏览器的 Agent

`opencut` 是本地 Rust 程序，复用编辑器的创作存储、身份校验和参数准备逻辑。不打开浏览器也能读磁盘工程、剧本、提示词、参考图和工作流，并另存片段新稿。当前选择、实时轨道和浏览器候选通过编辑器只读心跳取得。

## 安装与发现

在代码仓库执行 `./scripts/install-cli.ps1`，构建两个原生程序并同步浏览器使用的宿主程序。Windows 启动器位于 `%USERPROFILE%\.local\bin\opencut.cmd`。该目录已在本机 PATH；其他机器可以使用完整路径。仓库移动或更新代码后重新运行安装器。旧的不同内容启动器自动备份。

非 Windows：`cargo build -p creative --features native --bin opencut`，用二进制加 `--repo <代码仓库根>`，或设置 `OPENCUT_REPO`。不要把作品目录当作代码仓库根。

```powershell
opencut --help
opencut projects
$projectId = 'restored-ad3867fc-177c-4371-bb51-7ed75d686e30'
opencut current --project $projectId
opencut clips --project $projectId
opencut clip read --project $projectId --clip CUT003
opencut script --project $projectId
opencut assets --project $projectId
opencut workflows list --project $projectId --clip CUT003
```

标准输出只有一个 JSON 对象：`{ok:true,value:...}` 或 `{ok:false,code,error}`。退出码 0 成功、3 版本/身份冲突、1 其他失败。`--input -` 读取标准输入；`--input file.json` 读取 UTF-8（支持 BOM）。`--output new.json` 另存 UTF-8 结果，只创建新文件；文件已存在时不执行保存。I/O 错误或保存结果不确定时，重新读取历史核实，禁止无条件重试写入。

## 修改片段新稿

`clip read` 返回 `source_context`（历史执行来源）、`draft.current`（已保存新稿）、`draft.history` 和 `references`。参考文件路径为 `media_root` 加各项 `path`，同时保留 SHA-256。`clips.bindings` 是磁盘关联时快照，不代表此刻浏览器轨道；实时轨道使用 `timeline`。

```powershell
$read = opencut clip read --project $projectId --clip CUT003 | ConvertFrom-Json
$draft = $read.value.draft.current
$request = @{ expected_revision=$draft.revision; texts=$draft.texts }
# 仅改需要修改的项；保留剧本/提示词数组的顺序及数量。
$request.texts.script[0] = '这里填写修改后的这组剧本。'
$request | ConvertTo-Json -Depth 20 | Set-Content -Encoding utf8 draft.json
opencut clip save --project $projectId --clip CUT003 --input draft.json
opencut clip history --project $projectId --clip CUT003
```

保存使用现有锁及版本比较，追加不可变版本。重复提交旧 `expected_revision` 返回冲突，不生成第二个版本。历史执行、完整场景剧本、时间线不随局部新稿改写。冲突后重新读取、合并差异，再决定是否保存。

历史稿命令 `clip version --input version.json`，输入 `{"revision":0}`。恢复时先读取旧版，再使用**当前**版本号提交旧文本，成为新修订，不删除历史。此版写入面向导入片段上下文（白米饭 CUT001–CUT118）；原生分镜及完整剧本可读取，尚不提供完整场景剧本的 CLI 编辑。

编辑器约三秒检测当前片段磁盘稿变化。左侧保留未保存输入；右侧刷新已保存提示词并作废旧准备结果。浏览器脏稿仍须处理版本冲突，不会被 CLI 新稿自动覆盖。

## 准备工作流参数

先 `workflows list` 取得条目、保存稿、参考素材键、`context.token` 与 `catalog_hash`，再按条目的 `params`/`slots` 填写参数与媒体键。Woosh 示例：

```powershell
$catalog = (opencut workflows list --project $projectId --clip CUT003 | ConvertFrom-Json).value
@{ entry_id='woosh-sfx'; context_token=$catalog.context.token;
   catalog_hash=$catalog.catalog_hash; params=@{}; media=@{};
   text_input='缓慢的风声与轻微衣料摩擦' } |
   ConvertTo-Json -Depth 20 | Set-Content -Encoding utf8 prepare.json
opencut workflows prepare --project $projectId --clip CUT003 --input prepare.json --output prepared.json
```

旧上下文/目录 token 会被拒绝。结果包含 `submitted:false`、`uploaded:false`、`execution_enabled:false`。ComfyUI 本地媒体占位待后续执行层处理。没有 submit/run/upload 命令，无云端密钥读取，无 GPU 调用。界面未保存的提示词不参与准备。Woosh 描述只用于本次音效准备，三个未绑定的配音/转录模板仍不可准备。

## 浏览器状态

```powershell
opencut current --project $projectId
opencut timeline --project $projectId
opencut candidates --project $projectId --clip CUT003
```

打开编辑器即可桥接。`current.value.state` 返回工程、场景、选择、播放头、镜头和轨道；`received_at` 是服务端 Unix 秒。三秒心跳，超过十五秒拒绝实时读取。切工程/关闭时撤销旧心跳，乱序请求不能覆盖新状态；异常退出/休眠由过期规则兜底。

多窗口同时在线时不会猜测，错误列出会话编号，用 `--session <ID>` 选择，并建议同时指定 `--project`。选字幕、多选、未关联片段遵循工作区的空镜头状态，`selected` 仍可读取。`candidates` 返回浏览器已登记且归属本镜的候选；历史参考图使用 `clip read`。

会话记录在 `.local/agent-sessions`，不属于备份，不改 IndexedDB/OPFS。此版不提供时间线增删、候选采用/恢复或撤销重做命令，保留 UI 原生操作。后续须经过原生命令栈与身份校验，不直接修改浏览器数据库。

## 验收

- Rust 测试覆盖 CLI 真进程、退出码、另存/历史、重复提交、错工程、输入白名单、撤销/乱序/切工程、多窗口及过期。
- `python scripts/verify-agent-cli.py --project <恢复工程编号>` 只读核对全片段/参考文件，准备 Woosh 参数，对比创作资料和清单哈希；报告 `.local/agent-cli-validation.json`。不会另存作品新稿。
- 原生测试：`cargo test -p creative --features native --target-dir target/agent-cli`；前端回归：`bun test ./apps/web/src/creative/`。
