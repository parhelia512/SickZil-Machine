'''
Utils for File Processing
'''
import os
import re
from pathlib import PurePosixPath, Path


def children(dirpath):
    ''' Return children file path list of `dirpath` '''
    parent = Path(dirpath)
    print('dirpath', dirpath)
    print('parent', parent)
    print('children?', list(parent.iterdir()))
    return list(map(
        lambda child_path: str(parent / child_path.name),
        parent.iterdir()
    ))

def descendants(root_dirpath):
    ''' Return descendants file path list of `root_dirpath` ''' 
    fpaths = []
    it = os.walk(root_dirpath)
    for root,dirs,files in it:
        for path in map(lambda name:PurePosixPath(root) / name,files):
            fpaths.append(str(path))
    return fpaths

def human_sorted(iterable):
    ''' Sorts the given iterable in the way that is expected. '''
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(iterable, key = alphanum_key)

def write_text(path, text, mode=0o777, exist_ok=False):
    path = Path(PurePosixPath(path))
    os.makedirs(path.parent, mode, exist_ok)
    path.write_text(text)

import funcy as F
@F.autocurry
def replace1(old, new, path):
    parts = list(Path(path).parts) # NOTE: because of set_in implementation..
    idx = parts.index(old)
    return str(Path(*F.set_in(parts, [idx], new)))


if __name__ == '__main__':
    for x in Path('.').iterdir():
        print(Path('.') / x)
    print('----')
    print(children('.'))
    print('----')
    print(descendants('.'))
    print('----')
    assert replace1('a','n', 'asd/ab/a') == 'asd/ab/n'
    assert replace1('asd','new', '//asd/ab/a') == '//new/ab/a'
    unittest.main()
