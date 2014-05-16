# Android Studio environment plus i386 linux environment (for running emulation)

FROM google/androidtools
MAINTAINER doug orr "doug.orr@gmail.com"


# install the i386 world so that the android emulator will work
RUN apt-get -y install libc6-i386
RUN dpkg --add-architecture i386
RUN apt-get update
RUN apt-get -y install ia32-libs

# Customize the environment and start ssh services.
CMD ["/bin/bash", "/src/android-start.sh"]
