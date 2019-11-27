package main

import (
	"fmt"
	"sync"
	"time"
)

func say(n int, wg *sync.WaitGroup) {
	fmt.Printf("I am %d\n", n)
	time.Sleep(time.Second * 1)
	wg.Done()

}

func main() {
	var wg sync.WaitGroup
	for i := 0; i <= 1000; i++ {
		go say(i, &wg)
		wg.Add(1)
	}
	wg.Wait()
	fmt.Println("say task finish")
}
