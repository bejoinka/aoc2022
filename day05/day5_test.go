package main

import (
	"testing"
)

type Fxn func(s string) string

func TestDay1(t *testing.T) {
	tests := []struct {
		name     string
		fxn      Fxn
		input    string
		expected string
	}{
		{
			name:     "ComputePart1",
			fxn:      ComputePart1,
			input:    input,
			expected: "CMZ",
		},
		{
			name:     "ComputePart2",
			fxn:      ComputePart2,
			input:    input,
			expected: "MCD",
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			res := tt.fxn(tt.input)
			if res != tt.expected {
				t.Errorf("Part1 = %v, expected %v", res, tt.expected)
			} else {
				t.Logf("PASS: %v, %v", tt.name, tt.expected)
			}
		})
	}
}
