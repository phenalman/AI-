from novel import (
    generate_setting,
    generate_outline
)

from storage import (
    create_novel,
    save_setting,
    save_outline
)



def main():

    novel_name=input(
        "请输入小说名称:"
    )


    idea=input(
        "请输入小说创意:"
    )


    create_novel(
        novel_name
    )


    print(
        "正在生成设定..."
    )


    setting=generate_setting(
        idea
    )


    save_setting(
        novel_name,
        setting
    )


    print(
        "设定保存完成"
    )



    print(
        "正在生成大纲..."
    )


    outline=generate_outline(
        setting
    )


    save_outline(
        novel_name,
        outline
    )


    print(
        "大纲保存完成"
    )



if __name__=="__main__":
    main()