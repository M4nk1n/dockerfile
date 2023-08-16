FROM nginx

WORKDIR /app

RUN apt update \
  && apt install -y git \
  && git clone https://github.com/mayswind/AriaNg-DailyBuild.git /app \
  && cp -R /app/*  /usr/share/nginx/html \
  && apt clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
  # && rm -rf /etc/nginx/conf.d

EXPOSE 80

ENTRYPOINT ["nginx", "-g","daemon off;"]
