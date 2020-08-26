import argparse
import cuefix
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Clean and fix a CUE file in a directory')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(cuefix.__version__))
    parser.add_argument('-d', '--encoding', action='store',
                        default='utf-8-sig')
    parser.add_argument('-n', '--newline', action='store', default='unix')
    parser.add_argument('-v', '--verbose', action='store',
                        type=bool, default=False)

    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    main()
