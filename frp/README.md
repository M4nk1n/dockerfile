# frp_server

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
      - 6400:6400
    volumes:
      - ./frps.ini:/config/frps.ini:ro
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
      - 6400:6400
    volumes:
      - ./frpc.ini:/config/frpc.ini:ro
    # override the entrypoint
    entrypoint: ["/frpc","-c","/config/frpc.ini"]
```
