import argparse
import cuefix
import sys


def main():
    parser = argparse.ArgumentParser(
        prog='cuefix',
        description='Clean and fix a CUE file in a directory',
    )
    parser.add_argument('filepath', help='file path to the input cue file')

    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(cuefix.__version__))

    parser.add_argument('-i', '--info', action='store_true', default=False,
                        help='display metainfo of the input cue file only')

    parser.add_argument('-e', '--encoding', default='utf-8-sig',
                        help='encoding which cue file will be converted to, default is UTF-8 BOM')

    parser.add_argument('-n', '--newline', default='unix',
                        help='newline format which cue file will be converted to, default is Unix')

    parser.add_argument('--no-encoding', action='store_true', default=False,
                        help='converting encoding will be skipped')

    parser.add_argument('--no-newline', action='store_true', default=False,
                        help='converting newline will be skipped')

    parser.add_argument('--no-backup', action='store_true', default=False,
                        help='no backup for the input cue file, USE WITH CAUTION!')

    parser.add_argument('--dryrun', action='store_true', default=False,
                        help='dry-run and print out fixed cue file')

    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='print version and exit')

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
