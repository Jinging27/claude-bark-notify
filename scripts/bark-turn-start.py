"""UserPromptSubmit Hook - 记录本轮提问时间（供 Stop 计算单轮时长）"""
import sys
import os
from datetime import datetime

SCRIPTS_DIR = os.environ.get(
    "BARK_SCRIPTS_DIR",
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, SCRIPTS_DIR)

from bark_shared import TURN_SENTINEL

try:
    with open(TURN_SENTINEL, "w", encoding="utf-8") as f:
        f.write(datetime.now().isoformat())
except Exception:
    pass
