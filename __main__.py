import sys

from gcdev import get_parser


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
    print args
    
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
