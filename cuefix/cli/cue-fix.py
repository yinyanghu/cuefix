import argparse
import sys


from cuefix import __version__


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Clean and fix a CUE file in a directory')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(__version__))
    args = parser.parse_args(argv)


if __name__ == '__main__':
    main()
