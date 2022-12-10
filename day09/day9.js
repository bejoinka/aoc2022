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

class Snake {
    arr
    tailpos
    constructor(length) {
        this.arr = new Array(length).fill().map(_ => [0,0])
        this.tailpos = new Set(['0,0'])
    }

    moveTail(i) {
        const [tail, head] = [this.arr[i], this.arr[i-1]]
        const dist = [head[0] - tail[0], head[1] - tail[1]] // xdist, yDist
        // if any xDist or yDist is 2 then we need to move the tail
        if (Math.max(...dist.map(v => Math.abs(v))) == 2) {
            const tailMove = dist.map(v => Math.abs(v) == 2 ? v / 2 : v)
            this.arr[i] = this.arr[i].map((c, i) => c + tailMove[i])
        }
    }
    
    move(d) {
        let shift // [x, y]
        switch (d) {
            case "R": {
                shift = [1, 0]
                break
            }
            case "U": {
                shift = [0, 1]
                break
            }
            case "L": {
                shift = [-1, 0]
                break
            }
            case "D": {
                shift = [0, -1]
                break
            }
        }
        this.arr[0] = this.arr[0].map((c, i) => c + shift[i])
        for (let i = 1; i < this.arr.length; i++) {
            this.moveTail(i)
        }
        const theTail = this.arr[this.arr.length - 1]
        this.tailpos.add(`${theTail[0]},${theTail[1]}`)
    }

}

function part1(input) {
    const instructions = input.trim().split('\n')
    const snake = new Snake(2)
    instructions.forEach(i => {
        const [direction, amount] = i.split(' ')
        for (let i = 0; i < amount; i++) {
            snake.move(direction)
        }
    })
    return snake.tailpos.size
}

function part2(input) {
    const instructions = input.trim().split('\n')
    const snake = new Snake(10)
    instructions.forEach(i => {
        const [direction, amount] = i.split(' ')
        for (let i = 0; i < amount; i++) {
            snake.move(direction)
        }
    })
    return snake.tailpos.size
}

module.exports = {
    run
}