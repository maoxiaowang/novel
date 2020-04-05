import re


def get_filename_extension(filename):
    res = re.findall(r'^.*\.(.*)$', filename)
    extension = res[0] if res else None
    return extension


def calc_word_count(content):
    return len(re.sub(r'[^\S]+', '', content))
