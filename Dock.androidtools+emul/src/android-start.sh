#!/bin/bash

#
# ** create the per-user dynamic environment **
#

echo "ANDROID startup shell"

set -x

. /src/base-start.sh

echo "starting android studio for" $DOCKERENV_USER $DOCKERENV_HOME

mv /home/android-sdk-linux/* /home/android-studio/sdk/
# chown -R $DOCKERENV_USER:androiddev /home/android-studio

# start the android studio in our X environment
/bin/bash -x /src/crd-start.sh /home/android-studio/bin/studio.sh

