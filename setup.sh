#!/bin/bash

# pass in user as environement variable on first run; creates empty passwd
# entry; open up shadow file so that unix_chkpwd can read it (setgid
# doesn't work)... this is needed for chrome remote desktop to work

dq='"'

DOCKERENV_USER=$USER
DOCKERENV_HOST="$(hostname)"
DOCKERENV_HOSTIP="$(grep $DOCKERENV_HOST /etc/hosts | awk '{ print $1 }')"
DOCKERENV_AUTHKEYS=$(ssh-add -L)

# build a container and specialize it to this user
docker build --rm=true -t dougbo/docker-desktop .
if [ $? != 0 ]; then
  echo ERROR: docker build failed
  exit 1
fi

# add -t to address https://github.com/dotcloud/docker/issues/4605
CONTAINER_ID=$(docker run -t \
    -e DOCKERENV_HOST="$DOCKERENV_HOST" \
    -e DOCKERENV_HOSTIP="$DOCKERENV_HOSTIP" \
    -e DOCKERENV_USER="$DOCKERENV_USER" \
    -e DOCKERENV_AUTHKEYS="$DOCKERENV_AUTHKEYS" \
    -d -P dougbo/docker-desktop)
if [ $? != 0 ]; then
  echo ERROR: docker run failed
  exit 1
fi
echo $CONTAINER_ID


read -p "Name this session: " name

# ssh into the container and start X+chromote+studio; chromote will prompt for auth code

# try ssh'ing to make sure the service has started
for i in 1 2 3 4 5; do
  ssh=$(./GETSSH.sh $CONTAINER_ID)
  if $ssh echo >/dev/null 2>&1; then break; fi
  if [ $i == 5 ]; then 
    echo ERROR: ssh service failed to start
    exit 1
  fi
  sleep `expr 2 '*' $i`
done

echo Starting chrome remote desktop

$ssh ". .profile; /opt/google/chrome-remote-desktop/start-host --redirect-url=https://chromoting-auth.googleplex.com/auth --name=${dq}$name${dq}"
