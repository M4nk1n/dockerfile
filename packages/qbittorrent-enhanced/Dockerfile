FROM linuxserver/qbittorrent:latest

ARG ARCH
ARG QB_VERSION=5.1.3.10

# 根据架构下载和替换 qbittorrent-nox
RUN cd /tmp && echo ${QB_VERSION} \
    && ARCH=$(arch | sed s/arm64/aarch64/ | sed s/amd64/x86_64/) \
    && curl -L https://github.com/c0re100/qBittorrent-Enhanced-Edition/releases/download/release-${QB_VERSION}/qbittorrent-enhanced-nox_${ARCH}-linux-musl_static.zip -o qbittorrent.zip \
    # && echo -e "WebUI\\CSRFProtection=false\nWebUI\\ClickjackingProtection=false\nWebUI\\HostHeaderValidation=false" > /defaults/qBittorrent.conf \
    && rm /usr/bin/qbittorrent-nox \
    && 7z x qbittorrent.zip -o/usr/bin \
    && chmod +x /usr/bin/qbittorrent-nox \
    && rm qbittorrent.zip
