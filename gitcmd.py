# Copyright 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    
