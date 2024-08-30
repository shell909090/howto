package main

import (
	"fmt"
)

func fib(n int) (r int) {
	if n <= 0 {
		return 0
	}
	if n <= 2 {
		return 1
	}
	return fib(n-1) + fib(n-2)

}

func main() {
	n := 20
	fmt.Printf("fib(%d) = %d\n", n, fib(n))

	return
}
