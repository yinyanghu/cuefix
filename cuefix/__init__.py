from .version import __version__, VERSION
from .cuefix import CueFile, CueFix


def fix(filepath, encoding='utf-8-sig', newline='unix', dryrun=False, verbose=False):
    CueFix(CueFile(filepath)).fix(encoding, newline, dryrun, verbose)


__all__ = [fix, '__version__', 'VERSION', CueFile, CueFix, fix]
