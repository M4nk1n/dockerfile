# frp

[fatedier/frp: A fast reverse proxy to help you expose a local server behind a NAT or firewall to the internet.](https://github.com/fatedier/frp)

## frps

docker-compose.yaml

```yaml
version: '3'

services:
  frps:
    container_name: frps
    image: cwjii/frp
    restart: always
    ports:
      - 7000:7000
    volumes:
      - ./frps.toml:/config/frps.toml:ro
```

## frpc

docker-compose.yaml

```yaml
version: '3'

services:
  frpc:
    container_name: frpc
    image: cwjii/frp
    restart: always
    ports:
      - 7000:7000
    volumes:
      - ./frpc.toml:/config/frpc.toml:ro
    # override the entrypoint
    entrypoint: ["/frpc","-c","/config/frpc.toml"]
```
