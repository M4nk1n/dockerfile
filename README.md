# dockerfile

## GitHub Actions 自动发布

`packages/` 下每个直接子目录是一个镜像项目，以该目录为构建上下文，使用根 Dockerfile。
PR 合并到 `main` 后，`.github/workflows/docker-publish.yml` 选择受影响的项目，通过 `run.sh` 构建并推送双架构镜像。
仅关闭 PR 不发布，直接 push 到 `main` 也不触发此流程。

### 首次配置

在 [仓库 Actions 配置](https://github.com/M4nk1n/dockerfile/settings/secrets/actions) 中设置：

| 类型 | 名称 | 内容 |
| --- | --- | --- |
| Repository variable | `DOCKERHUB_USERNAME` | `cwjii` |
| Repository secret | `DOCKERHUB_TOKEN` | 有目标镜像推送权限的 Docker Hub access token |

确认目标 Docker Hub 仓库已存在或账号有创建权限，且仓库的 GitHub Actions 已启用。
Token 直接录入 GitHub Secrets，不提交到代码中。

### 构建范围与发布标签

- 修改 `packages/frp/**` 只选择 `frp`；修改多个项目则分别构建，嵌套或归档 Dockerfile 不单独发布。
- 通过 GitHub API 分页读取 PR 文件列表，不依赖合并方式，普通合并、Squash 和 Rebase 均使用同一筛选逻辑；文件列表达到 API 的 3000 文件上限时明确失败，避免漏构建。
- 跨项目移动文件检查两个目录；已删除或没有根 Dockerfile 的项目跳过。
- 修改根目录 `run.sh`、`build.sh`、`buildx.sh`、`publish.sh`、`scripts/ci.py`、`.gitmodules` 或发布 workflow 时选择全部项目。
- `aria2-pro` 是 Git 子模块，workflow 递归检出子模块；更新 `packages/aria2-pro` 的提交指针会选择该镜像。子模块远端有新提交但主仓库指针未更新时不会触发。
- 只修改根 README、TASK 等文档时不构建；项目目录内文档改动仍构建该项目，保持筛选规则简单。
- 每个镜像发布 `cwjii/<项目名>:latest` 和一个追溯标签，两者均包含 `linux/amd64`、`linux/arm64`。
- 有 Dockerfile 同级 `version` 文件时直接使用其中的版本，例如 `cwjii/frp:0.71.0`；没有时直接使用实际构建的完整提交号，不加前缀。
- `version` 支持无结尾换行、LF 或 CRLF 结尾，内容必须是一个合法 Docker 标签，不能为空、多行、超过 128 个 ASCII 字符或等于 `latest`；有文件但无效时直接失败，不回退。
- 同一版本再次发布会覆盖同名标签；需要保留不同版本时，应一起更新 `version`。版本文件仅控制镜像标签，不修改 Dockerfile 中的软件版本。

工作流使用 `pull_request_target` 的合并事件，以便来自 fork 的 PR 合并后也能使用发布凭据；只执行已合并的 `main` 代码，不执行 PR head 代码。
任务按 GitHub concurrency 队列串行执行（`queue: max`，最多 100 个等待任务），各项目独立并行，单个失败不取消其他项目。
由于入队顺序不一定等于合并顺序，每次任务开始时读取最新 `main`，随后所有项目固定构建这个提交；筛选范围仍取触发 PR 的改动。
因此排队期间有后续合并时，镜像可能包含后续已合并的改动，提交号标签也以实际构建提交为准。重跑旧任务同样使用当前 `main`。
不要把 checkout 改回旧 PR 的合并提交，否则旧任务可能覆盖较新的 `latest`。

构建失败不继续发布该项目；不同项目不保证全部一起成功。发布后检查远端镜像清单是否包含两种架构。
上游基础镜像或远程下载更新不会主动触发本仓库构建。失败或队列已满的任务可在 Actions 页面重跑。

### 本地调用与自检

需要 Bash、GNU getopt、Git、Python 3 和 Docker；macOS 自带 getopt 不支持脚本所需的长选项，应使用 GNU getopt。
先按下文准备多架构构建器并执行 `docker login`，再调用：

```bash
# 自动读取 packages/frp/version；不存在时使用当前完整提交号。
bash run.sh -d frp -a cwjii --platform linux/amd64,linux/arm64 -b -p

# 显式指定标签；保留原来的单架构入口，省略 --platform 即可。
bash run.sh -d frp -a cwjii -t 0.71.0 -b -p

# 不需要 Docker 或发布凭据的自检：使用临时目录和 Docker 命令替身。
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

`--platform` 必须同时搭配 `-b -p`，不能搭配 `--rm`；多架构路径调用 `buildx.sh --push`，不会再调用 `publish.sh`。
直接调用 `buildx.sh` 的原有用法仍可用，但自动读取版本标签由 `run.sh` 负责。

## 1. 检查 buildx

```bash
docker buildx version
```

## 2. 开启 binfmt_misc 来运行非本地架构的 Docker 镜像

如果您使用的是 Mac 或者 Windows 版本 Docker 桌面版，则可以跳过这个步骤，因为 binfmt_misc 默认开启。

如果使用的是其它平台，可使用 tonistiigi/binfmt 镜像进行安装

```bash
docker run --privileged --rm tonistiigi/binfmt --install all
```

## 3. 将默认 Docker 构建器切换为多架构构建器

```bash
docker buildx create --use --name multi-platform-builder
```

查看新的多架构构建器是否生效，需执行 `docker buildx ls`

```bash
 ➜ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT             STATUS   PLATFORMS
mybuilder *     docker-container                     
  mybuilder0    unix:///var/run/docker.sock inactive 
desktop-linux   docker                               
  desktop-linux desktop-linux               running  linux/arm64, linux/amd64, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/arm/v7, linux/arm/v6
default         docker                               
  default       default                     running  linux/arm64, linux/amd64, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/arm/v7, linux/arm/v6
```

> 清理构建器
> ```bash
> ➜ docker buildx prune
> ➜ docker buildx rm multi-platform-builder
> ```

## 4. 构建多架构镜像

```bash
./buildx.sh -d <dir> -a <account> -t <tag> -p linux/arm64,linux/amd64

# docker buildx build -t <image-name> --platform=linux/arm64,linux/amd64 . --push
# 参数 --push 会自动将镜像推送到 Docker Hub，本地并不会保留该镜像。如果不想推送，则可去掉该参数
```
