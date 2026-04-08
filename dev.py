"""
开发相关的命令集合，包含代码格式化、静态类型检查、代码质量检查等功能。
"""
import os
import sys
import atexit
import platform
import subprocess
from pathlib import Path
from functools import wraps
from time import perf_counter_ns as get_time_ns

import rich
import rich.console
import typer

CWD = Path(__file__).parent

CONSOLE = rich.console.Console()


def mark_text(text: str, mark: str) -> str:
    """ 使用 rich 的标记语法为文本添加颜色或样式 """
    return f"[{mark}]{text}[/{mark}]"


def show_time_spent(start_time: int, end_time: int, cmd: str) -> None:
    """ 显示命令执行的耗时，自动选择合适的时间单位 """
    units = ("ns", "µs", "ms", "s")
    unit_index = 0
    elapsed_time: float = end_time - start_time
    while elapsed_time >= 1000 and unit_index < len(units) - 1:
        elapsed_time /= 1000
        unit_index += 1
    rich.print(
        mark_text(
            rf"\[dev.py] 命令 '{cmd}' 执行成功, 耗时: {elapsed_time:.2f} {units[unit_index]}",
            "green",
        )
    )


def cmd_run(
    cmd: list[str | Path],
    capture_output: bool = False,
    error_on_output: bool = False,
    cwd: Path = CWD,
) -> str:
    """ 模拟命令行终端运行命令 """
    if error_on_output:
        capture_output = True

    norm_cmd = [str(i) for i in cmd]
    rich.print(mark_text(rf"\[command] {' '.join(norm_cmd)}", "cyan"))
    try:
        ret = subprocess.run(
            norm_cmd,
            stdout=subprocess.PIPE if capture_output else sys.stdout,
            stderr=subprocess.STDOUT,
            text=capture_output,
            cwd=cwd,
            check=True,
        )
    except FileNotFoundError:
        rich.print(mark_text(rf"\[command] 未找到指令：{norm_cmd[0]}", "red"))
        sys.exit(1)

    if ret.stdout:
        print(ret.stdout, end="", flush=True)

    if (error_on_output and ret.stdout) and not ret.returncode:
        # 如果有 stdout 并且存在错误，则设置返回代码为 1
        ret.returncode = 1

    ret.check_returncode()
    return ret.stdout.strip() if capture_output else ""


def get_poetry_executable() -> Path | None:
    """ 查找 Poetry 可执行文件的路径 """
    rich.print(mark_text(r"\[dev.py] 查找 Poetry 可执行文件", "green"))
    try:
        # 命令行查找
        subprocess.run(
            ["poetry", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        if sys.platform == "win32":
            poetry_path = cmd_run(["where", "poetry"], capture_output=True)
        else:
            poetry_path = cmd_run(["which", "poetry"], capture_output=True)
        if poetry_path and Path(poetry_path).exists():
            return Path(poetry_path)
        raise FileNotFoundError("Poetry executable not found in PATH")

    except (subprocess.CalledProcessError, FileNotFoundError):
        # 命令行查找失败，遍历常见路径
        poetry_paths = [
            Path.home() / ".local/bin/poetry",
            Path.home() / ".local/share/pypoetry/venv/bin/poetry",
            Path.home() / ".local/share/pypoetry/venv/Scripts/poetry",
            Path(os.environ.get("APPDATA", Path.home())) / "Python/Scripts/poetry.exe",
            Path("/usr/local/bin/poetry"),
            Path("/usr/bin/poetry"),
        ]

        for path in poetry_paths:
            if path.exists() and os.access(path, os.X_OK):
                rich.print(
                    mark_text(rf"\[dev.py] 找到 Poetry 可执行文件：{path}", "green")
                )
                return path
    rich.print(mark_text(r"\[dev.py] 未找到 Poetry 可执行文件", "red"))
    return None


def prep_poetry() -> Path:
    """ 准备 Poetry，确保后续命令可以使用 Poetry 来管理依赖 """
    rich.print(mark_text(r"\[dev.py] 准备 Poetry 中", "green"))

    poetry_path = get_poetry_executable()
    if poetry_path is None:
        rich.print(mark_text(r"\[dev.py] Poetry 未找到，请先安装 Poetry", "red"))
        sys.exit(1)

    rich.print(mark_text(rf"\[dev.py] Poetry 已就绪 ({poetry_path})", "green"))

    return poetry_path


def remind_switch_venv(venv_py: Path) -> None:
    """ 提醒用户切换到虚拟环境，确保后续命令在隔离的环境中运行 """
    if sys.executable != str(venv_py):
        rich.print(
            mark_text(
                rf"\[dev.py] 当前 Python 解释器是 {sys.executable}，建议使用虚拟环境 {venv_py} 来运行后续命令以确保依赖隔离",
                "yellow",
            )
        )
        if platform.system() == "Windows":
            rich.print(
                mark_text(
                    rf"\[dev.py] 运行 {venv_py.parent / 'activate'} 来激活虚拟环境",
                    "cyan",
                )
            )
        else:
            rich.print(
                mark_text(
                    rf"\[dev.py] 运行 source {venv_py.parent / 'activate'} 来激活虚拟环境",
                    "cyan",
                )
            )


def prep_venv(poetry_path: Path, py: Path) -> Path:
    """ 准备虚拟环境，确保后续命令在隔离的环境中运行 """
    rich.print(mark_text(r"\[dev.py] 准备虚拟环境中", "green"))

    cmd_run([poetry_path, "env", "use", py])
    venv_py = cmd_run([poetry_path, "env", "info", "--path"], capture_output=True)
    if sys.platform == "win32":
        venv_py = Path(venv_py) / "Scripts" / "python.exe"
    else:
        venv_py = Path(venv_py) / "bin" / "python"

    atexit.register(remind_switch_venv, venv_py)
    rich.print(mark_text(rf"\[dev.py] 虚拟环境已就绪 ({venv_py})", "green"))
    return venv_py


def prep_deps(poetry_path: Path) -> None:
    """ 使用 Poetry 安装项目依赖 """
    rich.print(mark_text(r"\[dev.py] 安装开发环境依赖中", "green"))

    try:
        cmd_run([poetry_path, "install", "--no-root"])
    except subprocess.CalledProcessError as e:
        rich.print(mark_text(r"\[dev.py] 项目依赖安装失败", "red"))
        raise e

    rich.print(mark_text(r"\[dev.py] 开发环境已就绪", "green"))


def prep_all() -> tuple[Path, Path]:
    """ 一键准备所有环境，确保后续命令可以顺利运行 """
    poetry_path = prep_poetry()
    venv_py = prep_venv(poetry_path, sys.executable)
    prep_deps(poetry_path)

    return poetry_path, venv_py


app = typer.Typer(
    help="开发相关的命令集合",
    add_completion=False,
)


def command(func):
    """ 装饰器，用于包装命令函数，添加统一的日志输出和错误处理 """
    @app.command()
    @wraps(func)
    def command_func(*args, **kwargs):
        start_time = get_time_ns()
        rich.print(mark_text(rf"\[dev.py] 运行命令 '{func.__name__}'", "green"))

        try:
            result = func(*args, **kwargs)
        except subprocess.CalledProcessError:
            rich.print(
                mark_text(
                    rf"\[dev.py] 命令 '{func.__name__}' 运行失败，请检查错误信息", "red"
                )
            )
            sys.exit(1)
        except KeyboardInterrupt:
            rich.print(
                mark_text(rf"\[dev.py] 命令 '{func.__name__}' 被用户中断", "yellow")
            )
            sys.exit(1)

        end_time = get_time_ns()
        show_time_spent(start_time, end_time, func.__name__)
        return result

    return command_func


@command
def format(): # pylint: disable=redefined-builtin
    """格式化代码"""
    _, venv_py = prep_all()
    rich.print(mark_text(r"\[dev.py] 格式化代码中", "green"))
    try:
        cmd_run([venv_py, "-m", "black", "server", "client", "dev.py"])
    except subprocess.CalledProcessError:
        rich.print(mark_text(r"\[dev.py] 代码格式化失败，请检查错误信息", "red"))
        sys.exit(1)
    rich.print(mark_text(r"\[dev.py] 代码已格式化", "green"))


@command
def stubs():
    """静态类型检查"""
    _, venv_py = prep_all()
    rich.print(mark_text(r"\[dev.py] 进行静态类型检查中", "green"))
    try:
        cmd_run([venv_py, "-m", "mypy"])
    except subprocess.CalledProcessError:
        rich.print(mark_text(r"\[dev.py] 静态类型检查失败，请检查错误信息", "red"))
        sys.exit(1)
    rich.print(mark_text(r"\[dev.py] 静态类型检查完成", "green"))


@command
def lint():
    """代码质量检查"""
    _, venv_py = prep_all()
    rich.print(mark_text(r"\[dev.py] 进行代码质量检查中", "green"))
    try:
        cmd_run(
            [
                venv_py,
                "-m",
                "pylint",
                "server",
                "client",
                "dev.py",
                "--output-format=colorized",
            ]
        )
    except subprocess.CalledProcessError:
        rich.print(mark_text(r"\[dev.py] 代码质量检查失败，请检查错误信息", "red"))
        sys.exit(1)
    rich.print(mark_text(r"\[dev.py] 代码质量检查完成", "green"))


if __name__ == "__main__":
    app()
