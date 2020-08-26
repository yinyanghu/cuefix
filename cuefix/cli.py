import argparse
import cuefix
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Clean and fix a CUE file in a directory')
    parser.add_argument('filepath')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(cuefix.__version__))
    parser.add_argument('-e', '--encoding', default='utf-8-sig')
    parser.add_argument('-n', '--newline', default='unix')
    parser.add_argument('--dryrun', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', default=False)

    args = parser.parse_args()
    print(args)
    cuefix.fix(args.filepath, args.encoding,
               args.newline, args.dryrun, args.verbose)


if __name__ == '__main__':
    main()
