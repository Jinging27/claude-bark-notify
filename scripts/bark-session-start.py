"""SessionStart Hook - 清理去重缓存"""
import sys
import os

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
