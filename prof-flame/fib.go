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
	// f, err := os.Create("out.perf")
	// if err != nil {
	// 	log.Fatal("could not create CPU profile: ", err)
	// }
	// defer f.Close()

	// if err := pprof.StartCPUProfile(f); err != nil {
	// 	log.Fatal("could not start CPU profile: ", err)
	// }
	// defer pprof.StopCPUProfile()

	n := 45
	fmt.Printf("fib(%d) = %d\n", n, fib(n))

	return
}
