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

import docker
from gitcmd import git_init_repo
from metadatadatastore import MetadataDataStore
import gcd_errors


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
                             help='Set development project name')
    parser_init.add_argument('--appengine', action='store_true', dest='is_gae',
                             help='Initialize App Engine configuration')
    parser_init.add_argument('--scopes', dest='project_scopes',
                             nargs='*', action='append',
                             help='Set authorization scopes')
    parser_init.add_argument('--repo', dest='git_repo',
                             default=None,
                             help='Set git repository')
    parser_init.add_argument('--lang', dest='project_lang',
                             default=None,
                             help='Set language:framework for default template')

    # Edit
    parser_edit = subparsers.add_parser('edit', help='Create editor.')
    parser_edit.set_defaults(cmd='edit')
    parser_edit.add_argument('--project', dest='project_name',
                             help="Project to edit")
    parser_edit.add_argument('--desktop_name', dest='crd_name',
                             default="google-dev",
                             help="Name of the Chrome Remote Desktop sessoinn")

    # Publish
    parser_publish = subparsers.add_parser('publish', help='Publish current project in Apps Marketplace')
    parser_publish.set_defaults(cmd='publish')
    parser_publish.add_argument('--project', dest='project_name',
                                help='Project to publish')



    return parser



_GOOGLE_DEV_IMAGE="google/dev-env" # our docker image name

def edit(args):
    """
    Use the parameters stored in the metadata store to guide creation of a
    cloud-based edit session that we tie in with, via GVC.
    """
    mdds = MetadataDataStore()

    def _get_env():
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
            }
	print "ENV: ", env
        return env

    if mdds.get('project_name') == None:
        raise gcd_errors.InvalidCondition("Uninitialized project")

    
    # see if we have a running docker environment (has the machine been
    # rebooted since our last 'edit'
    # ssh = docker.get_ssh(image=_GOOGLE_DEV_IMAGE)
    ssh = None
    if not ssh:
        container = docker.start(_GOOGLE_DEV_IMAGE, env=_get_env())

        ssh = docker.get_ssh()
        if not ssh:
            raise gcd_errors.Fail("Container failed to start")

        # make sure that ssh has had enough time to start
        for timeout in range(1,5):
            try:
                output = ssh("echo","hi")
                break
            except subprocess.CalledProcessError:
                print "ssh: sleep ",timeout
                time.sleep(timeout*5)

        # fetch the latest of the user's work into the template
        if mdds.get('active_template'):
            user_template = mdds.get('user_template')
            git_repo = mdds.get('git_repo')
            ssh("git --repo %s pull %s" (git_repo, user_template))
        
    
    # otherwise, layer on top of it Chrome Remote Desktop,
    # specialized to bring up the
    # editor of their choice which is specialized to their GIT repository
    crd_name = mdds.get('crd_name')
    _CRD_CMD="/opt/google/chrome-remote-desktop/start-host"
    
    ssh(". .profile; %s %s" % (_CRD_CMD, "--name=%s" % crd_name))


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
    if 'project_name' not in argdict or argdict['project_name'] == None:
        raise gcd_errors.Fail("Project name must be specified")

    # store the current project state in the metadata store for this user
    mdds = MetadataDataStore()

    for arg in argdict:
        if arg in _NON_PERSISTENT_ARGS:
            pass
        
        mdds.store(arg, argdict[arg])

    # create a docker environment using an underlying base of the Google Cloud
    # SDK, plus popular API client libraries.

    # xxx(orr): probably consolidate this into one well-known Dockerfile?
    output = docker.do(["build", "-t", _GOOGLE_DEV_IMAGE, "."])
    if not output:
        raise gcd_errors.Fail("Docker build failed")

    # xxx(orr)
    #_docker("run -t google-dev pull google/sdk")
    #_docker("run -t google-dev pull google/apps-apis")
    #_docker("run -t google-dev pull google/geo-apis")
    #_docker("run -t google-dev pull google/yt-apis")

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
