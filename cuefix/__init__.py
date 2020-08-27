from .version import __version__, VERSION
from .cuefix import CueFile, CueFix


def fix(filepath, encoding='utf-8-sig', newline='unix', backup=True, dryrun=False, verbose=False):
    CueFix(CueFile(filepath), backup, dryrun, verbose).fix(encoding, newline)


def info(filepath):
    return str(CueFile(filepath))


__all__ = [fix, '__version__', 'VERSION', CueFile, CueFix, fix, info]
