# snell-server

[Snell Protocol · GitBook](https://manual.nssurge.com/others/snell.html)

[Snell Server · GitBook](https://manual.nssurge.com/others/snell-server.html)

```yaml
# version: '3'

services:
  snell:
    container_name: snell
    image: cwjii/snell-server:latest
    restart: always
    ports:
      - "6160:6160"
    environment:
      - TZ=Asia/Hong_Kong
    volumes:
      - ./snell-server.conf:/config/snell-server.conf:ro
```

snell-server.conf

```conf
[snell-server]
listen = 0.0.0.0:6160
psk = RANDOM_KEY_HERE
obfs = off
ipv6 = false
```

obfs:

```conf
obfs = http  # http, tls
obfs-host = www.bing.com
```

If you don't already have a password generator installed,
you can run this command to install `pwgen``, a popular generator:

```bash
pwgen -s 32 1
```
