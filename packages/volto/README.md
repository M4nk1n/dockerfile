# volto

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
```
