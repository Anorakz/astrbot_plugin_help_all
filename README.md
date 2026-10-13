<div align="center">

# 功能总览

[![AstrBot](https://img.shields.io/badge/AstrBot-%3E%3D4.24.0-blue)](https://github.com/AstrBotDevs/AstrBot)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**一条命令看清机器人都会什么**

</div>

## 为什么需要它

AstrBot 自带的 `/help` **只显示内置的保留指令**（`help` / `sid` / `reset` / `provider` 等），
所有**插件指令一个都不显示** —— 装了十几个插件之后，你根本不知道机器人现在能做什么。

本插件补上这一环：动态读取 AstrBot 的指令注册表，按插件分组列出**全部**可用指令。

## 命令

| 命令 | 别名 | 说明 |
|:-----|:-----|:-----|
| `/功能` | `/菜单`、`/能做什么`、`/功能总览`、`/help_all` | 按插件分组列出全部指令 |
| `/功能 <关键词>` | | 搜索指令（匹配命令名、说明、插件名、别名） |

### 输出示例

```
AstrBot 功能总览 · 共 52 条指令

【RSS订阅】18 条
/sub（/订阅） 新增订阅
/sub_list（/订阅列表） 查看当前会话订阅
...

【Bangumi 群友动态】6 条
/bgm绑定（/bgm_bind） 绑定你的 Bangumi 账号
...

【内置指令】11 条
/help 查看帮助
...

想找具体的？发 /功能 <关键词>，例如 /功能 订阅
```

## 特点

- **零维护** —— 数据来自 AstrBot 运行时的指令注册表，新增/删除插件后**自动同步**，不存在硬编码清单过时的问题
- **零依赖** —— 只用 AstrBot 自身的接口
- **自动截断** —— 输出超过长度上限时自动截断并提示用关键词精确查找，避免刷屏或超出发送限制
- **权限标注** —— 需要管理员权限的指令会标注出来
- **命令组展开** —— 命令组（如 `/sub_profile set|get`）会展示子命令

## 安装

```bash
docker exec astrbot sh -c \
  'cd /AstrBot/data/plugins && git clone --depth 1 \
   https://github.com/Anorakz/astrbot_plugin_help_all.git'
docker compose restart astrbot
```

## 配置

| 配置项 | 默认 | 说明 |
|:-------|:-----|:-----|
| `show_builtin` | `true` | 是否显示内置指令（归到「内置指令」分组） |
| `show_permission` | `true` | 是否标注权限要求 |

## 许可

MIT
