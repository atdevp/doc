package main

import (
	"fmt"
	"os"
	"time"
)

var running bool
running = true

func say(n int, f *os.File) {
	for running {
		fmt.Fprintf(f, "I am sub_thread: %d\n", n)
	}

}

func main() {

	f, err := os.OpenFile("run.log", os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Fprint(f, err.Error())
		return
	}
	defer f.Close()

	for i := 0; i <= 1000; i++ {
		go say(i, f)
	}
	time.Sleep(time.Second * 3)
	running = false
	time.Sleep(time.Second * 3)
	fmt.Fprintln(f, "parent thread finish")
}
