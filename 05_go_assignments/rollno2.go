package main

import (
	"fmt"
	"math/big"
)

func main() {
	var input string

	// Prompt the user to enter a number
	fmt.Print("Enter an integer (up to 50 digits): ")
	// Read the number as a string to handle large numbers
	fmt.Scanln(&input)

	// Create a big.Int to handle large numbers
	num := new(big.Int)

	// Parse the input string as a big integer
	_, success := num.SetString(input, 10)
	if !success {
		fmt.Println("Invalid input! Please enter a valid integer.")
		return
	}

	// Check if the number is even or odd using bitwise AND with 1
	// If the least significant bit is 0, the number is even
	if num.Bit(0) == 0 {
		fmt.Printf("%s is an even number.\n", input)
	} else {
		fmt.Printf("%s is an odd number.\n", input)
	}
}
