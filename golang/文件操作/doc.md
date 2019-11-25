# golang 文件操作

## 打开、关闭文件f
```
package main

import (
	"fmt"
	"os"
)

func main() {
	f, err := os.Open("doc.md")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer f.Close()
}
```

## f.Read()
#### func (f *File) Read(b []byte) (n int, err error)
```
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

```
