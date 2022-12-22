from __future__ import annotations

import re
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

    def modifier(self, nm):
        mod = {
            "ore": 1 / self.clay_to_ore,
            "clay": self.clay_to_ore,
            "obs": self.geode[1] * self.cost_obs,
        }
        return mod.get(nm)

    @property
    def modifier_ore(self):
        return self.ore

    @property
    def cost_c(self):
        return self.clay

    @property
    def cost_obs(self):
        return self.obsidian[0] + self.clay * self.obsidian[1]

    @property
    def cost_g(self):
        return self.geode[0] + self.cost_obs * self.geode[1]
        
    @property
    def clay_geode(self):
        return self.clay * self.obsidian[1]

    @property
    def ore_geode(self):
        return self.geode[0] + self.obsidian[0] * self.geode[1]

    @property
    def clay_to_ore(self):
        return self.clay_geode / self.ore_geode

    def __str__(self):
        return f"###### BLUEPRINT ######\n Costs:\n - Ore: {self.ore}\n - Clay: {self.clay}\n - Obsidian: {self.obsidian} (Ore, Clay)\n - Geode: {self.geode} (Ore, Obsidian)\n Modifiers:\n - Ore: {self.modifier('ore')}\n - Clay: {self.modifier('clay')}\n - Obsidian: {self.modifier('obs')}"

@dataclass
class Mats:
    ore: int
    clay: int
    obsidian: int
    geode: int

@dataclass
class Robots:
    ore: int = 1
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __repr__(self):
        return f"<Robots: Ore: {self.ore}, Clay: {self.clay}, Obsidian: {self.obsidian}, geodes: {self.geode}>"


def time_to_obsidian(bp: Blueprint, robots: Robots, cache: Mats):
    clay_needed = bp.obsidian[1] - cache.clay
    ore_needed = bp.obsidian[0] - cache.ore
    clay_days = math.ceil(clay_needed / robots.clay)

def time_to_clay(n: int, bp: Blueprint, robots: Robots, cache: Mats):
    clay_needed = n - cache.clay
    if clay_needed <= 0:
        return 0
    production_time = math.ceil(clay_needed / robots.clay)
    for i in range(production_time, robots.clay):
        t = bp.clay + (1 + robots.clay)
        production_time = min()
    return math.ceil()

# def value_of_geode(bp: Blueprint, robots: Robots, cache: Mats, days_left):
#     modifier = 1 # (1 + robots.geode) / robots.geode
#     value = bp.cost_g
#     return modifier * value * days_left
import copy
def value_of_obsidian(bp: Blueprint, robots: Robots, cache: Mats, days_left):
    """
    There's this issue called teh "time to geode"
    if buying something today pushes back my time to geode, that's bad.
    does time to geode next turn improve or worsen if i buy this thing?
    """
    time_with = geode_build_time(
        bp,
        Mats(
            ore=cache.ore - bp.obsidian[0],
            clay=cache.clay - bp.obsidian[1],
            obsidian=cache.obsidian,
            geode=cache.geode
        ),
        Robots(
            ore=robots.ore,
            clay=robots.clay,
            obsidian=robots.obsidian + 1,
            geode=robots.geode
        )
    )
    time_without = geode_build_time(bp, cache, robots)
    if obsidian_build_time(bp, cache, robots) == 0 and time_without < time_with:
        modifier = 0
    else:
        modifier = 12/8 * bp.modifier('clay')
    value = bp.cost_obs
    return modifier * value * days_left


def value_of_clay(bp: Blueprint, robots: Robots, cache: Mats, days_left):
    time_with = geode_build_time(
        bp,
        Mats(
            ore=cache.ore - bp.clay,
            clay=cache.clay,
            obsidian=cache.obsidian,
            geode=cache.geode
        ),
        Robots(
            ore=robots.ore,
            clay=robots.clay + 1,
            obsidian=robots.obsidian,
            geode=robots.geode
        )
    )
    time_without = geode_build_time(bp, cache, robots)
    if obsidian_build_time(bp, cache, robots) == 0 and time_without < time_with:
        modifier = 0
    else:
        modifier = bp.modifier("clay")
    value = bp.cost_c
    return modifier * value * days_left

def value_of_ore(bp: Blueprint, robots: Robots, cache: Mats, days_left):
    modifier = bp.modifier("ore")
    value = 1
    return modifier * value * days_left

def ore_build_time(bp: Blueprint, cache: Mats, robots: Robots) -> int:
    return math.ceil((bp.ore - cache.ore) / robots.ore)

def clay_build_time(bp: Blueprint, cache: Mats, robots: Robots) -> int:
    return math.ceil((bp.clay - cache.ore) / robots.ore)

def obsidian_build_time(bp: Blueprint, cache: Mats, robots: Robots) -> int:
    if robots.clay == 0:
        return math.inf
    clay_needed = bp.obsidian[1]
    clay_have = cache.clay
    clay_days = math.ceil((clay_needed - clay_have) / robots.clay)
    ore_needed = bp.obsidian[0]
    ore_have = cache.ore
    ore_days = math.ceil((ore_needed - ore_have) / robots.ore)
    return max([clay_days, ore_days])

def geode_build_time(bp: Blueprint, cache: Mats, robots: Robots) -> int:
    if robots.obsidian == 0:
        return math.inf
    obsidian_needed = bp.geode[1]
    obsidian_have = cache.obsidian
    obs_days = math.ceil((obsidian_needed - obsidian_have) / robots.obsidian)
    ore_needed = bp.geode[0]
    ore_have = cache.ore
    ore_days = math.ceil((ore_needed - ore_have) / robots.ore)
    return max([obs_days, ore_days])
    

REGEX = re.compile(r"Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")

def buy_robot(cache: Mats, bp: Blueprint, robots: Robots, minutes_remaining: int):
    robots_to_add = {'geode': 0, 'obsidian': 0, 'clay': 0, 'ore': 0}
    values = {
        # "geode": value_of_geode(bp, robots, cache, minutes_remaining),
        "obs": value_of_obsidian(bp, robots, cache, minutes_remaining),
        "clay": value_of_clay(bp, robots, cache, minutes_remaining),
        "ore": value_of_ore(bp, robots, cache, minutes_remaining)
    }
    build_times = {
        # "geode": geode_build_time(bp, cache, robots),
        "obs": obsidian_build_time(bp, cache, robots),
        "clay": clay_build_time(bp, cache, robots),
        "ore": ore_build_time(bp, cache, robots)
    }
    print("\tvalues", values)
    print("\tbuild times", build_times)
    cost_val_fxn = {
        k: values[k] / math.exp(max(0, build_times[k])) for k in values.keys()
    }
    # print('cost/val', cost_val_fxn)
    sorted_val = sorted(cost_val_fxn.items(), key=lambda x: x[1], reverse=True)
    print('\tSORTED', sorted_val)
    # ALWAYS buy the geode
    if cache.ore >= bp.geode[0] and cache.obsidian >= bp.geode[1]:
        robots_to_add['geode'] += 1
        cache.ore -= bp.geode[0]
        cache.obsidian -= bp.geode[1]
    elif sorted_val[0][0] == 'obs' and cache.ore >= bp.obsidian[0] and cache.clay >= bp.obsidian[1]:
        robots_to_add['obsidian'] += 1
        cache.ore -= bp.obsidian[0]
        cache.clay -= bp.obsidian[1]
    elif sorted_val[0][0] == 'clay' and cache.ore >= bp.clay: # and robots.clay / robots.ore < bp.clay_to_ore:
        robots_to_add['clay'] += 1
        cache.ore -= bp.clay
    elif sorted_val[0][0] == 'ore' and cache.ore >= bp.ore:
        robots_to_add['ore'] += 1
        cache.ore -= bp.ore
    return robots_to_add

def compute(s: str) -> int:
    ls = s.strip().splitlines()
    matches = [REGEX.findall(b) for b in ls]
    blueprints = [Blueprint(int(m[0][0]), int(m[0][1]), (int(m[0][2]), int(m[0][3])), (int(m[0][4]), int(m[0][5]))) for m in matches]
    geodes = []
    for bp in blueprints:
        print(bp)
        # print("########### BLUEPRINT ############", "\n", "clay cost", bp.clay, "obsidian cost", bp.cost_obs, "geode cost", bp.cost_g, "clay_ore", bp.clay_to_ore)
        robots = Robots(ore=1, clay=0, obsidian=0, geode=0)
        cache = Mats(ore=0, clay=0, obsidian=0, geode=0)
        for i in range(1, 25):
            print(f'====== beginning {i} ======')
            robots_to_add = buy_robot(cache, bp, robots, 24 - i)
            cache.ore += robots.ore
            cache.clay += robots.clay
            cache.obsidian += robots.obsidian
            cache.geode += robots.geode
            for k, v in robots_to_add.items():
                attr = robots.__getattribute__(k)
                robots.__setattr__(k, attr + v)
            print('\t', robots)
            print('\tcache:', cache)
        geodes.append(cache.geode)
    print(geodes)
    return sum((i * val) for i, val in zip(range(1, len(geodes) + 1), geodes))

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