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

function makeStacks(stacks) {
    const numberOfStacks = stacks[stacks.length - 1].replaceAll(" ", "").length
    const st = new Array(numberOfStacks).fill().map(a => [])
    for (s of stacks.slice(0, stacks.length - 1)) {
        for (i = 0; i < s.length / 4; i ++) {
            if (s[i * 4 + 1] != " ") {
                st[i].push(s[i * 4 + 1])
            }
        }
    }
    return st
}

function part1(input) {
    const [st, instructions] = input.split('\n\n').map(s => s.split('\n'))
    const stacks = makeStacks(st)
    instructions.forEach(instr => {
        const [num, src, dest] = instr.matchAll(/[0-9]/g)
        if (num == undefined) {
            return
        }
        for (i = 0; i < num[0]; i++) {
            stacks[dest[0] - 1].unshift(stacks[src[0] - 1].shift())
        }
    })
    return stacks.reduce((str, stack) => {
        str += stack[0]
        return str
    }, "")
}

function part2(input) {
    const [st, instructions] = input.split('\n\n').map(s => s.split('\n'))
    const stacks = makeStacks(st)
    instructions.forEach(instr => {
        const [num, src, dest] = instr.matchAll(/[0-9]/g)
        if (num == undefined) {
            return
        }
        const vals = []
        for (i = 0; i < num[0]; i++) {
            vals.push(stacks[src[0] - 1].shift())
        }
        stacks[dest[0] - 1].unshift(...vals)
    })
    return stacks.reduce((str, stack) => {
        str += stack[0]
        return str
    }, "")
}

module.exports = {
    run
}