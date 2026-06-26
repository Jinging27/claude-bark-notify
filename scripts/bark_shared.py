"""bark_shared - 通用 Bark 推送模块

所有 hook 脚本通过 import 调用 send() 发送通知。
路径优先级：BARK_SCRIPTS_DIR 环境变量 > __file__ 所在目录
"""
import os
import sys
import json
import urllib.parse
import urllib.request

# ─── 配置 ────────────────────────────────────────────────
BARK_KEY = os.environ.get("BARK_KEY", "")
BARK_BASE = "https://api.day.app"
BARK_ICON = "https://i.ibb.co/twGCn2Xx/claude-color.png"

# 脚本目录：优先环境变量，其次 __file__ 所在目录
SCRIPTS_DIR = os.environ.get(
    "BARK_SCRIPTS_DIR",
    os.path.dirname(os.path.abspath(__file__))
)
SEEN_FILE = os.path.join(SCRIPTS_DIR, ".bark-seen-commits")


def is_configured() -> bool:
    return bool(BARK_KEY) and BARK_KEY != "your_bark_push_key_here"


def send(
    title: str,
    body: str,
    sound: str = "chime",
    level: str = "active",
    group: str = "Claude Code",
    url: str = "",
    copy: str = "",
    auto_copy: bool = False,
    is_archive: int = 1,
) -> bool:
    """发送 Bark 通知。返回是否成功。"""
    if not is_configured():
        return False

    parts = [
        BARK_BASE,
        BARK_KEY,
        urllib.parse.quote(title),
        urllib.parse.quote(body),
    ]
    params = {
        "sound": sound,
        "level": level,
        "group": urllib.parse.quote(group),
        "icon": BARK_ICON,
        "isArchive": str(is_archive),
    }
    if url:
        params["url"] = url
    if copy:
        params["copy"] = copy
        params["automaticallyCopy"] = "1" if auto_copy else "0"

    full_url = "/".join(parts) + "?" + "&".join(f"{k}={v}" for k, v in params.items())

    try:
        req = urllib.request.Request(full_url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return True
    except Exception as e:
        print(f"[bark] 推送失败: {e}", file=sys.stderr)
        return False


def read_stdin_json() -> dict:
    """从 stdin 读取 hook 输入 JSON"""
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def get_tool_input(data: dict) -> dict:
    """提取 tool_input"""
    return data.get("tool_input", {})


def get_tool_response(data: dict) -> dict:
    """提取 tool_response（PostToolUse 时才有）"""
    return data.get("tool_response", {})


def is_commit_seen(hash_str: str) -> bool:
    """检查该 commit 是否已通知过（去重）"""
    try:
        with open(SEEN_FILE, "r") as f:
            return hash_str in f.read()
    except FileNotFoundError:
        return False


def mark_commit_seen(hash_str: str):
    """标记该 commit 已通知"""
    try:
        with open(SEEN_FILE, "a") as f:
            f.write(hash_str + "\n")
    except Exception:
        pass


def clean_seen_file(max_lines: int = 200):
    """清理过大的去重文件"""
    try:
        with open(SEEN_FILE, "r") as f:
            lines = f.readlines()
        if len(lines) > max_lines:
            with open(SEEN_FILE, "w") as f:
                f.writelines(lines[-max_lines:])
    except Exception:
        pass
