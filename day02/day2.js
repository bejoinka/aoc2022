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

function RPS(val) {
    let theVal
    switch (val) {
        case "A":
        case "X": {
            theVal = 1
            break
        }
        case "B":
        case "Y": {
            theVal = 2
            break
        }
        case "C":
        case "Z": {
            theVal = 3
            break
        }
    }
    return theVal
}

function matchup(round) {
    const [opp, you] = round.split(" ").map(s => RPS(s))
    if (you - opp == 1 || you - opp + 3 == 1) {
        return you + 6
    } else if (you == opp) {
        return you + 3
    } else {
        return you
    }
}

function matchup2(round) {
    const [opp, you] = round.split(" ").map(s => RPS(s))
    let yourScore
    switch (you) {
        case 1: {
            yourScore = opp - 1
            if (yourScore == 0) {
                yourScore = 3
            }
            break
        }
        case 2: {
            yourScore = opp + 3
            break
        }
        case 3: {
            yourScore = opp + 7
            if (yourScore == 10) {
                yourScore = 7
            }
            break
        }
    }
    return yourScore
}

function part1(input) {
    const matches = input.trim().split('\n')
    return matches.reduce((tot, cur) => { return tot + matchup(cur) }, 0)
}

function part2(input) {
    const matches = input.trim().split('\n')
    return matches.reduce((tot, cur) => { return tot + matchup2(cur) }, 0)
}

module.exports = {
    run
}