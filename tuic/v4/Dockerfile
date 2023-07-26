FROM alpine:latest

LABEL com.centurylinklabs.watchtower.enable="false"

ARG VERSION=0.8.5
ARG SYSTEM=linux-musl

WORKDIR /etc/tuic

# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
# && apk --no-cache add curl \
# && curl -L https://github.com/EAimTY/tuic/releases/download/${VERSION}/tuic-server-${VERSION}-$(uname -m) -o /usr/bin/tuic-server \
# && chmod +x /usr/bin/tuic-server

RUN apk --no-cache add curl \
&& curl -L https://github.com/EAimTY/tuic/releases/download/${VERSION}/tuic-server-${VERSION}-$(uname -m)-${SYSTEM} -o /usr/bin/tuic-server \
&& chmod +x /usr/bin/tuic-server

COPY config.json /etc/tuic/

EXPOSE 443/udp

ENTRYPOINT ["tuic-server"]
CMD ["-c", "/etc/tuic/config.json"]
