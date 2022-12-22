"""
This is the ugliest of all of my aoc. I'll come back to it, but I bet
it's possible to solve in a formula of some sort rather than using
any sort of traversal function. In other words, there are likely a
group of heuristics that can win.
"""

from __future__ import annotations

import re
import collections
import math
from dataclasses import dataclass
import argparse
import os.path

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from dataclasses import dataclass

@dataclass
class Blueprint:
    ore: int
    clay: int
    obsidian: tuple[int, int] # ore and clay
    geode: tuple[int, int]  # ore and obsidian

    def __str__(self):
        return f"###### BLUEPRINT ######\n Costs:\n - Ore: {self.ore}\n - Clay: {self.clay}\n" + \
        f" - Obsidian: {self.obsidian} (Ore, Clay)\n - Geode: {self.geode} (Ore, Obsidian)"

@dataclass(frozen=True, eq=True)
class Cache:
    ore: int
    clay: int
    obsidian: int
    geode: int


    def can_build(self, itm: str, bp: Blueprint) -> bool:
        match itm:
            case "ore":
                return self.ore >= bp.ore
            case "clay":
                return self.ore >= bp.clay
            case "obsidian":
                return self.ore >= bp.obsidian[0] and self.clay >= bp.obsidian[1]
            case "geode":
                return self.ore >= bp.geode[0] and self.obsidian >= bp.geode[1]
            case _:
                raise ValueError("itm should be ore, clay, obsidian, or geode")

@dataclass(frozen=True, eq=True)
class Robots:
    ore: int
    clay: int
    obsidian: int
    geode: int

    def add_to_cache(self, cache: Cache) -> Cache:
        return Cache(
            ore=cache.ore + self.ore,
            clay=cache.clay + self.clay,
            obsidian=cache.obsidian + self.obsidian,
            geode=cache.geode + self.geode,
        )

    def __repr__(self):
        return f"<Robots: Ore: {self.ore}, Clay: {self.clay}, Obsidian: {self.obsidian}, geodes: {self.geode}>"

def build(itm: str, robots: Robots, cache: Cache, bp: Blueprint) -> tuple[Robots, Cache]:
    match itm:
        case "ore":
            return (
                Robots(
                    ore=robots.ore + 1,
                    clay=robots.clay,
                    obsidian=robots.obsidian,
                    geode=robots.geode,
                ),
                Cache(
                    ore=cache.ore - bp.ore,
                    clay=cache.clay,
                    obsidian=cache.obsidian,
                    geode=cache.geode,
                ),
            )
        case "clay":
            return (
                Robots(
                    ore=robots.ore,
                    clay=robots.clay + 1,
                    obsidian=robots.obsidian,
                    geode=robots.geode,
                ),
                Cache(
                    ore=cache.ore - bp.clay,
                    clay=cache.clay,
                    obsidian=cache.obsidian,
                    geode=cache.geode,
                ),
            )
        case "obsidian":
            return (
                Robots(
                    ore=robots.ore,
                    clay=robots.clay,
                    obsidian=robots.obsidian + 1,
                    geode=robots.geode,
                ),
                Cache(
                    ore=cache.ore - bp.obsidian[0],
                    clay=cache.clay - bp.obsidian[1],
                    obsidian=cache.obsidian,
                    geode=cache.geode,
                ),
            )
        case "geode":
            return (
                Robots(
                    ore=robots.ore,
                    clay=robots.clay,
                    obsidian=robots.obsidian,
                    geode=robots.geode + 1,
                ),
                Cache(
                    ore=cache.ore - bp.geode[0],
                    clay=cache.clay,
                    obsidian=cache.obsidian - bp.geode[1],
                    geode=cache.geode,
                ),
            )
        case _:
            raise ValueError("itm should be ore, clay, obsidian, or geode")


REGEX = re.compile(r"Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")


def compute(s: str, minutes: int = 32) -> int:
    ls = s.strip().splitlines()
    matches = [REGEX.findall(b) for b in ls]
    blueprints = [Blueprint(int(m[0][0]), int(m[0][1]), (int(m[0][2]), int(m[0][3])), (int(m[0][4]), int(m[0][5]))) for m in matches]
    geodes = []
    best = []
    for i, bp in enumerate(blueprints[0:3]):
        best.append({'finish': 0, 'minutes': [0 for _ in range(1, minutes + 1)]})
        queue = collections.deque()
        SEEN = set()
        print(bp)
        # robots = Robots(ore=1, clay=0, obsidian=0, geode=0)
        # cache = Cache(ore=0, clay=0, obsidian=0, geode=0)
        r = (1, 0, 0, 0)
        m = (0, 0, 0, 0)
        cost = bp # (bp.ore, bp.clay, bp.obsidian, bp.geode)
        queue.append((*r, *m, minutes))
        while queue:
            itm = queue.popleft()
            ro, rc, rb, rg, mo, mc, mb, mg, t = itm
            if itm in SEEN:
                continue
            if t == 0:
                best[i]['finish'] = max(best[i]['finish'], mg)
                continue
            if mg < best[i]['minutes'][minutes-t]:
                continue
            best[i]['minutes'][minutes-t] = max(best[i]['minutes'][minutes-t], mg)
            SEEN.add(itm)
            
            if len(SEEN) % 1000000 == 0:
                print((i, mg, len(SEEN)))
            # do nothing
            queue.append((ro, rc, rb, rg, mo+ro, mc+rc, mb+rb, mg+rg, t-1))

            # optimizations
            max_ore = max(cost.ore, cost.clay, cost.obsidian[0], cost.geode[0])
            max_clay = cost.obsidian[1]
            max_obs = cost.geode[1]
            if ro > max_ore or rc > max_clay or rb > max_obs:
                continue
            # if we have excess mats given max spend until the end
            mo = max(mo - (max_ore - ro) * t, mo)
            mc = max(mc - (max_clay - rc) * t, mc)
            mb = max(mb - (max_obs - rb) * t, mb)

            if mo >= cost.ore:
                queue.append(
                    (ro + 1, rc, rb, rg, mo - cost.ore + ro, mc + rc, mb + rb, mg + rg, t - 1)
                )
            if mo >= cost.clay:
                queue.append(
                    (ro, rc + 1, rb, rg, mo - cost.clay + ro, mc + rc, mb + rb, mg + rg, t - 1)
                )
            if mo >= cost.obsidian[0] and mc >= cost.obsidian[1]:
                queue.append(
                    (ro, rc, rb + 1, rg, mo - cost.obsidian[0] + ro, mc - cost.obsidian[1] + rc, mb + rb, mg + rg, t - 1)
                )
            if mo >= cost.geode[0] and mb >= cost.geode[1]:
                queue.append(
                    (ro, rc, rb, rg + 1, mo - cost.geode[0] + ro, mc + rc, mb - cost.geode[1] + rb, mg + rg, t - 1)
                )
            # build a robot
            # for itm in ["ore", "clay", "obsidian", "geode"]:
            #     if cache.can_build(itm, bp):
            #         r, c = build(itm, robots, robots.add_to_cache(cache), bp)
            #         print(r, c, t)
            #         queue.append((r, c, t - 1))

        # geodes.append(cache.geode)
    # return sum((i * val) for i, val in zip(range(1, len(geodes) + 1), geodes))
    print(best)
    # return 0
    return sum(b['finish'] for b in best)

INPUT_S = '''\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''
EXPECTED = 33


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