# CueFix

[![Python](https://img.shields.io/pypi/pyversions/cuefix.svg?style=plastic)](https://badge.fury.io/py/cuefix)
[![PyPI](https://badge.fury.io/py/cuefix.svg)](https://badge.fury.io/py/cuefix)
[![Travis-CI](https://travis-ci.com/yinyanghu/cuefix.svg)](https://travis-ci.com/github/yinyanghu/cuefix)

CueFix is simple command-line tool to fix CUE files which are popular in lossless audio / albums.

CueFix provides the following functionalities:

- automatically detect encoding of CUE file: GB2312, GBK, GB18030, UTF-8, UTF-8 BOM, and SHIFT-JIS
- convert encoding of CUE file: support GB2312, UTF-8, UTF-8 BOM, etc.
- convert newline format of CUE file: support Windows CRLF and Unix LF
- scan the directory and fix not matched audio file in CUE file
- backup the original CUE file so that users can revert the CUE file back
- interactive with users to verify fixed CUE files

Please feel free to fork and contribute to the project if you like.

## Installation

### Prerequisites

The following dependencies are necessary:

- Python 3.6 or above

**Option 1: Install via pip**

The official release of `cuefix` is distributed on PyPI. Note that you should use the Python 3 version of `pip`:

```bash
$ pip3 install cuefix
```

**Option 2: Download from Github or git clone**

This is the recommended way for developers.

```bash
$ git clone git://github.com/yinyanghu/cuefix
```

Run `./setup.py install` to install `cuefix` to your user path.

## Upgrading

If you install `cuefix` using `pip`, you could upgrade it via

```bash
$ pip3 install --upgrade cuefix
```

## Getting Started

```
$ cuefix -h
usage: cuefix [-h] [--version] [-v] [-y] [-i] [--dryrun] [-e {utf-8-sig,utf-8,gb2312}] [-n {unix,windows}]
              [--no-encoding] [--no-newline] [--no-backup]
              filepath

Fix a CUE file in a directory: convert encoding, convert newline character, fix not matched audio file.

positional arguments:
  filepath              file path to the input cue file

optional arguments:
  -h, --help            show this help message and exit
  --version             print the version of cuefix and exit
  -v, --verbose         enable verbose output

dry-run options:
  -y, --yes             disable interactive mode and yes to all prompts
  -i, --info            display metainfo of the input cue file only
  --dryrun              dry-run and print out fixed cue file

fix options:
  -e {utf-8-sig,utf-8,gb2312}, --encoding {utf-8-sig,utf-8,gb2312}
                        encoding which cue file will be converted to, default is UTF-8 BOM (utf-8-sig)
  -n {unix,windows}, --newline {unix,windows}
                        newline format which cue file will be converted to, default is Unix
  --no-encoding         converting encoding will be skipped
  --no-newline          converting newline will be skipped

backup options:
  --no-backup           no backup for the input cue file, USE WITH CAUTION!
```

## CUE Formats Supported by Popular Media Players

### Media Players

- [Foobar 2000](https://www.foobar2000.org/)
  - Windows (version 1.5.5)
- [DeaDBeeF](https://deadbeef.sourceforge.io/)
  - Linux (version 1.8.4)
  - Android
  - Windows (unstable, nightly build)
  - macOS (unstable, nightly build)
- [VOX](https://vox.rocks/)
  - macOS (version 3.3.17)
  - iOS
- [Synology Audio Station](https://www.synology.com/en-ca/dsm/feature/audio_station)
  - Synology DSM (version 6.2.3)
  - Audio Station (version 6.5.5-3374)

### Encoding

Please use the following encoding name in `cuefix`:

- UTF-8: `utf-8`
- UTF-8 BOM: `utf-8-sig`
- GB 2312: `gb2312`

|                        |    Platform     |       UTF-8        |     UTF-8 BOM      |      GB 2312       |
| :--------------------: | :-------------: | :----------------: | :----------------: | :----------------: |
|      Foobar 2000       |     Windows     |        :x:         | :heavy_check_mark: | :heavy_check_mark: |
|        DeaDBeeF        | Linux / Android | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
|          VOX           |   macOS / iOS   | :heavy_check_mark: | :heavy_check_mark: |        :x:         |
| Synology Audio Station |   NAS / Linux   | :heavy_check_mark: | :heavy_check_mark: |        :x:         |

> Note: DeaDBeeF on Linux could support CUE file in encoding GB 2312 by enabling `Chinese CP 936 detection and recording` in the settings.
> However, DeaDBeeF on macOS still cannot support GB 2312 even if we enable the setting.
> DeadDBeeF on Android has not been tested yet.

> Note: VOX on iOS has not been tested yet.

### Newline

|                        |    Platform     |     Unix (LF)      |   Windows (CRLF)   |
| :--------------------: | :-------------: | :----------------: | :----------------: |
|      Foobar 2000       |     Windows     | :heavy_check_mark: | :heavy_check_mark: |
|        DeaDBeeF        | Linux / Android | :heavy_check_mark: | :heavy_check_mark: |
|          VOX           |   macOS / iOS   | :heavy_check_mark: | :heavy_check_mark: |
| Synology Audio Station |   NAS / Linux   | :heavy_check_mark: | :heavy_check_mark: |

## License

[GNU General Public License v3.0](https://github.com/yinyanghu/cuefix/blob/master/LICENSE)
