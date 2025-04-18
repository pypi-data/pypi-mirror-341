__version__ = "0.0.3"


import argparse
import locale
import platform
import sys


def is_ch():
    """ 如果是Windows系统，且是中文环境，返回True"""
    return 'Chinese' in str(locale.getlocale())


def system_check(verbose=False, more_verbose=False):
    """使用platform检测操作系统类型
    :param verbose: Whether to return the system name string

    :param more_verbose: Return the original detected results

    :return: str if verbose else bool
    """
    os_name_map = {
        "Windows": "Windows",
        "Linux": "Linux",
        "Darwin": "macOS"
    }
    system_id = platform.system()
    if verbose:
        return os_name_map.get(system_id, "Unknown")
    elif more_verbose:
        return system_id
    else:
        return system_id == "Windows"


def is_idle():
    """通过检查 sys.modules 来判断是否在IDLE中运行"""
    return 'idlelib' in sys.modules


def system_clear(force=False):
    import os
    """根据系统选择清屏命令"""
    """如果是IDLE则不执行清屏"""
    if force or (not is_idle()):
        os.system("cls" if system_check() else "clear")


def color():
    """
    返回一个包含前景色、背景色和文本样式的字典列表。

    :return:
        list: 包含三个字典的列表，分别表示前景色、背景色和文本样式。
    """
    colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]

    fg = {
        **{Color: f"\033[{30 + i}m" for i, Color in enumerate(colors)},
        **{f"bright_{Color}": f"\033[{90 + i}m" for i, Color in enumerate(colors)},
        "reset": "\033[39m"
    }

    bg = {
        **{Color: f"\033[{40 + i}m" for i, Color in enumerate(colors)},
        **{f"bright_{Color}": f"\033[{100 + i}m" for i, Color in enumerate(colors)},
        "reset": "\033[49m"
    }

    style_mapping = [
        ("bold", 1), ("dim", 2), ("italic", 3), ("underline", 4),
        ("blink", 5), ("reverse", 7), ("hidden", 8), ("strikethrough", 9),
        ("reset_all", 0)
    ]
    style = {name: f"\033[{code}m" for name, code in style_mapping}

    return [fg, bg, style]


class CustomHelpFormatter(argparse.HelpFormatter):
    """
    CustomHelpFormatter 类用于自定义 argparse 模块的帮助信息格式。

    该类继承自 argparse.HelpFormatter，并重写了 _format_action_invocation 方法，以自定义命令行参数的显示方式。

    核心功能：
    - 自定义命令行参数的显示方式，使其更符合特定需求。

    使用示例：
    ```python
    import argparse

    parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
    parser.add_argument('--foo', help='foo help')
    parser.add_argument('--bar', help='bar help')
    args = parser.parse_args(['--foo', 'value'])
    ```


    """
    def __init__(self, prog):
        super().__init__(prog, max_help_position=30, width=100)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            return self._metavar_formatter(action, action.dest)(1)[0]
        else:
            parts = []
            parts.extend(action.option_strings)
            return ", ".join(parts)