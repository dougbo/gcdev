
FROM google/crd-env
MAINTAINER doug orr "doug.orr@gmail.com"

# define ENV's for version-specific downloads
# get the android studio and r22 sdk; put the sdk in studio's sdk area
ENV STUDIO android-studio-bundle-133.1028713-linux.tgz
ENV SDK android-sdk_r22.6.2-linux.tgz


# ** get some basics **
RUN apt-get update && apt-get install -y -qq --no-install-recommends wget unzip python bzip2

# ** install general utility developer tools **

# get git
RUN apt-get install -y git

# get java
RUN apt-get install -y openjdk-7-jre openjdk-7-jdk

# Copy the files into the container
ADD src/ /src

# * get android sdk *

# there's some funky group thing -- make sure that there's group permission
# for the studio so that we can install it in a well known place rather than
# installing to someone's home directory. plus chgrp -R takes forever in this 
# context

# make sure we know the directory name the tar file goes into
ADD http://dl.google.com/android/studio/install/0.4.6/$STUDIO /home/
ADD http://dl.google.com/android/$SDK /home/
RUN chmod a+rx /home/$STUDIO /home/$SDK

# RUN cd /home; tar -xvf $STUDIO
# RUN cd /home; tar -xvf $SDK

# Customize the environment and start ssh services.
CMD ["/bin/bash", "/src/android-start.sh"]
