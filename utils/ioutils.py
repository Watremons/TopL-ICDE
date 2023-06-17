import os


def create_folder(folder_name: str) -> None:
    # Create folder at "../<folder_name>"
    folder_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_name)  # 创建data文件夹
