#!/bin/sh

#
# ** create the per-user dynamic environment **
#

### initialize for our container owner ###

echo "Starting Chrome Remote Desktop environment"

. /src/base-start.sh

echo "launching crd"

echo set terminal size
# the default sizes work tragically on a laptop -- we're making a small
# number of windows, not some arbitrary workspace
echo "export CHROME_REMOTE_DESKTOP_DEFAULT_DESKTOP_SIZES=1024x800" >> $DOCKERENV_HOME/.profile

# Command line args indicate what X services to start for this
# crd session
echo set up session in $DOCKERENV_HOME
echo "#!/usr/bin/env bash" >$DOCKERENV_HOME/.xsession

if [ $# != 0 ]; then
  startprogram=$1; shift
else
  startprogram=xterm
fi
echo >>$DOCKERENV_HOME/.xsession
for svc in $*; do
  echo "SESSION: " $svc
  echo "$svc &" >>$DOCKERENV_HOME/.xsession
done
echo exec $startprogram >>$DOCKERENV_HOME/.xsession
chown $DOCKERENV_USER:users $DOCKERENV_HOME/.xsession

### finish initializing the system ###

# gather up syslog in the containing vm's log infrastructure
echo "*.*	@$DOCKERENV_HOST" >>/etc/rsyslog.conf

chmod 1777 /dev/shm

# restarts the core windowing and logging services service
/etc/init.d/rsyslog restart

/etc/init.d/dbus restart

echo start sshd
# Start the ssh service
mkdir /var/run/sshd 
/usr/sbin/sshd &

su $DOCKERENV_USER -c "/opt/google/chrome-remote-desktop/start-host --redirect-url=https://chromoting-auth.googleplex.com/auth --name=$DOCKERENV_USER"


