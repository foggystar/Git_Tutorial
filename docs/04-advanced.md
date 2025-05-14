# 04-advanced.md

# Git 进阶操作与技巧

在本章中，我们将探讨一些 Git 的进阶操作和技巧，以帮助你更高效地使用 Git 进行版本控制。

## 1. Git Rebase

`git rebase` 是一个强大的命令，用于将一个分支的更改应用到另一个分支上。与 `git merge` 不同，`rebase` 会将提交历史重写为线性，这使得项目历史更加整洁。

### 使用示例

```bash
# 切换到要进行 rebase 的分支
git checkout feature-branch

# 将主分支的更改应用到当前分支
git rebase main
```

## 2. Git Stash

`git stash` 允许你暂时保存未提交的更改，以便你可以在干净的工作区中切换分支或进行其他操作。

### 使用示例

```bash
# 保存当前更改
git stash

# 查看存储的更改
git stash list

# 恢复最近的存储
git stash apply
```

## 3. 解决合并冲突

在合并分支时，可能会遇到合并冲突。Git 会标记冲突的文件，你需要手动解决这些冲突。

### 解决步骤

1. 查看冲突文件：
   ```bash
   git status
   ```

2. 打开冲突文件，查找 `<<<<<<<`, `=======`, `>>>>>>>` 标记，手动编辑以解决冲突。

3. 添加解决后的文件：
   ```bash
   git add <conflicted-file>
   ```

4. 完成合并：
   ```bash
   git commit
   ```

## 4. .gitignore 文件

在项目中，某些文件或目录不应被 Git 跟踪。你可以通过 `.gitignore` 文件来指定这些文件。

### 示例 .gitignore 内容

```
# Python 缓存文件
__pycache__/
*.pyc

# 虚拟环境
venv/
.env
```

## 5. Git 标签

标签用于标记特定的提交，通常用于发布版本。

### 创建标签

```bash
# 创建轻量标签
git tag v1.0

# 创建附注标签
git tag -a v1.0 -m "版本 1.0 发布"
```

### 查看标签

```bash
git tag
```

## 6. 进阶命令

- `git cherry-pick <commit>`: 将特定提交应用到当前分支。
- `git reflog`: 查看所有的引用日志，帮助你找回丢失的提交。

## 总结

掌握这些进阶操作和技巧将使你在使用 Git 时更加得心应手。继续实践并探索更多 Git 的功能，以提升你的版本控制能力。