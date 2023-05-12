#!/bin/bash

if [ -z ${XLOGIN+x} ];
then
    echo "ERROR: xlogin is unset"
    exit 1;
fi
if [ -z ${PASSWD+x} ];
then
    echo "ERROR: passwd is unset"
    exit 1;
fi
if [ -z ${TODWN+x} ];
then
    echo "ERROR: toDwn is unset"
    exit 1;
fi
if [ -z ${SCHEDULE+x} ];
then
    echo "ERROR: SCHEDULE is unset"
    exit 1;
fi

if [ -z ${USERS+x} ];
then
    echo "ERROR: USERS is unset"
    exit 1;
fi

if [ -z ${TARGETS+x} ];
then
    echo "ERROR: TARGETS is unset"
    exit 1;
fi

./gentargets.py $TARGETS

IFS=':'
read -ra USERSARRAY <<< $USERS

if [ ${USERSARRAY[0]+x} ]
then
    IFS=' '
    read -ra COMMANDARRAY <<< ${USERSARRAY[0]}
    htpasswd -c -b /etc/nginx/.htpasswd ${COMMANDARRAY[0]} ${COMMANDARRAY[1]}
fi

for u in ${!USERSARRAY[@]}; do
  if [[ $u -ne "0" ]]
  then
    IFS=' '
    read -ra COMMANDARRAY <<< ${USERSARRAY[u]}
    htpasswd -b /etc/nginx/.htpasswd ${COMMANDARRAY[0]} ${COMMANDARRAY[1]}
  fi
done

nohup nginx
echo "nginx has started"
echo " ${SCHEDULE//"\*"/'*'} python3 /video/video.py >> /video/log.log" > /video/crontab
./gentargets
crontab /video/crontab
echo "cron has been set"
screen -dm -S firstDownload "/video/video.py"
echo "started first download"
crond -f