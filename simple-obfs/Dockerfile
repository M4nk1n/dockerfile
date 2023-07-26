#
# Dockerfile for simple-obfs
#

FROM alpine:latest

ENV SERVER_ADDR 0.0.0.0
ENV SERVER_PORT 8139
ENV OBFS_OPTS http
ENV DNS_SERVER 8.8.8.8,1.1.1.1
ENV FORWARD 127.0.0.1:8388
ENV FAILOVER 127.0.0.1:80
ENV ARGS=

LABEL com.centurylinklabs.watchtower.enable="false"

WORKDIR /app

RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
        git \
        gcc autoconf make libtool automake zlib-dev openssl asciidoc xmlto libpcre32 libev-dev g++ linux-headers \
    && git clone https://github.com/shadowsocks/simple-obfs.git \
    && cd simple-obfs \
    && git submodule update --init --recursive \
    && ./autogen.sh \
    && ./configure --prefix=/usr --disable-documentation\
    && make \
    && make install \
    && apk add --no-cache --virtual .run-deps \
        rng-tools \
        $(scanelf --needed --nobanner /usr/bin/obfs-* \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | xargs -r apk info --installed \
        | sort -u) \
    && apk del .build-deps \
    && rm -rf simple-obfs


EXPOSE $SERVER_PORT

CMD exec obfs-server \
    -a nobody \
    --fast-open \
    -s $SERVER_ADDR \
    -p $SERVER_PORT \
    -r $FORWARD \
    --obfs $OBFS_OPTS \
    -d $DNS_SERVER \
    --failover $FAILOVER \
    $ARGS
