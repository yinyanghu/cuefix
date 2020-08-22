import chardet
import os

def scan_folder():
    pass

class CueFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.directory, self.filename = os.path.split(filepath)
        with open(filepath, 'rb') as f:
            self.byte_str = f.read()
        self.encoding = 'not detected'

    def __str__(self):
        return '''Cue File Info:
    Name: {0}
    Directory: {1}
    Size: {2} bytes'''.format(self.filename, self.directory, len(self.byte_str))

    def fix(self):
      self.encoding = self.detect_file_encoding()
      print(self.encoding)

    def detect_file_encoding(self):
        encoding = chardet.detect(self.byte_str)
        if encoding['confidence'] < 0.75:
            raise ValueError('Cannot detect encoding of file {0}: {1}'.format(
                self.filename, encoding))
        return encoding['encoding']



def encoding_to_utf8(byte_str, filename):
    return byte_str


def newline_to_lf(filename):
    pass


cue = CueFile("/Users/jianliyyh/平等路.cue")
print(cue)
cue.fix()
