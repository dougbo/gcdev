# Cloud Tools Docker environment

FROM dougbo/gcdev-crd
MAINTAINER doug orr "doug.orr@gmail.com"

# define ENV's for version-specific downloads
ENV SUBLIME http://c758482.r82.cf2.rackcdn.com/Sublime%20Text%202.0.2%20x64.tar.bz2

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

RUN wget https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.zip && unzip google-cloud-sdk.zip && rm google-cloud-sdk.zip
RUN google-cloud-sdk/install.sh --usage-reporting=true --path-update=true --bash-completion=true --rc-path=/.bashrc --disable-installation-options
RUN yes | google-cloud-sdk/bin/gcloud components update pkg-go pkg-python pkg-java


# add our custom scripts
ADD src/ /src


# Customize the environment; define X clients and start ssh services.
#  startfluxbox xterm sublime rox fluxbox
CMD ["/bin/bash", "/src/crd-start.sh", "startfluxbox", "xterm", "sublime", "rox", "fluxbox"]
