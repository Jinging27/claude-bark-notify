"""Bark 通知声音配置 - 在这里挑选每种场景的提示音

修改下面的值即可自定义声音，无需重启 Claude Code（下次会话生效）。
声音列表见 README.md。
"""

# ─── 🟢 回复完成（30 秒 ~ 10 分钟）──────────────────
STOP_SOUND = "healthnotification"
STOP_LEVEL = "active"

# ─── 🟣 长任务完成（Stop ≥ 10 分钟）──────────────────
LONG_TASK_SOUND = "shake"
LONG_TASK_LEVEL = "active"

# ─── 🔵 Git 提交通知 ────────────────────────────────
GIT_COMMIT_SOUND = "chime"
GIT_COMMIT_LEVEL = "active"

# ─── 🔴 错误报警（PostToolUseFailure）───────────────
ERROR_SOUND = "alarm"
ERROR_LEVEL = "timeSensitive"   # ⚡ 突破勿扰模式
