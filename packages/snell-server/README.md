# snell-server

[Snell Protocol · GitBook](https://manual.nssurge.com/others/snell.html)

[Snell Server · GitBook](https://manual.nssurge.com/others/snell-server.html)

```yaml
# version: '3'

services:
  snell:
    container_name: snell
    image: cwjii/snell-server:latest
    restart: unless-stopped
    # ports:
    #   - [HOST:]CONTAINER[/PROTOCOL]
    environment:
      TZ: Asia/Hong_Kong
      PORT: 9102
      PSK: password # Change here
```

---

## snell-server.conf

可以通过 `snell-server` 生成一个配置，或者自己写

```bash
docker exec -it snell-server /usr/bin/snell-server --wizard -c /config/snell-temp.conf
```

```conf
[snell-server]
listen = 0.0.0.0:PORT_HERE
psk = RANDOM_KEY_HERE
ipv6 = false
```

obfs:

```conf
obfs = http  # off, http, tls
obfs-host = www.bing.com
```

If you don't already have a password generator installed,
you can run this command to install `pwgen``, a popular generator:

```bash
pwgen -s 32 1
```
