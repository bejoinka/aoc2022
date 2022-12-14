package main

import (
	"flag"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"

	support "jbb.dev/aoc2022/support_go"
)

var input string
var part int

type Tree struct {
	coord  support.Coord
	height int
}

type Forest struct {
	trees map[support.Coord]Tree
}

func (forest *Forest) HasClearView(tree Tree) bool {
	for _, dir := range support.Directions() {
		coords := support.Coord{X: tree.coord.X, Y: tree.coord.Y}
		for {
			if forest.OnPeriphery(coords) {
				return true
			}
			coords = support.Coord{X: coords.X + dir.X, Y: coords.Y + dir.Y}
			if forest.trees[coords].height >= tree.height {
				break
			}
		}
	}
	return false
}

func (forest *Forest) ScenicScore(tree Tree) int {
	visibility := []int{0, 0, 0, 0}
	for i, dir := range support.Directions() {
		coords := support.Coord{X: tree.coord.X, Y: tree.coord.Y}
		for {
			coords = support.Coord{X: coords.X + dir.X, Y: coords.Y + dir.Y}
			_, exists := forest.trees[coords]
			if !exists {
				break
			}
			visibility[i] += 1
			if tree.height <= forest.trees[coords].height {
				break
			}
		}
	}
	val := 1
	for _, v := range visibility {
		val = v * val
	}
	return val
}

func (forest *Forest) OnPeriphery(coord support.Coord) bool {
	length := int(math.Sqrt(float64(len(forest.trees))))
	return (coord.X == 0 || coord.Y == 0) || (coord.X == length-1 || coord.Y == length-1)
}

func ComputePart1(s string) int {
	lines := strings.Split(s, "\n")
	forest := Forest{map[support.Coord]Tree{}}
	for y, ln := range lines {
		for x, height := range strings.Split(ln, "") {
			ht, _ := strconv.Atoi(height)
			forest.trees[support.Coord{X: x, Y: y}] = Tree{support.Coord{X: x, Y: y}, ht}
		}
	}
	visible_trees := 0
	for _, tree := range forest.trees {
		if forest.HasClearView(tree) {
			visible_trees += 1
		}
	}
	return visible_trees
}

func ComputePart2(s string) int {
	lines := strings.Split(s, "\n")
	forest := Forest{map[support.Coord]Tree{}}
	for y, ln := range lines {
		for x, height := range strings.Split(ln, "") {
			ht, _ := strconv.Atoi(height)
			forest.trees[support.Coord{X: x, Y: y}] = Tree{support.Coord{X: x, Y: y}, ht}
		}
	}
	highest_visibility_score := 0
	for _, tree := range forest.trees {
		scenic_score := forest.ScenicScore(tree)
		if scenic_score > highest_visibility_score {
			highest_visibility_score = scenic_score
		}
	}
	return highest_visibility_score
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
	input = `30373
25512
65332
33549
35390
`
}
