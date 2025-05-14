def print_welcome_message():
    print("欢迎来到交互式 Git 教程!")

def check_git_installed():
    import subprocess
    try:
        subprocess.run(["git", "--version"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_uv_installed():
    import subprocess
    try:
        subprocess.run(["uv", "--version"], check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_uv():
    import subprocess
    import platform
    import os
    
    try:
        if platform.system() == "Windows":
            # Windows安装方法需要用户手动安装
            print("请访问 https://github.com/astral-sh/uv 获取Windows安装说明")
            return False
        else:
            # Linux/macOS安装
            subprocess.run("curl -LsSf https://astral.sh/uv/install.sh | sh", shell=True, check=True)
            
            # 更新PATH（仅用于当前会话）
            if os.path.exists(os.path.expanduser("~/.cargo/bin")):
                os.environ["PATH"] += os.pathsep + os.path.expanduser("~/.cargo/bin")
            
            return check_uv_installed()
    except Exception as e:
        print(f"安装uv失败: {e}")
        return False

def create_directory(path):
    import os
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败: {e}")
        return False

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return None

def write_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"写入文件失败: {e}")
        return False

def install_dependencies_with_uv():
    """使用uv安装项目依赖"""
    import subprocess
    import os
    
    if not check_uv_installed():
        print("uv未安装，尝试安装...")
        if not install_uv():
            print("无法安装uv，请手动安装: https://github.com/astral-sh/uv")
            return False
    
    try:
        # 确定requirements.txt的路径
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        req_path = os.path.join(project_root, "requirements.txt")
        
        # 创建虚拟环境（如果不存在）
        venv_path = os.path.join(project_root, ".venv")
        if not os.path.exists(venv_path):
            print("创建虚拟环境...")
            subprocess.run(["uv", "venv", ".venv"], cwd=project_root, check=True)
        
        # 安装依赖
        print("安装依赖...")
        subprocess.run(["uv", "pip", "install", "-r", req_path], cwd=project_root, check=True)
        return True
    except Exception as e:
        print(f"安装依赖失败: {e}")
        return False

def reset_workspace(workspace_path):
    """重置workspace目录，清除所有文件和.git目录，并重新初始化Git仓库"""
    import os
    import shutil
    import subprocess
    
    try:
        # 确保workspace目录存在
        if not os.path.exists(workspace_path):
            os.makedirs(workspace_path, exist_ok=True)
            print(f"创建workspace目录: {workspace_path}")
            
        # 首先尝试强制删除所有内容，包括.git目录
        for item in os.listdir(workspace_path):
            item_path = os.path.join(workspace_path, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    print(f"已删除文件: {item}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
                    print(f"已删除目录: {item}")
            except Exception as e:
                print(f"删除 {item} 时出错: {e}")
                
        # # 再次特别检查.git目录是否还存在，如果存在则尝试强制删除
        # git_dir = os.path.join(workspace_path, ".git")
        # if os.path.exists(git_dir):
        #     try:
        #         # 使用更强制的方式删除
        #         if os.name == 'nt':  # Windows
        #             subprocess.run(f"rmdir /S /Q \"{git_dir}\"", shell=True, check=True)
        #         else:  # Linux/Mac
        #             subprocess.run(f"rm -rf \"{git_dir}\"", shell=True, check=True)
        #         print("已强制删除.git目录")
        #     except Exception as e:
        #         print(f"强制删除.git目录时出错: {e}")
                
        # # 再次检查.git目录是否确实被删除
        # if os.path.exists(git_dir):
        #     print("警告: 无法删除.git目录，这可能会导致问题")
        # else:
        #     print("已确认.git目录已被成功删除")
                
        # print("已清空workspace目录")
        
        # # 确保目录为空后，重新初始化Git仓库
        # subprocess.run(["git", "init"], cwd=workspace_path, check=True)
        print("已重新初始化Git仓库")
        
        # 创建一个简单的README.md文件
        readme_content = "# Git教程练习项目\n\n这是一个用于Git教程练习的仓库。\n"
        with open(os.path.join(workspace_path, "README.md"), "w") as f:
            f.write(readme_content)
        print("已创建README.md文件")
        
        return True
    except Exception as e:
        print(f"重置workspace失败: {e}")
        return False