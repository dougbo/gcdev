
# get this user GIT enhancement for sublime
SUBLIME_CONFIG=$DOCKERENV_HOME/.config/sublime-text-2/Packages
mkdir -p $SUBLIME_CONFIG
(cd $SUBLIME_CONFIG; git clone https://github.com/kemayo/sublime-text-git.git)
chown -R $DOCKERENV_USER:users $DOCKERENV_HOME/.config
