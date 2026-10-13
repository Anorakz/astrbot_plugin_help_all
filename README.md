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

两级结构：先看有哪些插件，再看某个插件有什么指令。

| 命令 | 别名 | 说明 |
|:-----|:-----|:-----|
| `/功能` | `/菜单`、`/能做什么`、`/功能总览`、`/help_all` | **只列插件清单**（插件名 + 指令条数 + 示例指令） |
| `/功能 <插件名>` | | 列出**该插件的全部指令**（含别名、说明、子命令、权限） |

> 关键词也可以直接填指令名或别名，会自动定位到所属插件（如 `/功能 订阅` → RSS订阅插件）。
> 如果关键词同时匹配多个插件（如 `/功能 bangumi`），会先列出候选让你指定。

### 输出示例

`/功能` —— 插件清单：

```
插件清单 · 共 6 个

/功能 功能总览   —— 1 条指令，如 /功能
/功能 Bangumi 增强版   —— 10 条指令，如 /bgm
/功能 Bangumi 群友动态   —— 6 条指令，如 /bgm绑定
/功能 RSS订阅   —— 18 条指令，如 /sub
/功能 群聊 LLM 聊天开关   —— 5 条指令，如 /off
/功能 内置指令   —— 11 条指令，如 /help

想看某个插件的具体指令？发 /功能 <插件名>
```

`/功能 Bangumi 群友动态` —— 该插件指令：

```
【Bangumi 群友动态】6 条指令

/bgm绑定（/bgm_bind、/绑定bgm） 绑定你的 Bangumi 账号
/bgm群报（/bgm_group、/群报） 汇总全群今天谁在追番
...

发 /功能 返回插件清单
```

## 特点

- **零维护** —— 数据来自 AstrBot 运行时的指令注册表，新增/删除插件后**自动同步**，不存在硬编码清单过时的问题
- **零依赖** —— 只用 AstrBot 自身的接口
- **两级不刷屏** —— 清单只列插件名，避免一屏几十条指令糊脸
- **自动截断** —— 输出超过长度上限时自动截断并提示，避免超出发送限制
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
| `show_hint` | `true` | 插件清单中是否附一条示例指令，关闭后更紧凑 |

## 许可

MIT
