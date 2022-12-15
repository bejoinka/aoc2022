package main

import (
	"flag"
	"fmt"
	"os"
	"sort"
	"strings"
)

var input string
var input2 string
var part int

type Monkey struct {
	items                   []int
	op                      func(int) int
	divisibleBy             int
	trueMonkey, falseMonkey int //monkey index
}

// func MakeMonkey(s string) Monkey {
// 	lines := strings.Split(s, "\n")
// 	var items []int
// 	items_s := regexp.MustCompile("[0-9]+").FindAllString(lines[1], -1)
// 	for _, itm_s := range items_s {
// 		itm, _ := strconv.Atoi(itm_s)
// 		items = append(items, itm)
// 	}
// 	op_s := regexp.MustCompile(": new = old (?P<op>[+*/-]) (?P<num>[0-9a-zA-Z]+)").FindStringSubmatch(lines[2])
// 	fmt.Println("op:", op_s[1], "num", op_s[2])
// 	eval := goval.NewEvaluator()
// 	vars := map[string]interface{}{
// 		"old": 500,
// 		"op":  op_s[1],
// 		"num": op_s[2],
// 	}
// 	result, _ := eval.Evaluate(`old op num`, vars, nil)
// 	fmt.Println(result)
// 	return Monkey{items, nil, nil}
// }

func (monkey *Monkey) PopLeft() int {
	lst := &monkey.items
	val := (*lst)[0]
	if len(*lst) > 1 {
		*lst = (*lst)[1:]
	} else {
		*lst = []int{}
	}
	return val
}

func ComputePart1(s string) int {
	monkeys_s := strings.Split(s, "\n\n")
	var monkeys []Monkey
	len_monkeys := len(monkeys_s)
	if len_monkeys == 4 {
		monkeys = makeTestMonkeys()
	} else {
		monkeys = makeMonkeys()
	}
	monkey_touches := make([]int, len(monkeys))
	for t := range monkey_touches {
		monkey_touches[t] = 0
	}
	for i := 1; i <= 20; i++ {
		for i := range monkeys {
			for range monkeys[i].items {
				itm := monkeys[i].PopLeft()
				monkey_touches[i]++
				itm = monkeys[i].op(itm)
				itm = itm / 3
				if itm%monkeys[i].divisibleBy == 0 {
					monkeys[monkeys[i].trueMonkey].items = append(monkeys[monkeys[i].trueMonkey].items, itm)
				} else {
					monkeys[monkeys[i].falseMonkey].items = append(monkeys[monkeys[i].falseMonkey].items, itm)
				}
			}
		}
	}
	sort.Ints(monkey_touches)
	return monkey_touches[len_monkeys-1] * monkey_touches[len_monkeys-2]
}

func ComputePart2(s string) int {
	monkeys_s := strings.Split(s, "\n\n")
	var monkeys []Monkey
	len_monkeys := len(monkeys_s)
	if len_monkeys == 4 {
		monkeys = makeTestMonkeys()
	} else {
		monkeys = makeMonkeys()
	}
	bigmod := 1
	for _, m := range monkeys {
		bigmod *= m.divisibleBy
	}
	monkey_touches := make([]int, len(monkeys))
	for t := range monkey_touches {
		monkey_touches[t] = 0
	}
	for i := 1; i <= 10000; i++ {
		for i := range monkeys {
			for range monkeys[i].items {
				itm := monkeys[i].PopLeft()
				monkey_touches[i]++
				itm = monkeys[i].op(itm)
				itm = itm % bigmod
				if itm%monkeys[i].divisibleBy == 0 {
					monkeys[monkeys[i].trueMonkey].items = append(monkeys[monkeys[i].trueMonkey].items, itm)
				} else {
					monkeys[monkeys[i].falseMonkey].items = append(monkeys[monkeys[i].falseMonkey].items, itm)
				}
			}
		}
	}
	sort.Ints(monkey_touches)
	return monkey_touches[len_monkeys-1] * monkey_touches[len_monkeys-2]
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

func makeMonkeys() []Monkey {
	return []Monkey{
		{
			items: []int{98, 89, 52},
			op: func(old int) int {
				return old * 2
			},
			divisibleBy: 5,
			trueMonkey:  6,
			falseMonkey: 1,
		},
		{
			items: []int{57, 95, 80, 92, 57, 78},
			op: func(old int) int {
				return old * 13
			},
			divisibleBy: 2,
			trueMonkey:  2,
			falseMonkey: 6,
		},
		{
			items: []int{82, 74, 97, 75, 51, 92, 83},
			op: func(old int) int {
				return old + 5
			},
			divisibleBy: 19,
			trueMonkey:  7,
			falseMonkey: 5,
		},
		{
			items: []int{97, 88, 51, 68, 76},
			op: func(old int) int {
				return old + 6
			},
			divisibleBy: 7,
			trueMonkey:  0,
			falseMonkey: 4,
		},
		{
			items: []int{63},
			op: func(old int) int {
				return old + 1
			},
			divisibleBy: 17,
			trueMonkey:  0,
			falseMonkey: 1,
		},
		{
			items: []int{94, 91, 51, 63},
			op: func(old int) int {
				return old + 4
			},
			divisibleBy: 13,
			trueMonkey:  4,
			falseMonkey: 3,
		},
		{
			items: []int{61, 54, 94, 71, 74, 68, 98, 83},
			op: func(old int) int {
				return old + 2
			},
			divisibleBy: 3,
			trueMonkey:  2,
			falseMonkey: 7,
		},
		{
			items: []int{90, 56},
			op: func(old int) int {
				return old * old
			},
			divisibleBy: 11,
			trueMonkey:  3,
			falseMonkey: 5,
		},
	}
}

func makeTestMonkeys() []Monkey {
	return []Monkey{
		{
			items: []int{79, 98},
			op: func(old int) int {
				return old * 19
			},
			divisibleBy: 23,
			trueMonkey:  2,
			falseMonkey: 3,
		},
		{
			items: []int{54, 65, 75, 74},
			op: func(old int) int {
				return old + 6
			},
			divisibleBy: 19,
			trueMonkey:  2,
			falseMonkey: 0,
		},
		{
			items: []int{79, 60, 97},
			op: func(old int) int {
				return old * old
			},
			divisibleBy: 13,
			trueMonkey:  1,
			falseMonkey: 3,
		},
		{
			items: []int{74},
			op: func(old int) int {
				return old + 3
			},
			divisibleBy: 17,
			trueMonkey:  0,
			falseMonkey: 1,
		},
	}
}

func init() {
	input = `Monkey 0:
Starting items: 79, 98
Operation: new = old * 19
Test: divisible by 23
	If true: throw to monkey 2
	If false: throw to monkey 3

Monkey 1:
Starting items: 54, 65, 75, 74
Operation: new = old + 6
Test: divisible by 19
	If true: throw to monkey 2
	If false: throw to monkey 0

Monkey 2:
Starting items: 79, 60, 97
Operation: new = old * old
Test: divisible by 13
	If true: throw to monkey 1
	If false: throw to monkey 3

Monkey 3:
Starting items: 74
Operation: new = old + 3
Test: divisible by 17
	If true: throw to monkey 0
	If false: throw to monkey 1
`
}
