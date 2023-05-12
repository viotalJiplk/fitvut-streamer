FROM nginx:alpine

RUN apk add --update --no-cache bash dos2unix apache2-utils coreutils nano screen
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip --upgrade
ENV PYTHONUNBUFFERED=1
RUN touch /var/log/cron.log

#config nginx

RUN rm /etc/nginx/conf.d/default.conf
ADD default.conf /etc/nginx/conf.d
RUN dos2unix /etc/nginx/conf.d/default.conf
#RUN htpasswd -b -c /etc/nginx/.htpasswd viotal 123

#prepare python app

RUN mkdir /video
WORKDIR /video
COPY src/ /video/
RUN dos2unix /video/*
RUN chmod u=rwx,g=rx,o=r video.py
RUN chmod u=rwx,g=rx,o=r gentargets.py
RUN chmod u=rwx,g=rx,o=r start.sh
RUN mkdir www
COPY index.html /video/www/index.html
RUN chmod u=rw,g=rw,o=rw /video/www/index.html
RUN mkdir www/video
RUN pip3 install requests regex pathlib shutils bs4 urllib3

CMD ["/video/start.sh"]

EXPOSE 80