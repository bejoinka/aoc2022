package support

import (
	"math"
)

func AbsInt(x int) int {
	return int(math.Abs(float64(x)))
}

type Coord struct {
	X int
	Y int
}

func DiffCoord(coord1 Coord, coord2 Coord) Coord {
	return Coord{
		X: coord1.X - coord2.X,
		Y: coord1.Y - coord2.Y,
	}
}

func AddCoord(coord Coord, dif Coord) Coord {
	return Coord{coord.X + dif.X, coord.Y + dif.Y}
}

func AvgCoord(coord1 Coord, coord2 Coord) Coord {
	return Coord{
		X: int((coord1.X + coord2.X) / 2),
		Y: int((coord1.Y + coord2.Y) / 2),
	}
}

func Directions() []Coord {
	return []Coord{
		{X: 0, Y: -1}, // up
		{X: 1, Y: 0},  // right
		{X: 0, Y: 1},  // down
		{X: -1, Y: 0}, // left
	}
}
