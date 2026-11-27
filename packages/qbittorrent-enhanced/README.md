# docker-qbittorrentee

https://github.com/c0re100/qBittorrent-Enhanced-Edition

https://github.com/SuperNG6/Docker-qBittorrent-Enhanced-Edition


## linuxserver/docker-qbittorrent

https://github.com/linuxserver/docker-qbittorrent

https://hub.docker.com/r/linuxserver/qbittorrent

https://docs.linuxserver.io/images/docker-qbittorrent/

## 自动更新与基础镜像

GitHub Actions 每小时检查上游最新正式 Release；有新版本且对应 LinuxServer 基础镜像已发布时，更新 `version` 并推送 commit，之后由主仓库发布 workflow 构建镜像。
Enhanced Edition 版本格式为 `主版本.次版本.修订版.增强版号`，例如 `5.2.4.10`；构建时自动将前三段 `5.2.4` 作为 `linuxserver/qbittorrent` 的基础镜像标签，下载增强版二进制时使用完整版本号。
更新任务使用仓库已有的 `CONTENTS_UPDATE_TOKEN` Secret；如果上游 Release 先于 LinuxServer 对应标签发布，workflow 会等待后续定时检查。
