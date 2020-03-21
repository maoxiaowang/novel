import re


def get_filename_extension(filename):
    res = re.findall(r'^.*\.(.*)$', filename)
    extension = res[0] if res else None
    return extension
