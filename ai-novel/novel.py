
from llm import ask_ai

from prompts import (
    SETTING_PROMPT,
    OUTLINE_PROMPT,
    CHAPTER_PROMPT,
    SUMMARY_PROMPT,
    NEXT_OUTLINE_PROMPT,
)


def generate_setting(idea: str) -> str:
    """根据用户创意生成小说设定。"""

    prompt = f"""
{SETTING_PROMPT}

用户的小说创意：

{idea}
"""
    return ask_ai(prompt)


def generate_outline(setting: str) -> str:
    """生成小说最初的 10 章大纲。"""

    prompt = f"""
{OUTLINE_PROMPT}

以下是小说设定：

{setting}

请生成第 1 章至第 10 章的大纲。
"""
    return ask_ai(prompt)


def generate_next_outline(
    setting: str,
    previous_summaries: str,
    start_chapter: int,
    end_chapter: int,
) -> str:
    """根据小说设定和已有总结生成下一阶段大纲。"""

    prompt = f"""
{NEXT_OUTLINE_PROMPT}

小说设定：

{setting}

此前各阶段的剧情总结：

{previous_summaries or "目前没有此前阶段的剧情总结。"}

本次需要规划的章节范围：
第 {start_chapter} 章至第 {end_chapter} 章。

请只生成指定范围内的章节大纲，并确保章节编号正确。
"""
    return ask_ai(prompt)


def generate_summary(
    setting: str,
    start_chapter: int,
    end_chapter: int,
    chapters_text: str,
) -> str:
    """总结指定章节范围内的剧情。"""

    prompt = f"""
{SUMMARY_PROMPT}

小说设定：

{setting}

需要总结的章节范围：
第 {start_chapter} 章至第 {end_chapter} 章。

以下是这些章节的正文：

{chapters_text}

请根据以上正文生成阶段剧情总结。
"""
    return ask_ai(prompt)


def generate_chapter(
    setting: str,
    outline: str,
    chapter_number: int,
    previous_chapter: str = "",
    previous_summaries: str = "",
    chapter_outline: str = "",
) -> str:
    """根据设定、大纲和上一章正文生成指定章节。"""

    current_outline = chapter_outline or outline

    prompt = f"""
{CHAPTER_PROMPT}

小说设定：

{setting}

此前各阶段的剧情总结：

{previous_summaries or "目前没有此前阶段的总结。"}

当前阶段的大纲：

{outline}

当前章节的具体大纲：

{current_outline}

上一章正文：

{previous_chapter or "目前没有上一章正文，这是小说第一章。"}

现在请创作第 {chapter_number} 章。

要求：

- 严格遵守小说设定和已确认的剧情事实。
- 依据当前章节的具体大纲推进剧情。
- 如果存在上一章正文，请自然承接其结尾。
- 不要重复上一章已经发生的剧情。
- 不要提前完成后续章节的重要剧情。
- 保持人物性格、人物关系和世界观一致。
- 直接输出小说正文，不要解释写作过程。
"""
    return ask_ai(prompt)