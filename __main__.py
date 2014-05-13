import sys

from gcdev import get_parser
from gcdev import init
from gcdev import edit
from gcdev import publish
from gcdev import ssh

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
    if args.cmd == 'edit':
        edit(args)
    elif args.cmd == 'init':
        init(args)
    elif args.cmd == 'publish':
        publish(args)
    elif args.cmd == 'ssh':
        ssh(args)
    else:
        fatal("Unexpected command: "+args.cmd)
    
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
