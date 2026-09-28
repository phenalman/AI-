
from llm import ask_ai

from prompts import (
    SETTING_PROMPT,
    OUTLINE_PROMPT,
    CHAPTER_PROMPT,
)


def generate_setting(idea: str) -> str:
    prompt = f"""
{SETTING_PROMPT}

用户的小说创意：

{idea}
"""

    return ask_ai(prompt)


def generate_outline(setting: str) -> str:
    prompt = f"""
{OUTLINE_PROMPT}

以下是小说设定：

{setting}
"""

    return ask_ai(prompt)


def generate_chapter(
    setting: str,
    outline: str,
    chapter_number: int,
    previous_chapter: str = "",
) -> str:
    prompt = f"""
{CHAPTER_PROMPT}

小说设定：

{setting}

章节大纲：

{outline}

上一章正文：

{previous_chapter}

现在请创作第 {chapter_number} 章。

要求：

- 如果这是第一章，没有上一章正文，请直接开始创作。
- 如果存在上一章正文，请自然承接上一章的剧情。
- 保持人物性格、世界观和故事设定一致。
- 不要重复上一章已经发生的剧情。
- 当前章节必须推动故事继续发展。
- 直接输出小说正文，不要解释写作过程。
"""

    return ask_ai(prompt)


