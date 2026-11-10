# 发布说明

本仓库是作品 **baimifan-short-film** 的公开快照，不是创作的唯一工作面。

| 项 | 值 |
| --- | --- |
| 源目录 | `/mnt/e/projects/内容创作/故事短片/白米饭` |
| 源仓库 HEAD | `830c7e7`（导出于一点时未提交改动 4901 处） |
| 导出时间 | 2026-11-10 19:50 |
| 收录 | 6135 个文件 / 270M |
| 滤掉媒体文件 | 57 个 |
| 滤掉 >40MB 文件 | 0 个 |

## 为什么不完整

公开仓库只收**源码、文档、脚本与配置**。成片、素材、模型权重、工程文件（.blend / 达芬奇工程）
体积到 GB 级，GitHub 单文件上限 100MB、仓库建议 1GB，传不上去；其中一部分还包含第三方版权素材，
不适合公开分发。这些内容保留在本地源目录。

## 重新同步

源目录有更新时，重新导出再提交：

```bash
rm -rf /mnt/e/projects/public/baimifan-short-film
/mnt/e/projects/.publish/export.sh baimifan-short-film "/mnt/e/projects/内容创作/故事短片/白米饭"
```
