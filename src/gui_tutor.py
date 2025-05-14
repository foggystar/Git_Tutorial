#!/usr/bin/env python3
# filepath: /home/foggystar/Projects/Git_Tutorial/src/gui_tutor.py

import os
import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QTextEdit, QTreeView, QTabWidget,
                             QSplitter, QFileSystemModel, QGroupBox, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt, QProcess, QDir, QTimer
from PyQt5.QtGui import QTextCursor, QFont, QColor, QPalette, QIcon
import git
from utils import check_git_installed, check_uv_installed
import markdown
import os.path

class GitRepoViewer(QWidget):
    """显示Git仓库状态的组件 - 仅用于观察，不执行命令"""
    def __init__(self, workspace_path, parent=None):
        super().__init__(parent)
        self.workspace_path = workspace_path
        self.init_ui()
        self.git_repo = None
        self.init_repo()
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_repo_status)
        self.update_timer.start(2000)  # 每2秒更新一次

    def init_ui(self):
        layout = QVBoxLayout()
        
        # 标题和说明
        header = QLabel("Git仓库观察器")
        header_font = QFont()
        header_font.setBold(True)
        header_font.setPointSize(12)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        description = QLabel("此面板实时显示workspace目录的Git状态，请在您自己的终端中执行Git命令")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)
        
        # 仓库路径和刷新按钮
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel(f"仓库路径: {self.workspace_path}"))
        refresh_btn = QPushButton("刷新")
        refresh_btn.clicked.connect(self.update_repo_status)
        path_layout.addWidget(refresh_btn)
        layout.addLayout(path_layout)
        
        # 文件系统树
        file_group = QGroupBox("仓库文件结构")
        file_layout = QVBoxLayout()
        
        self.model = QFileSystemModel()
        self.model.setRootPath(self.workspace_path)
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.workspace_path))
        self.tree.setColumnWidth(0, 250)
        file_layout.addWidget(self.tree)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Git状态区域
        status_group = QGroupBox("Git仓库状态")
        status_layout = QVBoxLayout()
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        
        # 设置等宽字体以便更好地显示状态信息
        font = QFont("Courier New", 10)
        self.status_text.setFont(font)
        
        status_layout.addWidget(self.status_text)
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        self.setLayout(layout)

    def init_repo(self):
        try:
            self.git_repo = git.Repo(self.workspace_path)
            self.update_repo_status()
        except git.exc.InvalidGitRepositoryError:
            self.status_text.setText("当前目录不是Git仓库。运行 git init 来初始化它。")
        except Exception as e:
            self.status_text.setText(f"加载Git仓库时出错: {str(e)}")

    def update_repo_status(self):
        """更新Git仓库状态"""
        try:
            if os.path.exists(os.path.join(self.workspace_path, ".git")):
                # 重新加载仓库以获取最新状态
                try:
                    if self.git_repo is None:
                        self.git_repo = git.Repo(self.workspace_path)
                        
                    # 强制重新加载
                    self.git_repo = git.Repo(self.workspace_path)
                    
                    # 清空状态文本并更新
                    self.status_text.clear()
                    
                    status = []
                    
                    # 检查是否是空仓库（没有提交）
                    try:
                        commits_exist = bool(list(self.git_repo.iter_commits('HEAD', max_count=1)))
                    except (git.exc.GitCommandError, ValueError):
                        commits_exist = False
                        
                    # 获取当前分支
                    try:
                        branch = self.git_repo.active_branch.name
                        status.append(f"当前分支: {branch}")
                    except (TypeError, ValueError):
                        status.append("HEAD处于分离状态或这是一个新仓库")
                    
                    # 获取最后一次提交
                    if commits_exist:
                        try:
                            commits = list(self.git_repo.iter_commits('HEAD', max_count=1))
                            if commits:
                                commit = commits[0]
                                status.append(f"最后提交: {commit.hexsha[:7]} - {commit.message.strip()}")
                        except:
                            status.append("无法获取提交信息")
                    else:
                        status.append("这是一个新的空仓库，尚无提交")
                        status.append("提示：请创建一些文件并执行第一次提交")
                    
                    # 本地更改
                    status.append("\n--- 本地更改 ---")
                    try:
                        changed_files = [item.a_path for item in self.git_repo.index.diff(None)]
                        if changed_files:
                            status.append("修改但未暂存的文件:")
                            for f in changed_files:
                                status.append(f"  - {f}")
                        else:
                            status.append("工作区干净，没有修改")
                    except (git.exc.GitCommandError, ValueError):
                        status.append("无法获取工作区状态")
                    
                    # 暂存区
                    status.append("\n--- 暂存区 ---")
                    if commits_exist:
                        try:
                            staged_files = [item.a_path for item in self.git_repo.index.diff('HEAD')]
                            if staged_files:
                                status.append("已暂存的更改:")
                                for f in staged_files:
                                    status.append(f"  + {f}")
                            else:
                                status.append("暂存区为空")
                        except (git.exc.GitCommandError, ValueError):
                            status.append("无法获取暂存区状态")
                    else:
                        try:
                            # 对于空仓库，检查索引中的文件
                            staged_entries = self.git_repo.index.entries
                            if staged_entries:
                                status.append("已暂存的文件:")
                                for entry in staged_entries:
                                    path = entry[0][0].decode() if isinstance(entry[0][0], bytes) else entry[0][0]
                                    status.append(f"  + {path}")
                            else:
                                status.append("暂存区为空")
                        except:
                            status.append("暂存区为空")
                    
                    # 未跟踪文件
                    status.append("\n--- 未跟踪文件 ---")
                    try:
                        untracked = self.git_repo.untracked_files
                        if untracked:
                            status.append("未跟踪的文件:")
                            for f in untracked:
                                status.append(f"  ? {f}")
                        else:
                            status.append("没有未跟踪的文件")
                    except Exception as e:
                        status.append(f"无法获取未跟踪文件: {str(e)}")
                    
                    self.status_text.setText("\n".join(status))
                    
                except Exception as e:
                    self.status_text.setText(f"更新Git状态时出错: {str(e)}")
                    # 提供更具体的错误信息和解决建议
                    if "Ref 'HEAD' did not resolve to an object" in str(e):
                        self.status_text.append("\n\n这是一个新初始化的空仓库，尚未有任何提交。")
                        self.status_text.append("请创建一些文件，使用git add添加它们，然后执行git commit创建第一个提交。")
            else:
                self.status_text.setText("当前目录不是Git仓库。运行 git init 来初始化它。")
                self.git_repo = None
                
        except Exception as e:
            self.status_text.setText(f"检查Git仓库状态时出错: {str(e)}")
            self.git_repo = None

class CommandGuide(QWidget):
    """命令指南组件 - 显示当前步骤的指导和命令示例"""
    def __init__(self, working_dir, parent=None):
        super().__init__(parent)
        self.working_dir = working_dir
        self.current_step = "intro"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # 标题
        header = QLabel("Git命令指南")
        header_font = QFont()
        header_font.setBold(True)
        header_font.setPointSize(12)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # 步骤导航
        steps_layout = QHBoxLayout()
        steps_label = QLabel("选择教程步骤:")
        steps_layout.addWidget(steps_label)
        
        # 步骤按钮
        self.step_buttons = []
        steps = [
            ("intro", "介绍"),
            ("init_repo", "初始化"),
            ("add_files", "添加文件"),
            ("commit", "提交"),
            ("branch", "分支"),
            ("merge", "合并"),
            ("remote", "远程"),
            ("fetch_pull", "获取/拉取"),
            ("push", "推送")
        ]
        
        for step_id, label in steps:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, s=step_id: self.load_step(s))
            steps_layout.addWidget(btn)
            self.step_buttons.append(btn)
            
        layout.addLayout(steps_layout)
        
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        
        # 创建"步骤指南"标签页
        guide_tab = QWidget()
        guide_layout = QVBoxLayout()
        self.guide_text = QTextEdit()
        self.guide_text.setReadOnly(True)
        guide_layout.addWidget(self.guide_text)
        guide_tab.setLayout(guide_layout)
        
        # 创建"在您的终端中执行"标签页
        cmd_tab = QWidget()
        cmd_layout = QVBoxLayout()
        self.cmd_example = QTextEdit()
        self.cmd_example.setReadOnly(True)
        # 设置等宽字体和背景色，模拟终端
        term_font = QFont("Courier New", 11)
        self.cmd_example.setFont(term_font)
        # 设置暗色背景
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.Text, QColor(220, 220, 220))
        self.cmd_example.setPalette(palette)
        cmd_layout.addWidget(self.cmd_example)
        cmd_tab.setLayout(cmd_layout)
        
        # 添加标签页到标签页控件
        self.tab_widget.addTab(guide_tab, "步骤指南")
        self.tab_widget.addTab(cmd_tab, "在您的终端中执行")
        
        # 将标签页控件添加到主布局
        layout.addWidget(self.tab_widget)
        
        # 提示和帮助区域
        tip_label = QLabel("提示: 在您自己的终端窗口中执行命令，然后观察右侧的Git仓库状态变化")
        tip_label.setWordWrap(True)
        layout.addWidget(tip_label)
        
        self.setLayout(layout)
        
        # 默认加载介绍步骤
        self.load_step("intro")

    def load_step(self, step_id):
        """加载指定步骤的指南和命令"""
        self.current_step = step_id
        
        # 步骤指南和命令定义
        steps_content = {
            "intro": {
                "guide": """
<h2>欢迎使用Git交互式教程!</h2>

<p>本教程将引导您学习Git的基本概念和操作。请按照以下步骤进行：</p>

<ol>
    <li>阅读顶部的教程文档</li>
    <li>按照本区域的指南进行操作</li>
    <li>在您自己的终端窗口中执行命令（而不是在此GUI中）</li>
    <li>观察右侧面板中的Git仓库状态变化</li>
</ol>

<p>准备好开始了吗？请先确保您已经Fork并Clone了本仓库!</p>
                """,
                "commands": """
# 确认Git已正确安装:
git --version

# 查看您当前的目录:
pwd  # Linux/macOS
cd   # Windows

# 请确保您位于Git_Tutorial目录下
# 如果不是，请先切换到该目录:
cd path/to/Git_Tutorial
                """
            },
            "init_repo": {
                "guide": """
<h2>初始化Git仓库</h2>

<p>第一步是在workspace目录中初始化一个Git仓库。这将创建一个.git目录，用于存储仓库的所有版本信息。</p>

<p>请在您的终端中执行右侧所示命令：</p>

<p>执行后，workspace目录将变成一个Git仓库。您可以使用<code>ls -a</code>或<code>dir /a</code>查看是否生成了<code>.git</code>目录。</p>

<p>初始化后，您可以执行<code>git status</code>查看仓库的当前状态，这会显示哪些文件未被跟踪。</p>
                """,
                "commands": """
# 进入workspace目录:
cd workspace

# 初始化Git仓库:
git init

# 查看.git目录是否创建:
ls -a  # Linux/macOS
dir /a # Windows

# 查看仓库状态:
git status
                """
            },
            "add_files": {
                "guide": """
<h2>添加文件到暂存区</h2>

<p>现在，您已经初始化了Git仓库，可以看到workspace目录中有一些文件，但它们尚未被Git跟踪。</p>

<p>要让Git开始跟踪文件，您需要使用<code>git add</code>命令将文件添加到暂存区(staging area)。</p>

<p>暂存区是Git中一个重要的概念，它是提交前的准备区域，您可以决定哪些文件的更改将包含在下一次提交中。</p>

<p>试试下面的命令，然后观察右侧Git状态的变化：</p>
                """,
                "commands": """
# 确保您在workspace目录中:
pwd  # Linux/macOS
cd   # Windows

# 查看当前未跟踪的文件:
git status

# 添加单个文件到暂存区:
git add file1.txt

# 再次查看状态，注意file1.txt现在在"要提交的更改"下:
git status

# 添加所有文件:
git add .

# 再次查看状态:
git status
                """
            },
            "commit": {
                "guide": """
<h2>提交更改</h2>

<p>现在您的文件已经在暂存区了，下一步是创建一个提交(commit)。</p>

<p>提交是Git中的核心概念，它代表了项目在特定时间点的快照。每个提交都有一个唯一的ID，并包含了提交消息，解释了这次更改的内容。</p>

<p>好的提交消息非常重要，它们应该简洁地说明所做的更改，以便日后查看历史记录时能够理解每次更改的原因和内容。</p>

<p>试试下面的命令，然后查看提交历史：</p>
                """,
                "commands": """
# 确保您在workspace目录中且有暂存的更改:
git status

# 创建一个提交:
git commit -m "初始提交：添加基本文件"

# 查看提交历史:
git log

# 查看简洁的提交历史:
git log --oneline
                """
            },
            "branch": {
                "guide": """
<h2>创建和切换分支</h2>

<p>分支(branch)是Git的另一个核心概念，它允许您在不影响主线开发的情况下进行并行开发。</p>

<p>每个Git仓库默认有一个名为"master"或"main"的主分支。创建新分支后，您可以在新分支上进行更改，而不会影响主分支。</p>

<p>分支在团队协作和功能开发中非常有用，它允许不同的团队成员同时处理不同的功能。</p>

<p>试试下面的命令来创建和切换分支：</p>
                """,
                "commands": """
# 查看当前分支:
git branch

# 创建一个新分支:
git branch feature-1

# 切换到新分支:
git checkout feature-1
# 或使用新命令(Git 2.23+):
# git switch feature-1

# 查看当前分支(应该显示在feature-1上):
git branch

# 在新分支上进行一些更改:
echo "这是feature-1分支上的新内容" > feature-file.txt
git add feature-file.txt
git commit -m "在feature-1分支添加新文件"

# 切回主分支:
git checkout main  # 或 master，取决于您的默认分支名
                """
            },
            "merge": {
                "guide": """
<h2>合并分支</h2>

<p>当您在一个分支上完成了开发工作，您可能想要将这些更改合并回主分支。这通过<code>git merge</code>命令完成。</p>

<p>合并可能很简单(fast-forward)，也可能需要解决冲突(如果两个分支修改了同一文件的同一部分)。</p>

<p>以下命令将演示如何将您的功能分支合并回主分支：</p>
                """,
                "commands": """
# 确保您在主分支上:
git checkout main  # 或 master

# 查看所有分支:
git branch

# 合并feature-1分支到当前分支:
git merge feature-1

# 查看提交历史，注意合并提交:
git log --oneline --graph

# 如果完成了功能开发，您可以删除feature-1分支:
git branch -d feature-1

# 再次查看分支列表:
git branch
                """
            },
            "remote": {
                "guide": """
<h2>添加远程仓库</h2>

<p>远程仓库(remote repository)允许您与他人协作。GitHub、GitLab和Bitbucket等平台提供了托管远程Git仓库的服务。</p>

<p>添加远程仓库是将本地仓库与远程仓库关联的过程。通常，我们使用"origin"作为主要远程仓库的名称。</p>

<p>本节将指导您如何添加、查看和管理远程仓库。完成这些步骤后，您的本地仓库将与远程仓库建立连接。</p>
                """,
                "commands": """
# 查看当前配置的远程仓库(如果有):
git remote -v

# 添加远程仓库(用您自己的GitHub/GitLab仓库URL替换下面的URL):
git remote add origin https://github.com/用户名/仓库名.git

# 如果您没有远程仓库，可在GitHub/GitLab上创建一个新仓库后再执行上面的命令

# 查看添加后的远程仓库:
git remote -v

# 查看远程仓库的详细信息:
git remote show origin
                """
            },
            "fetch_pull": {
                "guide": """
<h2>获取和拉取远程更改</h2>

<p>与远程仓库协作时，您需要获取其他人的更改。Git提供了两个主要命令：<code>fetch</code>和<code>pull</code>。</p>

<p><strong>git fetch</strong> - 从远程仓库下载内容，但不合并到当前分支。这允许您查看远程的更改而不修改本地工作区。</p>

<p><strong>git pull</strong> - 下载并合并远程更改到当前分支。它相当于<code>git fetch</code>后跟<code>git merge</code>。</p>

<p>这些命令对于团队协作和保持项目同步至关重要。</p>
                """,
                "commands": """
# 确保您已添加远程仓库

# 获取远程仓库的所有信息，但不合并:
git fetch origin

# 查看远程分支:
git branch -r

# 查看所有分支(本地和远程):
git branch -a

# 拉取远程更改并合并到当前分支:
git pull origin main

# 如果您只想要获取某个特定分支的更新:
git fetch origin 分支名

# 查看远程分支与本地分支的差异:
git log HEAD..origin/main --oneline
                """
            },
            "push": {
                "guide": """
<h2>推送更改到远程仓库</h2>

<p>完成本地更改后，您可以使用<code>git push</code>将这些更改推送到远程仓库，与团队成员共享您的工作。</p>

<p>推送前，最好先拉取最新的远程更改，以避免可能的冲突。</p>

<p>首次推送到新创建的远程分支时，您需要设置上游(upstream)关联，这样以后可以简化命令。</p>

<p>以下步骤将指导您如何安全地推送更改到远程仓库。</p>
                """,
                "commands": """
# 确保您有要推送的更改(创建新文件或修改现有文件)
echo "这是要推送到远程的新内容" > push_demo.txt
git add push_demo.txt
git commit -m "添加要推送的演示文件"

# 推送到远程仓库:
git push origin main

# 首次推送新分支并设置上游关联:
git checkout -b feature-remote
echo "远程分支上的内容" > remote_feature.txt
git add remote_feature.txt
git commit -m "在新分支上添加文件"
git push -u origin feature-remote

# 设置上游关联后，后续可以简化推送命令:
# git push

# 查看推送历史:
git log --oneline
                """
            },
        }
        
        # 更新界面
        if step_id in steps_content:
            content = steps_content[step_id]
            self.guide_text.setHtml(content["guide"])
            self.cmd_example.setText(content["commands"])
        else:
            self.guide_text.setHtml("<p>未找到此步骤的指南内容</p>")
            self.cmd_example.setText("# 未找到此步骤的命令示例")
        
        # 滚动到顶部
        self.guide_text.moveCursor(QTextCursor.Start)
        self.cmd_example.moveCursor(QTextCursor.Start)

class TutorialBrowser(QWidget):
    """教程浏览器组件"""
    def __init__(self, docs_dir, parent=None):
        super().__init__(parent)
        self.docs_dir = docs_dir
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 教程标题
        title = QLabel("Git交互式教程")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 教程导航按钮
        nav_layout = QHBoxLayout()
        self.tutorial_buttons = []
        
        tutorials = [
            ("00-introduction.md", "介绍"),
            ("01-basics.md", "基础"),
            ("02-branching.md", "分支"),
            ("03-remote.md", "远程"),
            ("04-advanced.md", "高级")
        ]
        
        for filename, label in tutorials:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, f=filename: self.load_tutorial(f))
            nav_layout.addWidget(btn)
            self.tutorial_buttons.append(btn)
            
        layout.addLayout(nav_layout)
        
        # 教程内容显示区域
        self.content = QTextEdit()
        self.content.setReadOnly(True)
        layout.addWidget(self.content)
        
        self.setLayout(layout)
        
        # 默认加载第一个教程
        if self.tutorial_buttons:
            self.tutorial_buttons[0].click()
    
    def load_tutorial(self, filename):
        """加载指定的教程文件"""
        try:
            file_path = os.path.join(self.docs_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                # 将Markdown转换为HTML
                html_content = markdown.markdown(content)
                
                # 添加基本样式
                styled_content = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
                        h1 {{ color: #2c3e50; }}
                        h2 {{ color: #3498db; }}
                        code {{ background-color: #f8f8f8; padding: 2px 5px; border-radius: 3px; }}
                        pre {{ background-color: #f8f8f8; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """
                
                self.content.setHtml(styled_content)
            else:
                self.content.setPlainText(f"找不到教程文件: {filename}")
        except Exception as e:
            self.content.setPlainText(f"加载教程时出错: {str(e)}")

class GitTutorialApp(QMainWindow):
    """主应用窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git交互式教程")
        self.resize(1200, 800)
        
        # 确定项目根目录
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.workspace_dir = os.path.join(self.project_root, "workspace")
        self.docs_dir = os.path.join(self.project_root, "docs")
        
        # 检查工作区目录是否存在
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
            
        self.init_ui()
        
    def init_ui(self):
        # 主布局使用QSplitter以允许调整各部分大小
        main_splitter = QSplitter(Qt.Vertical)
        
        # 顶部区域为教程内容
        self.tutorial = TutorialBrowser(self.docs_dir)
        main_splitter.addWidget(self.tutorial)
        
        # 底部区域分为命令指南和Git仓库观察器
        bottom_splitter = QSplitter(Qt.Horizontal)
        
        # 命令指南区域
        self.command_guide = CommandGuide(self.workspace_dir)
        bottom_splitter.addWidget(self.command_guide)
        
        # Git仓库观察器区域
        self.repo_viewer = GitRepoViewer(self.workspace_dir)
        bottom_splitter.addWidget(self.repo_viewer)
        
        main_splitter.addWidget(bottom_splitter)
        
        # 设置初始分割比例
        main_splitter.setSizes([300, 500])
        bottom_splitter.setSizes([500, 500])
        
        self.setCentralWidget(main_splitter)
        
        # 菜单栏
        self.create_menu()
        
        # 状态栏 - 添加提示信息
        self.statusBar().showMessage("Git交互式教程已启动 - 请在您自己的终端中执行命令", 5000)
        
    def create_menu(self):
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        # 检查环境选项
        check_action = file_menu.addAction('检查环境')
        check_action.triggered.connect(self.check_environment)
        
        # 添加重置选项
        reset_action = file_menu.addAction('重置Workspace')
        reset_action.triggered.connect(self.reset_workspace)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction('退出')
        exit_action.triggered.connect(self.close)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        open_terminal_action = help_menu.addAction('如何打开终端')
        open_terminal_action.triggered.connect(self.show_terminal_help)
        
        git_help_action = help_menu.addAction('Git命令参考')
        git_help_action.triggered.connect(self.show_git_help)
        
        remote_reset_help_action = help_menu.addAction('如何重置远程仓库')
        remote_reset_help_action.triggered.connect(self.show_remote_reset_help)
        
        help_menu.addSeparator()
        
        about_action = help_menu.addAction('关于')
        about_action.triggered.connect(self.show_about)
        
    def check_environment(self):
        """检查环境是否正确设置"""
        if not check_git_installed():
            QMessageBox.warning(self, "Git未安装", 
                         "未检测到Git。请先安装Git后再继续。\n\n"
                         "您可以从 https://git-scm.com/downloads 下载Git。")
            return
            
        QMessageBox.information(self, "环境检查", 
                         "Git已正确安装。\n\n"
                         "请确保您已经Fork并Clone了教程仓库，"
                         "并在自己的终端中操作。")
    
    def reset_workspace(self):
        """重置workspace目录"""
        from utils import reset_workspace
        
        # 显示确认对话框
        reply = QMessageBox.question(self, '确认重置', 
                            '这将删除workspace目录中的所有文件和.git目录，并重新初始化一个空的Git仓库。\n\n'
                            '如果您有任何未保存的更改，它们将会丢失。\n\n'
                            '您确定要继续吗？',
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            
        if reply == QMessageBox.Yes:
            # 执行重置
            success = reset_workspace(self.workspace_dir)
            
            if success:
                # 更新仓库观察器
                self.repo_viewer.update_repo_status()
                
                QMessageBox.information(self, "重置完成", 
                                "workspace目录已重置。\n\n"
                                "已创建一个新的空Git仓库，并添加了README.md文件。\n\n"
                                "如果您之前有远程仓库关联，需要重新添加。\n\n"
                                "注意：如果遇到权限问题，请尝试关闭所有可能使用workspace目录的程序，"
                                "然后再试一次。")
            else:
                QMessageBox.warning(self, "重置失败", 
                              "重置workspace目录时出错。\n"
                              "请查看控制台输出了解详细信息。\n\n"
                              "如果问题与权限有关，请尝试手动删除workspace/.git目录。")
    
    def show_terminal_help(self):
        """显示如何打开终端的帮助"""
        QMessageBox.information(self, "如何打开终端", 
                         "要执行Git命令，您需要打开一个终端窗口：\n\n"
                         "- Windows: 按 Win+R，输入 'cmd' 并按回车，或搜索'命令提示符'\n"
                         "- macOS: 按 Cmd+Space，输入 'terminal' 并按回车\n"
                         "- Linux: 通常可以按 Ctrl+Alt+T，或从应用菜单找到'终端'\n\n"
                         "在终端中，导航到您克隆的Git_Tutorial目录，"
                         "然后按照教程的指导执行Git命令。")
    
    def show_git_help(self):
        """显示Git命令参考"""
        QMessageBox.information(self, "Git命令参考", 
                         "基本Git命令：\n\n"
                         "- git init: 初始化仓库\n"
                         "- git status: 查看仓库状态\n"
                         "- git add <文件>: 添加文件到暂存区\n"
                         "- git commit -m \"消息\": 提交更改\n"
                         "- git log: 查看提交历史\n"
                         "- git branch: 查看分支\n"
                         "- git checkout <分支>: 切换分支\n"
                         "- git merge <分支>: 合并分支\n\n"
                         "更多命令请参考: https://git-scm.com/docs")
                         
    def show_remote_reset_help(self):
        """显示如何重置远程仓库的帮助"""
        QMessageBox.information(self, "如何重置远程仓库", 
                         "重置远程仓库关联的步骤：\n\n"
                         "1. 查看当前远程仓库：\n   git remote -v\n\n"
                         "2. 移除现有远程仓库关联：\n   git remote remove origin\n\n"
                         "3. 添加新的远程仓库：\n   git remote add origin <新仓库URL>\n\n"
                         "4. 验证远程仓库已更新：\n   git remote -v\n\n"
                         "注意：如果您想完全重置本地和远程关联，请先使用菜单中的"
                         "\"重置Workspace\"选项，然后再添加新的远程仓库。")
        
    def show_remote_reset_help(self):
        """显示如何重置远程仓库的帮助"""
        QMessageBox.information(self, "如何重置远程仓库", 
                         "要重置远程仓库，您可以按照以下步骤操作：\n\n"
                         "1. 删除远程仓库中的所有分支：\n"
                         "   - git push origin --delete <branch_name>\n\n"
                         "2. 强制推送本地分支覆盖远程仓库：\n"
                         "   - git push origin <branch_name> --force\n\n"
                         "请注意，强制推送可能会导致数据丢失，请谨慎操作。")
        
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于Git交互式教程",
            "Git交互式教程 v1.0\n\n"
            "一个帮助用户学习Git的交互式教程应用。\n"
            "通过阅读指南、在自己的终端中执行命令，\n"
            "并观察GUI中的仓库状态变化来学习Git。\n\n"
            "© 2025 Git教程项目")

def check_dependencies():
    """检查必要的依赖是否安装"""
    try:
        import PyQt5
        import git
        import markdown
        return True
    except ImportError as e:
        print(f"缺少必要的依赖: {str(e)}")
        print("请运行: uv pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    if not check_dependencies():
        sys.exit(1)
    
    # 检查Git是否安装
    if not check_git_installed():
        print("警告: 未检测到Git安装。本教程需要Git才能正常工作。")
        print("请先安装Git: https://git-scm.com/downloads")
    
    app = QApplication(sys.argv)
    window = GitTutorialApp()
    window.show()
    
    # 显示欢迎消息
    welcome_message = """欢迎使用Git交互式教程！

本应用是一个辅助工具，用来指导您学习Git操作。

请注意：
1. 阅读顶部的教程文档
2. 查看左下方的命令指南
3. 在您自己的终端窗口中执行Git命令（不是在此应用中）
4. 观察右下方的Git仓库状态变化

点击"确定"开始学习！"""
    
    QMessageBox.information(window, "欢迎使用Git交互式教程", welcome_message)
    
    sys.exit(app.exec_())
