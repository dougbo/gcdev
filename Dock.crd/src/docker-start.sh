#!/bin/bash


### initialize for our container owner ###

# DOCKERENV_HOST: hostname we are invoked from
# DOCKERENV_USER: user we're setting this host up for
# DOCKERENV_AUTHKEYS: user's ssh keys

if [ x"$DOCKERENV_AUTHKEYS" == x ]; then
  echo ERROR: must have ssh keys in your environment
  echo Check ssh-add -L to verify that you have inherited keys for $DOCKERENV_USER
fi

# chromote wants a user to operate on behalf of
DOCKERENV_HOME=/home/$DOCKERENV_USER
useradd -m -d $DOCKERENV_HOME -g users $DOCKERENV_USER
adduser $DOCKERENV_USER sudo

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

# get this user GIT enhancement for sublime
SUBLIME_CONFIG=$DOCKERENV_HOME/.config/sublime-text-2/Packages
mkdir -p $SUBLIME_CONFIG
(cd $SUBLIME_CONFIG; git clone https://github.com/kemayo/sublime-text-git.git)
chown -R $DOCKERENV_USER:users $DOCKERENV_HOME/.config

echo set terminal size
# the default sizes work tragically on a laptop -- we're making a small
# number of windows, not some arbitrary workspace
echo "export CHROME_REMOTE_DESKTOP_DEFAULT_DESKTOP_SIZES=1024x800" >> $DOCKERENV_HOME/.profile


echo set up session
echo "#!/usr/bin/env bash" >$DOCKERENV_HOME/.xsession

startprogram=$1; shift
echo >>$DOCKERENV_HOME/.xsession
for svc in $*; do
  echo "SESSION: ", $svc
  echo "$svc &" >>$DOCKERENV_HOME/.xsession
done
echo $startprogram >>$DOCKERENV_HOME/.xsession
chown $DOCKERENV_USER:users .xsession


### finish initializing the system ###

# gather up syslog in the containing vm's log infrastructure
echo "*.*	@$DOCKERENV_HOST" >>/etc/rsyslog.conf

# restarts the core windowing and logging services service
/etc/init.d/rsyslog restart

/etc/init.d/dbus restart

echo start sshd
# Start the ssh service
mkdir /var/run/sshd 

/usr/sbin/sshd -D
