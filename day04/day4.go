package main

import (
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"

	"golang.org/x/exp/maps"
)

var input string
var part int

func makeRange(s string) map[int]bool {
	nums := strings.Split(s, "-")
	num1, _ := strconv.Atoi(nums[0])
	num2, _ := strconv.Atoi(nums[1])
	rng := make(map[int]bool, 0)
	for i := num1; i <= num2; i++ {
		rng[i] = true
	}
	return rng
}

func ComputePart1(s string) int {
	fullyContainedPairs := 0
	for _, ln := range strings.Split(s, "\n") {
		if len(ln) == 0 {
			continue
		}
		parts := strings.Split(ln, ",")
		combined := makeRange(parts[0])
		maps.Copy(combined, makeRange(parts[1]))
		if len(combined) == len(makeRange(parts[0])) || len(combined) == len(makeRange(parts[1])) {
			fullyContainedPairs += 1
		}
	}
	return fullyContainedPairs
}

func ComputePart2(s string) int {
	partiallyContainedRanges := 0
	for _, ln := range strings.Split(s, "\n") {
		if len(ln) == 0 {
			continue
		}
		parts := strings.Split(ln, ",")
		combined := makeRange(parts[0])
		maps.Copy(combined, makeRange(parts[1]))
		if len(combined) < (len(makeRange(parts[0])) + len(makeRange(parts[1]))) {
			partiallyContainedRanges += 1
		}
	}
	return partiallyContainedRanges
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
	input = `2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
`
}
