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
    parser_init.add_argument('--lang', dest='project_lang',
                             default='python:flask',
                             help='Set language:framework')

    # Edit
    parser_edit = subparsers.add_parser('edit', help='Create editor.')
    parser_edit.set_defaults(cmd='edit')
    parser_edit.add_argument('--projectl', dest='project_name',
                             help="Project to edit")


    return parser
