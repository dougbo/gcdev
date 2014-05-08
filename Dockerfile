#
#
FROM debian
MAINTAINER doug orr "doug.orr@gmail.com"


# add repo for chrome remote desktop
RUN echo deb http://dl.google.com/linux/chrome-remote-desktop/deb/ stable main >/etc/apt/sources.list.d/chromeos.list

RUN apt-get update
RUN apt-key update
RUN apt-get install -y apt-utils

# get crd
RUN apt-get -y --allow-unauthenticated install chrome-remote-desktop

# get git
RUN apt-get install -y git

# get the various google api runtime packages
# get sublime
# ENV SUBLIME sublime-text_build-3047_amd64.deb
# ADD http://c758482.r82.cf2.rackcdn.com/$SUBLIME /tmp/$SUBLIME
# RUN dpkg -i /tmp/$SUBLIME


RUN apt-get install -y bzip2
ADD http://c758482.r82.cf2.rackcdn.com/Sublime%20Text%202.0.2%20x64.tar.bz2 /opt/sublime.tbz
RUN cd /opt; tar -xvjf sublime.tbz
RUN ln -s /opt/Sublime\ Text\ 2/sublime_text /usr/bin/sublime



# google cloud SDK
RUN apt-get install -y curl
# RUN curl https://dl.google.com/dl/cloudsdk/release/install_google_cloud_sdk.bash | bash

# ** PYTHON **
# popular GAPI client libraries: drive, geo, youtube, etc.
ENV GOOGLE_OAUTH_CLIENT python-google-api-python-client_1.2.0-1_all.deb
ADD https://google-api-python-client.googlecode.com/files/$GOOGLE_OAUTH_CLIENT /tmp/
RUN dpkg -i /tmp/$GOOGLE_OAUTH_CLIENT

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
ADD . /src


# minor cleanup
RUN sed 's/# en_US/en_US/g' </etc/locale.gen >/tmp/locale.out; mv /tmp/locale.out /etc/locale.gen
RUN locale-gen
# RUN localedef -v -c -i en_US -f UTF-8 en_US.UTF-8
RUN ln -s /usr/bin/Xvfb /usr/bin/xvfb


# NOTE: we're single user and various things don't work if they try
# to work with setgid programs that try to read /etc/shadow;
# DON"T STORE PASSWORDS IN THIS CONTAINER
RUN chmod go+r /etc/shadow

# https://github.com/dotcloud/docker/issues/5126
RUN chmod 1777 /dev/shm

# allow ssh -- we'll have to dig the port out of the ps entry later
EXPOSE 22

# Customize the environment and start ssh services.
CMD ["/bin/bash", "/src/docker-start.sh"]
