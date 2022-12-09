const aoc = require('./day7')

const input = `\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
`
describe('day7', () => {
    test('part1', () => {
        expect(aoc.run({part: 1, input})).toStrictEqual(95437)
    })
    test('part2', () => {
        expect(aoc.run({part: 2, input})).toStrictEqual(24933642)
    })
})