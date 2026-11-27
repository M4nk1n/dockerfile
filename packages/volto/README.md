# volto

[vcarus/volto](https://github.com/vcarus/volto)

GitHub Actions 每小时检查上游最新正式 Release；发现新版本后会更新本目录的 `version` 文件并提交到主仓库，随后由主仓库现有发布 workflow 构建并推送镜像。

MASQUE proxy server (HTTP/3 CONNECT + CONNECT-UDP) in Rust, built to interoperate with Surge

```yaml
services:
  volto:
    container_name: volto
    image: cwjii/volto
    restart: unless-stopped
    ports:
      - 443:443/udp
    volumes:
      - ./config.toml:/etc/volto/config.toml:ro
      - ./certs:/etc/volto/cert:ro
```
