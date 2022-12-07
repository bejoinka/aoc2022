const aoc = require('./day2')

const input = `\
A Y
B X
C Z
`
describe('day2', () => {
    test('part1', () => {
        expect(aoc.run({part: 1, input})).toStrictEqual(15)
    })
    test('part2', () => {
        expect(aoc.run({part: 2, input})).toStrictEqual(12)
    })
})