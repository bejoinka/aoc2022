package main

import (
	"errors"
	"flag"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

var input string
var input2 string
var part int

type Register struct {
	val          int
	cycles       int
	instructions []string
	current_op   int
}

func (register *Register) ProcessOp() (int, int, error) {
	register.current_op++
	if register.current_op == len(register.instructions) {
		// shut it down!
		return 0, 0, nil
	}
	instr := register.instructions[register.current_op]
	if instr == "noop" {
		return 1, 0, nil
	} else if regexp.MustCompile("addx").MatchString(instr) {
		register_change, _ := strconv.Atoi(strings.Split(instr, " ")[1])
		return 2, register_change, nil
	} else {
		return 0, 0, errors.New("not processing op correctly")
	}
}

func ComputePart1(s string) int {
	instructions := strings.Split(s, "\n")
	register := Register{1, 220, instructions, -1}
	countdown := 0
	var value_change int
	var err error
	sum_signal_strength := 0
	for c := 1; c <= register.cycles; c++ {
		if countdown == 0 {
			countdown, value_change, err = register.ProcessOp()
			if err != nil {
				panic(err)
			}
		}
		if c%40 == 20 {
			sum_signal_strength += c * register.val
			fmt.Println("cycle", c, "register", register.val, "signal strength", c*register.val)
		}
		countdown--
		if countdown == 0 {
			register.val += value_change
			value_change = 0
		}
	}
	return sum_signal_strength
}

func ComputePart2(s string) int {
	instructions := strings.Split(s, "\n")
	register := Register{1, 240, instructions, -1}
	countdown := 0
	var value_change int
	var err error
	crt := ""
	for c := 0; c < register.cycles; c++ {
		if countdown == 0 {
			countdown, value_change, err = register.ProcessOp()
			if err != nil {
				panic(err)
			}
		}
		x := c % 40
		if x == 0 {
			crt += "\n"
		}
		if x >= register.val-1 && x <= register.val+1 {
			crt += "#"
		} else {
			crt += " "
		}
		countdown--
		if countdown == 0 {
			register.val += value_change
			value_change = 0
		}
	}
	fmt.Println(strings.Trim(crt, "\n"))
	return 0
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
	input = `addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
`
}
