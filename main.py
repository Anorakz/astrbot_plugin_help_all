"""功能总览

一条命令看清机器人都会什么。

数据来源是 AstrBot 运行时的指令注册表（`command_management.list_commands()`），
因此**新增/删除插件后自动同步**，不需要维护任何硬编码清单。

内置的 `/help` 只列出「保留指令」（help/sid/reset 等），插件命令一概不显示，
所以有了这个插件来补上「机器人到底能做什么」这一环。
"""

from __future__ import annotations

from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register

PLUGIN_NAME = "astrbot_plugin_help_all"
BUILTIN_GROUP = "内置指令"
SELF_GROUP = "功能总览"

MAX_OUTPUT_CHARS = 1800
MAX_ALIASES = 3


@register(
    PLUGIN_NAME,
    "Anorakz",
    "一条命令看清机器人都会什么，按插件分组展示并支持关键词搜索",
    "v1.0.0",
)
class HelpAllPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.show_builtin = bool(config.get("show_builtin", True))
        self.show_permission = bool(config.get("show_permission", True))
        logger.info("[help_all] 功能总览插件已加载")

    # ── 取数 ────────────────────────────────────────────────

    async def _collect(self) -> list[dict]:
        """读取当前生效的全部指令（含插件指令）。"""
        try:
            from astrbot.core.star import command_management
        except Exception as exc:  # 框架接口变动时的兜底
            logger.warning(f"[help_all] 无法导入 command_management: {exc}")
            return []

        try:
            items = await command_management.list_commands()
        except Exception as exc:
            logger.warning(f"[help_all] 读取指令清单失败: {exc}")
            return []

        result = []
        for item in items:
            if not item.get("enabled"):
                continue
            if item.get("plugin_activated") is False:
                continue
            if item.get("reserved") and not self.show_builtin:
                continue
            result.append(item)
        return result

    # ── 渲染 ────────────────────────────────────────────────

    @staticmethod
    def _name_of(cmd: dict) -> str:
        return str(
            cmd.get("effective_command")
            or cmd.get("original_command")
            or cmd.get("handler_name")
            or "?"
        )

    def _group_of(self, cmd: dict) -> str:
        if cmd.get("reserved"):
            return BUILTIN_GROUP
        if cmd.get("plugin") == PLUGIN_NAME:
            return SELF_GROUP
        return str(
            cmd.get("plugin_display_name") or cmd.get("plugin") or "其他插件"
        )

    def _render(self, cmd: dict) -> str:
        name = self._name_of(cmd)
        line = f"/{name}"

        aliases = [
            str(a) for a in (cmd.get("aliases") or [])
            if a and str(a) != name
        ]
        if aliases:
            shown = "、".join(f"/{a}" for a in aliases[:MAX_ALIASES])
            line += f"（{shown}）"

        desc = str(cmd.get("description") or "").strip()
        if desc:
            line += f" {desc}"

        if self.show_permission:
            permission = str(cmd.get("permission") or "")
            if permission and permission not in ("everyone", "member"):
                line += f"  [需 {permission}]"

        subs = [
            s for s in (cmd.get("sub_commands") or [])
            if s.get("enabled") and s.get("effective_command")
        ]
        if subs:
            sub_text = "、".join(f"/{self._name_of(s)}" for s in subs)
            line += f"\n    子命令：{sub_text}"

        return line

    def _grouped(self, commands: list[dict]) -> dict[str, list[dict]]:
        groups: dict[str, list[dict]] = {}
        for cmd in commands:
            groups.setdefault(self._group_of(cmd), []).append(cmd)
        # 内置放最后，自身插件放最前
        ordered: dict[str, list[dict]] = {}
        for key in sorted(groups):
            if key in (SELF_GROUP, BUILTIN_GROUP):
                continue
            ordered[key] = groups[key]
        if SELF_GROUP in groups:
            ordered = {SELF_GROUP: groups[SELF_GROUP], **ordered}
        if BUILTIN_GROUP in groups:
            ordered[BUILTIN_GROUP] = groups[BUILTIN_GROUP]
        return ordered

    def _search(self, commands: list[dict], keyword: str) -> list[dict]:
        key = keyword.lower()
        hits = []
        for cmd in commands:
            haystack = " ".join(
                [
                    self._name_of(cmd),
                    str(cmd.get("description") or ""),
                    str(cmd.get("plugin") or ""),
                    str(cmd.get("plugin_display_name") or ""),
                    " ".join(str(a) for a in (cmd.get("aliases") or [])),
                ]
            ).lower()
            if key in haystack:
                hits.append(cmd)
        return hits

    @staticmethod
    def _fit(lines: list[str]) -> tuple[str, int]:
        """按长度上限拼装，返回 (文本, 被截断的条数)。"""
        out: list[str] = []
        used = 0
        kept = 0
        for line in lines:
            if used + len(line) + 1 > MAX_OUTPUT_CHARS:
                break
            out.append(line)
            used += len(line) + 1
            kept += 1
        return "\n".join(out), len(lines) - kept

    # ── 命令 ────────────────────────────────────────────────

    @filter.command("功能", alias={"菜单", "能做什么", "功能总览", "help_all"})
    async def capability(self, event: AstrMessageEvent):
        commands = await self._collect()
        if not commands:
            yield event.plain_result(
                "暂时读不到指令清单。可直接用 /help 查看内置指令。"
            )
            return

        args = (event.message_str or "").split()
        keyword = args[1].strip() if len(args) > 1 else ""

        if keyword:
            hits = self._search(commands, keyword)
            if not hits:
                yield event.plain_result(
                    f"没有匹配「{keyword}」的指令。\n"
                    f"试试 /功能 看全部（当前共 {len(commands)} 条）。"
                )
                return
            lines = [f"匹配「{keyword}」的指令 · {len(hits)} 条", ""]
            for cmd in hits:
                lines.append(self._render(cmd))
            text, dropped = self._fit(lines)
            if dropped:
                text += f"\n…… 还有 {dropped} 条被省略，换个更精确的关键词试试"
            yield event.plain_result(text)
            return

        groups = self._grouped(commands)
        lines = [f"AstrBot 功能总览 · 共 {len(commands)} 条指令", ""]
        for group_name, items in groups.items():
            lines.append(f"【{group_name}】{len(items)} 条")
            for cmd in items:
                lines.append(self._render(cmd))
            lines.append("")

        lines.append("想找具体的？发 /功能 <关键词>，例如 /功能 订阅")

        text, dropped = self._fit(lines)
        if dropped:
            text += (
                f"\n…… 因长度限制省略了 {dropped} 行，"
                "可用 /功能 <关键词> 精确查看"
            )
        yield event.plain_result(text)
