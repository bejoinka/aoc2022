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
    let files = {"/": []}
    let cur_dir = ""
    const str = input.trim().split('\n')
    str.forEach(ln => {
        if (ln.startsWith('$ cd')) {
            switch (ln.slice(5, undefined)) {
                case '/': {
                    cur_dir = '/'
                    break
                }
                case '..': {
                    const d = cur_dir
                        .slice(0, cur_dir.length - 1)
                        .split('/')
                    cur_dir = d.slice(0, d.length - 1).reduce(tot, cur => tot + "/" + cur, "") + "/"
                    break
                }
                default: {
                    cur_dir = cur_dir + "/" + ln.slice(5, undefined)
                }
            }
            console.log_cur_dir
        } else if (ln.startsWith('$ ls')) {
            return
        } else {
            if (files[cur_dir] == undefined) {
                files[cur_dir] = []
            }
            files[cur_dir].push(ln.split(' '))
        }
    })
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