# 这是 Git 分支管理的教程文档

## Git 分支管理

Git 分支是 Git 中一个非常强大的功能，它允许你在同一个代码库中并行开发不同的功能或修复不同的 bug。通过使用分支，你可以在不影响主代码库的情况下进行实验和开发。

### 1. 什么是分支？

分支是指在 Git 中创建的一个独立的开发线。每个分支都有自己的提交历史，可以在分支上进行修改，而不会影响其他分支。

### 2. 创建分支

要创建一个新的分支，可以使用以下命令：

```bash
git branch <branch-name>
```

例如，要创建一个名为 `feature-xyz` 的新分支，可以运行：

```bash
git branch feature-xyz
```

### 3. 切换分支

创建分支后，你可以使用以下命令切换到该分支：

```bash
git checkout <branch-name>
```

例如，切换到 `feature-xyz` 分支：

```bash
git checkout feature-xyz
```

从 Git 2.23 开始，你也可以使用 `git switch` 命令来切换分支：

```bash
git switch feature-xyz
```

### 4. 合并分支

当你完成了在某个分支上的开发后，可以将其合并到主分支（通常是 `main` 或 `master`）中。首先，切换到主分支：

```bash
git checkout main
```

然后，使用以下命令合并分支：

```bash
git merge <branch-name>
```

例如，合并 `feature-xyz` 分支：

```bash
git merge feature-xyz
```

### 5. 删除分支

如果你不再需要某个分支，可以将其删除。使用以下命令删除分支：

```bash
git branch -d <branch-name>
```

例如，删除 `feature-xyz` 分支：

```bash
git branch -d feature-xyz
```

### 6. 解决合并冲突

在合并分支时，可能会遇到合并冲突。这通常发生在两个分支对同一文件的同一部分进行了不同的修改。Git 会提示你解决冲突。你需要手动编辑冲突的文件，解决冲突后，使用以下命令标记为已解决：

```bash
git add <file>
```

然后，继续合并：

```bash
git commit
```

### 7. 小结

分支是 Git 的核心功能之一，能够帮助你在开发过程中保持代码的整洁和组织。通过合理使用分支，你可以更高效地管理项目的不同功能和版本。