import chardet


def scan_folder():
    pass


def detect_file_encoding(byte_str, filename):
    encoding = chardet.detect(byte_str)
    if encoding['confidence'] < 0.75:
        raise ValueError('Cannot detect encoding of file {filename}: {encoding}'.format(
            filename=filename, encoding=encoding))
    return encoding['encoding']


def encoding_to_utf8(byte_str, filename):
    return byte_str.


def newline_to_lf(filename):
    pass
