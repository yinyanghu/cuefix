import argparse
import cuefix
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Clean and fix a CUE file in a directory')
    parser.add_argument('filepath')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(cuefix.__version__))
    parser.add_argument('-i', '--info', action='store_true', default=False)
    parser.add_argument('-e', '--encoding', default='utf-8-sig')
    parser.add_argument('-n', '--newline', default='unix')
    parser.add_argument('--no-encoding', action='store_true', default=False)
    parser.add_argument('--no-newline', action='store_true', default=False)
    parser.add_argument('--no-backup', action='store_true', default=False)
    parser.add_argument('--dryrun', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', default=False)

    args = parser.parse_args()
    if args.info:
        print(cuefix.info(args.filepath))
        return

    cuefix.fix(args.filepath,
               args.encoding if not args.no_encoding else None,
               args.newline if not args.no_newline else None,
               not args.no_backup,
               args.dryrun, args.verbose)


if __name__ == '__main__':
    main()
