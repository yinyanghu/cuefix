import os

import pytest
from cuefix import CueFile, CueFix, fix, info

SUPPORT_CUE_DIR = 'tests/support_cue'
SUPPORT_CUE_FILE = {
    'GB2312-LF.cue': {'encoding': 'gb2312', 'newline': 'unix'},
    'GB2312-CRLF.cue': {'encoding': 'gb2312', 'newline': 'windows'},
    'UTF-8-BOM-LF.cue': {'encoding': 'utf-8-sig', 'newline': 'unix'},
    'UTF-8-BOM-CRLF.cue': {'encoding': 'utf-8-sig', 'newline': 'windows'},
    'UTF-8-LF.cue': {'encoding': 'utf-8', 'newline': 'unix'},
    'UTF-8-CRLF.cue': {'encoding': 'utf-8', 'newline': 'windows'},
}


def test_CueFile_detect_file_encoding():
    for filename in SUPPORT_CUE_FILE:
        filepath = os.path.join(SUPPORT_CUE_DIR, filename)
        cuefile = CueFile(filepath, interactive=False)
        enc = cuefile.detect_file_encoding()
        assert enc == SUPPORT_CUE_FILE[filename]['encoding']
