FROM alpine:latest

ARG PUID=${PUID:-1000}
ARG PGID=${PGID:-1000}

RUN apk update && apk add --no-cache nginx nginx-mod-http-dav-ext nginx-mod-http-fancyindex nginx-mod-http-headers-more apache2-utils
RUN apk --no-cache add shadow && usermod -u $PUID nginx && groupmod -g $PGID nginx
RUN rm -rf /var/cache/apk/* && rm -rf /tmp/*

COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY conf/webdav.conf /etc/nginx/http.d/default.conf
COPY webdav-js/ /webdav-js/

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

CMD /entrypoint.sh && /usr/sbin/nginx -g "daemon off;"

VOLUME /data

EXPOSE 80
