package support

type Coord struct {
	X int
	Y int
}

func Directions() []Coord {
	return []Coord{
		{X: 0, Y: -1}, // up
		{X: 1, Y: 0},  // right
		{X: 0, Y: 1},  // down
		{X: -1, Y: 0}, // left
	}
}
