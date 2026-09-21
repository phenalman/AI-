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
) -> str:
    prompt = f"""
{CHAPTER_PROMPT}

小说设定：

{setting}

章节大纲：

{outline}

现在请创作第 {chapter_number} 章。
"""

    return ask_ai(prompt)