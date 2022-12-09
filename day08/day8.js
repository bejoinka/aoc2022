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

function lookAround() {
    return [
        [1, 0], // look down
        [-1, 0], // look up
        [0, -1], // look left
        [0, 1], // look right
    ]
}

class Trees {
    area
    height
    width
    constructor(area) {
        this.area = area
        this.height = area.length
        this.width = area[0].length
    }

    atEdge(pos) {
        if (
            pos[0] == 0 ||
            pos[1] == 0 ||
            pos[0] == this.height - 1 ||
            pos[1] == this.width - 1
        ) {
            return true
        }
        return false
    }

    numberOfTreesWithAView() {
        const views = this.area.map((row, rowIdx) => {
            return row.map((_, colIdx) => {
                return this.canSeeEdge({x: colIdx, y: rowIdx})
            })
        })
        return views.flat().reduce((tot, cur) => tot + cur, 0)
    }

    mostScenicTree() {
        const views = this.area.map((row, rowIdx) => {
            return row.map((_, colIdx) => {
                return this.treeTopView({x: colIdx, y: rowIdx})
            })
        })
        return Math.max(...views.flat())
    }

    canSeeEdge(coords) {
        let treeHeight = this.area[coords.y][coords.x]
        let canSee = false
        if (this.atEdge([coords.x, coords.y])) { return true }
        lookAround().forEach(direction => {
            let pos = [coords.x, coords.y]
            if (canSee) { return }
            while (!this.atEdge(pos)) {
                pos[0] += direction[0]
                pos[1] += direction[1]
                const nextTree = this.area[pos[1]][pos[0]]
                if (treeHeight <= nextTree) {
                    break
                }
                if (this.atEdge(pos)) {
                    canSee = true
                }
            }
        })
        return canSee
    }

    treeTopView(coords) {
        const view = [0,0,0,0]  // down, up, left, right
        let treeHeight = this.area[coords.y][coords.x]
        if (this.atEdge([coords.x, coords.y])) { return 0 }
        lookAround().forEach((direction, dirIdx) => {
            let pos = [coords.x, coords.y]
            while (!this.atEdge(pos)) {
                pos[0] += direction[0]
                pos[1] += direction[1]
                view[dirIdx]++
                const nextTree = this.area[pos[1]][pos[0]]
                if (treeHeight <= nextTree) {
                    break
                }
            }
        })
        return view.reduce((tot, cur) => tot * cur, 1)
    }

}


function part1(input) {
    const rows = input.trim().split('\n')
    const forest = new Trees(rows.map(num => num.split('').map(i => Number(i))))
    return forest.numberOfTreesWithAView()
}

function part2(input) {
    const rows = input.trim().split('\n')
    const forest = new Trees(rows.map(num => num.split('').map(i => Number(i))))
    return forest.mostScenicTree()
}

module.exports = {
    run
}