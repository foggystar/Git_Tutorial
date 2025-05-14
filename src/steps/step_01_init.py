# src/steps/step_01_init.py

def initialize_git_repository():
    import os
    import subprocess

    # 获取当前工作目录
    workspace_dir = os.path.join(os.getcwd(), 'workspace')

    # 检查工作目录是否存在
    if not os.path.exists(workspace_dir):
        print("工作目录 'workspace' 不存在，请确保在正确的目录下运行此脚本。")
        return

    # 切换到工作目录
    os.chdir(workspace_dir)

    # 初始化 Git 仓库
    try:
        subprocess.run(['git', 'init'], check=True)
        print("成功初始化 Git 仓库！")
    except subprocess.CalledProcessError:
        print("初始化 Git 仓库失败，请检查 Git 是否已安装并在 PATH 中。")

if __name__ == "__main__":
    initialize_git_repository()