package main

import (
	"flag"
	"fmt"
	"os"
	"strings"
)

var input string
var part int

func ComputePart1(s string) int {
	str := strings.Split(s, "\n")[0]
	hash := make(map[string]int, 0)
	for i := range str {
		if i < 3 {
			continue
		}
		for j := i - 3; j <= i; j++ {
			fmt.Println("i", i, "j", j, "str[j]", string(str[j]))
			hash[string(str[j])] = 1
		}
		if len(hash) == 4 {
			return i + 1
		} else {
			hash = make(map[string]int, 0)
		}
	}
	return 0
}

func ComputePart2(s string) int {
	str := strings.Split(s, "\n")[0]
	hash := make(map[string]int, 0)
	for i := range str {
		if i < 13 {
			continue
		}
		for j := i - 13; j <= i; j++ {
			fmt.Println("i", i, "j", j, "str[j]", string(str[j]))
			hash[string(str[j])] = 1
		}
		if len(hash) == 14 {
			return i + 1
		} else {
			hash = make(map[string]int, 0)
		}
	}
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
	input = `mjqjpqmgbljsphdztnvjfqwrcgsmlb
`
}
