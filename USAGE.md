# GitHub Star List Manager

这是一个受 [maguowei/starred](https://github.com/maguowei/starred) 启发的项目，用于管理我自己的 GitHub Star 列表。

## 功能

- 使用 GitHub GraphQL API 高效获取 Star 列表。
- 支持按语言（Language）或标签（Topics）分类生成 README.md。
- 本地化运行，支持 `.env` 配置。

## 快速开始

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **配置环境变量**：
   在根目录创建 `.env` 文件并填写：
   ```env
   GITHUB_TOKEN=你的GitHub个人访问令牌
   GITHUB_USERNAME=你的GitHub用户名
   ```

3. **运行脚本**：
   ```bash
   python starlist.py --groupby language --output README.md
   ```

## 如何配置 GitHub Actions 自动更新

1. **推送至 GitHub**：创建一个新仓库（如 `my-stars`）并将所有文件推送。
   - **注意**：由于本地 `.env` 包含敏感信息，它已被记录在 [.gitignore](.gitignore) 中。**你不需要也不应该将 `.env` 文件推送到 GitHub。**

2. **GitHub Actions 自动配置**：
   - 脚本会自动识别 GitHub Actions 环境中的默认变量。
   - 你**不需要**在 GitHub 的 `Secrets` 中手动配置 `GITHUB_TOKEN` 或 `GITHUB_USERNAME`。工作流文件 [.github/workflows/update.yml](.github/workflows/update.yml) 已经通过 `${{ secrets.GITHUB_TOKEN }}` 和 `${{ github.repository_owner }}` 自动处理。

3. **开启写入权限 (唯一需要手动操作的)**：
   - 进入仓库网页端的 `Settings` -> `Actions` -> `General`。
   - 在 **Workflow permissions** 部分，勾选 **Read and write permissions** 并保存。


## 同步到博客 (Yzeph.github.io)

项目已配置支持将 Star 列表同步到您的博客仓库。由于涉及跨仓库操作，您需要：

1. **创建 Personal Access Token (PAT)**：
   - 访问 [GitHub PAT Settings](https://github.com/settings/tokens)。
   - 生成一个新 Token，勾选 `repo` 权限。
2. **在 StarList 仓库添加 Secret**：
   - 进入此 StarList 仓库的 `Settings` -> `Secrets and variables` -> `Actions`。
   - 点击 `New repository secret`。
   - Name 填：`BLOG_SYNC_TOKEN`。
   - Value 填：刚才生成的 PAT。
3. **调整博客存放路径**：
   - 目前工作流默认将文件同步到博客仓库的 `content/stars.md`。
   - 如需更改（例如 Hexo 的 `source/_posts/`），请修改 [.github/workflows/update.yml](.github/workflows/update.yml) 中的 `cp README.md blog-repo/...` 这一行。

2. **配置环境变量**：
   在根目录创建 `.env` 文件并填写（仅限本地运行，Actions 自动配置）：
   ```env
   GITHUB_TOKEN=你的GitHub个人访问令牌
   GITHUB_USERNAME=你的GitHub用户名
   ```

3. **运行脚本**：
   ```bash
   python starlist.py --groupby language --output README.md
   ```

