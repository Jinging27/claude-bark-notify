"""一键测试所有 Bark 通知

用法：python3 bark-test.py
"""
import sys
import os
import time

sys.path.insert(0, os.environ.get(
    "BARK_SCRIPTS_DIR",
    os.path.dirname(os.path.abspath(__file__))
))

from bark_shared import send, is_configured
from bark_sounds import (
    STOP_SOUND, STOP_LEVEL,
    LONG_TASK_SOUND, LONG_TASK_LEVEL,
    GIT_COMMIT_SOUND, GIT_COMMIT_LEVEL,
    ERROR_SOUND, ERROR_LEVEL,
)

if not is_configured():
    print("❌ BARK_KEY 未配置，请设置环境变量 BARK_KEY")
    print("   export BARK_KEY='你的Bark推送Key'")
    sys.exit(1)

print("🔔 开始测试 4 种通知...\n")

tests = [
    ("1/4 短会话结束", STOP_SOUND, STOP_LEVEL,
     "Claude Code · 会话结束", "已停止，本次会话 3 分 42 秒"),
    ("2/4 长任务完成", LONG_TASK_SOUND, LONG_TASK_LEVEL,
     "🎉 长任务完成", "本次会话持续 1 小时 23 分 45 秒，辛苦了！"),
    ("3/4 Git 提交", GIT_COMMIT_SOUND, GIT_COMMIT_LEVEL,
     "Git 提交", "feat: 新增天气问候 hook"),
    ("4/4 错误报警", ERROR_SOUND, ERROR_LEVEL,
     "⚠️ Bash 执行失败", "命令: rm -rf /protected | 错误: Permission denied"),
]

for label, sound, level, title, body in tests:
    print(f"  🔔 {label}：{title} ({sound})")
    send(title=title, body=body, sound=sound, level=level)
    time.sleep(1.5)

print("\n✅ 4 条通知已全部发送！检查手机确认。")
print("   如果没收到，检查 BARK_KEY 和 Bark App 通知权限。")
