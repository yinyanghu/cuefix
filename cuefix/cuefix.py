import logging
import os
import re
import time

import chardet

log = logging.getLogger('cuefix')
log.setLevel(logging.WARNING)


NEWLINE_CHAR = {
    'windows': b'\r\n',
    # must check windows format before unix format, since '\n' is a substring of '\r\n'
    'unix': b'\n',
}
AUDIO_FILE_REGEX = re.compile(r'FILE "(.*)" WAVE')
AUDIO_FILE_EXTENSION = ['wav', 'flac', 'ape', 'tta', 'tak']
SUPPORT_ENCODING = ['gb2312', 'gbk', 'gb18030',
                    'utf-8', 'utf-8-sig', 'shift-jis']


def feedback():
    ans = input('Looks good? (y/n)')
    return ans.lower() in ['y', 'yes', 't', 'true', 'ok', 'okay']


class CueFile:
    def __init__(self, filepath, interactive=True):
        self.interactive = interactive
        self.filepath = os.path.abspath(filepath)
        self.directory, self.filename = os.path.split(self.filepath)
        with open(self.filepath, 'rb') as file:
            self.byte_str = file.read()
        self.encoding = self.detect_file_encoding()
        self.newline = self.detect_newline()
        self.audio_file = self.extract_audio_file()

    def __str__(self):
        return '''Cue File Info:
    Name: {}
    Directory: {}
    Size: {} bytes
    Encoding: {}
    Newline: {}
    Audio File: {}'''.format(self.filename, self.directory, len(self.byte_str),
                             self.encoding, self.newline, self.audio_file)

    def auto_detect_file_encoding(self):
        encoding = chardet.detect(self.byte_str)
        log.info('result of automatic detection: %s', encoding)
        enc = encoding['encoding']
        enc = enc.lower() if enc is not None else None
        if enc is None or encoding['confidence'] < 0.6:
            raise UnicodeError(
                'unknown' if enc is None else enc,
                self.byte_str, 0, len(self.byte_str),
                'cannot automatically detect encoding of file {}: {}'.format(
                    self.filename, encoding))
        decoded = self.byte_str.decode(encoding=enc, errors='strict')
        log.info('found encoding: %s', enc)
        if not self.interactive:
            return enc, encoding
        if enc in ['ascii', 'utf-8-sig']:
            log.info('woohoo! 100%% sure it is %s, skip prompt!', enc)
            return enc, encoding
        print(decoded)
        print('encoding: {}', enc)
        if feedback():
            return enc, encoding
        raise UnicodeError(
            'unknown', self.byte_str, 0, len(self.byte_str),
            'cannot automatically detect encoding of file {}: {}'.format(
                self.filename, encoding))

    def trial_and_error_detect_file_encoding(self):
        for enc in SUPPORT_ENCODING:
            try:
                decoded = self.byte_str.decode(encoding=enc, errors='strict')
                if not self.interactive:
                    log.info('found exact encoding: %s', enc)
                    return enc
                print(decoded)
                print('encoding: {}', enc)
                if feedback():
                    log.info('found exact encoding: %s', enc)
                    return enc
                raise UnicodeError(enc, self.byte_str, 0, len(self.byte_str),
                                   'failed on encoding {}'.format(enc))
            except UnicodeError:
                log.info('failed on encoding %s', enc)

        raise UnicodeError(
            'unknown',
            self.byte_str, 0, len(self.byte_str),
            'cannot use any support encodings to decode the cue file')

    def detect_file_encoding(self):
        try:
            enc, encoding = self.auto_detect_file_encoding()
            return enc
        except UnicodeError:
            log.info('cannot automatically detect encoding: %s', encoding)

        return self.trial_and_error_detect_file_encoding()

    def detect_newline(self):
        for sys in NEWLINE_CHAR:
            if NEWLINE_CHAR[sys] in self.byte_str:
                return sys
        raise Exception(
            'cannot detect newline character of file {}'.format(self.filename))

    def extract_audio_file(self):
        cue_str = self.byte_str.decode(self.encoding)
        result = AUDIO_FILE_REGEX.search(cue_str)
        if result is None:
            raise Exception('cannot extract audio file name')
        return result.group(1)


class CueFix:
    def __init__(self, cue, backup=True, dryrun=False):
        self.cue = cue
        self.backup = backup
        self.dryrun = dryrun

    def fix(self, encoding='utf-8-sig', newline='unix'):
        current_encoding = self.cue.encoding

        cue_byte_str = self.cue.byte_str
        file_changed = False

        if encoding is not None:
            cue_byte_str, changed = self.convert_encoding(
                cue_byte_str, encoding)
            current_encoding = encoding
            file_changed = file_changed or changed
        else:
            log.info('converting encoding is skipped')

        if newline is not None:
            cue_byte_str, changed = self.convert_newline(cue_byte_str, newline)
            file_changed = file_changed or changed
        else:
            log.info('converting newline is skipped')

        cue_byte_str, changed = self.fix_audio_file(
            cue_byte_str, current_encoding)
        file_changed = file_changed or changed

        decoded = cue_byte_str.decode(current_encoding)

        if self.dryrun:
            log.info('just a dry-run')
            return decoded

        if not file_changed:
            log.info('everything looks good!')
            return decoded

        cue_filename = self.cue.filename
        directory = self.cue.directory

        if self.backup:
            backup_cue_filename = cue_filename + '.backup'

            if not os.path.exists(backup_cue_filename):
                log.info('backup cue file %s to %s',
                         cue_filename, backup_cue_filename)
            else:
                log.info('found previous backup cue file')
                timestamp = str(int(time.time() * 10000))
                backup_cue_filename = cue_filename + '.' + timestamp + '.backup'

            os.rename(os.path.join(directory, cue_filename),
                      os.path.join(directory, backup_cue_filename))

        with open(os.path.join(directory, cue_filename), 'wb') as cue_file:
            log.info('write the fixed cue into file %s', cue_filename)
            cue_file.write(cue_byte_str)

        return decoded

    def convert_encoding(self, byte_str, encoding='utf-8-sig'):
        if self.cue.encoding == encoding:
            log.info('no need to convert encoding, it is %s already', encoding)
            return byte_str, False
        log.info("convert encoding from %s to %s", self.cue.encoding, encoding)
        return byte_str.decode(self.cue.encoding).encode(encoding), True

    def convert_newline(self, byte_str, newline='unix'):
        if self.cue.newline == newline:
            log.info('no need to convert newline, it is %s format already',
                     newline)
            return byte_str, False
        log.info('convert newline from %s to %s format',
                 self.cue.newline, newline)
        return byte_str.replace(
            NEWLINE_CHAR[self.cue.newline],
            NEWLINE_CHAR[newline]
        ), True

    def find_audio_file(self, directory, audio_file, cue_file):
        audio_files = []
        for filename in os.listdir(directory):
            for ext in AUDIO_FILE_EXTENSION:
                if filename.endswith(ext):
                    audio_files.append(filename)

        log.info('found candidate audio files: %s', audio_files)

        if not audio_files:
            raise Exception(
                'cannot find any available audio file in directory {}'.format(directory))

        if len(audio_files) == 1:
            return audio_files[0]

        # TODO(yinyanghu): Design a smart matching algorithm.
        for hint_f in [audio_file, cue_file]:
            name = hint_f.rsplit('.', 1)[0]
            for filename in audio_files:
                if filename.startswith(name):
                    return filename

        raise Exception(
            'more than one audio file candidates: {}'.format(audio_files))

    def fix_audio_file(self, byte_str, encoding):
        audio_file = self.cue.audio_file
        directory = self.cue.directory

        audio_filepath = os.path.join(directory, audio_file)
        if os.path.exists(audio_filepath):
            log.info('no need to fix, audio file %s exists in directory %s',
                     audio_file, directory)
            return byte_str, False

        log.info('cannot find audio file %s in directory %s',
                 audio_file, directory)
        new_audio_file = self.find_audio_file(
            directory, audio_file, self.cue.filename)
        log.info('found audio file %s', new_audio_file)

        return byte_str.decode(encoding).replace(audio_file, new_audio_file).encode(encoding), True


def fix(filepath,
        encoding='utf-8-sig',
        newline='unix',
        backup=True,
        dryrun=False,
        interactive=True):
    log.info('start fixing CUE file: %s', filepath)
    cue_file = CueFile(filepath, interactive)
    log.info(str(cue_file))
    fixed_cue = CueFix(cue_file, backup, dryrun).fix(encoding, newline)
    if dryrun:
        print(fixed_cue)


def info(filepath, interactive=True):
    log.info('start fixing CUE file: %s', filepath)
    print(CueFile(filepath, interactive))
