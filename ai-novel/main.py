from novel import (
    generate_setting,
    generate_outline,
    generate_chapter
)

from storage import (
    create_novel,
    save_setting,
    save_outline,
    save_chapter,
    load_setting,
    load_outline,
    load_chapter,
    get_latest_chapter
)


def create_new_novel():

    novel_name = input(
        "请输入小说名称："
    )

    idea = input(
        "请输入小说创意："
    )


    # 创建目录

    create_novel(
        novel_name
    )


    print(
        "\n正在生成小说设定..."
    )

    setting = generate_setting(
        idea
    )


    save_setting(
        novel_name,
        setting
    )


    print(
        "小说设定保存完成"
    )


    print(
        "\n正在生成前10章大纲..."
    )


    outline = generate_outline(
        setting
    )


    save_outline(
        novel_name,
        outline
    )


    print(
        "小说大纲保存完成"
    )


    print(
        "\n开始创作第一章..."
    )


    chapter = generate_chapter(
        setting,
        outline,
        1
    )


    save_chapter(
        novel_name,
        1,
        chapter
    )


    print(
        "第一章保存完成"
    )



def continue_novel():

    novel_name = input(
        "请输入小说名称："
    )


    print(
        "\n正在读取小说资料..."
    )


    setting = load_setting(
        novel_name
    )


    outline = load_outline(
        novel_name
    )


    latest = get_latest_chapter(
        novel_name
    )


    if latest == 0:

        print(
            "这本小说还没有章节"
        )

        return


    next_chapter = latest + 1


    print(
        f"\n当前最新章节：第{latest}章"
    )


    print(
        f"正在生成第{next_chapter}章..."
    )


    previous_chapter = load_chapter(
        novel_name,
        latest
    )


    chapter = generate_chapter(
        setting,
        outline,
        next_chapter,
        previous_chapter
    )


    save_chapter(
        novel_name,
        next_chapter,
        chapter
    )


    print(
        f"第{next_chapter}章保存完成"
    )


def main():


    while True:

        print(
"""
====== AI小说生成器 ======

1. 创建新小说
2. 续写小说
3. 退出

"""
        )


        choice=input(
            "请选择："
        )


        if choice=="1":

            create_new_novel()


        elif choice=="2":

            continue_novel()


        elif choice=="3":

            break


        else:

            print(
                "输入错误"
            )



if __name__=="__main__":

    main()