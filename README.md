<div align="center">

# 🔔 Claude Bark Notify

**Claude Code 手机推送通知系统 — 基于 Bark**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Hook-orange.svg)](https://docs.anthropic.com/en/docs/claude-code)
[![Bark](https://img.shields.io/badge/Bark-iOS%20Push-green.svg)](https://github.com/Finb/Bark)

*让你的手机成为 Claude Code 的通知中心 📱*

</div>

---

## ✨ 功能一览

| # | 功能 | 触发时机 | 默认声音 | 级别 |
|---|------|---------|---------|------|
| 🟢 | **短会话结束** | 会话 < 10 分钟 | `healthnotification` | active |
| 🟣 | **长任务完成** | 会话 ≥ 10 分钟 | `shake` | active |
| 🔵 | **Git 提交通知** | `git commit` 成功 | `chime` | active |
| 🔴 | **错误报警** | 任何工具调用失败 | `alarm` | ⚡ timeSensitive |

> **timeSensitive** 级别会突破 iOS 勿扰模式，重要错误绝不错过。

---

## 📁 文件结构

```
~/.claude/scripts/
├── bark_shared.py          # 共享模块（Bark API 封装、去重逻辑）
├── bark_sounds.py          # 🔧 声音配置文件（改声音改这个）
├── bark-stop.py            # Stop hook：智能判断短会话 / 长任务
├── bark-session-start.py   # SessionStart hook：记录开始时间
├── bark-git-commit.py      # PostToolUse hook：Git 提交通知
├── bark-error.py           # PostToolUseFailure hook：错误报警
└── bark-test.py            # 🧪 一键测试脚本
```

---

## 🚀 快速开始

### 前提条件

- [Claude Code](https://claude.ai/code) 已安装
- [Bark](https://github.com/Finb/Bark) iOS App 已安装并获取到推送 Key
- Python 3.8+

### 第一步：下载脚本

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/claude-bark-notify.git

# 复制脚本到 Claude Code hooks 目录
cp claude-bark-notify/scripts/*.py ~/.claude/scripts/
```

### 第二步：配置 BARK_KEY

在你的 shell 配置文件（`.bashrc` / `.zshrc` / PowerShell `$PROFILE`）中添加：

```bash
# Bash / Zsh
export BARK_KEY="你的Bark推送Key"

# PowerShell
$env:BARK_KEY = "你的Bark推送Key"
```

或者在 Claude Code 的 `settings.json` 中配置：

```json
{
  "env": {
    "BARK_KEY": "你的Bark推送Key"
  }
}
```

### 第三步：添加 Hook 配置

编辑 `~/.claude/settings.json`（用户级）或 `.claude/settings.json`（项目级），在 `hooks` 中添加：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "command": "python3 ~/.claude/scripts/bark-session-start.py",
            "type": "command",
            "timeout": 5
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "command": "python3 ~/.claude/scripts/bark-stop.py",
            "statusMessage": "推送 Bark 通知...",
            "timeout": 15,
            "type": "command"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "command": "python3 ~/.claude/scripts/bark-git-commit.py",
            "if": "Bash(git commit*)",
            "type": "command",
            "async": true,
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUseFailure": [
      {
        "hooks": [
          {
            "command": "python3 ~/.claude/scripts/bark-error.py",
            "type": "command",
            "async": true,
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

> ⚠️ 如果你的 `hooks` 中已有其他 hook，请将上述条目**追加到对应数组**中，不要覆盖。

### 第四步：测试

```bash
python3 ~/.claude/scripts/bark-test.py
```

手机应该收到 4 条测试通知，声音各不相同 🔊

---

## 🎵 自定义声音

编辑 `bark_sounds.py`，修改对应的值即可：

```python
# 🟢 短会话结束
STOP_SOUND = "healthnotification"   # 改成你喜欢的声音
STOP_LEVEL = "active"

# 🟣 长任务完成
LONG_TASK_SOUND = "shake"
LONG_TASK_LEVEL = "active"

# 🔵 Git 提交
GIT_COMMIT_SOUND = "chime"
GIT_COMMIT_LEVEL = "active"

# 🔴 错误报警
ERROR_SOUND = "alarm"
ERROR_LEVEL = "timeSensitive"       # ⚡ 突破勿扰
```

<details>
<summary>📋 完整声音列表（点击展开）</summary>

| 声音名 | 描述 |
|--------|------|
| `alarm` | 警报声（刺耳，适合紧急） |
| `anticipatory` | 期待感音效 |
| `bell` | 铃声 |
| `bloom` | 花开音效 |
| `calypso` | 卡里普索风 |
| `chime` | 风铃声 |
| `classic` | 经典提示音 |
| `cricket` | 蟋蟀声 |
| `default` | 系统默认 |
| `dog` | 狗叫 |
| `electronic` | 电子音 |
| `fanfare` | 号角声 |
| `glass` | 玻璃声 |
| `healthnotification` | 健康通知音 |
| `keys` | 键盘声 |
| `lively` | 活泼音效 |
| `multiwayinvitation` | 多路邀请 |
| `newmail` | 新邮件 |
| `noir` | 黑色电影风 |
| `piano` | 钢琴声 |
| `pop` | 弹出音 |
| `pulse` | 脉冲声 |
| `radiant` | 光芒音效 |
| `shake` | 震动声 |
| `shimmer` | 闪烁音 |
| `silent` | 静音 |
| `spell` | 咒语声 |
| `telegraph` | 电报声 |
| `tremolo` | 颤音 |
| `triumphant` | 凯旋声 |
| `upbeat` | 欢快音效 |
| `vibrate` | 震动 |
| `whistle` | 口哨声 |

</details>

---

## 🔧 工作原理

```
┌─────────────────────────────────────────────────┐
│              Claude Code Hook 系统               │
├─────────────┬───────────────┬───────────────────┤
│ SessionStart│      Stop     │ PostToolUse(Fail) │
└──────┬──────┴───────┬───────┴─────────┬─────────┘
       │              │                 │
       ▼              ▼                 ▼
  记录开始时间    计算会话时长        提取错误信息
       │              │                 │
       └──────────────┼─────────────────┘
                      ▼
              ┌──────────────┐
              │  bark_shared  │  ← 统一封装 Bark API
              │   .send()    │
              └──────┬───────┘
                     ▼
              ┌──────────────┐
              │  api.day.app │  ← Bark 推送服务
              └──────┬───────┘
                     ▼
                 📱 iPhone
```

### 智能时长判断

- **SessionStart** 时记录时间戳到 `.bark-session-start`
- **Stop** 时读取时间戳，计算精确到秒的会话时长
- 时长 < 10 分钟 → 短会话通知（healthnotification）
- 时长 ≥ 10 分钟 → 长任务通知（shake 🎉）

### Git 提交去重

- 从 `git commit` 输出中提取 commit hash
- 已通知的 hash 记录在 `.bark-seen-commits`
- 自动跳过重复通知，最多保留 200 条记录

### 错误报警

- 任何工具调用失败（Bash 报错、Write 权限不足等）
- 自动提取工具名、命令/文件路径、错误信息
- 以 `timeSensitive` 级别推送，突破勿扰模式

---

## 🤝 与其他 Hook 共存

本项目的所有 hook 都是**追加式**的，不会影响你已有的 hook 配置。

比如你已经有 Clawd on Desk 的 hook：

```json
"Stop": [
  {
    "hooks": [{ "command": "python3 ~/.claude/scripts/bark-stop.py", ... }]
  },
  {
    "matcher": "",
    "hooks": [{ "command": "clawd-hook.js Stop", ... }]
  }
]
```

两个 hook 各自独立运行，互不干扰。

---

## ❓ FAQ

**Q: 通知没收到？**
1. 确认 `BARK_KEY` 环境变量已设置
2. 确认 Bark App 有通知权限
3. 运行 `python3 ~/.claude/scripts/bark-test.py` 测试

**Q: 怎么只关闭某个通知？**
在 `bark_sounds.py` 中把对应声音改成 `"silent"` 即可静音。

**Q: Windows 路径怎么写？**
Hook 命令中用正斜杠：`python3 C:/Users/你的用户名/.claude/scripts/bark-stop.py`

**Q: macOS / Linux 可以用吗？**
可以！把脚本路径改成 `~/.claude/scripts/` 即可，代码兼容全平台。

---

## 📄 License

[MIT](LICENSE) — 随便用，开心就好 🎉

---

<div align="center">

**如果觉得有用，给个 ⭐ 吧！**

Made with ❤️ by [Your Name]

</div>
