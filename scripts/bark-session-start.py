"""SessionStart Hook - 记录会话开始时间（供 Stop 计算时长）"""
import sys
import os
from datetime import datetime

SCRIPTS_DIR = os.environ.get(
    "BARK_SCRIPTS_DIR",
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, SCRIPTS_DIR)

try:
    from bark_shared import clean_seen_file
    clean_seen_file()
except Exception:
    pass

# 记录开始时间
try:
    sentinel = os.path.join(SCRIPTS_DIR, ".bark-session-start")
    with open(sentinel, "w", encoding="utf-8") as f:
        f.write(datetime.now().isoformat())
except Exception:
    pass
