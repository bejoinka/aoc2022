const path = require("path")

// options should be {part: 1 | 2, input: string}
function run(options) {
    console.debug(`running ${path.basename(__filename)}, part ${options.part}`)
    if (options.part == 1) {
        const val = part1(options.input)
        console.log(val)
        return val
    } else if (options.part == 2) {
        const val = part2(options.input)
        console.log(val)
        return val
    }
}

function getCharVal(s) {
    if (s === s.toLowerCase()) {
        return s.charCodeAt() - 'a'.charCodeAt() + 1
    } else {
        return s.charCodeAt() - 'A'.charCodeAt() + 27
    }
}

function getCommonChars(...vals) {
    for (char of vals[0])  {
        if (vals.every(v => v.includes(char))) {
            return getCharVal(char)
        }
    }
    return 0
}

function part1(input) {
    const rucksacks = input.trim().split('\n')
    return rucksacks.reduce((tot, sack) => {
        pieceLen = sack.length / 2
        const v = getCommonChars(
            sack.slice(0, pieceLen),
            sack.slice(pieceLen, undefined),
        )
        return v + tot
    }, 0)
}

function part2(input) {
    const rucksacks = input.trim().split('\n')
    let tot = 0
    for (let i = 1; i <= rucksacks.length / 3; i ++) {
        const slice = rucksacks.slice(i*3 - 3, i*3)
        tot += getCommonChars(...slice)
    }
    return tot
}

module.exports = {
    run
}