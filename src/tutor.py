import argparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from utils import check_git_installed, check_uv_installed, install_uv, install_dependencies_with_uv

console = Console()

def display_welcome():
    console.print(Panel(Text("欢迎来到交互式 Git 教程!", style="bold green"), title="Git Tutorial"))
    console.print("请按照 docs/ 目录下的文档顺序学习。")
    console.print("使用 'python src/tutor.py --step <步骤名>' 来获取提示。")

def check_environment():
    """检查环境并确保所有必要的工具都已安装"""
    if not check_git_installed():
        console.print("[bold red]错误:[/bold red] Git未安装，请先安装Git。")
        return False
    
    if not check_uv_installed():
        console.print("[yellow]提示:[/yellow] 未检测到uv工具，推荐使用uv来管理Python依赖。")
        choice = input("是否安装uv？(y/n): ").strip().lower()
        if choice == 'y':
            if install_uv():
                console.print("[green]成功:[/green] uv已安装。")
            else:
                console.print("[yellow]警告:[/yellow] 无法自动安装uv，将使用传统方式继续。")
    else:
        console.print("[green]检测到uv工具已安装。[/green]")
        # 确认是否需要安装依赖
        choice = input("是否使用uv安装项目依赖？(y/n): ").strip().lower()
        if choice == 'y':
            if install_dependencies_with_uv():
                console.print("[green]成功:[/green] 依赖已安装。")
            else:
                console.print("[yellow]警告:[/yellow] 安装依赖失败，请查看错误信息。")
    
    return True

def handle_step(step_name):
    if step_name == "intro":
        console.print(Panel("这是教程的介绍部分。请阅读 docs/00-introduction.md", title="步骤: 介绍"))
        console.print("接下来，尝试 'python src/tutor.py --step init_repo'")
    elif step_name == "init_repo":
        console.print(Panel(
            "现在，我们将在 'workspace/' 目录下初始化一个新的 Git 仓库。\n"
            "1. 请确保你当前在 `git-tutorial-repository` 的根目录。\n"
            "2. 进入 `workspace` 目录: `cd workspace`\n"
            "3. 执行 Git 命令: `git init`\n"
            "4. 执行后，你可以用 `ls -a` (Linux/macOS) 或 `dir /a` (Windows) 查看是否生成了 `.git` 目录。",
            title="步骤: 初始化仓库 (git init)",
            subtitle="在 'workspace' 目录操作"
        ))
        console.print("\n完成后，你可以尝试 'git status' 查看仓库状态。")
        console.print("然后继续阅读下一节文档，并运行 'python src/tutor.py --step add_files'")
    else:
        console.print(f"[bold red]错误:[/bold red] 未知的步骤 '{step_name}'.")
        display_welcome()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="交互式 Git 教程引导脚本")
    parser.add_argument("--step", help="指定当前的教程步骤名", default="welcome")
    parser.add_argument("--check-env", action="store_true", help="检查环境并安装必要工具")
    args = parser.parse_args()

    if args.check_env:
        check_environment()
    elif args.step == "welcome":
        display_welcome()
    else:
        handle_step(args.step)