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

func sumChars(strs []string) int {
	total := 0
	for _, c := range strs {
		runes := []rune(c)
		if c == strings.ToUpper(c) {
			total += int(runes[0]) - int('A') + 27
		} else {
			total += int(runes[0]) - int('a') + 1
		}
	}
	return total
}

func calcLine(s string) int {
	vals := strings.Split(s, "")
	mid := int(len(vals) / 2)
	left := make(map[string]bool)
	right := make(map[string]bool)
	chars := make([]string, 0)
	for i, s := range vals {
		if i < mid {
			left[s] = true
		} else {
			right[s] = true
		}
	}
	for k := range left {
		if right[k] {
			chars = append(chars, k)
		}
	}
	return sumChars(chars)
}

func calcThreeLines(strs []string) int {
	goal := len(strs)
	if goal == 0 {
		return 0
	}
	chars := make([]string, 0)
	hashes := make([]map[string]bool, goal)
	for i := range hashes {
		hashes[i] = make(map[string]bool, 0)
	}
	for i, s := range strs {
		for _, k := range strings.Split(s, "") {
			hashes[i][k] = true
		}
	}
	for char := range hashes[0] {
		v := 0
		for _, h := range hashes {
			if h[char] {
				v += 1
			}
		}
		if v == goal {
			chars = append(chars, char)
		}
	}
	return sumChars(chars)
}

func ComputePart1(s string) int {
	res := strings.Split(s, "\n")
	total := 0
	for _, s := range res[:len(res)-1] {
		if s == "" {
			continue
		}
		total += calcLine(s)
	}
	return total
}

func ComputePart2(s string) int {
	res := strings.Split(s, "\n")
	total := 0
	badges := make([]string, 0)
	for i, s := range res[:len(res)-1] {
		if s == "" {
			continue
		}
		if i%3 == 2 {
			badges = append(badges, s)
			total += calcThreeLines(badges)
			badges = make([]string, 0)
		} else {
			badges = append(badges, s)
		}
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
	input = `vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
`
}
