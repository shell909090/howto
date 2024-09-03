package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"runtime/pprof"
	"sort"
	"strconv"
	"strings"
	"time"
)

type Item struct {
	data [2]int
}

type Items []Item

func (is Items) Len() int {
	return len(is)
}

func (is Items) Swap(i, j int) {
	is[i], is[j] = is[j], is[i]
}

func (is Items) Less(i, j int) bool {
	return is[i].data[1] < is[j].data[1]
}

func main() {
	var is Items
	var item Item

	time.Sleep(1 * time.Second)

	f, err := os.Open(os.Args[1])
	if err != nil {
		fmt.Println(err)
		return
	}
	defer f.Close()

	stream := bufio.NewReader(f)
	line, err := stream.ReadString('\n')
	for err == nil {
		line = strings.TrimRight(line, "\n")
		fields := strings.Split(line, " ")
		item.data[0], _ = strconv.Atoi(fields[0])
		item.data[1], _ = strconv.Atoi(fields[1])
		is = append(is, item)
		line, err = stream.ReadString('\n')
	}

	sort.Sort(is)

	time.Sleep(10 * time.Second)

	f, err = os.Create("out.perf")
	if err != nil {
		log.Fatal("could not create mem profile: ", err)
	}
	defer f.Close()

	// runtime.GC() // get up-to-date statistics
	if err := pprof.WriteHeapProfile(f); err != nil {
		log.Fatal("could not write memory profile: ", err)
	}
	return
}
