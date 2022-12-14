package main

import (
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"

	support "jbb.dev/aoc2022/support_go"
)

var input string
var input2 string
var part int

type Instruction struct {
	direction support.Coord
	number    int
}

type Snake struct {
	tail_coords map[support.Coord]bool
	coords      []support.Coord
}

func makeSnake(size int) Snake {
	coords := make([]support.Coord, size)
	for c := range coords {
		coords[c] = support.Coord{X: 0, Y: 0}
	}
	return Snake{
		tail_coords: map[support.Coord]bool{},
		coords:      coords,
	}
}

func (snake *Snake) Move(instruction Instruction) {
	for n := 0; n < instruction.number; n++ {
		snake.coords[0] = support.Coord{
			X: snake.coords[0].X + instruction.direction.X,
			Y: snake.coords[0].Y + instruction.direction.Y,
		}
		for i := range snake.coords[1:] {
			dif := support.DiffCoord(snake.coords[i+1], snake.coords[i])
			if support.AbsInt(dif.X) == 2 && support.AbsInt(dif.Y) == 2 {
				snake.coords[i+1] = support.AvgCoord(snake.coords[i], snake.coords[i+1])
			} else if support.AbsInt(dif.X) == 2 {
				snake.coords[i+1] = support.Coord{
					X: support.AvgCoord(snake.coords[i], snake.coords[i+1]).X,
					Y: snake.coords[i].Y,
				}
			} else if support.AbsInt(dif.Y) == 2 {
				snake.coords[i+1] = support.Coord{
					X: snake.coords[i].X,
					Y: support.AvgCoord(snake.coords[i], snake.coords[i+1]).Y,
				}
			}
		}
		// fmt.Println(snake.coords[len(snake.coords)-1])
		snake.tail_coords[snake.coords[len(snake.coords)-1]] = true
	}
}

func ParseInstruction(s string) Instruction {
	dir_map := map[string]support.Coord{
		"D": {X: 0, Y: 1},
		"U": {X: 0, Y: -1},
		"L": {X: -1, Y: 0},
		"R": {X: 1, Y: 0},
	}
	in := strings.Split(s, " ")
	num, _ := strconv.Atoi(in[1])
	return Instruction{
		direction: dir_map[in[0]],
		number:    num,
	}
}

func ComputePart1(s string) int {
	instructions := strings.Split(s, "\n")
	snake := makeSnake(2)
	for _, instr := range instructions {
		if instr == "" {
			break
		}
		instruction := ParseInstruction(instr)
		snake.Move(instruction)
	}
	return len(snake.tail_coords)
}

func ComputePart2(s string) int {
	instructions := strings.Split(s, "\n")
	snake := makeSnake(10)
	for _, instr := range instructions {
		if instr == "" {
			break
		}
		instruction := ParseInstruction(instr)
		snake.Move(instruction)
	}
	return len(snake.tail_coords)
}

func main() {
	flag.IntVar(&part, "part", 1, "part 1 or 2")
	flag.Parse()
	contents, err := os.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	input = string(contents)
	if part == 1 {
		fmt.Println(ComputePart1(input))
	} else {
		fmt.Println(ComputePart2(input))
	}
}

func init() {
	input = `R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
`
	input2 = `R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
`
}
