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

function part1(input) {
    str = input.trim()
    let i = -1
    // str.split('').forEach((char, idx, arr) => {
    const strArr = str.split('')
    for (i = 3; i < strArr.length; i++) {
        if (new Set(strArr.slice(i - 3, i+1)).size == 4) {
            return i + 1
        }
    }
    return i
}

function part2(input) {
    str = input.trim()
    let i = -1
    const strArr = str.split('')
    for (i = 13; i < strArr.length; i++) {
        if (new Set(strArr.slice(i - 13, i+1)).size == 14) {
            return i + 1
        }
    }
    return i
}

module.exports = {
    run
}