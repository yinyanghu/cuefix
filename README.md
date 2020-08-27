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

### Encoding

Please use the following encoding name in `cuefix`:

- UTF-8: `utf-8`
- UTF-8 BOM: `utf-8-sig`
- GB 2312: `gb2312`

|                        |    Platform     | UTF-8 |     UTF-8 BOM      |      GB 2312       |
| :--------------------: | :-------------: | :---: | :----------------: | :----------------: |
|      Foobar 2000       |     Windows     |  :x:  | :heavy_check_mark: | :heavy_check_mark: |
|        DEADBEEF        | Linux / Android |       |                    |                    |
|          VOX           |   macOS / iOS   |       |                    |                    |
| Synology Audio Station |   NAS / Linux   |       |                    |                    |  |

### Newline

|                        |    Platform     |     Unix (LF)      |   Windows (CRLF)   |
| :--------------------: | :-------------: | :----------------: | :----------------: |
|      Foobar 2000       |     Windows     | :heavy_check_mark: | :heavy_check_mark: |
|        DEADBEEF        | Linux / Android |                    |                    |
|          VOX           |   macOS / iOS   |                    |                    |
| Synology Audio Station |   NAS / Linux   |                    |                    |

## License

[GNU General Public License v3.0](https://github.com/yinyanghu/cuefix/blob/master/LICENSE)
