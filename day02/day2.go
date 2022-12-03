package main

import (
	"flag"
	"fmt"
	"os"

	// "sort"
	// "strconv"
	"strings"
)

var input string
var part int

func RPS(s string) int {
	res := strings.Split(s, " ")
	val := 0
	opp := []rune(res[0])
	you := []rune(res[1])
	opp_val := int(opp[0]) - int(rune('A')) + 1
	you_val := int(you[0]) - int(rune('X')) + 1
	if you_val-opp_val == -1 || you_val%3-opp_val == -1 {
		val = 0 + you_val
	} else if you_val-opp_val == 1 || you_val-opp_val%3 == 1 {
		val = 6 + you_val
	} else {
		val = 3 + you_val
	}
	return val
}

func RPS2(s string) int {
	res := strings.Split(s, " ")
	val := 0
	opp := []rune(res[0])
	you := []rune(res[1])
	opp_val := int(opp[0]) - int(rune('A')) + 1
	you_val := int(you[0]) - int(rune('X')) + 1
	if you_val == 1 {
		if opp_val == 1 {
			opp_val = 4
		}
		val = 0 + opp_val - 1
	} else if you_val == 2 {
		val = 3 + opp_val
	} else if you_val == 3 {
		if opp_val == 3 {
			opp_val = 0
		}
		val = 6 + opp_val + 1
	}
	return val
}

func ComputePart1(s string) int {
	res := strings.Split(s, "\n")
	total := 0
	for _, s := range res {
		if s == "" {
			continue
		}
		total += RPS(s)
	}
	return total
}

func ComputePart2(s string) int {
	res := strings.Split(s, "\n")
	total := 0
	for _, s := range res {
		if s == "" {
			continue
		}
		total += RPS2(s)
	}
	return total
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
	input = `A Y
B X
C Z`
}
