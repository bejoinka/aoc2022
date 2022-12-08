const aoc = require('./day6')

const input = `\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
`
const input2 = `\
bvwbjplbgvbhsrlpgdmjqwftvncz
`
describe('day6', () => {
    test('part1', () => {
        expect(aoc.run({part: 1, input})).toStrictEqual(7)
        expect(aoc.run({part: 1, input: input2})).toStrictEqual(5)
    })
    test('part2', () => {
        expect(aoc.run({part: 2, input})).toStrictEqual(19)
        expect(aoc.run({part: 2, input: input2})).toStrictEqual(23)
    })
})