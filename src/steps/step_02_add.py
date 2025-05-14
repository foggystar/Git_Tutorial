# src/steps/step_02_add.py

from rich.console import Console
from rich.panel import Panel

console = Console()

def display_add_files_prompt():
    console.print(Panel(
        "现在，我们将学习如何将文件添加到 Git 的暂存区。\n"
        "请确保你在 'workspace/' 目录下，并且有文件可以添加。\n"
        "你可以使用以下命令将文件添加到暂存区：\n"
        "`git add <file_name>`\n"
        "例如：`git add file1.txt`",
        title="步骤: 添加文件到暂存区 (git add)",
        subtitle="在 'workspace' 目录操作"
    ))
    console.print("完成后，你可以运行 `git status` 来查看暂存区的状态。")