import os
# 导入 os 模块，提供操作系统相关的功能，如文件路径操作。
import sys
# 导入 sys 模块，提供与 Python 解释器交互的接口，例如获取 Python 可执行文件路径。
import shutil
# 导入 shutil 模块，提供高级文件操作功能，例如查找可执行文件。
import subprocess
# 导入 subprocess 模块，用于创建和管理子进程，方便执行外部命令（如 pip）。
from typing import Optional
# 从 typing 模块导入 Optional 类型，用于类型提示，表明变量可以为指定类型或 None。

def install_jupyterlab_language_pack(
    language_code: str = "jupyterlab-language-pack-zh-CN",
    # 要安装的 JupyterLab 语言包名称，默认为简体中文包。
    default_pip_path: str = r"C:\anaconda3\Scripts\pip.exe",
    # 默认 pip 可执行文件的完整路径，适用于 Anaconda 环境。
    mirror_url: Optional[str] = r"https://pypi.tuna.tsinghua.edu.cn/simple",
    # PyPI 镜像源 URL，用于加速包的下载。例如，清华镜像源。可以设置为 None 以使用默认 PyPI。
    prefer_default_pip: bool = 0
    # 布尔值，指示是否优先使用提供的默认 pip 路径。
    # 默认为 False，表示优先在系统路径中查找 pip。设置为 True 时，会先检查 default_pip_path。
) -> bool:
    """使用 pip 安装指定的 JupyterLab 语言包，并返回安装结果。

    Args:
        language_code (str, optional): 要安装的语言包名称。
            默认为 "jupyterlab-language-pack-zh-CN" (简体中文)。
        default_pip_path (str, optional): 默认的 pip 可执行文件路径。
            默认为 r"C:\anaconda3\Scripts\pip.exe"。
        mirror_url (str, optional): PyPI 镜像源 URL。
            例如 "https://pypi.tuna.tsinghua.edu.cn/simple"。默认为 None。
        prefer_default_pip (bool, optional): 是否优先使用提供的默认 pip 路径。
            默认为 False。如果为 True，则优先查找 default_pip_path。

    Returns:
        bool: True 表示语言包安装成功，False 表示安装失败。
    """
    language_code = language_code.strip()
    # 移除语言包名称两侧的空白字符，确保名称的准确性。
    pip_location = None
    # 初始化 pip_location 变量，用于存储找到的 pip 可执行文件路径。

    if prefer_default_pip:
        # 如果用户选择优先使用默认 pip 路径。
        if os.path.exists(default_pip_path):
            # 检查提供的默认 pip 路径是否存在于文件系统中。
            pip_location = default_pip_path
            # 如果存在，则将 pip_location 设置为默认路径。
            print(f"使用預設 Pip 位置: {pip_location}")
        else:
            # 如果默认 pip 路径不存在。
            print(f"預設 Pip 位置無效: {default_pip_path}，將嘗試其他方法。")
    else:
        # 如果用户选择优先查找系统路径中的 pip。
        print("將優先查找系統路徑中的 pip。")

    if not pip_location:
        # 如果之前没有找到 pip，尝试通过导入自定义模块获取。
        try:
            import f_other.system_info as sys_info
            # 尝试导入名为 f_other.system_info 的自定义模块。
            pip_location = sys_info.get_pip_location()
            # 调用自定义模块中的函数来获取 pip 的位置。
            if pip_location:
                print(f"Pip 位置 (來自自訂模組): {pip_location}")
            else:
                print("自訂模組未找到 pip，將嘗試其他方法。")
        except ImportError:
            # 如果导入自定义模块失败（例如，模块不存在）。
            print("無法導入 f_other.system_info 模組，將嘗試其他方法。")

    if not pip_location:
        # 如果仍然没有找到 pip，尝试使用 shutil.which 在系统 PATH 中查找。
        pip_location = shutil.which("pip")
        # shutil.which 会在系统的环境变量 PATH 中搜索指定的可执行文件。
        if pip_location:
            print(f"Pip 位置 (來自 shutil.which): {pip_location}")
        else:
            print("shutil.which 未找到 pip。")

    if not pip_location and not prefer_default_pip:
        # 如果在不优先使用默认 pip 的情况下，系统路径中找不到，则最后检查默认路径。
        if os.path.exists(default_pip_path):
            pip_location = default_pip_path
            print(f"使用預設 Pip 位置: {pip_location}")
        else:
            print(f"預設 Pip 位置無效: {default_pip_path}。")

    if not pip_location:
        # 如果到目前为止仍然没有找到 pip 的位置。
        print(
            "找不到 pip。請確保 pip 已安裝並且在系統路徑中，或提供正確的預設路徑。"
        )
        return False

    install_command = [pip_location, "install", language_code]
    # 构建 pip install 命令的列表，包括 pip 的路径、install 命令和要安装的语言包名称。

    if mirror_url:
        # 如果提供了镜像源 URL，则将其添加到 pip 命令中。
        install_command.extend(["-i", mirror_url])
        # -i 参数用于指定 pip 的镜像源。

    print(f"安装命令: {' '.join(install_command)}")
    # 打印即将执行的完整 pip 安装命令。

    process = subprocess.run(
        install_command,
        capture_output=True,
        # 捕获子进程的输出（包括标准输出和标准错误）。
        text=True,
        # 将输出解码为文本格式。
        encoding='utf-8'
        # 指定输出的编码格式为 UTF-8。
    )

    print(f"Python 可执行文件: {sys.executable}")
    # 打印当前 Python 解释器的可执行文件路径，用于调试。
    print(f"验证后的 pip 位置: {shutil.which('pip')}")
    # 再次使用 shutil.which 验证当前系统是否能找到 pip，用于调试。

    if process.returncode == 0:
        # 如果子进程的返回码为 0，表示命令执行成功。
        print("JupyterLab 语言包安装成功。")
        return True
    else:
        # 如果子进程的返回码不为 0，表示命令执行失败。
        print("JupyterLab 语言包安装失败。")
        print(f"错误信息:\n{process.stderr}")
        # 打印错误信息，帮助用户诊断问题。
        return False

if __name__ == "__main__":
    # 当此脚本作为主程序运行时，执行以下代码。
    # 使用清华镜像源安装简体中文语言包，并优先使用系统路径中的 pip。
    installation_successful = install_jupyterlab_language_pack(
        language_code="jupyterlab-language-pack-zh-CN",
        mirror_url="https://pypi.tuna.tsinghua.edu.cn/simple",
        prefer_default_pip=False
    )
    print(f"安装是否成功: {installation_successful}")

    # 使用清华镜像源安装简体中文语言包，并优先使用默认提供的 pip 路径。
    installation_successful_default_pip = install_jupyterlab_language_pack(
        language_code="jupyterlab-language-pack-zh-CN",
        mirror_url="https://pypi.tuna.tsinghua.edu.cn/simple",
        prefer_default_pip=True
    )
    print(f"安装是否成功 (優先使用預設 pip): {installation_successful_default_pip}")