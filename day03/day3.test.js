const aoc = require('./day3')

const input = `\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
`
describe('day3', () => {
    test('part1', () => {
        expect(aoc.run({part: 1, input})).toStrictEqual(157)
    })
    test('part2', () => {
        expect(aoc.run({part: 2, input})).toStrictEqual(70)
    })
})