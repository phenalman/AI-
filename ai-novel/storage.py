import os


OUTPUT_DIR = "output"



def create_novel(novel_name:str):
    """
    创建一本小说的目录结构
    """

    novel_path = os.path.join(
        OUTPUT_DIR,
        novel_name
    )

    folders = [
        "setting",
        "outline",
        "chapters"
    ]


    for folder in folders:

        path = os.path.join(
            novel_path,
            folder
        )

        os.makedirs(
            path,
            exist_ok=True
        )


    return novel_path




def save_setting(
        novel_name:str,
        content:str
):

    path = os.path.join(
        OUTPUT_DIR,
        novel_name,
        "setting",
        "setting.md"
    )


    write_file(path,content)

    return path




def save_outline(
        novel_name:str,
        content:str
):

    path = os.path.join(
        OUTPUT_DIR,
        novel_name,
        "outline",
        "outline.md"
    )


    write_file(path,content)

    return path




def save_chapter(
        novel_name:str,
        chapter_number:int,
        content:str
):

    filename = (
        f"chapter_{chapter_number:03}.md"
    )


    path = os.path.join(
        OUTPUT_DIR,
        novel_name,
        "chapters",
        filename
    )


    write_file(path,content)

    return path




def write_file(path,content):

    folder = os.path.dirname(path)

    os.makedirs(
        folder,
        exist_ok=True
    )


    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(content)