const path = require("path")

// options should be {part: 1 | 2, input: string}
function run(options) {
    console.debug(`running ${path.basename(__filename)}, part ${options.part}`)
    if (options.part == 1) {
        console.log(part1(options.input))
    } else if (options.part == 2) {
        console.log(part2(options.input))
    }
}

function collectSums(elves) {
    const sums = elves.map(s => {
        return s.split('\n').reduce((acc, cur) => {return acc + new Number(cur)}, 0)
    })
    sums.sort((a, b) => b - a)
    return sums
}

function part1(input) {
    const elves = input.split('\n\n')
    return collectSums(elves)[0]
}

function part2(input) {
    const elves = input.split('\n\n')
    return collectSums(elves).slice(0, 3).reduce((tot, cur) => { return tot + cur }, 0)
}

module.exports = {
    run
}