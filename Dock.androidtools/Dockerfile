
FROM dougbo/gcdev-crd
MAINTAINER doug orr "doug.orr@gmail.com"

# define ENV's for version-specific downloads
# get the android studio and r22 sdk; put the sdk in studio's sdk area
ENV STUDIO android-studio-bundle-133.1028713-linux.tgz
ENV SDK android-sdk_r22.6.2-linux.tgz

USER root

# * get android sdk *

# make sure we know the directory name the tar file goes into

ADD http://dl.google.com/android/studio/install/0.4.6/$STUDIO $HOME/$STUDIO
ADD http://dl.google.com/android/$SDK $HOME/$SDK

RUN chown crd $HOME/$STUDIO $HOME/$SDK


# ** get some basics **
RUN apt-get update && apt-get install -y -qq --no-install-recommends wget unzip python bzip2

# ** install general utility developer tools **

# get git
RUN apt-get install -y git

# get java
RUN apt-get install -y openjdk-7-jre openjdk-7-jdk

USER crd

RUN cd $HOME; tar -xf $STUDIO
RUN cd $HOME; tar -C $HOME/android-studio/sdk --strip 1 -xf $SDK

RUN echo "exec $HOME/android-studio/bin/studio.sh" >$HOME/.xsession

CMD /opt/google/chrome-remote-desktop/start-host --redirect-url=https://chromoting-auth.googleplex.com/auth --name=AndroidStudio; while true; do read line; done
