const aoc = require('./day4')

const input = `\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
`
describe('day4', () => {
    test('part1', () => {
        expect(aoc.run({part: 1, input})).toStrictEqual(2)
    })
    test('part2', () => {
        expect(aoc.run({part: 2, input})).toStrictEqual(4)
    })
})