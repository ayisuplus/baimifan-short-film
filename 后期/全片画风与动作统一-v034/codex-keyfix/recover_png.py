"""从 codex 日志里抢救被文件锁截断的 PNG。

Codex 把生成的图以 base64 塞进执行的 PowerShell 命令，日志里留有完整串。
若目标文件写入被占用而截断，用这里从日志重建。
"""
import base64
import re
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
PAT = re.compile(r"FromBase64String\('([A-Za-z0-9+/=]+)'\)")


def targets(log: Path):
    """日志名 codex-090b.log -> 目标 090b-style-codex.png"""
    shot = log.stem.replace("codex-", "")
    cands = sorted(HERE.glob(f"{shot}*.png"))
    return cands[0] if cands else None


def repair_png(path: Path):
    """文件锁导致 Codex 重试追加，同一份 PNG 可能被追加多遍。
    按首个 PNG 结束块(IEND)截断即可还原为完整图片。"""
    raw = path.read_bytes()
    end = raw.find(b"IEND")
    if end == -1:
        return False
    cut = end + 8  # IEND + CRC32
    if cut >= len(raw):
        return False
    try:
        Image.open(__import__("io").BytesIO(raw[:cut])).verify()
    except Exception:
        return False
    path.write_bytes(raw[:cut])
    return True


def main():
    logs = sorted(HERE.glob("codex-*.log"))
    for log in logs:
        text = log.read_text(encoding="utf-8", errors="ignore")
        hits = PAT.findall(text)
        if not hits:
            print(f"{log.name}: 无 base64")
            continue
        raw = base64.b64decode(max(hits, key=len))
        tgt = targets(log)
        if tgt is None:
            print(f"{log.name}: 找不到目标 PNG")
            continue
        try:
            im = Image.open(tgt)
            im.verify()
            print(f"{log.name}: 目标已完整 {tgt.name} {im.size}，跳过")
            continue
        except Exception as e:
            print(f"{log.name}: 目标损坏({type(e).__name__})，尝试重建")
        if repair_png(tgt):
            im = Image.open(tgt)
            print(f"  已按 IEND 截断修复 {tgt.name} {im.size} ({tgt.stat().st_size} bytes)")
            continue
        try:
            Image.open(__import__("io").BytesIO(raw)).verify()
        except Exception as e:
            print(f"  日志里的 base64 也不完整({type(e).__name__})，需要重新生成")
            continue
        tgt.write_bytes(raw)
        im = Image.open(tgt)
        print(f"  已重建 {tgt.name} {im.size} ({len(raw)} bytes)")


if __name__ == "__main__":
    main()
