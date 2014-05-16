#!/bin/bash

# prevent multiple calls
if [ "x$BASE_SH_VISITED" == x ]; then

export BASE_SH_VISITED=true


#
# ** create the per-user dynamic environment **
#

### initialize for our container owner ###

# DOCKERENV_HOST: hostname we are invoked from
# DOCKERENV_USER: user we're setting this host up for
# DOCKERENV_AUTHKEYS: user's ssh keys

if [ x"$DOCKERENV_USER" == x ]; then
  echo ERROR: must specify user to own the Docker environment
  exit 1
fi

if [ x"$DOCKERENV_AUTHKEYS" == x ]; then
  echo ERROR: must have ssh keys in your environment
  echo Check ssh-add -L to verify that you have inherited keys for $DOCKERENV_USER
  exit 1
fi

# chromote wants a user to operate on behalf of
export DOCKERENV_HOME=/home/$DOCKERENV_USER
useradd -m -d $DOCKERENV_HOME -g users -G androiddev,sudo $DOCKERENV_USER


echo set up user ssh environment
# set up that user's ssh environment; create a new user using the existing
# user and their currently authorized keys
mkdir $DOCKERENV_HOME/.ssh
echo "$DOCKERENV_AUTHKEYS" >$DOCKERENV_HOME/.ssh/authorized_keys
echo "Authorizing keys: $DOCKERENV_AUTHKEYS"
chmod -R go-rx $DOCKERENV_HOME/.ssh
chown -R $DOCKERENV_USER:users $DOCKERENV_HOME/.ssh

echo add sudoer and shell
# for debugging, since we don't have a password and containers are open
SUDOFILE=/etc/sudoers.d/$DOCKERENV_USER
echo "$DOCKERENV_USER   ALL=(ALL:ALL) NOPASSWD: ALL" >$SUDOFILE
chmod 0440 $SUDOFILE
chsh -s /bin/bash $DOCKERENV_USER


# https://github.com/dotcloud/docker/issues/5126 for Docker 0.10.0
chmod 1777 /dev/shm


fi ### END BASE_SH_VISITED