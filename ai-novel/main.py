
import os
import re

from novel import (
    generate_setting,
    generate_outline,
    generate_chapter,
    generate_summary,
    generate_next_outline,
)

from storage import (
    create_novel,
    save_setting,
    save_outline,
    save_summary,
    save_chapter,
    load_setting,
    load_outline,
    load_summary,
    load_chapter,
    get_latest_chapter,
)


OUTPUT_DIR = "output"
BATCH_SIZE = 10


def outline_path(novel_name, start_chapter, end_chapter):
    """获取指定阶段大纲的文件路径。"""

    filename = (
        f"outline_{start_chapter:03}_{end_chapter:03}.md"
    )

    return os.path.join(
        OUTPUT_DIR,
        novel_name,
        "outline",
        filename,
    )


def summary_path(novel_name, start_chapter, end_chapter):
    """获取指定阶段总结的文件路径。"""

    filename = (
        f"summary_{start_chapter:03}_{end_chapter:03}.md"
    )

    return os.path.join(
        OUTPUT_DIR,
        novel_name,
        "summary",
        filename,
    )


def load_previous_summaries(novel_name, completed_chapter):
    """读取此前已经完成的阶段总结。"""

    summaries = []

    for end_chapter in range(
        BATCH_SIZE,
        completed_chapter + 1,
        BATCH_SIZE,
    ):
        start_chapter = end_chapter - BATCH_SIZE + 1

        path = summary_path(
            novel_name,
            start_chapter,
            end_chapter,
        )

        if os.path.exists(path):
            summary = load_summary(
                novel_name,
                start_chapter,
                end_chapter,
            )

            summaries.append(
                f"## 第 {start_chapter}–{end_chapter} 章总结\n\n"
                f"{summary}"
            )

    return "\n\n".join(summaries)



def chinese_number_to_int(text):
    """把中文数字章节号转换成整数。"""

    chinese_numbers = {
        "零": 0,
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
        "十": 10,
        "百": 100,
    }

    if text.isdigit():
        return int(text)

    if text == "十":
        return 10

    if "十" in text:
        parts = text.split("十")

        if parts[0] == "":
            tens = 10
        else:
            tens = chinese_numbers[parts[0]] * 10

        if len(parts) == 1 or parts[1] == "":
            ones = 0
        else:
            ones = chinese_numbers[parts[1]]

        return tens + ones

    if text in chinese_numbers:
        return chinese_numbers[text]

    return None


def extract_chapter_outline(outline, chapter_number):
    """从阶段大纲中提取指定章节；支持阿拉伯数字和中文数字章节号。"""

    pattern = re.compile(
        r"^\s*(?:#{1,6}\s*)?第\s*([0-9零一二三四五六七八九十百]+)\s*章.*$",
        re.MULTILINE,
    )

    matches = list(pattern.finditer(outline))

    for index, match in enumerate(matches):
        chapter_text = match.group(1)
        detected_number = chinese_number_to_int(chapter_text)

        if detected_number == chapter_number:
            start = match.start()

            if index + 1 < len(matches):
                end = matches[index + 1].start()
            else:
                end = len(outline)

            return outline[start:end].strip()

    print(
        f"提示：没有识别出第 {chapter_number} 章的独立大纲，"
        "本次将使用完整阶段大纲。"
    )

    return outline


def finalize_completed_batch(novel_name, setting, completed_chapter):
    """
    每完成 10 章：
    1. 生成并保存阶段总结。
    2. 生成并保存下一阶段大纲。
    """

    if completed_chapter < BATCH_SIZE:
        return

    if completed_chapter % BATCH_SIZE != 0:
        return

    start_chapter = completed_chapter - BATCH_SIZE + 1
    end_chapter = completed_chapter

    current_summary_path = summary_path(
        novel_name,
        start_chapter,
        end_chapter,
    )

    # 第一步：生成阶段总结（如果尚未保存）。
    if not os.path.exists(current_summary_path):
        print(
            f"\n正在整理第 {start_chapter}–{end_chapter} 章的剧情总结..."
        )

        chapters = []

        for number in range(start_chapter, end_chapter + 1):
            chapter_text = load_chapter(
                novel_name,
                number,
            )

            chapters.append(
                f"# 第 {number} 章\n\n{chapter_text}"
            )

        chapters_text = "\n\n".join(chapters)

        summary = generate_summary(
            setting,
            start_chapter,
            end_chapter,
            chapters_text,
        )

        save_summary(
            novel_name,
            start_chapter,
            end_chapter,
            summary,
        )

        print(
            f"阶段总结已保存：第 {start_chapter}–{end_chapter} 章"
        )
    else:
        print(
            f"第 {start_chapter}–{end_chapter} 章的总结已存在，跳过生成。"
        )

    # 第二步：为下一阶段生成大纲（如果尚未保存）。
    next_start = completed_chapter + 1
    next_end = completed_chapter + BATCH_SIZE

    next_outline_path = outline_path(
        novel_name,
        next_start,
        next_end,
    )

    if not os.path.exists(next_outline_path):
        print(
            f"\n正在生成第 {next_start}–{next_end} 章的大纲..."
        )

        previous_summaries = load_previous_summaries(
            novel_name,
            completed_chapter,
        )

        next_outline = generate_next_outline(
            setting,
            previous_summaries,
            next_start,
            next_end,
        )

        save_outline(
            novel_name,
            next_start,
            next_end,
            next_outline,
        )

        print(
            f"下一阶段大纲已保存：第 {next_start}–{next_end} 章"
        )
    else:
        print(
            f"第 {next_start}–{next_end} 章的大纲已存在，跳过生成。"
        )


def create_new_novel():
    """创建新小说，生成设定、首批大纲和第一章。"""

    novel_name = input("请输入小说名称：").strip()

    if not novel_name:
        print("小说名称不能为空。")
        return

    novel_dir = os.path.join(OUTPUT_DIR, novel_name)

    if os.path.exists(novel_dir):
        print(
            "这个小说目录已经存在。为避免覆盖已有作品，"
            "请使用续写功能，或换一个小说名称。"
        )
        return

    idea = input("请输入小说创意：").strip()

    if not idea:
        print("小说创意不能为空。")
        return

    create_novel(novel_name)

    print("\n正在生成小说设定...")

    setting = generate_setting(idea)

    save_setting(novel_name, setting)

    print("小说设定保存完成。")

    print("\n正在生成第 1–10 章大纲...")

    outline = generate_outline(setting)

    save_outline(
        novel_name,
        1,
        BATCH_SIZE,
        outline,
    )

    print("首批大纲保存完成。")

    chapter_number = 1

    chapter_outline = extract_chapter_outline(
        outline,
        chapter_number,
    )

    print("\n正在创作第一章...")

    chapter = generate_chapter(
        setting,
        chapter_outline,
        chapter_number,
    )
    print("第一章正文类型：", type(chapter))
    print("第一章正文长度：", len(chapter) if isinstance(chapter, str) else "不是字符串")
    save_chapter(
        novel_name,
        chapter_number,
        chapter,
    )

    print("第一章保存完成。")
  

def continue_novel():
    """续写下一章，并在每 10 章完成时处理阶段任务。"""

    novel_name = input("请输入小说名称：").strip()

    if not novel_name:
        print("小说名称不能为空。")
        return

    novel_dir = os.path.join(OUTPUT_DIR, novel_name)

    if not os.path.isdir(novel_dir):
        print("没有找到这本小说，请检查名称是否正确。")
        return

    print("\n正在读取小说资料...")

    setting = load_setting(novel_name)

    latest = get_latest_chapter(novel_name)

    if latest == 0:
        print("这本小说还没有章节，请检查小说文件。")
        return

    # 如果上次在完成整十章节后中断，先补做阶段任务。
    if latest % BATCH_SIZE == 0:
        finalize_completed_batch(
            novel_name,
            setting,
            latest,
        )

    next_chapter = latest + 1

    # 例如第 11 章使用第 11–20 章的大纲。
    stage_start = (
        (next_chapter - 1) // BATCH_SIZE
    ) * BATCH_SIZE + 1

    stage_end = stage_start + BATCH_SIZE - 1

    current_outline_path = outline_path(
        novel_name,
        stage_start,
        stage_end,
    )

    # 如果当前阶段大纲不存在，尝试根据此前总结生成。
    if not os.path.exists(current_outline_path):
        print(
            f"\n缺少第 {stage_start}–{stage_end} 章的大纲，"
            "正在生成..."
        )

        previous_summaries = load_previous_summaries(
            novel_name,
            stage_start - 1,
        )

        if stage_start == 1:
            outline = generate_outline(setting)
        else:
            outline = generate_next_outline(
                setting,
                previous_summaries,
                stage_start,
                stage_end,
            )

        save_outline(
            novel_name,
            stage_start,
            stage_end,
            outline,
        )

    outline = load_outline(
        novel_name,
        stage_start,
        stage_end,
    )

    previous_chapter = load_chapter(
        novel_name,
        latest,
    )

    previous_summaries = load_previous_summaries(
        novel_name,
        stage_start - 1,
    )

    chapter_outline = extract_chapter_outline(
        outline,
        next_chapter,
    )

    print(
        f"\n当前最新章节：第 {latest} 章"
    )

    print(
        f"正在生成第 {next_chapter} 章..."
    )

    chapter = generate_chapter(
        setting,
        chapter_outline,
        next_chapter,
        previous_chapter,
        previous_summaries,
    )

    save_chapter(
        novel_name,
        next_chapter,
        chapter,
    )

    print(
        f"第 {next_chapter} 章保存完成。"
    )

    # 第 10、20、30……章完成后自动总结并规划下一阶段。
    finalize_completed_batch(
        novel_name,
        setting,
        next_chapter,
    )


def main():
    """程序主菜单。"""

    while True:
        print(
            """
====== AI 小说生成器 ======

1. 创建新小说
2. 续写小说
3. 退出

"""
        )

        choice = input("请选择：").strip()

        if choice == "1":
            create_new_novel()

        elif choice == "2":
            continue_novel()

        elif choice == "3":
            print("已退出小说生成器。")
            break

        else:
            print("输入错误，请输入 1、2 或 3。")


if __name__ == "__main__":
    main()