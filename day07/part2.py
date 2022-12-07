from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class Drive:
    fs = {'/': []}
    current_dir = "/"
    def __init__(self):
        pass

    def lst(self, itm: str):
        d = self.fs.get(self.current_dir, list())
        d.append(itm.split())
        self.fs[self.current_dir] = d
    
    def chg_loc(self, d):
        if d == '/':
            self.current_dir = '/'
        elif d == '..':
            self.current_dir = "/".join(self.current_dir.split('/')[:-2]) + "/"
        else:
            self.current_dir += f"{d}/"

    def calc_size(self, d):
        tot = 0
        for f in self.fs[d]:
            if f[0] == 'dir':
                rec_dir = f"{d}{f[1]}/"
                tot += self.calc_size(rec_dir)
            else:
                tot += int(f[0])
        return tot


def compute(s: str) -> int:
    l = s.strip().split('\n')
    drive = Drive()
    in_list = False
    for ln in l:
        # no need to parse further, has to be part of ls
        if not ln.startswith('$'):
            if not in_list:
                print('how??')
            drive.lst(ln)
        
        # ls
        elif ln.startswith('$ ls'):
            in_list = True
        
        # cmd
        elif ln.startswith('$ cd'):
            in_list = False
            drive.chg_loc(ln[5:])
    val_tup = []
    for k in drive.fs.keys():
        val_tup.append(drive.calc_size(k))
    for t in sorted(val_tup):
        if t > 8381165:
            return t
    raise ValueError("did not find")


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 24933642


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
