FROM debian:stable-slim

ENV VERSION=v5.0.0b1
ENV TZ=Asia/Shanghai

RUN apt-get update && \
    apt-get install -y --no-install-recommends wget unzip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app/

RUN wget --no-check-certificate -O snell.zip https://dl.nssurge.com/snell/snell-server-${VERSION}-linux-$(arch | sed s/x86_64/amd64/).zip

COPY entrypoint.sh /app/

RUN if [ -f snell.zip ]; then unzip snell.zip && rm -f snell.zip; fi && \
    chmod +x snell-server && \
    chmod +x entrypoint.sh

# ENTRYPOINT ["/app/snell-server","-c","/config/snell-server.conf"]
ENTRYPOINT ["/app/entrypoint.sh"]
# CMD ["/app/entrypoint.sh"]
