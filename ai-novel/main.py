from novel import generate_setting, generate_outline, generate_chapter


def main():
    idea = input("请输入你的小说创意：")

    print("\n正在生成小说设定，请稍候...\n")

    setting = generate_setting(idea)

    print("===== 小说设定 =====")
    print(setting)

    print("\n正在生成前10章大纲，请稍候...\n")

    outline = generate_outline(setting)

    print("===== 前10章大纲 =====")
    print(outline)

    print("\n正在生成第1章，请稍候...\n")

    chapter = generate_chapter(
        setting,
        outline,
        1,
    )

    print("===== 第1章 =====")
    print(chapter)


if __name__ == "__main__":
    main()