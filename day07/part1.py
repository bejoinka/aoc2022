from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from enum import Enum

class TermCmd(Enum):
    NONE = None
    LIST = "list"

# class Dir(int):
#     contents: dict[str, Dir] = dict()
#     def __init__(self, val):
#         self.val = val
    
#     def list_contents(self, recursive: bool = False):
#         if recursive:
#             d = dict()
#             for k, v in self.contents.items():
#                 if type(v) == Dir:
#                     d[k] = v.list_contents(recursive)
#                 else:
#                     d[k] = v
#             return d
#         else:
#             return self.contents

#     def add_file_or_dir(self, file_or_dir: str):
#         val, name = file_or_dir.split()
#         if val == 'dir':
#             self.contents[name] = Dir(0)
#         else:
#             self.contents[name] = Dir(val)

#     def __sum__(self):
#         return sum(self.contents.values())


class Drive:
    fs = {'/': []}
    current_loc = "/"
    # current_action: TermCmd = TermCmd.NONE

    @property
    def current_dir(self):
        return self.fs[self.current_loc]
    
    def __init__(self):
        pass

    def lst(self, itm: str):
        d = self.fs.get(self.current_loc, list())
        d.append(itm.split())
        self.fs[self.current_loc] = d

    def chg_loc(self, d):
        if d == '/':
            self.current_loc = '/'
        elif d == '..':
            self.current_loc = "/".join(self.current_loc.split('/')[:-2]) + "/"
        else:
            self.current_loc += f"{d}/"

    def calc_size(self, d):
        tot = 0
        for f in self.fs[d]:
            if f[0] == 'dir':
                rec_dir = f"{d}{f[1]}/"
                tot += self.calc_size(rec_dir)
            else:
                tot += int(f[0])
        return tot

    def calc_total(self, d: dict):
        tot = 0
        for k, v in d.items():
            if k == '..':
                continue
            if type(v) == dict:
                tot += self.calc_total(d[k])
            else:
                tot += v
        return tot
    
    # def act(self, cmd: str):

    #     # first part of cmd is shell
    #     match cmd.split()[1:]:
    #         case ["ls"]:
    #             # self.current_action = TermCmd.LIST
    #             pass
    #         case ["cd", d]:
    #             self.chg_loc(d)
    
    # def ingest(self, vals: str):
    #     size, filename = vals.split()
    #     if size == 'dir':
    #         self.current_dir[filename] = self.current_dir.get(filename, {'..': self.current_dir})
    #     else:
    #         self.current_dir[filename] = int(size)
            


def compute(s: str) -> int:
    l = s.strip().split('\n')
    drive = Drive()
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

    # I was working on a system to hold in dicts but ran into trouble and put it down.
    # import re
    # gen = re.finditer(r"([A-Za-z0-9 $./]+)", s)
    # try:
    #     while True:
    #         ln = next(gen)
    #         if ln[0].startswith("$"):
    #             fs.act(ln[0].strip())
    #         else:
    #             fs.ingest(ln[0].strip())
    # except StopIteration:
    #     print('finished parsing')
    # total_size = fs.calc_total(fs.drive['/'])
    # return total_size

    sum_vals = 0
    for k in drive.fs.keys():
        val = drive.calc_size(k)
        if val < 100000:
            sum_vals += val
            # sum_vals += drive.calc_size(k)
    return sum_vals


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
EXPECTED = 95437


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
