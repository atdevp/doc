package main

import (
	"fmt"
	"io/ioutil"
)

func main() {
	buf, err := ioutil.ReadFile("/etc/hosts")
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(string(buf))
}
