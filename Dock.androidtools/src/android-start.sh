#!/bin/bash

#
# ** create the per-user dynamic environment **
#

echo "ANDROID startup shell"

set -x

. /src/base-start.sh

echo "starting android studio for" $DOCKERENV_USER $DOCKERENV_HOME

# copy android studio, changing permissions (needs to be readable by the user)
# tar -C /home -cf - android-studio | su  -c "tar -C $DOCKERENV_HOME/ -xf -" $DOCKERENV_USER
# install the plugins, fixing their permissions also
# tar -C /home/android-sdk-linux -cf - . | su -c "tar -C $DOCKERENV_HOME/android-studio/sdk -xf -" $DOCKERENV_USER 

# cp -R /home/android-studio $DOCKERENV_HOME/android-studio
mv /home/android-studio $DOCKERENV_HOME/android-studio
tar -C /home/android-sdk-linux -cf - . | tar -C $DOCKERENV_HOME/android-studio/sdk -xf -
chown -R $DOCKERENV_USER:androiddev $DOCKERENV_HOME/android-studio



echo export PATH="$DOCKERENV_HOME/android-studio/bin:$PATH" >> $DOCKERENV_HOME/.profile
chown $DOCKERENV_USER:users $DOCKERENV_HOME/.profile

chmod 1777 /dev/shm

# start the android studio in our X environment
/bin/bash -x /src/crd-start.sh $DOCKERENV_HOME/android-studio/bin/studio.sh

