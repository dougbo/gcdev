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

"""Command line tool for managing Google Cloud Platform development process
"""

import argparse
import subprocess
import os
import time
import sys

import docker
from gitcmd import git_init_repo
from metadatadatastore import MetadataDataStore
import gcd_errors

_SHORT_CONTAINER_ID_LEN=12    # there's a short and long ID form

def get_parser():
    """Argument parser for gcdev

    Registers the commands:
        init: For setting the project/language/framework parameters
        edit: For creating a cloud instance in which to do development

    Returns:
        An argparse.ArgumentParser that can parse the passed in arguments.
    """
    parser = argparse.ArgumentParser(
            prog='gcdev', description='gcdev Google Cloud developement interface')
    subparsers = parser.add_subparsers(help='gcdev commands')

    # Init
    parser_init = subparsers.add_parser('init', help='Init environment.')
    parser_init.set_defaults(cmd='init')
    parser_init.add_argument('--project', dest='project_name',
                             default=None,
                             help='Set development project name')
    parser_init.add_argument('--appengine', action='store_true', dest='is_gae',
                             help='Initialize for App Engine development')
    parser_init.add_argument('--android', action='store_true', dest='is_android',
                             help='Intialize for Android development')
    parser_init.add_argument('--platform', dest='platform',
                             help='Platform template')
    parser_init.add_argument('--emul', action='store_true', dest='emul',
                             help='Initialize for Andoid+emulation development')
    parser_init.add_argument('--repo', dest='git_repo',
                             help='Set git repository to pull from/push to')
    parser_init.add_argument('--lang', dest='project_lang',
                             help='Set language:framework for default template')

    # Edit
    parser_edit = subparsers.add_parser('edit', help='Create editor.')
    parser_edit.set_defaults(cmd='edit')
    parser_edit.add_argument('--project', dest='project_name',
                             default=None,
                             help='Project to edit')
    parser_edit.add_argument('--desktop_name', dest='crd_name',
                             help='Name of the Chrome Remote Desktop session')
    parser_edit.add_argument('--restart', dest='restart',
                             default=False, action='store_true',
                             help='Restart the editor environment')
    parser_edit.add_argument('--container', dest='container',
                             help='Name of the edit container to replace')

    # Publish
    parser_publish = subparsers.add_parser('publish', help='Publish current project in Apps Marketplace')
    parser_publish.set_defaults(cmd='publish')
    parser_publish.add_argument('--project', dest='project_name',
                                default=None,
                                help='Project to publish')


    # ssh
    parser_ssh = subparsers.add_parser('ssh', help='Ssh interactively into docker container')
    parser_ssh.set_defaults(cmd='ssh')
    parser_ssh.add_argument('--image', dest='image',
                            help='Image to use to create container to ssh into')
    parser_ssh.add_argument('--container', dest='container',
                            help='Container to ssh into')


    return parser


# docker sub-modules: 
#  crd: chrome remote desktop
#  clouddev: tools for cloud development (sublime, git, etc.)
#  androiddev: android studio
#  gcp: google cloud platform sdk/apis
#  gapi: google apis (apps, geo, yt, etc.)
#  data: *per user* data volume for persistent storage of state
_GOOGLE_CRD_IMAGE="google/crd-env"
_GOOGLE_CLOUD_IMAGE="google/cloudtools" 
_GOOGLE_ANDROID_IMAGE="google/androidtools" 
_GOOGLE_ANDROIDPLUSEMUL_IMAGE="google/androidtools-emul" 

_DOCKER_CRD=("Dock.crd/", _GOOGLE_CRD_IMAGE)
_DOCKER_CLOUDTOOLS=("Dock.cloudtools/", _GOOGLE_CLOUD_IMAGE)
_DOCKER_ANDROIDTOOLS=("Dock.androidtools/", _GOOGLE_ANDROID_IMAGE)
_DOCKER_ANDROIDTOOLSPLUSEMUL=("Dock.androidtools+emul/", _GOOGLE_ANDROIDPLUSEMUL_IMAGE)

_MAX_SSH_RETRY=8


def _start(image, mdds):
    """
    Create a new container from the given image
    """

    def _get_env():
        """
        _get_env: create a dict with the env variables we wish to pass to the 
        docker container
        """
        try:
            authkeys = subprocess.check_output(["ssh-add", "-L"])
        except subprocess.CalledProcessError:
            raise gcd_errors.NoAuthKeys("User must have forwarded ssh auth keys.\n"
                                        "Please use 'ssh -A' to connect to this system")
        try:
            hostname = subprocess.check_output("hostname")
        except subprocess.CalledProcessError:
            hostname = ""

        env = {
            'DOCKERENV_USER': mdds.get('user') or os.getenv('USER'),
            'DOCKERENV_AUTHKEYS': mdds.get('ssh-keys') or authkeys,
            'DOCKERENV_HOST': hostname,
            'DOCKERENV_PROJECT': mdds.get('project_name')
            }
        return env

    # edit: start a new containerized editing environment

    # first, find out how many currently running containers we have
    latest_image = "%s:latest" % image

    containers = [d for d in docker.ps() if d['image'] == latest_image]
    print "EXISTING CONTAINERS: ", containers

    if len(containers):
        print "%12.12s\t%s" % ("CONTAINER ID", "CREATED")
    for c in containers:
        print "%12.12s\t%s" % (c['container id'], c['created'])

    container = docker.start(latest_image, env=_get_env())[0:_SHORT_CONTAINER_ID_LEN]
    print "started: container=", container

    # get an ssh connection into the new container
    ssh = docker.get_ssh(container_id=container)
    if not ssh:
        raise gcd_errors.Fail("container failed to start")

    # make sure that ssh has had enough time to start
    for timeout in range(1,_MAX_SSH_RETRY):
        try:
            output = ssh("echo","Connected")
            break
        except subprocess.CalledProcessError:
            if timeout == _MAX_SSH_RETRY:
                raise gcd_errors.Fail("Couldn't connect to ssh service")
            time.sleep(timeout*10)

    # note that we have a container, and track what image it's with
    return container


def init(args):
    """
    Save parameters in the metadata store that we will use to guide
    creation of cloud-based edit sessions

    Create a docker container specialized to the language/sdk environment

    parameters:
      project*
      git repository (may be project-derived)*
      editor*
      language[:framework]
    """

    _NON_PERSISTENT_ARGS=['cmd'] # arguments not intended to persist

    # check the parameters for semantic issues
    argdict = vars(args)
    if argdict['project_name'] == None:
        raise gcd_errors.Fail("Project name must be specified")
    if argdict['is_gae'] and argdict['is_android']:
        raise gcd_errors.InvalidCondition("Cannot specify both Android and App Engine")


    # store the current project state in the metadata store for this user; 
    # restart database
    mdds = MetadataDataStore(init=True)

    for arg in argdict:
        if arg in _NON_PERSISTENT_ARGS:
            pass
        mdds.store(arg, argdict[arg])


    # make sure that our component images are built
    if argdict['is_gae']:
        images = [_DOCKER_CLOUDTOOLS]
    elif argdict['is_android'] or argdict['emul']:
        if argdict['emul']:
            images = [_DOCKER_ANDROIDTOOLSPLUSEMUL]
        else:
            images = [_DOCKER_ANDROIDTOOLS]
    elif argdict['platform']:
        platform = argdict['platform']
        images = [('Dock.%s' % platform, 'google/gcdev-%s' % platform)]
    else:
        images = [_DOCKER_CRD]

    for dir, tag in images:
        output = docker.do(["build", "--rm=true", "-t", tag, dir])
        if not output:
            raise gcd_errors.Fail("Docker build failed for %s" % tag)
        print "BUILD: ", tag, output

    image = images[-1][1]
    mdds.store('project_image', image)
    print "INIT: image: '%s'" % image

    # add in a specialized version of whatever framework the user is intending
    # to use in their language of choice
    template = gen_template(args.project_lang)
    if template:
        # add to the repository; it will be pulled into the user's home dir
        # in the edit phase
        git_repo = mdds.get('git_repo')
        git = git_init_repo(git_repo)
        git("push %s" % template)
        
        mdds.store('active_template', 'true')


def edit(args):
    """
    Use create the cloud-based container for program development based on 
    parameters in the metadata store, modified by our arguments

    edit --image <image>, starts a new container with that image
    edit [no args] 
        if mdds['project_image'] starts a new container from that image
    """

    mdds = MetadataDataStore()
    project_name = mdds.get("project_name")
    if not project_name:
        raise gcd_errors.InvalidCondition("Uninitialized project")

    argdict = vars(args)
    image = argdict.get('image') or mdds.get('project_image')

    print "EDIT: image: ", image
    container = _start(image, mdds)

    print "EDIT: using container ", container
    mdds.store('project_image', image)
    mdds.store('project_container', container)

    # fetch the latest of the user's work into the template
    if mdds.get('active_template'):
        user_template = mdds.get('user_template')
        git_repo = mdds.get('git_repo')
        ssh("git --repo %s pull %s" (git_repo, user_template))
        

    ssh = docker.get_ssh(container_id=container)
    
    # otherwise, layer on top of it Chrome Remote Desktop,
    # specialized to bring up the
    # editor of their choice which is specialized to their GIT repository
    crd_name = argdict.get('crd_name') or project_name
    _CRD_CMD="/opt/google/chrome-remote-desktop/start-host --redirect-url=https://chromoting-auth.googleplex.com/auth"
    ssh(". .profile; %s %s" % (_CRD_CMD, "--name=%s" % crd_name))




def gen_template(lang):
    """
    Create the base file that will be used as the starting basis for the
    program
    """
    
    return None


def publish(args):
    """
    Publish the current project in the Apps marketplace
    """
    raise gcd_errors.Fail("Not yet implemented")

def ssh(args):
    """
    invoke ssh interactively with a container (possibly in the current project)

    ssh --image <image> will start an image and ssh to that container
    ssh --container <container> will ssh to that container

    ssh [no args]:
        if mdds['container'] ssh to that container
        if mdds['project_image'] start that image, ssh to that container
    """

    def _container_exists(container):
        # make sure it's still running
        for c in docker.ps():
            if c['container id'] == container[:_SHORT_CONTAINER_ID_LEN]:
                return True

        return False

    def _ssh_to_container(container):
        try:
            # get back the raw command so that we can exec it
            ssh_cmd = docker.get_ssh_cmd(container_id=container)
        except:
            gcd_errors.Fail("Couldn't start connection")

        return subprocess.check_call(ssh_cmd)



    argdict = vars(args)

    mdds = MetadataDataStore()

    if argdict.get('image', None) and argdict.get('container', None):
        raise gcd_errors.InvalidCondition("Cannot specify both --image and --container")

    container = argdict.get('container', None)
    if container:
        # we directly reference an existing container
        print "SSH: container: '%s'" % (container)
        return _ssh_to_container(container)

    # may need to start a container
    image = argdict.get('image')
    if image:
        container = _start(image, mdds)

        print "SSH: image: '%s' container '%s'" % (image, container)
        return _ssh_to_container(container)

    # no explicit image or container. see if the current project has a container
    container = mdds.get('project_container')
    if container:
        print "SSH: container: '%s'" % (container)
        return _ssh_to_container(container)

    # no project container -- if we have an project image, start it and use that container
    image = mdds.get('project_image')
    if not image:
        raise gcd_errors.InvalidCondition("No --image or initialized project")

    container = _start(image, mdds)
    print "SSH: image: '%s' container '%s'" % (image, container)
    return _ssh_to_container(container)




if __name__ == '__main__':
    class v:
        project_name = 'test'
        restart = False
        container = 'aa584cb86b1c'

    edit(v)
