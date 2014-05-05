"""
Git support for gcdev: provide a simple interface to 
"""



def git_init_repo(repo_name):
    _GITHUB_ID = "git@github.com"
    
    if repo_name[0:len(_GITHUB)] == _GITHUB:
        if _github_init(repo_name):
            return lambda gitcmd: _github_cmd(repo_name, gitcmd)
        return None
    else:
        # xxx(orr): for the moment assume we're a GAE repository
        # xxx(orr): figure out what all the options are, really
        return lambda gitcmd: _gae_repo_cmd(repo_name, gitcmd)


def _github_cmd(repo, cmd):
    print 'XXX: github repo "%s" cmd "%s"' % (repo, cmd)

def _gae_repo_cmd(repo, cmd):
    print 'XXX: gae repo "%s" cmd "%s"' % (repo, cmd)
    
