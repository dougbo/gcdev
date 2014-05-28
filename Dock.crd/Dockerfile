# Chrome Remote Desktop Docker environment

# Install Chrome remote desktop and set up an X-based platform that we can 

# attach environments and set up tools on

FROM debian
MAINTAINER doug orr "doug.orr@gmail.com"

# add repo for chrome remote desktop
RUN echo deb http://dl.google.com/linux/chrome-remote-desktop/deb/ stable main >/etc/apt/sources.list.d/chromeos.list

RUN apt-get update
RUN apt-key update
RUN apt-get install -y apt-utils

# get crd
RUN apt-get -y --allow-unauthenticated install chrome-remote-desktop

# installing crd updates the source lists (arg); remove the now-redundant
# spec's so we don't get apt errors
RUN rm /etc/apt/sources.list.d/chromeos.list


# Set the env variable DEBIAN_FRONTEND to noninteractive
ENV DEBIAN_FRONTEND noninteractive

# Installing the environment required: xserver and ssh
RUN apt-get install -y xserver-xorg 
RUN apt-get install -y xterm
RUN apt-get install -y rox-filer ssh fluxbox 
RUN apt-get install -y rsyslog
RUN apt-get install -y strace

# Set locale (fix the locale warnings)
RUN apt-get install -y locales

RUN apt-get -y upgrade

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

# run as a non-root user; in derived containers we'll set up more 
# per-user customization
ENV USER crd
ENV HOME /home/$USER

RUN addgroup chrome-remote-desktop
RUN adduser --quiet --disabled-login --disabled-password --home $HOME --ingroup sudo $USER
RUN echo "$USER ALL=(ALL:ALL) NOPASSWD: ALL" >/etc/sudoers.d/$USER
RUN chmod 0440 /etc/sudoers.d/$USER

RUN echo "exec xterm" >$HOME/.xsession
RUN chown $USER $HOME/.xsession

# pick a better default size
ENV CHROME_REMOTE_DESKTOP_DEFAULT_DESKTOP_SIZES 1024x800

# launch the remote desktop as our new user
# it's gross, but we need to make sure the CMD doesn't exit 
USER crd
CMD /opt/google/chrome-remote-desktop/start-host --redirect-url=https://chromoting-auth.googleplex.com/auth --name=BasicCRD; while true; do read line; done
