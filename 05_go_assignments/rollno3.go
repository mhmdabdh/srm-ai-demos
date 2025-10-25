package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// EvenOddChecker provides advanced even/odd checking with multiple features
type EvenOddChecker struct {
	processedCount int
	evenCount      int
	oddCount       int
}

// NewChecker creates a new EvenOddChecker instance
func NewChecker() *EvenOddChecker {
	return &EvenOddChecker{}
}

// CheckNumber performs comprehensive even/odd analysis
func (e *EvenOddChecker) CheckNumber(num int) map[string]interface{} {
	e.processedCount++

	result := make(map[string]interface{})
	result["number"] = num

	if num%2 == 0 {
		result["type"] = "Even"
		e.evenCount++
	} else {
		result["type"] = "Odd"
		e.oddCount++
	}

	// Advanced features
	result["divisibleBy3"] = num%3 == 0
	result["divisibleBy5"] = num%5 == 0
	result["isPrime"] = e.isPrime(num)
	result["absolute"] = abs(num)

	return result
}

// isPrime checks if a number is prime
func (e *EvenOddChecker) isPrime(n int) bool {
	if n < 2 {
		return false
	}
	if n == 2 {
		return true
	}
	if n%2 == 0 {
		return false
	}
	for i := 3; i*i <= n; i += 2 {
		if n%i == 0 {
			return false
		}
	}
	return true
}

// GetStatistics returns processing statistics
func (e *EvenOddChecker) GetStatistics() string {
	return fmt.Sprintf("\n--- Statistics ---\nTotal Processed: %d\nEven Numbers: %d\nOdd Numbers: %d\nEven Percentage: %.2f%%",
		e.processedCount, e.evenCount, e.oddCount, float64(e.evenCount)/float64(e.processedCount)*100)
}

// ProcessBatch handles multiple numbers efficiently
func (e *EvenOddChecker) ProcessBatch(numbers []int) []map[string]interface{} {
	results := make([]map[string]interface{}, len(numbers))
	for i, num := range numbers {
		results[i] = e.CheckNumber(num)
	}
	return results
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func main() {
	checker := NewChecker()
	reader := bufio.NewReader(os.Stdin)

	fmt.Println("=== Advanced Even/Odd Checker (Rollno3) ===")
	fmt.Println("Features: Batch processing, Prime detection, Statistics")
	fmt.Println("\nOptions:")
	fmt.Println("1. Single number check")
	fmt.Println("2. Batch processing (comma-separated)")
	fmt.Print("\nEnter choice: ")

	choice, _ := reader.ReadString('\n')
	choice = strings.TrimSpace(choice)

	switch choice {
	case "1":
		fmt.Print("Enter a number: ")
		input, _ := reader.ReadString('\n')
		num, err := strconv.Atoi(strings.TrimSpace(input))
		if err != nil {
			fmt.Println("Invalid number!")
			return
		}

		result := checker.CheckNumber(num)
		fmt.Printf("\n--- Analysis for %d ---\n", num)
		fmt.Printf("Type: %s\n", result["type"])
		fmt.Printf("Divisible by 3: %v\n", result["divisibleBy3"])
		fmt.Printf("Divisible by 5: %v\n", result["divisibleBy5"])
		fmt.Printf("Is Prime: %v\n", result["isPrime"])
		fmt.Printf("Absolute Value: %d\n", result["absolute"])

	case "2":
		fmt.Print("Enter numbers (comma-separated): ")
		input, _ := reader.ReadString('\n')
		parts := strings.Split(strings.TrimSpace(input), ",")

		var numbers []int
		for _, p := range parts {
			num, err := strconv.Atoi(strings.TrimSpace(p))
			if err != nil {
				fmt.Printf("Skipping invalid input: %s\n", p)
				continue
			}
			numbers = append(numbers, num)
		}

		results := checker.ProcessBatch(numbers)
		fmt.Println("\n--- Batch Results ---")
		for _, r := range results {
			fmt.Printf("%d: %s (Prime: %v)\n", r["number"], r["type"], r["isPrime"])
		}

	default:
		fmt.Println("Invalid choice!")
		return
	}

	fmt.Println(checker.GetStatistics())
}
