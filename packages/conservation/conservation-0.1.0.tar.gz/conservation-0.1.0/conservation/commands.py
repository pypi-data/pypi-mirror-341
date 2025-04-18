import argparse
import textwrap
import sys
from conservation.version import __version__
from conservation.conservation_codon import main as codon_main


def conservation_parser():
    usage = '''\
    conservation <command> [options]
    Commands:
        codon           Codon conservation analysis
    Run conservation <command> -h for help on a specific command.
    '''
    parser = argparse.ArgumentParser(
        description='Conservation: Codon and Amino Acid Conservation Analysis',
        usage=textwrap.dedent(usage)
    )

    parser.add_argument('--version', action='version', version=f'conservation {__version__}')
    parser.add_argument('command', nargs='?', help='Subcommand to run')

    return parser


def codon_parser():
    from conservation.conservation_codon import parse_args
    return parse_args()


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def main():
    parser = conservation_parser()
    args, remaining_args = parser.parse_known_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == 'codon':
        sys.argv = [sys.argv[0]] + remaining_args
        codon_main()
    else:
        sys.stderr.write(f"Unknown command: {args.command}\n")
        parser.print_help()
        return 1

    return 0
