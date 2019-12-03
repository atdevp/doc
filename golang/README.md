# golang 


## vscode golang 开发环境
### 安装go插件
> commmand+shift+P
Install extensions  选择go版本

### 自动补全和自动倒入包

* 国内用户配置下代理
```
perferences->settings  找到http.proxy,编辑settings.json

{
	"http.proxy": "http://127.0.0.1:9999"
}
```
* command+shift+P ,输入 go:install/update/tools
```
gocode
gopkgs
go-outline
go-symbols
guru
gorename
dlv
godef
godoc
goreturns
golint
gotests
gomodifytags
impl
fillstruct
goplay
```

* 编辑settings.json
```
{
	"go.autocompleteUnimportedPackages": true,
}
```

## 文件操作
### 打开、关闭文件f
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

### Read方法构建切片读取数据
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

### bufio构建reader

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
### Reader的几种读取数据的方法
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

### 全量读取小文件
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

## Goroutine

### sync.WaitGroup 并发控制
```
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
```

### 全局变量控制goroutine


