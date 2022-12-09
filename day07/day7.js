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

/**
 * returns the filesystem in a record, where each folder is an entry, regardless of hierarchy
 * @param {string[]} input 
 * @returns {Record<string, Array<string | number>>}
 */
 function getFS(input) {
    const files = {"/": []}
    let curDir = ""
    input.forEach(ln => {
        if (ln.startsWith('$ cd')) {
            curDir = parseCurDir(ln, curDir)
        } else if (ln.startsWith('$ ls')) {
            return
        } else {
            if (files[curDir] == undefined) {
                files[curDir] = []
            }
            files[curDir].push(ln.split(' '))
        }
    })
    return files
}

function parseCurDir(ln, curDir) {
    switch (ln.slice(5, undefined)) {
        case '/': {
            curDir = '/'
            break
        }
        case '..': {
            curDir = curDir.replace(/\w+\/$/g, "")
            break
        }
        default: {
            curDir = curDir + ln.slice(5, undefined) + "/"
        }
    }
    return curDir
}

function getTotalSize(k, contents, files) {
    return contents.reduce((t, c) => {
        if (c[0] == 'dir') {
            const subDirName = k + c[1] + '/'
            return t + getTotalSize(
                ...Object.entries(files).filter(f => f[0] == subDirName)[0],
                files
            )
        }
        return t+Number(c[0])
    }, 0)
}

function part1(input) {
    const shell = input.trim().split('\n')
    const files = getFS(shell)
    const fileSizes = Object.entries(files).map(f => {
        return getTotalSize(...f, files)
    })
    return fileSizes.reduce((tot, cur) => {
        return cur < 100000 ? tot + cur : tot
    }, 0)
}

function part2(input) {
    const shell = input.trim().split('\n')
    const files = getFS(shell)
    const fileSizes = Object.entries(files).map(f => {
        return getTotalSize(...f, files)
    })
    return fileSizes.sort((a, b) => a - b).filter(f => f > 8381165)[0]
}

module.exports = {
    run
}