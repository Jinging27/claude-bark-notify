"""Stop Hook - 每轮回复结束通知（智能判断：短回复 / 长任务）

每次 Claude 回复完成后触发，计算本轮回复耗时（从用户提问到 Claude 回复完成）。
"""
import sys
import os

SCRIPTS_DIR = os.environ.get(
    "BARK_SCRIPTS_DIR",
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, SCRIPTS_DIR)

from datetime import datetime
from bark_shared import send
from bark_sounds import STOP_SOUND, STOP_LEVEL, LONG_TASK_SOUND, LONG_TASK_LEVEL

# 读取本轮提问时间（由 UserPromptSubmit hook 写入）
TURN_SENTINEL = os.path.join(SCRIPTS_DIR, ".bark-turn-start")
LONG_TASK_MINUTES = 10

is_long = False
duration = ""
try:
    with open(TURN_SENTINEL, "r", encoding="utf-8") as f:
        start = datetime.fromisoformat(f.read().strip())
    total = int((datetime.now() - start).total_seconds())
    is_long = total >= LONG_TASK_MINUTES * 60
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        duration = f"{h} 小时 {m} 分 {s} 秒"
    elif m > 0:
        duration = f"{m} 分 {s} 秒"
    else:
        duration = f"{s} 秒"
except Exception:
    pass

if is_long:
    title = "🎉 长任务完成"
    body = f"本轮耗时 {duration}，辛苦了！"
    send(title=title, body=body, sound=LONG_TASK_SOUND, level=LONG_TASK_LEVEL)
else:
    if duration:
        title = "Claude Code · 回复完成"
        body = f"本轮耗时 {duration}"
    else:
        title = "Claude Code"
        body = "已停止，请查看结果"
    send(title=title, body=body, sound=STOP_SOUND, level=STOP_LEVEL)
