package main

import (
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
)

var input string
var part int

func makeStackMap(part1 []string) [][]string {
	stacks := strings.ReplaceAll(string(part1[len(part1)-1]), " ", "")
	numberOfStacks, _ := strconv.Atoi(string(stacks[len(stacks)-1]))

	// Build empty stackMap
	stackMap := [][]string{}
	for i := 0; i < numberOfStacks; i++ {
		stackMap = append(stackMap, make([]string, 0))
	}

	// Assign the letters to the stacks
	for row_no, l := range part1 {
		if row_no == len(part1)-1 {
			break
		}
		for i := 0; i < numberOfStacks; i++ {
			st := string(l[i*4+1])
			if st != " " {
				stackMap[i] = append(stackMap[i], st)
			}
		}
	}
	return stackMap
}

func ComputePart1(s string) string {
	parts := strings.Split(s, "\n\n")
	stackMap := makeStackMap(strings.Split(parts[0], "\n"))

	// Commence instructions
	instructions := strings.Split(parts[1], "\n")

	for _, instr := range instructions {
		ins := strings.Split(instr, " ")
		if len(ins) < 6 {
			continue
		}
		numLetters, _ := strconv.Atoi(ins[1])
		source, _ := strconv.Atoi(ins[3])
		dest, _ := strconv.Atoi(ins[5])
		for i := 0; i < numLetters; i++ {
			v := stackMap[source-1][0]
			// fmt.Println("moving v", v, "from source:", stackMap[source-1], "to dest:", stackMap[dest-1])
			stackMap[source-1] = stackMap[source-1][1:]
			stackMap[dest-1] = append([]string{v}, stackMap[dest-1]...)
		}
	}
	finalStr := ""
	for i := range stackMap {
		finalStr += stackMap[i][0]
	}

	return finalStr
}

func ComputePart2(s string) string {
	parts := strings.Split(s, "\n\n")
	stackMap := makeStackMap(strings.Split(parts[0], "\n"))

	// Commence instructions
	instructions := strings.Split(parts[1], "\n")

	for _, instr := range instructions {
		ins := strings.Split(instr, " ")
		if len(ins) < 6 {
			continue
		}
		numLetters, _ := strconv.Atoi(ins[1])
		source, _ := strconv.Atoi(ins[3])
		dest, _ := strconv.Atoi(ins[5])
		v := stackMap[source-1][:numLetters]
		stackMap[source-1] = append([]string{}, stackMap[source-1][numLetters:]...)
		stackMap[dest-1] = append(v, stackMap[dest-1]...)
	}
	finalStr := ""
	for i := range stackMap {
		finalStr += stackMap[i][0]
	}

	return finalStr
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
	input = `    [D]    
[N] [C]    
[Z] [M] [P]
	1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
`
}
