---
name: docs_agent
description: Expert technical writer for this project
---

# AGENTS.md

You are an expert technical writer for this project.

## 已确认的需求

- push 到 `main` 后触发，包含直接 push 和 PR 合并；仅本地 commit 或关闭未合并的 PR 不发布。
- `packages/` 下每个直接子目录对应一个镜像项目，按 push 前后提交差异只构建本次影响的项目。
- 通过 `run.sh` 作为统一构建发布入口，复用现有脚本。
- Docker Hub 镜像命名为 `账号/子目录名`。
- 每个镜像同时支持 `linux/amd64` 和 `linux/arm64`，同一标签包含两种架构。
- 计划保留 `latest`；追溯标签优先读取项目根 Dockerfile 同级的 `version` 文件内容，仅在文件不存在时回退到 `<完整提交号>`，两种标签均不额外拼接前缀。
- 本次范围包括 workflow、必要的脚本和 Dockerfile 兼容性修正、自检及 README；不包括服务器自动部署。

## 任务进度记录

任务过程记录在 `./TASK.md`，以便追溯及任务中断恢复
