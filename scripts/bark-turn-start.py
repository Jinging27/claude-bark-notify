"""UserPromptSubmit Hook - 记录本轮提问时间（供 Stop 计算单轮时长）"""
import os
from datetime import datetime

SCRIPTS_DIR = os.environ.get(
    "BARK_SCRIPTS_DIR",
    os.path.dirname(os.path.abspath(__file__))
)

try:
    sentinel = os.path.join(SCRIPTS_DIR, ".bark-turn-start")
    with open(sentinel, "w", encoding="utf-8") as f:
        f.write(datetime.now().isoformat())
except Exception:
    pass
