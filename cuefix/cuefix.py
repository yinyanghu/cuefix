import chardet
import logging
import os
import re
import time

log = logging.getLogger('cuefix')
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))


def scan_folder():
    pass


NEWLINE_CHAR = {
    'windows': b'\r\n',
    # must check windows format before unix format, since '\n' is a substring of '\r\n'
    'unix': b'\n',
}
AUDIO_FILE_RE = re.compile(r'FILE "(.*)" WAVE')


class CueFile:
    def __init__(self, filepath):
        self.filepath = os.path.abspath(filepath)
        self.directory, self.filename = os.path.split(self.filepath)
        with open(filepath, 'rb') as f:
            self.byte_str = f.read()
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

    def detect_file_encoding(self):
        encoding = chardet.detect(self.byte_str)
        if encoding['confidence'] < 0.75:
            raise Exception('Cannot detect encoding of file {}: {}'.format(
                self.filename, encoding))
        return encoding['encoding'].lower()

    def detect_newline(self):
        for sys in NEWLINE_CHAR:
            if NEWLINE_CHAR[sys] in self.byte_str:
                return sys
        raise Exception(
            'cannot detect newline character of file {}'.format(self.filename))

    def extract_audio_file(self):
        cue_str = self.byte_str.decode(self.encoding)
        result = AUDIO_FILE_RE.search(cue_str)
        if result == None:
            raise Exception('cannot extract audio file name')
        return result.group(1)


class CueFix:
    def __init__(self, cue, backup=True, dryrun=False, verbose=False):
        self.cue = cue
        self.backup = backup
        self.dryrun = dryrun
        self.verbose = verbose

    def fix(self, encoding='utf-8-sig', newline='unix'):
        current_encoding = self.cue.encoding

        cue_byte_str = self.cue.byte_str
        file_changed = False

        if encoding is not None:
            cue_byte_str, c = self.convert_encoding(cue_byte_str, encoding)
            current_encoding = encoding
            file_changed = file_changed or c
        elif self.verbose:
            log.info('converting encoding is skipped')

        if newline is not None:
            cue_byte_str, c = self.convert_newline(cue_byte_str, newline)
            file_changed = file_changed or c
        elif self.verbose:
            log.info('converting newline is skipped')

        cue_byte_str, c = self.fix_audio_file(cue_byte_str, current_encoding)
        file_changed = file_changed or c

        if self.dryrun:
            if self.verbose:
                log.info('just a dry-run')
            print(cue_byte_str.decode(encoding))
            return

        if file_changed:
            cue_filename = self.cue.filename
            dir = self.cue.directory

            if self.backup:
                backup_cue_filename = cue_filename + '.backup'

                if not os.path.exists(backup_cue_filename):
                    if self.verbose:
                        log.info('backup cue file {} to {}'.format(
                            cue_filename, backup_cue_filename))
                else:
                    if self.verbose:
                        log.info('found previous backup cue file')
                    timestamp = str(int(time.time() * 10000))
                    backup_cue_filename = cue_filename + '.' + timestamp + '.backup'

                os.rename(os.path.join(dir, cue_filename),
                          os.path.join(dir, backup_cue_filename))

            with open(os.path.join(dir, cue_filename), 'wb') as f:
                if self.verbose:
                    log.info(
                        'write the fixed cue into file {}'.format(cue_filename))
                f.write(cue_byte_str)
        elif self.verbose:
            log.info('everything looks good!')

    def convert_encoding(self, byte_str, encoding='utf-8-sig'):
        if self.cue.encoding == encoding:
            if self.verbose:
                log.info(
                    'no need to convert encoding, it is {} already'.format(encoding))
            return byte_str, False
        # print(self.cue.byte_str)
        # s = byte_str.decode(self.cue.encoding)
        # print(s)
        # t = s.encode(encoding)
        # print(t)
        if self.verbose:
            log.info("convert encoding from {} to {}".format(
                self.cue.encoding, encoding))
        return byte_str.decode(self.cue.encoding).encode(encoding), True

    def convert_newline(self, byte_str, newline='unix'):
        if self.cue.newline == newline:
            if self.verbose:
                log.info(
                    'no need to convert newline, it is {} format already'.format(newline))
            return byte_str, False
        if self.verbose:
            log.info('convert newline from {} to {} format'.format(
                self.cue.newline, newline))
        return byte_str.replace(
            NEWLINE_CHAR[self.cue.newline],
            NEWLINE_CHAR[newline]
        ), True

    def find_audio_file(self, directory, filename):
        audio_files = []
        for filename in os.listdir(directory):
            for ext in ['wav', 'flac', 'ape', 'tta']:
                if filename.endswith(ext):
                    audio_files.append(filename)

        if self.verbose:
            log.info('found candidate audio files: {}'.format(audio_files))

        if not audio_files:
            raise Exception(
                'cannot find any available audio file in directory {}'.format(directory))

        if len(audio_files) == 1:
            return audio_files[0]

        # TODO(yinyanghu): Design a smart matching algorithm.
        name = filename.rsplit('.', 1)[0]
        for filename in audio_files:
            if filename.startswith(name):
                return filename

        raise Exception(
            'more than one audio file candidates to be used to fix the cue file: {}', audio_files)

    def fix_audio_file(self, byte_str, encoding):
        audio_file = self.cue.audio_file
        dir = self.cue.directory

        audio_filepath = os.path.join(dir, audio_file)
        if os.path.exists(audio_filepath):
            if self.verbose:
                log.info('no need to fix, audio file {} exists in directory {}'.format(
                    audio_file, dir))
            return byte_str, False

        if self.verbose:
            log.info('cannot find audio file {} in directory {}'.format(
                audio_file, dir))
        new_audio_file = self.find_audio_file(dir, audio_file)
        if self.verbose:
            log.info('found audio file {}'.format(new_audio_file))

        return byte_str.decode(encoding).replace(audio_file, new_audio_file).encode(encoding), True
