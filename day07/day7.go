package main

import (
	"flag"
	"fmt"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

var input string
var part int

type FS struct {
	CurrentDirectory *Directory
	Directories      map[*Directory]bool
}

func (fs FS) GatherValue(d *Directory) int {
	size := d.Size()
	for _, dir_s := range d.Directories {
		dir_p := fs.GetOrMakeDir(d.Dir + dir_s + "/")
		size += fs.GatherValue(dir_p)
	}
	return size
}

func (fs *FS) GetOrMakeDir(s string) *Directory {
	for d := range fs.Directories {
		if s == d.Dir {
			return d
		}
	}
	newDir := makeDirectory(s)
	fs.AddCurrentDirectory(&newDir)
	fs.CurrentDirectory = &newDir
	return &newDir
}

func (fs *FS) AddCurrentDirectory(dir *Directory) {
	fs.Directories[dir] = true
}

func (fs *FS) ParseCommand(s string) {
	if s == "$ ls" {
		return
	}
	var new_dir *Directory
	switch the_dir := s[5:]; the_dir {
	case "/":
		new_dir = fs.GetOrMakeDir("/")
	case "..":
		new_dir_s := regexp.MustCompile("[a-zA-Z]+/$").ReplaceAllString(fs.CurrentDirectory.Dir, "")
		new_dir = fs.GetOrMakeDir(new_dir_s)
	default:
		dir := makeDirectory(fs.CurrentDirectory.Dir + the_dir + "/")
		new_dir = &dir
		fs.Directories[new_dir] = true
	}
	fs.CurrentDirectory = new_dir
}

type Directory struct {
	Dir         string
	Files       []int
	Directories []string
}

func (d Directory) Size() int {
	v := 0
	for _, sz := range d.Files {
		v += sz
	}
	return v
}

func (d *Directory) AddFile(f int) {
	d.Files = append(d.Files, f)
}

func (d *Directory) AddDirectory(dir string) {
	d.Directories = append(d.Directories, dir)
}

func (d *Directory) ParseFileOrDir(s string) {
	split_s := strings.Split(s, " ")
	if split_s[0] == "dir" {
		d.Directories = append(d.Directories, split_s[1])
	} else {
		val, err := strconv.Atoi(split_s[0])
		if err == nil {
			d.Files = append(d.Files, val)
		}
	}
}

func makeDirectory(d string) Directory {
	return Directory{
		Dir:         d,
		Files:       make([]int, 0),
		Directories: make([]string, 0),
	}
}

func (fs *FS) BuildDirectoryTree(lines []string) {
	current := *fs.CurrentDirectory
	fs.Directories[&current] = true
	for _, ln := range lines {
		is_command := strings.Contains(ln, "$")
		if is_command {
			fs.ParseCommand(ln)
		} else {
			fs.CurrentDirectory.ParseFileOrDir(ln)
		}
	}
}

func ComputePart1(s string) int {
	lines := strings.Split(strings.Trim(s, "\n"), "\n")
	current := makeDirectory("/")
	fs := FS{
		CurrentDirectory: &current,
		Directories:      make(map[*Directory]bool, 0),
	}
	fs.BuildDirectoryTree(lines)
	size := 0
	for dir := range fs.Directories {
		val := fs.GatherValue(dir)
		if val < 100000 {
			size += val
		}
	}
	return size
}

func ComputePart2(s string) int {
	lines := strings.Split(strings.Trim(s, "\n"), "\n")
	current := makeDirectory("/")
	fs := FS{
		CurrentDirectory: &current,
		Directories:      make(map[*Directory]bool, 0),
	}
	fs.AddCurrentDirectory(&current)
	fs.BuildDirectoryTree(lines)
	dirs_to_delete := make([]int, 0)
	for dir := range fs.Directories {
		val := fs.GatherValue(dir)
		if val > 8381165 {
			dirs_to_delete = append(dirs_to_delete, val)
		}
	}
	sort.Ints(dirs_to_delete)
	return dirs_to_delete[0]
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
