package main

import "fmt"

func main() {
	var num int

	// Prompt the user to enter a number
	fmt.Print("Enter an integer: ")
	// Read the number from the user
	fmt.Scanln(&num)

	// Check if the number is even or odd using the modulo operator
	if num%2 == 0 {
		fmt.Printf("%d is an even number.\n", num)
	} else {
		fmt.Printf("%d is an odd number.\n", num)
	}
}
