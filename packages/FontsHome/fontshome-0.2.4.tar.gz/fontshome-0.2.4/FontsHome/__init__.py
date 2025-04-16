import os

__version__ = '0.2.4'
__all__ = [
    'get_font'
]


def get_font(font_name):
    # 获取当前文件的目录
    current_dir = os.path.dirname(__file__)
    # 字体文件目录
    fonts_dir = os.path.join(current_dir, 'fonts')

    # 检查字体目录是否存在
    if not os.path.exists(fonts_dir):
        RED = "\033[31m"
        RESET = "\033[0m"

        text = (
            "[FontNotFindError] Font directory not found. Please go to \"https://pan.baidu.com/s/1adAbeeSCVtLb4cq4aNYQhA?pwd=9fwn#list"
            "/path=%2F%E5%AD%97%E4%BD%93%E5%86%8C&parentPath=%2F\" Download the \"fonts\" folder and drag it into this "
            "package."
        )

        print(f"{RED}{text}{RESET}")
        return

    # 常见的字体文件扩展名
    font_extensions = [
        '.ttf',
        '.ttc',
        '.otf',
        ''
    ]

    # 在字体目录中查找匹配的字体文件
    for ext in font_extensions:
        font_file = font_name + ext
        font_path = os.path.join(fonts_dir, font_file)
        if os.path.isfile(font_path):
            return font_path

    # 如果没有找到匹配的字体文件，抛出异常
    raise FileNotFoundError(f"Font '{font_name}' not found in supported formats: {font_extensions}")
