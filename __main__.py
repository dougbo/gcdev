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
Driver program for gcdev, CLI for manipulating cloud development 
environments accessed via Chrome Remote Desktop
"""

import sys

from gcdev import get_parser
from gcdev import init
from gcdev import run
from gcdev import publish
from gcdev import ssh

import gcd_errors

def main(argv):
    """Runs main program.

    Args:
        argv: The list of command line arguments.

    Returns:
        The status code of the script.
    """
    first = argv[0]
    remaining = argv[1:]

    parser = get_parser()
    args = parser.parse_args(remaining)

    # xxx(orr): use introspection on gcdev module
    if args.cmd == 'run':
        run(args)
    elif args.cmd == 'init':
        init(args)
    elif args.cmd == 'publish':
        publish(args)
    elif args.cmd == 'ssh':
        ssh(args)
    else:
        gcd_errors.Fail("Unexpected command: "+args.cmd)
    
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
