# Git Interactive Tutorial

欢迎来到 Git 交互式教程项目！本项目旨在通过互动的方式帮助用户学习 Git 的基本概念和操作。

## 项目概述

本教程将引导用户通过实际操作来掌握 Git 的使用，包括初始化仓库、基本命令、分支管理、远程操作以及一些进阶技巧。用户将通过运行引导脚本和阅读文档来逐步学习。

## 安装说明

1. 确保你的系统上已安装 Git 和 Python 3.x。
2. Fork本仓库
3. 克隆本仓库到本地：
   ```
   git clone https://github.com/YOUR_USERNAME/git-tutorial-interactive.git
   ```
4. 进入项目目录：
   ```
   cd Git_Tutorial
   ```
5. 安装 uv 工具（如果尚未安装）：
   ```
   curl -fsSL https://fnm.vercel.app/install | bash   # 安装 fnm (可选)
   pip install uv                                     # 使用现有的 pip 安装 uv
   ```
6. 使用 uv 创建虚拟环境并安装依赖：
   ```
   uv venv .venv                                      # 创建虚拟环境
   source .venv/bin/activate                          # Linux/macOS
   .venv\Scripts\activate                             # Windows
   uv pip install -r requirements.txt                 # 安装依赖
   ```

## 使用指南

### 图形界面版本（推荐）

1. 运行GUI版本的交互式教程：
   ```
   python src/gui_tutor.py
   ```
2. 学习流程：
   - **阅读教程**：在顶部区域阅读教程文档，了解Git的基本概念
   - **查看命令指南**：在左下方区域查看当前步骤的具体指导和命令示例
   - **在您自己的终端中执行命令**：打开一个单独的终端窗口，在workspace目录中执行指导中的Git命令
   - **观察仓库状态变化**：在右下方区域实时查看Git仓库的文件结构和状态变化

3. 重要提示：
   - 本GUI应用是一个辅助工具，用于展示教程内容和观察仓库状态
   - 您需要在自己的终端中执行Git命令，而不是在GUI中

### 命令行版本

如果你更喜欢命令行界面，也可以使用传统方式：
1. 从 `docs/00-introduction.md` 开始阅读，了解 Git 的基本概念。
2. 按照文档中的指示，运行引导脚本：
   ```
   python src/tutor.py --step <step_name>
   ```
3. 在 `workspace/` 目录中进行实际的 Git 操作练习。

## 贡献

欢迎任何形式的贡献！请查看 `CONTRIBUTING.md` 文件以获取更多信息。

## 许可证

本项目采用 MIT 许可证，详细信息请查看 `LICENSE` 文件。