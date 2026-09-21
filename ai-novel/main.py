from novel import generate_setting, generate_outline
from storage import save_text


def main():
    idea = input("请输入你的小说创意：")

    print("\n正在生成小说设定，请稍候...\n")

    setting = generate_setting(idea)

    save_text(
        "setting.md",
        setting
    )

    print("===== 小说设定 =====")
    print(setting)


    print("\n正在生成前10章大纲，请稍候...\n")

    outline = generate_outline(setting)

    save_text(
        "outline.md",
        outline
    )

    print("===== 前10章大纲 =====")
    print(outline)


if __name__ == "__main__":
    main()