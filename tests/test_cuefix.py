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
FIXED_CUE_FILE = 'fixed.cue'


@pytest.mark.parametrize('filename', list(SUPPORT_CUE_FILE.keys()))
def test_CueFile_detect_file_encoding(filename):
    filepath = os.path.join(SUPPORT_CUE_DIR, filename)
    cuefile = CueFile(filepath, interactive=False)
    enc = cuefile.detect_file_encoding()
    assert enc == SUPPORT_CUE_FILE[filename]['encoding']


@pytest.mark.parametrize('filename', list(SUPPORT_CUE_FILE.keys()))
def test_CueFile_detect_file_newline(filename):
    filepath = os.path.join(SUPPORT_CUE_DIR, filename)
    cuefile = CueFile(filepath, interactive=False)
    newline = cuefile.detect_newline()
    assert newline == SUPPORT_CUE_FILE[filename]['newline']


FIXED_CUE = ''
with open(os.path.join(SUPPORT_CUE_DIR, FIXED_CUE_FILE), 'rb') as file:
    FIXED_CUE = file.read().decode('utf-8-sig')

@pytest.mark.parametrize('filename', list(SUPPORT_CUE_FILE.keys()))
def test_CueFix_fix(filename):
    filepath = os.path.join(SUPPORT_CUE_DIR, filename)
    output_cue = CueFix(
        CueFile(filepath, interactive=False), dryrun=True).fix()
    assert FIXED_CUE == output_cue
