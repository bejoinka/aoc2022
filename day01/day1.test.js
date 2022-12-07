const aoc = require('./day1')

const input = `\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
`
describe('day1', () => {
    test('part1', () => {
        expect(aoc.run({part: 1, input})).toStrictEqual(24000)
    })
    test('part2', () => {
        expect(aoc.run({part: 2, input})).toStrictEqual(45000)
    })
})