# CueFix

[![Python](https://img.shields.io/pypi/pyversions/cuefix.svg?style=plastic)](https://badge.fury.io/py/cuefix)
[![PyPI](https://badge.fury.io/py/cuefix.svg)](https://badge.fury.io/py/cuefix)

CueFix is simple command-line tool to fix CUE files which are popular in lossless audio / albums.

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

TODO(yinyanghu)

## CUE Formats Supported by Popular Media Players

### Media Players

- Foobar 2000
  - Windows (version 1.5.5)
- DeaDBeeF
  - Linux (version 1.8.4)
  - Android
  - Windows (unstable, nightly build)
  - macOS (unstable, nightly build)
- VOX
  - macOS (version 3.3.17)
  - iOS
- Synology Audio Station
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
