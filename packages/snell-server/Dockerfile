FROM cyphernode/alpine-glibc-base:v3.12.4_2.31-0

ENV VERSION=v4.1.0rc1
ENV TZ=Asia/Shanghai

WORKDIR /tmp

RUN apk add --update libstdc++ && rm -rf /var/cache/apk/* && \
    ARCH=$(arch | sed s/x86_64/amd64/) && \
    wget -q -O "snell-server.zip" https://dl.nssurge.com/snell/snell-server-${VERSION}-linux-${ARCH}.zip && \
    unzip snell-server.zip && rm snell-server.zip && \
    mv snell-server /usr/bin/

COPY start.sh /start.sh
RUN chmod +x /start.sh

# ENTRYPOINT ["/usr/bin/snell-server","-c","/config/snell-server.conf"]
ENTRYPOINT ["/start.sh"]
CMD ["/start.sh"]
