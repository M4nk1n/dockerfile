# dockerfile

## 1. 检查 buildx

```bash
docker buildx version
```

## 2. 开启 binfmt_misc 来运行非本地架构的 Docker 镜像

如果您使用的是 Mac 或者 Windows 版本 Docker 桌面版，则可以跳过这个步骤，因为 binfmt_misc 默认开启。

如果使用的是其它平台，可使用 tonistiigi/binfmt 镜像进行安装

```bash
docker run --privileged --rm tonistiigi/binfmt --install all
```

## 3. 将默认 Docker 构建器切换为多架构构建器

```bash
docker buildx create --use --name multi-platform-builder
```

查看新的多架构构建器是否生效，需执行 `docker buildx ls`

```bash
 ➜ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT             STATUS   PLATFORMS
mybuilder *     docker-container                     
  mybuilder0    unix:///var/run/docker.sock inactive 
desktop-linux   docker                               
  desktop-linux desktop-linux               running  linux/arm64, linux/amd64, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/arm/v7, linux/arm/v6
default         docker                               
  default       default                     running  linux/arm64, linux/amd64, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/arm/v7, linux/arm/v6
```

> 清理构建器
> ```bash
> ➜ docker buildx prune
> ➜ docker buildx rm multi-platform-builder
> ```

## 4. 构建多架构镜像

```bash
./buildx.sh -d <dir> -a <account> -t <tag> -p linux/arm64,linux/amd64

# docker buildx build -t <image-name> --platform=linux/arm64,linux/amd64 . --push
# 参数 --push 会自动将镜像推送到 Docker Hub，本地并不会保留该镜像。如果不想推送，则可去掉该参数
```
