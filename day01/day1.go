package main

import (
	"flag"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

var input string

func sum(arr []int) int {
	tot := 0
	for _, s := range arr {
		tot += s
	}
	return tot
}

func SortedList(res []string) []int {
	elves := []int{}
	var total int
	for _, s := range res {
		if s == "" {
			elves = append(elves, total)
			total = 0
		}
		val, _ := strconv.Atoi(s)
		total += val
	}
	sort.Slice(elves, func(i, j int) bool {
		return elves[i] > elves[j]
	})
	return elves
}

func ComputePart1(s string) int {
	res := strings.Split(s, "\n")
	elves := SortedList(res)
	return elves[0]
}

func ComputePart2(s string) int {
	res := strings.Split(s, "\n")
	elves := SortedList(res)
	return sum(elves[0:3])
}

func main() {
	var part int
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
	input = `
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
`
}
