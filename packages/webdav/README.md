# WebDAV Docker

Fork from: [noodlefighter/docker-webdav](https://github.com/noodlefighter/docker-webdav) (ver.340788a)

## 新增一个 HeaderName 配置

> 需要在把 webdav-js 目录复制到 docker-compose 同目录下，然后设置只读（防止被误修改/删除）影射到容器内

```yaml
services:
  webdav:
    ...
    volumes:
      # webdav-js
      - ./webdav-js:/data/webdav-js:ro
```

## Changelog (Supported tags)

- [`2.4.3`, `latest`]
  - `AUTH_TYPE` 参数新增一个 `None` 选项，用于存在前置代理登录授权（如：traefik basicauth）的的情况下，不再设置 webdav 的用户登录授权

- [`2.4.2`]
  - 新增一个 `HeaderName` 配置

- [`2.4.1`]
  - 固定 base image version (2.4.43)
  - 移动数据目录到根目录位置（/data）
  - 修正 PUID & PGID

## Quick reference

自行查看：[noodlefighter/docker-webdav](https://github.com/noodlefighter/docker-webdav)
