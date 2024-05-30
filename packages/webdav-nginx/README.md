# WebDAV Docker

## Changelog (Supported tags)

- [`1.0`, `latest`]
  - new project.

## Quick reference

### docker compose

```yaml
services:
  webdav:
    container_name: webdav
    image: cwjii/webdav-nginx:latest
    restart: always
    environment:
      TZ: Asia/Hong_Kong
      PUID: 1000
      PGID: 1000
    ports:
      - 80:80
    volumes:
      - ./data:/data
```

#### Single user

Specifying `USERNAME` and `PASSWORD` only supports a single user. 

```yaml
services:
  webdav:
    ...
    environment:
      ...
      USERNAME: guest
      PASSWORD: test
```

#### Multiple user

If you want to have lots of different logins for various users,
bind mount your own file to `/etc/nginx/htpasswd` and the container will use that instead.

run the following commands:

```bash
touch user.passwd
htpasswd -B user.passwd alice
htpasswd -B user.passwd bob
```

Once you've created your own `user.passwd`, bind mount it into your container:

```yaml
services:
  webdav:
    ...
    volumes:
      ...
      # bind mount `htpasswd` into your container
      - ./user.passwd:/etc/nginx/htpasswd
```

### Work with traefik

```yaml
services:
  webdav:
    ...
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.webdav.rule=Host(`webdav.domain.com`)"
      - "traefik.http.routers.webdav.entrypoints=foo"
      - "traefik.http.routers.webdav.service=webdav"
      - "traefik.http.services.webdav.loadbalancer.server.port=80"
      - "traefik.http.services.webdav.loadbalancer.server.scheme=http"

      # use webdav basicauth
      # - "traefik.http.routers.webdav.middlewares=webdav-auth"
      # - "traefik.http.middlewares.webdav-auth.basicauth.users=guest:$$apr1$$wJ.CCIEe$$gdNQGpB3a4k.m7r06HtO31"
```

## 参考资料

[dom111/webdav-js](https://github.com/dom111/webdav-js/tree/master/docker/nginx)
[docker-projects/docker-webdav-alpine](https://github.com/docker-projects/docker-webdav-alpine)
[uGeek/docker-webdav](https://github.com/uGeek/docker-webdav)
