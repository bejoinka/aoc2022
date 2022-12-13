package main

import (
	"flag"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

var input string
var part int

func GatherValue(dir string, dirs map[string]int) int {
	size := dirs[dir]
	// fmt.Println(dir, size)
	for subdir := range dirs {
		re := regexp.MustCompile(dir + "[[:alpha:]]+")
		if re.MatchString(subdir) {
			// if strings.Contains(subdir, dir+"/") {
			new_val := GatherValue(subdir, dirs)
			size += new_val
		}
	}
	if size > 100000 {
		return 0
	}
	return size
}

type FS struct {
	CurrentDirectory *Directory
	Directories      []Directory
}

func (fs FS) GetOrMakeDir(s string) *Directory {
	for _, d := range fs.Directories {
		if d.Dir == d.Dir {
			return &d
		}
	}
	newDir := makeDirectory(s)
	fs.Directories = append(fs.Directories, newDir)
	return &newDir
}

func (fs FS) ParseCommand(d Directory, s string) *Directory {
	if s == "$ ls" {
		return &d
	}
	var new_dir string
	repl := regexp.MustCompile("//")
	switch the_dir := s[5:]; the_dir {
	case "/":
		return fs.GetOrMakeDir("/")
	case "..":
		re := regexp.MustCompile("[a-zA-Z]+/$")
		new_dir = re.ReplaceAllString(d.Dir, "")
	default:
		new_dir = d.Dir + "/" + the_dir
	}

	dir := fs.GetOrMakeDir(repl.ReplaceAllString(new_dir, "/"))
	fmt.Println("old dir", d.Dir, "new dir", dir)
	return dir
}

type Directory struct {
	Dir         string
	Files       []int
	Directories []string
}

func (d Directory) Size() int {
	v := 0
	for sz := range d.Files {
		v += sz
	}
	return v
}
func (d Directory) Subdirectories() []string {
	dirs := make([]string, 0)
	for _, ds := range d.Directories {
		new_dir := d.Dir + "/" + ds
		repl := regexp.MustCompile("//")
		dirs = append(dirs, repl.ReplaceAllString(new_dir, "/"))
	}
	return dirs
}
func makeDirectory(d string) Directory {
	return Directory{
		Dir:         d,
		Files:       make([]int, 0),
		Directories: make([]string, 0),
	}
}

func ParseFileOrDir(s string) int {
	split_s := strings.Split(s, " ")
	if split_s[0] == "dir" {
		return 0
	}
	val, err := strconv.Atoi(split_s[0])
	if err != nil {
		fmt.Println(err)
		fmt.Println(s)
		return 0
	}
	return val
}

func ComputePart1(s string) int {
	lines := strings.Split(strings.Trim(s, "\n"), "\n")
	current := makeDirectory("/")
	fs := FS{
		CurrentDirectory: &current,
		Directories:      append(make([]Directory, 0), current),
	}
	// dirs = append(dirs, current)
	for _, ln := range lines {
		is_command := strings.Contains(ln, "$")
		if is_command {
			current_dir, _ = fs.ParseCommand(current, ln)
		} else {
			val_to_add := ParseFileOrDir(ln)
			dirs[current_dir] += val_to_add
		}
	}
	size := 0
	for dir := range dirs {
		size += GatherValue(dir, dirs)
	}
	return size
}

func ComputePart2(s string) int {
	// str := strings.Split(s, "\n")[0]

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
	input = `$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k	
`
}
