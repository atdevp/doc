package main

import (
	"fmt"
	"io"
	"os"
)

func main() {
	f, err := os.Open("doc.md")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer f.Close()

	for {
		var buf = make([]byte, 1)
		offset, err := f.Read(buf)
		if err != nil {
			fmt.Println(err)
			return
		}
		fmt.Printf(string(buf[:offset]))
		if err == io.EOF {
			fmt.Println("读完了")
			break
		}
	}

}
