const aoc = require('./day5')

const input = `\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
`
describe('day5', () => {
    test('part1', () => {
        expect(aoc.run({part: 1, input})).toStrictEqual("CMZ")
    })
    test('part2', () => {
        expect(aoc.run({part: 2, input})).toStrictEqual("MCD")
    })
})