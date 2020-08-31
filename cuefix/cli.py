import logging

import argparse
import cuefix
import sys


def validate_args(args):
    pass


def main():
    parser = argparse.ArgumentParser(
        prog='cuefix',
        description='Fix a CUE file in a directory: convert encoding, convert newline character, fix not matched audio file.',
    )
    parser.add_argument('filepath', help='file path to the input cue file')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(cuefix.__version__),
                        help='print the version of cuefix and exit')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='enable verbose output')

    dryrun_group = parser.add_argument_group('dry-run options')
    dryrun_group.add_argument('-y', '--yes', action='store_true', default=False,
                              help='disable interactive mode and yes to all prompts')
    dryrun_group.add_argument('-i', '--info', action='store_true', default=False,
                              help='display metainfo of the input cue file only')
    dryrun_group.add_argument('--dryrun', action='store_true', default=False,
                              help='dry-run and print out fixed cue file')

    fix_group = parser.add_argument_group('fix options')
    fix_group.add_argument('-e', '--encoding', default='utf-8-sig',
                           choices=['utf-8-sig', 'utf-8', 'gb2312'],
                           help='encoding which cue file will be converted to, default is UTF-8 BOM (utf-8-sig)')
    fix_group.add_argument('-n', '--newline', default='unix',
                           choices=['unix', 'windows'],
                           help='newline format which cue file will be converted to, default is Unix')
    fix_group.add_argument('--no-encoding', action='store_true', default=False,
                           help='converting encoding will be skipped')
    fix_group.add_argument('--no-newline', action='store_true', default=False,
                           help='converting newline will be skipped')

    backup_group = parser.add_argument_group('backup options')
    backup_group.add_argument('--no-backup', action='store_true', default=False,
                              help='no backup for the input cue file, USE WITH CAUTION!')

    args = parser.parse_args()

    validate_args(args)

    logging.basicConfig(level=logging.INFO)
    if args.verbose:
        cuefix.log.setLevel(logging.INFO)

    if args.info:
        cuefix.info(args.filepath, not args.yes)
        return

    cuefix.fix(args.filepath,
               args.encoding if not args.no_encoding else None,
               args.newline if not args.no_newline else None,
               not args.no_backup, args.dryrun, not args.yes)


if __name__ == '__main__':
    main()
