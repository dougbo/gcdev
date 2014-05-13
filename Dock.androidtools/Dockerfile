
FROM google/crd-env
MAINTAINER doug orr "doug.orr@gmail.com"

# define ENV's for version-specific downloads
# get the android studio and r22 sdk; put the sdk in studio's sdk area
ENV STUDIO android-studio-bundle-133.1028713-linux.tgz
ENV STUDIO_BASE android-studio
ENV SDK android-sdk_r22.6.2-linux.tgz


# ** get some basics **
RUN apt-get update && apt-get install -y -qq --no-install-recommends wget unzip python bzip2

# ** install general utility developer tools **

# get git
RUN apt-get install -y git

# get java
RUN apt-get install -y openjdk-7-jre openjdk-7-jdk

# * get android sdk *

ADD http://dl.google.com/android/studio/install/0.4.6/$STUDIO /opt/$STUDIO
# make sure we know the directory name the tar file goes into
RUN mkdir /opt/$STUDIO_BASE
RUN cd /opt/$STUDIO_BASE ; tar --strip=1 -xvzf ../$STUDIO

ADD http://dl.google.com/android/$SDK /opt/$SDK
RUN cd /opt; tar -C $STUDIO_BASE/sdk  --strip=1 --show-transformed -xvf $SDK

# install the i386 world so that the android emulator will work
RUN apt-get -y install libc6-i386
RUN dpkg --add-architecture i386
RUN apt-get update
RUN apt-get -y install ia32-libs

# Customize the environment and start ssh services.
CMD ["/bin/bash", "/src/docker-start.sh", "/opt/android-studio/bin/studio.sh"]
