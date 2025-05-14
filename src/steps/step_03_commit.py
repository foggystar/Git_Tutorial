# src/steps/step_03_commit.py

from rich.console import Console
from rich.panel import Panel

console = Console()

def display_commit_instructions():
    console.print(Panel(
        "现在，我们将学习如何提交更改到 Git 仓库。\n"
        "请确保你已经在 'workspace' 目录下，并且已经添加了文件到暂存区。\n"
        "接下来，请在终端中输入以下命令：\n"
        "git commit -m '你的提交信息'\n"
        "这条命令将会把暂存区的更改提交到本地仓库。\n"
        "请记得用描述性的提交信息来说明你所做的更改。",
        title="步骤: 提交更改 (git commit)",
        subtitle="在 'workspace' 目录操作"
    ))
    console.print("\n完成后，你可以运行 'git log' 查看提交历史，或者继续学习下一节。")