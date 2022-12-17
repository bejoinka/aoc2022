from __future__ import annotations
# from typing_extensions import Self

import heapq
import re
from dataclasses import dataclass
import argparse
import os.path
import itertools

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass
class Valve:
    name: str
    flow_rate: int
    paths: list[str]
    is_open: bool = False
    is_visited: bool = False

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def potential(self, minutes_remaining: int):
        if self.is_open:
            return 0
        return self.flow_rate * minutes_remaining



class Valves:
    valves: frozenset[Valve]
    minutes_remaining: int

    def __init__(self, valves, minutes_remaining: int = 30):
        self.valves = valves
        self.minutes_remaining = minutes_remaining

    def get(self, name: str):
        try:
            return next(filter(lambda v: v.name == name, self.valves))
        except StopIteration:
            raise ValueError(f'No valve exists with name {name}')

    def dist(self, v1s: str, v2s: str):
        """Calculated distance between two valves, using their names"""
        if v1s == v2s:
            return 0
        v1, v2 = self.get(v1s), self.get(v2s)
        queue: list[Valve] = list()
        for i, p in enumerate(v1.paths):
            heapq.heappush(queue, (1, i, set(), self.get(p)))
        while queue:
            val: tuple[int, int, set[Valve], Valve] = heapq.heappop(queue)
            dist, _, visited, v = val
            if v == v2:
                return dist
            else:
                visited.add(v)
                for pth in v.paths:
                    i += 1
                    if self.get(pth) not in visited:
                        heapq.heappush(queue, (dist + 1, i, visited, self.get(pth)))
        raise AssertionError('There should be no stranded valves')

regexp = re.compile(r"^Valve (?P<name>[A-Z]+) has flow rate=(?P<flow_rate>[0-9]+); \w+ \w+ to \w+ (?P<valves>[\w, ]+)$")


def compute(s: str) -> int:
    ls = s.strip().splitlines()
    closed_valves: set[Valve] = set()
    for ln in ls:
        match = regexp.match(ln.strip())
        vlv = Valve(name=match.group("name"), flow_rate=int(match.group("flow_rate")), paths=[p.strip() for p in match.group("valves").split(',')])
        closed_valves.add(vlv)
    v = Valves(closed_valves)
    interesting_valves = ["AA"] + [vv.name for vv in closed_valves if vv.flow_rate > 0]
    d = {}
    for a, b in itertools.combinations(interesting_valves, 2):
        d[(a, b)] = v.dist(a, b)
        d[(b, a)] = v.dist(a, b)
    flow_rates = {vv.name: vv.flow_rate for vv in closed_valves}
    queue = list()
    max_pressure = -1
    queue = [(0, 30, ('AA',),)]
    while queue:
        pressure, time, route = queue.pop()
        cur_valve = route[-1]
        if pressure > max_pressure:
            max_pressure = pressure
        for to_open in set(interesting_valves) - set(route):
            if d[(cur_valve, to_open)] < time:
                remaining_time = time - d[(cur_valve, to_open)] - 1
                queue.append((
                    pressure + flow_rates[to_open] * remaining_time,
                    remaining_time,
                    route + (to_open,)
                ))
    return max_pressure


INPUT_S = '''\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''
EXPECTED = 1651


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