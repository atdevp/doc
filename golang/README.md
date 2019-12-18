# golang 
<!-- TOC -->

- [golang](#golang)
    - [vscode golang 开发环境](#vscode-golang-开发环境)
        - [安装go插件](#安装go插件)
        - [自动补全和自动倒入包](#自动补全和自动倒入包)
    - [文件操作](#文件操作)
        - [打开、关闭文件f](#打开关闭文件f)
        - [Read方法构建切片读取数据](#read方法构建切片读取数据)
        - [bufio构建reader](#bufio构建reader)
        - [Reader的几种读取数据的方法](#reader的几种读取数据的方法)
        - [全量读取小文件](#全量读取小文件)
    - [Goroutine](#goroutine)
        - [sync.WaitGroup 并发控制](#syncwaitgroup-并发控制)
    - [golang数据类型](#golang数据类型)
        - [数组](#数组)
            - [数组声明](#数组声明)
            - [初始化数组](#初始化数组)
            - [遍历数组](#遍历数组)
        - [切片](#切片)
            - [切片声明](#切片声明)
            - [初始化切片](#初始化切片)
            - [make函数构造切片](#make函数构造切片)
            - [append函数添加元素至切片](#append函数添加元素至切片)
            - [切片复制](#切片复制)
            - [切片遍历](#切片遍历)
        - [map](#map)
            - [map声明](#map声明)
            - [make函数构建map](#make函数构建map)
            - [map赋值](#map赋值)
            - [map取值](#map取值)
            - [判断key是否存在](#判断key是否存在)
            - [删除map中指定key](#删除map中指定key)
            - [遍历map](#遍历map)
            - [清空map](#清空map)

<!-- /TOC -->

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

## golang数据类型

### 数组
```
数据是一段固定长度的内存区域，在go语言中数组从声明中就确定，使用时可以修改数组成员，但是数组大小不可改变。
``` 
#### 数组声明
```
var 变量名 [元素数量]元素类型
元素数量：可以是一个表达式，最终结果是个整型数值
元素类型：任意基本类型，可以是数组类型《实现多维数组》
var person [3]string
person[0] = "aname"
person[1] = "bname"
person[2] = "cname"
```
#### 初始化数组
```
指定个数：
var person = [3]string{"aname", "bname", "cname"}

未知个数：
var person = [...]string{"aname", "bname", "cname"}
... 表示让编译器确定数组大小，上面例子，编译器会自动为这个数组设置元素个数为3。

```

#### 遍历数组
```
package main

import "fmt"

func main() {
    var person = [...]string{"aname", "bname", "cname"}
    for k, v := range person {
        fmt.Println(k, v)
    }
}

输出：
0 aname
1 bname
2 cname
```

### 切片
```
动态分配大小的连续空间，在内存中和数组一样都是连续地址空间。
```
#### 切片声明
```
var 变量名  []元素类型
var person []string
```

#### 初始化切片
```
var person = []string{}
```

#### make函数构造切片
```
make([]T, size, cap)
T: 切片的元素类型
size: 分配多少个元素
cap: 预分配的元素数量，提前分配空间，可以降低日后多次分配空间带来的性能问题

num := make([]int, 0, 100)
```

#### append函数添加元素至切片
```
var person = make([]string, 0, 10)
person = append(person, "aname")
person = append(person, "bname")
person = append(person, "cname")

```

#### 切片复制
```
package main

import "fmt"

func main() {
    var a = make([]int, 0, 2000000)
    for i := 1; i <= 2000000; i++ {
        a = append(a, i)
    }
    var b = make([]int, len(a))
    copy(b, a)
    fmt.Println(b)
}
```

#### 切片遍历
```
package main

import "fmt"

func main() {
    var a = make([]int, 0, 10)
    for i := 1; i <= 10; i++ {
        a = append(a, i)
    }
    for k, v := range a {
        fmt.Println(k, v)
    }
}

输出：
0 1
1 2
2 3
3 4
4 5
5 6
6 7
7 8
8 9
9 10
```

### map
```
golang中的map使用散列表hash实现，大多数域名中映射关系容器使用的是两种算法，散列表和平衡树。
```
#### map声明
```
var person map[string]string
```
#### make函数构建map
```
var person = make(map[string]string)
person := make(map[string]string)
```

#### map赋值
```
person := make(map[string]string)
person["a"] = "www.a.com"
person["b"] = "www.b.com"
```

#### map取值
```
a_url := person["a"]
```

#### 判断key是否存在
```
func exist() bool {
	if v, ok := person["a"]; ok {
		return true
	}
	return false
}

```

#### 删除map中指定key
```
Usage： delete(map, key)

package main

import (
	"fmt"
	"os"
)

func main() {
	var s1 = make([]int, 0, 10)
	for i := 0; i < 10; i++ {
		s1 = append(s1, i)
	}

	m := make(map[int]string)
	for idx, v := range s1 {
		m[idx] = fmt.Sprintf("%s-%d", "str", v)
	}

	fmt.Fprintln(os.Stdout, "del before: ", m)
	delete(m, 9)
	fmt.Fprintln(os.Stdout, "del after : ", m)

}
输出：
del before:  map[0:str-0 1:str-1 2:str-2 3:str-3 4:str-4 5:str-5 6:str-6 7:str-7 8:str-8 9:str-9]
del after :  map[0:str-0 1:str-1 2:str-2 3:str-3 4:str-4 5:str-5 6:str-6 7:str-7 8:str-8]
```

#### 遍历map
```
package main

import (
    "fmt"
    "os"
)

func main() {
    var p = make(map[string]int)
    p["a"] = 1
    p["b"] = 2
    for k, v := range p {
        fmt.Fprintln(os.Stdout, k, v)
    }
}
```

#### 清空map
```
go语言中没有提供任何清空所有元素的函数和方法。清空map的唯一办法是重新make一个新的map。不用担心垃圾回收的效率，因为效率很高。
```



