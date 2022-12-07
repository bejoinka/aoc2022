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

function isOverlap(s) {
    [s1, s2] = s.split(',').map(rng => {
        const [lo, hi] = rng.split('-').map(n => new Number(n))
        const v = new Array(hi - lo + 1).fill(0).map((_, idx) => lo + idx)
        return new Set(v)
    })
    combined = new Set([...s1, ...s2])
    if (s1.size === combined.size || s2.size === combined.size) {
        return true
    } else {
        return false
    }
}

function isPartialOverlap(s) {
    [s1, s2] = s.split(',').map(rng => {
        const [lo, hi] = rng.split('-').map(n => new Number(n))
        const v = new Array(hi - lo + 1).fill(0).map((_, idx) => lo + idx)
        return new Set(v)
    })
    combined = new Set([...s1, ...s2])
    if (combined.size < s1.size + s2.size) {
        return true
    } else {
        return false
    }
}


function part1(input) {
    const pairs = input.trim().split('\n')
    return pairs.reduce((tot, pair) => {
        if (isOverlap(pair)) {
            return tot + 1
        } else {
            return tot
        }
    }, 0)
}

function part2(input) {
    const pairs = input.trim().split('\n')
    return pairs.reduce((tot, pair) => {
        if (isPartialOverlap(pair)) {
            return tot + 1
        } else {
            return tot
        }
    }, 0)
}

module.exports = {
    run
}