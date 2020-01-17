# Redis
<!-- TOC -->

- [Redis](#redis)
  - [Redis常见数据结构使用方法](#redis%e5%b8%b8%e8%a7%81%e6%95%b0%e6%8d%ae%e7%bb%93%e6%9e%84%e4%bd%bf%e7%94%a8%e6%96%b9%e6%b3%95)
  - [缓存策略](#%e7%bc%93%e5%ad%98%e7%ad%96%e7%95%a5)
  - [Redis不同数据类型的操作](#redis%e4%b8%8d%e5%90%8c%e6%95%b0%e6%8d%ae%e7%b1%bb%e5%9e%8b%e7%9a%84%e6%93%8d%e4%bd%9c)
    - [string类型](#string%e7%b1%bb%e5%9e%8b)
    - [list类型](#list%e7%b1%bb%e5%9e%8b)
    - [hash类型](#hash%e7%b1%bb%e5%9e%8b)
  - [Redis使用场景](#redis%e4%bd%bf%e7%94%a8%e5%9c%ba%e6%99%af)
    - [分布式锁](#%e5%88%86%e5%b8%83%e5%bc%8f%e9%94%81)
    - [FIFO队列](#fifo%e9%98%9f%e5%88%97)

<!-- /TOC -->
## Redis常见数据结构使用方法
1. String
> 常用命令 set、get、decr、incr、mget
2. Hash
> 常用命令 hset、hget、hgetall
3. List
> 常用命令 lpush、rpush、lpop、lrange
4. Set
> 常用命令 sadd、spop、smembers、sunion
5. SortList
> 常用命令 zadd、zrange、zrem、zcard

## 缓存策略
1. volatile-lru
> 从已设置过期的数据集中删除最近最少使用的key
2. volatile-ttl
> 从已设置过期的数据集中调出快要过期的key
3. volatile-random
> 从已设置过期的数据集中随机删除一个key
4. allkeys-lru
> 从所有的数据集中挑选出最近最少使用的key
5. allkeys-random
> 从所有的数据集中随机删除某个key
6. no-enviction 
> 禁止数据驱逐

## Redis不同数据类型的操作
### string类型

```



```

### list类型
> 一个列表最多能放2^32 - 1个元素（40亿多） 
```
# 列表左侧插入
lpush(key, v1,v2,v3,)
rpush(key, v1,v2,v3,)

# 已有列表中插入,若key不存在，则返回false
lpushx(key, v1) 
rpushx(key, v1)

# 列表右侧插入
rpop(key) 右取
lpop(key) 左取

# 列表长度 
llen(key) 

# 获取区间元素 
lrange(key, start, end) 

# 读旧右插新左
lpush("a", 1,2,3,4,5,)
rpoplpush("a", "b")
lpop("b") => 5 4 3 2 1
rpop("b") => 1 2 3 4 5
```

### hash类型
```
key = "article:newsid"

# 单个字段写入数据
hset(key, "title", "新闻标题")
hset(key, "image", "新闻图片")

# 获取散列表中指定字段的值
hget(key, "title")

# 获取散列表中指定key的所有字段和值
hgetall(key) => {'title': '新闻标题', 'content': '新闻内容', 'image': '新闻图片'}

# 判断散列表中指定key的某个字段是否存在
hexists(key, "title") => bool

# 对散列表中的指定可以的指定字段指定增量值
c.hset(key, "number", "10")
c.hincrby(key, "number", amount=2)
c.hget(key, "number") => 12
c.hincrbyfloat(key, "number", amount=1.2)
c.hget(key, "number") => 13.2

# 获取散列表中指定key的所有字段名称
c.hkeys(key) => ['title', 'content', 'image', 'number']

# 获取散列表中指定key的所有字段数量
c.hlen(key) => 4

# 获取多个字段


# 多个字段写入

```




## Redis使用场景
### 分布式锁
```
import redis

class RedisClient:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.socket_timeout = 5


    def new(self):
        return redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            socket_timeout=self.socket_timeout,
            decode_responses=True
        )


class LOCK:
    def __init__(self, client, key):
        self.c = client
        self.k = key
        self.v = "locking"
    
    def acquire(self):
        return self.c.set(self.k, self.v, nx=True)

    def release(self):
        return self.c.delete(self.k) == 1

def main():
    ip = "localhost"
    port = 8765
    password = "123456"
    rds = RedisClient(ip, port, password)    
    c = rds.new()

    lock = LOCK(c, "test")

    # delete lock
    print("1 del lock: ", lock.release())

    # get lock
    print("1 get lock: ", lock.acquire())

    print("2 get lock: ", lock.acquire())

    print("3 get lock: ", lock.acquire())


main()

```

### FIFO队列
```
# coding: utf-8
import redis
import threading
import sys
import time

class RedisClient:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.socket_timeout = None


    def new(self):
        return redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            socket_timeout=self.socket_timeout,
            decode_responses=True
        )


class Popthread(threading.Thread):
    def __init__(self, client, key, timeout=0):
        threading.Thread.__init__(self)
        self.c = client
        self.k = key
        self.t = timeout
    
    def run(self):
        while True:
            v = self.c.brpop(self.k, self.t)
            print(v)

class PushThread(threading.Thread):
    def __init__(self, client, key):
        threading.Thread.__init__(self)
        self.c = client
        self.k = key
    
    def run(self):
        while True:
            for i in range(10):
                self.c.lpush(self.k, i)
                time.sleep(1)
                if i == 9:
                    return

def main():
    ip = "localhost"
    port = 8765
    password = "123456"
    rds = RedisClient(ip, port, password)    
    c = rds.new()

    key = "key_list"
    t1 = PushThread(c, key)
    t1.start()
    
    t2 = Popthread(c, key)
    t2.start()

    if t1.isAlive():
        t1.join()
    
    if t2.isAlive():
        t2.join()

main()

```
