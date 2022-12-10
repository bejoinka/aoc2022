const aoc = require('./day8')

const input = `\
30373
25512
65332
33549
35390
`
describe('day8', () => {
    test('part1', () => {
        expect(aoc.run({part: 1, input})).toStrictEqual(21)
    })
    test('part2', () => {
        expect(aoc.run({part: 2, input})).toStrictEqual(8)
    })
})