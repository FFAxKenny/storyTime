import os
import re


def enum(*args):
    enums = dict(zip(args, range(len(args))))
    enums['names'] = args
    return type('enum', (), enums)

def listdir(path):
    """
    Return a sorted list of the full paths of the entries in the 
    current directory.
    
    `path` -- path of directory or filename in directory to list
    """
    if os.path.isfile(path):
        path = os.path.split(path)[0]
    return sorted([os.path.join(path, x) for x in os.listdir(path)])

def get_latest_version(dirname):
    """Return the latest version of the given filename"""
    VERS_RE = re.compile('(?P<vers>[v|V]\d+)')
    try:
        filename = os.path.join(dirname, os.listdir(dirname)[0])
        dir_, base = os.path.split(filename)
        pat = VERS_RE.sub('[v|V]\d{3}', base.replace('.', '\.'))
        matches = [x for x in os.listdir(dir_) if re.match(pat, x) and os.path.isfile(os.path.join(dir_, x))]
        return sorted(matches)[-1]
    except:
        return None