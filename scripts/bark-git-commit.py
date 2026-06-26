"""PostToolUse Hook - Git 提交通知（去重 + 详细信息）"""
import sys, os, re
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
commit_hash = ""
hash_match = re.search(r"\[(?:main|master|[\w-]+)\s+([a-f0-9]{7,})\]", output)
if hash_match:
    commit_hash = hash_match.group(1)
    if is_commit_seen(commit_hash):
        sys.exit(0)
    mark_commit_seen(commit_hash)

# ─── 提取 commit message ───────────────────────────────
msg = ""
m = re.search(r'(?:-m|--message)\s+["\'](.+?)["\']', cmd)
if not m:
    m = re.search(r'(?:-m|--message)\s+(\S+)', cmd)
if m:
    msg = m.group(1)

# ─── 从 output 提取详细信息 ─────────────────────────────
branch = ""
file_stats = ""
commit_line = ""

for line in output.split("\n"):
    line = line.strip()
    # [main abc1234] commit message（作为 message 的 fallback）
    bracket = re.search(r"\[([\w-]+)\s+[a-f0-9]+\]\s*(.+)", line)
    if bracket:
        branch = bracket.group(1)
        if not msg:
            commit_line = bracket.group(2)
    # 3 files changed, 15 insertions(+), 2 deletions(-)
    stat = re.search(r"(\d+ files? changed.*)", line)
    if stat:
        file_stats = stat.group(1)

if not msg:
    msg = commit_line or "有新的 commit"

# ─── 组装通知内容 ───────────────────────────────────────
body_parts = [msg]
if branch:
    body_parts[0] = f"[{branch}] {msg}"
if file_stats:
    body_parts.append(file_stats)
if commit_hash:
    body_parts.append(f"#{commit_hash}")

body = "\n".join(body_parts)

title = "Git 提交"
send(title=title, body=body, sound=GIT_COMMIT_SOUND, level=GIT_COMMIT_LEVEL)
