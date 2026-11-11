# Tailscale derper

从 [Tailscale 官方源码](https://github.com/tailscale/tailscale/tree/main/cmd/derper) 编译原版 `derper`，不修改客户端校验或协议行为。

## 版本与构建

`version` 同时决定下载的上游 Release 标签和镜像标签，保留官方的 `v`，不再额外添加前缀。
初始版本 `v1.104.6` 来自 2026-11-11 查询的 [官方最新正式版](https://github.com/tailscale/tailscale/releases/tag/v1.104.6)。
构建使用该 Release 的 `go.toolchain.rev` 指定的官方工具链，在构建机原生架构上交叉编译两个目标架构。

## 自动跟随 Release

`.github/workflows/derper-release.yml` 每小时第 17 分钟（UTC）查询官方 `releases/latest`，只跟随最新正式版。
版本未变时不提交；版本变化时只更新 `packages/derper/version`，创建 commit 并推送到 `main`。
这个 push 触发原有 `.github/workflows/docker-publish.yml`，由原任务筛选出 derper、调用 `run.sh` 构建发布双架构镜像并检查远端清单；更新任务不包含 Docker 构建或登录步骤。
提交被拒绝会报告失败，下次检查会重试，不强制推送。
Actions 页面手动运行更新 workflow 只会立即检查版本，无变化不创建空提交；如镜像构建失败，应重跑原发布 workflow 的失败任务。

更新任务需要新增 Repository secret **`CONTENTS_UPDATE_TOKEN`**：创建 fine-grained PAT，仅授权本仓库，Repository permissions 设置 `Contents: Read and write`，将 Token 保存到仓库 Actions Secrets，勿提交到代码。
该 PAT 所属账号须有本仓库写权限，分支保护或 ruleset 须允许它向 `main` 推送；如果要求所有修改必须走 PR，此实现不能直接提交更新。Token 到期后需更换 Secret。
不能用默认 `GITHUB_TOKEN` 代替，因为它推送的提交不会触发 push workflow；使用 PAT 推送才能接通原发布流程，详见 [GitHub 官方说明](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)。
两个 workflow 共用 concurrency 队列，启动后读取当前 `main`；更新任务完成后原发布任务继续执行。

检查不是实时通知，GitHub 调度可能延迟；两次检查之间发布多个版本时只构建最新正式版。
定时任务只在默认分支运行，因此默认分支须为 `main`；公开仓库长期无活动时 GitHub 可能暂停定时任务，需在 Actions 页面重新启用。
更换版本会更新 `latest`，不负责服务器自动部署。
