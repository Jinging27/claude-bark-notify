"""PostToolUseFailure Hook - 错误报警通知"""
import sys
import os

SCRIPTS_DIR = os.environ.get(
    "BARK_SCRIPTS_DIR",
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, SCRIPTS_DIR)

from bark_shared import read_stdin_json, get_tool_input, get_tool_response, send
from bark_sounds import ERROR_SOUND, ERROR_LEVEL

data = read_stdin_json()
tool = data.get("tool_name", "未知工具")
inp = get_tool_input(data)
resp = get_tool_response(data)

# 构建错误摘要
body_parts = []

if tool == "Bash":
    cmd = inp.get("command", "")[:60]
    body_parts.append(f"命令: {cmd}")
elif tool in ("Write", "Edit"):
    path = inp.get("file_path", inp.get("filePath", ""))
    body_parts.append(f"文件: {os.path.basename(path)}")
elif tool == "Read":
    path = inp.get("file_path", "")
    body_parts.append(f"文件: {os.path.basename(path)}")

# 提取错误信息
error = resp.get("error", "")
if not error:
    error = resp.get("stderr", "") or resp.get("output", "")

if error:
    short_err = error.strip().replace("\n", " ")[:100]
    body_parts.append(f"错误: {short_err}")

body = " | ".join(body_parts) if body_parts else "工具调用失败"

send(
    title=f"⚠️ {tool} 执行失败",
    body=body,
    sound=ERROR_SOUND,
    level=ERROR_LEVEL,
)
