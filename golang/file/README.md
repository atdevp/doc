# golang 文件操作

<!-- TOC -->

- [golang 文件操作](#golang-%e6%96%87%e4%bb%b6%e6%93%8d%e4%bd%9c)
	- [打开、关闭文件f](#%e6%89%93%e5%bc%80%e5%85%b3%e9%97%ad%e6%96%87%e4%bb%b6f)
	- [Read方法构建切片读取数据](#read%e6%96%b9%e6%b3%95%e6%9e%84%e5%bb%ba%e5%88%87%e7%89%87%e8%af%bb%e5%8f%96%e6%95%b0%e6%8d%ae)
	- [bufio构建reader](#bufio%e6%9e%84%e5%bb%bareader)
	- [Reader的几种读取数据的方法](#reader%e7%9a%84%e5%87%a0%e7%a7%8d%e8%af%bb%e5%8f%96%e6%95%b0%e6%8d%ae%e7%9a%84%e6%96%b9%e6%b3%95)
	- [全量读取小文件](#%e5%85%a8%e9%87%8f%e8%af%bb%e5%8f%96%e5%b0%8f%e6%96%87%e4%bb%b6)

<!-- /TOC -->


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

## Read方法构建切片读取数据
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

	// 构建一个切片,使用read方法读取数据
	var content []byte
	var buf = make([]byte, 1)
	for {
		n, err := f.Read(buf)
		if err == io.EOF {
			fmt.Println("读完了")
			break
		}
		if err != nil {
			fmt.Println(err)
			return
		}
		content = append(content, buf[:n]...)
	}
	fmt.Println(string(content))
}
```

## bufio构建reader

```
package main
import (
	"bufio"
	"os"
	"fmt"
)

func main() {
	f, err := os.Open("doc.md")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer f.Close()

	reader = bufio.NewReader(f)
}

``` 
## Reader的几种读取数据的方法
以下方法读取文件类似，后三种都是调用ReadSlice实现。

* ReadSlice
  ```
  for {
		buf, err := reader.ReadSlice('\n')
		if err != nil {
			fmt.Println(err)
			return
		}
		if err == io.EOF {
			fmt.Println("读完了")
			break
		}
		sbuf := string(buf)
		fmt.Println(strings.Split(sbuf, "\n")[0])
	}
  ```

* ReadBytes
  ```
  for {
		buf, err := reader.ReadBytes('\n')
		if err != nil {
			fmt.Println(err)
			return
		}
		if err == io.EOF {
			fmt.Println("读完了")
			break
		}
		sbuf := string(buf)
		fmt.Println(strings.Split(sbuf, "\n")[0])
	}
  ```
* ReadLine
  ```
   一般不用这个，为啥呢？
   readline方法有3个返回值，line， isPrefix, err，不是使用ReadSlice实现的。当一条数据很大时，就会被切割分割成两次或者多次传输，isPrefix为true时代表切割了，第二次传输剩下的数据。这里不再演示；
  
  ```
* ReadString
  ```
  for {
		buf, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println(err)
			return
		}
		if err == io.EOF {
			fmt.Println("读完了")
			break
		}
		sbuf := string(buf)
		fmt.Println(strings.Split(sbuf, "\n")[0])
	}
  ```

## 全量读取小文件
```
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
```

