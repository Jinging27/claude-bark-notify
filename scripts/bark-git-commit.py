"""PostToolUse Hook - Git 提交通知（去重）"""
import sys
import os
import re

sys.path.insert(0, os.environ.get(
    "BARK_SCRIPTS_DIR",
    os.path.dirname(os.path.abspath(__file__))
))

from bark_shared import read_stdin_json, get_tool_input, get_tool_response, is_commit_seen, mark_commit_seen, send
from bark_sounds import GIT_COMMIT_SOUND, GIT_COMMIT_LEVEL

data = read_stdin_json()
cmd = get_tool_input(data).get("command", "")
output = get_tool_response(data).get("output", "")

# 从 output 提取 commit hash 做去重
hash_match = re.search(r"\[(?:main|master|[\w-]+)\s+([a-f0-9]{7,})\]", output)
if hash_match:
    commit_hash = hash_match.group(1)
    if is_commit_seen(commit_hash):
        sys.exit(0)
    mark_commit_seen(commit_hash)

# 提取 commit message（支持多种写法）
msg = ""

# 1. 双引号 / 单引号：git commit -m "msg" / -m 'msg' / --message "msg"
m = re.search(r'(?:-m|--message)\s+["\'](.+?)["\']', cmd)
if m:
    msg = m.group(1)
else:
    # 2. 无引号：git commit -m msg
    m = re.search(r'(?:-m|--message)\s+(\S+)', cmd)
    if m:
        msg = m.group(1)
    else:
        # 3. 从 output 提取
        for line in output.split("\n"):
            line = line.strip()
            bracket = re.search(r"\]\s*(.+)", line)
            if bracket:
                msg = bracket.group(1)
                break
            if "file" in line and "changed" in line:
                msg = f"提交完成：{line}"
                break

if not msg:
    msg = "有新的 commit"

title = "Git 提交"
send(title=title, body=msg, sound=GIT_COMMIT_SOUND, level=GIT_COMMIT_LEVEL)
