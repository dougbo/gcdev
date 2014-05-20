# Chrome Remote Desktop Docker environment

# Install Chrome remote desktop and set up an X-based platform that we can attach
# environments and set up tools on

FROM debian
MAINTAINER doug orr "doug.orr@gmail.com"

# add repo for chrome remote desktop
RUN echo deb http://dl.google.com/linux/chrome-remote-desktop/deb/ stable main >/etc/apt/sources.list.d/chromeos.list

RUN apt-get update
RUN apt-key update
RUN apt-get install -y apt-utils

# get crd
RUN apt-get -y --allow-unauthenticated install chrome-remote-desktop


# Set the env variable DEBIAN_FRONTEND to noninteractive
ENV DEBIAN_FRONTEND noninteractive

# Installing the environment required: xserver and ssh
RUN apt-get install -y xserver-xorg 
RUN apt-get install -y xterm
RUN apt-get install -y rox-filer ssh fluxbox 
RUN apt-get install -y rsyslog

# Set locale (fix the locale warnings)
RUN apt-get install -y locales

RUN apt-get -y upgrade

# Copy the files into the container
ADD src/ /src
RUN groupadd androiddev


# minor cleanup
RUN sed 's/# en_US/en_US/g' </etc/locale.gen >/tmp/locale.out; mv /tmp/locale.out /etc/locale.gen
RUN locale-gen
# RUN localedef -v -c -i en_US -f UTF-8 en_US.UTF-8
RUN ln -s /usr/bin/Xvfb /usr/bin/xvfb


# NOTE: we're single user and various things don't work if they try
# to work with setgid programs that try to read /etc/shadow;
# DON"T STORE PASSWORDS IN THIS CONTAINER
RUN chmod go+r /etc/shadow

RUN chmod 1777 /dev/shm

# allow ssh -- we'll have to dig the port out of the ps entry later
EXPOSE 22

# Customize the environment and start ssh services.
CMD ["/bin/bash", "/src/crd-start.sh"]
