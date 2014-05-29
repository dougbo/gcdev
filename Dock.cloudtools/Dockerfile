# Cloud Tools Docker environment

FROM dougbo/gcdev-crd
MAINTAINER doug orr "doug.orr@gmail.com"

# define ENV's for version-specific downloads
ENV SUBLIME http://c758482.r82.cf2.rackcdn.com/Sublime%20Text%202.0.2%20x64.tar.bz2

USER root

# ** get some basics **
RUN apt-get update && apt-get install -y -qq --no-install-recommends wget unzip python bzip2

# ** install general utility developer tools **

# get git
RUN apt-get install -y git

# get sublime
ADD $SUBLIME /opt/sublime.tar.bz
RUN cd /opt; tar -xvjf ./sublime.tar.bz
RUN rm -f /usr/bin/sublime
RUN ln -s /opt/Sublime*/sublime_text /usr/bin/sublime
RUN rm -f /opt/sublime.tar.bz

# emacs and vim just for good measure
RUN apt-get install -y emacs vim


# install the google cloud platform tools

USER crd

RUN cd $HOME; wget https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.zip && unzip google-cloud-sdk.zip && rm google-cloud-sdk.zip
RUN cd $HOME; google-cloud-sdk/install.sh --usage-reporting=true --path-update=true --bash-completion=true --rc-path=$HOME/.bashrc --disable-installation-options
RUN cd $HOME; yes | google-cloud-sdk/bin/gcloud components update pkg-go pkg-python pkg-java

# Customize the environment; define X clients and start ssh services.

RUN echo "" >$HOME/.xsession
RUN echo "rox &" >>$HOME/.xsession
RUN echo "sublime &" >>$HOME/.xsession
RUN echo "xterm &" >>$HOME/.xsession
RUN echo "exec startfluxbox" >>$HOME/.xsession

CMD /opt/google/chrome-remote-desktop/start-host --redirect-url=https://chromoting-auth.googleplex.com/auth --name=CloudTools; while true; do read line; done
